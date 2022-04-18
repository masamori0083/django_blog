from os import environ
import dj_database_url
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# herokuの設定
ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']
ALLOWED_HOSTS = ['*']

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)

# cloudinary.config(
#     cloud_name='dfknwzkbh',
#     api_key=os.environ.get('CLOUDINARY_API_KEY'),
#     api_secret=os.environ.get('CLOUDINARY_API_SECRET')
# )
