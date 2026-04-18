"""Django settings for TimberClaw Builder API (M0-01 minimal scaffold)."""

import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-timberclaw-dev-only-change-in-prod",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "*").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "accounts.apps.AccountsConfig",
    "llm.apps.LlmConfig",
    "gitlab_integration.apps.GitlabIntegrationConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tc_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tc_project.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# --- LLM Gateway (M0-03 / PRD §8.5) ---
TC_LLM_PROVIDER = os.environ.get("TC_LLM_PROVIDER", "mock")
TC_OPENAI_API_KEY = os.environ.get("TC_OPENAI_API_KEY", "")
TC_OPENAI_BASE_URL = os.environ.get("TC_OPENAI_BASE_URL", "https://api.openai.com/v1")
TC_DASHSCOPE_API_KEY = os.environ.get("TC_DASHSCOPE_API_KEY", "")
TC_DASHSCOPE_BASE_URL = os.environ.get(
    "TC_DASHSCOPE_BASE_URL",
    "https://dashscope.aliyuncs.com/compatible-mode/v1",
)
TC_LLM_MODEL_OPENAI = os.environ.get("TC_LLM_MODEL_OPENAI", "gpt-4o-mini")
TC_LLM_MODEL_DASHSCOPE = os.environ.get("TC_LLM_MODEL_DASHSCOPE", "qwen-turbo")
TC_LLM_MAX_OUTPUT_TOKENS = int(os.environ.get("TC_LLM_MAX_OUTPUT_TOKENS", "512"))
TC_LLM_TIMEOUT_SECONDS = float(os.environ.get("TC_LLM_TIMEOUT_SECONDS", "30"))

# --- GitLab (M0-04 / PRD §8.7) ---
TC_GITLAB_URL = os.environ.get("TC_GITLAB_URL", "").rstrip("/")
TC_GITLAB_TOKEN = os.environ.get("TC_GITLAB_TOKEN", "")
TC_GITLAB_PROJECT_ID = os.environ.get("TC_GITLAB_PROJECT_ID", "").strip()
TC_GITLAB_SSL_VERIFY = os.environ.get("TC_GITLAB_SSL_VERIFY", "1") == "1"
TC_GITLAB_ENABLE_WRITE = os.environ.get("TC_GITLAB_ENABLE_WRITE", "0") == "1"
