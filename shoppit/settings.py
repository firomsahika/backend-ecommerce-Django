
from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()


# Access the OpenAI API key from the environment variable
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure--b@udpeo&@w^3e$yxt3^737b4)6*n&bv9a%+47_qc6kacwj#p!'


DEBUG = True

ALLOWED_HOSTS = ["myshop-app-hjgf.onrender.com","localhost","127.0.0.1"]




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'shop_app',
    'chatbot',
    'chapa',
    'corsheaders',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [

"http://localhost:5173",
"http://localhost:5174",
"http://localhost:5175",
"https://shoppit-jqdk.onrender.com"

]

ROOT_URLCONF = 'shoppit.urls'

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

WSGI_APPLICATION = 'shoppit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_STORAGE =  "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = 'img/'
MEDIA_ROOT = BASE_DIR/"media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'core.CustomUser'


REST_FRAMEWORK = {
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )

}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7), 
}

CHAPA_SECRET = "CHASECK_TEST-CIYSZgWmpEB4ed8X4dlPhKbvrzyHSTxQ"
CHAPA_PUBLIC_KEY = "CHAPUBK_TEST-GY6MMxalo87x6yMfh9GnFcLwOSXG7Y4x"
CHAPA_API_URL = 'https://api.chapa.co'
CHAPA_API_VERSION = 'v1'
CHAPA_TRANSACTION_MODEL = 'chapa.ChapaTransaction'
CHAPA_WEBHOOK_URL = "http://127.0.0.1:8000/api/chapa-webhook"


REACT_BASE_URL = os.getenv('REACT_BASE_URL', "http://localhost:5173/")