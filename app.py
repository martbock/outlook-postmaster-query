import yaml
import config
from blessings import Terminal
from exceptions import CrawlException, EmailException, ValidationException
from email_notifier import EmailNotifier
from crawler import Crawler

t = Terminal()


def print_error(title, error, yaml_dump=True):
    print(f'{t.red + t.reverse} ERROR {t.normal + t.red} {title + t.normal}')
    print(yaml.dump(error) if yaml_dump else error)


class App:

    def __init__(self):
        try:
            self.config = config.load_config()
            self.notifier = EmailNotifier(self.config)
            self.crawler = Crawler(self.config)
        except ValidationException as e:
            print_error('Your configuration is invalid.', e.errors)
            exit(1)

    def main(self):
        try:
            blocked_result = self.crawler.query_api()
        except CrawlException as e:
            print_error('Crawling API failed.', e, yaml_dump=False)
            return exit(1)
        if len(blocked_result) < 1:
            return exit(0)
        for recipient in self.config['email']['recipients']:
            self.notify_via_email(recipient, blocked_result)

    def notify_via_email(self, recipient: dict, blocked_result: list):
        """Notify a recipient about blocked IPs."""
        email = self.notifier.build_email(recipient, blocked_result)
        try:
            self.notifier.send(recipient_email=recipient['email'], message=email)
        except EmailException as e:
            print_error('Sending email failed.', e, yaml_dump=False)
            exit(1)


if __name__ == '__main__':
    App().main()
