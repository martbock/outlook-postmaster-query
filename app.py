from smtplib import SMTPException

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
        recipient = self.config['email']['recipients'][0]
        email = notifier.build_email(
            recipient=recipient,
            blocked_result=[{'first_ip': '1.1.1.1', 'last_ip': '9.9.9.9', 'blocked': True,
                             'details': 'Evidence of spamming'}]
        )
        try:
            notifier.send(recipient_email=recipient['email'], message=email)
        except SMTPException as e:
            self.print_error('Sending email failed.', e, yaml_dump=False)
            exit(1)

    def config_invalid(self, e: ValidationException):
        self.print_error('Your configuration is invalid.', e.errors)
        exit(1)

    def print_error(self, title, error, yaml_dump=True):
        print(f'{t.red + t.reverse} ERROR {t.normal + t.red} {title + t.normal}')
        print(yaml.dump(error) if yaml_dump else error)


if __name__ == '__main__':
    App().main()
