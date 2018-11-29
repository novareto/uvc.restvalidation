import pytest
import types
import zope.schema
import zope.interface
from uvc.restvalidation import serialize


class IDummy(zope.interface.Interface):
    """Dummy test schema with fields.
    """
    active = zope.schema.Bool(title=u"Active", required=True)
    title = zope.schema.TextLine(title=u"Title")
    age = zope.schema.Int(title=u"Age")


class IDummer(zope.interface.Interface):
    """Dummy test schema with fields.
    """
    gender = zope.schema.Choice(title=u"Gender", values=('m', 'f'))


def test_fields():
    fields = serialize.fields(IDummy)
    assert isinstance(fields, types.GeneratorType)
    assert list(fields) == [
        IDummy['active'],
        IDummy['title'],
        IDummy['age']
    ]

    fields = serialize.fields(IDummy, IDummer)
    assert list(fields) == [
        IDummy['active'],
        IDummy['title'],
        IDummy['age'],
        IDummer['gender']
    ]
