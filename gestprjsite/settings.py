"""
Django settings for gestprjsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from django.http import HttpResponseRedirect


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f8z-u^p(n9+dq8w#p1s*v553x1wb9bl#g=j#k)xodey%u($)3!'

TEMPLATE_DEBUG = True



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'gestprj',
    'rest_framework',
    'ldap_groups'
    # 'debug_toolbar',
)

REST_FRAMEWORK = {
    'PAGE_SIZE': 1000000,
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'gestprjsite.urls'

WSGI_APPLICATION = 'gestprjsite.wsgi.application'





# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-es'

DATE_FORMAT = 'd-m-Y'

TIME_ZONE = 'UTC' #Ojo que este son 2 horas menos,por si miro algun log o insert en la bdd

USE_I18N = True

# USE_L10N = True Deshabilitado porque mostraba las fechas en formato ingles

USE_TZ = True


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# MUY IMPORTANTE!!!!
from settings_local import *