import os
from os import environ as env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = env.get("SECRET_KEY")

ALLOWED_HOSTS = ["localhost"]
DEBUG = bool(env.get("DEBUG"))

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'api',
]

MIDDLEWARE = [
]# Create your tests here.


ROOT_URLCONF = 'rest.urls'

TEMPLATES = [
]

WSGI_APPLICATION = 'rest.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.postgresql',
        'NAME'    : 'postgres',
        'USER'    : 'postgres',
        'PASSWORD': env.get("POSTGRES_PASSWORD"),
        'HOST'    : env.get("POSTGRES_HOST"),
        'PORT'    : '5432',
    }
}

STATIC_URL = '/static/'
