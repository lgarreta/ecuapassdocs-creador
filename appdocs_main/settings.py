"""
Django settings for appdocs_main project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

#SECRET_KEY = config('SECRET_KEY')
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-*e!pw-wwqm=az^o+oy0a$2u$rhkf(05i&!c3ic8@49dsh9&hmi')

DEBUG = True

ALLOWED_HOSTS = ['ecuapassdocs-production.up.railway.app', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://ecuapassdocs-production.up.railway.app']


# Application definition

INSTALLED_APPS = [
	"appreportes",
	"appdocs.apps.AppdocsConfig",
	"appusuarios.apps.UsuariosConfig",
	'django_tables2',
	"crispy_forms",
	"crispy_bootstrap4",
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
]


MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	'whitenoise.middleware.WhiteNoiseMiddleware',
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "appdocs_main.urls"

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		#"DIRS": [],
		'DIRS': [os.path.join (BASE_DIR, 'templates'),],
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.debug",
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
			],
		},
	},
]

WSGI_APPLICATION = "appdocs_main.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#DATABASES = {
#	"default": {
#		"ENGINE": "django.db.backends.sqlite3",
#		"NAME": BASE_DIR / "db.sqlite3",
#	}
#}

# Remote railway database
DATABASES = {
	'default': {
		'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
		'NAME'	  : os.environ.get ('PGDATABASE'),
		'USER'	  : os.environ.get ('PGUSER'),
		'PASSWORD': os.environ.get ('PGPASSWORD'),
		'HOST'	  : os.environ.get ('PGHOST'),
		'PORT'	  : os.environ.get ('PGPORT'),
	}
}

## Local postgress database
#DATABASES = {
#	 'default': {
#		 'ENGINE'  : 'django.db.backends.postgresql_psycopg2',
#		 'NAME'    : 'ecuapassdocsdb',
#		 'USER'    : 'byza',
#		 'PASSWORD': 'byza2024',
#		 'HOST'    : 'localhost',
#		 'PORT'    : '5432',
#	 }
#}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	#{ "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator", },
	{ "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
	#{ "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
	{ "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# Set the language code to Spanish for Colombia
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

AUTH_USER_MODEL = 'appusuarios.UsuarioEcuapass'

LOGIN_URL = 'login'	# Replace with your login URL name

LOGOUT_URL = 'logout'  # Replace with your logout URL name

LOGIN_REDIRECT_URL = 'index'  # Replace with your desired redirect URL

LOGOUT_REDIRECT_URL = 'index'  # Replace with your desired redirect URL

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'
CRISPY_TEMPLATE_PACK = "bootstrap4"

STATIC_URL	= "staticfiles/"
STATIC_ROOT = os.path.join (BASE_DIR, 'staticfiles')

# Static file serving.
# https://whitenoise.readthedocs.io/en/stable/django.html#add-compression-and-caching-support
STORAGES = {
	# ...
	"staticfiles": {
		"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
	},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

