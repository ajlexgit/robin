import re
import random
from .models import Banner


class PopupBannerMiddleware:
    @staticmethod
    def process_request(request):
        banners = []
        for banner in Banner.objects.filter(active=True):
            for regex in banner.pages.values_list('regex', flat=True):
                if re.fullmatch(r'^%s$' % regex.replace('*', '.*'), request.path_info):
                    banners.append(banner)
                    break

        if not banners:
            return

        js_storage = getattr(request, 'js_storage', None)
        if js_storage is None:
            raise RuntimeError('PopupBannerMiddleware should be after JsStorageMiddleware')

        banner = random.choice(banners)
        js_storage.update({
            'popup_banner_id': banner.pk,
            'popup_banner_timeout': banner.timeout,
            'popup_show_type': banner.show_type,
        })

