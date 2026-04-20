import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR

ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]


def _split_csv_env(name, default=""):
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]

frontend_origins = _split_csv_env(
    "CORS_ALLOWED_ORIGINS",
    "https://egate-deployment-react.onrender.com,https://e-gate-system.onrender.com",
)
csrf_origins = _split_csv_env(
    "CSRF_TRUSTED_ORIGINS",
    ",".join(
        [f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"] if os.environ.get('RENDER_EXTERNAL_HOSTNAME') else []
    ),
)
for origin in frontend_origins:
    if origin not in csrf_origins:
        csrf_origins.append(origin)

CSRF_TRUSTED_ORIGINS = csrf_origins

DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
]
if whitenoise:
    MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
if corsheaders:
    MIDDLEWARE.append('corsheaders.middleware.CorsMiddleware')

MIDDLEWARE += [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


CORS_ALLOWED_ORIGINS = frontend_origins

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },

}

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}
