"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
import mimetypes
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

mimetypes.add_type("text/javascript", ".js", True)

DEBUG = os.getenv("DEBUG", False) == "True"

SECRET_KEY = os.getenv("SECRET_KEY")

production_level = os.getenv("PRODUCTION_LEVEL", False) == "True"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "*"]

if production_level:
    ALLOWED_HOSTS = ["www.doctoroncall.com", "doctoroncall.com"]

# Application definition

INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ckeditor",
    "rest_framework",
    "backend",
    "media",
    "blog",
    "content",
    "core",
    "inquiries",
    "dynamic_linking",
    "debug_toolbar"
]

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

CKEDITOR_CONFIGS = {"default": {"versionCheck": False}}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware"
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates"],
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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
DATABASES_COMMON = {
    "ENGINE": "django.db.backends.mysql",
    "PORT": "3306",
    "NAME": "doctoroncall",
}

# Environment-specific settings
if production_level:
    DATABASES = {
        "default": {
            **DATABASES_COMMON,
            "USER": "server-user",
            "PASSWORD": "server-pass",
            "HOST": os.getenv("DB_PROD_HOST"),
        }
    }
else:
    DATABASES = {
        "default": {
            **DATABASES_COMMON,
            "USER": "root",
            "PASSWORD": "",
            "HOST": os.getenv("DB_TEST_HOST"),
        }
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"
if production_level:    
    TIME_ZONE = "Asia/Dubai"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if DEBUG:

    STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

else:

    STATIC_ROOT = os.path.join(BASE_DIR, "static")


MEDIA_URL = "/media/"
if production_level:
    MEDIA_ROOT = ""
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOG_DIR = os.path.join(BASE_DIR, "logging/logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False if DEBUG else True,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        # Log to file
        "file": {
            "level": "ERROR",  # Change to desired logging level
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "django_errors.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        # Send emails for errors
        "mail_admins": {
            "level": "ERROR",  # Change to desired logging level
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "mail_admins"],
            "level": "ERROR",  # Change to desired logging level
            "propagate": True,
        },
    },
}


RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY")
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
EMAIL_USE_TLS = True

INTERNAL_IPS = [
    "localhost",
    "127.0.0.1",
]