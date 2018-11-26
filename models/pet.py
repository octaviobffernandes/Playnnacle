from mongoengine import *

class Pet(EmbeddedDocument):
    name = StringField()
    breed = StringField()
    birth_date = DateTimeField()