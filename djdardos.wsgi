import os
import sys

#Para que encuentre djdardos.basic.xxxx
path = '/home/perriman/dev'
if path not in sys.path:
    sys.path.append(path)

#Para que encuentre dardos.xxxx
path = '/home/perriman/dev/djdardos'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
