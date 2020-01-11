from cerberus import Validator
import os
import yaml

from exceptions import ValidationException


def load_schema():
    with open(os.path.join(os.path.dirname(__file__), 'config-schema.yml'), mode='r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def load_config():
    with open('env.yml', mode='r') as file:
        content = yaml.load(file, Loader=yaml.FullLoader)
        validator = Validator(load_schema())
        if not validator.validate(content):
            raise ValidationException(validator.errors)
        return content
