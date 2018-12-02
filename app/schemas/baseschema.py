from marshmallow import Schema, ValidationError
import re


class BaseSchema(Schema):
    class Meta:
        ordered = True

    def to_obj(self, data, obj):
        for k, v in data.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj
    
    @staticmethod
    def must_be_name(data):
        if not re.match(r"^[A-Z]{1}[a-z]*$", data):
            raise ValidationError('Invalid name.')