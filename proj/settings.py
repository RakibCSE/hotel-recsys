import os
from decouple import config
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# try:
#     with open(BASE_DIR + "/" + "config.local.json", "r") as file:
#         JSON_DATA = json.load(file)
# except FileNotFoundError:
#     with open(BASE_DIR + "/" + "config.json", "r") as file:
#         JSON_DATA = json.load(file)

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['3.227.35.153']

if DEBUG:
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',

    # Custom Apps
    'hotel',
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

ROOT_URLCONF = 'proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'proj.wsgi.application'

# Database

# DATABASES = {
#     'default':
#         {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#         } if DEBUG else {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': config('DBNAME'),
#             'USER': config('DBUSER'),
#             'PASSWORD': config('DBPASSWORD'),
#             'ATOMIC_REQUESTS': True,
#             'HOST': 'localhost',
#             'PORT': '5432',
#             'CONN_MAX_AGE': 600,
#         }
# }

DATABASES = {
    'default': {
        'NAME': config('DB_NAME'),
        'ENGINE': 'django.db.backends.postgresql',
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'ATOMIC_REQUESTS': True,
        'HOST': 'localhost',
        'PORT': 5432,
        'CONN_MAX_AGE': 600,
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = "hotel.CustomUser"
LOGIN_REDIRECT_URL = "hotel:index"
LOGOUT_REDIRECT_URL = "hotel:index"

# Internationalization

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'Asia/Dhaka'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# STATICFILES_FINDERS = {
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder"
# }

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Media Settings
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# INTERNAL_IPS = JSON_DATA["internal_ip"]
#
# if not DEBUG:
#     django_heroku.settings(locals())
