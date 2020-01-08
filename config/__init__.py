from cerberus import Validator
import os
import yaml


class Config:

    def __init__(self):
        schema = self.load_schema()
        self.config = self.load_config(schema)

    def load_schema(self):
        with open(os.path.join(os.path.dirname(__file__), 'schema.yml')) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def load_config(self, schema):
        with open('env.yml') as file:
            content = yaml.load(file, Loader=yaml.FullLoader)
            v = Validator()
            v.validate(content, schema)
            print(v.errors)
            return content
