# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_block_ct(apps, schema_editor):
    AttachableReference = apps.get_model("attachable_blocks", "AttachableReference")
    for blockref in AttachableReference.objects.all():
        old_ct = blockref.block_ct
        blockref.block_ct = blockref.block.block_content_type
        if old_ct != blockref.block_ct:
            print("Corrected ContentType for blockref '%s'" % blockref.pk)
            blockref.save()


class Migration(migrations.Migration):

    dependencies = [
        ('attachable_blocks', '0002_attachablereference_block_ct'),
    ]

    operations = [
        migrations.RunPython(set_block_ct, reverse_code=lambda a, b:None)
    ]
