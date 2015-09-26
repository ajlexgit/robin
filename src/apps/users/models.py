from django.db import models
from django.templatetags.static import static
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from libs.stdimage import StdImageField
from libs.media_storage import MediaStorage
from . import options


class CustomUser(AbstractUser):
    avatar = StdImageField(_('avatar'),
        storage = MediaStorage(options.AVATAR_PATH),
        blank = True,
        admin_variation = 'normal',
        min_dimensions = options.AVATAR_NORMAL,
        crop_area = True,
        aspects = 'normal',
        variations = dict(
            normal=dict(
                size=options.AVATAR_NORMAL,
            ),
            small=dict(
                size=options.AVATAR_SMALL,
            ),
            micro=dict(
                size=options.AVATAR_MICRO,
            ),
        ),
    )

    @property
    def normal_avatar(self):
        if self.avatar:
            return self.avatar.normal.url_nocache
        else:
            return static('users/img/default_150x150.png')

    @property
    def small_avatar(self):
        if self.avatar:
            return self.avatar.small.url_nocache
        else:
            return static('users/img/default_50x50.png')

    @property
    def micro_avatar(self):
        if self.avatar:
            return self.avatar.micro.url_nocache
        else:
            return static('users/img/default_32x32.png')
