from django.core import management
from optparse import make_option

# pm dumpdata --natural --exclude=contenttypes --exclude=auth.Permission --exclude=admin.logentry

class Command(management.BaseCommand):

    option_list = management.BaseCommand.option_list + (
        make_option('--database', action='store', dest='database', default='default', help='База данных'),
    )

    def handle(self, *args, **options):
        management.call_command('dumpdata',
            *args,
            natural=True,
            exclude=('contenttypes', 'auth.Permission', 'admin.logentry'),
            **options
        )
