import os

from problog.settings.base import *


DEBUG = True
SECRET_KEY = 'django-insecure-c%iy-)(bo7_=npvt+$lu+f=9!c$ojt#tq8qlwyz1i7y&zt@637'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
