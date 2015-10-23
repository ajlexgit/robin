from django.apps import apps
from django.contrib import admin
from django.views.generic import View
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse, Http404, HttpResponse
from libs.views_ajax import AjaxAdminViewMixin
from libs.upload import upload_chunked_file, TemporaryFileNotFoundError, NotLastChunk


def _get_gallery(request):
    app_label = request.POST.get('app_label')
    model_name = request.POST.get('model_name')
    gallery_model = apps.get_model(app_label, model_name)
    if not gallery_model:
        raise Http404

    try:
        gallery_id = request.POST.get('gallery_id')
    except (TypeError, ValueError):
        raise Http404

    try:
        gallery = gallery_model.objects.get(pk=gallery_id)
    except gallery_model.DoesNotExist:
        raise Http404
    else:
        return gallery


def _get_gallery_item(request, gallery):
    try:
        item_id = request.POST.get('item_id')
    except (TypeError, ValueError):
        raise Http404

    try:
        item = gallery.items.model.objects.get(pk=item_id)
    except gallery.items.model.DoesNotExist:
        raise Http404
    else:
        return item


class GalleryViewMixin:
    gallery_model = None
    gallery_id = None
    item_id = None

    def before_post(self, request):
        # Определение модели галереи
        app_label = request.POST.get('app_label')
        model_name = request.POST.get('model_name')
        try:
            self.gallery_model = apps.get_model(app_label, model_name)
        except LookupError:
            pass

        # ID галереи
        try:
            self.gallery_id = request.POST.get('gallery_id')
        except (TypeError, ValueError):
            pass

        # ID элемента
        try:
            self.item_id = request.POST.get('item_id')
        except (TypeError, ValueError):
            pass


