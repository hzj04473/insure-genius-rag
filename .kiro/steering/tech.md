# 기술 스택 및 개발 환경

## 핵심 프레임워크

- **Django 5.2.4** - 메인 웹 프레임워크
- **Django REST Framework** - REST API 개발
- **Python 3.x** - 주 개발 언어 (권장: 3.10+)
- **SQLite** - 개발용 기본 데이터베이스
- **PostgreSQL** - 운영 환경 데이터베이스 지원 (psycopg2-binary)

## AI 및 머신러닝 스택

- **OpenAI GPT-4o-mini** - 자연어 처리 및 대화형 추천 엔진
- **Pinecone** - RAG 검색용 벡터 데이터베이스 (768차원, 코사인 유사도)
- **SentenceTransformers** - 텍스트 임베딩 생성 (paraphrase-multilingual-MiniLM-L12-v2)
- **HuggingFace Transformers** - 사전 훈련된 모델 호스팅 및 추론
- **PyTorch** - 딥러닝 프레임워크
- **scikit-learn** - 전통적인 머신러닝 알고리즘

## 문서 처리 라이브러리

- **PyMuPDF, PyPDF2, pdfplumber** - PDF 문서 파싱 및 텍스트 추출
- **pdf2image, pytesseract** - OCR 기능 (이미지에서 텍스트 추출)
- **Pillow** - 이미지 처리 및 변환

## 외부 API 통합

- **CODEF API** - 실제 보험료 계산 (운영 환경)
- **Mock Server** - 개발용 보험료 계산 시뮬레이션

## 환경 설정 및 배포

- **python-dotenv** - 환경 변수 관리
- **가상환경 (.venv)** - 의존성 격리
- **requirements.txt** - 패키지 의존성 관리
- **Docker** - 컨테이너화 배포 지원

## 완벽한 초기 설정 (⚠️ setup-guide.md 필수 참조)

```bash
# 🔥 중요: 시스템 패키지 먼저 설치 (OS별)
# macOS: brew install python@3.10 tesseract tesseract-lang-korean poppler git
# Ubuntu: sudo apt install python3.10 tesseract-ocr tesseract-ocr-kor poppler-utils
# Windows: choco install python310 tesseract git

# 1. 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# Windows: .venv\Scripts\activate

# 2. 의존성 설치 (시간 소요 주의)
pip install --upgrade pip
pip install -r requirements.txt

# 3. 환경 변수 설정 (.env 파일 생성 필수)
# 필수 키: OPENAI_API_KEY, PINECONE_API_KEY, HF_TOKEN

# 4. 데이터베이스 초기화
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 5. 개발 서버 실행
python manage.py runserver
```

## 주요 개발 명령어

### 개발 서버 실행

```bash
# 개발 서버 시작 (기본 포트 8000)
python manage.py runserver

# 특정 포트로 실행
python manage.py runserver 8080
```

### 데이터베이스 관리

```bash
# 모델 변경사항을 마이그레이션 파일로 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate

# 특정 앱의 마이그레이션만 적용
python manage.py migrate insurance_app
```

### 정적 파일 관리

```bash
# 정적 파일 수집 (운영 환경용)
python manage.py collectstatic

# 개발 환경에서는 자동으로 서빙됨
```

### 데이터 관리 (커스텀 명령어)

```bash
# 용어 사전 데이터 로드
python manage.py load_glossary

# 보험 문서를 Pinecone에 업로드
python manage.py shell
>>> from insurance_app.upload_all_to_pinecone import main
>>> main()

# 과실 판정 지식베이스 재색인
python manage.py reindex_fault_md

# Pinecone에서 모든 벡터 삭제 (주의!)
python manage.py shell
>>> from insurance_app.purge_all_vectors import main
>>> main()
```

### 개발 도구

```bash
# Django 쉘 실행
python manage.py shell

# 데이터베이스 쉘 실행
python manage.py dbshell

# 테스트 실행
python manage.py test
```

## 핵심 아키텍처 구성요소

### 메인 애플리케이션

- `insurance_app/` - 보험 추천 및 RAG 시스템
- `accident_project/` - 교통사고 관리 시스템
- `insurance_portal/` - 지식 베이스 (아카이브)

### AI/ML 모듈

