from __future__ import unicode_literals

import os
import sys

# Do not run in DEBUG in production!!!
DEBUG = False

ALLOWED_HOSTS = ['*']
LANGUAGE_CODE = 'en-us'
SECRET_KEY = '12345abcd'
SITE_ID = 1
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
TIME_ZONE = 'UTC'
USE_I18N = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django_core',
    'django_nose',
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

if 'test' in sys.argv:
    NOSE_ARGS = ('--nocapture', '--with-doctest', '--testmatch=^test')
