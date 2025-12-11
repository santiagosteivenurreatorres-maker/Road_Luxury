"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
# Cargar datos iniciales en Render automáticamente
try:
    from .load_initial_data import load_initial_data
    load_initial_data()
except Exception as e:
    print(f"Error cargando datos iniciales: {e}")
