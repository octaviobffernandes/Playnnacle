from app.models import Country
from mongoengine import *
from app.utils import dotdict
import functools

class CountryService():
    def get_many(self, req_dict):
        req = dotdict(req_dict)
        query_set = []
        limit = 5
        offset = 0

        if req.name:
            query_set.append(Q(name__icontains=req.name))
        if req.iso_code:
            query_set.append(Q(iso_code__iexact=req.iso_code))
        if req.language:
            query_set.append(Q(language__icontains=req.language))
        if req.limit:
            limit = int(req.limit)
        if req.offset:
            offset = int(req.offset)

        query = None
        if query_set:
            query = functools.reduce(lambda a,b : a & b, query_set)
        
        return Country.objects[offset:limit+offset](query)

    def save(self, country):
        country.save()
        return country