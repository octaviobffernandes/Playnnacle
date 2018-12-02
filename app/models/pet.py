from mongoengine import *

class Pet(EmbeddedDocument):
    name = StringField(required=True)
    breed = StringField(required=True)
    birth_date = DateTimeField()