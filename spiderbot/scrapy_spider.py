import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class LinkSpider(scrapy.Spider):
    name = 'links'
    '''More settings can be added here to change the spider behaviour
    https://docs.scrapy.org/en/latest/topics/settings.html'''
    custom_settings = {
        # 'DOWNLOAD_DELAY': 10,
        'LOG_LEVEL': 'ERROR',
        'DEPTH_LIMIT': 5
    }

    def __init__(self, *args, **kwargs):
        self.main_domain = kwargs.get('main_domain')
        self.link_extractor = LinkExtractor(allow=self.main_domain)
        super(LinkSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        depth = response.meta['depth']
        print(f'current url: {response.url}, depth: {depth}')

        extracted_links = self.link_extractor.extract_links(response)
        # Here we can plug the classifier
        for link in extracted_links:
            # print(f'extracted_link: {link.url}, text: {link.text}')
            # Here we can add more conditions to discard URLs we don't want
            # explore further.
            yield scrapy.Request(
                response.urljoin(link.url),
                callback=self.parse)


class LinkItem(scrapy.Item):
    link = scrapy.Field()
    text = scrapy.Field()


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(LinkSpider, start_urls=['https://www.stanford.edu/'],
                  main_domain=['stanford.edu'])
    process.start()