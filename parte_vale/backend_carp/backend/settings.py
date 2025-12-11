"""
Django settings for backend project.
"""

import os
import dj_database_url
from pathlib import Path
from datetime import timedelta
DEBUG = os.getenv("RENDER", False) != "1"

# ------------------------
# BASE DIR
# ------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------
# CONFIGURACIÓN GENERAL
# ------------------------
SECRET_KEY = 'django-insecure-waf*a8z8*n*9zb*jyuh4vu52q&)hk4a2*tvvbjb_%^^9!b9x$e'
DEBUG = True

# Para Render (permite acceso externo)
ALLOWED_HOSTS = ['*']


# ------------------------
# APPS INSTALADAS
# ------------------------
INSTALLED_APPS = [
    # apps Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # apps externas
    'rest_framework',
    'rest_framework_simplejwt',

    # tu app personalizada
    'users.apps.UsersConfig',
]


# ------------------------
# MIDDLEWARE
# ------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # ⭐ Permite servir archivos estáticos en producción (Render)
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ------------------------
# URL PRINCIPAL
# ------------------------
ROOT_URLCONF = 'backend.urls'


# ------------------------
# TEMPLATES
# ------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # contexto extra para reservas
                'users.context_processors.reservas_usuario',
            ],
        },
    },
]


# ------------------------
# WSGI
# ------------------------
WSGI_APPLICATION = 'backend.wsgi.application'
# ------------------------
# BASE DE DATOS
# ------------------------

# Render define la variable de entorno RENDER=1
IS_RENDER = os.getenv("RENDER") == "1"

if IS_RENDER:
    # Producción → PostgreSQL en Render
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    # Local → SQLite sin errores
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / "db.sqlite3",
        }
    }

# ------------------------
# VALIDADORES DE CONTRASEÑA
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ------------------------
# INTERNACIONALIZACIÓN
# ------------------------
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True


# ------------------------
# ARCHIVOS ESTÁTICOS
# ------------------------
STATIC_URL = '/static/'

# Archivos estáticos del proyecto
STATICFILES_DIRS = [BASE_DIR / "static"]

# Carpeta donde Django guardará los archivos recopilados
STATIC_ROOT = BASE_DIR / "staticfiles"

# ⭐ WhiteNoise: servir archivos comprimidos en Render
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ------------------------
# ARCHIVOS MULTIMEDIA (IMÁGENES)
# ------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"


# ------------------------
# DEFAULT AUTO FIELD
# ------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ------------------------
# CONFIG REST FRAMEWORK
# ------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


# ------------------------
# CONFIG JWT
# ------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
}

LOGIN_URL = 'login'

