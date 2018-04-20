"""
Django settings for sapl project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

Quick-start development settings - unsuitable for production
See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

"""
import logging

from decouple import config
from dj_database_url import parse as db_url
from easy_thumbnails.conf import Settings as thumbnail_settings
from unipath import Path

from .temp_suppress_crispy_form_warnings import \
    SUPRESS_CRISPY_FORM_WARNINGS_LOGGING

BASE_DIR = Path(__file__).ancestor(1)
PROJECT_DIR = Path(__file__).ancestor(2)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ALLOWED_HOSTS = ['*']

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/?next='

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


# SAPL business apps in dependency order
SAPL_APPS = (
    'sapl.audiencia',
    'sapl.base',
    'sapl.crud',
    'sapl.parlamentares',
    'sapl.comissoes',
    'sapl.materia',
    'sapl.norma',
    'sapl.sessao',
    'sapl.lexml',
    'sapl.painel',
    'sapl.protocoloadm',
    'sapl.redireciona_urls',
    'sapl.compilacao',
    'sapl.api',

    'sapl.rules'

)

INSTALLED_APPS = (
    'django_admin_bootstrapped',  # must come before django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # more
    'django_extensions',
    'djangobower',
    'bootstrap3',  # basically for django_admin_bootstrapped
    'crispy_forms',
    'easy_thumbnails',
    'image_cropping',
    'floppyforms',
    'haystack',
    'sass_processor',
    'rest_framework',
    'reversion',
    'whoosh',
    'speedinfo',

) + SAPL_APPS

# FTS = Full Text Search
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
SEARCH_BACKEND = 'haystack.backends.whoosh_backend.WhooshEngine'
SEARCH_URL = ('PATH', PROJECT_DIR.child('whoosh'))

SOLR_URL = config('SOLR_URL', cast=str, default='')
if SOLR_URL:
    SEARCH_BACKEND = 'haystack.backends.solr_backend.SolrEngine'
    SEARCH_URL = ('URL', config('SOLR_URL', cast=str))
    # ...or for multicore...
    # 'URL': 'http://127.0.0.1:8983/solr/mysite',


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': SEARCH_BACKEND,
        SEARCH_URL[0]: SEARCH_URL[1]
    },
}


if DEBUG:
    INSTALLED_APPS += ('debug_toolbar', 'rest_framework_docs',)

MIDDLEWARE = [
    'reversion.middleware.RevisionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'speedinfo.middleware.ProfilerMiddleware',
]

CACHES = {
    'default': {
        'BACKEND': 'speedinfo.backends.proxy_cache',
        'CACHE_BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

REST_FRAMEWORK = {
    "UNICODE_JSON": False,
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
        "sapl.api.permissions.DjangoModelPermissions",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "sapl.api.pagination.StandardPagination",
    "DEFAULT_FILTER_BACKENDS": (
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.DjangoFilterBackend",
    ),
}


ROOT_URLCONF = 'sapl.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['sapl/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                'django.contrib.messages.context_processors.messages',
                'sapl.context_processors.parliament_info',
            ],
            'debug': DEBUG
        },
    },
]


WSGI_APPLICATION = 'sapl.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL', default='sqlite://:memory:',
        cast=db_url,
    )
}

IMAGE_CROPPING_JQUERY_URL = None
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS

THUMBNAIL_SOURCE_GENERATORS = (
    'sapl.utils.pil_image',
)

# troque no caso de reimplementação da classe User conforme
# https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#substituting-a-custom-user-model
AUTH_USER_MODEL = 'auth.User'

X_FRAME_OPTIONS = 'ALLOWALL'

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
EMAIL_SEND_USER = config('EMAIL_SEND_USER', cast=str, default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', cast=str, default='')
SERVER_EMAIL = config('SERVER_EMAIL', cast=str, default='')

MAX_DOC_UPLOAD_SIZE = 20 * 1024 * 1024  # 20MB
MAX_IMAGE_UPLOAD_SIZE = 2 * 1024 * 1024  # 2MB

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/
LANGUAGE_CODE = 'pt-br'
LANGUAGES = (
    ('pt-br', 'Português'),
)

TIME_ZONE = config('TZ', cast=str, default='America/Sao_Paulo')
USE_I18N = True
USE_L10N = True
USE_TZ = True
# DATE_FORMAT = 'N j, Y'
DATE_FORMAT = 'd/m/Y'
SHORT_DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y H:i:s'
SHORT_DATETIME_FORMAT = 'd/m/Y H:i'
DATE_INPUT_FORMATS = ('%d/%m/%Y', '%m-%d-%Y', '%Y-%m-%d')

LOCALE_PATHS = (
    'locale',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = PROJECT_DIR.child("collected_static")
STATICFILES_DIRS = (BASE_DIR.child("static"),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'sass_processor.finders.CssFinder',
)

MEDIA_ROOT = PROJECT_DIR.child("media")
MEDIA_URL = '/media/'

DAB_FIELD_RENDERER = \
    'django_admin_bootstrapped.renderers.BootstrapFieldRenderer'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap3'
CRISPY_FAIL_SILENTLY = not DEBUG

BOWER_COMPONENTS_ROOT = PROJECT_DIR.child("bower")
BOWER_INSTALLED_APPS = (
    'jquery#3.1.1',
    'bootstrap-sass#3.3.7',
    'components-font-awesome#4.5.0',
    'tinymce#4.3.8',
    'jquery-ui#1.12.1',
    'jQuery-Mask-Plugin#1.14.0',
    'jsdiff#2.2.2',
    'https://github.com/interlegis/drunken-parrot-flat-ui.git',
    'jquery-query-object#2.2.3',
)

# Additional search paths for SASS files when using the @import statement
SASS_PROCESSOR_INCLUDE_DIRS = (BOWER_COMPONENTS_ROOT.child(
    'bower_components', 'bootstrap-sass', 'assets', 'stylesheets'),
)

# suprime texto de ajuda default do django-filter
FILTERS_HELP_TEXT_FILTER = False


# FIXME update cripy-forms and remove this
# hack to suppress many annoying warnings from crispy_forms
# see sapl.temp_suppress_crispy_form_warnings
LOGGING = SUPRESS_CRISPY_FORM_WARNINGS_LOGGING


LOGGING_CONSOLE = config('LOGGING_CONSOLE', default=False, cast=bool)
if DEBUG and LOGGING_CONSOLE:
    # Descomentar linha abaixo fará com que logs aparecam, inclusive SQL
    # LOGGING['handlers']['console']['level'] = 'DEBUG'
    LOGGING['loggers']['django']['level'] = 'DEBUG'
    LOGGING.update({
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(pathname)s '
                '%(funcName)s %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
    })
    LOGGING['handlers']['console']['formatter'] = 'verbose'
    LOGGING['loggers'][BASE_DIR.name] = {
        'handlers': ['console'],
        'level': 'DEBUG',
    }


def excepthook(*args):
    logging.getLogger(BASE_DIR.name).error(
        'Uncaught exception:', exc_info=args)

# sys.excepthook = excepthook


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',  # default
    'sapl.hashers.ZopeSHA1PasswordHasher',
]
