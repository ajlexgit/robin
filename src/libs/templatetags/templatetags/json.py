import json
from django.template import Library
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from django.utils.safestring import mark_safe

register = Library()


@register.filter
def to_json(object):
    if isinstance(object, QuerySet):
        result = serialize('json', object)
    else:
        result = json.dumps(object)
    return mark_safe(result)
