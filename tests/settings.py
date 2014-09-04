from __future__ import unicode_literals

import os


DEBUG = False

ALLOWED_HOSTS = ['*']
LANGUAGE_CODE = 'en-us'
ROOT_URLCONF = 'urls'
SECRET_KEY = '12345abcd'
SITE_ID = 1
TIME_ZONE = 'UTC'
USE_I18N = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_core',
    'django_testing',
    'test_objects',  # so the test models get picked up
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': here('test_db.db')
    }
}
