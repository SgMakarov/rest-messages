import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'bew9%agaop4^%62ff_v&90ahm2tp8&f%=kap&%q*$#0but2ef5' 

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_framework',
    'api',
]

MIDDLEWARE = [
]

ROOT_URLCONF = 'rest.urls'

TEMPLATES = [
]

WSGI_APPLICATION = 'rest.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
