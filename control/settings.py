import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '5rgj4(l8a*v@gb_g4ilg!7)!dpkv%0uj7ldsav+zi62n9(o5rs'
DEBUG = True
ALLOWED_HOSTS = []
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/start'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'samba_manager',
    'server_manager',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'control.urls'
WSGI_APPLICATION = 'control.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#
# Gnoffel
#
STATIC_URL = '/static/'
TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

ROOT_PASSWORD = ''
SAMBA_CONF = '/etc/samba/smb.conf'
USER_HOME_DIR = '/home/{0}'
SAMBA_SHARES_DIR = '/srv/{0}'

with open('/etc/passwd') as fh:
    USERS = [ line.split(':')[0] for line in fh.readlines() if not line.startswith('#')]

with open('/etc/group') as fh2:
    GROUPS = [ line.split(':')[0] for line in fh2.readlines() if not line.startswith('#')]