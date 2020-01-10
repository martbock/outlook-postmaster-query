import yaml
from blessings import Terminal
from config import Config, ValidationException
from notification import EmailNotifier

t = Terminal()


class App:

    def __init__(self):
        try:
            self.config = Config().config
        except ValidationException as e:
            self.config_invalid(e)

    def main(self):
        notifier = EmailNotifier(self.config)
        email = notifier.build_email(
            recipient=self.config['email']['recipients'][0],
            sender=self.config['email']['sender'],
            blocked_result=[{'first_ip': '1.1.1.1', 'last_ip': '9.9.9.9', 'blocked': True,
                             'details': 'Evidence of spamming'}]
        )
        print(email)

    def config_invalid(self, e: ValidationException):
        print(f'{t.red + t.reverse} ERROR {t.normal + t.red} Your configuration is invalid.{t.normal}')
        print(yaml.dump(e.errors))
        exit(1)


if __name__ == '__main__':
    App().main()
