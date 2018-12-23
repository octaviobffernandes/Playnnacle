from flask_restful import Resource, request
from flask import Response
from flask_restful_swagger import swagger
from app.schemas import PersonSchema, GetPeopleSchema
from app.services import PersonService
import json

class PersonResource(Resource):
    service = PersonService()

    @swagger.operation(
        notes='some really good notes',
        responseClass=PersonSchema.__name__,
        nickname='GetAllPeople',
        parameters=[
            {
              "name": "bsn",
              "description": "Exact BSN number of the person",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "firstName",
              "description": "Part of the first name of the person",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "lastName",
              "description": "Part of the last name of the person",
              "required": False,
              "allowMultiple": False,
              "dataType": "string",
              "paramType": "query"
            },
            {
              "name": "limit",
              "description": "Limit of items per page. Default is 5",
              "required": False,
              "allowMultiple": False,
              "dataType": "int",
              "paramType": "query"
            },
            {
              "name": "offset",
              "description": "Number of items to skip in the result set. Default is 0",
              "required": False,
              "allowMultiple": False,
              "dataType": "int",
              "paramType": "query"
            }                        
          ],
        responseMessages=[
            {
              "code": 200,
              "message": "Success"
            },
            {
              "code": 500,
              "message": "Internal Server Error"
            }
          ]
        )    
    def get(self):
        req = GetPeopleSchema().load(request.args).data
        people = self.service.get_many(req)

        result = [PersonSchema().dump(p) for p in people]
        return result, 200

    @swagger.operation(
        notes='some really good notes',
        responseClass=PersonSchema.__name__,
        nickname='SavePerson',
        parameters=[
            {
              "name": "person",
              "description": "Information about the person to be saved",
              "required": True,
              "allowMultiple": False,
              "dataType": PersonSchema.__name__,
              "paramType": "body"
            }                        
          ],
        responseMessages=[
            {
              "code": 200,
              "message": "Success"
            },
            {
              "code": 400,
              "message": "Bad Request"
            },
            {
              "code": 500,
              "message": "Internal Server Error"
            }
          ]
        )   
    def post(self):
        person_schema = PersonSchema()
        person_model = person_schema.load(request.get_json())

        if person_model.errors:
            return person_model.errors, 400

        person = self.service.save(person_model.data)
        return person_schema.dump(person)