class GalleryCreate(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Создание галереи """
    def post(self, request):
        if not self.gallery_model:
            return self.json_response({
                'message': _('Gallery model not found')
            }, status=400)

        # Создание галереи
        gallery = self.gallery_model.objects.create()

        context = {
            'gallery': gallery,
            'name': request.POST.get('field_name'),
        }
        return self.json_response({
            'gallery_id': gallery.pk,
            'html': self.render_to_string(gallery.ADMIN_TEMPLATE_ITEMS, context)
        })


class GalleryDelete(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Удаление галереи """
    def post(self, request):
        if not self.gallery_model:
            return self.json_response({
                'message': _('Gallery model not found')
            }, status=400)

        if not self.gallery_id:
            return self.json_response({
                'message': _('Gallery ID not found')
            }, status=400)

        try:
            gallery = self.gallery_model.objects.get(pk=self.gallery_id)
        except self.gallery_model.DoesNotExist:
            return self.json_response({
                'message': _('Gallery not found')
            }, status=400)

        gallery.delete()

        return self.json_response({
            'html': self.render_to_string(gallery.ADMIN_TEMPLATE_EMPTY)
        })


class GalleryUploadImage(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Загрузка картинки """
    def post(self, request):
        if not self.gallery_model:
            return self.json_response({
                'message': _('Gallery model not found')
            }, status=400)

        if not self.gallery_id:
            return self.json_response({
                'message': _('Gallery ID not found')
            }, status=400)

        try:
            gallery = self.gallery_model.objects.get(pk=self.gallery_id)
        except self.gallery_model.DoesNotExist:
            return self.json_response({
                'message': _('Gallery not found')
            }, status=400)

        try:
            uploaded_file = upload_chunked_file(request, 'image')
        except TemporaryFileNotFoundError as e:
            return self.json_response({
                'message': str(e),
            }, status=400)
        except NotLastChunk:
            return HttpResponse()

        # Создание экземпляра элемента галереи
        item = gallery.IMAGE_MODEL(
            gallery=gallery,
        )
        item.image.save(uploaded_file.name, uploaded_file, save=False)
        uploaded_file.close()

        try:
            item.full_clean()
        except ValidationError as e:
            return self.json_response({
                'message': '; '.join(e.messages),
            }, status=400)
        else:
            item.save()

        response = {
            'id': item.pk,
            'preview_url': item.admin_variation.url,
            'show_url': item.show_url,
            'source_url': item.image.url_nocache,
            'source_size': ','.join(map(str, item.image.dimensions)),
        }
        return JsonResponse(response)


class GalleryUploadVideoImage(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Загрузка видео """
    def post(self, request):
        if not self.gallery_model:
            return self.json_response({
                'message': _('Gallery model not found')
            }, status=400)

        if not self.gallery_id:
            return self.json_response({
                'message': _('Gallery ID not found')
            }, status=400)

        try:
            gallery = self.gallery_model.objects.get(pk=self.gallery_id)
        except self.gallery_model.DoesNotExist:
            return self.json_response({
                'message': _('Gallery not found')
            }, status=400)

        link = request.POST.get('link', '')

        # Создание экземпляра элемента галереи
        item = gallery.VIDEO_LINK_MODEL(
            gallery=gallery,
            video=link
        )

        try:
            item.full_clean()
        except ValidationError as e:
            return self.json_response({
                'message': '; '.join(e.messages),
            }, status=400)
        else:
            item.save()

        return self.json_response({
            'id': item.pk,
            'preview_url': item.admin_variation.url,
            'show_url': item.show_url,
        })


class GalleryDeleteItem(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Удаление элемента галереи """
    def post(self, request):
        if not self.gallery_model:
            return self.json_response({
                'message': _('Gallery model not found')
            }, status=400)

        if not self.gallery_id:
            return self.json_response({
                'message': _('Gallery ID not found')
            }, status=400)

        try:
            gallery = self.gallery_model.objects.get(pk=self.gallery_id)
        except self.gallery_model.DoesNotExist:
            return self.json_response({
                'message': _('Gallery not found')
            }, status=400)

        if not self.item_id:
            return self.json_response({
                'message': _('Item ID not found')
            }, status=400)

        try:
            item = gallery.items.model.objects.get(pk=self.item_id)
        except gallery.items.model.DoesNotExist:
            return self.json_response({
                'message': _('Item not found')
            }, status=400)

        item.delete()

        return self.json_response()


class GalleryRotateItem(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Поворот картинки """
    def post(self, request):
        if not self.gallery_model:
            return self.json_response({
                'message': _('Gallery model not found')
            }, status=400)

        if not self.gallery_id:
            return self.json_response({
                'message': _('Gallery ID not found')
            }, status=400)

        try:
            gallery = self.gallery_model.objects.get(pk=self.gallery_id)
        except self.gallery_model.DoesNotExist:
            return self.json_response({
                'message': _('Gallery not found')
            }, status=400)

        if not self.item_id:
            return self.json_response({
                'message': _('Item ID not found')
            }, status=400)

        try:
            item = gallery.items.model.objects.get(pk=self.item_id)
        except gallery.items.model.DoesNotExist:
            return self.json_response({
                'message': _('Item not found')
            }, status=400)

        if not item.is_image:
            return self.json_response({
                'message': _('Item is not image')
            }, status=400)
        elif not item.image.exists():
            return self.json_response({
                'message': _('Image is not exists')
            }, status=400)

        direction = request.GET.get('direction')
        if not direction or direction not in ('left', 'right'):
            return self.json_response({
                'message': _('Invalid rotate direction')
            }, status=400)

        if direction == 'left':
            item.image.rotate(-90)
        else:
            item.image.rotate(90)

        return self.json_response({
            'preview_url': item.admin_variation.url_nocache
        })


class GalleryCropItem(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Обрезка картинки """
    def post(self, request):
        if not self.gallery_model:
            return self.json_response({
                'message': _('Gallery model not found')
            }, status=400)

        if not self.gallery_id:
            return self.json_response({
                'message': _('Gallery ID not found')
            }, status=400)

        try:
            gallery = self.gallery_model.objects.get(pk=self.gallery_id)
        except self.gallery_model.DoesNotExist:
            return self.json_response({
                'message': _('Gallery not found')
            }, status=400)

        if not self.item_id:
            return self.json_response({
                'message': _('Item ID not found')
            }, status=400)

        try:
            item = gallery.items.model.objects.get(pk=self.item_id)
        except gallery.items.model.DoesNotExist:
            return self.json_response({
                'message': _('Item not found')
            }, status=400)

        if not item.is_image:
            return self.json_response({
                'message': _('Item is not image')
            }, status=400)
        elif not item.image.exists():
            return self.json_response({
                'message': _('Image is not exists')
            }, status=400)

        try:
            croparea = request.POST.get('coords', '')
            item.image.recut(croparea=croparea)
        except ValueError:
            return self.json_response({
                'message': _('Invalid crop coords')
            }, status=400)

        return self.json_response({
            'preview_url': item.admin_variation.url_nocache
        })


class GalleryGetItemDescr(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Получение описания """
    def post(self, request):
        if not self.gallery_model:
            return self.json_response({
                'message': _('Gallery model not found')
            }, status=400)

        if not self.gallery_id:
            return self.json_response({
                'message': _('Gallery ID not found')
            }, status=400)

        try:
            gallery = self.gallery_model.objects.get(pk=self.gallery_id)
        except self.gallery_model.DoesNotExist:
            return self.json_response({
                'message': _('Gallery not found')
            }, status=400)

        if not self.item_id:
            return self.json_response({
                'message': _('Item ID not found')
            }, status=400)

        try:
            item = gallery.items.model.objects.get(pk=self.item_id)
        except gallery.items.model.DoesNotExist:
            return self.json_response({
                'message': _('Item not found')
            }, status=400)

        if not item.is_image:
            return self.json_response({
                'message': _('Item is not image')
            }, status=400)
        elif not item.image.exists():
            return self.json_response({
                'message': _('Image is not exists')
            }, status=400)

        return self.json_response({
            'description': item.description
        })


class GallerySetItemDescr(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Установка описания """
    def post(self, request):
        if not self.gallery_model:
            return self.json_response({
                'message': _('Gallery model not found')
            }, status=400)

        if not self.gallery_id:
            return self.json_response({
                'message': _('Gallery ID not found')
            }, status=400)

        try:
            gallery = self.gallery_model.objects.get(pk=self.gallery_id)
        except self.gallery_model.DoesNotExist:
            return self.json_response({
                'message': _('Gallery not found')
            }, status=400)

        if not self.item_id:
            return self.json_response({
                'message': _('Item ID not found')
            }, status=400)

        try:
            item = gallery.items.model.objects.get(pk=self.item_id)
        except gallery.items.model.DoesNotExist:
            return self.json_response({
                'message': _('Item not found')
            }, status=400)

        if not item.is_image:
            return self.json_response({
                'message': _('Item is not image')
            }, status=400)
        elif not item.image.exists():
            return self.json_response({
                'message': _('Image is not exists')
            }, status=400)

        description = request.POST.get('description', None)
        if description is None:
            return self.json_response({
                'message': _('Invalid description')
            }, status=400)

        item.description = description
        item.save()

        return self.json_response({
            'description': item.description
        })


@admin.site.admin_view
def sort(request):
    """ Сохранение сортировки галереи """
    gallery = _get_gallery(request)

    try:
        item_ids = request.POST.get('item_ids', '').split(',')
        item_ids = map(int, item_ids)
    except (TypeError, ValueError):
        raise Http404

    for order, item_id in enumerate(item_ids, start=1):
        try:
            item = gallery.items.model.objects.get(pk=item_id)
        except gallery.items.model.DoesNotExist:
            raise Http404
        else:
            item.sort_order = order
            item.save()
    return HttpResponse()
