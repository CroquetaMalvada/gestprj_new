"""
WSGI config for gestprjsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys
sys.path.append('c:/wsgi_app/gestprjsite/')
sys.path.append('c:/Users/minidani/Envs/gestprj/Lib/site-packages/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestprjsite.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
