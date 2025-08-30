from pathlib import Path
import os
from dotenv import load_dotenv
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from celery.schedules import crontab

load_dotenv()


CELERY_BEAT_SCHEDULE = {
    "update-rates-every-minute": {
        "task": "apps.whitebitx.tasks.update_rates_from_ticker",
        "schedule": crontab(), 
        "options": {"queue": "default", "expires": 3600}, 
    },
}

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-9uf62=)v=%-hn#ib#*xi11v75(16l58lrbs_15ei(!ajnl=4n)'

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters", 
    "unfold.contrib.forms", 
    "unfold.contrib.inlines", 
    "unfold.contrib.import_export",  
    "unfold.contrib.guardian", 
    "unfold.contrib.simple_history",  
    "unfold.contrib.location_field", 
    "unfold.contrib.constance",  
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', 
    'rest_framework.authtoken',
    'corsheaders',    
    'drf_spectacular', 
    "django_celery_beat",
    'ckeditor',
    'ckeditor_uploader',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'qrcode',


    #apps
    'apps.home',
    'apps.users',
    'apps.whitebitx',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('NAME'),
        'USER': os.getenv("USER"),
        'PASSWORD': os.getenv("PASSWORD"),
        'HOST': 'localhost',
        'PORT': '',
    }
}


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

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Naka',
    'DESCRIPTION': 'Документация Naka',
    'VERSION': '1.0.0',
}


NIKITA_LOGIN = os.getenv("NIKITA_LOGIN")
NIKITA_PASSWORD = os.getenv("NIKITA_PASSWORD")
NIKITA_SENDER = os.getenv("NIKITA_SENDER")

TWO_FACTOR_CALL_GATEWAY = 'two_factor.gateways.fake.Fake'
TWO_FACTOR_SMS_GATEWAY = 'two_factor.gateways.fake.Fake'
TWO_FACTOR_AUTHENTICATION_METHODS = ['otp_totp']

AML_BASE_URL= os.getenv("AML_BASE_URL")
AMLBOT_API_TOKEN = os.getenv("AMLBOT_API_TOKEN")
AML_FORM_ID = os.getenv("AML_FORM_ID")
PRO_KYC = os.getenv("ProKYC")
ADVANCED_KYC = os.getenv("AdvancedKYC")
BASIC_KYC = os.getenv("BasicKYC")

FRONTEND_PASSWORD_RESET_URL = os.getenv("FRONTEND_PASSWORD_RESET_URL")


WHITEBIT_BASE_URL = os.getenv("WHITEBIT_BASE_URL")

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "https://nako.navisdevs.ru",
    "https://naka.kz",
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = [
    "https://nako.navisdevs.ru",
    "https://naka.kz",
]

CORS_ALLOW_METHODS = (
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "DELETE"
)


LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True


CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/1")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/1")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True


STATIC_URL = 'api_static/'
STATIC_ROOT = BASE_DIR / 'api_static'


MEDIA_URL = f'{os.getenv("SITE_URL")}/media/'
MEDIA_ROOT = BASE_DIR / 'media'



EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = 'na.records7@gmail.com'
EMAIL_HOST_PASSWORD = 'zkfw efvm pglx latm'


CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"

AUTH_USER_MODEL = 'users.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

public_key = os.getenv('public_key')
secret_key = os.getenv('secret_key')




# CKEDITOR_CONFIGS = {
#     'default': {
#         "height": 400,
#         "width": 600,
#         'skin': 'moono',
#         'toolbar_Basic': [
#             ['Source', '-', 'Bold', 'Italic']
#         ],
#         'toolbar_YourCustomToolbarConfig': [
#             {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
#             {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
#             {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
#             {'name': 'forms',
#              'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
#                        'HiddenField']},
#             '/',
#             {'name': 'basicstyles',
#              'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
#             {'name': 'paragraph',
#              'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
#                        'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
#                        'Language']},
#             {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
#             {'name': 'insert',
#              'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
#             '/',
#             {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
#             {'name': 'colors', 'items': ['TextColor', 'BGColor']},
#             {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
#             {'name': 'about', 'items': ['About']},
#             '/', 
#             {'name': 'yourcustomtools', 'items': [
#                 'Preview',
#                 'Maximize',

