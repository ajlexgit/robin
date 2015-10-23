from django.conf.urls import url
from . import admin_views


urlpatterns = [
    url(r'^create/$', admin_views.GalleryCreate.as_view(), name='create'),
    url(r'^delete/$', admin_views.GalleryDelete.as_view(), name='delete'),
    url(r'^upload/$', admin_views.GalleryUploadImage.as_view(), name='upload'),
    url(r'^upload_video/$', admin_views.GalleryUploadVideoImage.as_view(), name='upload_video'),
    url(r'^delete_item/$', admin_views.GalleryDeleteItem.as_view(), name='delete_item'),
    url(r'^rotate_item/$', admin_views.GalleryRotateItem.as_view(), name='rotate_item'),
    url(r'^crop_item/$', admin_views.GalleryCropItem.as_view(), name='crop_item'),
    url(r'^get_description/$', admin_views.GalleryGetItemDescr.as_view(), name='get_description'),
    url(r'^set_description/$', admin_views.GallerySetItemDescr.as_view(), name='set_description'),

    url(r'^sort/$', admin_views.sort, name='sort'),
]
