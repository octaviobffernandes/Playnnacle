from marshmallow import Schema, fields, post_load, validate, ValidationError
from .models import Country
from app.utils.schemas import *


class CountrySchema(Schema):
    id = fields.Str(dump_only=True)
    name  = fields.Str(required=True)
    iso_code = fields.Str(dump_to='isoCode', load_from='isoCode', required=True)
    population = fields.Int(required=True)
    language = fields.Str(required=True)

    @post_load
    def make_country(self, data):
        country = Country()
        return to_obj(data, country)


class GetCountriesSchema(Schema):
    name = fields.Str()
    iso_code = fields.Str(load_from='isoCode')
    language = fields.Str()
    limit = fields.Int()
    offset = fields.Int()
