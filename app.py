import config
import json


def main():
    print('Hello World. This is your config:')
    print(json.dumps(config.config, indent=4))


def config_missing():
    print('Please provide config in env.yml')
    exit(1)


if __name__ == '__main__':
    main()
