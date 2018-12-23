from flask_restful import Resource, request
from flask import Response
from app.schemas import PersonSchema, GetPeopleSchema
from app.services import PersonService
import json

class PersonResource(Resource):
    service = PersonService()

    def get(self):
        req = GetPeopleSchema().load(request.args).data
        people = self.service.get_many(req)

        result = [PersonSchema().dump(p) for p in people]
        return result, 200

    def post(self):
        person_schema = PersonSchema()
        person_model = person_schema.load(request.get_json())

        if person_model.errors:
            return person_model.errors, 400

        person = self.service.save(person_model.data)
        return person_schema.dump(person)