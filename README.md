# 🏥 AI 보험 추천 플랫폼

## 📋 프로젝트 개요

AI 기술을 활용한 종합 보험 플랫폼으로, 사용자에게 맞춤형 보험 상품을 추천하고 보험 관련 정보를 제공하는 웹 서비스입니다.

## ✨ 주요 기능

### 🤖 AI 보험 추천 시스템

- **RAG(Retrieval-Augmented Generation)** 기반 맞춤형 보험 상품 추천
- **Pinecone 벡터 데이터베이스**를 활용한 의미 기반 검색
- 사용자 프로필(나이, 성별, 운전면허 보유 여부 등)을 고려한 개인화된 추천

### 📚 보험 용어 사전

- 보험 관련 전문 용어의 체계적인 정리 및 검색 기능
- 카테고리별 분류 (보장, 면책, 금액, 절차 등)
- 초보자도 이해하기 쉬운 설명 제공

### 🚗 사고 관리 시스템

- 디지털 교통사고 신고서 작성 및 관리
- 사고 협의서 처리 및 PDF 다운로드
- 사용자별 사고 이력 관리

### 💬 AI 챗봇 상담

- 자연어 처리를 통한 실시간 보험 상담
- 보험 약관 검색 및 해석
- 맞춤형 답변 제공

## 🛠 기술 스택

### Backend

- **Django 5.2.4** - 메인 웹 프레임워크
- **Python 3.10+** - 주 개발 언어
- **SQLite/PostgreSQL** - 데이터베이스

### AI/ML

- **OpenAI GPT-4o-mini** - 자연어 처리 및 대화형 추천 엔진
- **Pinecone** - RAG 검색용 벡터 데이터베이스
- **SentenceTransformers** - 텍스트 임베딩 생성
- **HuggingFace Transformers** - 사전 훈련된 모델

### Frontend

- **HTML5/CSS3** - 반응형 웹 디자인
- **JavaScript (ES6+)** - 동적 UI 구현
- **통합 디자인 시스템** - 일관된 사용자 경험

## 🚀 빠른 시작

### 1. 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd insurance-platform

# 가상환경 생성 및 활성화
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가하세요:

```bash
# Django 설정
DEBUG=True
SECRET_KEY=your-secret-key-here

# AI 서비스 API 키
OPENAI_API_KEY=your-openai-key-here
PINECONE_API_KEY=your-pinecone-key-here
HF_TOKEN=your-huggingface-token-here

# 개발 모드 설정
USE_MOCK_API=True
```

### 3. 데이터베이스 설정

```bash
# 마이그레이션 적용
python manage.py migrate

# 용어사전 데이터 로드
python manage.py load_glossary

# 슈퍼유저 생성 (선택사항)
python manage.py createsuperuser
```

### 4. 개발 서버 실행

```bash
python manage.py runserver
```

브라우저에서 `http://localhost:8000`으로 접속하세요.

## 📱 주요 페이지

### 🏠 홈페이지 (`/`)

- 전체 서비스 개요 및 주요 기능 접근
- 사용자 인증 (로그인/회원가입)

### 🔍 AI 약관 검색 (`/insurance-recommendation/`)

- 자연어 질문을 통한 보험 약관 검색
- RAG 기반 정확한 답변 제공
- 참조 문서 및 페이지 정보 표시

### 📊 보험 추천 (`/recommend/`)

- 사용자 정보 기반 맞춤형 보험 상품 추천
- 보험료, 보장 내용 비교
- PDF 다운로드 기능

### 📘 용어 사전 (`/glossary/`)

- 보험 용어 검색 및 카테고리별 탐색
- 쉬운 설명과 상세 설명 제공

### ✍️ 협의서 작성 (`/accident/agreement/new/`)

- 교통사고 협의서 디지털 작성
- 차량 손상 부위 시각적 표시
- PDF 출력 및 저장 기능

## 🎯 데모 시나리오

### AI 챗봇 테스트 질문 예시

```
"음주운전 사고 시 보상이 되나요?"
"자차보험과 종합보험의 차이점은?"
"보험료를 줄일 수 있는 방법이 있나요?"
"사고 시 보험금 청구 절차는?"
```

### 보험 추천 테스트 시나리오

1. 사용자 정보 입력 (나이: 30세, 성별: 남성, 운전경력: 5년)
2. 지역: 서울, 연간주행거리: 12,000km
3. 차종: 준중형, 보장수준: 표준
4. AI 추천 결과 확인 및 PDF 다운로드

## 📊 프로젝트 구조

```
├── insurance_app/          # 메인 보험 애플리케이션
│   ├── models.py          # 사용자, 보험상품, 용어사전 모델
│   ├── views.py           # 메인 뷰 및 API 엔드포인트
│   ├── templates/         # HTML 템플릿
│   ├── static/           # CSS, JS, 이미지 파일
│   └── documents/        # 보험사별 PDF 약관 문서
├── accident_project/       # 사고 관리 시스템
│   ├── models.py          # 사고 협의서 모델
│   ├── views.py           # 사고 관련 뷰
│   └── templates/         # 사고 관련 템플릿
├── insurance_project/      # Django 프로젝트 설정
└── requirements.txt        # Python 의존성
```

## 🔧 개발 도구

### 관리자 명령어

```bash
# 용어사전 데이터 로드
python manage.py load_glossary

# Pinecone에 문서 업로드
python manage.py shell
>>> from insurance_app.upload_all_to_pinecone import main
>>> main()

# 개발 서버 실행
python manage.py runserver
```

### API 엔드포인트

- `POST /insurance-recommendation/` - AI 챗봇 질의응답
- `POST /recommend/` - 보험 상품 추천
- `GET /api/glossary/` - 용어사전 검색
- `POST /accident/agreement/submit/` - 협의서 제출

## 🎨 디자인 시스템

프로젝트는 통합 디자인 시스템을 사용합니다:

- **색상 팔레트**: 일관된 브랜드 색상
- **타이포그래피**: 시스템 폰트 기반
- **컴포넌트**: 재사용 가능한 UI 요소
- **반응형**: 모바일 친화적 디자인

자세한 내용은 `DESIGN_SYSTEM.md`를 참조하세요.

## 🚀 배포

### 운영 환경 설정

1. `DEBUG=False` 설정
2. PostgreSQL 데이터베이스 연결
3. 정적 파일 수집: `python manage.py collectstatic`
4. 환경 변수 보안 설정

### Docker 배포 (선택사항)

```bash
# Docker 이미지 빌드
docker build -t insurance-platform .

# 컨테이너 실행
docker run -p 8000:8000 insurance-platform
```

## 🤝 기여하기

1. 이슈 생성 또는 기존 이슈 확인
2. 기능 브랜치 생성: `git checkout -b feature/새기능`
3. 변경사항 커밋: `git commit -m "새기능 추가"`
4. 브랜치 푸시: `git push origin feature/새기능`
5. Pull Request 생성

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 📞 문의

프로젝트 관련 문의사항이 있으시면 이슈를 생성해 주세요.

---

**🎯 발표 포인트**

- AI 기술을 활용한 혁신적인 보험 서비스
- 사용자 친화적인 인터페이스와 직관적인 UX
- 실제 보험 업무에 활용 가능한 실용적 기능
- 확장 가능한 아키텍처와 모듈화된 설계
