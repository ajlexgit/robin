import os
import time
import subprocess
from django.utils.encoding import smart_bytes
from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler
from pipeline.exceptions import CompilerError


class SASSCMetaclass(type):
    def __init__(cls, name, bases, nmspc):
        super().__init__(name, bases, nmspc)
        cls.start = time.time()


class SASSCCompiler(SubProcessCompiler, metaclass=SASSCMetaclass):
    """
        Класс для компилирования JS и CSS через sassc.
        В settings.py необходимо добавить:
            SASS_INCLUDE_DIR = BASE_DIR + '/static/scss/'
            PIPELINE['SASS_BINARY'] = '/usr/bin/env sassc --load-path ' + SASS_INCLUDE_DIR
            PIPELINE['SASS_ARGUMENTS'] = '-t nested'
            PIPELINE['COMPILERS'] = (
                'libs.sassc.SASSCCompiler',
            )
            STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
    """
    start = None
    output_extension = 'css'

    def match_file(self, filename):
        return filename.endswith('.scss')

    def execute_command(self, command, content=None, cwd=None):
        pipe = subprocess.Popen(command, shell=True, cwd=cwd,
                                stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if content:
            content = smart_bytes(content)
        stdout, stderr = pipe.communicate(content)

        if isinstance(stderr, bytes):
            try:
                stderr = stderr.decode()
            except UnicodeDecodeError:
                pass

        if stderr.strip():
            raise CompilerError(stderr, error_output=stderr)

        if self.verbose:
            print(stderr)

        if pipe.returncode != 0:
            msg = "Command '{0}' returned non-zero exit status {1}".format(command, pipe.returncode)
            raise CompilerError(msg, error_output=msg)

        return stdout

    def compile_file(self, infile, outfile, outdated=False, force=False):
        if os.path.isfile(outfile):
            # Уже есть свежий скомпиленный файл
            if os.stat(outfile).st_mtime > self.start:
                return

        command = "%s %s %s" % (
            ' '.join(settings.SASS_BINARY),
            ' '.join(settings.SASS_ARGUMENTS),
            infile
        )
        try:
            output = self.execute_command(command, cwd=os.path.dirname(infile))
        except CompilerError:
            print('CompilerError at file: %s' % infile)
            raise
        else:
            output = output.decode('utf-8-sig')
            with open(outfile, 'w+', encoding='utf-8') as f:
                f.write(output)
