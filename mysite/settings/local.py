from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y6u*sqteo!3cg1!s!r=vq$m=b@stp!y*yi=0iv822h*^#d8_x5'

BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
