from mongoengine import *
from .pet import Pet

class Person(Document):
    first_name = StringField()
    last_name = StringField()
    bsn = IntField()
    birth_date = DateTimeField()
    pets = ListField(EmbeddedDocumentField(Pet))
