
import os, sys
paths = ['/home/mgabed/bugit', '/home/mgabed']
for path in paths:
    if path not in sys.path:
        sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'bugit.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
