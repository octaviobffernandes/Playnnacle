from app.schemas import CountrySchema, GetCountriesSchema
from app.services import CountryService
from flask import request
from flask.json import jsonify
from flask.views import MethodView


class CountryResource(MethodView):
    service = CountryService()

    def get(self):
      """Country endpoint
      ---
      description: Get all countries, with optional filters
      parameters:
          - name: isoCode
            in: query
            type: string
            description: the exact country code to use when filtering
          - name: name
            in: query
            type: string
            description: part of the country name to use when filtering
          - name: language
            in: query
            type: string
            description: part of the language name to use when filtering
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
              description: A list with countries meeting specified criteria
              schema: CountrySchema
          500:
              description: Internal server error            
      """
      req = GetCountriesSchema().load(request.args).data
      countries = self.service.get_many(req)
      result = [CountrySchema().dump(p).data for p in countries]
      return jsonify(result),  200

    def post(self):
      """Country endpoint
      ---
      description: Post a new country
      parameters:
          - name: country
            in: body
            description: information about a new country
            schema: CountrySchema
      responses:
          200:
              description: the inserted entity
              schema: CountrySchema
          400:
              description: Bad req
          500:
              description: Internal server error                                
      """

      country_schema = CountrySchema()
      country_model = country_schema.load(request.get_json())

      if country_model.errors:
          return country_model.errors, 400

      country = self.service.save(country_model.data)
      result = country_schema.dump(country).data
      return jsonify(result)