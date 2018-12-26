from mongoengine import *


class Pet(EmbeddedDocument):
    name = StringField(required=True)
    breed = StringField(required=True)
    birth_date = DateTimeField()

class Person(Document):
    first_name = StringField(required=True)
    last_name = StringField(required=True)
    bsn = IntField(required=True)
    birth_date = DateTimeField()
    pets = ListField(EmbeddedDocumentField(Pet))


