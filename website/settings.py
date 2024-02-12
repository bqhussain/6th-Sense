import os
from chatterbot import constants


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'enterkeyhere'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['ee384f24.ngrok.io', 'localhost', '127.0.0.1']

DIALOGFLOW_PROJECT_ID='zarish-60ed7'

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='/Users/Bilal/Downloads/DialogFlowBot/Zarish-1a18c6735e4d.json'



# Application definition

INSTALLED_APPS = [

    'bot',
    'home',
    'chatbot',
    'therapist',
    'loginstuff',
    'livechat',
    'chatterbot.ext.django_chatterbot',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_countries',
    'bootstrap_datepicker_plus',
    'bootstrap4',
    'phone_field',
    'datetimepicker',
    'stripe',
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

ROOT_URLCONF = 'website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'therapist.context_processor.appointment_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sixthsense',
        'USER': 'root',
        'PASSWORD': 'Goku420!!',

    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/
# AUTH_USER_MODEL = 'home.User'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

if DEBUG:

    STRIPE_PUBLISHABLE_KEY = 'pk_test_wM20CX424AaiJgdrjO6x3NN500Wtkr7tv8'
    STRIPE_SECRET_KEY = 'sk_test_3YWsTlaEAM4sUDN0SBEhM5py00mNeyB1zB'
else:
    STRIPE_PUBLISHABLE_KEY = ''
    STRIPE_SECRET_KEY = ''


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]



MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPALTE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'dashboard'

LOGIN_URL = 'login'
SILENCED_SYSTEM_CHECKS = ['mysql.E001']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'sixthsensefyp@gmail.com'
EMAIL_HOST_PASSWORD = 'Goku420!!'



BOOTSTRAP4 = {
    'include_jquery': True,
}

CHATTERBOT = {
    'name': 'AssistantBot',
    'logic_adapters': [
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ],
    'trainer': 'chatterbot.trainers.ChatterBotCorpusTrainer',
    'training_data': [
        'chatterbot.corpus.english'
    ],
    'storage_adapter': 'chatterbot.storage.DjangoStorageAdapter',
    'django_app_name': constants.DEFAULT_DJANGO_APP_NAME,
    'initialize': False,
}
