from marshmallow import Schema, fields, post_load, validate
from . import Person, Pet
from app.utils.schemas import *


class PetSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Str(dump_only=True)
    name = fields.Str()
    breed = fields.Str()

    @post_load
    def make_pet(self, data):
        pet = Pet()
        return to_obj(data, pet)


class GetPersonSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Str(dump_only=True)
    first_name = fields.Str(load_from='firstName', dump_to='firstName')
    last_name = fields.Str(load_from='lastName', dump_to='lastName')
    bsn = fields.Int()
    pets = fields.List(fields.Nested(PetSchema), dump_only=True, missing=[])
    limit = fields.Int(load_only=True)
    offset = fields.Int(load_only=True)
    

class CreatePersonSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Str(dump_only=True)
    first_name = fields.Str(dump_to='firstName', load_from='firstName', required=True, validate=must_be_name)
    last_name = fields.Str(dump_to='lastName', load_from='lastName', required=True, validate=must_be_name)
    bsn = fields.Int(required=True)
    pets = fields.List(fields.Nested(PetSchema), missing=[])

    @post_load
    def make_person(self, data):
        person = Person()
        return to_obj(data, person)


class UpdatePersonSchema(Schema):
    class Meta:
        ordered = True

    first_name = fields.Str(dump_to='firstName', load_from='firstName', required=True, validate=must_be_name)
    last_name = fields.Str(dump_to='lastName', load_from='lastName', required=True, validate=must_be_name)
    bsn = fields.Int(required=True)
    pets = fields.List(fields.Nested(PetSchema), missing=[])
