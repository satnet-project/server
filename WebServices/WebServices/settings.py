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

# Django settings for WebServices project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = [
    ("Ricardo Tubio-Pardavila", "rtubiopa@calpoly.edu"),
]

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'satnet_db',
        'USER': 'satnet_django',
        'PASSWORD': '_805Django',
        'HOST': '',
        'PORT': '',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

TIME_ZONE = 'America/Los_Angeles'
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
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
import os
main_static = os.path.join(os.path.dirname(__file__), 'static')
primeui_static = os.path.join(os.path.dirname(__file__), 'static', 'prime-ui')
STATICFILES_DIRS = (
    main_static,
    primeui_static,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'y!b^rbe7rjefa828rqf7*k6-v7lmtene#pl9e3n7anhc-$ag#p'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
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
)

ROOT_URLCONF = 'WebServices.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'WebServices.wsgi.application'

# ### templates directories loading, relative to project's structure
main_templates = os.path.join(os.path.dirname(__file__), 'templates')
accounts_templates = os.path.join(os.path.dirname(__file__), '..', 'accounts', 'templates')
configuration_templates = os.path.join(os.path.dirname(__file__), '..', 'configuration', 'templates')

TEMPLATE_DIRS = (
    main_templates,
    accounts_templates,
    configuration_templates,
)

INSTALLED_APPS = (
    # ### default applications
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # ### django-registration
    'registration',
    # ### django-session-security
    'session_security',
    # ### mapping!
    'leaflet',
    # ### periodical task scheduling
    'periodically',
    # ### django-admin
    'django.contrib.admin',
    'django.contrib.admindocs',
    # ### rpc4django (must appear before RPC implementors)
    'rpc4django',
    
    # ### developed applications
    'accounts',
    'configuration',

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
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
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
            'handlers': ['console'],
            'level': 'ERROR',
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
        'rpc4django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

# ### django-registration: 4 days for the user to activate the account
ACCOUNT_ACTIVATION_DAYS = 4
LOGIN_URL = '/accounts/login'
LOGIN_REDIRECT_URL = '/accounts/login_ok/'
LOGOUT_URL = '/accounts/logout'
CSRF_FAILURE_VIEW = 'accounts.views.csrf_failure_handler'
# ### this parameter links __my__ UserProfile with the User from contrib.auth
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
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

# ### e-mail settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST='mail.calpoly.edu'
EMAIL_PORT=25

# ### TODO Real non-personal account
EMAIL_HOST_USER='rtubiopa@calpoly.edu'
# ### EMAIL_HOST_PASSWORD=''
EMAIL_USE_TLS='True'

