from marshmallow import Schema, fields, post_load
from app.models import Person
from app.models.pet import Pet
import datetime

class PersonInformation(Schema):
    FirstName = fields.Str()
    LastName = fields.Str()
    Bsn = fields.Int()
    Pets = fields.List(fields.Dict, missing=[])

    @post_load
    def make_person(self, data):
        person = Person()
        person.first_name = data['FirstName']
        person.last_name = data['LastName']
        person.bsn = data['Bsn']
        person.birth_date = datetime.date(1985, 10, 2)

        person.pets = []
        for p in data['Pets']:
            person.pets.append(Pet(name=p['Name'], breed=p['Breed']))
        return person