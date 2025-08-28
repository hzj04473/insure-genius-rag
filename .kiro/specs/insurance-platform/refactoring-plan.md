# AI 보험 플랫폼 리팩토링 계획서

## 개요

현재 AI 보험 플랫폼은 85% 완성도를 달성했으나, 팀원들의 개별 작업물을 통합하는 과정에서 발생한 구조적 문제들과 코드 일관성 문제들을 해결하기 위한 리팩토링이 필요합니다.

## 현재 문제점 분석

### 1. 폴더 구조 문제

**문제 상황:**

```
현재 경로: /Volumes/DATA/mbc_project/rag-insure-bot/0826-5/Volumes/DATA/mbc_project/rag-insure-bot/accident_project
```

- `0826-5/` 아카이브 폴더에 중복된 절대 경로가 포함됨
- 팀원 작업물을 단순 복사하면서 발생한 중복 경로 문제
- `settings.py`에서 복잡한 경로 탐색 로직 필요

**영향:**

- 정적 파일 서빙 오류 가능성
- 템플릿 경로 충돌
- 배포 시 경로 문제 발생 위험

### 2. 코드 일관성 문제

**레거시 파일 중복:**

- `accident_project/views.py` (현재 사용)
- `accident_project/views old.py` (레거시)
- `accident_project/views old_2(0824_01s).py` (레거시)

**폼 검증 복잡성:**

```python
# forms.py의 문제적 코드
if "damages_raw" not in self.fields:
    return self.cleaned_data.get("damages_raw")
```

**데이터 구조 불일치:**

- `damages_raw` 필드가 TextField와 JSONField 사이에서 혼재
- 런타임 필드 존재 여부 체크로 인한 불안정성

### 3. 프론트엔드 일관성 문제

**디자인 시스템 분산:**

- `insurance_app`: Bootstrap 기반 기본 스타일
- `accident_project`: 커스텀 스타일
- `insurance_portal`: 독립적인 디자인 시스템

**JavaScript 모듈 중복:**

- `chatbot.js`: 챗봇 기본 기능
- `fault_answer.js`: 과실비율 답변 렌더링
- `fab-controller.js`: 플로팅 액션 버튼 관리
- `navigation_handler.js`: 네비게이션 상태 관리

**중복 기능 예시:**

```javascript
// chatbot.js
function renderFaultResult(result) { ... }

// fault_answer.js
class FaultAnswerRenderer {
    render(data) { ... }
}
```

## 리팩토링 우선순위 및 작업 계획

### Phase 1: 구조 정리 (최우선 - 1주)

#### 1.1 폴더 구조 정리

**작업 내용:**

```bash
# 현재 문제 경로 정리
rm -rf 0826-5/Volumes/
# 필요한 파일들만 적절한 위치로 이동
cp -r 0826-5/accident_project/* accident_project/
```

**체크리스트:**

- [ ] 중복 경로 제거
- [ ] 필요한 파일 이동
- [ ] `settings.py` 경로 설정 단순화
- [ ] 정적 파일 경로 검증

#### 1.2 레거시 파일 정리

**제거 대상:**

- `accident_project/views old.py`
- `accident_project/views old_2(0824_01s).py`
- 사용하지 않는 템플릿 파일들
- 중복된 JavaScript/CSS 파일들

**보존 및 통합:**

- 현재 사용 중인 `views.py` 유지
- 필요한 기능은 현재 파일에 통합

### Phase 2: 백엔드 코드 정리 (1-2주)

#### 2.1 모델 일관성 확보

**Agreement 모델 표준화:**

```python
# 개선 전 (문제적 구조)
class Agreement(models.Model):
    damages_raw = models.TextField()  # JSON 문자열로 저장

# 개선 후 (표준화된 구조)
class Agreement(models.Model):
    damages_raw = models.JSONField(default=dict)  # 네이티브 JSON 필드
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

#### 2.2 폼 검증 로직 단순화

**개선 전:**

```python
def clean_damages_raw(self):
    if "damages_raw" not in self.fields:  # 런타임 체크
        return self.cleaned_data.get("damages_raw")
    # 복잡한 타입 변환 로직...
