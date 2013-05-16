
import os, sys
paths = ['/srv/bugit/bugit', '/srv/bugit']
for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bugit.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
