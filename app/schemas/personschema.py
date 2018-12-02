from marshmallow import Schema, fields, post_load, validate, ValidationError
from app.models import Person
from app.models.pet import Pet
from .petschema import PetSchema
from .baseschema import BaseSchema


class PersonSchema(BaseSchema):
    id = fields.Str(dump_only=True)
    first_name = fields.Str(dump_to='firstName', load_from='firstName', required=True, validate=BaseSchema.must_be_name)
    last_name = fields.Str(dump_to='lastName', load_from='lastName', required=True, validate=BaseSchema.must_be_name)
    bsn = fields.Int(required=True)
    pets = fields.List(fields.Nested(PetSchema), missing=[])

    @post_load
    def make_person(self, data):
        person = Person()
        return super(PersonSchema, self).to_obj(data, person)