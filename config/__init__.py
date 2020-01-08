from cerberus import Validator
import os
import yaml

from config.exceptions import ValidationException


class Config:

    def __init__(self):
        schema = self.load_schema()
        self.config = self.load_config(schema)

    def load_schema(self):
        with open(os.path.join(os.path.dirname(__file__), 'schema.yml'), mode='r') as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def load_config(self, schema):
        with open('env.yml', mode='r') as file:
            content = yaml.load(file, Loader=yaml.FullLoader)
            validator = Validator(schema)
            if not validator.validate(content):
                raise ValidationException(validator.errors)
            return content
