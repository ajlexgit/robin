from django.conf.urls import url
from . import admin

urlpatterns = [
    url(r'^upload_pagephoto/$', view=admin.upload_pagephoto, name='upload_pagephoto'),
    url(r'^upload_pagefile/$', view=admin.upload_pagefile, name='upload_pagefile'),
    url(r'^upload_simplephoto/$', view=admin.upload_simplephoto, name='upload_simplephoto'),
]