#             ]},
#         ],
#         'toolbar': 'YourCustomToolbarConfig', 
#         'tabSpaces': 4,
#         'extraPlugins': ','.join([
#             'uploadimage', 
#             'div',
#             'autolink',
#             'autoembed',
#             'embedsemantic',
#             'autogrow',
#             'widget',
#             'lineutils',
#             'clipboard',
#             'dialog',
#             'dialogui',
#             'elementspath',
#         ]),
#     }
# }




UNFOLD = {
    "SITE_TITLE": "Админ-панель Naka",
    "SITE_HEADER": "Naka Administration",
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": _("Перейти в сайт ->"),
            "link": "https://nako.navisdevs.ru",
        },
    ],
    "DARK_MODE": True,

    "SIDEBAR": {
        "show_search": False,
        "command_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "", 
                "separator": False,
                "collapsible": False,
                "items": [
                    {"title": _("Новости"), "icon": "article", "link": reverse_lazy("admin:home_news_changelist"), "link_type": "button"},
                    {"title": _("Обратный связь"), "icon": "feedback", "link": reverse_lazy("admin:home_feedback_changelist"), "link_type": "button"},
                    {"title": _("FAQ"), "icon": "help", "link": reverse_lazy("admin:home_faq_changelist"), "link_type": "button"},
                    {"title": _("Пользователи"), "icon": "people", "link": reverse_lazy("admin:users_user_changelist"), "link_type": "button"},
                    {"title": _("Верификация"), "icon": "people", "link": reverse_lazy("admin:users_verification_changelist"), "link_type": "button"},
                    {"title": _("Финансы"), "icon": "people", "link": reverse_lazy("admin:whitebitx_finance_changelist"), "link_type": "button"},
                    {"title": _("Направление"), "icon": "people", "link": reverse_lazy("admin:whitebitx_rates_changelist"), "link_type": "button"},
                    {"title": _("История транзакций"), "icon": "people", "link": reverse_lazy("admin:whitebitx_historytransactions_changelist"), "link_type": "button"},
                    {"title": _("Tokens"), "icon": "key", "link": reverse_lazy("admin:authtoken_tokenproxy_changelist"), "link_type": "button"},
                ],
            }
        ],
    },

    "SITE_URL": "https://nako.navisdevs.ru",
    "SITE_ICON": {
        "light": lambda request: static("log.jpg"), 
        "dark": lambda request: static("log.jpg"), 
    },
    "SITE_SYMBOL": "speed",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.svg"),
        },
    ],
    "BORDER_RADIUS": "6px",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True, 
    "SHOW_BACK_BUTTON": False,

    "COLORS": {
        "primary": {
            "50":  "230, 248, 247",
            "100": "207, 241, 239",
            "200": "158, 227, 223",
            "300": "109, 213, 207",
            "400": "60, 199, 191",
            "500": "3, 163, 158",
            "600": "2, 131, 127",
            "700": "2, 99, 96",
            "800": "1, 67, 66",
            "900": "1, 35, 34",
            "950": "0, 18, 18",
        },
        "font": {
            "subtle-light": "90, 90, 90",       
            "subtle-dark": "200, 200, 200",     
            "default-light": "0, 0, 0",      
            "default-dark": "255, 255, 255",     
            "important-light": "0, 0, 0",        
            "important-dark": "255, 255, 255",  
        },
        "base": {
            "light": "255, 255, 255", 
            "dark": "30, 30, 30",      
        },
        "input": {
            "light": "255, 255, 255",
            "dark": "45, 45, 45",
        },

    },

    "SITE_LOGO": {
        "light": lambda request: static("log.jpg"),
        "dark": lambda request: static("log.jpg"),
    },
    "STYLES": [
        lambda request: static("css/admin-fix.css"),
    ],
}