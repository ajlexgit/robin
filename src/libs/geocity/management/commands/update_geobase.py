import os
from zipfile import ZipFile
from urllib import request, error
from django.core.management import BaseCommand
from ... import options as geocity_options


def reporthook(blocknum, bs, size):
    bar_width = 20
    
    progress = (blocknum * bs) / size
    bar_filled = round(bar_width * progress)
    line = 'Uploading... [%s>%s] %s%%\r' % (
        '='*bar_filled,
        ' '*(bar_width - bar_filled),
        int(progress * 100)
    )
    print(line, end='')


class Command(BaseCommand):
    """ Обновление базы GeoCity """
    def handle(self, *args, **options):
        try:
            filename, headers = request.urlretrieve(geocity_options.DB_UPDATE_URL, reporthook=reporthook)
        except error.HTTPError as e:
            print(e)
            return
        
        print()
        with ZipFile(filename, 'r') as zf:
            zf.extract(geocity_options.DB_NAME, os.path.dirname(geocity_options.DB_PATH))
        
        print('Done')
            