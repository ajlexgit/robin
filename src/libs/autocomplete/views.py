import math
import pickle
import importlib
from django.apps import apps
from django.db.models import Q
from django.conf import settings
from django.core.cache import caches
from django.http import Http404, JsonResponse

CACHE_BACKEND = getattr(settings,  'AUTOCOMPLETE_CACHE_BACKEND', 'default')
cache = caches[CACHE_BACKEND]


def default_item2dict_func(obj):
    return {
        'id': obj.pk,
        'text': str(obj),
    }


def autocomplete_widget(request, application, model_name, name):
    if not request.is_ajax():
        raise Http404

    # Получаем данные из Redis
    redis_data = pickle.loads(
        cache.get('.'.join((application, model_name, name)))
    )

    # Восстанавливаем queryset
    model = apps.get_model(application, model_name)
    if model is None:
        raise Http404

    queryset = model.objects.all()
    queryset.query = redis_data['query']

    # Зависимое поле
    keys = (item[0] for item in redis_data['dependencies'])
    values = request.POST.get("values").split(';')
    multiples = (item[2] for item in redis_data['dependencies'])
    for key, val, multiple in zip(keys, values, multiples):
        if not val:
            val = None
        elif multiple:
            val = val.split(',')
            key += '__in'

        queryset = queryset.filter(Q((key, val)))

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

    data = {
        'result': [],
    }

    # Постраничная навигация
    page = int(request.POST.get('page', 1))
    page_limit = int(request.POST.get('page_limit', 0))
    if page and page_limit:
        count = data['total'] = queryset.count()
        max_pages = math.ceil(count / page_limit)
        real_page = max(1, min(page, max_pages))
        offset = (real_page - 1) * page_limit
        queryset = queryset[offset:offset+page_limit]

    # Метод
    item2dict = default_item2dict_func
    try:
        module = importlib.import_module(redis_data['item2dict_module'])
    except ImportError:
        pass
    else:
        current_obj = module
        for part in redis_data['item2dict_method'].split('.'):
            try:
                current_obj = getattr(current_obj, part)
            except AttributeError:
                break
        else:
            item2dict = current_obj

    for item in queryset.iterator():
        item_dict = item2dict(item)
        if not isinstance(item_dict, dict):
            raise ValueError('autocomplete item2dict_method should return dict')
        if ('id' not in item_dict) or ('text' not in item_dict):
            raise ValueError('autocomplete item2dict_method should contain "id" and "text"')
        data['result'].append(item_dict)

    return JsonResponse(data)
