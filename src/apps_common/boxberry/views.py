from django.http.response import JsonResponse
from . import api


def cities(request):
    """ Позволяет получить список городов, в которых есть пункты выдачи """
    return JsonResponse({
        'data': api.getCities(),
    })


def cities_courier(request):
    """ Позволяет получить список городов в которых осуществляется курьерская доставка """
    return JsonResponse({
        'data': api.getCitiesCourier(),
    })


def cities_full(request):
    """ Позволяет получить список городов, в которых осуществляется доставка Boxberry """
    return JsonResponse({
        'data': api.getCitiesFull(),
    })


def points(request, city_id):
    """ Позволяет получить информацию о всех точках выдачи заказов """
    return JsonResponse({
        'data': api.getPoints(city_id),
    })


def point(request, point_id):
    """ Позволяет получить всю информацию по ПВЗ, включая фотографии """
    try:
        photos = int(request.GET.get('photos', 0))
    except (TypeError, ValueError):
        photos = 0

    return JsonResponse({
        'data': api.getPoint(point_id, photos),
    })


def cost(request, point_id):
    """ Позволяет получить всю информацию по ПВЗ, включая фотографии """
    params = {}
    for param in ('ordersum', 'weight', 'height', 'width', 'depth'):
        try:
            value = int(request.GET.get(param, 0))
        except (TypeError, ValueError):
            value = 0
        params[param] = value

    return JsonResponse({
        'data': api.getDeliveryCosts(point_id, **params),
    })
