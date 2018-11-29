import pytest
import zope.schema
import zope.interface
from uvc.restvalidation import validate, serialize


class IDummy(zope.interface.Interface):
    """Dummy test schema with fields.
    """
    active = zope.schema.Bool(title=u"Active", required=True)
    title = zope.schema.TextLine(title=u"Title")
    age = zope.schema.Int(title=u"Age")


def test_extracted():
    extracted = validate.Extracted()
    assert extracted == {}
    assert extracted.by_schema == {}

    field = zope.schema.Bool(
        title=u"Boolean field"
        )

    with pytest.raises(TypeError):
        extracted.insert(field, True)

    extracted.insert(IDummy['active'], False)
    assert extracted == {'active': False}
    assert extracted.by_schema == {IDummy: {'active': False}}

    extracted.insert(IDummy['title'], u'My title')
    assert extracted == {'active': False,
                         'title': u'My title'}
    assert extracted.by_schema == {IDummy: {'active': False,
                                            'title': u'My title'}}


def test_validate():
    data = {
        'active': object(),
        'age': 12
    }
    fields = serialize.fields(IDummy)
    parsed, errors = validate.validate(data, fields)

    assert parsed == {'age': 12}
    assert errors == [
        u'active: Object is of wrong type.',
        u'Missing field `title`'
    ]

    assert data == {}

    data = {
        'active': object(),
        'age': 12
    }
    fields = serialize.fields(IDummy)
    parsed, errors = validate.validate(data, fields, strict=[])

    assert parsed == {'age': 12}
    assert errors == [u'active: Object is of wrong type.']
