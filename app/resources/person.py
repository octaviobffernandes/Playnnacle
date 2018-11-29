from flask_restful import Resource, request
from flask import Response
from app.models import Person
from app.factories import PersonInformation
from mongoengine import *
import sys

class PersonResource(Resource):
    def get(self):
        return Response(Person.objects.to_json(), mimetype='application/json')

    def post(self):
        person_information = PersonInformation()

        person = person_information.load(request.get_json())
        person.save()

        return 'ok'