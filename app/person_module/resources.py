from . import CreatePersonSchema, UpdatePersonSchema, GetPersonSchema, PersonService
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
              schema: GetPersonSchema
          500:
              description: Internal server error            
      """
      schema = GetPersonSchema()
      req = schema.load(request.args).data
      people = self.service.get_many(req)
      result = [schema.dump(p).data for p in people]
      return jsonify(result),  200

    def post(self):
      """People endpoint
      ---
      description: Post a new person
      parameters:
          - name: person
            in: body
            description: information about a new person
            schema: CreatePersonSchema
      responses:
          200:
              description: the inserted entity
              schema: CreatePersonSchema
          400:
              description: Bad req
          500:
              description: Internal server error                                
      """

      schema = CreatePersonSchema()
      person_model = schema.load(request.get_json())

      if person_model.errors:
          return jsonify(person_model.errors), 400

      person = self.service.save(person_model.data)
      result = schema.dump(person).data
      return jsonify(result)

    def put(self):
        """People endpoint
        ---
        description: Update an existing person
        parameters:
            - name: person
              in: body
              description: information about the person to update
              schema: UpdatePersonSchema
        responses:
            204:
                description: successfully updated
            400:
                description: Bad req
            404:
                description: Could not find person with provided id
            500:
                description: Internal server error                                
        """        
        schema = UpdatePersonSchema()
        person_new_data = schema.load(request.get_json())

        if person_new_data.errors:
            return jsonify(person_new_data.errors), 400
        
        person = self.service.get(person_new_data.data['id'])

        if person is None:
            return "could not find person with provided id", 404
        
        for key, val in person_new_data.data.items():
            setattr(person, key, val)

        self.service.save(person)
        return "saved successfully", 204

    def delete(self):
        """People endpoint
        ---
        description: Delete an existing person
        parameters:
            - name: id
              in: query
              type: string
              description: id of the person to delete
        responses:
            204:
                description: successfully deleted
            404:
                description: Could not find person with provided id
            500:
                description: Internal server error                                
        """        
        person_id = request.args['id']
        person = self.service.get(person_id)

        if person is None:
            return "could not find person with provided id", 404
        
        self.service.delete(person)
        return "deleted successfully", 204        