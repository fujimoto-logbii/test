from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS.extend(
    [
        'api',
        'rest_framework',
        'corsheaders',

    ]
)

CORS_ORIGIN_WHITELIST = [
    'http://localhost',
]

ROOT_URLCONF = 'config.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'api',
        'USER': 'user',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '3306',
    }
}

AUTH_USER_MODEL = 'api.User'

# LOGIN_URL = 'account:login'

# LOGIN_REDIRECT_URL = 'main:main'

STATICROOT = os.path.join(BASE_DIR, 'static')

USE_TZ = False

STATIC_URL = '/static/'