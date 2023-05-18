"""
Django settings for enroute project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import environ
import os
from dotenv import load_dotenv


env = environ.Env()
environ.Env.read_env()
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
APPEND_SLASH=False

# Application definition

INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'corsheaders',
    'oauth2_provider',
    'social_django',
    'drf_social_oauth2',
    'users',
    'utilities',
    'packages',
    'home',
    'django_filters',
    'booking',
    'experience',
    'admin_material.apps.AdminMaterialDashboardConfig',
    'django.contrib.admin',

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
]
CORS_ALLOWED_ORIGINS = [    "http://localhost:3000",    "https://api.razorpay.com",'https://admin.enroutetravel.co.in','https://enroutetravel.co.in']

CSRF_TRUSTED_ORIGINS = [    "http://localhost:3000",    "https://api.razorpay.com" ,'https://admin.enroutetravel.co.in','https://enroutetravel.co.in']


CORS_ORIGIN_WHITELIST = [    'http://localhost:3000',    'https://api.razorpay.com','https://admin.enroutetravel.co.in','https://enroutetravel.co.in']

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
    },

    'CLIENT_ID_GENERATOR_CLASS': 'oauth2_provider.generators.ClientIdGenerator',
    'ACCESS_TOKEN_EXPIRE_SECONDS':31536000 

}


ROOT_URLCONF = 'enroute.urls'

GDAL_LIBRARY_PATH = ''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends', #added
                'social_django.context_processors.login_redirect', #added
            ],
        },
    },
]

WSGI_APPLICATION = 'enroute.wsgi.application'

LOGIN_REDIRECT_URL = '/'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    ),
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'PORT': os.environ.get('POSTGRES_PORT'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR /'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
ACCESS_TOKEN_EXPIRE_SECONDS = 94630400 
USE_I18N = True

USE_TZ = True
API_BASE_URL = 'https://admin.enroutetravel.co.in/media/'
AUTH_USER_MODEL='users.Account'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR/'static'
STATICFILES_DIRS=[
    'enroute/static'
    ]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR/'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Google Authenticator
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'drf_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

# Google configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

# Define SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE to get extra permissions from Google.
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
]


EMAIL_BACKEND=os.environ.get('EMAIL_BACKEND')
EMAIL_HOST_USER=os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST=os.environ.get('EMAIL_HOST')
EMAIL_PORT=os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS=os.environ.get('EMAIL_USE_TLS')
EMAIL_HOST_PASSWORD=os.environ.get('EMAIL_HOST_PASSWORD')

AUTH_CLIENT_ID=os.environ.get('AUTH_CLIENT_ID')
AUTH_CLIENT_SECRET=os.environ.get('AUTH_CLIENT_SECRET')
RAZOR_ID=os.environ.get('RAZOR_ID')
RAZOR_KEY=os.environ.get('RAZOR_KEY')

TWILIO_SID=os.environ.get('TWILIO_SID')
TWILIO_TOKEN=os.environ.get('TWILIO_TOKEN')
 
WHATSAPP_TOKEN=os.environ.get('WHATSAPP_TOKEN')
WHATSAPP_ID=os.environ.get('WHATSAPP_ID')
WHATSAPP_NUM=os.environ.get('WHATSAPP_NUM')

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
