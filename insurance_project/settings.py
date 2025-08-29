from pathlib import Path
from dotenv import load_dotenv
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

# 0826-5 안의 앱들을 파이썬 import 경로에 추가 (아카이브 폴더 인식용)
sys.path.append(str(BASE_DIR / "0826-5"))

# ───────────────── 보안/디버그 ─────────────────
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ───────────────── 앱 구성 ─────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 프로젝트 앱
    "insurance_app",
    "accident_project",
    # 서드파티
    "rest_framework",
]

# 아카이브(0826-5/insurance_portal) 또는 프로젝트 루트(insurance_portal) 중 존재하는 쪽만 앱으로 등록
if (BASE_DIR / "insurance_portal").exists() or (
    BASE_DIR / "0826-5" / "insurance_portal"
).exists():
    INSTALLED_APPS.append("insurance_portal")

AUTH_USER_MODEL = "insurance_app.CustomUser"

# ───────────────── 환경 변수 ─────────────────
load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ───────────────── 미들웨어 ─────────────────
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
WSGI_APPLICATION = "insurance_project.wsgi.application"

# ───────────────── 템플릿 ─────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
            BASE_DIR / "insurance_app" / "templates",
            # ✅ 아카이브 템플릿 경로(이 폴더에 partial들이 들어있음)
            BASE_DIR / "0826-5" / "insurance_portal" / "templates",
            # 루트에 풀어뒀다면 이것도 커버
            BASE_DIR / "insurance_portal" / "templates",
        ],
        "APP_DIRS": True,  # 각 앱의 templates 자동 탐색
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ───────────────── 데이터베이스 ─────────────────
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

# ───────────────── 인증/국제화 ─────────────────
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "ko-kr"
TIME_ZONE = "Asia/Seoul"
USE_I18N = True
USE_TZ = True

# ───────────────── 정적/미디어 ─────────────────
STATIC_URL = "/static/"

# 정적 파일 디렉토리 설정 (중복 방지)
STATICFILES_DIRS = []

# 메인 앱들의 정적 파일 (우선순위 높음)
_main_static_dirs = [
    BASE_DIR / "insurance_app" / "static",
    BASE_DIR / "accident_project" / "static",
]

# 아카이브 폴더의 정적 파일 (네임스페이스 적용)
_archive_static_dirs = [
    (BASE_DIR / "0826-5" / "insurance_portal" / "static", "archive_portal"),
]

# 존재하는 디렉토리만 추가
for static_dir in _main_static_dirs:
    if static_dir.exists():
        STATICFILES_DIRS.append(static_dir)

# 아카이브 디렉토리는 네임스페이스와 함께 추가
for static_dir, namespace in _archive_static_dirs:
    if static_dir.exists():
        STATICFILES_DIRS.append((namespace, static_dir))

# 루트 레벨 insurance_portal이 있다면 추가
if (BASE_DIR / "insurance_portal" / "static").exists():
    STATICFILES_DIRS.append(BASE_DIR / "insurance_portal" / "static")

# 배포용 정적 파일 수집 디렉토리
STATIC_ROOT = BASE_DIR / "staticfiles"

# 정적 파일 파인더 (collectstatic 최적화)
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# 정적 파일 압축 및 캐싱 (운영 환경용)
if not DEBUG:
    STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    )

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ───────────────── 기타 ─────────────────
USE_MOCK_API = os.getenv("USE_MOCK_API", "True").lower() == "true"
LOGIN_URL = "/login/"
X_FRAME_OPTIONS = "DENY"

DOCUMENTS_URL = "/documents/"
# 수정 (실제 파일이 insurance_app/documents에 있다면)
DOCUMENTS_ROOT = BASE_DIR / "insurance_app" / "documents"

# ───────────────── 배포 환경 설정 ─────────────────
# HTTP 배포 환경 설정 (HTTPS 미사용)
if not DEBUG:
    # 기본 보안 헤더 (HTTPS 관련 제외)
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # 쿠키 보안 (HTTPS 미사용이므로 Secure 플래그 제외)
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True

    # HTTPS 관련 설정 비활성화
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# ───────────────── 로깅 설정 ─────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "django.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"] if not DEBUG else ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "insurance_app": {
            "handlers": ["console", "file"] if not DEBUG else ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
    },
}
