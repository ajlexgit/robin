"""
    TODO: Весь этот только код ради того, чтобы заменить WSGIRequestHandler
    на SlimWSGIRequestHandler
"""
import os
import sys
import errno
import socket
import socketserver
from datetime import datetime

import six
from django.conf import settings
from django.core.servers.basehttp import WSGIServer
from django.utils.encoding import get_system_encoding, force_text
from django.core.exceptions import ImproperlyConfigured
from django.core.management.commands.runserver import Command as BaseCommand
from django.contrib.staticfiles.handlers import StaticFilesHandler

from .http import SlimWSGIRequestHandler


def run(addr, port, wsgi_handler, ipv6=False, threading=False):
    server_address = (addr, port)
    if threading:
        httpd_cls = type(str('WSGIServer'), (socketserver.ThreadingMixIn, WSGIServer), {})
    else:
        httpd_cls = WSGIServer
    httpd = httpd_cls(server_address, SlimWSGIRequestHandler, ipv6=ipv6)
    httpd.set_app(wsgi_handler)
    httpd.serve_forever()


class Command(BaseCommand):
    def get_handler(self, *args, **options):
        handler = super().get_handler(*args, **options)

        if 'django.contrib.staticfiles' in settings.INSTALLED_APPS:
            handler = StaticFilesHandler(handler)

        return handler

    def inner_run(self, *args, **options):
        from django.utils import translation

        threading = options.get('use_threading')
        shutdown_message = options.get('shutdown_message', '')
        quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'

        self.stdout.write("Performing system checks...\n\n")
        self.validate(display_num_errors=True)
        try:
            self.check_migrations()
        except ImproperlyConfigured:
            pass
        now = datetime.now().strftime('%B %d, %Y - %X')
        if six.PY2:
            now = now.decode(get_system_encoding())
        self.stdout.write((
            "%(started_at)s\n"
            "Django version %(version)s, using settings %(settings)r\n"
            "Starting development server at http://%(addr)s:%(port)s/\n"
            "Quit the server with %(quit_command)s.\n"
        ) % {
            "started_at": now,
            "version": self.get_version(),
            "settings": settings.SETTINGS_MODULE,
            "addr": '[%s]' % self.addr if self._raw_ipv6 else self.addr,
            "port": self.port,
            "quit_command": quit_command,
        })
        # django.core.management.base forces the locale to en-us. We should
        # set it up correctly for the first request (particularly important
        # in the "--noreload" case).
        translation.activate(settings.LANGUAGE_CODE)

        try:
            handler = self.get_handler(*args, **options)
            run(self.addr, int(self.port), handler,
                ipv6=self.use_ipv6, threading=threading)
        except socket.error as e:
            # Use helpful error messages instead of ugly tracebacks.
            ERRORS = {
                errno.EACCES: "You don't have permission to access that port.",
                errno.EADDRINUSE: "That port is already in use.",
                errno.EADDRNOTAVAIL: "That IP address can't be assigned-to.",
            }
            try:
                error_text = ERRORS[e.errno]
            except KeyError:
                error_text = force_text(e)
            self.stderr.write("Error: %s" % error_text)
            # Need to use an OS exit because sys.exit doesn't work in a thread
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)
