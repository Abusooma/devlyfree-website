from pathlib import Path
from environ import Env
import dj_database_url


env = Env()
Env.read_env()

ENVIRONMENT = env('ENVIRONMENT')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = ENVIRONMENT != 'production'

ALLOWED_HOSTS = env('ALLOWED_HOSTS').split(',')

# Sans le slash à la fin
CSRF_TRUSTED_ORIGINS = [
    'https://devlyfree-website-production.up.railway.app',
    'http://devlyfree-website-production.up.railway.app',
]

# Pour plus de sécurité, configure aussi ceci
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Application definition

INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "compressor",
    'devlyfree',
    'accounts',
    'django_quill',
    'cloudinary_storage',
    'cloudinary',
]

# Configuration complète UNFOLD

UNFOLD = {
    "SITE_TITLE": "DevlyFree",
    "SITE_HEADER": "DevlyFree Administration",
    "SITE_URL": "/",
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True
    }
}

# Configuration Quill Editor
QUILL_CONFIGS = {
    'default': {
        'theme': 'snow',
        'modules': {
            'syntax': True,
            'toolbar': [
                [{'header': [1, 2, 3, 4, 5, 6, False]}],
                ['bold', 'italic', 'underline', 'strike'],
                ['blockquote', 'code-block'],
                [{'list': 'ordered'}, {'list': 'bullet'}],
                [{'script': 'sub'}, {'script': 'super'}],
                [{'indent': '-1'}, {'indent': '+1'}],
                [{'direction': 'rtl'}],
                [{'size': ['small', False, 'large', 'huge']}],
                [{'header': [1, 2, 3, 4, 5, 6, False]}],
                [{'color': []}, {'background': []}],
                [{'font': []}],
                ['clean'],
                ['link', 'image', 'video']
            ]
        }
    }
}

# Configuration de Cloudinary
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET'),
    'SECURE': True
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'devlyfree.middleware.SEOMiddleware',
]

WHITENOISE_MAX_AGE = 31536000  # 1 an en secondes

# Remplacez le STORAGES actuel par ceci
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Configuration de base des finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Configuration de django-compressor
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = ENVIRONMENT != 'production'
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter'
]

COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_STORAGE = 'compressor.storage.GzipCompressorFileStorage'

ROOT_URLCONF = 'devlyfree_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'devlyfree.context_processors.services_processor'
            ],
        },
    },
]

WSGI_APPLICATION = 'devlyfree_website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


if ENVIRONMENT != 'development':
    DATABASES = {
        'default': dj_database_url.config(
            default=env('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.CustomUser'
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'profile', 'accounts']


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {  # Configuration du logger racine
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'devlyfree': {  # Votre application
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
