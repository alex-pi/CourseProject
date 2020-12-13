import scrapy
import re
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from scrapy import signals
from urlclassification import url_classification as uc
from scrapy.exporters import CsvItemExporter
from globals import get_data_paths
from globals import crawler_settings as settings
from pathlib import Path


class LinkSpider(scrapy.Spider):
    name = 'links'

    def __init__(self, *args, **kwargs):

        self.start_url = kwargs['start_urls'][0]
        self.data_paths = get_data_paths(self.start_url)
        self.main_domain = [self.data_paths['domain']]
        self.start_urls = [self.data_paths['base_url']]
        kwargs['start_urls'] = self.start_urls
        self.max_to_scrap = int(kwargs.get('max_to_scrap', 10))
        print(f'Start url: {self.start_urls[0]}, Domain: {self.main_domain}, Max to positives: {self.max_to_scrap}')

        #self.exported_data_path = os.path.join(DATA_OUTPUT_PATH, domain)
        #elf.main_domain = kwargs.get('main_domain')
        self.num_scraped = 0
        self.link_extractor = LinkExtractor(allow_domains=self.main_domain)
        super(LinkSpider, self).__init__(*args, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(LinkSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        return spider

    def item_scraped(self, item):
        self.num_scraped = self.num_scraped + 1

    #def closed(self, reason):
    #    Path(self.data_paths['done']).touch()

    def parse(self, response):
        if self.num_scraped >= self.max_to_scrap:
            # Stop yielding request and items to stop the crawling
            return
        depth = response.meta['depth']
        print(f'current url: {response.url}, depth: {depth}')
        headers = response.headers
        # print(headers['Content-Type'])
        if 'text/html' in str(headers.get('Content-Type', '')):
            # Link extractor by default avoids most extensions
            # but sometimes extensions are not part of the URL
            # For now I put all under this if, but a better way is to
            # implement a Download Middleware (way to go is add more logic to avoid certain content)
            extracted_links = self.link_extractor.extract_links(response)
            for link in extracted_links:
                item = LinkItem()
                item['link'] = link.url
                item['text'] = re.sub(r'\s+', ' ', link.text)
                item['depth'] = depth
                yield item
                # print(f'extracted_link: {link.url}, text: {link.text}')
                # Here we can add more conditions to discard URLs we don't want
                # explore further.
                yield scrapy.Request(
                    response.urljoin(link.url),
                    callback=self.parse)


class ClassificationPipeline:

    def __init__(self):
        self.classifier = uc.ulr_faculty_classification()
        self.classifier.SVM_Classification()

    # We can make this async
    def process_item(self, item, spider):
        # print(f"Classifying URL: {item['link']}")

        result = self.classifier.SVM_Predict(item['link'])
        item['label'] = result[0]
        # if result != 0:
        #     print(f"Found candidate: {item['link']}")
        # else:
        #     print(f"{item!r} is not a candidate")
        return item


class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['link'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['link'])
            return item


class LinkItemExporterPipeline2:

    def __init__(self):
        self.batch = list()
        self.batch_all = list()
        self.exported = False

    #def open_spider(self, spider):
        #f = open(spider.data_paths['positive_data_path'], 'wb')
        #f.close()

    def process_item(self, item, spider):
        if self.exported:
            raise DropItem(f"{item!r} dropped, num URLs reached")
        if spider.num_scraped < spider.max_to_scrap:
            self.batch_all.append(item)
            if item['label'] != 0:
                print(f"Found candidate: {item['link']}")
                self.batch.append(item)
                return item
            else:
                raise DropItem(f"{item!r} is not a candidate")
        elif not self.exported:
            self.exported = True
            with open(spider.data_paths['positive_data_path'], "w", encoding="utf-8") as f:
                for it in self.batch:
                    f.write(f"{it['label']},{it['depth']},{it['link']},{it['text']}\n")
                f.flush()
                self.batch.clear()
            with open(spider.data_paths['all_data_path'], "w", encoding="utf-8") as f:
                for it in self.batch_all:
                    f.write(f"{it['label']},{it['depth']},{it['link']},{it['text']}\n")
                f.flush()
                self.batch_all.clear()
            Path(spider.data_paths['done']).touch()



class LinkItemExporterPipeline:

    def open_spider(self, spider):
        f = open(spider.data_paths['all_data_path'], 'wb')
        self.f2 = open(spider.data_paths['positive_data_path'], 'wb')
        self.exporter_all = CsvItemExporter(f)
        self.exporter_all.start_exporting()
        self.exporter_pos = CsvItemExporter(self.f2)
        self.exporter_pos.start_exporting()
        self.finished = False

    #def close_spider(self, spider):
    #    self.exporter_all.finish_exporting()
    #    self.exporter_pos.finish_exporting()

    def process_item(self, item, spider):
        if spider.num_scraped >= spider.max_to_scrap and not self.finished:
            self.exporter_all.finish_exporting()
            self.exporter_pos.finish_exporting()
            self.finished = True
            self.f2.flush()
            raise DropItem(f"Dropping {item!r}, we had enough")

        self.exporter_all.export_item(item)
        if item['label'] != 0:
            print(f"Found candidate: {item['link']}")
            self.exporter_pos.export_item(item)
            return item
        else:
            raise DropItem(f"{item!r} is not a candidate")


class LinkItem(scrapy.Item):
    link = scrapy.Field()
    text = scrapy.Field()
    depth = scrapy.Field()
    label = scrapy.Field()

def start(base_url, max_urls_to_scrap=50):
    '''More settings can be added here to change the spider behaviour
    https://docs.scrapy.org/en/latest/topics/settings.html'''
    process = CrawlerRunner(settings)

    return process.crawl(LinkSpider, start_urls=[base_url], max_to_scrap=max_urls_to_scrap)


def cli_start(base_url, max_urls_to_scrap=50):
    process = CrawlerProcess(settings)

    process.crawl(LinkSpider, start_urls=[base_url], max_to_scrap=max_urls_to_scrap)
    process.start()


if __name__ == "__main__":
    cli_start('https://illinois.edu/', max_urls_to_scrap=100)
    #cli_start('https://www.stanford.edu/', max_urls_to_scrap=300)
    #start('https://www.stanford.edu/')