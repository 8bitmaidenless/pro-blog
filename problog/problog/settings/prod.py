import os

from problog.settings.base import *


DEBUG = False
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {

    }
}
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT'), 587)
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS') is not None
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
ADMINS = [
    ('Dylan Garrett', 'dmgarrett72@protonmail.com'),
    ('Stoney Coffelt', 'stoneycoffelt3@gmail.com'),
]