- `llm_client.py` - OpenAI GPT 통합
- `rag_search.py` - RAG 구현
- `pinecone_client.py` - Pinecone 벡터 DB 클라이언트
- `pinecone_search.py` - 보험 약관 검색

### 데이터 처리 모듈

- `pdf_processor.py` - PDF 문서 처리
- `pdf_to_pinecone.py` - 벡터 임베딩 파이프라인
- `upload_all_to_pinecone.py` - 배치 업로드

### API 통합 모듈

- `insurance_api.py` - CODEF API 통합
- `insurance_mock_server.py` - 개발용 Mock 서버
- `codef_client.py` - CODEF API 클라이언트

### 핵심 모델

- `CustomUser` - 확장된 사용자 모델 (birth_date, gender, has_license)
- `Clause` - 보험 약관 조항
- `InsuranceQuote` - 보험 추천 결과
- `GlossaryTerm` - 보험 용어 사전
- `Agreement` - 교통사고 협의서

## 환경 변수 설정

`.env` 파일에 다음 변수들이 필요합니다:

### AI 서비스 API 키

- `OPENAI_API_KEY` - OpenAI GPT API 접근 키
- `HF_TOKEN` - HuggingFace 모델 접근 토큰
- `LANGCHAIN_API_KEY` - LangChain 서비스 키
- `UPSTAGE_API_KEY` - Upstage AI 서비스 키

### 벡터 데이터베이스 설정

- `PINECONE_API_KEY` - Pinecone 벡터 DB API 키
- `PINECONE_REGION` - Pinecone 서버 지역 (예: us-east-1)
- `PINECONE_INDEX_NAME` - 벡터 인덱스 이름 (기본값: insurance-rag)
- `PINECONE_ENV` - Pinecone 환경 (serverless)

### 외부 API 설정

- `CODEF_CLIENT_ID` - CODEF API 클라이언트 ID
- `CODEF_CLIENT_SECRET` - CODEF API 클라이언트 시크릿
- `USE_MOCK_API` - Mock 서버 사용 여부 (True/False)

### 모델 설정

- `LLM_MODEL` - 사용할 언어 모델 (예: gpt-4o-mini)
- `EMBED_MODEL` - 임베딩 모델 (기본값: intfloat/multilingual-e5-large)
- `EMBED_DIM` - 임베딩 차원 수 (1024)

### RAG 시스템 튜닝

- `TERM_GATE_MODE` - 용어 필터링 모드 (auto/and/or/off)
- `RAG_MIN_RATIO` - 최소 유사도 비율 (예: 0.35)
- `RAG_MIN_COUNT` - 최소 검색 결과 수 (예: 5)
- `USE_LLM_REFINE` - LLM 결과 정제 사용 여부 (1/0)

## 개발 모드 설정

### Mock vs Production 모드

- `settings.py`에서 `USE_MOCK_API = True`로 설정하면 개발 모드
- Mock 서버 사용으로 실제 CODEF API 호출 없이 개발 가능
- 운영 환경에서는 `False`로 설정

### 벡터 데이터베이스 설정

- Pinecone 인덱스는 768차원 임베딩 사용
- 코사인 유사도 메트릭
- AWS us-east-1 리전의 서버리스 스펙

### 문서 처리 파이프라인

1. PDF 파일을 `insurance_app/documents/[회사명]/`에 저장
2. `pdf_processor.py`로 텍스트 및 메타데이터 추출
3. SentenceTransformers로 임베딩 생성
4. `upload_all_to_pinecone.py`로 Pinecone에 업로드

## 개발 시 주의사항

### 벡터 검색 최적화

- 중복 결과 제거를 위한 튜플 기반 필터링 구현
- 퍼지 매칭을 통한 노이즈 제거
- 질문 의도 분석으로 약관형/일반형 구분

### 보안 고려사항

- 환경 변수를 통한 API 키 관리
- 사용자별 데이터 접근 제어
- 개인정보 마스킹 기능 (주민등록번호 등)

### 성능 최적화

- 벡터 검색 결과 캐싱
- 데이터베이스 쿼리 최적화
- 정적 파일 압축 및 CDN 활용

## 개발 환경 권장사항

- Python 3.8 이상 (권장: 3.10+)
- 가상환경 사용 필수
- IDE: PyCharm, VSCode 등
- 데이터베이스 관리: DB Browser for SQLite (개발용)
- API 테스트: Postman, Thunder Client
