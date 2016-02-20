import os
import subprocess
from django.utils.encoding import smart_bytes
from pipeline.conf import settings
from pipeline.compilers import SubProcessCompiler
from pipeline.exceptions import CompilerError


class SASSCCompiler(SubProcessCompiler):
    """
        Класс для компилирования JS и CSS через sassc.
        В settings.py необходимо добавить:
            PIPELINE_CSS_COMPRESSOR = ''
            PIPELINE_JS_COMPRESSOR = ''
            PIPELINE_COMPILERS = (
                'libs.sassc.SASSCCompiler',
            )
            SASS_INCLUDE_DIR = BASE_DIR + '/static/scss/'
            PIPELINE_SASS_BINARY = '/usr/bin/env sassc --load-path ' + SASS_INCLUDE_DIR
            PIPELINE_SASS_ARGUMENTS = '-t nested'
            STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
    """
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
            raise CompilerError(stderr)

        if self.verbose:
            print(stderr)

        if pipe.returncode != 0:
            raise CompilerError("Command '{0}' returned non-zero exit status {1}".format(command, pipe.returncode))

        return stdout

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = "%s %s %s" % (
            settings.PIPELINE_SASS_BINARY,
            settings.PIPELINE_SASS_ARGUMENTS,
            infile
        )
        try:
            output = self.execute_command(command, cwd=os.path.dirname(infile))
        except CompilerError:
            print('CompilerError at file: %s' % infile)
            raise
        else:
            output = output.decode('utf-8-sig')
            with open(outfile, 'w+') as f:
                f.write(output)

