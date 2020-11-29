import scrapy
import time
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
from scrapy import signals
from urlclassification import url_classification as uc


class LinkSpider(scrapy.Spider):
    name = 'links'

    def __init__(self, *args, **kwargs):
        self.main_domain = kwargs.get('main_domain')
        self.max_to_scrap = kwargs.get('max_to_scrap')
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
                item['text'] = link.text
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

        # Change this condition for a call to Gang's classifier
        # time.sleep(5)
        result = self.classifier.SVM_Predict(item['link'])
        if result != 0:
            print(f"Found candidate: {item['link']}")
            return item
        else:
            raise DropItem(f"{item!r} is not a candidate")


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


class LinkItem(scrapy.Item):
    link = scrapy.Field()
    text = scrapy.Field()


def start(base_url):
    '''More settings can be added here to change the spider behaviour
    https://docs.scrapy.org/en/latest/topics/settings.html'''
    process = CrawlerProcess({
        # 'DOWNLOAD_DELAY': 10,
        # Broad crawling can demand more memory but page crawling is faster
        # Next 3 lines force to do BFO instead of DFO
        'DEPTH_PRIORITY': 1,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        # End of Broad crawling configuration
        'LOG_LEVEL': 'ERROR',
        'DEPTH_LIMIT': 7,
        'CLOSESPIDER_PAGECOUNT': 5000,
        # Defaults to 8
        'CONCURRENT_REQUESTS_PER_DOMAIN': 12,
        # Concurrent items (per response) to be processed in the pipelines
        'CONCURRENT_ITEMS': 120,
        # Improves performance at the cost of missing content
        'RETRY_ENABLED': False,
        'DOWNLOAD_TIMEOUT': 40,
        'ITEM_PIPELINES': {
            # We can add more pipeline steps like sending URL candidates to
            # a second classifier based on actual page content.
            'spiderbot.scrapy_spider.DuplicatesPipeline': 100,
            'spiderbot.scrapy_spider.ClassificationPipeline': 300
        }
    })
    process.crawl(LinkSpider, start_urls=[base_url],
                  main_domain=['stanford.edu'], max_to_scrap=1000)
    process.start()


if __name__ == "__main__":
    start('https://www.stanford.edu/')