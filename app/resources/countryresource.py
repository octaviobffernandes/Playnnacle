from flask_restful import Resource, request
from flask import Response
from app.models import Country
from app.schemas import CountrySchema
from mongoengine import *
import json

class CountryResource(Resource):
    schema = CountrySchema()

    def get(self):
        countries = Country.objects
        result = [self.schema.dump(p) for p in countries]
        return result, 200

    def post(self):
        result = self.schema.load(request.get_json())

        if result.errors:
            return result.errors, 400

        person = result.data
        person.save()
        
        return self.schema.dump(person)