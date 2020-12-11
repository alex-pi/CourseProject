import os
from urllib.parse import urlparse

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(ROOT_DIR, 'data')
DATA_OUTPUT_PATH = os.path.join(DATA_PATH, 'output')


def extract_domain(base_url):
    domain = urlparse(base_url).netloc
    # TODO improve this subdomain extraction
    if 'www' in domain:
        domain = '.'.join(domain.split('.')[1:])
    return domain


def get_data_paths(url):
    domain = extract_domain(url)
    exported_data_path = os.path.join(DATA_OUTPUT_PATH, domain)

    return {
        'domain': domain,
        'exported_data_path': exported_data_path,
        'all_data_path': f'{exported_data_path}-all.csv',
        'positive_data_path': f'{exported_data_path}-positive.csv',
        'done': f'{exported_data_path}.done',
    }
