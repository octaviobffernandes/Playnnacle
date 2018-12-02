from mongoengine import *
from .pet import Pet


class Person(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    bsn = IntField(required=True)
    birth_date = DateTimeField()
    pets = ListField(EmbeddedDocumentField(Pet))
