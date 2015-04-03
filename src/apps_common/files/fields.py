from django.db import models
from django.db.models import signals


class RemovableFileField(models.FileField):
    """ Поле файла, удаляющегося при удалении сущности, к которой он привязан """
    def post_delete(self, instance=None, **kwargs):
        field_file = getattr(instance, self.name)
        if field_file.name:
            self.storage.delete(field_file.name)
            
    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        signals.post_delete.connect(self.post_delete, sender=cls)


