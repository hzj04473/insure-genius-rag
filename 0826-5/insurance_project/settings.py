from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# 환경 변수 로드
load_dotenv()

# ───────────────── 보안/디버그 ─────────────────
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "insurance_app",
    "rest_framework",
    "insurance_portal",
]

AUTH_USER_MODEL = "insurance_app.CustomUser"

# ───────────────── 환경 변수 ─────────────────
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_KEY_MY = os.getenv("PINECONE_API_KEY_MY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
FAULT_INDEX_NAME = os.getenv("FAULT_INDEX_NAME")
UPSTAGE_API_KEY = os.getenv("UPSTAGE_API_KEY")
UPSTAGE_EMBED_MODEL = os.getenv("UPSTAGE_EMBED_MODEL", "solar-embedding-1-large")
UPSTAGE_EMBED_URL = os.getenv(
    "UPSTAGE_EMBED_URL", "https://api.upstage.ai/v1/embeddings"
)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "insurance_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "insurance_app" / "templates"],  # 앱 템플릿 경로 추가
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "insurance_project.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 🌐 한국어/한국 시간대 설정
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# ───────────────── 정적/미디어 ─────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# 정적 파일 디렉토리 설정
STATICFILES_DIRS = []
_static_candidates = [
    BASE_DIR / "insurance_app" / "static",
    BASE_DIR / "insurance_portal" / "static",
]
for static_dir in _static_candidates:
    if static_dir.exists():
        STATICFILES_DIRS.append(static_dir)

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ───────────────── 기타 ─────────────────
USE_MOCK_API = os.getenv("USE_MOCK_API", "True").lower() == "true"
LOGIN_URL = "/login/"
X_FRAME_OPTIONS = "DENY"

# ───────────────── 배포 환경 설정 ─────────────────
if not DEBUG:
    # 기본 보안 헤더
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # 쿠키 보안 (HTTP 환경)
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True

    # HTTPS 관련 설정 비활성화
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
