from django.core.management import BaseCommand
from django.contrib.contenttypes.models import ContentType
from ...models import AttachableReference, AttachableBlock


class Command(BaseCommand):
    """
        Установка block_ct для AttachableReference
    """
    def handle(self, *args, **options):
        for blockref in AttachableReference.objects.all():
            old_ct = blockref.block_ct

            block = AttachableBlock.objects.filter(pk=blockref.block_id).select_subclasses().first()
            blockref.block_ct = ContentType.objects.get_for_model(block)

            if old_ct != blockref.block_ct:
                print("Corrected ContentType for '%s'" % blockref)
                blockref.save()