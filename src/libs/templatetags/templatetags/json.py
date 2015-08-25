import json
from django.template import Library
from django.db.models.query import QuerySet
from django.core.serializers import serialize
from django.utils.safestring import mark_safe

register = Library()


@register.filter
def to_json(obj):
    if isinstance(obj, QuerySet):
        result = serialize('json', obj)
    else:
        result = json.dumps(obj)
    return mark_safe(result)
