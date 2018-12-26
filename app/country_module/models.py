from mongoengine import *


class Country(Document):
    name = StringField(required=True)
    iso_code = StringField(required=True)
    population = IntField(required=True)
    language = StringField(required=True)
