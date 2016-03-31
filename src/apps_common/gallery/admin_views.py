from django.apps import apps
from django.views.generic import View
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.http import JsonResponse, Http404
from libs.views_ajax import AjaxAdminViewMixin, JSONError
from libs.upload import upload_chunked_file, TemporaryFileNotFoundError, NotLastChunk


class GalleryViewMixin:
    gallery_model = None
    require_gallery_model = True

    gallery = None
    require_gallery = False

    item = None
    require_item = False

    def post(self, request):
        # Определение модели галереи
        app_label = request.POST.get('app_label')
        model_name = request.POST.get('model_name')
        try:
            self.gallery_model = apps.get_model(app_label, model_name)
        except LookupError:
            if self.require_gallery_model:
                raise JSONError({
                    'message': _('Gallery model not found')
                })

        # Галерея
        try:
            gallery_id = int(request.POST.get('gallery_id'))
        except (TypeError, ValueError):
            gallery_id = 0
            if self.require_gallery:
                raise JSONError({
                    'message': _('Gallery not found')
                })

        try:
            self.gallery = self.gallery_model.objects.get(pk=gallery_id)
        except self.gallery_model.DoesNotExist:
            if self.require_gallery:
                raise JSONError({
                    'message': _('Gallery not found')
                })

        # Элемент
        if self.gallery:
            try:
                item_id = int(request.POST.get('item_id'))
            except (TypeError, ValueError):
                item_id = 0
                if self.require_item:
                    raise JSONError({
                        'message': _('Item not found')
                    })

            try:
                self.item = self.gallery.items.model.objects.get(pk=item_id)
            except self.gallery.items.model.DoesNotExist:
                if self.require_item:
                    raise JSONError({
                        'message': _('Item not found')
                    })


