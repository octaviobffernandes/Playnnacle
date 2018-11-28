from flask_restful import Resource, request
from flask import Response
from app.models import Person
from app.models import Pet
from mongoengine import *
import datetime
from webargs import fields
from webargs.flaskparser import parser
import sys

class PersonResource(Resource):
    def get(self):
        return Response(Person.objects.to_json(), mimetype='application/json')

    def post(self):
        personal_info = {
            "FirstName": fields.Str(required=True),
            "LastName": fields.Str(required=True),
            "Bsn": fields.Int(required=True),
            "Pets": fields.List(fields.Dict, missing=[]),
        }

        args = parser.parse(personal_info, request)

        person = Person()
        
        person.first_name=args['FirstName']
        person.last_name=args['LastName']
        person.bsn=args['Bsn']
        person.birth_date = datetime.date(1985, 10, 2)
        
        person.pets = []
        for p in args['Pets']:
            person.pets.append(Pet(name=p['Name'], breed=p['Breed']))
        person.save()
        return 'ok'