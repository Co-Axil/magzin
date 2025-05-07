"""
Django settings for config project.
"""

from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings - Production uchun MUST!
SECRET_KEY = os.environ.get('SECRET_KEY')  # Environmentdan olinadi
DEBUG = False
ALLOWED_HOSTS = ['*']  # Aniq domainlar

# Application definition
INSTALLED_APPS = [
    'admin_tabler.apps.AdminTablerConfig',
    'rest_framework',
    'corsheaders',  # CORS oldiga o'tkazildi
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'onlinemarket',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS eng oldinda
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]



# Database (PostgreSQL + Connection Pool)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 300,
        'OPTIONS': {
            'application_name': 'django_app',  # PgBouncer uchun
        }
    }
}

# CORS sozlamalari
CORS_ORIGIN_WHITELIST = [
    'https://yourdomain.com',
    'https://client-app.com',
]
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST  # CSRF uchun

# Cache va Session (Redis)
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": os.environ.get('REDIS_PASSWORD', ''),
        },
        "KEY_PREFIX": "django_cache"
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# Celery config
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_TRACK_STARTED = True
CELERY_ACKS_LATE = True

# Static & Media (AWS S3)
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False

STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'

# Qolgan sozlamalar
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SPECTACULAR_SETTINGS = {
    'TITLE': 'OnlineMarket API',
}


# Xavfsizlik sozlamalari
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

