import json
import functools
import collections
import zope.schema
from zope.interface.exceptions import BrokenImplementation
from zope.interface.verify import verifyObject

from .serialize import fields


class Extracted(dict):

    def __init__(self, *args, **kwargs):
        super(Extracted, self).__init__(*args, **kwargs)
        self.by_schema = collections.defaultdict(dict)

    def insert(self, field, value):
        if field.interface is None:
            raise TypeError('%r needs to be declared inside an interface.')
        name = field.__name__
        self[name] = value
        self.by_schema[field.interface][name] = value


def validate(data, fields, strict=True):
    parsed = Extracted()
    errors = []
    for field in fields:
        name = field.__name__
        if name in data:
            value = data.pop(name)
            try:
                field.validate(value)
            except zope.schema.ValidationError as err:
                errors.append('%s: %s' % (name, err.__doc__))
            else:
                parsed.insert(field, value)
        elif field.required and (strict is True or name in strict):
            errors.append('Missing field `%s`' % name)
    if data:
        errors.append('Unexpected field `%s`' % ', '.join(data.keys()))
    return parsed, errors


def expected(*fields, **kws):

    strict = kws.get('strict', True)
    decode = kws.get('decode', json.loads)
    handle_errors = kws.get('handle_errors', True)

    def method_validator(api_meth):

        @functools.wraps(api_meth)
        def validate_incoming_data(api):
            try:
                data = decode(api.body)
            except ValueError:
                parsed = None
                errors = ['Impossible to decode the body.']
            else:
                parsed, errors = validate(data, fields, strict)
            return api_meth(api, parsed, errors)

        return validate_incoming_data

    return method_validator


def error_handler(api_meth):

    @functools.wraps(api_meth)
    def safeguard(api, parsed, errors):
        if not errors:
            try:
                return api_meth(api, parsed)
            except KeyError as err:
                errors.append(err.message)
        api.request.response.setStatus(400)
        return {'errors': errors}

    return safeguard
