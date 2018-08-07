# -*- coding: utf-8 -*-
"""Define the Gitcoin project settings.

Copyright (C) 2018 Gitcoin Core

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
import os
import socket

from django.http import Http404
from django.utils.translation import gettext_noop

import environ
import raven
from easy_thumbnails.conf import Settings as easy_thumbnails_defaults

root = environ.Path(__file__) - 2  # Set the base directory to two levels.
env = environ.Env(DEBUG=(bool, False), )  # set default values and casting
env.read_env(str(root.path('app/.env')))  # reading .env file

DEBUG = env.bool('DEBUG', default=True)
ENV = env('ENV', default='local')
DEBUG_ENVS = env.list('DEBUG_ENVS', default=['local', 'stage', 'test'])
IS_DEBUG_ENV = ENV in DEBUG_ENVS
HOSTNAME = env('HOSTNAME', default=socket.gethostname())
BASE_URL = env('BASE_URL', default='http://localhost:8000/')
SECRET_KEY = env('SECRET_KEY', default='YOUR-SupEr-SecRet-KeY')
ADMINS = (env.tuple('ADMINS', default=('TODO', 'todo@todo.net')))
BASE_DIR = root()

# Ratelimit
RATELIMIT_ENABLE = env.bool('RATELIMIT_ENABLE', default=True)
RATELIMIT_USE_CACHE = env('RATELIMIT_USE_CACHE', default='default')
RATELIMIT_VIEW = env('RATELIMIT_VIEW', default='tdi.views.ratelimited')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS', default=['localhost'])

# Notifications - Global on / off switch
ENABLE_NOTIFICATIONS_ON_NETWORK = env('ENABLE_NOTIFICATIONS_ON_NETWORK', default='mainnet')

# Application definition
INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'storages',
    'social_django',
    'cookielaw',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'autotranslate',
    'django_extensions',
    'easy_thumbnails',
    'crispy_forms',
    'account',
    'raven.contrib.django.raven_compat',
    'app',
    'avatar',
    'retail',
    'rest_framework',
    'bootstrap4',
    'marketing',
    'economy',
    'dashboard',
    'enssubdomain',
    'faucet',
    'tdi',
    'gas',
    'git',
    'legacy',
    'chartit',
    'email_obfuscator',
    'linkshortener',
    'credits',
    'gitcoinbot',
    'external_bounties',
    'dataviz',
    'impersonate',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ratelimit.middleware.RatelimitMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
]

CRISPY_TEMPLATE_PACK = env('CRISPY_TEMPLATE_PACK', default='bootstrap4')

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ('sumo.com', 'load.sumo.com', 'googleads.g.doubleclick.net', )

ROOT_URLCONF = env('ROOT_URLCONF', default='app.urls')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',  # for Github authentication
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['retail/templates/', 'external_bounties/templates/', 'dataviz/templates', ],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug', 'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages',
            'app.context.insert_settings', 'social_django.context_processors.backends',
            'social_django.context_processors.login_redirect',
        ],
    },
}]

SITE_ID = env.int('SITE_ID', default=1)
WSGI_APPLICATION = env('WSGI_APPLICATION', default='app.wsgi.application')

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {'default': env.db()}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [{
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
}, {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
}]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend', ),
    'DEFAULT_THROTTLE_CLASSES': ('rest_framework.throttling.AnonRateThrottle', ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '1000/day',
    },
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'],
    'DEFAULT_AUTHENTICATION_CLASSES': []
}

AUTH_USER_MODEL = 'auth.User'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
LANGUAGE_CODE = env('LANGUAGE_CODE', default='en-us')
USE_I18N = env.bool('USE_I18N', default=True)
USE_L10N = env.bool('USE_L10N', default=True)
USE_TZ = env.bool('USE_TZ', default=True)
TIME_ZONE = env.str('TIME_ZONE', default='UTC')

LOCALE_PATHS = ('locale', )

LANGUAGES = [
    ('en', gettext_noop('English')),
    ('es', gettext_noop('Spanish')),
    ('de', gettext_noop('German')),
    ('hi', gettext_noop('Hindi')),
    ('it', gettext_noop('Italian')),
    ('ko', gettext_noop('Korean')),
    ('pl', gettext_noop('Polish')),
    ('zh-hans', gettext_noop('Simplified Chinese')),
    ('zh-hant', gettext_noop('Traditional Chinese')),
]

if ENV not in ['local', 'test']:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',  # To capture more than ERROR, change to WARNING, INFO, etc.
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {
                    'custom-tag': 'x'
                },
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'WARN',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

    LOGGING['loggers']['django.request'] = LOGGING['loggers']['django.db.backends']
    for ia in INSTALLED_APPS:
        LOGGING['loggers'][ia] = LOGGING['loggers']['django.db.backends']
else:
    LOGGING = {}

GEOIP_PATH = env('GEOIP_PATH', default='/usr/share/GeoIP/')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATICFILES_STORAGE = env('STATICFILES_STORAGE', default='app.static_storage.SilentFileStorage')
STATICFILES_DIRS = env.tuple('STATICFILES_DIRS', default=('assets/', ))
STATIC_ROOT = root('static')

STATIC_HOST = env('STATIC_HOST', default='')
STATIC_URL = STATIC_HOST + env('STATIC_URL', default='/static/')

THUMBNAIL_PROCESSORS = easy_thumbnails_defaults.THUMBNAIL_PROCESSORS + ('app.thumbnail_processors.circular_processor', )

THUMBNAIL_ALIASES = {
    '': {
        'graph_node': {
            'size': (30, 30),
            'crop': True
        },
        'graph_node_circular': {
            'size': (30, 30),
            'crop': True,
            'circle': True
        }
    }
}

CACHES = {'default': env.cache()}

# HTTPS Handling
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD', default=True)
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=3600)
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=False)

CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=False)
CSRF_COOKIE_HTTPONLY = env.bool('CSRF_COOKIE_HTTPONLY', default=True)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=False)
SECURE_BROWSER_XSS_FILTER = env.bool('SECURE_BROWSER_XSS_FILTER', default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool('SECURE_CONTENT_TYPE_NOSNIFF', default=True)
X_FRAME_OPTIONS = env('X_FRAME_OPTIONS', default='DENY')

# Email Integrations
CONTACT_EMAIL = env('CONTACT_EMAIL', default='')  # TODO
PERSONAL_CONTACT_EMAIL = env('PERSONAL_CONTACT_EMAIL', default='you@foo.bar')
SENDGRID_API_KEY = env('SENDGRID_API_KEY', default='')  # TODO - Required to send email.
EMAIL_HOST = env('EMAIL_HOST', default='smtp.sendgrid.net')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='')  # TODO
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default='')  # TODO
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
SERVER_EMAIL = env('SERVER_EMAIL', default='server@TODO.co')

# ENS Subdomain Settings
# The value of ENS_LIMIT_RESET_DAYS should be higher since only one transaction is allowed per user.
# The only reason for a user to make more than one request is when he looses access to the wallet.
ENS_TLD = env('ENS_TLD', default='gitcoin.eth')
ENS_LIMIT_RESET_DAYS = env.int('ENS_LIMIT_RESET_DAYS', default=30)
ENS_OWNER_ACCOUNT = env('ENS_OWNER_ACCOUNT', default='0x00000')
ENS_PRIVATE_KEY = env('ENS_PRIVATE_KEY', default=None)

# IMAP Settings
IMAP_EMAIL = env('IMAP_EMAIL', default='<email>')
IMAP_PASSWORD = env('IMAP_PASSWORD', default='<password>')

# Mailchimp Integration
MAILCHIMP_USER = env.str('MAILCHIMP_USER', default='')
MAILCHIMP_API_KEY = env.str('MAILCHIMP_API_KEY', default='')
MAILCHIMP_LIST_ID = env.str('MAILCHIMP_LIST_ID', default='')

# Github
GITHUB_API_BASE_URL = env('GITHUB_API_BASE_URL', default='https://api.github.com')
GITHUB_AUTH_BASE_URL = env('GITHUB_AUTH_BASE_URL', default='https://github.com/login/oauth/authorize')
GITHUB_TOKEN_URL = env('GITHUB_TOKEN_URL', default='https://github.com/login/oauth/access_token')
GITHUB_SCOPE = env('GITHUB_SCOPE', default='read:user,user:email')
GITHUB_CLIENT_ID = env('GITHUB_CLIENT_ID', default='')  # TODO
GITHUB_CLIENT_SECRET = env('GITHUB_CLIENT_SECRET', default='')  # TODO
GITHUB_API_USER = env('GITHUB_API_USER', default='')  # TODO
GITHUB_API_TOKEN = env('GITHUB_API_TOKEN', default='')  # TODO
GITHUB_APP_NAME = env('GITHUB_APP_NAME', default='gitcoin-local')

# Social Auth
LOGIN_URL = 'gh_login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'explorer'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'explorer'
SOCIAL_AUTH_GITHUB_KEY = GITHUB_CLIENT_ID
SOCIAL_AUTH_GITHUB_SECRET = GITHUB_CLIENT_SECRET
SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'last_name', 'email']
SOCIAL_AUTH_GITHUB_SCOPE = ['read:public_repo', 'read:user', 'user:email', ]

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details', 'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed', 'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username', 'social_core.pipeline.user.create_user', 'app.pipeline.save_profile',
    'social_core.pipeline.social_auth.associate_user', 'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

# Gitter
GITTER_TOKEN = env('GITTER_TOKEN', default=False)

# optional: only needed if you run the gitcoinbot app
# Setup instructions: https://github.com/gitcoinco/web/blob/master/app/gitcoinbot/README.md
GITCOINBOT_APP_ID = env('GITCOINBOT_APP_ID', default='')
GITCOIN_BOT_CERT_PATH = env('GITCOIN_BOT_CERT_PATH', default='')
SECRET_KEYSTRING = ''
if GITCOIN_BOT_CERT_PATH:
    with open(str(root.path(GITCOIN_BOT_CERT_PATH))) as f:
        SECRET_KEYSTRING = f.read()

GITCOIN_SLACK_ICON_URL = 'https://gitcoin.co/static/v2/images/helmet.png'

# Twitter Integration
TWITTER_CONSUMER_KEY = env('TWITTER_CONSUMER_KEY', default='')  # TODO
TWITTER_CONSUMER_SECRET = env('TWITTER_CONSUMER_SECRET', default='')  # TODO
TWITTER_ACCESS_TOKEN = env('TWITTER_ACCESS_TOKEN', default='')  # TODO
TWITTER_ACCESS_SECRET = env('TWITTER_ACCESS_SECRET', default='')  # TODO
TWITTER_USERNAME = env('TWITTER_USERNAME', default='')  # TODO

# Slack Integration
# optional: only needed if you slack things
SLACK_TOKEN = env('SLACK_TOKEN', default='')  # TODO
SLACK_WELCOMEBOT_TOKEN = env('SLACK_WELCOMEBOT_TOKEN', default='')  # TODO

# Reporting Integrations
MIXPANEL_TOKEN = env('MIXPANEL_TOKEN', default='')

GA_PRIVATE_KEY_PATH = env('GA_PRIVATE_KEY_PATH', default='')
GA_PRIVATE_KEY = ''
if GA_PRIVATE_KEY_PATH:
    with open(str(root.path(GA_PRIVATE_KEY_PATH))) as cert_file:
        GA_PRIVATE_KEY = cert_file.read()

# https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py
GOOGLE_ANALYTICS_AUTH_JSON = {
    'type': env('GA_TYPE', default='service_account'),
    'project_id': env('GA_PROJECT_ID', default=''),
    'private_key_id': env('GA_PRIVATE_KEY_ID', default=''),
    'private_key': GA_PRIVATE_KEY,
    'client_email': env('GA_CLIENT_EMAIL', default=''),
    'client_id': env('GA_CLIENT_ID', default=''),
    'auth_uri': env('GA_AUTH_URI', default='https://accounts.google.com/o/oauth2/auth'),
    'token_uri': env('GA_TOKEN_URI', default='https://accounts.google.com/o/oauth2/token'),
    'auth_provider_x509_cert_url':
        env('GA_AUTH_PROVIDER_X509_CERT_URL', default='https://www.googleapis.com/oauth2/v1/certs'),
    'client_x509_cert_url': env('GA_CLIENT_X509_CERT_URL', default='')
}
HOTJAR_CONFIG = {'hjid': env.int('HOTJAR_ID', default=0), 'hjsv': env.int('HOTJAR_SV', default=0), }

# Sentry
SENTRY_USER = env('SENTRY_USER', default='')
SENTRY_PASSWORD = env('SENTRY_PASSWORD', default='')
SENTRY_ADDRESS = env('SENTRY_ADDRESS', default='')
SENTRY_JS_DSN = env.str('SENTRY_JS_DSN', default='')
SENTRY_PROJECT = env('SENTRY_PROJECT', default='')
RELEASE = raven.fetch_git_sha(os.path.abspath(os.pardir)) if SENTRY_USER else ''
RAVEN_JS_VERSION = env.str('RAVEN_JS_VERSION', default='3.26.4')
if SENTRY_ADDRESS and SENTRY_PROJECT:
    RAVEN_CONFIG = {
        'dsn': f'https://{SENTRY_USER}:{SENTRY_PASSWORD}@{SENTRY_ADDRESS}/{SENTRY_PROJECT}',
        'release': RELEASE,
    }

# List of github usernames to not count as comments on an issue
IGNORE_COMMENTS_FROM = ['gitcoinbot', ]

# optional: only needed if you run the activity-report management command
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', default='')

AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME', default='')
AWS_S3_OBJECT_PARAMETERS = env.dict('AWS_S3_OBJECT_PARAMETERS', default={'CacheControl': 'max-age=86400'})
S3_USE_SIGV4 = env.bool('S3_USE_SIGV4', default=True)
AWS_IS_GZIPPED = env.bool('AWS_IS_GZIPPED', default=True)
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME', default='us-west-2')
AWS_S3_SIGNATURE_VERSION = env('AWS_S3_SIGNATURE_VERSION', default='s3v4')
AWS_QUERYSTRING_AUTH = env.bool('AWS_QUERYSTRING_AUTH', default=False)
AWS_S3_FILE_OVERWRITE = env.bool('AWS_S3_FILE_OVERWRITE', default=True)
# AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN', default='assets.gitcoin.co')

S3_REPORT_BUCKET = env('S3_REPORT_BUCKET', default='')  # TODO
S3_REPORT_PREFIX = env('S3_REPORT_PREFIX', default='')  # TODO

# Handle local file storage
if ENV == 'local' and not AWS_STORAGE_BUCKET_NAME:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = root('media')
else:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

INSTALLED_APPS += env.list('DEBUG_APPS', default=[])

# Faucet App config
FAUCET_AMOUNT = env.float('FAUCET_AMOUNT', default=.00025)

SENDGRID_EVENT_HOOK_URL = env('SENDGRID_EVENT_HOOK_URL', default='sg_event_process')
GITHUB_EVENT_HOOK_URL = env('GITHUB_EVENT_HOOK_URL', default='github/payload/')

# Web3
WEB3_HTTP_PROVIDER = env('WEB3_HTTP_PROVIDER', default='https://rinkeby.infura.io')

# COLO Coin
COLO_ACCOUNT_ADDRESS = env('COLO_ACCOUNT_ADDRESS', default='')  # TODO
COLO_ACCOUNT_PRIVATE_KEY = env('COLO_ACCOUNT_PRIVATE_KEY', default='')  # TODO

IPFS_HOST = env('IPFS_HOST', default='ipfs.infura.io')
IPFS_SWARM_PORT = env.int('IPFS_SWARM_PORT', default=4001)
IPFS_UTP_PORT = env.int('IPFS_UTP_PORT', default=4002)
IPFS_API_PORT = env.int('IPFS_API_PORT', default=5001)
IPFS_GATEWAY_PORT = env.int('IPFS_GATEWAY_PORT', default=8080)
IPFS_SWARM_WS_PORT = env.int('IPFS_SWARM_WS_PORT', default=8081)
IPFS_API_ROOT = env('IPFS_API_ROOT', default='/api/v0')
IPFS_API_SCHEME = env('IPFS_API_SCHEME', default='https')

# Silk Profiling and Performance Monitoring
ENABLE_SILK = env.bool('ENABLE_SILK', default=False)
if ENABLE_SILK:
    INSTALLED_APPS += ['silk']
    MIDDLEWARE.append('silk.middleware.SilkyMiddleware')
    SILKY_PYTHON_PROFILER = env.bool('SILKY_PYTHON_PROFILER', default=True)
    SILKY_PYTHON_PROFILER_BINARY = env.bool('SILKY_PYTHON_PROFILER_BINARY', default=False)
    SILKY_AUTHENTICATION = env.bool('SILKY_AUTHENTICATION', default=False)
    SILKY_AUTHORISATION = env.bool('SILKY_AUTHORISATION', default=False)
    SILKY_META = env.bool('SILKY_META', default=True)
    SILKY_INTERCEPT_PERCENT = env.int('SILKY_INTERCEPT_PERCENT', default=50)
    SILKY_MAX_RECORDED_REQUESTS = env.int('SILKY_MAX_RECORDED_REQUESTS', default=10000)
    SILKY_DYNAMIC_PROFILING = env.list('SILKY_DYNAMIC_PROFILING', default=[])
    if ENV == 'stage':
        SILKY_DYNAMIC_PROFILING += [{
            'module': 'dashboard.views',
            'function': 'profile',
            'name': 'Profile View',
        }, {
            'module': 'retail.views',
            'function': 'index',
            'name': 'Index View',
        }]
    SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = env.int('SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT', default=10)
