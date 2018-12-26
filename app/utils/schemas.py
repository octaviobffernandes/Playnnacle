import re
from marshmallow import ValidationError

def to_obj(data, obj):
    for k, v in data.items():
        if hasattr(obj, k):
            setattr(obj, k, v)
    return obj

def must_be_name(data):
    if not re.match(r"^[A-Z]{1}[a-z]*$", data):
        raise ValidationError('Invalid name.')        
