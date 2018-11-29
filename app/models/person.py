from mongoengine import *
from .pet import Pet
import json


class Person(Document):
    first_name = StringField()
    last_name = StringField()
    bsn = IntField()
    birth_date = DateTimeField()
    pets = ListField(EmbeddedDocumentField(Pet))

    def from_json(self, json):
        for k, v in json.items():
            setattr(self, k, v)
