import os
import subprocess
from django.core.management.base import NoArgsCommand

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        subprocess.call('sh %s/init.sh' % CURRENT_DIR, shell=True)