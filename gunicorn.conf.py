# Gunicorn 설정 파일
import multiprocessing
import os

# 서버 소켓
bind = "0.0.0.0:945"
backlog = 2048

# 워커 프로세스
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# 재시작 설정
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# 로깅
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 프로세스 이름
proc_name = "insurance_platform"

# 보안
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# 성능 튜닝
worker_tmp_dir = "/dev/shm"  # 리눅스에서 메모리 기반 임시 디렉토리 사용

# 환경 변수
raw_env = [
    "DJANGO_SETTINGS_MODULE=insurance_project.settings",
]

# 개발/운영 환경 구분
if os.getenv("DEBUG", "False").lower() == "true":
    reload = True
    loglevel = "debug"
else:
    reload = False

# PID 파일
pidfile = "logs/gunicorn.pid"

# 사용자/그룹 (운영 환경에서 필요시 설정)
# user = "www-data"
# group = "www-data"