class GalleryCreate(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Создание галереи """
    require_gallery_model = True

    def post(self, request):
        super().post(request)

        # Создание галереи
        gallery = self.gallery_model.objects.create()

        return self.json_response({
            'gallery_id': gallery.pk,
            'html': self.render_to_string(gallery.ADMIN_TEMPLATE_ITEMS, {
                'gallery': gallery,
                'name': request.POST.get('field_name'),
            })
        })


class GalleryDelete(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Удаление галереи """
    require_gallery_model = True
    require_gallery = True

    def post(self, request):
        super().post(request)
        self.gallery.delete()
        return self.json_response({
            'html': self.render_to_string(self.gallery.ADMIN_TEMPLATE_EMPTY)
        })


class UploadImage(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Загрузка картинки """
    require_gallery_model = True
    require_gallery = True

    def post(self, request):
        super().post(request)

        try:
            uploaded_file = upload_chunked_file(request, 'image')
        except TemporaryFileNotFoundError as e:
            return self.json_response({
                'message': str(e),
            }, status=400)
        except NotLastChunk:
            return self.json_response()

        # Создание экземпляра элемента галереи
        item = self.gallery.IMAGE_MODEL(
            gallery=self.gallery,
        )
        item.image.save(uploaded_file.name, uploaded_file, save=False)
        uploaded_file.close()

        try:
            item.full_clean()
        except ValidationError as e:
            item.image.delete(save=False)
            return self.json_response({
                'message': '; '.join(e.messages),
            }, status=400)
        else:
            item.save()

        try:
            self.gallery.clean()
        except ValidationError as e:
            item.delete()
            return self.json_response({
                'message': '; '.join(e.messages),
            }, status=400)

        response = {
            'id': item.pk,
            'preview_url': item.admin_variation.url,
            'show_url': item.admin_show_url,
            'source_url': item.image.url_nocache,
            'source_size': ','.join(map(str, item.image.dimensions)),
        }
        return JsonResponse(response)


class UploadVideoImage(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Загрузка видео """
    require_gallery_model = True
    require_gallery = True

    def post(self, request):
        super().post(request)

        # Создание экземпляра элемента галереи
        item = self.gallery.VIDEO_LINK_MODEL(
            gallery=self.gallery,
            video=request.POST.get('link', '')
        )

        try:
            item.full_clean()
        except ValidationError as e:
            item.video_preview.delete(save=False)
            return self.json_response({
                'message': '; '.join(e.messages),
            }, status=400)
        else:
            item.save()

        try:
            self.gallery.clean()
        except ValidationError as e:
            item.delete()
            return self.json_response({
                'message': '; '.join(e.messages),
            }, status=400)

        return self.json_response({
            'id': item.pk,
            'preview_url': item.admin_variation.url,
            'show_url': item.admin_show_url,
        })


class DeleteItem(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Удаление элемента галереи """
    require_gallery_model = True
    require_gallery = True
    require_item = True

    def post(self, request):
        super().post(request)
        self.item.delete()
        return self.json_response()


class RotateItem(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Поворот картинки """
    require_gallery_model = True
    require_gallery = True
    require_item = True

    def post(self, request):
        super().post(request)

        if not self.item.is_image:
            return self.json_response({
                'message': _('Item is not image')
            }, status=400)
        elif not self.item.image.exists():
            return self.json_response({
                'message': _('Image is not exists')
            }, status=400)

        direction = request.GET.get('direction')
        if not direction or direction not in ('left', 'right'):
            return self.json_response({
                'message': _('Invalid rotate direction')
            }, status=400)

        if direction == 'left':
            self.item.image.rotate(-90)
        else:
            self.item.image.rotate(90)

        return self.json_response({
            'preview_url': self.item.admin_variation.url_nocache
        })


class CropItem(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Обрезка картинки """
    require_gallery_model = True
    require_gallery = True
    require_item = True

    def post(self, request):
        super().post(request)

        if not self.item.is_image:
            return self.json_response({
                'message': _('Item is not image')
            }, status=400)
        elif not self.item.image.exists():
            return self.json_response({
                'message': _('Image is not exists')
            }, status=400)

        try:
            croparea = request.POST.get('coords', '')
            self.item.image.recut(croparea=croparea)
        except ValueError:
            return self.json_response({
                'message': _('Invalid crop coords')
            }, status=400)

        return self.json_response({
            'preview_url': self.item.admin_variation.url_nocache
        })


class GetItemDescr(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Получение описания """
    require_gallery_model = True
    require_gallery = True
    require_item = True

    def post(self, request):
        super().post(request)

        if self.item.is_image and not self.item.image.exists():
            return self.json_response({
                'message': _('Image is not exists')
            }, status=400)

        return self.json_response({
            'description': self.item.description
        })


class SetItemDescr(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Установка описания """
    require_gallery_model = True
    require_gallery = True
    require_item = True

    def post(self, request):
        super().post(request)

        if self.item.is_image and not self.item.image.exists():
            return self.json_response({
                'message': _('Image is not exists')
            }, status=400)

        description = request.POST.get('description', None)
        if description is None:
            return self.json_response({
                'message': _('Invalid description')
            }, status=400)

        self.item.description = description
        self.item.save()

        return self.json_response({
            'description': self.item.description
        })


class SortItems(GalleryViewMixin, AjaxAdminViewMixin, View):
    """ Установка описания """
    require_gallery_model = True
    require_gallery = True

    def post(self, request):
        super().post(request)

        try:
            item_ids = request.POST.get('item_ids', '').split(',')
            item_ids = map(int, item_ids)
        except (TypeError, ValueError):
            raise Http404

        for order, item_id in enumerate(item_ids, start=1):
            try:
                item = self.gallery.items.model.objects.get(pk=item_id)
            except self.gallery.items.model.DoesNotExist:
                return self.json_response({
                    'message': _('Gallery item #%s not found' % item_id)
                }, status=400)
            else:
                item.sort_order = order
                item.save()

        return self.json_response()
