# 배포 체크리스트

## ✅ 완료된 설정

### 1. 정적 파일 설정
- [x] `STATIC_ROOT` 설정 완료 (`staticfiles/`)
- [x] `STATICFILES_DIRS` 중복 파일 문제 해결
- [x] `collectstatic` 실행 완료 (204개 파일 수집)
- [x] 정적 파일 서빙 URL 설정 완료

### 2. 보안 설정
- [x] HTTP 배포용 보안 설정 (HTTPS 비활성화)
- [x] `ALLOWED_HOSTS`에 `3.39.66.116` 추가
- [x] 기본 보안 헤더 설정

### 3. 환경 변수
- [x] `.env` 파일 배포용 설정 추가
- [x] `DEBUG`, `ALLOWED_HOSTS`, `USE_MOCK_API` 환경 변수화

## 🔧 배포 전 필요한 작업

### 1. 환경 변수 설정 (운영 서버에서)
```bash
# .env 파일에서 다음 값들을 운영 환경에 맞게 수정
DEBUG=False
ALLOWED_HOSTS=3.39.66.116,localhost,127.0.0.1
USE_MOCK_API=False  # 실제 API 사용 시
```

### 2. 데이터베이스 마이그레이션
```bash
source .venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### 3. 슈퍼유저 생성 (필요시)
```bash
python manage.py createsuperuser
```

### 4. 서버 실행
```bash
# 개발 서버 (테스트용)
python manage.py runserver 0.0.0.0:945

# 운영 서버 (권장)
gunicorn --bind 0.0.0.0:945 insurance_project.wsgi:application
```

## 📋 배포 후 확인사항

### 1. 기본 페이지 접속
- [ ] http://3.39.66.116:945/ (홈페이지)
- [ ] http://3.39.66.116:945/admin/ (관리자 페이지)
- [ ] http://3.39.66.116:945/static/admin/css/base.css (정적 파일)

### 2. 주요 기능 테스트
- [ ] 사용자 회원가입/로그인
- [ ] 보험 추천 시스템
- [ ] AI 상담 기능
- [ ] 사고 협의서 작성
- [ ] PDF 다운로드

### 3. API 엔드포인트 테스트
- [ ] `/insurance-recommendation/` (AI 상담)
- [ ] `/recommend/` (보험 추천)
- [ ] `/api/glossary` (용어 사전)

## ⚠️ 주의사항

### 1. 보안
- 운영 환경에서는 반드시 `DEBUG=False` 설정
- 실제 도메인 사용 시 `ALLOWED_HOSTS`에서 `*` 제거
- API 키들이 노출되지 않도록 주의

### 2. 성능
- 정적 파일은 웹서버(Nginx)에서 직접 서빙 권장
- 데이터베이스는 PostgreSQL 사용 권장 (대용량 처리 시)
- Redis 캐싱 고려 (AI API 응답 캐싱용)

### 3. 모니터링
- 로그 파일 위치: `logs/django.log`
- 에러 발생 시 로그 확인
- 메모리 사용량 모니터링 (AI 모델 로딩으로 인한)

## 🚀 배포 명령어 요약

```bash
# 1. 가상환경 활성화
source .venv/bin/activate

# 2. 의존성 설치 (새 서버인 경우)
pip install -r requirements.txt

# 3. 환경 변수 설정
# .env 파일 수정

# 4. 데이터베이스 설정
python manage.py migrate

# 5. 정적 파일 수집
python manage.py collectstatic --noinput

# 6. 서버 실행
python manage.py runserver 0.0.0.0:945
```

배포가 완료되면 http://3.39.66.116:945 로 접속하여 모든 기능이 정상 작동하는지 확인하세요!