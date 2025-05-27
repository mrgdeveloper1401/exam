from pathlib import Path
from async_django.utils.simple_jwt import *
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = 'django-insecure-#i6(oj7bmr88z3hco=h1q&&z^k^pfvqh=n61+32ccul0$w@&&e'
else:
    SECRET_KEY = config('SECRET_KEY', cast=str)

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ''.join(config("PRODUCTION_ALLOWED_HOST", cast=list)).split(",")

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "django.contrib.admin",
    "daphne",
    'django.contrib.staticfiles',

#     third party package
    "rest_framework",
    "drf_spectacular",
    "corsheaders",

    # third party app
    "products.apps.ProductsConfig",
    "accounts.apps.AccountsConfig",
    "core.apps.CoreConfig",
    'exam.apps.ExamConfig'
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

if not DEBUG:
    # insert cors middleware into first middleware
    MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware",)
    MIDDLEWARE += [
        # whitenoise middlewere
        "whitenoise.middleware.WhiteNoiseMiddleware",
    ]

ROOT_URLCONF = 'async_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI_APPLICATION = 'async_django.wsgi.application'
ASGI_APPLICATION = 'async_django.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

if not DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config("COMPOSE_POSTGRES_DB", cast=str),
            "PORT": "5432",
            "USER": config("COMPOSE_POSTGRES_USER", cast=str),
            "PASSWORD": config("COMPOSE_POSTGRES_PASSWORD", cast=str),
            "HOST": "postgres",
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': "async_django_db",
            "PORT": "5433",
            "USER": "postgres",
            "PASSWORD": "postgres",
            "HOST": "localhost",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# collect static , save static in directory
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# custom user model
AUTH_USER_MODEL = "accounts.User"

# config drf framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# config simple jwt secret key
SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY

# max image size for upload image
IMAGE_SIZE_MAX = 2

# permission async
# DJANGO_ALLOW_ASYNC_UNSAFE = True

# config storages
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# config cors
# for use test
CORS_ALLOW_ALL_ORIGINS = True
# for use production
CORS_ALLOWED_ORIGINS = ''.join(config("CORS_ALLOW_ORIGINS_CORS", cast=list)).split(",")
