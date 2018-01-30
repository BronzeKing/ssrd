"""
Local settings

- Run in Debug mode

- Use console backend for emails

- Add Django Debug Toolbar
- Add django-extensions as app
"""

from .base import *  # noqa

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='e;Kw&CNh${oO.DA?yKVP-T*jdibwa31E}q!e=oxVOn#7Gy@@R9')

# Mail settings
# ------------------------------------------------------------------------------

EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
default='django.core.mail.backends.console.EmailBackend')

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

INTERNAL_IPS = [
    '127.0.0.1',
    '10.0.2.2',
]

import socket
import os
# tricks to have debug toolbar when developing with docker
if os.environ.get('USE_DOCKER') == 'yes':
    ip = socket.gethostbyname(socket.gethostname())
    INTERNAL_IPS += [ip[:-1] + '1']

#  DEBUG_TOOLBAR_CONFIG = {
#  'DISABLE_PANELS': [
#  'debug_toolbar.panels.redirects.RedirectsPanel',
#  ],
#  'SHOW_TEMPLATE_CONTEXT': True,
#  }

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += [
    'django_extensions',
]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------


try:
    import __builtin__ as builtins
except ImportError:
    import builtins
try:
    from line_profiler import LineProfiler
except ImportError:
    pass

import functools

class Line_Profiler(object):
    def __init__(self, follow=None):
        self.follow = follow or []

    def __call__(self, func):
        def profiled_func(*args, **kwargs):
            line_profiler = LineProfiler()
            line_profiler.add_function(func)
            map(lambda x: line_profiler.add_function(x), self.follow)
            line_profiler.enable_by_count()
            result = func(*args, **kwargs)
            line_profiler.disable_by_count()
            line_profiler.print_stats(stripzeros=True)
            return result

        return functools.wraps(func)(profiled_func)


builtins.profile = Line_Profiler
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'thread': {
            'format':
            '%(asctime)s [%(threadName)s:%(thread)d] [%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
        'standard': {
            'format':
            '%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    },
    'loggers': {
        #  'django.db.backends': {
        #  'handlers': ['console'],
        #  'propagate': True,
        #  'level': 'DEBUG',
        #  },
    }
}
