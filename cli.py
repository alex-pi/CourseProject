from spiderbot.scrapy_spider import cli_start
from globals import get_data_paths
from threading import Thread
import os
import time
import sys


def check(data_paths):
    while True:
        if os.path.exists(data_paths['done']):

            count = 0
            for line in open(data_paths['positive_data_path']):
                count += 1
                print(line, end='')
            print(f'--- Finished writing output at: {data_paths["positive_data_path"]} ---')
            print(f'- Lines: {count} -')
            print('--- Crawling finished. Spider will take a bit to close. ---')
            os.remove(data_paths['done'])
            break
        time.sleep(2)


n = len(sys.argv)
if n is not 3:
    print(f'Usage example: python cli.py https://www.stanford.edu/ 500')
    print(f'Where 500 is the desired number of positive results to obtain.')

url = sys.argv[1]
max_results = int(sys.argv[2])

paths = get_data_paths(url)

thread = Thread(target=check, args=(paths,))
thread.daemon = False
thread.start()

print('Crawling from CLI started.')
cli_start(url, max_results)



