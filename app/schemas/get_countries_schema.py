from marshmallow import Schema, fields
from .baseschema import BaseSchema


class GetCountriesSchema(BaseSchema):
    name = fields.Str()
    iso_code = fields.Str(load_from='isoCode')
    language = fields.Str()
    limit = fields.Int()
    offset = fields.Int()
