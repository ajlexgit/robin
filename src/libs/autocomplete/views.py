import math
import pickle
import importlib
from itertools import zip_longest
from django.apps import apps
from django.db.models import Q
from django.conf import settings
from django.core.cache import caches
from django.http import Http404, JsonResponse

CACHE_BACKEND = getattr(settings,  'AUTOCOMPLETE_CACHE_BACKEND', 'default')
cache = caches[CACHE_BACKEND]


def autocomplete_widget(request, application, model_name, name):
    if not request.is_ajax():
        raise Http404

    try:
        page = int(request.POST.get('page', 1))
        page_limit = int(request.POST.get('page_limit', 0))
    except (TypeError, ValueError):
        raise Http404

    # Получаем данные из Redis
    redis_data = pickle.loads(
        cache.get('.'.join((application, model_name, name)))
    )

    # Восстанавливаем queryset
    model = apps.get_model(application, model_name)
    if model is None:
        raise Http404

    data = {
        'result': [],
    }

    queryset = model.objects.all()
    queryset.query = redis_data['query']

    # Зависимое поле
    query = Q()
    dependencies = tuple(item[0] for item in redis_data['dependencies'])
    values = request.POST.get("values").split(';')
    is_multiple = tuple(item[2] for item in redis_data['dependencies'])
    for index, key in enumerate(dependencies):
        try:
            value = values[index]
            multiple = is_multiple[index]
        except KeyError:
            return JsonResponse(data)

        if not value:
            value = None
        elif multiple:
            value = value.split(',')
            key += '__in'

        query &= Q((key, value))

    queryset = queryset.filter(query)

    # Поиск по выражениям
    expressions = request.POST.get('expressions')
    if not expressions:
        raise Http404
    else:
        expressions_query = Q()
        token = request.POST.get('q', '')
        for expression in expressions.split(','):
            if expression.endswith('__in'):
                expressions_query |= Q((expression, token.split(",")))
            else:
                expressions_query |= Q((expression, token))

        queryset = queryset.filter(expressions_query)

    # Постраничная навигация
    if page and page_limit:
        count = data['total'] = queryset.count()
        max_pages = math.ceil(count / page_limit)
        real_page = max(1, min(page, max_pages))
        offset = (real_page - 1) * page_limit
        queryset = queryset[offset:offset+page_limit]

    # Кастомное форматирование списка
    module = importlib.import_module(redis_data['format_item_module'])
    current_obj = module
    for part in redis_data['format_item_method'].split('.'):
        current_obj = getattr(current_obj, part)
    else:
        format_item = current_obj

    for item in queryset.iterator():
        item_dict = format_item(item)
        if not isinstance(item_dict, dict):
            raise ValueError('autocomplete format_item should return dict')
        if ('id' not in item_dict) or ('text' not in item_dict):
            raise ValueError('autocomplete format_item should contain "id" and "text"')
        data['result'].append(item_dict)

    return JsonResponse(data)
