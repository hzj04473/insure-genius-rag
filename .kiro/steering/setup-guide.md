# 개발환경 완벽 설정 가이드

## 시스템 요구사항

### 최소 요구사항

- **OS**: macOS 10.15+, Ubuntu 18.04+, Windows 10+
- **Python**: 3.8 이상 (권장: 3.10+)
- **메모리**: 8GB RAM (AI 모델 로딩용)
- **디스크**: 20GB 여유 공간
- **인터넷**: 안정적인 연결 (AI API 호출용)

### 필수 시스템 패키지

#### macOS

```bash
# Homebrew 설치 (없는 경우)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 필수 패키지 설치
brew install python@3.10
brew install tesseract tesseract-lang-korean
brew install poppler
brew install git
```

#### Ubuntu/Debian

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# Python 및 필수 패키지 설치
sudo apt install -y python3.10 python3.10-venv python3-pip
sudo apt install -y tesseract-ocr tesseract-ocr-kor
sudo apt install -y poppler-utils
sudo apt install -y git curl wget
sudo apt install -y build-essential libpq-dev
```

#### Windows

```powershell
# Chocolatey 설치 (관리자 권한 PowerShell)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 필수 패키지 설치
choco install python310 -y
choco install tesseract -y
choco install git -y
```

## 프로젝트 설정 단계별 가이드

### 1단계: 저장소 클론 및 디렉토리 이동

```bash
# 저장소 클론 (실제 URL로 변경)
git clone <repository-url> insurance-platform
cd insurance-platform

# 현재 디렉토리 확인
pwd
ls -la
```

### 2단계: Python 가상환경 설정

```bash
# Python 버전 확인
python3 --version  # 3.8 이상이어야 함

# 가상환경 생성
python3 -m venv .venv

# 가상환경 활성화
# macOS/Linux:
source .venv/bin/activate

# Windows:
# .venv\Scripts\activate

# 가상환경 활성화 확인
which python  # .venv/bin/python이 나와야 함
python --version
```

### 3단계: Python 패키지 설치

```bash
# pip 최신 버전으로 업그레이드
pip install --upgrade pip

# 의존성 설치 (시간이 오래 걸릴 수 있음)
pip install -r requirements.txt

# 설치 확인
pip list | grep -E "(Django|openai|pinecone|torch)"
```

### 4단계: 환경 변수 설정

```bash
# .env 파일 생성 (없는 경우)
touch .env

# .env 파일 편집
# 다음 내용을 .env 파일에 추가:
```

**.env 파일 필수 내용:**

```bash
# Django 설정
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# AI 서비스 API 키 (실제 키로 교체 필요)
OPENAI_API_KEY=sk-proj-your-openai-key-here
HF_TOKEN=hf_your-huggingface-token-here
LANGCHAIN_API_KEY=lsv2_pt_your-langchain-key-here
UPSTAGE_API_KEY=your-upstage-key-here

# Pinecone 설정
PINECONE_API_KEY=your-pinecone-key-here
PINECONE_REGION=us-east-1
PINECONE_INDEX_NAME=insurance-rag

# RAG 시스템 설정
TERM_GATE_MODE=auto
STRICT_FILL_MIN=3
LLM_MODEL=gpt-4o-mini
EMBED_MODEL=intfloat/multilingual-e5-large
EMBED_DIM=1024
RAG_MIN_RATIO=0.35
RAG_MIN_COUNT=5

# LLM 정제 설정
USE_LLM_REFINE=1
LLM_REFINE_MODEL=gpt-4o-mini
ANS_LLM_MODEL=gpt-4o-mini
ANS_MAX_TOKENS=600

# 개발 모드 설정
USE_MOCK_API=True
```

### 5단계: 데이터베이스 설정

```bash
# Django 설정 확인
python manage.py check

# 마이그레이션 파일 생성
python manage.py makemigrations

# 마이그레이션 적용
python manage.py migrate

# 슈퍼유저 생성 (선택사항)
python manage.py createsuperuser
```

### 6단계: 정적 파일 및 미디어 디렉토리 설정

```bash
# 필요한 디렉토리 생성
mkdir -p media
mkdir -p staticfiles
mkdir -p insurance_app/documents

