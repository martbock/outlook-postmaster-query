import yaml
from blessings import Terminal
from config import Config, ValidationException

t = Terminal()


class App:

    def __init__(self):
        try:
            self.config = Config().config
        except ValidationException as e:
            self.config_invalid(e)

    def main(self):
        print('Hello World. This is your config:')
        print(yaml.dump(self.config))

    def config_invalid(self, e: ValidationException):
        print(f'{t.red + t.reverse} ERROR {t.normal + t.red} Your configuration is invalid.{t.normal}')
        print(yaml.dump(e.errors))
        exit(1)


if __name__ == '__main__':
    App().main()
