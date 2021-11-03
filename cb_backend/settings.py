"""
Django settings for cb_backend project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a2nqj%9)l8vbxtry2yfy+zlqlx9e0s#4gm*0u*8$q7d_y2g7zu'

# SECURITY WARNING: don't run with debug turned on in production!
# 开发环境：True；生产环境：False
DEBUG = True
# DEV：开发环境；PROD：生产环境
ENV = 'DEV'
# ENV = 'PROD'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.user_manage',
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

REST_FRAMEWORK = {
    # 修改默认返回JSON的renderer的类
    'DEFAULT_RENDERER_CLASSES': (
        'utils.renderer.CustomRenderer',
    ),
    # 全局配置异常模块
    'EXCEPTION_HANDLER': 'utils.intercepter.custom_exception_handler',
}


ROOT_URLCONF = 'cb_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'cb_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

if ENV == 'DEV':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # 指定数据库驱动
            'NAME': 'cb_db',  # 指定的数据库名
            'USER': 'root',  # 数据库登录的用户名
            'PASSWORD': 'Heroking113.',  # 登录数据库的密码
            'HOST': 'localhost',
            'PORT': 6895  # 数据库服务器端口，mysql默认为3306
        }
    }
elif ENV == 'PROD':
    # TODO
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',  # 指定数据库驱动
            'NAME': 'cb_db',  # 指定的数据库名
            'USER': 'root',  # 数据库登录的用户名
            'PASSWORD': 'Heroking113.',  # 登录数据库的密码
            'HOST': 'localhost',
            'PORT': 6895  # 数据库服务器端口，mysql默认为3306
        }
    }



# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# 日志配置
BASE_LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(BASE_LOG_DIR):
    os.makedirs(BASE_LOG_DIR)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
       'default': {
            'format': '[%(levelname)s] [%(name)s] %(asctime)s %(pathname)s %(module)s %(funcName)s %(lineno)d: %(message)s'
       }
    },
    'handlers': {
        'backend': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, 'cb_backend.log'),
            'maxBytes':1024 * 1024 * 20,
            'backupCount': 7,
            'formatter':'default',
        },
        'request': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_LOG_DIR, 'request.log'),
            'maxBytes': 1024 * 1024 * 20,
            'backupCount': 7,
            'formatter': 'default',
        }
    },
    'loggers': {
        'grape_backend': {
            'handlers': ['backend'],
            'level': 'INFO'
        },
        'django': {
            'handlers': ['request'],
            'level': 'WARNING'
        },
        'django.request': {
            'handlers': ['request'],
            'level': 'WARNING'
        }
    }
}

