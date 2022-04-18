import environ
import dj_database_url
from .base import *

env = environ.Env()
environ.Env.read_env(str(BASE_DIR / '.env'))

# Security
SECRET_KEY = env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Database

DATABASES = {
    'default': env.db()
}
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


cloudinary.config(
    cloud_name='dfknwzkbh',
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET')
)

# STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
