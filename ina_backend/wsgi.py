"""
WSGI config for ina_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os, sys, django
from django.core.wsgi import get_wsgi_application

print(django.__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ina_backend.settings")

application = get_wsgi_application()
