# vim: set fileencoding=utf-8 :
from underTheaterWS.settings import *       # noqa

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'ut_simple_test_db'
        }
}
