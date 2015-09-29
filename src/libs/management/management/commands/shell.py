"""
    Добавлены доп. параметры для iPython, заглушающие мусорные строки.
    Добавлена автозагрузка модулей при старте
"""
from django.conf import settings
from django.core.management.base import NoArgsCommand


SHELL_IMPORTS = [
    ('os', ()),
    ('django.db', ('models', )),
    ('django.apps', ('apps', )),
    ('django.conf', ('settings', )),
    ('django.contrib.contenttypes.models', ('ContentType', )),
]


class Command(NoArgsCommand):
    help = "Runs a Python interactive interpreter. Tries to use IPython, if it is available."
    requires_system_checks = False

    def ipython(self):
        """Start any version of IPython"""
        try:
            from IPython import start_ipython
        except ImportError:
            pass
        else:
            imported_objects = self.import_objects()
            start_ipython(argv=['--no-banner', '--no-confirm-exit'], user_ns=imported_objects)
            return
        # no IPython, raise ImportError
        raise ImportError("No IPython")

    def import_objects(self):
        import importlib
        from django.apps import apps
        from django.utils.termcolors import colorize

        imported_objects = {}
        imports = SHELL_IMPORTS.copy()

        for app in apps.get_apps():
            if not app.__file__.startswith(settings.BASE_DIR):
                continue

            app_models = apps.get_models(app)
            if not app_models:
                continue

            app_models = [model.__name__ for model in app_models]
            imports.append((app.__name__, app_models))

        self.stdout.write('\nAutoload modules:')
        for module_name, parts in imports:
            module = importlib.import_module(module_name)
            if not parts:
                imported_objects[module_name] = module

                msg = '  import %s' % module_name
                self.stdout.write(colorize(msg, fg='green'))
            else:
                for part in parts:
                    imported_objects[part] = getattr(module, part)
                msg = '  from %s import %s' % (module_name, ', '.join(parts))
                self.stdout.write(colorize(msg, fg='green'))

        return imported_objects

    def add_arguments(self, parser):
        parser.add_argument('-p', '--plain',
            action='store_true',
            dest='plain',
            help='Tells Django to use plain Python, not IPython or bpython.'
        )

        parser.add_argument('--no-startup',
            action='store_true',
            dest='no_startup',
            help='When using plain Python, ignore the PYTHONSTARTUP environment variable and ~/.pythonrc.py script.'
        )

    def handle_noargs(self, **options):
        import os

        use_plain = options.get('plain', False)
        no_startup = options.get('no_startup', False)

        try:
            if use_plain:
                # Don't bother loading IPython, because the user wants plain Python.
                raise ImportError

            self.ipython()
        except ImportError:
            import code
            # Set up a dictionary to serve as the environment for the shell, so
            # that tab completion works on objects that are imported at runtime.
            # See ticket 5082.
            imported_objects = {}
            try:  # Try activating rlcompleter, because it's handy.
                import readline
            except ImportError:
                pass
            else:
                # We don't have to wrap the following import in a 'try', because
                # we already know 'readline' was imported successfully.
                import rlcompleter
                readline.set_completer(rlcompleter.Completer(imported_objects).complete)
                readline.parse_and_bind("tab:complete")

            # We want to honor both $PYTHONSTARTUP and .pythonrc.py, so follow system
            # conventions and get $PYTHONSTARTUP first then .pythonrc.py.
            if not no_startup:
                for pythonrc in (os.environ.get("PYTHONSTARTUP"), '~/.pythonrc.py'):
                    if not pythonrc:
                        continue
                    pythonrc = os.path.expanduser(pythonrc)
                    if not os.path.isfile(pythonrc):
                        continue
                    try:
                        with open(pythonrc) as handle:
                            exec(compile(handle.read(), pythonrc, 'exec'), imported_objects)
                    except NameError:
                        pass
            code.interact(local=imported_objects)
