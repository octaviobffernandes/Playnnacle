from marshmallow import Schema, fields, post_load, validate, ValidationError
from app.models import Person
from app.models.pet import Pet
from .petschema import PetSchema
from .baseschema import BaseSchema


class UpdatePersonSchema(BaseSchema):
    id = fields.Str()
    first_name = fields.Str(dump_to='firstName', load_from='firstName', required=True, validate=BaseSchema.must_be_name)
    last_name = fields.Str(dump_to='lastName', load_from='lastName', required=True, validate=BaseSchema.must_be_name)
    bsn = fields.Int(required=True)
    pets = fields.List(fields.Nested(PetSchema), missing=[])