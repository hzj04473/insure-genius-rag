# 개발 워크플로우 및 작업 가이드

## 일반적인 개발 작업 순서

### ⚠️ 최초 개발환경 설정 (필수)

**반드시 setup-guide.md를 완전히 따라하고 시작하세요!**

### 1. 새로운 기능 개발 시

```bash
# 0. 개발환경 확인 (최초 1회)
python --version  # 3.8+ 확인
which python      # .venv/bin/python 확인
pip list | grep -E "(Django|openai|pinecone|torch)"

# 1. 브랜치 생성 (선택사항)
git checkout -b feature/새기능명

# 2. 가상환경 활성화 확인
source .venv/bin/activate

# 3. 환경 변수 확인
python manage.py check

# 4. 개발 서버 실행
python manage.py runserver
```

### 2. 모델 변경 시 필수 순서

```bash
# 1. 모델 수정 후 마이그레이션 생성
python manage.py makemigrations

# 2. 마이그레이션 검토 (생성된 파일 확인)
# 3. 마이그레이션 적용
python manage.py migrate

# 4. 테스트 실행 (있는 경우)
python manage.py test
```

### 3. 정적 파일 변경 시

```bash
# 개발 환경에서는 자동 서빙되므로 별도 작업 불필요
# 운영 환경 배포 시에만:
python manage.py collectstatic
```

### 4. AI 서비스 연동 테스트

```bash
# OpenAI API 테스트
python manage.py shell
>>> from insurance_app.llm_client import LLMClient
>>> client = LLMClient()
>>> client.test_connection()

# Pinecone 연결 테스트
>>> from insurance_app.pinecone_client import PineconeClient
>>> pc = PineconeClient()
>>> pc.test_connection()
```

### 5. 현재 프로젝트 특화 작업 순서

#### 리팩토링 작업 시

```bash
# 1. 백업 생성
cp -r accident_project accident_project_backup_$(date +%Y%m%d_%H%M%S)

# 2. 레거시 파일 정리
rm "accident_project/views old.py"
rm "accident_project/views old_2(0824_01s).py"

# 3. 폴더 구조 정리 (중복 경로 제거)
# 4. 마이그레이션 실행
python manage.py makemigrations
python manage.py migrate
```

## 앱별 작업 우선순위

### insurance_app (핵심 보험 기능)

**우선순위: 최고**

- 보험 추천 시스템 안정성 확보
- RAG 검색 성능 최적화
- 용어 사전 데이터 정확성 검증

### accident_project (사고 관리)

**우선순위: 높음**

- 레거시 파일 정리 (`views old.py`, `views old_2(0824_01s).py` 등)
- 모델 필드 일관성 확보 (damages_raw JSONField 변경)
- PDF 생성 기능 안정화

### insurance_portal (지식 베이스)

**우선순위: 중간**

- `0826-5/` 폴더 구조 정리 (중복 경로 제거)
- 챗봇 기능 통합 (`chatbot.js`, `fault_answer.js` 통합)
- 프론트엔드 디자인 통합

## 코드 품질 가이드

### Python 코드 스타일

- PEP 8 준수
- 함수/클래스 docstring 작성
- 타입 힌트 사용 권장
- 예외 처리 명시적 작성

### Django 모범 사례

- 모델 필드에 verbose_name 설정
- 외래키는 settings.AUTH_USER_MODEL 참조
- URL 패턴에 name 속성 필수
- 템플릿에서 {% load static %} 사용

### JavaScript 코드 가이드

- ES6+ 문법 사용
- 함수형 프로그래밍 선호
- DOM 조작 시 안전한 선택자 사용
- 에러 핸들링 필수

## 디버깅 및 문제 해결

### 일반적인 문제 해결 순서

1. **에러 로그 확인**: Django 콘솔 출력 검토
2. **브라우저 개발자 도구**: JavaScript 에러 확인
3. **데이터베이스 상태**: 마이그레이션 상태 확인
4. **환경 변수**: .env 파일 설정 검증
5. **의존성**: requirements.txt와 실제 설치된 패키지 비교

### 자주 발생하는 문제들

- **ImportError**: INSTALLED_APPS 설정 확인
- **TemplateDoesNotExist**: TEMPLATES DIRS 경로 확인
- **NoReverseMatch**: URL 패턴 name 확인
- **IntegrityError**: 모델 관계 및 제약조건 확인

## 성능 최적화 체크리스트

### 데이터베이스 최적화

- [ ] 자주 조회되는 필드에 인덱스 설정
- [ ] N+1 쿼리 문제 해결 (select_related, prefetch_related)
- [ ] 불필요한 데이터 조회 최소화

### 프론트엔드 최적화

- [ ] 정적 파일 압축 및 캐싱
- [ ] 이미지 최적화 (WebP 포맷 사용)
- [ ] JavaScript 번들 크기 최소화
- [ ] CSS 중복 제거

### AI 서비스 최적화

- [ ] Pinecone 쿼리 결과 캐싱
- [ ] OpenAI API 호출 최소화
- [ ] 임베딩 생성 배치 처리

## 보안 체크리스트

### Django 보안 설정

- [ ] DEBUG = False (운영 환경)
- [ ] SECRET_KEY 환경 변수로 관리
- [ ] ALLOWED_HOSTS 적절히 설정
- [ ] CSRF 보호 활성화
- [ ] XSS 보호 설정

### 데이터 보안

- [ ] 개인정보 마스킹 처리
- [ ] API 키 환경 변수 관리
- [ ] 사용자 입력 데이터 검증
- [ ] SQL 인젝션 방지

## 테스트 가이드

### 단위 테스트 작성

```python
# tests.py 예시
from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()

    def test_user_creation(self):
        user = self.User.objects.create_user(
            username='testuser',
            email='test@example.com'
        )
        self.assertEqual(user.username, 'testuser')
```

### 통합 테스트 우선순위

1. 사용자 인증 플로우
2. 보험 추천 API
3. 사고 협의서 생성
4. PDF 다운로드 기능

## 배포 준비 체크리스트

### 운영 환경 설정

- [ ] 환경 변수 설정 완료
- [ ] 데이터베이스 마이그레이션 적용
- [ ] 정적 파일 수집 완료
- [ ] 로그 설정 구성
- [ ] 에러 모니터링 설정

### 성능 테스트

- [ ] 부하 테스트 실행
- [ ] 메모리 사용량 모니터링
- [ ] API 응답 시간 측정
- [ ] 데이터베이스 쿼리 성능 확인

이 워크플로우를 따라 개발하면 일관성 있고 안정적인 코드를 유지할 수 있습니다.

## 배포 관련 추가 정보

### Docker 배포 설정

```dockerfile
FROM python:3.10-slim

# 시스템 패키지 설치 (OCR 지원)
RUN apt-get update && apt-get install -y \
    gcc g++ libpq-dev tesseract-ocr tesseract-ocr-kor poppler-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "insurance_project.wsgi:application"]
```

### 운영 환경 체크리스트

- [ ] DEBUG = False 설정
- [ ] SECRET_KEY 환경 변수로 관리
- [ ] ALLOWED_HOSTS 적절히 설정
- [ ] SSL 인증서 설정
- [ ] 데이터베이스 백업 시스템 구축
- [ ] 로그 모니터링 설정
