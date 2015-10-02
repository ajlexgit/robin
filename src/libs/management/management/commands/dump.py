from django.core import management


class Command(management.BaseCommand):
    """
        Алиас для команды
            pm dumpdata --natural-foreign
                        --exclude=contenttypes
                        --exclude=auth.Permission
                        --exclude=admin.logentry
    """
    help = 'Dump database data'

    def add_arguments(self, parser):
        parser.add_argument('app',
            nargs='*',
            help='Dumped applications'
        )
        parser.add_argument('--database',
            action='store',
            dest='database',
            default='default',
            help='Database alias (e.g. "default")'
        )

    def handle(self, *args, **options):
        apps = options.pop('app')
        database = options.pop('database')

        management.call_command('dumpdata',
            *apps,
            use_natural_foreign_keys=True,
            exclude=('contenttypes', 'auth.Permission', 'admin.logentry'),
            database=database,
            **options
        )
