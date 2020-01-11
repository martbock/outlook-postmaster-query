import csv
import requests
from requests.exceptions import BaseHTTPError, ConnectionError

from exceptions import CrawlException


class Crawler:

    def __init__(self, config: dict):
        self.config = config

    def query_api(self) -> list:
        """Crawl and parse the Outlook IP Status API."""
        c = self.config['outlook']['api']
        try:
            response = requests.get(f"{c['url']}?key={c['key']}")
        except (BaseHTTPError, ConnectionError) as e:
            raise CrawlException(e)
        raw_csv = response.text
        csv_reader = csv.reader(raw_csv.splitlines(), delimiter=',')
        return [{
            'first_ip': row[0],
            'last_ip': row[1],
            'blocked': row[2],
            'details': row[3]
        } for row in csv_reader]
