from mongoengine import *
from .pet import Pet
import json


class Person(Document):
    first_name = StringField()
    last_name = StringField()
    bsn = IntField()
    birth_date = DateTimeField()
    pets = ListField(EmbeddedDocumentField(Pet))

    @staticmethod
    def from_json(json):
        person = Person()
        for k, v in json.items():
            setattr(person, k, v)
        return person
