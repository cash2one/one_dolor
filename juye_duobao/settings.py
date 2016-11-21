#coding=utf-8
"""
Django settings for juye_duobao project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import codecs
codecs.register(lambda name: codecs.lookup('utf8') if name == 'utf8mb4' else None)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gleb59jjoa_3-9r$)7rc4gie)p$b^q@&2h!0cqr#8es)lz1$a!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

APPEND_SLASH=False
# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'yiyuanduobao_shop',
    'duobao_wechat_app',
    'market_game_draw_circle',
    'polls',
    'xadmin',
    'crispy_forms',
    'reversion',
    'gunicorn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'juye_duobao.urls'

WSGI_APPLICATION = 'juye_duobao.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'one_dolor', #生产
        'USER': 'one_dolor_admin',
        'PASSWORD': 'AAaa1234',
        'HOST': 'rm-0xidx2c29r4wh1347o.mysql.rds.aliyuncs.com',
        'PORT': '3306',
        # 'OPTIONS': {'charset':'utf8mb4'},  
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh_cn'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'
OSS_PATH_PREFIX = 'http://juye-yiyuanduobao.oss-cn-beijing.aliyuncs.com/'




LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
                'format': '[%(name)s:%(lineno)d] [%(levelname)s]- [%(asctime)s] %(message)s'
                },
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'standard',
        },
        'default': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join('/home/duobao_log'+'/logs/','default.log'), 
            'formatter':'standard',
        },
        'user': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join('/home/duobao_log'+'/logs/','user.log'), 
            'formatter':'standard',
        },     
        'record': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join('/home/duobao_log'+'/logs/','record.log'), 
            'formatter':'standard',
        },            
        'test2_handler': {
            'level':'DEBUG',
                   'class':'logging.handlers.RotatingFileHandler',
            'filename':'path2',
            'formatter':'standard',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'default':{
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
        'user':{
            'handlers': ['user'],
            'level': 'INFO',
            'propagate': True
        },    
        'record':{
            'handlers': ['record'],
            'level': 'INFO',
            'propagate': True
        },                
         'test2':{
            'handlers': ['test2_handler'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

