"""
Django settings for ssrd project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import datetime

import environ

ROOT_DIR = environ.Path(__file__) - 3  # (ssrd/config/settings/base.py - 3 = ssrd/)
APPS_DIR = ROOT_DIR.path("ssrd")
BASE_DIR = str(ROOT_DIR)

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=True)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path(".env"))
    print("Loading : {}".format(env_file))
    env.read_env(env_file)
    print("The .env file has been loaded. See base.py for more information")

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Useful template tags:
    # 'django.contrib.humanize',
    # Admin
]
GRAPHENE = {"SCHEMA": "app.schema.schema"}  # Where your Graphene schema lives
THIRD_PARTY_APPS = ["rest_framework", "rest_framework.authtoken", "rest_framework_swagger", "social_django"]

# Apps specific for this project go here.
LOCAL_APPS = [
    # custom users app
    "ssrd.users.apps.UsersConfig",
    "ssrd.home",
    "ssrd.accounts",
    # Your stuff: custom apps go here
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {"sites": "ssrd.contrib.sites.migrations"}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", True)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (str(APPS_DIR.path("fixtures")),)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""drinksober""", "drinksober@foxmail.com")]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = "Asia/Shanghai"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "zh-cn"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        "DIRS": [str(APPS_DIR.path("templates"))],
        "OPTIONS": {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            "debug": DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            "loaders": ["django.template.loaders.filesystem.Loader", "django.template.loaders.app_directories.Loader"],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                # Your stuff: custom template context processors go here
            ],
        },
    }
]

QINIU_ACCESS_KEY = env("QINIU_ACCESS_KEY")
QINIU_SECRET_KEY = env("QINIU_SECRET_KEY")
QINIU_BUCKET_NAME = env("QINIU_BUCKET_NAME") or "mumumu"
QINIU_BUCKET_DOMAIN = env("QINIU_BUCKET_DOMAIN") or "static.mum5.cn"
QINIU_SECURE_URL = True
#  if 'production' in env("DJANGO_SETTINGS_MODULE", default='config.settings.local'):
DEFAULT_FILE_STORAGE = "qiniustorage.backends.QiniuStaticStorage"
STATICFILES_STORAGE = "qiniustorage.backends.QiniuStaticStorage"
# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = "bootstrap4"

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [str(APPS_DIR.path("static"))]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
STATIC_URL = "/static/"
MEDIA_URL = "/"
MEDIA_ROOT = ""
STATIC_ROOT = "/"

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "social_core.backends.open_id.OpenIdAuth",
    "social_core.backends.weixin.WeixinOAuth2",
    "social_core.backends.weibo.WeiboOAuth2",
    "social_core.backends.qq.QQOAuth2",
    "django.contrib.auth.backends.ModelBackend",
    "aspect.backend.custom.Backend",
]
SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple
    # format to create the user instance later. On some cases the details are
    # already part of the auth response from the provider, but sometimes this
    # could hit a provider API.
    "social_core.pipeline.social_auth.social_details",
    # Get the social uid from whichever service we're authing thru. The uid is
    # the unique identifier of the given user in the provider.
    "social_core.pipeline.social_auth.social_uid",
    # Verifies that the current auth process is valid within the current
    # project, this is where emails and domains whitelists are applied (if
    # defined).
    "social_core.pipeline.social_auth.auth_allowed",
    # Checks if the current social-account is already associated in the site.
    "social_core.pipeline.social_auth.social_user",
    # Make up a username for this person, appends a random string at the end if
    # there's any collision.
    "social_core.pipeline.user.get_username",
    # Send a validation email to the user to verify its email address.
    # Disabled by default.
    # 'social_core.pipeline.mail.mail_validation',
    # Associates the current social details with another user account with
    # a similar email address. Disabled by default.
    "social_core.pipeline.social_auth.associate_by_email",
    # Create a user account if we haven't found one yet.
    "social_core.pipeline.user.create_user",
    # Create the record that associates the social account with the user.
    "social_core.pipeline.social_auth.associate_user",
    # Populate the extra_data field in the social record with the values
    # specified by settings (and the default ones like access_token, etc).
    "social_core.pipeline.social_auth.load_extra_data",
    # Update the user record with any changed info from the auth service.
    "social_core.pipeline.user.user_details",
)

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = "username"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
ACCOUNT_ADAPTER = "ssrd.users.adapters.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "ssrd.users.adapters.SocialAccountAdapter"

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "redirect"
LOGIN_URL = "login"

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r"^admin/"

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "TIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
}
expiration = 12 * 60 * 60
JWT_AUTH = {
    "JWT_AUTH_HEADER_PREFIX": "Bearer",
    "JWT_EXPIRATION_DELTA": datetime.timedelta(seconds=expiration),
    "JWT_SECRET_KEY": "1qaz2wsx3edcssrd",
}

