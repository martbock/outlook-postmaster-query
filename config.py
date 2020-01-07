import yaml


def load_config():
    with open('env.yml') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


config = load_config()
