# 배포 가이드

이 문서는 AI 주식 분석 시스템을 서버에 배포하는 방법을 설명합니다.

## 배포 옵션 비교

| 옵션 | 장점 | 단점 | 추천 대상 |
|------|------|------|----------|
| **Docker Compose** ⭐ | 원클릭 배포, 격리된 환경, 쉬운 마이그레이션, 쉬운 업그레이드 | Docker 설치 필요 | **권장**: 대부분의 상황 |
| **직접 배포** | 단순함, 추가 의존성 없음 | 환경 의존성, 마이그레이션 어려움 | 임시 테스트 |
| **Systemd Service** | 시스템 수준 관리, 부팅 시 자동 시작 | 설정이 복잡함 | 장기 안정 운영 |
| **Supervisor** | 프로세스 관리, 자동 재시작 | 추가 설치 필요 | 다중 프로세스 관리 |

**결론: 가장 빠르고 편리하게 이전하려면 Docker Compose를 권장합니다.**

---

## 옵션 1: Docker Compose 배포(권장)

### 1. Docker 설치

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# CentOS
sudo yum install -y docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. 설정 파일 준비

```bash
# 코드 클론(또는 서버에 코드 업로드)
git clone <your-repo-url> /opt/stock-analyzer
cd /opt/stock-analyzer

# 설정 파일 복사 및 편집
cp .env.example .env
vim .env  # 실제 API Keys와 설정 입력
```

### 3. 원클릭 시작

```bash
# 빌드 및 시작
docker-compose -f ./docker/docker-compose.yml up -d

# 로그 보기
docker-compose -f ./docker/docker-compose.yml logs -f

# 실행 상태 보기
docker-compose -f ./docker/docker-compose.yml ps
```

### 3.1 리소스 권장 사항

기본 `docker/docker-compose.yml`은 각 서비스에 `limits.memory: 1G`와 `reservations.memory: 512M`을 설정합니다. 전체 분석 워크로드의 권장 시작점으로 보세요.

- 최소 시험: `512M`. 가벼운 Web/API 사용, 단일 종목 실행, 낮은 동시성에만 적합합니다. `MAX_WORKERS=1`로 설정하세요.
- 권장: `1G`. `server` 또는 `analyzer` 중 하나를 실행하는 일반 분석에 적합합니다.
- 무거운 워크로드: `2G+`. `server + analyzer` 동시 실행, 다중 종목 분석, 기본 `MAX_WORKERS=3`, 시장 리뷰, 뉴스 확장, 이미지 리포트, AlphaSift에 적합합니다.

`512M`만 사용할 수 있다면 `server`와 `analyzer`를 동시에 시작하지 말고, 필수가 아닌 시장 리뷰, 뉴스 확장, 이미지 리포트 기능을 비활성화하세요.

### 4. 일반 관리 명령

```bash
# 서비스 중지
docker-compose -f ./docker/docker-compose.yml down

# 서비스 재시작
docker-compose -f ./docker/docker-compose.yml restart

# 코드 업데이트 후 재배포
git pull
docker-compose -f ./docker/docker-compose.yml build --no-cache
docker-compose -f ./docker/docker-compose.yml up -d

# 디버깅을 위해 컨테이너 진입
docker-compose -f ./docker/docker-compose.yml exec -u dsa stock-analyzer bash

# 분석을 수동으로 한 번 실행
docker-compose -f ./docker/docker-compose.yml exec -u dsa stock-analyzer python main.py --no-notify
```

### 5. 데이터 영속성

데이터는 호스트 디렉터리에 자동 저장됩니다.
- `./data/` - 데이터베이스 파일
- `./logs/` - 로그 파일
- `./reports/` - 분석 리포트

### 6. 권한

Docker 이미지 시작 entrypoint는 mount된 `./data`, `./logs`, `./reports` 디렉터리를 자동으로 생성하고 소유권을 수정한 뒤, 권한을 non-root `dsa` 사용자(UID 1000)로 낮춥니다. 일반 배포에서는 호스트에서 수동으로 `chown` / `chmod`를 실행할 필요가 없습니다.

