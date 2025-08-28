# API 문서

## 개요

AI 보험 플랫폼의 REST API 엔드포인트 문서입니다. 모든 API는 JSON 형태로 데이터를 주고받으며, 인증이 필요한 엔드포인트는 Django 세션 인증을 사용합니다.

## 기본 정보

- **Base URL**: `http://localhost:8000`
- **인증 방식**: Django Session Authentication
- **Content-Type**: `application/json`
- **문자 인코딩**: UTF-8

## 인증 API

### 회원가입

```http
POST /signup/
Content-Type: application/x-www-form-urlencoded

username=testuser&email=test@example.com&password1=testpass123&password2=testpass123&birth_date=1990-01-01&gender=M&has_license=true
```

**응답:**

```http
HTTP/1.1 302 Found
Location: /login/
```

### 로그인

```http
POST /login/
Content-Type: application/x-www-form-urlencoded

username=testuser&password=testpass123
```

**응답:**

```http
HTTP/1.1 302 Found
Location: /
Set-Cookie: sessionid=abc123...
```

### 로그아웃

```http
POST /logout/
X-CSRFToken: [csrf_token]
```

**응답:**

```http
HTTP/1.1 302 Found
Location: /login/
```

## 보험 추천 API

### 보험 추천 요청

```http
POST /recommend/
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=abc123...

region=서울&driving_experience=5&accident_history=0&annual_mileage=12000&car_type=준중형&coverage_level=표준
```

**응답:**

```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "insurer": "삼성화재",
        "premium": 850000,
        "coverage": "대인배상II 무한, 대물배상 2억원, 자기신체사고 1억원",
        "special_terms": "무사고할인 20%, 마일리지할인 10%",
        "score": 8.5
      }
    ],
    "user_profile": {
      "age": 33,
      "gender": "M",
      "has_license": true,
      "region": "서울"
    }
  }
}
```

## RAG 질의응답 API

### 보험 상담 질문

```http
POST /insurance-recommendation/
Content-Type: application/json
Cookie: sessionid=abc123...

{
  "query": "음주운전 사고 시 보상이 되나요?",
  "company": "삼성화재",
  "answer_mode": "normal",
  "top_k": 10
}
```

**응답:**

```json
{
  "success": true,
  "answer": "결론: 음주·약물 또는 무면허 운전 중 발생한 사고는 약관상 보상 제외(면책) 또는 제한 보상에 해당하는 경우가 많습니다. 다만 의무보험이나 일부 특별약관으로 최소한의 보상이 이뤄질 수 있으며, 사고부담금/자기부담금이 부과될 수 있습니다.",
  "references": [
    {
      "uid": "samsung_001_p15_chunk3",
      "company": "삼성화재",
      "file": "삼성화재.pdf",
      "page": 15,
      "score": 0.89
    }
  ],
  "results": [
    {
      "company": "삼성화재",
      "file": "삼성화재.pdf",
      "page": 15,
      "title": "면책사항",
      "chunk": "음주운전, 무면허운전 또는 약물복용 상태에서의 운전 중 발생한 사고는 보상하지 않습니다.",
      "chunk_idx": 3
    }
  ],
  "total_results": 8,
  "used_model": "intfloat/multilingual-e5-large"
}
```

### 일반 질문 (LLM 직접 응답)

```http
POST /insurance-recommendation/
Content-Type: application/json

{
  "query": "보험이란 무엇인가요?",
  "force_mode": "general"
}
```

**응답:**

```json
{
  "success": true,
  "answer": "보험은 예상치 못한 위험이나 손실에 대비하여 여러 사람이 보험료를 내어 공동으로 대비하는 제도입니다. 사고나 질병 등이 발생했을 때 보험금을 지급받아 경제적 손실을 보상받을 수 있습니다.",
  "references": [],
  "results": [],
  "total_results": 0,
  "used_model": "project-llm"
}
```

## 용어 사전 API

### 용어 검색

```http
GET /api/glossary?q=면책&cat=면책
```

**응답:**

```json
{
  "success": true,
  "terms": [
    {
      "slug": "myeoncheak",
      "term": "면책",
      "short_def": "보험회사가 보험금을 지급하지 않는 경우",
      "long_def": "보험계약에서 정한 특정 사유가 발생했을 때 보험회사가 보험금 지급 의무를 지지 않는 것을 말합니다. 예를 들어 고의사고, 음주운전, 전쟁 등이 면책사유에 해당합니다.",
      "category": "면책",
      "aliases": ["면책사항", "면책조항"],
      "related": ["myeoncheak-geumek", "jadamgeumek"]
    }
  ],
  "total": 1
}
```

