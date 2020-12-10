from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from spiderbot.scrapy_spider import start
from globals import DATA_OUTPUT_PATH
from urllib.parse import urlparse
import os
from threading import Thread

import crochet
crochet.setup()

# Flask setup.
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Global vars.
in_progress = set([])
completed_tasks = {}

# Flask routes.
@app.route("/", methods=["POST"])
@cross_origin()
def submit():
    if request.method == "POST":
        url = request.json["url"]

        if url in completed_tasks:
            return_urls = completed_tasks[url]
            del completed_tasks[url]
            return jsonify(result=True, urls=return_urls)
        elif url in in_progress:
            return jsonify(result=False, urls=[])
        else:
            # Scrape the URL.
            in_progress.add(url)
            thread = Thread(target=scrape, args=(url,))
            thread.daemon = True
            thread.start()
            return jsonify(result=False, urls=[])

def scrape(url):
    scrape_with_crochet(url)

    # Convert the CSV data to JSON.
    domain = urlparse(url).netloc
    if 'www' in domain:
        domain = '.'.join(domain.split('.')[1:])
    csv_path = os.path.join(DATA_OUTPUT_PATH, domain)
    csv_path += "-positive.csv"
    completed_tasks[url] = convert_csv_to_json(csv_path)
    in_progress.remove(url)

@crochet.wait_for(timeout=99999)
def scrape_with_crochet(url):
    return start(url, max_urls_to_scrap=200)

def convert_csv_to_json(csvPath):
    urls = []

    # Iterate through the CSV and grab only the desired values.
    if (os.path.getsize(csvPath) != 0):
        with open(csvPath, "r") as file:

            next(file)
            for line in file:
                line_split = line.split(",")
                urls.append(line_split[1])

    return urls

if __name__ == '__main__':
    app.run()
