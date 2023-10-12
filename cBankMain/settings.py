import os
from pathlib import Path
import posixpath
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

DEBUG = 'RENDER' not in os.environ

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# change the default user models to our custom model

# AUTH_USER_MODEL = 'accounts.User' 

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "dashboard", 
    "microservermails",
    'crispy_forms',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

AUTH_USER_MODEL = 'dashboard.User'

ROOT_URLCONF = "cBankMain.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR /'templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "cBankMain.wsgi.application"

#DATABASE_URL = DATABASE_URL='postgres://usuario:contraseña@localhost:5432/database_bank'

# Configuración de la base de datos predeterminada
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database_bank',
        'USER': 'postgres',
        'PASSWORD': '5179/*',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Usa dj_database_url para cargar la configuración de la base de datos desde la URL si está disponible,
# de lo contrario, utiliza la configuración predeterminada.
#DATABASES = {
    #'default': dj_database_url.config(default=DEFAULT_DB_CONFIG if DATABASE_URL is None else DATABASE_URL)
#}



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

if not DEBUG:    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'




MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'static','media')



STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')





DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# crispy config
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Login

LOGIN_URL='/login/'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

# Login With email

AUTHENTICATION_BACKENDS = [
    'dashboard.auth.DashboardUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]


# Email Configuracion

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = 'alistdktrue2@gmail.com'
EMAIL_HOST_PASSWORD = 'istmbqzrgfbpotxw'