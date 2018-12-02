from marshmallow import Schema, fields, post_load, validate, ValidationError
from app.models import Person
from .baseschema import BaseSchema
from app.models import Country

class CountrySchema(BaseSchema):
    id = fields.Str(dump_only=True)
    name  = fields.Str(required=True)
    iso_code = fields.Str(dump_to='isoCode', load_from='isoCode', required=True)
    population = fields.Int(required=True)
    language = fields.Str(required=True)

    @post_load
    def make_country(self, data):
        country = Country()
        return super(CountrySchema, self).to_obj(data, country)