from app.models import Person
from mongoengine import Q
from app.utils import dotdict
import functools

class PersonService():
    def get_many(self, req_dict):
        req = dotdict(req_dict)
        query_set = []
        limit = 5
        offset = 0

        if req.bsn:
            query_set.append(Q(bsn__exact=req.bsn))
        if req.last_name:
            query_set.append(Q(last_name__icontains=req.last_name))
        if req.first_name:
            query_set.append(Q(first_name__icontains=req.first_name))
        if req.limit:
            limit = int(req.limit)
        if req.offset:
            offset = int(req.offset)

        query = None
        if query_set:
            query = functools.reduce(lambda a,b : a & b, query_set)
        
        return Person.objects[offset:limit+offset](query).all()

    def get(self, id):
        return Person.objects(pk=id).first()        

    def save(self, person):
        person.save()
        return person

    def delete(self, person):
        person.delete()