from marshmallow import Schema, fields, post_load, validate, ValidationError
from app.models import Person
from app.models.pet import Pet
import datetime
import re

def must_be_name(data):
    if not re.match(r"^[A-Z]{1}[a-z]*$", data):
        raise ValidationError('Invalid name.')

class PetFields(Schema):
    Name = fields.Str(attribute="name")
    Breed = fields.Str(attribute="breed")


class PersonBuilder(Schema):
    FirstName = fields.Str(attribute="first_name", required=True, validate=must_be_name)
    LastName = fields.Str(attribute="last_name", required=True, validate=must_be_name)
    Bsn = fields.Int(attribute="bsn", required=True)
    Pets = fields.List(fields.Nested(PetFields), attribute="pets", missing=[])

    @post_load
    def make_person(self, data):
        person = Person()
        for k, v in data.items():
            setattr(person, k, v)

        return person