import re
from django.apps import apps
from django.contrib import admin
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse, Http404, HttpResponse
from libs.upload_chunked_file import upload_chunked_file, NotCompleteError
from . import options


def _get_gallery(request):
    app_label = request.POST.get('app_label')
    model_name = request.POST.get('model_name')
    gallery_model = apps.get_model(app_label, model_name)
    if not gallery_model:
        raise Http404

    gallery_id = request.POST.get('gallery_id', 0)
    try:
        gallery = gallery_model.objects.get(pk=gallery_id)
    except gallery_model.DoesNotExist:
        raise Http404
    else:
        return gallery


def _get_gallery_item(request, gallery):
    item_id = request.POST.get('item_id', 0)
    try:
        item = gallery.items.model.objects.get(pk=item_id)
    except gallery.items.model.DoesNotExist:
        raise Http404
    else:
        return item


@admin.site.admin_view
def create(request):
    """ Создание галереи """
    app_label = request.POST.get('app_label')
    model_name = request.POST.get('model_name')
    gallery_model = apps.get_model(app_label, model_name)
    if not gallery_model:
        raise Http404

    # Создание галереи
    gallery = gallery_model.objects.create()

    context = {
        'gallery': gallery,
        'options': options,
        'name': request.POST.get('field_name'),
    }
    return JsonResponse({
        'gallery_id': gallery.pk,
        'html': render_to_string(gallery.ADMIN_TEMPLATE_ITEMS, context)
    })


@admin.site.admin_view
def delete(request):
    """ Удаление галереи """
    gallery = _get_gallery(request)
    gallery.delete()
    return render_to_response(gallery.ADMIN_TEMPLATE_EMPTY)


@admin.site.admin_view
def sort(request):
    """ Сохранение сортировки галереи """
    gallery = _get_gallery(request)
    item_ids = request.POST.get('item_ids', '').split(',')
    for order, item_id in enumerate(item_ids, start=1):
        try:
            item = gallery.items.model.objects.get(pk=item_id)
        except gallery.items.model.DoesNotExist:
            raise Http404
        else:
            item.order = order
            item.save()
    return HttpResponse()


@admin.site.admin_view
def upload(request):
    """ Загрузка файла """
    gallery = _get_gallery(request)

    try:
        uploaded_file = upload_chunked_file(request, 'image')
    except (LookupError, FileNotFoundError):
        raise Http404
    except NotCompleteError:
        return HttpResponse()

    # Создание экземпляра элемента галереи
    item = gallery.IMAGE_MODEL(
        gallery=gallery,
    )
    item.image.save(uploaded_file.name, uploaded_file, save=False)
    uploaded_file.close()

    try:
        item.image.field.clean(item.image, item)
    except ValidationError as e:
        item.image.delete(save=False)
        return JsonResponse({
            'message': ', '.join(e.messages),
        }, status=400)

    item.clean()
    item.save()

    response = {
        'id': item.pk,
        'preview_url': getattr(item.image, item.ADMIN_VARIATION).url,
        'browse_url': item.browse_url,
        'source_url': item.image.url_nocache,
        'source_size': ','.join(map(str, item.image.dimensions)),
    }

    return JsonResponse(response)


@admin.site.admin_view
def upload_video(request):
    gallery = _get_gallery(request)

    link = request.POST.get('link', '')

    for provider_id, provider in options.PROVIDERS.items():
        for pattern in provider['link_patterns']:
            match = re.match(pattern, link)
            if not match:
                continue

            video_key = match.group(1)

            try:
                video_preview = provider['preview_url'](video_key)
            except ConnectionError as e:
                return JsonResponse({
                    'message': ', '.join(e.args),
                }, status=400)

            # Создание экземпляра элемента галереи
            item = gallery.VIDEO_LINK_MODEL(
                gallery=gallery,
                video_provider=provider_id,
                video_key=video_key,
                video_preview=video_preview,
            )
            item.clean()
            item.save()

            response = {
                'id': item.pk,
                'preview_url': item.video_preview,
                'browse_url': item.browse_url,
            }
            return JsonResponse(response)

    return JsonResponse({
        'message': _('Invalid link'),
    }, status=400)


@admin.site.admin_view
def delete_item(request):
    """ Удаление элемента галереи """
    gallery = _get_gallery(request)
    item = _get_gallery_item(request, gallery)
    item.delete()
    return HttpResponse()


@admin.site.admin_view
def rotate_item(request):
    """ Поворот элемента галереи """
    gallery = _get_gallery(request)
    item = _get_gallery_item(request, gallery)
    if not item.is_image or not item.image.exists():
        raise Http404

    direction = request.GET.get('direction')
    if not direction or direction not in ('left', 'right'):
        raise Http404

    if direction == 'left':
        item.image.rotate(-90)
    else:
        item.image.rotate(90)

    return JsonResponse({
        'preview_url': getattr(item.image, item.ADMIN_VARIATION).url_nocache
    })


@admin.site.admin_view
def crop_item(request):
    """ Обрезка элемента галереи """
    gallery = _get_gallery(request)
    item = _get_gallery_item(request, gallery)
    if not item.is_image or not item.image.exists():
        raise Http404

    coords = request.POST.get('coords', '').split(':')
    try:
        coords = tuple(map(int, coords))
    except (TypeError, ValueError):
        raise Http404

    if len(coords) < 4:
        raise Http404
    else:
        coords = coords[:4]

    item.image.recut(crop=coords)
    item.crop = ':'.join(map(str, coords))
    item.save()

    return JsonResponse({
        'preview_url': getattr(item.image, item.ADMIN_VARIATION).url_nocache
    })