### 용어 상세 조회

```http
GET /glossary/
```

**응답**: HTML 페이지 (용어 사전 웹 인터페이스)

## 교통사고 관리 API

### 협의서 작성

```http
POST /accident/agreements/submit/
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=abc123...

accident_date=2024-08-28T14:30&location=서울시 강남구 테헤란로&a_name=홍길동&a_plate=12가3456&b_name=김철수&b_plate=78나9012&accident_description=신호대기 중 후미추돌 사고
```

**응답:**

```http
HTTP/1.1 302 Found
Location: /accident/agreements/123/?mask_rrn=false&format=pdf
```

### 협의서 조회

```http
GET /accident/agreements/123/
Cookie: sessionid=abc123...
```

**응답**: HTML 페이지 (협의서 출력 화면)

### 협의서 PDF 다운로드

```http
GET /accident/agreements/123/pdf/
Cookie: sessionid=abc123...
```

**응답:**

```http
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Disposition: attachment; filename="agreement_123.pdf"

[PDF 바이너리 데이터]
```

### 사용자 협의서 목록

```http
GET /accident/mypage/agreements/?page=1
Cookie: sessionid=abc123...
```

**응답**: HTML 페이지 (협의서 목록)

### 협의서 수정

```http
POST /accident/agreements/123/update/
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=abc123...
X-CSRFToken: [csrf_token]

accident_date=2024-08-28T14:30&location=서울시 강남구 테헤란로 수정&a_name=홍길동&...
```

**응답:**

```http
HTTP/1.1 302 Found
Location: /accident/mypage/agreements/
```

### 협의서 삭제

```http
POST /accident/agreements/123/delete/
Cookie: sessionid=abc123...
X-CSRFToken: [csrf_token]
```

**응답:**

```http
HTTP/1.1 302 Found
Location: /accident/mypage/agreements/
```

## 오류 응답

### 인증 오류

```json
{
  "success": false,
  "error": "로그인이 필요합니다.",
  "error_code": "AUTH_REQUIRED"
}
```

### 권한 오류

```json
{
  "success": false,
  "error": "본인 소유 문서만 접근할 수 있습니다.",
  "error_code": "PERMISSION_DENIED"
}
```

### 입력 검증 오류

```json
{
  "success": false,
  "error": "질문을 입력해주세요.",
  "error_code": "VALIDATION_ERROR"
}
```

### 서버 오류

```json
{
  "success": false,
  "error": "검색 실패: Pinecone 연결 오류",
  "error_code": "INTERNAL_ERROR"
}
```

## 상태 코드

- `200 OK`: 성공
- `302 Found`: 리다이렉션 (주로 폼 제출 후)
- `400 Bad Request`: 잘못된 요청
- `401 Unauthorized`: 인증 필요
- `403 Forbidden`: 권한 없음
- `404 Not Found`: 리소스 없음
- `500 Internal Server Error`: 서버 오류

## 요청 제한

- **Rate Limiting**: 현재 미적용 (향후 구현 예정)
- **File Upload**: PDF 파일 최대 50MB
- **Query Length**: 질문 최대 1000자
- **Session Timeout**: 2주

## SDK 및 예제

### JavaScript 예제

```javascript
// 보험 상담 질문
async function askInsuranceQuestion(query) {
  const response = await fetch('/insurance-recommendation/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ query }),
  });

  return await response.json();
}

// CSRF 토큰 가져오기
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
```

### Python 예제

```python
import requests

# 세션 생성 및 로그인
session = requests.Session()
login_data = {
    'username': 'testuser',
    'password': 'testpass123'
}
session.post('http://localhost:8000/login/', data=login_data)

# 보험 상담 질문
question_data = {
    'query': '음주운전 사고 시 보상이 되나요?',
    'answer_mode': 'normal'
}
response = session.post(
    'http://localhost:8000/insurance-recommendation/',
    json=question_data
)
result = response.json()
print(result['answer'])
```

## 변경 이력

### v1.0.0 (2024-08-28)

- 초기 API 버전 릴리스
- 기본 인증 및 보험 추천 기능
- RAG 기반 질의응답 시스템
- 교통사고 관리 기능

### 향후 계획

- OpenAPI 3.0 스펙 문서 생성
- API 버전 관리 시스템 도입
- Rate Limiting 구현
- WebSocket 기반 실시간 API 추가
