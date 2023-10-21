import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-rcrvx-j^bi+oz+3@9d&ub2#r4%@zzmy7=n1%35n0-^-+hep_0u')


DEBUG = os.environ.get("DEBUG","False") == "True"



ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")


#ALLOWED_HOSTS = []

# change the default user models to our custom model

# AUTH_USER_MODEL = 'accounts.User' 

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "dashboard", 
    "microservermails",
    'crispy_forms',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
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



database_url=os.environ.get("DATABASE_URL")

#database_url="postgres://bank_data_base_user:pJ6cuYdLUqjvD0jiwqzajUznDpQFvKqf@dpg-ckpt37o1hnes73f3v7dg-a.oregon-postgres.render.com/bank_data_base"

DATABASES["default"] = dj_database_url.parse(database_url)



#DATABASES["default"] = dj_database_url.parse("postgres://database_bank_user:E7jvQkOhYKPvSFlzDD9t47ooARUE4doD@dpg-ckk4fd6mlsqc73bp24r0-a.oregon-postgres.render.com/database_bank")



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

EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')