import os

from django.core.management.utils import get_random_secret_key as get_secret_key

from problog.settings.base import *


# DEBUG = False
# # ALLOWED_HOSTS = ['www.no-outlet-blog.xyz', 'no-outlet-blog.xyz']
# ALLOWED_HOSTS = ['*.no-outlet-blog.xyz']
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('POSTGRES_DB'),
#         'USER': os.environ.get('POSTGRES_USER'),
#         'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#         'HOST': 'db',
#         'PORT': 5432,
#     }
# }
# SECRET_KEY = get_secret_key()
# EMAIL_HOST = os.environ.get('EMAIL_HOST')
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = 587
# EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') is not None
# DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
# ADMINS = [
#     ('Dylan Garrett', 'dmgarrett72@protonmail.com'),
#     ('Stoney Coffelt', 'stoneycoffelt3@gmail.com'),
# ]

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
DEBUG = False
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}
SECRET_KEY = get_secret_key()
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') is not None
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
ADMINS = [
    ('Dylan Garrett', 'dmgarrett72@protonmail.com'),
    ('Stoney Coffelt', 'stoneycoffelt3@gmail.com'),
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True