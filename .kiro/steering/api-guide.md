# API 사용 가이드

## 개요

AI 보험 플랫폼의 REST API 엔드포인트 사용 가이드입니다. 모든 API는 JSON 형태로 데이터를 주고받으며, 인증이 필요한 엔드포인트는 Django 세션 인증을 사용합니다.

## 기본 정보

- **Base URL**: `http://localhost:8000` (개발 환경)
- **인증 방식**: Django Session Authentication
- **Content-Type**: `application/json`
- **문자 인코딩**: UTF-8

## ⚠️ API 테스트 전 필수 확인사항

### 개발환경 준비 완료 확인

```bash
# 1. setup-guide.md 완전히 따라하기 완료 확인
python manage.py check

# 2. 개발 서버 실행 중인지 확인
curl http://localhost:8000/

# 3. 로그인 페이지 접근 확인
curl http://localhost:8000/login/

# 4. 관리자 페이지 접근 확인
curl http://localhost:8000/admin/
```

### 환경 변수 설정 확인

```bash
# .env 파일의 필수 키들이 설정되어 있는지 확인
python manage.py shell
>>> import os
>>> print("OpenAI:", bool(os.getenv('OPENAI_API_KEY')))
>>> print("Pinecone:", bool(os.getenv('PINECONE_API_KEY')))
>>> print("HF Token:", bool(os.getenv('HF_TOKEN')))
```

## 주요 API 엔드포인트

### 보험 추천 API

```http
POST /recommend/
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=abc123...

region=서울&driving_experience=5&accident_history=0&annual_mileage=12000&car_type=준중형&coverage_level=표준
```

**응답 예시:**

```json
{
  "success": true,
  "data": {
    "recommendations": [
      {
        "insurer": "삼성화재",
        "premium": 850000,
        "coverage": "대인배상II 무한, 대물배상 2억원",
        "score": 8.5
      }
    ]
  }
}
```

### RAG 질의응답 API

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

**응답 예시:**

```json
{
  "success": true,
  "answer": "음주·약물 또는 무면허 운전 중 발생한 사고는 약관상 보상 제외에 해당합니다.",
  "references": [
    {
      "company": "삼성화재",
      "file": "삼성화재.pdf",
      "page": 15,
      "score": 0.89
    }
  ]
}
```

### 용어 사전 API

```http
GET /api/glossary?q=면책&cat=면책
```

**응답 예시:**

```json
{
  "success": true,
  "terms": [
    {
      "term": "면책",
      "short_def": "보험회사가 보험금을 지급하지 않는 경우",
      "category": "면책"
    }
  ]
}
```

### 사고 협의서 API

```http
POST /accident/agreement/submit/
Content-Type: application/x-www-form-urlencoded
Cookie: sessionid=abc123...

accident_date=2024-01-15&location=서울시 강남구&a_name=홍길동&b_name=김철수
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

### 입력 검증 오류

```json
{
  "success": false,
  "error": "질문을 입력해주세요.",
  "error_code": "VALIDATION_ERROR"
}
```

### AI 서비스 오류

```json
{
  "success": false,
  "error": "OpenAI API 키가 설정되지 않았습니다.",
  "error_code": "API_KEY_MISSING"
}
```

## 상태 코드

- `200 OK`: 성공
- `400 Bad Request`: 잘못된 요청
- `401 Unauthorized`: 인증 필요
- `403 Forbidden`: 권한 없음
- `500 Internal Server Error`: 서버 오류

## 사용 예제

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
session.post('http://localhost:8000/login/', data={
    'username': 'testuser',
    'password': 'testpass123'
})

# 보험 상담 질문
response = session.post(
    'http://localhost:8000/insurance-recommendation/',
    json={'query': '음주운전 사고 시 보상이 되나요?'}
)
result = response.json()
print(result['answer'])
```

### cURL 예제

```bash
# 로그인
curl -c cookies.txt -d "username=testuser&password=testpass123" \
     -X POST http://localhost:8000/login/

# 보험 상담 질문
curl -b cookies.txt -H "Content-Type: application/json" \
     -d '{"query":"음주운전 사고 시 보상이 되나요?"}' \
     -X POST http://localhost:8000/insurance-recommendation/
```

## API 테스트 도구 추천

### Postman 설정

1. Environment 생성: `Insurance Platform Dev`
2. Variables 설정:
   - `base_url`: `http://localhost:8000`
   - `csrf_token`: `{{csrf_token}}`

### Thunder Client (VS Code)

1. Collection 생성: `Insurance APIs`
2. Environment 설정: `dev.json`

## 개발 시 주의사항

### CSRF 보호

- POST 요청 시 CSRF 토큰 필수
- JavaScript에서는 `X-CSRFToken` 헤더 사용
- Form 데이터에서는 `csrfmiddlewaretoken` 필드 사용

### 세션 관리

- 로그인 후 세션 쿠키 유지 필요
- 개발 환경에서는 `sessionid` 쿠키 사용

### 에러 처리

- 모든 API 응답에서 `success` 필드 확인
- `error_code`를 통한 구체적인 에러 처리
- 네트워크 오류와 서버 오류 구분

이 가이드를 참고하여 API를 효율적으로 테스트하고 통합하세요!
