from django.apps import apps
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
        dumped_apps = options.pop('app')
        database = options.pop('database')

        # exclude unmanaged models
        exclude = ['contenttypes', 'auth.Permission', 'admin.logentry']
        for model in apps.get_models():
            if not model._meta.managed:
                exclude.append('%s.%s' % (model._meta.app_label, model._meta.model_name))

        management.call_command('dumpdata',
            *dumped_apps,
            use_natural_foreign_keys=True,
            exclude=exclude,
            database=database,
            **options
        )