# 정적 파일 수집 (개발 환경에서는 선택사항)
python manage.py collectstatic --noinput
```

### 7단계: 개발 서버 실행 및 테스트

```bash
# 개발 서버 시작
python manage.py runserver

# 다른 터미널에서 테스트
curl http://localhost:8000/
```

## API 키 획득 가이드

### OpenAI API 키

1. https://platform.openai.com/ 접속
2. 계정 생성/로그인
3. API Keys 메뉴에서 새 키 생성
4. 사용량 제한 및 결제 정보 설정

### Pinecone API 키

1. https://www.pinecone.io/ 접속
2. 계정 생성/로그인
3. API Keys 섹션에서 키 생성
4. 무료 플랜으로 시작 가능

### HuggingFace 토큰

1. https://huggingface.co/ 접속
2. 계정 생성/로그인
3. Settings > Access Tokens에서 토큰 생성
4. Read 권한으로 충분

## 개발 도구 설정

### VS Code 확장 프로그램 (권장)

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.black-formatter",
    "ms-python.flake8",
    "bradlc.vscode-tailwindcss",
    "ms-vscode.vscode-json",
    "redhat.vscode-yaml"
  ]
}
```

### PyCharm 설정

1. Python Interpreter를 .venv/bin/python으로 설정
2. Django 지원 활성화
3. Code Style을 PEP 8로 설정

## 문제 해결 가이드

### 일반적인 설치 오류

#### 1. PyTorch 설치 실패

```bash
# CPU 버전으로 설치
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

#### 2. Tesseract 관련 오류

```bash
# macOS
brew reinstall tesseract

# Ubuntu
sudo apt reinstall tesseract-ocr tesseract-ocr-kor

# Windows: 환경 변수에 Tesseract 경로 추가
# C:\Program Files\Tesseract-OCR
```

#### 3. PDF 처리 라이브러리 오류

```bash
# Poppler 재설치
# macOS
brew reinstall poppler

# Ubuntu
sudo apt reinstall poppler-utils
```

#### 4. 메모리 부족 오류

```bash
# 스왑 메모리 증가 (Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Django 관련 오류

#### 1. 마이그레이션 오류

```bash
# 마이그레이션 초기화
python manage.py migrate --fake-initial

# 특정 앱 마이그레이션
python manage.py migrate insurance_app
python manage.py migrate accident_project
```

#### 2. 정적 파일 오류

```bash
# 정적 파일 디렉토리 권한 확인
chmod -R 755 staticfiles/
chmod -R 755 media/
```

## 개발환경 검증 체크리스트

### ✅ 기본 환경

- [ ] Python 3.8+ 설치 확인
- [ ] 가상환경 생성 및 활성화
- [ ] requirements.txt 설치 완료
- [ ] .env 파일 설정 완료

### ✅ Django 설정

- [ ] `python manage.py check` 통과
- [ ] 마이그레이션 적용 완료
- [ ] 개발 서버 정상 실행 (http://localhost:8000)
- [ ] 관리자 페이지 접근 가능 (http://localhost:8000/admin)

### ✅ AI 서비스 연동

- [ ] OpenAI API 키 설정 및 테스트
- [ ] Pinecone 연결 테스트
- [ ] HuggingFace 모델 로딩 테스트

### ✅ 문서 처리 기능

- [ ] PDF 파일 읽기 테스트
- [ ] OCR 기능 테스트 (한국어)
- [ ] 이미지 처리 기능 테스트

### ✅ 개발 도구

- [ ] IDE/에디터 설정 완료
- [ ] Git 설정 완료
- [ ] 디버깅 환경 구성

## 성능 최적화 설정

### Python 최적화

```bash
# Python 바이트코드 최적화
export PYTHONOPTIMIZE=1

# Python 경고 숨기기 (운영 환경)
export PYTHONWARNINGS=ignore
```

### Django 개발 설정

```python
# settings.py 개발 환경 최적화
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        },
    }
```

이 가이드를 따라하면 100% 완벽한 개발환경을 구축할 수 있습니다!
