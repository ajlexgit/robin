import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class MediaStorage(FileSystemStorage):
    """
        Файловое хранилище в папке media
    """
    def __init__(self, directory=''):
        location = None
        base_url = None
        directory = directory.strip(' /')
        if directory:
            location = os.path.join(settings.MEDIA_ROOT, directory)
            base_url = '%s%s/' % (settings.MEDIA_URL, directory.strip(' /'))
        super().__init__(location, base_url)

    def set_directory(self, directory):
        """ Динамическое изменение директории """
        directory = directory.strip(' /')
        if directory:
            self.base_location = self.location = os.path.join(settings.MEDIA_ROOT, directory)
            self.base_url = '%s%s/' % (settings.MEDIA_URL, directory.strip(' /'))
        else:
            raise ValueError('empty directory in MediaStorage')
