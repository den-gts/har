# -*- coding: utf-8 -*-
import webbrowser, time, sys, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'har.settings'
import django
import har.settings

from django.core.servers.basehttp import run, AdminMediaHandler, WSGIServerException
from django.core.handlers.wsgi import WSGIHandler

class DummyFile(object):
    def write(*a, **kw): pass

if __name__ == "__main__":


    port = 8000
    out = sys.stdout
    import cards.admin

    from django.conf import settings
    try:
        path = 'adminmedia/'
        handler = AdminMediaHandler(WSGIHandler(), path)

        #sys.stderr = sys.stdout = DummyFile()
        webbrowser.open('http://localhost:%s/search/' % port) #mmm
        run('0.0.0.0', port, handler)
    except WSGIServerException, e:
        # Use helpful error messages instead of ugly tracebacks.
        ERRORS = {
            13: "You don't have permission to access that port.",
            98: "That port is already in use.",
            99: "That IP address can't be assigned-to.",
            }
        try:
            error_text = ERRORS[e.args[0].args[0]]
            sys.stderr.write("Error: %s \n" % error_text)
        except (AttributeError, KeyError):
            error_text = str(e)