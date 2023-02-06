from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, 'DjangoAirERP/.env'))

# SECRET_KEY = env("SECRET_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = bool(int(os.environ.get('DEBUG', default=1)))
# ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")
ALLOWED_HOSTS = ['*']

# Login
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
AUTH_USER_MODEL = 'user_model.User'

INSTALLED_APPS = [
    "daphne",
    'channels',
    'rest_framework',

    'django.contrib.contenttypes',
    'user_model.apps.UserModelConfig',
    'customer.apps.CustomerConfig',
    'management.apps.ManagementConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'crispy_forms',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DjangoAirERP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'DjangoAirERP.context_processor.signup_form',
                'DjangoAirERP.context_processor.login_form',
            ],
        },
    },
]

# WSGI_APPLICATION = 'DjangoAirERP.wsgi.application'
# For websocket
ASGI_APPLICATION = 'DjangoAirERP.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [('redis', 6379)],
            # "hosts": [("localhost", 6379)],
        },
    },
}
# End websocket

# Database

# Dev
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': env("NAME"),
#         'USER': env("USER"),
#         'PASSWORD': env("PASSWORD"),
#         'HOST': env("HOST"),
#         'PORT': env("PORT")
#     }
# }

# Prod
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", 'django.db.backends.postgresql'),
        "NAME": os.environ.get("SQL_DATABASE", env("NAME")),
        "USER": os.environ.get("SQL_USER", env("USER")),
        "PASSWORD": os.environ.get("SQL_PASSWORD", env("PASSWORD")),
        "HOST": os.environ.get("SQL_HOST", env("HOST")),
        "PORT": os.environ.get("SQL_PORT", env("PORT")),
    }
}

# End Database


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = False
## Static file
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# STATIC_DIR = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [STATIC_DIR]
## End Static file

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Setting up to send emails

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT")
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")

# End setting up to send emails

# django-crispy-form
# https://django-crispy-forms.readthedocs.io/en/latest/install.html#installing-django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# End django-crispy-form

# Auth by third-party services https://django-allauth.readthedocs.io/en/latest/installation.html

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v13.0',
        'GRAPH_API_URL': 'https://graph.facebook.com/v13.0',
    }
}

# # End auth
