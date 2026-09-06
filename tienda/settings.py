"""
Configuración del proyecto tienda_ropa.
Cada sección está explicada con comentarios.
"""

from pathlib import Path

# Ruta base del proyecto (carpeta tienda_ropa/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta. En producción debe cambiarse y protegerse.
SECRET_KEY = 'django-insecure-)p0l2o464al4az1as6#+b#bj9ghud^ef^lp%bzhgig(pdpfvmc'

# Muestra errores detallados. En produccion debe ser False.
DEBUG = True

ALLOWED_HOSTS = []


# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Nuestras aplicaciones:
    'productos',
    'pedidos',
]


# Middleware: capas de seguridad que procesan cada peticion
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'tienda.urls'


# Plantillas: le dice a Django donde buscar los archivos HTML
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'productos.context_processors.pedidos_pendientes',  # ← NUEVO
            ],
        },
    },
]


WSGI_APPLICATION = 'tienda.wsgi.application'


# Base de datos SQLite para desarrollo
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validacion de contrasenas
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


# Idioma y zona horaria
LANGUAGE_CODE = 'es-419'

TIME_ZONE = 'America/La_Paz'

USE_I18N = True

USE_TZ = True


# Archivos estaticos (CSS y JS)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']


# Archivos media (imagenes subidas por el administrador)
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Redirecciones del sistema de login
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'panel_productos'
LOGOUT_REDIRECT_URL = 'inicio'


# Configuracion personalizada de la tienda
# Numero de WhatsApp: codigo de pais + numero, sin + ni espacios
# Ejemplo Bolivia: '59171234567'
TIENDA_CONFIG = {
    'WHATSAPP_NUMERO': '59174635330',
    'NOMBRE_TIENDA': 'ModaShop',
}