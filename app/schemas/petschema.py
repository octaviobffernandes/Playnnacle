from marshmallow import Schema, fields, post_load
from app.models import Pet
from .baseschema import BaseSchema


class PetSchema(BaseSchema):
    id = fields.Str(dump_only=True)
    name = fields.Str()
    breed = fields.Str()

    @post_load
    def make_pet(self, data):
        pet = Pet()
        return super(PetSchema, self).to_obj(data, pet)