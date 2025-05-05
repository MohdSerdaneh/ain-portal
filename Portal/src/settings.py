import os
from pathlib import Path
from django.contrib.messages import constants as messages

# Project Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------
# Message Tags for Bootstrap Alert Styling
# ----------------------------------------
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# ----------------------------------------
# Security & General Config
# ----------------------------------------
SECRET_KEY = 'django-insecure-^=#h(a@@0m)lhf+&k15m$xq4wvr92m*!d5__h0e3(zm)jiio4#'
GOOGLE_RECAPTCHA_SECRET_KEY = '6LfszWMeAAAAABmobDa2QPSZ6Xxu3_wQvyFcfMAy'

DEBUG = True  # ⚠️ Set to False in production!
ALLOWED_HOSTS = ["*"]  # ⚠️ Set specific domains in production

# ----------------------------------------
# Installed Applications
# ----------------------------------------
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'accounts.apps.AccountsConfig',
    'teacher.apps.TeacherConfig',
    'student.apps.StudentConfig',
    'adminDashboard.apps.AdmindashboardConfig',
    'quiz.apps.QuizConfig',
    'meeting.apps.MeetingConfig',

    # 3rd party
    'imagekit',
    'django_cleanup.apps.CleanupConfig',
    'django_filters',
    'crispy_forms',
    'crispy_tailwind',
    'channels',  # Optional: Only needed if using WebSockets
]

# ----------------------------------------
# Middleware Configuration
# ----------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'src.current_user.CurrentUserMiddleware',  # Custom middleware to access current user in forms
]

# ----------------------------------------
# URL Routing & WSGI/ASGI
# ----------------------------------------
ROOT_URLCONF = 'src.urls'
WSGI_APPLICATION = 'src.wsgi.application'
ASGI_APPLICATION = 'src.asgi.application'

# ----------------------------------------
# Channels (WebSocket layer)
# ----------------------------------------
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# ----------------------------------------
# Templates
# ----------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # You can add custom template paths here
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

# ----------------------------------------
# Database
# ----------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ----------------------------------------
# Authentication
# ----------------------------------------
AUTH_USER_MODEL = 'accounts.User'  # Custom User model
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'login'

# ----------------------------------------
# Password Validators
# ----------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------------------
# Internationalization
# ----------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ----------------------------------------
# Static & Media Files
# ----------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/static'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ----------------------------------------
# Crispy Forms (Tailwind integration)
# ----------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# ----------------------------------------
# Cache (Dummy in dev, Memcached in prod)
# ----------------------------------------
TEST_MEMCACHE = False
if not DEBUG or TEST_MEMCACHE:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# ----------------------------------------
# Security Headers
# ----------------------------------------
SECURE_REFERRER_POLICY = "None"
X_FRAME_OPTIONS = 'SAMEORIGIN'
