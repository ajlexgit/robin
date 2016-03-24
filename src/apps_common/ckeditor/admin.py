from django.apps import apps
from django.contrib import admin
from django.forms.utils import flatatt
from django.utils.html import escapejs
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.admin.options import IS_POPUP_VAR
from django.http import JsonResponse, Http404, HttpResponse
from django.template.response import SimpleTemplateResponse
from project.admin import ModelAdminMixin
from libs.upload import upload_chunked_file, TemporaryFileNotFoundError, NotLastChunk
from .models import PagePhoto, PageFile, SimplePhoto


def pagephoto_tag(instance, nocache=False):
    attrs = flatatt({
        'src': instance.photo.normal.url_nocache if nocache else instance.photo.normal.url,
        'srcset': ', '.join((
            instance.photo.wide.srcset_nocache,
            instance.photo.normal.srcset_nocache,
            instance.photo.mobile.srcset_nocache
        )),
        'width': instance.photo.normal.width,
        'height': instance.photo.normal.height,
        'sizes': '100vw',
    })

    return """<img data-id="{id}" alt="" {attrs}>""".format(
        id=instance.id,
        attrs=attrs,
    )


@admin.register(PagePhoto)
class PagePhotoAdmin(ModelAdminMixin, admin.ModelAdmin):
    exclude = ('app_name', 'model_name', 'instance_id')

    class Media:
        js = (
            'admin/js/jquery-ui.min.js',
            'common/js/jquery.Jcrop.js',
        )
        css = {
            'all': (
                'admin/css/jquery-ui/jquery-ui.min.css',
                'common/css/jcrop/jquery.Jcrop.css',
            )
        }

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return False

    def response_change(self, request, obj):
        if IS_POPUP_VAR in request.POST:
            return SimpleTemplateResponse('ckeditor/popup_response.html', {
                'newTag': escapejs(pagephoto_tag(obj, nocache=True)),
                'newId': obj.id,
            })

        return super().response_change(request, obj)


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
        pagephoto.full_clean()
    except ValidationError as e:
        pagephoto.photo.delete(save=False)
        return JsonResponse({
            'message': ', '.join(e.messages),
        }, status=400)
    else:
        pagephoto.save()

    return JsonResponse({
        'tag': pagephoto_tag(pagephoto),
        'field': field_name,
        'id': pagephoto.pk,
    })


def pagefile_tag(instance):
    return """
        <div class="page-file" data-id="{id}">
            <a href="{url}">{display}</a>
        </div>
    """.format(
        id=instance.id,
        url=reverse('ckeditor:download_pagefile', kwargs={
            'file_id': instance.pk,
        }),
        display=instance.file.name,
    )


@admin.register(PageFile)
class PageFileAdmin(ModelAdminMixin, admin.ModelAdmin):
    exclude = ('app_name', 'model_name', 'instance_id')

    class Media:
        js = (
            'admin/js/jquery-ui.min.js',
            'common/js/jquery.Jcrop.js',
        )
        css = {
            'all': (
                'admin/css/jquery-ui/jquery-ui.min.css',
                'common/css/jcrop/jquery.Jcrop.css',
            )
        }

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return False

    def response_change(self, request, obj):
        if IS_POPUP_VAR in request.POST:
            return SimpleTemplateResponse('ckeditor/popup_response.html', {
                'newTag': escapejs(pagefile_tag(obj)),
                'newId': obj.id,
            })

        return super().response_change(request, obj)


@admin.site.admin_view
def upload_pagefile(request):
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
        uploaded_file = upload_chunked_file(request, 'file')
    except TemporaryFileNotFoundError:
        raise Http404
    except NotLastChunk:
        return HttpResponse()

    # Создание экземпляра элемента галереи
    pagefile = PageFile(
        app_name=app_label,
        model_name=model_name,
    )
    pagefile.file.save(uploaded_file.name, uploaded_file, save=False)
    uploaded_file.close()

    try:
        pagefile.full_clean()
    except ValidationError as e:
        pagefile.photo.delete(save=False)
        return JsonResponse({
            'message': ', '.join(e.messages),
        }, status=400)
    else:
        pagefile.save()

    return JsonResponse({
        'tag': pagefile_tag(pagefile),
        'field': field_name,
        'id': pagefile.pk,
    })


def simplephoto_tag(instance, nocache=False):
    attrs = flatatt({
        'src': instance.photo.url_nocache if nocache else instance.photo.url,
        'srcset': ', '.join((
            instance.photo.srcset_nocache,
            instance.photo.mobile.srcset_nocache
        )),
        'width': instance.photo.width,
        'height': instance.photo.height,
        'sizes': '100vw',
    })

    return """<img data-id="{id}" alt="" {attrs}>""".format(
        id=instance.id,
        attrs=attrs,
    )


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
        simplephoto.full_clean()
    except ValidationError as e:
        simplephoto.photo.delete(save=False)
        return JsonResponse({
            'message': ', '.join(e.messages),
        }, status=400)
    else:
        simplephoto.save()

    return JsonResponse({
        'tag': simplephoto_tag(simplephoto),
        'field': field_name,
        'id': simplephoto.pk,
    })
