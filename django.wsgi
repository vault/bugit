
import os, sys

this = os.path.dirname(os.path.abspath(__file__))

up2 = os.path.join(this, '..')

paths = [up2]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bugit.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

