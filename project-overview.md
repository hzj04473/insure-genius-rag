# AI 보험 플랫폼 프로젝트 개요

## 프로젝트 소개

AI 기술을 활용한 종합 보험 플랫폼으로, 복잡한 보험 상품을 일반 사용자가 쉽게 이해하고 선택할 수 있도록 돕는 웹 애플리케이션입니다.

## 주요 기능

### 🤖 AI 보험 추천 시스템

- **RAG(Retrieval-Augmented Generation)** 기반 맞춤형 보험 상품 추천
- **Pinecone 벡터 데이터베이스**를 활용한 의미 기반 검색
- 사용자 프로필을 고려한 개인화된 추천
- 보험료, 보장 내용, 특약 조건 종합 분석

### 📚 보험 용어 사전

- 보험 관련 전문 용어의 체계적인 정리 및 검색
- 카테고리별 분류 (보장, 면책, 금액, 절차 등)
- 동의어 및 관련 용어 연결
- 초보자를 위한 쉬운 설명 제공

### 🚗 사고 관리 시스템

- 디지털 교통사고 신고서 작성 및 관리
- 시각적 차량 다이어그램을 통한 피해 부위 표시
- PDF/이미지 형태의 협의서 출력
- 개인정보 마스킹 기능

### 📖 보험 지식 포털

- 과실 비율 판정 가이드라인
- 챗봇을 통한 실시간 보험 상담
- RAG 기반 약관 검색 및 질의응답

### 👤 사용자 관리

- 보험 특화 사용자 프로필 관리
- 개인별 보험 추천 이력 저장
- 마이페이지를 통한 종합적인 정보 관리

## 기술 스택

### 백엔드

- **Django 5.2.4** - 메인 웹 프레임워크
- **Python 3.x** - 주 개발 언어
- **SQLite/PostgreSQL** - 데이터베이스
- **Django REST Framework** - API 개발

### AI/ML 스택

- **OpenAI GPT** - 자연어 처리 및 대화형 추천
- **Pinecone** - RAG 검색용 벡터 데이터베이스
- **HuggingFace Transformers** - 사전 훈련된 모델
- **Sentence Transformers** - 텍스트 임베딩 생성

### 문서 처리

- **PyMuPDF, PyPDF2, pdfplumber** - PDF 파싱
- **pytesseract** - OCR 기능
- **Pillow** - 이미지 처리

## 프로젝트 구조

```
├── insurance_project/          # Django 프로젝트 설정
├── insurance_app/              # 메인 보험 애플리케이션
├── accident_project/           # 사고 관리 애플리케이션
├── 0826-5/                     # 아카이브 폴더
│   └── insurance_portal/       # 지식 베이스
├── .kiro/                      # Kiro 설정 및 스펙
│   ├── steering/              # 개발 가이드라인
│   └── specs/                 # 기능 명세서
├── requirements.txt            # Python 의존성
└── manage.py                  # Django 관리 스크립트
```

## 현재 구현 상태

### ✅ 완료된 기능

1. **사용자 인증 시스템**

   - CustomUser 모델 (생년월일, 성별, 운전면허 보유 여부)
   - 회원가입/로그인/프로필 관리
   - 세션 기반 인증

2. **보험 추천 시스템**

   - InsuranceQuote 모델
   - 사용자 프로필 기반 추천 로직
   - 보험료 계산 및 점수화

3. **RAG 기반 질의응답**

   - Pinecone 벡터 검색 연동
   - 질문 의도 분석 (약관형 vs 일반형)
   - 검색 결과 중복 제거 및 정제
   - 자연어 답변 생성

4. **문서 처리 시스템**

   - PDF 텍스트 추출 (다중 라이브러리 지원)
   - OCR 기능
   - 벡터 임베딩 및 Pinecone 업로드

5. **보험 용어 사전**

   - GlossaryTerm 모델
   - 검색 및 필터링 기능
   - 카테고리별 분류

6. **교통사고 관리**
   - Agreement 모델
   - 협의서 작성 폼
   - 시각적 차량 다이어그램
   - PDF/이미지 출력
   - 개인정보 마스킹

### 🔄 진행 중인 작업

- 성능 최적화 및 캐싱
- 테스트 코드 작성
- API 문서화

### 📋 향후 계획

- 마이크로서비스 아키텍처 전환
- 클라우드 네이티브 배포
- 모바일 앱 개발
- 실시간 알림 시스템

## 개발 환경 설정

### 필수 요구사항

- Python 3.8 이상
- 가상환경 (.venv)
- 환경 변수 설정 (.env)

### 설치 및 실행

```bash
# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 초기화
python manage.py migrate
python manage.py createsuperuser

# 개발 서버 실행
python manage.py runserver
```

### 환경 변수 설정

```bash
# AI 서비스 API 키
OPENAI_API_KEY=your_openai_key
HF_TOKEN=your_huggingface_token
PINECONE_API_KEY=your_pinecone_key

# 벡터 데이터베이스 설정
PINECONE_REGION=us-east-1
PINECONE_INDEX_NAME=insurance-rag

# 모델 설정
LLM_MODEL=gpt-4
EMBED_MODEL=intfloat/multilingual-e5-large
```

## 기여 가이드

### 개발 원칙

- 모듈화된 아키텍처 유지
- 테스트 주도 개발 (TDD)
- 보안 우선 설계
- 성능 최적화 고려

### 코드 스타일

- Django 모범 사례 준수
- PEP 8 스타일 가이드 따르기
- 한국어 주석 및 문서화
- 의미 있는 변수명 사용

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 연락처

프로젝트 관련 문의사항이 있으시면 이슈를 등록해 주세요.