`--user` / Compose `user:`를 명시적으로 설정했거나, 읽기 전용 mount, rootless Docker, NFS 또는 컨테이너가 소유권을 수정하지 못하게 하는 다른 환경을 사용하는 경우 실제 런타임 사용자가 이 디렉터리에 쓸 수 있는지 확인하세요.

---

## 옵션 2: 직접 배포

### 1. Python 환경 설치

```bash
# Python 3.10+ 설치
sudo apt update
sudo apt install -y python3.10 python3.10-venv python3-pip

# 가상 환경 생성
python3.10 -m venv /opt/stock-analyzer/venv
source /opt/stock-analyzer/venv/bin/activate
```

### 2. 의존성 설치

```bash
cd /opt/stock-analyzer
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 환경 변수 설정

```bash
cp .env.example .env
vim .env  # 설정 입력
```

### 4. 실행

```bash
# 단일 실행
python main.py

# 스케줄 작업 모드(포그라운드)
python main.py --schedule

# 백그라운드 실행(nohup 사용)
nohup python main.py --schedule > /dev/null 2>&1 &
```

---

## 옵션 3: Systemd Service

부팅 시 자동 시작과 자동 재시작을 위해 systemd service 파일을 만듭니다.

### 1. Service 파일 생성

```bash
sudo vim /etc/systemd/system/stock-analyzer.service
```

내용:
```ini
[Unit]
Description=AI Stock Analysis System
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/stock-analyzer
Environment="PATH=/opt/stock-analyzer/venv/bin"
ExecStart=/opt/stock-analyzer/venv/bin/python main.py --schedule
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
```

### 2. Service 시작

```bash
# 설정 다시 로드
sudo systemctl daemon-reload

# 서비스 시작
sudo systemctl start stock-analyzer

# 부팅 시 자동 시작 활성화
sudo systemctl enable stock-analyzer

# 상태 보기
sudo systemctl status stock-analyzer

# 로그 보기
journalctl -u stock-analyzer -f
```

---

## 설정 가이드

### 필수 설정

| 설정 항목 | 설명 | 얻는 방법 |
|--------|------|----------|
| `ANSPIRE_API_KEYS` / `AIHUBMIX_KEY` / `GEMINI_API_KEY` / `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` | AI 모델 키를 최소 하나 설정합니다. Anspire 또는 AIHubMix를 우선 권장합니다. | 공급자 콘솔 |
| `STOCK_LIST` | 관심 종목 | 쉼표로 구분한 종목 코드 |
| 알림 채널 | WeChat Work, Feishu, Telegram, email 등 최소 하나 설정 | 알림 공급자 |

### 선택 설정

| 설정 항목 | 기본값 | 설명 |
|--------|--------|------|
| `SCHEDULE_ENABLED` | `false` | 스케줄 작업 활성화 |
| `SCHEDULE_TIME` | `18:00` | 매일 실행 시간 |
| `MARKET_REVIEW_ENABLED` | `true` | 시장 리뷰 활성화 |
| `ANSPIRE_API_KEYS` | - | Anspire LLM 및 뉴스 검색(권장) |
| `AIHUBMIX_KEY` | - | AIHubMix 원키 다중 모델 접근(권장) |
| `SERPAPI_API_KEYS` | - | SerpAPI 실시간 금융 뉴스 검색(권장) |
| `TAVILY_API_KEYS` | - | Tavily 뉴스 검색(선택) |
| `MINIMAX_API_KEYS` | - | MiniMax 검색(선택) |

---

## 프록시 설정

서버가 중국 본토에 있는 경우 Gemini API에 접근하려면 프록시가 필요합니다.

### Docker 방식

`docker-compose.yml` 편집:
```yaml
environment:
  - http_proxy=http://your-proxy:port
  - https_proxy=http://your-proxy:port
```

### 직접 배포 방식

`main.py` 상단 편집:
```python
os.environ["http_proxy"] = "http://your-proxy:port"
os.environ["https_proxy"] = "http://your-proxy:port"
```

---

## 모니터링 및 유지보수

### 로그 보기

```bash
# Docker 방식
docker-compose -f ./docker/docker-compose.yml logs -f --tail=100

