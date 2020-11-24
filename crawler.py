import csv
import requests
import itertools
from requests.exceptions import ConnectionError, HTTPError
from exceptions import CrawlException


class Crawler:

    def __init__(self, config: dict):
        self.config = config

    def query_api(self) -> list:
        """Crawl and parse the Outlook IP Status API."""
        c = self.config['outlook']['api']
        try:
            response = requests.get(f"{c['url']}?key={c['key']}")
            response.raise_for_status()
        except (ConnectionError, HTTPError) as e:
            raise CrawlException(e)
        raw_csv = response.text
        validation_reader, result_reader = itertools.tee(csv.reader(raw_csv.splitlines(), delimiter=','))
        for row in validation_reader:
            if type(row) is not list or len(row) != 4:
                raise CrawlException("Failed to parse response")
        return [{
            'first_ip': row[0],
            'last_ip': row[1],
            'blocked': row[2],
            'details': row[3]
        } for row in result_reader]
