from django.db import models
from django.utils.translation import ugettext_lazy as _
from solo.models import SingletonModel


class MainPageConfig(SingletonModel):
    title = models.CharField('title', max_length=255)

    class Meta:
        verbose_name = _("Settings")
