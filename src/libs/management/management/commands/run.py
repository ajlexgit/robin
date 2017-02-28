import inspect
import importlib
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
        Команда, запускающая скрипты на Python в окружении Django.

        В качестве пути к скрипту указывается:
            1) имя файла, если он лежит по-соседству с manage.py:
                "pm run do_something"
                -- запустит файл "do_something.py"
            2) Python-путь к модулю:
                "pm run application.scripts.do_something app2.do_more"
                -- запустит два скрипта по очереди

        Точкой входа в скрипте служит сам модуль или функция run(), если она определена.
        Точку входа можно переопределить параметром entry.
    """
    def add_arguments(self, parser):
        parser.add_argument('script', nargs='+')
        parser.add_argument('-e', '--entry', nargs='?', type=str, action='store', dest='entry', default='run')
        parser.add_argument(
            '--script-args',
            nargs='*',
            type=str,
            help='Space-separated argument list to be passed to the scripts. Note that the '
                 'same arguments will be passed to all named scripts.',
        )

    def handle(self, *args, **options):
        scripts = options['script']
        entry = options['entry']
        script_args = options.get('script_args') or ()

        for script in scripts:
            try:
                module = importlib.import_module(script)
            except ImportError as e:
                print("No (valid) module for script '%s' found" % script)
            else:
                run_func = getattr(module, entry, None)
                if run_func and inspect.isfunction(run_func):
                    run_func(*script_args)
