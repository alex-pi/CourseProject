import os
from urllib.parse import urlparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_DIR, 'data')
DATA_OUTPUT_PATH = os.path.join(DATA_PATH, 'output')


def extract_domain(base_url):
    domain = urlparse(base_url).netloc
    if domain is '':
        domain = base_url
    # TODO improve this subdomain extraction
    if 'www' in domain:
        domain = '.'.join(domain.split('.')[1:])
    url = f'https://www.{domain}/'
    return domain, url


def get_data_paths(url):
    domain, base_url = extract_domain(url)
    exported_data_path = os.path.join(DATA_OUTPUT_PATH, domain)

    return {
        'domain': domain,
        'base_url': base_url,
        'exported_data_path': exported_data_path,
        'all_data_path': f'{exported_data_path}-all.csv',
        'positive_data_path': f'{exported_data_path}-positive.csv',
        'done': f'{exported_data_path}.done',
    }


crawler_settings = {
    # 'DOWNLOAD_DELAY': 10,
    # Broad crawling can demand more memory but page crawling is faster
    # Next 3 lines force to do BFO instead of DFO
    'DEPTH_PRIORITY': 1,
    'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
    'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    # End of Broad crawling configuration
    'LOG_LEVEL': 'CRITICAL',
    'DEPTH_LIMIT': 4,
    'CLOSESPIDER_PAGECOUNT': 25000,
    # Defaults to 8
    'CONCURRENT_REQUESTS_PER_DOMAIN': 12,
    # Concurrent items (per response) to be processed in the pipelines
    'CONCURRENT_ITEMS': 8,
    # False Improves performance at the cost of missing content
    'RETRY_ENABLED': False,
    'DOWNLOAD_TIMEOUT': 25,
    'DNS_TIMEOUT': 10,
    # Need to find a way to avoid secured pages that redirect to a login page
    'REDIRECT_ENABLED': True,
    'ITEM_PIPELINES': {
        # We can add more pipeline steps like sending URL candidates to
        # a second classifier based on actual page content.
        'spiderbot.scrapy_spider.DuplicatesPipeline': 100,
        'spiderbot.scrapy_spider.ClassificationPipeline': 110,
        'spiderbot.scrapy_spider.LinkItemExporterPipeline2': 120
    }
}
