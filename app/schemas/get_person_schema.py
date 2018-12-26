from marshmallow import Schema, fields
from .baseschema import BaseSchema
from .petschema import PetSchema


class GetPersonSchema(BaseSchema):
    id = fields.Str(dump_only=True)
    first_name = fields.Str(load_from='firstName', dump_to='firstName')
    last_name = fields.Str(load_from='lastName', dump_to='lastName')
    bsn = fields.Int()
    pets = fields.List(fields.Nested(PetSchema), dump_only=True, missing=[])
    limit = fields.Int(load_only=True)
    offset = fields.Int(load_only=True)
    
