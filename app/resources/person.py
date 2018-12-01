from flask_restful import Resource, request
from flask import Response
from app.models import Person
from app.builders import PersonBuilder
from mongoengine import *


class PersonResource(Resource):
    def get(self):
        return Response(Person.objects.to_json(), mimetype='application/json')

    def post(self):
        person_information = PersonBuilder()
        person = person_information.load(request.get_json())

        print(person.first_name)
        print(person.last_name)
        print(person.bsn)
        print(person.pets)
        #person.save()

        return 'ok'