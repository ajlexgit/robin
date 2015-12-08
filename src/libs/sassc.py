import os
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

    def compile_file(self, infile, outfile, outdated=False, force=False):
        command = "%s %s %s > %s" % (
            settings.PIPELINE_SASS_BINARY,
            settings.PIPELINE_SASS_ARGUMENTS,
            infile,
            outfile
        )
        try:
            return self.execute_command(command, cwd=os.path.dirname(infile))
        except CompilerError:
            print('CompilerError at file: %s' % infile)
            raise
