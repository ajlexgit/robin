from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
    name = 'attachable_blocks'
    verbose_name = _('Attachable blocks')

    def ready(self):
        from django.apps import apps
        from django.core.cache import cache
        from django.contrib.contenttypes.models import ContentType

        # All block types
        blocks = []
        AttachableBlock = self.get_model('AttachableBlock')
        for model in apps.get_models():
            if issubclass(model, AttachableBlock) and model != AttachableBlock:
                ct = ContentType.objects.get_for_model(model)
                blocks.append((ct.pk, str(model._meta.verbose_name)))

        blocks = tuple(sorted(blocks, key=lambda x: x[1]))
        cache.set('attachable_block_types', blocks, timeout=-1)
