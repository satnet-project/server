"""
   Copyright 2013, 2014 Ricardo Tubio-Pardavila

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
__author__ = 'rtubiopa@calpoly.edu'

import os
import sys
from secrets import auth, database, email

# Django website for WebServices project.
DEBUG = True
TESTING = sys.argv[1:2] == ['test']

ADMINS = [
    ("Ricardo Tubio-Pardavila", "rtubiopa@calpoly.edu"),
]
MANAGERS = ADMINS

DATABASES = database.DATABASES

BASE_DIR = os.path.join(
    os.path.dirname(__file__), '..'
)

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/website/#allowed-hosts
ALLOWED_HOSTS = []

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in services' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(
    os.path.dirname(__file__), '..', 'public_html/static/'
)

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(
        os.path.dirname(__file__), 'static'
    ),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = auth.SECRET_KEY

# ### Creates the super user so that when loading the fixtures, there is a
# super user already available in the database.

if TESTING:
    from django.db.models import signals
    import utils
    signals.post_syncdb.connect(utils.test_create_admin)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # ### Session security middleware
    'session_security.middleware.SessionSecurityMiddleware',
)

# ### Context processors as required by django-session-security
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

ROOT_URLCONF = 'website.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'website.wsgi.application'

# ### templates directories loading, relative to project's structure
TEMPLATE_DIRS = (
    os.path.join(
        os.path.dirname(__file__), 'templates'
    ),
    os.path.join(
        os.path.dirname(__file__), '..', 'services', 'accounts', 'templates'
    ),
)

TEST_RUNNER = 'website.tests.SatnetTestRunner'

# ### TODO When migrating to Django >= 1.7, change to data migration...
# ### directories with fixtures for database
FIXTURE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'fixtures'),
)

INSTALLED_APPS = (

    # ### default applications
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'session_security',
    'leaflet',
    'periodically',
    'rpc4django',
    'rest_framework',
    'django_extensions',

    # ### developed applications
    'services.accounts',
    'services.configuration',
    'services.scheduling',
    'services.communications',
    'services.simulation',

    # ### django-admin
    'django.contrib.admin',

)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            #'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'periodically': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'rpc4django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'configuration': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'common': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'communications': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'scheduling': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'simulation': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# ### django-allauth configuration:
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend"
)

# ### django-allauth configuration:
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 4
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGOUT_REDIRECT_URL = 'services.accounts.views.redirect_home'
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_SIGNUP_FORM_CLASS = 'services.accounts.forms.RegistrationForm'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_MIN_LENGTH = 5
ACCOUNT_USERNAME_REQUIRED = True
EMAIL_CONFIRMATION_SIGNUP = True

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = 'account_confirmation'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'

LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'services.accounts.views.redirect_login'
LOGOUT_URL = 'services.accounts.views.redirect_home'
CSRF_FAILURE_VIEW = 'services.accounts.views.csrf_failure_handler'

# ### this parameter links __my__ UserProfile with the User from contrib.auth
AUTH_PROFILE_MODULE = 'services.accounts.UserProfile'
# ### this parameter provokes that a user has to re-log-in every time the
# browser is closed
# value required to be True bye django-session-security
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ### django-session-security
SESSION_SECURITY_WARN_AFTER = 600
SESSION_SECURITY_EXPIRE_AFTER = 540
# ### List with the urls that do not provoke the inactivity timer to be 
# restarted
# SESSION_SECURITY_PASSIVE_URLS = 

EMAIL_BACKEND = email.EMAIL_BACKEND
EMAIL_HOST = email.EMAIL_HOST
EMAIL_PORT = email.EMAIL_PORT
EMAIL_HOST_USER = email.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = email.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = email.EMAIL_USE_TLS

# https://github.com/dstufft/django-passwords/
PASSWORD_MIN_LENGTH = 8
PASSWORD_COMPLEXITY = {
    "UPPER":  1,
    "LOWER":  1,
    "DIGITS": 1
}

APPEND_SLASH = False