SWAGGER_SETTINGS = {
    "VERSION": "1.14.0",
    "USE_SESSION_AUTH": True,
    "SECURITY_DEFINITIONS": {
        "basic": {"type": "basic"},
        "apiKey": {"type": "apiKey", "name": "Authorization", "in": "header"},
    },
    "DOC_EXPANSION": None,
    "APIS_SORTER": None,
    "OPERATIONS_SORTER": None,
    "JSON_EDITOR": False,
    "SHOW_REQUEST_HEADERS": False,
    "SUPPORTED_SUBMIT_METHODS": ["get", "post", "put", "delete", "patch"],
    "VALIDATOR_URL": "",
}
ALLOWED_HOSTS = ["*"]

PARAER_APIVIEW = "ssrd.contrib.APIView"

APPEND_SLASH = False
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
SERVER_EMAIL = env("SERVER_EMAIL")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")

FE_DOMAIN = env("FE_DOMAIN") or "devs.cn:8888"

SOCIAL_AUTH_QQ_KEY = env("SOCIAL_AUTH_QQ_KEY")
SOCIAL_AUTH_QQ_SECRET = env("SOCIAL_AUTH_QQ_SECRET")

SOCIAL_AUTH_WEIBO_KEY = env("SOCIAL_AUTH_WEIBO_KEY")
SOCIAL_AUTH_WEIBO_SECRET = env("SOCIAL_AUTH_WEIBO_SECRET")

SOCIAL_AUTH_WEIXIN_KEY = env("SOCIAL_AUTH_WEIXIN_KEY")
SOCIAL_AUTH_WEIXIN_SECRET = env("SOCIAL_AUTH_WEIXIN_SECRET")

ALIYUN_ACCESSKEY_ID = env("ALIYUN_ACCESSKEY_ID")
ALIYUN_ACCESSKEY_SECRET = env("ALIYUN_ACCESSKEY_SECRET")
ALIYUN_SIGN = env("ALIYUN_SIGN")
ALIYUN_TEMPLATE_CODE = env("ALIYUN_TEMPLATE_CODE")
CREDENTIAL_CONFIRMATION_EXPIRE_DAYS = 15 * 60
CONFIRMATION_COOLDOWN = 3 * 60

REDIS = env.cache("REDIS_URL")
CACHES = {"default": REDIS}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CSRF_COOKIE_HTTPONLY = SESSION_COOKIE_HTTPONLY = False
SOCIAL_AUTH_URL_NAMESPACE = "social"
try:
    from psycopg2cffi import compat

    compat.register()
except ImportError:
    pass

PARAER_DATA_METHOD = "ssrd.contrib.auth.paraerData"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {"verbose": {"format": "%(levelname)s %(asctime)s %(module)s " "%(process)d %(thread)d %(message)s"}},
    "handlers": {"console": {"level": "DEBUG", "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": True},
        "default": {"handlers": ["console"], "level": "DEBUG", "propagate": True},
    },
}
