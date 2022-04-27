"""
Django settings for gestprjsite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
# VIRTUAL ENV USADO: gestprj_devel_2   <--Mensaje escrito el 25-02-2019

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
from django.http import HttpResponseRedirect
from django.conf.global_settings import DATETIME_INPUT_FORMATS


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f8z-u^p(n9+dq8w#p1s*v553x1wb9bl#g=j#k)xodey%u($)3!'

TEMPLATE_DEBUG = True

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(SETTINGS_PATH, 'gestprj/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# REST_FRAMEWORK = {
#     'PAGE_SIZE': 1000000,
# }

# MIDDLEWARE_CLASSES = (
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     #'django.middleware.security.SecurityMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# )

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'gestprjsite.urls'

WSGI_APPLICATION = 'gestprjsite.wsgi.application'





# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'es-es'

#Para que funcionene las nuevas fechas con el datetimefield en models(parece que no hace gran cosa ya que el models lo sigue devolviendo con tiempo...)
USE_L10N=False
USE_TZ = False
DATETIME_INPUT_FORMATS = ("%d-%m-%Y"),
DATETIME_FORMAT = "%d-%m-%Y"

REST_FRAMEWORK = {
    'DATETIME_INPUT_FORMATS': ["%d-%m-%Y"],# poner con []?
    'DATETIME_FORMAT': "%d-%m-%Y"

}
#
DATE_FORMAT = '%d-%m-%Y'
DATE_INPUT_FORMATS = "%d-%m-%Y"

TIME_ZONE = 'UTC' #Ojo que este son 2 horas menos,por si miro algun log o insert en la bdd

USE_I18N = False

# USE_L10N = True Deshabilitado porque mostraba las fechas en formato ingles

#USE_TZ = True


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
from .settings_local import *