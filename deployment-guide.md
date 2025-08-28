# 배포 가이드

## 개요

AI 보험 플랫폼의 개발 환경부터 운영 환경까지의 배포 가이드입니다. 단계별로 환경을 구성하고 배포하는 방법을 설명합니다.

## 개발 환경 설정

### 1. 시스템 요구사항

#### 최소 요구사항

- **OS**: macOS 10.15+, Ubuntu 18.04+, Windows 10+
- **Python**: 3.8 이상
- **메모리**: 4GB RAM
- **디스크**: 10GB 여유 공간

#### 권장 요구사항

- **OS**: macOS 12+, Ubuntu 20.04+
- **Python**: 3.10 이상
- **메모리**: 8GB RAM
- **디스크**: 20GB 여유 공간

### 2. 로컬 개발 환경 구축

#### 저장소 클론 및 가상환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd insurance-platform

# 가상환경 생성 및 활성화
python -m venv .venv

# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

#### 의존성 설치

```bash
# Python 패키지 설치
pip install --upgrade pip
pip install -r requirements.txt

# 개발용 추가 패키지 (선택사항)
pip install -r requirements-dev.txt
```

#### 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# 필수 환경 변수 설정
cat > .env << EOF
# Django 설정
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# AI 서비스 API 키
OPENAI_API_KEY=your-openai-api-key
HF_TOKEN=your-huggingface-token
UPSTAGE_API_KEY=your-upstage-api-key
LANGCHAIN_API_KEY=your-langchain-api-key

# Pinecone 설정
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_REGION=us-east-1
PINECONE_INDEX_NAME=insurance-rag

# 모델 설정
LLM_MODEL=gpt-4
EMBED_MODEL=intfloat/multilingual-e5-large
EMBED_DIM=1024

# RAG 시스템 튜닝
TERM_GATE_MODE=auto
RAG_MIN_RATIO=0.35
RAG_MIN_COUNT=5
USE_LLM_REFINE=1
EOF
```

#### 데이터베이스 초기화

```bash
# 마이그레이션 실행
python manage.py makemigrations
python manage.py migrate

# 슈퍼유저 생성
python manage.py createsuperuser

# 초기 데이터 로드 (선택사항)
python manage.py load_glossary
python manage.py upload_all_to_pinecone
```

#### 개발 서버 실행

```bash
# 개발 서버 시작
python manage.py runserver

# 특정 포트로 실행
python manage.py runserver 8080

# 외부 접속 허용
python manage.py runserver 0.0.0.0:8000
```

## 스테이징 환경 배포

### 1. Docker를 이용한 컨테이너화

#### Dockerfile 작성

```dockerfile
FROM python:3.10-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    tesseract-ocr \
    tesseract-ocr-kor \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 정적 파일 수집
RUN python manage.py collectstatic --noinput

# 포트 노출
EXPOSE 8000

# 애플리케이션 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "insurance_project.wsgi:application"]
```

#### docker-compose.yml 작성

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - '8000:8000'
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:password@db:5432/insurance_db
    depends_on:
      - db
      - redis
    volumes:
      - ./media:/app/media
      - ./staticfiles:/app/staticfiles

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: insurance_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - '5432:5432'

  redis:
    image: redis:6-alpine
    ports:
      - '6379:6379'

  nginx:
    image: nginx:alpine
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./staticfiles:/var/www/static
      - ./media:/var/www/media
    depends_on:
      - web

volumes:
  postgres_data:
```

#### 스테이징 배포 실행

```bash
# Docker 이미지 빌드 및 실행
docker-compose up -d

# 데이터베이스 마이그레이션
docker-compose exec web python manage.py migrate

# 정적 파일 수집
docker-compose exec web python manage.py collectstatic --noinput

# 로그 확인
docker-compose logs -f web
```

## 운영 환경 배포

### 1. AWS 배포

#### EC2 인스턴스 설정

```bash
# EC2 인스턴스 접속
ssh -i your-key.pem ubuntu@your-ec2-ip

# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Docker Compose 설치
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### RDS PostgreSQL 설정

```bash
# AWS CLI 설치 및 설정
sudo apt install awscli -y
aws configure

# RDS 인스턴스 생성 (AWS CLI)
aws rds create-db-instance \
    --db-instance-identifier insurance-db \
    --db-instance-class db.t3.micro \
    --engine postgres \
    --master-username admin \
    --master-user-password your-password \
    --allocated-storage 20 \
    --vpc-security-group-ids sg-xxxxxxxx
```

#### 환경 변수 설정 (운영용)

```bash
# 운영 환경 변수 설정
cat > .env.production << EOF
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 데이터베이스 (RDS)
DATABASE_URL=postgresql://admin:password@your-rds-endpoint:5432/insurance_db

# AI 서비스 (운영용 키)
OPENAI_API_KEY=your-production-openai-key
PINECONE_API_KEY=your-production-pinecone-key

# 보안 설정
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
EOF
```

### 2. Google Cloud Platform 배포

#### Cloud Run 배포

```bash
# Google Cloud SDK 설치 및 인증
curl https://sdk.cloud.google.com | bash
gcloud auth login
gcloud config set project your-project-id

# 컨테이너 이미지 빌드 및 푸시
gcloud builds submit --tag gcr.io/your-project-id/insurance-platform

# Cloud Run 서비스 배포
gcloud run deploy insurance-platform \
    --image gcr.io/your-project-id/insurance-platform \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars DEBUG=False,SECRET_KEY=your-secret
