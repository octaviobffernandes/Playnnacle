from flask_restful import Resource, request
from flask import Response
from app.models import Person
from app.schemas import PersonSchema
from mongoengine import *
import json

class PersonResource(Resource):
    schema = PersonSchema()

    def get(self):
        people = Person.objects
        result = [self.schema.dump(p) for p in people]
        return result, 200

    def post(self):
        result = self.schema.load(request.get_json())

        if result.errors:
            return result.errors, 400

        person = result.data
        person.save()
        
        return self.schema.dump(person)