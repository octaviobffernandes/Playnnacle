from marshmallow import Schema, fields
from .baseschema import BaseSchema


class GetPeopleSchema(BaseSchema):
    first_name = fields.Str(load_from='firstName')
    last_name = fields.Str(load_from='lastName')
    bsn = fields.Int(load_from='bsn')
    limit = fields.Int(load_from='limit')
    offset = fields.Int(load_from='offset')
