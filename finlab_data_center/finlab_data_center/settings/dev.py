from .base import *

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

CONFIG_DATA["PRODUCTION"] = False

DATABASES = {
    'admin_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DEV_ADMIN_DBNAME', CONFIG_DATA['DEV_ADMIN_DBNAME']),
        'USER': os.getenv('DBACCOUNT', CONFIG_DATA['DBACCOUNT']),
        'PASSWORD': os.getenv('DBPASSWORD', CONFIG_DATA['DBPASSWORD']),
        'HOST': os.getenv('DBHOST', CONFIG_DATA['DBHOST']),
        'PORT': os.getenv('DBPORT', CONFIG_DATA['DBPORT']),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        }
    },
    'us_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DEV_US_DBNAME', CONFIG_DATA['DEV_US_DBNAME']),
        'USER': os.getenv('DBACCOUNT', CONFIG_DATA['DBACCOUNT']),
        'PASSWORD': os.getenv('DBPASSWORD', CONFIG_DATA['DBPASSWORD']),
        'HOST': os.getenv('DBHOST', CONFIG_DATA['DBHOST']),
        'PORT': os.getenv('DBPORT', CONFIG_DATA['DBPORT']),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        }
    },
    'tw_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DEV_TW_DBNAME', CONFIG_DATA['DEV_TW_DBNAME']),
        'USER': os.getenv('DBACCOUNT', CONFIG_DATA['DBACCOUNT']),
        'PASSWORD': os.getenv('DBPASSWORD', CONFIG_DATA['DBPASSWORD']),
        'HOST': os.getenv('DBHOST', CONFIG_DATA['DBHOST']),
        'PORT': os.getenv('DBPORT', CONFIG_DATA['DBPORT']),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        }
    }
}
DATABASES['default'] = DATABASES['admin_db']