# 직접 배포
tail -f /opt/stock-analyzer/logs/stock_analysis_*.log
```

### Health Check

```bash
# 프로세스 확인
ps aux | grep main.py

# 최근 리포트 확인
ls -la /opt/stock-analyzer/reports/
```

### 정기 유지보수

```bash
# 오래된 로그 정리(7일 보관)
find /opt/stock-analyzer/logs -mtime +7 -delete

# 오래된 리포트 정리(30일 보관)
find /opt/stock-analyzer/reports -mtime +30 -delete
```

---

## FAQ

### 1. Docker build 실패

```bash
# 캐시를 지우고 다시 빌드
docker-compose -f ./docker/docker-compose.yml build --no-cache
```

### 2. API 접근 timeout

프록시 설정을 확인하고 서버가 Gemini API에 접근할 수 있는지 확인하세요.

### 3. Database locked

```bash
# 서비스를 중지한 뒤 lock 파일 삭제
rm /opt/stock-analyzer/data/*.lock
```

### 4. 메모리 부족

기본 Compose 권장값은 이미 `1G`입니다. 그래도 컨테이너가 OOM에 걸리거나 플랫폼에 의해 종료되면 `docker-compose.yml`의 메모리 제한을 높이세요. `server + analyzer` 동시 실행, 다중 종목 분석, 시장 리뷰, 이미지 리포트, AlphaSift를 사용할 때는 `2G+`를 사용하세요.
```yaml
deploy:
  resources:
    limits:
      memory: 1G
    reservations:
      memory: 512M
```

제약이 있는 `512M` 배포에서는 `MAX_WORKERS=1`로 설정하고, `server` 또는 `analyzer` 중 하나만 시작하며, 필수가 아닌 시장 리뷰, 뉴스 확장, 이미지 리포트 작업을 줄이세요.

---

## 빠른 마이그레이션

한 서버에서 다른 서버로 이전:

```bash
# 원본 서버: 패키징
cd /opt/stock-analyzer
tar -czvf stock-analyzer-backup.tar.gz .env data/ logs/ reports/

# 대상 서버: 배포
mkdir -p /opt/stock-analyzer
cd /opt/stock-analyzer
git clone <your-repo-url> .
tar -xzvf stock-analyzer-backup.tar.gz
docker-compose -f ./docker/docker-compose.yml up -d
```

---

## 옵션 4: GitHub Actions 배포(Serverless)

**가장 간단한 옵션입니다.** 서버가 필요 없고 GitHub의 무료 컴퓨팅 리소스를 활용합니다.

### 장점
- ✅ **완전 무료**(월 2000분)
- ✅ **서버 불필요**
- ✅ **자동 스케줄 실행**
- ✅ **유지보수 비용 없음**

### 제한
- ⚠️ 상태 없음(매 실행마다 새 환경)
- ⚠️ 스케줄 시간이 몇 분 지연될 수 있음
- ⚠️ HTTP API를 제공할 수 없음

### 배포 단계

#### 1. GitHub Repository 생성

```bash
# git 초기화(아직 안 했다면)
cd /path/to/daily_stock_analysis
git init
git add .
git commit -m "Initial commit"

# GitHub repo 생성 후 push
# GitHub 웹에서 새 repo를 만든 뒤:
git remote add origin https://github.com/your-username/daily_stock_analysis.git
git branch -M main
git push -u origin main
```

#### 2. Secrets 설정(중요)

repo 페이지 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**으로 이동합니다.

다음 Secrets를 추가하세요.

| Secret 이름 | 설명 | 필수 |
|------------|------|------|
| `ANSPIRE_API_KEYS` | Anspire Open API Key(LLM과 검색을 위한 원키) | 권장 |
| `AIHUBMIX_KEY` | AIHubMix API Key(여러 모델 계열을 위한 원키) | 권장 |
| `ANTHROPIC_API_KEY` | Anthropic API Key | 선택 |
| `GEMINI_API_KEY` | Gemini AI API Key | 선택 |
| `OPENAI_API_KEY` | OpenAI 호환 API Key | 선택 |
| `WECHAT_WEBHOOK_URL` | WeChat Work Bot Webhook | 선택* |
| `FEISHU_WEBHOOK_URL` | Feishu Bot Webhook | 선택* |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 선택* |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 선택* |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID | 선택* |
| `EMAIL_SENDER` | 발신 이메일 | 선택* |
| `EMAIL_PASSWORD` | 이메일 인증 코드 | 선택* |
| `SERVERCHAN3_SENDKEY` | ServerChan v3 Sendkey | 선택* |
| `CUSTOM_WEBHOOK_URLS` | Custom Webhook(여러 개는 쉼표로 구분) | 선택* |
| `STOCK_LIST` | 관심 종목, 예: `600519,300750` | ✅ |
| `SERPAPI_API_KEYS` | SerpAPI Key | 권장 |
| `TAVILY_API_KEYS` | Tavily Search API Key | 선택 |
| `BOCHA_API_KEYS` | Bocha Search API Key | 선택 |
| `BRAVE_API_KEYS` | Brave Search API Key | 선택 |
| `MINIMAX_API_KEYS` | MiniMax Coding Plan Web Search | 선택 |
| `TUSHARE_TOKEN` | Tushare Token | 선택 |
| `GEMINI_MODEL` | 모델명(기본값 gemini-2.0-flash) | 선택 |

> *참고: 알림 채널을 최소 하나 설정하세요. 여러 채널 동시 push를 지원합니다.

#### 3. Workflow 파일 확인

`.github/workflows/00-daily-analysis.yml` 파일이 존재하고 커밋되어 있는지 확인하세요.

```bash
git add .github/workflows/00-daily-analysis.yml
git commit -m "Add GitHub Actions workflow"
git push
```

#### 4. 수동 테스트 실행

1. repo 페이지 → **Actions** 탭으로 이동
2. **"Daily Stock Analysis"** workflow 선택
3. **"Run workflow"** 버튼 클릭
4. 실행 모드 선택:
   - `full` - 전체 분석(종목 + 시장)
   - `market-only` - 시장 리뷰만
   - `stocks-only` - 종목 분석만
5. 초록색 **"Run workflow"** 버튼 클릭

#### 5. 실행 로그 보기

- Actions 페이지에 실행 기록이 표시됩니다.
- 특정 실행 기록을 클릭하면 상세 로그를 볼 수 있습니다.
- 분석 리포트는 30일 동안 Artifacts로 저장됩니다.

### 스케줄 상세

기본 설정: **월요일부터 금요일까지, 베이징 시간 18:00** 자동 실행

시간 수정: `.github/workflows/00-daily-analysis.yml`의 cron 표현식을 편집합니다.

```yaml
schedule:
  - cron: '0 10 * * 1-5'  # UTC time, +8 = Beijing time
```

일반적인 cron 예시:
| 표현식 | 설명 |
|--------|------|
| `'0 10 * * 1-5'` | 월-금 18:00(베이징) |
| `'30 7 * * 1-5'` | 월-금 15:30(베이징) |
| `'0 10 * * *'` | 매일 18:00(베이징) |
| `'0 2 * * 1-5'` | 월-금 10:00(베이징) |

### 관심 종목 수정

방법 1: repo Secret `STOCK_LIST` 수정

방법 2: 코드를 직접 수정한 뒤 push:
```bash
# .env.example 수정 또는 코드에 기본값 설정
git commit -am "Update stock list"
git push
```

### FAQ

**Q: 스케줄 작업이 왜 실행되지 않나요?**
A: GitHub Actions 스케줄 작업은 5-15분 지연될 수 있고, repo에 활동이 있을 때만 트리거됩니다. 오랫동안 커밋이 없으면 workflow가 비활성화될 수 있습니다.

**Q: 과거 리포트는 어떻게 보나요?**
A: Actions → 실행 기록 선택 → Artifacts → `analysis-reports-xxx` 다운로드

**Q: 무료 할당량이 충분한가요?**
A: 실행 한 번에 약 2-5분이 걸리며, 월 22영업일 기준 44-110분으로 2000분 제한보다 훨씬 적습니다.

---

**배포가 순조롭기를 바랍니다!**