```

**개선 후:**

```python
def clean_damages_raw(self):
    val = self.cleaned_data.get("damages_raw")
    if isinstance(val, str):
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            raise forms.ValidationError("유효한 JSON 형식이 아닙니다.")
    return val or {}
```

#### 2.3 뷰 함수 권한 처리 표준화

**개선 전 (중복 코드):**

```python
def agreement_edit(request, pk):
    ag = get_object_or_404(Agreement, pk=pk)
    if getattr(ag, "owner_id", None) is None:
        ag.owner = request.user
        ag.save(update_fields=["owner"])
    if ag.owner_id != request.user.id:
        return HttpResponseForbidden("본인 소유 문서만 수정할 수 있습니다.")
```

**개선 후 (데코레이터 활용):**

```python
@login_required
@agreement_owner_required
def agreement_edit(request, pk):
    ag = get_object_or_404(Agreement, pk=pk)
    # 권한 확인은 데코레이터에서 처리
```

### Phase 3: 프론트엔드 통합 (2-3주)

#### 3.1 디자인 시스템 통합

**공통 디자인 토큰 정의:**

```css
:root {
  /* 색상 시스템 */
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #dc3545;

  /* 타이포그래피 */
  --font-family-base: 'Noto Sans KR', sans-serif;
  --font-size-base: 1rem;
  --line-height-base: 1.5;

  /* 간격 시스템 */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 3rem;
}
```

#### 3.2 JavaScript 모듈 통합

**통합 전략:**

1. **공통 유틸리티 분리**: `utils.js`
2. **렌더링 로직 통합**: `renderer.js`
3. **상태 관리 통합**: `state-manager.js`

**예시 - 렌더링 로직 통합:**

```javascript
// renderer.js
class UnifiedRenderer {
  renderFaultResult(result) {
    // chatbot.js와 fault_answer.js의 기능 통합
  }

  renderAnswerCards(data) {
    // 공통 카드 렌더링 로직
  }
}
```

#### 3.3 템플릿 구조 표준화

**기본 템플릿 계층:**

```
templates/
├── base.html (최상위 공통 레이아웃)
├── components/
│   ├── navbar.html
│   ├── footer.html
│   └── modal.html
├── insurance_app/
│   └── base_insurance.html (extends base.html)
├── accident_project/
│   └── base_accident.html (extends base.html)
└── insurance_portal/
    └── base_portal.html (extends base.html)
```

### Phase 4: 통합 테스트 및 검증 (1주)

#### 4.1 기능 검증 체크리스트

**핵심 기능:**

- [ ] 사용자 인증 및 프로필 관리
- [ ] 보험 추천 시스템
- [ ] RAG 기반 질의응답
- [ ] 협의서 작성/수정/삭제
- [ ] PDF 다운로드
- [ ] 용어 사전 검색

**통합 기능:**

- [ ] 앱 간 네비게이션
- [ ] 공통 디자인 적용
- [ ] JavaScript 모듈 연동
- [ ] 에러 처리

#### 4.2 성능 및 보안 검증

**성능 체크:**

- [ ] 페이지 로딩 속도
- [ ] 벡터 검색 응답 시간
- [ ] 파일 다운로드 속도

**보안 체크:**

- [ ] 권한 기반 접근 제어
- [ ] CSRF 보호
- [ ] 개인정보 마스킹

## 구체적 작업 가이드

### 1. 폴더 구조 정리 스크립트

```bash
#!/bin/bash
# cleanup_structure.sh

echo "🚀 폴더 구조 정리 시작..."

# 1. 백업 생성
cp -r 0826-5 0826-5_backup_$(date +%Y%m%d_%H%M%S)

