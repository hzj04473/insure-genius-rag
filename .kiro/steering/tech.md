# 기술 스택 및 개발 환경

## 핵심 프레임워크

- **Django 5.2.4** - 메인 웹 프레임워크
- **Django REST Framework** - REST API 개발
- **Python 3.x** - 주 개발 언어
- **SQLite** - 개발용 기본 데이터베이스
- **PostgreSQL** - 운영 환경 데이터베이스 지원 (psycopg2-binary)

## AI 및 머신러닝 스택

- **OpenAI GPT** - 자연어 처리 및 대화형 추천 엔진
- **Pinecone** - RAG 검색용 벡터 데이터베이스
- **HuggingFace Transformers** - 사전 훈련된 모델 호스팅 및 추론
- **Sentence Transformers** - 텍스트 임베딩 생성
- **PyTorch** - 딥러닝 프레임워크
- **scikit-learn** - 전통적인 머신러닝 알고리즘

## 문서 처리 라이브러리

- **PyMuPDF, PyPDF2, pdfplumber** - PDF 문서 파싱 및 텍스트 추출
- **pdf2image, pytesseract** - OCR 기능 (이미지에서 텍스트 추출)
- **Pillow** - 이미지 처리 및 변환

## 환경 설정 및 배포

- **python-dotenv** - 환경 변수 관리
- **가상환경 (.venv)** - 의존성 격리
- **requirements.txt** - 패키지 의존성 관리

## 주요 개발 명령어

### 초기 설정

```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 초기화
python manage.py migrate
python manage.py createsuperuser
```

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
python manage.py upload_all_to_pinecone

# 과실 판정 지식베이스 재색인
python manage.py reindex_fault_md
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
- `PINECONE_INDEX_NAME` - 벡터 인덱스 이름 (예: insurance-rag)

### 모델 설정

- `LLM_MODEL` - 사용할 언어 모델 (예: gpt-4)
- `EMBED_MODEL` - 임베딩 모델 (예: intfloat/multilingual-e5-large)
- `EMBED_DIM` - 임베딩 차원 수 (예: 1024)

### RAG 시스템 튜닝

- `TERM_GATE_MODE` - 용어 필터링 모드 (auto/and/or/off)
- `RAG_MIN_RATIO` - 최소 유사도 비율 (예: 0.35)
- `RAG_MIN_COUNT` - 최소 검색 결과 수 (예: 5)
- `USE_LLM_REFINE` - LLM 결과 정제 사용 여부 (1/0)

## 개발 환경 권장사항

- Python 3.8 이상
- 가상환경 사용 필수
- IDE: PyCharm, VSCode 등
- 데이터베이스 관리: DB Browser for SQLite (개발용)
- API 테스트: Postman, Thunder Client
