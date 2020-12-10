from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from spiderbot.scrapy_spider import start
from globals import DATA_OUTPUT_PATH
from urllib.parse import urlparse
import os

import crochet
crochet.setup()

# Flask setup.
app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

# Flask routes.
@app.route("/", methods=["POST"])
@cross_origin()
def submit():
    if request.method == "POST":
        # Scrape the URL.
        scrape_with_crochet(request.json['url'])

        # Convert the CSV data to JSON.
        domain = urlparse(request.json['url']).netloc
        if 'www' in domain:
            domain = '.'.join(domain.split('.')[1:])
        csv_path = os.path.join(DATA_OUTPUT_PATH, domain)
        csv_path += "-positive.csv"
        return convert_csv_to_json(csv_path)

@crochet.wait_for(timeout=99999)
def scrape_with_crochet(url):
    return start(url, max_urls_to_scrap=200)

def convert_csv_to_json(csvPath):
    urls = []

    # Iterate through the CSV and grab only the desired values.
    with open(csvPath, "r") as file:
        next(file)
        for line in file:
            line_split = line.split(",")
            urls.append(line_split[1])

    return jsonify(urls)

if __name__ == '__main__':
    app.run()
