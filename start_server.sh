#!/bin/bash

# 보험 플랫폼 서버 시작 스크립트

echo "🚀 보험 플랫폼 서버를 시작합니다..."

# 가상환경 활성화
source .venv/bin/activate

# 환경 변수 확인
if [ ! -f .env ]; then
    echo "❌ .env 파일이 없습니다. 환경 변수를 설정해주세요."
    exit 1
fi

# 로그 디렉토리 생성
mkdir -p logs

# 데이터베이스 마이그레이션 확인
echo "📊 데이터베이스 마이그레이션 확인 중..."
python manage.py migrate --check
if [ $? -ne 0 ]; then
    echo "⚠️  마이그레이션이 필요합니다. 실행 중..."
    python manage.py migrate
fi

# 정적 파일 수집 (운영 환경에서만)
if [ "$DEBUG" = "False" ]; then
    echo "📁 정적 파일 수집 중..."
    python manage.py collectstatic --noinput
fi

# 포트 설정 (환경 변수에서 가져오기)
PORT=${PORT:-8000}

# 서버 시작 방식 선택
if [ "$1" = "dev" ]; then
    echo "🔧 개발 서버로 시작합니다..."
    python manage.py runserver 0.0.0.0:$PORT
elif [ "$1" = "gunicorn" ]; then
    echo "🏭 Gunicorn으로 운영 서버를 시작합니다..."
    gunicorn -c gunicorn.conf.py insurance_project.wsgi:application
else
    echo "📖 사용법:"
    echo "  ./start_server.sh dev       # 개발 서버"
    echo "  ./start_server.sh gunicorn  # 운영 서버"
    echo ""
    echo "기본적으로 개발 서버를 시작합니다..."
    python manage.py runserver 0.0.0.0:$PORT
fi