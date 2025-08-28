# 프로젝트 구조 및 아키텍처

## 루트 레벨 구조

```
├── manage.py                    # Django 관리 스크립트
├── requirements.txt             # Python 의존성 패키지 목록
├── .env                        # 환경 변수 (Git에서 제외)
├── db.sqlite3                  # SQLite 데이터베이스 파일
├── insurance_project/          # Django 프로젝트 설정
├── insurance_app/              # 메인 보험 애플리케이션
├── accident_project/           # 사고 관리 애플리케이션
└── 0826-5/                     # 아카이브 폴더 (추가 앱들)
```

## 주요 애플리케이션 구조

### insurance_project/ (Django 프로젝트 설정)

- `settings.py` - AI 서비스 통합을 포함한 메인 설정
- `urls.py` - 루트 URL 라우팅 설정
- `wsgi.py/asgi.py` - WSGI/ASGI 서버 설정

### insurance_app/ (핵심 보험 기능)

```
├── models.py                   # CustomUser, InsuranceQuote, GlossaryTerm 모델
├── views.py                    # 메인 뷰 및 API 엔드포인트
├── urls.py                     # 앱 URL 패턴
├── forms.py                    # Django 폼 정의
├── documents/                  # 보험사별 PDF 문서 저장소
│   ├── 삼성화재/               # 삼성화재 보험 약관
│   ├── 현대해상/               # 현대해상 보험 약관
│   └── DB손해보험/             # DB손해보험 약관
├── static/insurance_app/       # CSS, JS 정적 파일
│   ├── css/                   # 스타일시트
│   ├── js/                    # JavaScript 파일
│   └── img/                   # 이미지 파일
├── templates/insurance_app/    # HTML 템플릿
│   ├── base.html              # 기본 템플릿
│   ├── home.html              # 홈페이지
│   ├── recommend.html         # 보험 추천 페이지
│   └── glossary.html          # 용어 사전 페이지
├── management/commands/        # 커스텀 Django 명령어
│   ├── load_glossary.py       # 용어 사전 데이터 로드
│   └── upload_all_to_pinecone.py  # Pinecone 업로드
├── migrations/                 # 데이터베이스 마이그레이션
└── utils/                      # 유틸리티 모듈
    ├── ai_service.py          # AI 서비스 연동
    ├── pdf_processor.py       # PDF 처리 유틸
    └── vector_search.py       # 벡터 검색 기능
```

### accident_project/ (사고 관리)

```
├── models.py                   # Agreement 모델 (사고 협의서)
├── views.py                    # 사고 관련 뷰
├── forms.py                    # 사고 신고서 폼
├── templates/accident_project/ # 사고 관련 템플릿
└── static/accident_project/    # 사고 관련 정적 파일
```

### insurance_portal/ (지식 베이스)

**위치**: `0826-5/insurance_portal/` (아카이브 폴더)

```
├── templates/                  # 포털 템플릿
│   └── partials/              # 재사용 가능한 템플릿 조각
├── static/                     # 포털 정적 파일
├── fault_md/                   # 과실 판정 마크다운 파일
├── weekly_articles/            # 주간 보험 뉴스
└── chatbot/                    # 챗봇 관련 파일
```

## 핵심 개발 규칙

### 모델 설계 원칙

- **CustomUser**를 AUTH_USER_MODEL로 사용
- 외래키는 `settings.AUTH_USER_MODEL` 참조
- 유연한 데이터 저장을 위한 JSONField 활용
- 관리자 인터페이스용 한국어 verbose_name 설정
- 생성/수정 시간 자동 추가 (auto_now_add, auto_now)

### 템플릿 구조

- 앱별 템플릿 디렉토리 분리
- 프로젝트 루트의 공유 템플릿
- `partials/` 서브디렉토리의 재사용 템플릿 조각
- 기본 템플릿 상속 구조 (base.html → 개별 페이지)

### 정적 파일 관리

- 앱별 static 디렉토리 분리
- `css/` 서브디렉토리의 스타일시트
- `js/` 서브디렉토리의 JavaScript 파일
- `img/` 서브디렉토리의 이미지 파일
- 개발 환경에서 자동 서빙, 운영 환경에서 collectstatic 사용

### URL 패턴 설계

- 네임스페이스 인식 URL 라우팅
- 직접 연결과 네임스페이스 연결 병행 지원
- API 엔드포인트는 `api/` 접두사 사용
- RESTful URL 구조 준수

### 파일 조직 원칙

- PDF 문서는 보험사별로 분류 저장
- 데이터 조작용 management commands 활용
- 재사용 가능한 기능은 utils 모듈로 분리
- 비즈니스 로직은 services 디렉토리에 구성

## 아카이브 구조 (0826-5/)

이 폴더는 다음과 같은 추가 구성 요소를 포함합니다:

- **대안 구현체**: 다른 접근 방식으로 구현된 기능들
- **팀원 기여분**: 개별 팀원이 작업한 모듈들
- **실험적 기능**: 테스트 중인 새로운 기능들
- **레거시 코드**: 이전 버전의 코드 보관

## 환경 파일 관리

- `.env` - 메인 환경 변수 (API 키, 데이터베이스 설정 등)
- `.gitignore` - Git 무시 패턴 (환경 변수, 캐시 파일 등)
- `.venv/` - 가상환경 디렉토리

## 데이터베이스 설계

- **개발 환경**: SQLite (db.sqlite3)
- **운영 환경**: PostgreSQL 지원
- **마이그레이션**: Django ORM 기반 스키마 관리
- **인덱싱**: 검색 성능 최적화를 위한 적절한 인덱스 설정

## 보안 고려사항

- 환경 변수를 통한 민감 정보 관리
- CSRF 보호 활성화
- XFrame 옵션 설정
- DEBUG 모드는 개발 환경에서만 활성화

## 성능 최적화

- 정적 파일 압축 및 캐싱
- 데이터베이스 쿼리 최적화
- 벡터 검색 결과 캐싱
- 이미지 최적화 및 지연 로딩
