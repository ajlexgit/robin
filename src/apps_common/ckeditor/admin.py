from django.apps import apps
from django.contrib import admin
from django.utils.html import escapejs
from django.core.exceptions import ValidationError
from django.contrib.admin.options import IS_POPUP_VAR
from django.http import JsonResponse, Http404, HttpResponse
from django.template.response import SimpleTemplateResponse
from libs.upload import upload_chunked_file, TemporaryFileNotFoundError, NotLastChunk
from .models import PagePhoto, SimplePhoto, generate_tag


@admin.register(PagePhoto)
class PagePhotoAdmin(admin.ModelAdmin):
    exclude = ('app_name', 'model_name', 'instance_id')

    class Media:
        js = (
            'admin/js/jquery-ui.min.js',
            'admin/js/jquery.Jcrop.js',
        )
        css = {
            'all': (
                'admin/css/jquery-ui/jquery-ui.min.css',
                'admin/css/jcrop/jquery.Jcrop.css',
            )
        }

    def response_change(self, request, obj):
        if IS_POPUP_VAR in request.POST:
            return SimpleTemplateResponse('ckeditor/popup_response.html', {
                'newTag': escapejs(generate_tag(obj, random_param=True)),
            })

        return super(PagePhotoAdmin, self).response_change(request, obj)


@admin.site.admin_view
def upload_pagephoto(request):
    """
        Функция, принимающая файлы, загружаемые через CKEditor.
        Может вызываться несколько раз для одного файла, если он разбит на части.
    """
    app_label = request.GET.get('app_label')
    model_name = request.GET.get('model_name')
    field_name = request.GET.get('field_name')

    instance_model = apps.get_model(app_label, model_name)
    if not instance_model:
        raise Http404

    try:
        uploaded_file = upload_chunked_file(request, 'image')
    except TemporaryFileNotFoundError:
        raise Http404
    except NotLastChunk:
        return HttpResponse()

    # Создание экземпляра элемента галереи
    pagephoto = PagePhoto(
        app_name=app_label,
        model_name=model_name,
    )
    pagephoto.photo.save(uploaded_file.name, uploaded_file, save=False)
    uploaded_file.close()

    try:
        pagephoto.photo.field.clean(pagephoto.photo, pagephoto)
    except ValidationError as e:
        pagephoto.photo.delete(save=False)
        return JsonResponse({
            'message': ', '.join(e.messages),
        }, status=400)

    pagephoto.clean()
    pagephoto.save()

    return JsonResponse({
        'tag': generate_tag(pagephoto),
        'field': field_name,
        'id': pagephoto.pk,
    })


@admin.site.admin_view
def upload_simplephoto(request):
    """
        Функция, принимающая файлы, загружаемые через CKEditor.
        Может вызываться несколько раз для одного файла, если он разбит на части.
    """
    app_label = request.GET.get('app_label')
    model_name = request.GET.get('model_name')
    field_name = request.GET.get('field_name')

    instance_model = apps.get_model(app_label, model_name)
    if not instance_model:
        raise Http404

    try:
        uploaded_file = upload_chunked_file(request, 'image')
    except TemporaryFileNotFoundError:
        raise Http404
    except NotLastChunk:
        return HttpResponse()


    # Создание экземпляра элемента галереи
    simplephoto = SimplePhoto(
        app_name=app_label,
        model_name=model_name,
    )
    simplephoto.photo.save(uploaded_file.name, uploaded_file, save=False)
    uploaded_file.close()

    try:
        simplephoto.photo.field.clean(simplephoto.photo, simplephoto)
    except ValidationError as e:
        simplephoto.photo.delete(save=False)
        return JsonResponse({
            'message': ', '.join(e.messages),
        }, status=400)

    simplephoto.clean()
    simplephoto.save()

    return JsonResponse({
        'url': simplephoto.photo.url,
        'field': field_name,
        'id': simplephoto.pk,
    })