```

#### Cloud SQL PostgreSQL 설정

```bash
# Cloud SQL 인스턴스 생성
gcloud sql instances create insurance-db \
    --database-version POSTGRES_13 \
    --tier db-f1-micro \
    --region us-central1

# 데이터베이스 생성
gcloud sql databases create insurance_db --instance insurance-db

# 사용자 생성
gcloud sql users create admin --instance insurance-db --password your-password
```

### 3. Kubernetes 배포

#### Kubernetes 매니페스트

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: insurance-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: insurance-platform
  template:
    metadata:
      labels:
        app: insurance-platform
    spec:
      containers:
        - name: web
          image: your-registry/insurance-platform:latest
          ports:
            - containerPort: 8000
          env:
            - name: DEBUG
              value: 'False'
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: db-secret
                  key: url
          resources:
            requests:
              memory: '512Mi'
              cpu: '250m'
            limits:
              memory: '1Gi'
              cpu: '500m'

---
apiVersion: v1
kind: Service
metadata:
  name: insurance-platform-service
spec:
  selector:
    app: insurance-platform
  ports:
    - port: 80
      targetPort: 8000
  type: LoadBalancer
```

#### 배포 실행

```bash
# 시크릿 생성
kubectl create secret generic db-secret \
    --from-literal=url=postgresql://user:pass@host:5432/db

# 애플리케이션 배포
kubectl apply -f deployment.yaml

# 상태 확인
kubectl get pods
kubectl get services
```

## 모니터링 및 로깅

### 1. 로그 설정

#### Django 로깅 설정

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/insurance.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

### 2. 성능 모니터링

#### Prometheus + Grafana 설정

```yaml
# monitoring/docker-compose.yml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    ports:
      - '9090:9090'
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - '3000:3000'
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
```

### 3. 헬스 체크

#### 헬스 체크 엔드포인트

```python
# insurance_app/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # 데이터베이스 연결 확인
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        # 외부 서비스 확인 (선택사항)
        # check_pinecone_connection()
        # check_openai_connection()

        return JsonResponse({
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'version': '1.0.0'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=503)
```

## 보안 설정

### 1. HTTPS 설정

#### Let's Encrypt SSL 인증서

```bash
# Certbot 설치
sudo apt install certbot python3-certbot-nginx

# SSL 인증서 발급
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 자동 갱신 설정
sudo crontab -e
# 다음 라인 추가: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. 방화벽 설정

#### UFW 방화벽 설정

```bash
# UFW 활성화
sudo ufw enable

# 필요한 포트만 열기
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 상태 확인
sudo ufw status
```

### 3. 환경 변수 보안

#### AWS Systems Manager Parameter Store

```bash
# 파라미터 저장
aws ssm put-parameter \
    --name "/insurance-platform/prod/SECRET_KEY" \
    --value "your-secret-key" \
    --type "SecureString"

# 파라미터 조회
aws ssm get-parameter \
    --name "/insurance-platform/prod/SECRET_KEY" \
    --with-decryption
```

## 백업 및 복구

### 1. 데이터베이스 백업

#### 자동 백업 스크립트

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="insurance_db"

# PostgreSQL 백업
pg_dump -h localhost -U admin $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# 압축
gzip $BACKUP_DIR/db_backup_$DATE.sql

# 7일 이상 된 백업 파일 삭제
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +7 -delete

echo "Backup completed: db_backup_$DATE.sql.gz"
```

#### 크론탭 설정

```bash
# 매일 새벽 2시에 백업 실행
0 2 * * * /path/to/backup.sh >> /var/log/backup.log 2>&1
```

### 2. 파일 백업

#### rsync를 이용한 파일 동기화

```bash
# 미디어 파일 백업
rsync -avz --delete /app/media/ backup-server:/backups/media/

# 정적 파일 백업
rsync -avz --delete /app/staticfiles/ backup-server:/backups/static/
```

## 트러블슈팅

### 1. 일반적인 문제들

#### 메모리 부족

```bash
# 메모리 사용량 확인
free -h
ps aux --sort=-%mem | head

# 스왑 파일 생성
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### 디스크 공간 부족

```bash
# 디스크 사용량 확인
df -h
du -sh /var/log/*

# 로그 파일 정리
sudo journalctl --vacuum-time=7d
sudo find /var/log -name "*.log" -mtime +7 -delete
```

### 2. 성능 최적화

#### Gunicorn 설정

```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 5
```

#### Nginx 설정

```nginx
# nginx.conf
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 50M;

    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /var/www/media/;
        expires 1y;
        add_header Cache-Control "public";
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 배포 체크리스트

### 배포 전 확인사항

- [ ] 모든 테스트 통과
- [ ] 환경 변수 설정 완료
- [ ] 데이터베이스 마이그레이션 확인
- [ ] 정적 파일 수집 완료
- [ ] SSL 인증서 설정
- [ ] 방화벽 설정 완료
- [ ] 백업 시스템 구축
- [ ] 모니터링 시스템 설정

### 배포 후 확인사항

- [ ] 애플리케이션 정상 동작
- [ ] 헬스 체크 통과
- [ ] 로그 정상 기록
- [ ] 성능 지표 정상
- [ ] 보안 스캔 통과
- [ ] 백업 정상 동작

이 가이드를 따라 단계별로 배포하면 안정적인 운영 환경을 구축할 수 있습니다.
