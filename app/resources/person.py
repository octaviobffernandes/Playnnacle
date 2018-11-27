from flask_restful import Resource, request
from flask import Response
from app.models import Person
from app.models import Pet
from mongoengine import *
import datetime

class PersonResource(Resource):
    def get(self):
        return Response(Person.objects.to_json(), mimetype='application/json')

    def post(self):
        person = Person()
        req = request.get_json()
        
        person.first_name=req['FirstName']
        person.last_name=req['LastName']
        person.bsn=req['Bsn']
        person.birth_date = datetime.date(1985, 10, 2)
        
        person.pets = []
        for p in req['Pets']:
            person.pets.append(Pet(name=p['Name'], breed=p['Breed']))
        person.save()
        return 'ok'