# 2. 중복 경로 확인 및 정리
if [ -d "0826-5/Volumes" ]; then
    echo "❌ 중복 경로 발견: 0826-5/Volumes"

    # 필요한 파일들만 추출
    if [ -d "0826-5/Volumes/DATA/mbc_project/rag-insure-bot/accident_project" ]; then
        echo "📁 accident_project 파일 이동 중..."
        rsync -av --exclude='*.pyc' --exclude='__pycache__' \
              0826-5/Volumes/DATA/mbc_project/rag-insure-bot/accident_project/ \
              accident_project_temp/
    fi

    # 중복 경로 제거
    rm -rf 0826-5/Volumes

    echo "✅ 중복 경로 정리 완료"
fi

# 3. settings.py 경로 설정 단순화
echo "⚙️  settings.py 업데이트 중..."
# 복잡한 경로 탐색 로직을 단순화

echo "✅ 폴더 구조 정리 완료"
```

### 2. 레거시 파일 정리 스크립트

```bash
#!/bin/bash
# cleanup_legacy.sh

echo "🧹 레거시 파일 정리 시작..."

# 레거시 뷰 파일 제거
LEGACY_FILES=(
    "accident_project/views old.py"
    "accident_project/views old_2(0824_01s).py"
)

for file in "${LEGACY_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "🗑️  제거: $file"
        rm "$file"
    fi
done

echo "✅ 레거시 파일 정리 완료"
```

### 3. 모델 마이그레이션 스크립트

```python
# migration_script.py
from django.core.management.base import BaseCommand
from accident_project.models import Agreement
import json

class Command(BaseCommand):
    help = 'Agreement 모델의 damages_raw 필드를 JSONField로 마이그레이션'

    def handle(self, *args, **options):
        self.stdout.write("🔄 데이터 마이그레이션 시작...")

        agreements = Agreement.objects.all()
        updated_count = 0

        for agreement in agreements:
            if isinstance(agreement.damages_raw, str):
                try:
                    # JSON 문자열을 파싱하여 딕셔너리로 변환
                    parsed_data = json.loads(agreement.damages_raw)
                    agreement.damages_raw = parsed_data
                    agreement.save(update_fields=['damages_raw'])
                    updated_count += 1
                except json.JSONDecodeError:
                    self.stdout.write(
                        self.style.WARNING(f'⚠️  Agreement {agreement.id}: JSON 파싱 실패')
                    )

        self.stdout.write(
            self.style.SUCCESS(f'✅ {updated_count}개 레코드 마이그레이션 완료')
        )
```

## 완료 기준 및 검증 방법

### Phase 1 완료 기준

- [ ] 중복 폴더 구조 완전 제거
- [ ] 모든 정적 파일 정상 로딩
- [ ] 템플릿 경로 오류 없음
- [ ] 개발 서버 정상 실행

### Phase 2 완료 기준

- [ ] 레거시 파일 완전 제거
- [ ] 모델 필드 일관성 확보
- [ ] 폼 검증 로직 단순화
- [ ] 권한 처리 표준화

### Phase 3 완료 기준

- [ ] 통합 디자인 시스템 적용
- [ ] JavaScript 모듈 중복 제거
- [ ] 템플릿 구조 표준화
- [ ] 크로스 브라우저 호환성 확인

### Phase 4 완료 기준

- [ ] 모든 핵심 기능 정상 작동
- [ ] 통합 테스트 100% 통과
- [ ] 성능 기준 달성
- [ ] 보안 검증 완료

## 위험 요소 및 대응 방안

### 데이터 손실 위험

**대응 방안:**

- 모든 작업 전 백업 생성
- 단계별 롤백 계획 수립
- 마이그레이션 스크립트 사전 테스트

### 기능 호환성 문제

**대응 방안:**

- 기존 URL 패턴 유지
- API 엔드포인트 하위 호환성 보장
- 점진적 마이그레이션 적용

### 성능 저하 위험

**대응 방안:**

- 리팩토링 전후 성능 측정
- 병목 지점 사전 식별
- 캐싱 전략 수립

이 리팩토링 계획을 단계별로 진행하면 안정적이고 유지보수가 용이한 코드베이스를 구축할 수 있습니다.
