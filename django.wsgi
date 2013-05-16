
import os, sys

up1 = os.path.join(os.getcwd(), '..')
up2 = os.path.join(os.getcwd(), '..', '..')

paths = [up1, up2]

for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bugit.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

