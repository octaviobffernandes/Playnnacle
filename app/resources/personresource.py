from app.schemas import PersonSchema, GetPeopleSchema
from app.services import PersonService
from flask import request
from flask.json import jsonify
from flask.views import MethodView


class PeopleResource(MethodView):
    service = PersonService()

    def get(self):
      """People endpoint
      ---
      description: Get all people, with optional filters
      parameters:
          - name: firstName
            in: query
            type: string
            description: part of a person's first name to use when filtering
          - name: lastName
            in: query
            type: string
            description: part of a person's last name to use when filtering
          - name: bsn
            in: query
            type: integer
            description: the exact person's bsn to use when filtering
          - name: limit
            in: query
            type: integer
            description: the maximum number of records to be returned (default 5)
          - name: offset
            in: query
            type: integer
            description: the number of records to skip when searching (default 0)            
      responses:
          200:
              description: A list with people meeting specified criteria
              schema: PersonSchema
          500:
              description: Internal server error            
      """
      req = GetPeopleSchema().load(request.args).data
      people = self.service.get_many(req)
      result = [PersonSchema().dump(p).data for p in people]
      return jsonify(result),  200

    def post(self):
      """People endpoint
      ---
      description: Post a new person
      parameters:
          - name: person
            in: body
            description: information about a new person
            schema: PersonSchema
      responses:
          200:
              description: the inserted entity
              schema: PersonSchema
          400:
              description: Bad req
          500:
              description: Internal server error                                
      """

      person_schema = PersonSchema()
      person_model = person_schema.load(request.get_json())

      if person_model.errors:
          return person_model.errors, 400

      person = self.service.save(person_model.data)
      result = person_schema.dump(person).data
      return jsonify(result)