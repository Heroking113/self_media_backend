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

BOND_APP_ID = 'wxe33fc2974499db5f'
BOND_APP_SECRET = '06ed44a39bce2c6fe897f22ef892f5a7'


# APP_ID__&__APP_SECRET
""" 
    ('0', 'unknown'),
    ('1', '深圳大学'),
    ('2', '暨南大学深圳校区'),
    ('3', '南方科技大学'),
    ('4', '哈尔滨工业大学'),
    ('5', '香港中文大学'),
    ('6', '深圳职业技术学院'),
    ('7', '深圳信息职业技术学院'),
    ('8', '中山大学'),
    ('9', '深圳理工大学'),
    ('10', '北理莫斯科大学'),
    ('11', '深圳技师学院')
"""
SCH_ID_SECRET = [
    {}, # None
    # 深大
    {
        'APP_ID': 'wx63ab32c6254ec2b0',
        'APP_SECRET': '4bf43e6e41ca0bacbab5c9e1bdc97b5e'
    },
    # 深旅
    {
        'APP_ID': 'wx5ec552ab899fc7ec',
        'APP_SECRET': 'f529e0ad26d02e8b5e4f9db1d9ebc7d4'
    },
    # 南科大
    {
        'APP_ID': 'wx1f4d15b22dad4413',
        'APP_SECRET': '5214c49e9b2c445845b10bd144c8b50d'
    },
    # 哈工大
    {
        'APP_ID': 'wx319c637ce3c08325',
        'APP_SECRET': 'f1a3aae02a6b3be14ac30c47b284aab2'
    },
    # 港中大
    {
        'APP_ID': '',
        'APP_SECRET': ''
    },
    # 深职院
    {
        'APP_ID': 'wxbfb658323ce48fca',
        'APP_SECRET': '345d4e0517b18a869be9e483e6e051f0'
    },
    # 深信息
    {
        'APP_ID': 'wx5356c44b7996f1a7',
        'APP_SECRET': '2714ecae5015bb9772d699a3a837c49d'
    },
    # 中大
    {
        'APP_ID': 'wxa3fa8208a0431e42',
        'APP_SECRET': '2d7fac829bd0230432722ff79a356735'
    },
    # 深圳理工
    {
        'APP_ID': 'wxf04cdb84352bbc1a',
        'APP_SECRET': 'e9e50fb5f4bc9bbd80355c5e555d003d'
    },
    # 北理莫斯科
    {
        'APP_ID': '',
        'APP_SECRET': ''
    },
    # 深技师
    {
        'APP_ID': 'wxe5270890fa80d028',
        'APP_SECRET': '0dfd476f2e8b128928d054488bcf2e27'
    }
]


# SECURITY WARNING: don't run with debug turned on in production!
# 开发环境：True；生产环境：False
DEBUG = True
# DEV：开发环境；PROD：生产环境
ENV = 'DEV'
# ENV = 'PROD'

ALLOWED_HOSTS = ['*']

DOMAIN = 'http://localhost:8008' if ENV == 'DEV' else 'https://www.xizhengmy.cn'

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


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
    'apps.base_convert',
    'apps.bond_manage',
    'apps.common_manage',
    'apps.file_manage',
    'apps.idle_manage',
    'apps.topic_manage'
]

# channels相关
# INSTALLED_APPS += [
#     'channels',
#     'apps.chat'
# ]
# # 设置ASGI应用
# ASGI_APPLICATION = 'cb_backend.asgi.application'
#
# # 设置通道层的通信后台 - 本地测试用
# CHANNEL_LAYERS = {
#      "default": {
#          "BACKEND": "channels_redis.core.RedisChannelLayer",
#          'CONFIG': {"hosts": ["redis://127.0.0.1:6379/3"],},
#      },
#  }

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
    # 分页模块
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.DataPageNumberPagination',
}


ROOT_URLCONF = 'cb_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
            'PASSWORD': 'Kzzbackend666.',  # 登录数据库的密码
            'HOST': 'localhost',
            'PORT': 6895  # 数据库服务器端口，mysql默认为3306
        }
    }


# ============ Celery配置相关 ==================
# Celery application definition
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC=True


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

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
# STATIC_ROOT = os.path.join(BASE_DIR, "static").replace('\\', '/')

# 静态文件路径相关
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media").replace('\\', '/')

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
        'cb_backend': {
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

