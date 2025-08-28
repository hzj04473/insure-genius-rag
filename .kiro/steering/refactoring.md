# 프로젝트 리팩토링 및 정리 가이드

## 현재 문제점 분석

### 1. 폴더 구조 문제

- `0826-5/` 아카이브 폴더에 중복된 `accident_project` 경로 존재
- 경로: `/Volumes/DATA/mbc_project/rag-insure-bot/0826-5/Volumes/DATA/mbc_project/rag-insure-bot/accident_project`
- 이는 팀원 작업물을 단순 복사하면서 발생한 중복 경로 문제

### 2. 코드 일관성 문제

- `views.py`, `views old.py`, `views old_2(0824_01s).py` 등 여러 버전 파일 공존
- `forms.py`에서 동적 필드 처리 방식의 복잡성
- 모델 필드 존재 여부를 런타임에 체크하는 불안정한 구조

### 3. 프론트엔드 일관성 문제

- 각 앱별로 다른 디자인 시스템 사용
- JavaScript 파일들의 중복 기능 (`chatbot.js`, `fault_answer.js` 등)
- CSS 스타일의 불일치

## 🚨 리팩토링 시작 전 필수 준비사항

### 개발환경 100% 완료 확인

- [ ] **setup-guide.md 완전히 따라하기 완료**
- [ ] 가상환경 활성화 및 의존성 설치 완료
- [ ] .env 파일 설정 및 API 키 확인
- [ ] `python manage.py runserver` 정상 실행 확인
- [ ] 모든 핵심 기능 정상 작동 확인

### 백업 생성 (필수)

```bash
# 전체 프로젝트 백업
cp -r . ../insurance-platform-backup-$(date +%Y%m%d_%H%M%S)

# 데이터베이스 백업
cp db.sqlite3 db.sqlite3.backup

# Git 커밋 (현재 상태 저장)
git add .
git commit -m "리팩토링 시작 전 백업"
```

## 작업 순서 및 우선순위

### Phase 1: 구조 정리 (최우선)

#### 1.1 폴더 구조 정리

```bash
# 현재 문제가 되는 중복 경로 정리
# 0826-5/ 폴더 내부의 잘못된 경로 구조 수정
```

**작업 내용:**

- `0826-5/` 내부의 중복 경로 제거
- 필요한 파일들만 적절한 위치로 이동
- `settings.py`의 경로 설정 업데이트

#### 1.2 레거시 파일 정리

**제거 대상:**

- `views old.py`
- `views old_2(0824_01s).py`
- 사용하지 않는 템플릿 파일들
- 중복된 JavaScript/CSS 파일들

**보존 대상:**

- 현재 사용 중인 `views.py`
- 활성 템플릿 파일들
- 필수 정적 파일들

### Phase 2: 백엔드 코드 정리

#### 2.1 모델 일관성 확보

**`accident_project/models.py` 정리:**

- Agreement 모델의 필드 정의 명확화
- `damages_raw` 필드 처리 방식 표준화
- `owner` 필드 관계 정리

#### 2.2 뷰 함수 정리

**현재 문제점:**

```python
# forms.py에서 런타임 필드 체크
if "damages_raw" not in self.fields:
    return self.cleaned_data.get("damages_raw")
```

**개선 방향:**

- 모델 필드를 명확히 정의
- 동적 필드 체크 로직 제거
- 일관된 데이터 검증 로직 적용

#### 2.3 URL 패턴 정리

**현재 상태:**

```python
# insurance_project/urls.py에서 중복 라우팅
path("", app_views.home, name="home"),
path("", include(("insurance_app.urls", "insurance_app"), namespace="insurance_app")),
```

**개선 필요:**

- 중복 라우팅 제거
- 네임스페이스 일관성 확보

### Phase 3: 프론트엔드 통합

#### 3.1 디자인 시스템 통합

**현재 문제:**

- `insurance_app`: 기본 Bootstrap 스타일
- `accident_project`: 커스텀 스타일
- `insurance_portal`: 별도 디자인 시스템

**통합 방향:**

1. 공통 디자인 토큰 정의
2. 컴포넌트 라이브러리 구축
3. 일관된 색상/타이포그래피 적용

#### 3.2 JavaScript 모듈 정리

**중복 기능 통합:**

- `chatbot.js`와 `fault_answer.js`의 렌더링 로직
- `fab-controller.js`의 모달 관리 기능
- 공통 유틸리티 함수들

#### 3.3 템플릿 구조 표준화

**기본 템플릿 계층:**

```
base.html (공통 레이아웃)
├── insurance_app/base.html
├── accident_project/base.html
└── insurance_portal/base.html
```

### Phase 4: 기능 검증 및 테스트

#### 4.1 핵심 기능 테스트

- 보험 추천 시스템
- 사고 협의서 작성/저장
- PDF 다운로드 기능
- 챗봇 상담 기능

#### 4.2 통합 테스트

- 앱 간 데이터 연동
- 사용자 인증 흐름
- 파일 업로드/다운로드

## 구체적 작업 가이드

### 1. 폴더 구조 정리 스크립트

```bash
# 중복 경로 정리
find 0826-5/ -name "accident_project" -type d
# 필요한 파일만 추출하여 올바른 위치로 이동
```

### 2. 모델 정리 우선순위

```python
# accident_project/models.py
class Agreement(models.Model):
    # 필수 필드들을 명확히 정의
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    accident_date = models.DateField()
    damages_raw = models.JSONField(default=dict)  # TextField에서 JSONField로 변경
    # ... 기타 필드들
```

### 3. 프론트엔드 통합 순서

1. **공통 CSS 변수 정의**
2. **컴포넌트별 스타일 모듈화**
3. **JavaScript 모듈 통합**
4. **템플릿 상속 구조 정리**

## 주의사항

### 데이터 마이그레이션

- 기존 데이터 백업 필수
- 단계별 마이그레이션 스크립트 작성
- 롤백 계획 수립

### 기능 호환성

- 기존 URL 패턴 유지 (리다이렉트 처리)
- API 엔드포인트 하위 호환성 보장
- 사용자 세션 데이터 보존

### 성능 고려사항

- 정적 파일 최적화
- 데이터베이스 쿼리 최적화
- 캐싱 전략 수립

## 완료 기준

### Phase 1 완료 기준

- [ ] 중복 폴더 구조 제거
- [ ] 레거시 파일 정리
- [ ] 경로 설정 정상화

### Phase 2 완료 기준

- [ ] 모델 필드 일관성 확보
- [ ] 뷰 함수 정리 완료
- [ ] URL 패턴 정리

### Phase 3 완료 기준

- [ ] 통합 디자인 시스템 적용
- [ ] JavaScript 모듈 정리
- [ ] 템플릿 구조 표준화

### Phase 4 완료 기준

- [ ] 모든 핵심 기능 정상 작동
- [ ] 통합 테스트 통과
- [ ] 성능 최적화 완료

이 가이드를 따라 단계별로 진행하면 안정적이고 일관된 프로젝트 구조를 구축할 수 있습니다.
