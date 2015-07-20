import json
from django.template import Library

register = Library()


@register.filter
def to_json(value):
    return json.dumps(value)


@register.filter
def from_json(value):
    return json.loads(value)
