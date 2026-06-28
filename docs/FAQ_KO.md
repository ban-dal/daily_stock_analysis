# 자주 묻는 질문(FAQ)

이 문서는 사용자가 자주 만나는 문제와 해결 방법을 정리합니다.

---

## 데이터 관련

### Q1: 미국 주식 코드(예: AMD, AAPL)를 분석할 때 가격이 잘못 표시되나요?

**증상**: 미국 주식 코드를 입력한 뒤 표시 가격이 명백히 잘못되거나(예: AMD가 7.33위안으로 표시), A주로 잘못 인식됩니다.

**원인**: 이전 버전의 코드 매칭 로직이 A주 규칙을 우선해 코드 충돌이 발생했습니다.

**해결 방법**:
1. v2.3.0에서 수정되었으며, 이제 시스템은 미국 주식 코드를 자동 인식합니다.
2. 문제가 계속되면 `.env`에 다음을 설정하세요.
   ```bash
   YFINANCE_PRIORITY=0
   ```
   이렇게 하면 미국 주식 데이터에 Yahoo Finance 데이터 소스를 우선 사용합니다.

> 관련 Issue: [#153](https://github.com/ZhuLinsen/daily_stock_analysis/issues/153)

---

### Q2: 리포트에서 "Volume Ratio" 필드가 비어 있거나 N/A로 표시되나요?

**증상**: 분석 리포트에 거래량 비율 데이터가 없어, AI의 거래량 변화 판단에 영향을 줍니다.

**원인**: 일부 기본 실시간 시세 소스(예: Sina 인터페이스)는 거래량 비율 필드를 제공하지 않습니다.

**해결 방법**:
1. v2.3.0에서 수정되었으며, Tencent 인터페이스가 이제 거래량 비율 파싱을 지원합니다.
2. 권장 실시간 시세 소스 우선순위:
   ```bash
   REALTIME_SOURCE_PRIORITY=tencent,akshare_sina,efinance,akshare_em
   ```
3. 시스템에는 fallback으로 5일 평균 거래량 계산이 내장되어 있습니다.

> 관련 Issue: [#155](https://github.com/ZhuLinsen/daily_stock_analysis/issues/155)

---

### Q3: Tushare 데이터 가져오기에 실패하고 Token 오류가 표시되나요?

**증상**: 로그에 `Tushare data fetch failed: Your token is incorrect, please verify`가 표시됩니다.

**해결 방법**:
1. **Tushare 계정이 없는 경우**: `TUSHARE_TOKEN`을 설정할 필요가 없습니다. 시스템은 무료 데이터 소스(AkShare, Efinance)를 자동으로 사용합니다.
2. **Tushare 계정이 있는 경우**: Token이 올바른지 확인하고 [Tushare Pro](https://tushare.pro/weborder/#/login?reg=834638) 개인 센터에서 확인하세요.
3. 이 프로젝트의 모든 핵심 기능은 Tushare 없이도 정상 동작합니다.

---

### Q4: 데이터 가져오기가 rate limit에 걸리거나 빈 값을 반환하나요?

**증상**: 로그에 `Circuit breaker triggered`가 표시되거나 데이터가 `None`으로 반환됩니다.

**원인**: 무료 데이터 소스(Eastmoney, Sina 등)에는 anti-scraping 메커니즘이 있어 고빈도 요청이 rate limit에 걸릴 수 있습니다.

**해결 방법**:
1. 시스템에는 다중 소스 자동 전환과 circuit breaker 보호가 내장되어 있습니다.
2. 관심 종목 수를 줄이거나 요청 간격을 늘리세요.
3. 분석을 너무 자주 수동 트리거하지 마세요.

---

## 설정 관련

### Q5: GitHub Actions 실행이 실패하고 환경 변수를 찾을 수 없다고 나오나요?

**증상**: Actions 로그에 `GEMINI_API_KEY` 또는 `STOCK_LIST`가 정의되지 않았다고 표시됩니다.

**원인**: GitHub는 `Secrets`(암호화됨)와 `Variables`(일반 변수)를 구분합니다. 잘못된 위치에 설정하면 읽기에 실패합니다.

**해결 방법**:
1. repo `Settings` → `Secrets and variables` → `Actions`로 이동합니다.
2. **Secrets**(`New repository secret` 클릭): 민감한 정보를 저장합니다.
   - `GEMINI_API_KEY`
   - `OPENAI_API_KEY`
   - `TELEGRAM_BOT_TOKEN`
   - 각종 Webhook URL
3. **Variables**(`Variables` 탭 클릭): 민감하지 않은 설정을 저장합니다.
   - `STOCK_LIST`
   - `GEMINI_MODEL`
   - `REPORT_TYPE`

> 호환성 참고: 일일 분석 workflow는 `STOCK_LIST` environment도 bind하므로, 해당 Environment의 variables에 실수로 추가한 `STOCK_LIST` 값도 읽을 수 있습니다. 그래도 Repository variables가 권장 위치입니다. 일일 작업이 수동 승인을 기다리게 만들고 싶지 않다면 이 Environment에 required reviewers, wait timers, deployment branch restrictions를 추가하지 마세요.

---

### Q6: .env 파일을 수정했는데 설정이 적용되지 않나요?

**해결 방법**:
1. `.env` 파일이 프로젝트 루트 디렉터리에 있는지 확인하세요.
2. **Docker 배포 / WebUI Settings**:
   - `--env-file .env` / Compose `env_file`은 호스트 `.env`를 시작 환경 변수로 주입할 뿐, 컨테이너 내부 `/app/.env`를 만들거나 다시 쓰지 않습니다.
   - 활성 `.env` 파일에 키가 없으면 WebUI Settings 페이지는 시작 시 주입된 환경 변수에서 같은 키를 fallback으로 표시합니다. raw `.env` export에는 여전히 활성 설정 파일 내용만 포함됩니다.
   - WebUI는 `STOCK_LIST`, `SCHEDULE_ENABLED`, `SCHEDULE_TIME`, `SCHEDULE_TIMES`, `SCHEDULE_RUN_IMMEDIATELY`, `RUN_IMMEDIATELY`를 컨테이너의 `.env`에 저장합니다.
   - WebUI 저장은 현재 프로세스에 config reload를 트리거하고, 런타임 읽기는 최신 persisted `.env`에서 계속 수행됩니다. 예를 들어 스케줄 실행은 저장된 `STOCK_LIST`를 계속 hot-read합니다.
   - 같은 키를 시작 env vars(`--env-file .env`, `docker run -e ...`, Compose `environment:`)로 전달하면 이후 재시작 시 그 시작 값이 여전히 우선될 수 있습니다. WebUI가 저장한 `.env` 값을 적용하려면 같은 이름의 override를 업데이트하거나 제거하세요.
   - WebUI 저장 설정을 영속화하려면 `ENV_FILE`을 `/app/data/runtime.env` 같은 쓰기 가능한 data-volume 파일로 지정하세요. 호스트 `.env`를 `/app/.env` 위에 단일 파일로 bind-mount하지 마세요.
   - `SCHEDULE_ENABLED`, `SCHEDULE_TIME`, `SCHEDULE_TIMES` 저장은 장기 실행 WebUI/API/Desktop 프로세스에서 런타임 스케줄러를 시작, 중지 또는 재구성합니다.
   - `SCHEDULE_RUN_IMMEDIATELY`와 `RUN_IMMEDIATELY`는 시작/일회성 설정으로 남습니다. 저장해도 즉시 분석 실행을 트리거하지 않습니다.
3. **Docker에서 `.env`를 수동 편집한 경우**: 변경 후 컨테이너를 재시작하세요.
   ```bash
   docker-compose down && docker-compose up -d
   ```
4. **GitHub Actions**: `.env` 파일은 작동하지 않으며 Secrets/Variables에 설정해야 합니다.
5. `.env.local` 같은 여러 `.env` 파일이 override를 일으키는지 확인하세요.

---

### Q7: Gemini/OpenAI API 접근을 위한 프록시는 어떻게 설정하나요?

**해결 방법**:

`.env`에 설정:
```bash
USE_PROXY=true
PROXY_HOST=127.0.0.1
PROXY_PORT=10809
```

> 참고: 프록시 설정은 로컬 실행에서만 작동하며, GitHub Actions 환경에는 프록시가 필요 없습니다.

---

### LLM 설정

> 전체 상세 내용: [LLM 설정 가이드](LLM_CONFIG_GUIDE_KO.md).

**Q: GEMINI_API_KEY와 LLM_CHANNELS를 모두 설정했는데 왜 channels만 사용하나요?**

시스템은 우선순위에 따라 정확히 하나의 모드만 사용합니다. 고급 YAML 라우팅(`LITELLM_CONFIG`) > `LLM_CHANNELS` > legacy 키 순서입니다. 단, YAML 라우팅은 파일이 성공적으로 파싱되고 비어 있지 않은 `model_list`를 생성할 때만 적용됩니다. YAML 경로가 잘못되었거나 내용이 비어 있으면 시스템은 자동으로 `LLM_CHANNELS` 또는 legacy 키로 fallback합니다. 한 tier가 활성화되면 낮은 우선순위 tier는 사용되지 않습니다.

**Q: check_env가 사용 가능한 AI 모델이 설정되지 않았다고 말하면 어떻게 해야 하나요?**

하나의 공급자와 해당 API 키부터 시작하세요. 기본 모델을 고정하려면 `LITELLM_MODEL=provider/model`을 추가하세요. 다중 모델 전환이 필요하면 `LLM_CHANNELS` 또는 고급 YAML 라우팅을 설정하세요. 설정 검증은 `python scripts/check_env.py --config`, 실제 API 호출 검사는 `python scripts/check_env.py --llm`으로 실행합니다.

**Q: 여러 모델을 동시에 사용하는 방법은 무엇인가요(예: AIHubmix + DeepSeek + Gemini)?**

채널 모드를 사용하세요. `LLM_CHANNELS=aihubmix,deepseek,gemini`로 설정하고 각 채널의 `LLM_{NAME}_BASE_URL`, `LLM_{NAME}_API_KEY`, `LLM_{NAME}_MODELS`를 구성합니다. Web Settings → AI Model → AI Model Access에서도 시각적으로 설정할 수 있습니다.

**Q: ask-stock / Agent 페이지에서 사용 가능한 LLM이 없다고 나오지만 legacy `GEMINI_*` / `OPENAI_*` / `ANTHROPIC_*` 설정만 쓰고 있습니다. 무엇을 확인해야 하나요?**

먼저 `LITELLM_CONFIG` 또는 `LLM_CHANNELS`가 활성화되어 있는지 확인하세요. 이 두 tier 중 하나라도 legacy 키보다 우선합니다. 둘 다 활성화되어 있지 않고 `AGENT_LITELLM_MODEL`이 비어 있으면 ask-stock Agent는 legacy 공급자 모델을 자동으로 상속합니다. `GEMINI_MODEL`, `OPENAI_MODEL`, `ANTHROPIC_MODEL`은 해당 런타임에 맞는 LiteLLM provider-prefixed 모델명으로 매핑됩니다. 이 수정은 예전 설정을 조용히 마이그레이션하거나 지우지 않습니다. 누락된 키, 누락된 모델명, 상위 tier 설정 우선 여부 등 실제 backend 이유를 frontend에 반환해 볼 수 있게 할 뿐입니다. 전체 호환성 세부 사항은 [LLM 설정 가이드](LLM_CONFIG_GUIDE_KO.md)의 “Ask-Stock Agent / LiteLLM compatibility notes”에 문서화되어 있습니다.

---

## Push 알림 관련

### Q8: Bot push가 실패하고 메시지가 너무 길다고 나오나요?

**증상**: 분석은 성공했지만 알림을 받지 못하고, 로그에 400 오류 또는 `Message too long`이 표시됩니다.

**원인**: 플랫폼마다 메시지 길이 제한이 다릅니다.
- WeChat Work: 4KB
- Feishu: 20KB
- DingTalk: 20KB

**해결 방법**:
1. **자동 분할**: 최신 버전은 긴 메시지 자동 분할을 구현했습니다.
2. **단일 종목 push 모드**: `SINGLE_STOCK_NOTIFY=true`로 설정하면 각 종목 분석 후 즉시 push합니다.
3. **간략 리포트**: `REPORT_TYPE=simple`로 설정해 간소화된 형식을 사용합니다.

---

### Q9: Telegram push 메시지를 받지 못하나요?

**해결 방법**:
1. `TELEGRAM_BOT_TOKEN`과 `TELEGRAM_CHAT_ID`가 모두 설정되어 있는지 확인하세요.
2. Chat ID 얻는 방법:
   - Bot에게 아무 메시지나 보냅니다.
   - `https://api.telegram.org/bot<TOKEN>/getUpdates`에 접속합니다.
   - 반환된 JSON에서 `chat.id`를 찾습니다.
3. 그룹 채팅이라면 Bot이 대상 그룹에 추가되어 있는지 확인하세요.
4. 로컬 실행 시 Telegram API에 접근할 수 있어야 합니다(프록시가 필요할 수 있음).

---

### Q10: WeChat Work Markdown 형식이 올바르게 표시되지 않나요?

**해결 방법**:
1. WeChat Work의 Markdown 지원은 제한적입니다. 다음 설정을 시도하세요.
   ```bash
   WECHAT_MSG_TYPE=text
   ```
2. 그러면 일반 텍스트 형식 메시지를 전송합니다.

---

## AI 모델 관련

### Q11: Gemini API가 429 오류(too many requests)를 반환하나요?

**증상**: 로그에 `Resource has been exhausted` 또는 `429 Too Many Requests`가 표시됩니다.

**해결 방법**:
1. Gemini 무료 tier에는 rate limit이 있습니다(약 15 RPM).
2. 동시에 분석하는 종목 수를 줄이세요.
3. 요청 지연을 늘리세요.
   ```bash
   GEMINI_REQUEST_DELAY=5
   ANALYSIS_DELAY=10
   ```
4. 또는 OpenAI 호환 API를 백업으로 전환하세요.

---

### Q12: DeepSeek 및 기타 중국 모델은 어떻게 사용하나요?

**설정 방법**:

```bash
# GEMINI_API_KEY를 설정할 필요 없음
OPENAI_API_KEY=sk-xxxxxxxx
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-v4-flash
# deepseek-chat / deepseek-reasoner는 계속 호환되지만, DeepSeek는 2026/07/24 이후 deprecated로 표시합니다
```

지원 모델 서비스:
- DeepSeek: `https://api.deepseek.com`
- Qwen (Tongyi Qianwen): `https://dashscope.aliyuncs.com/compatible-mode/v1`
- Moonshot: `https://api.moonshot.cn/v1`

---

### Q12b: Ollama 로컬 모델은 어떻게 사용하나요?

**설정**: `OLLAMA_API_BASE` + `LITELLM_MODEL`을 사용하거나, 채널 모드(`LLM_CHANNELS=ollama` + `LLM_OLLAMA_BASE_URL` + `LLM_OLLAMA_MODELS`)를 사용하세요.

**주의점**: Ollama에 `OPENAI_BASE_URL`을 사용하지 마세요. 시스템이 URL을 잘못 이어 붙일 수 있습니다(예: 404, `api/generate/api/show`). [LLM 설정 가이드](LLM_CONFIG_GUIDE_KO.md)의 Example 4와 채널 예시를 참고하세요.

---

### Q12c: `OllamaException / APIConnectionError`가 발생하나요(All LLM models failed)?

**증상**: 로그에 `litellm.APIConnectionError: OllamaException` 또는 `Analysis failed: All LLM models failed (tried 1 model(s))`가 표시됩니다.

다음 5개 체크포인트를 순서대로 확인하세요.

1. **Ollama 서비스가 실행 중인가요?**
   ```bash
   # 프로세스 확인
   pgrep -a ollama
   # 출력이 없으면 먼저 시작
   ollama serve
   ```
   listening 여부 확인: `curl http://localhost:11434`가 `Ollama is running`을 반환해야 합니다.

2. **`OLLAMA_API_BASE`가 올바르게 설정되어 있나요?**
   - ✅ 올바름: `OLLAMA_API_BASE=http://localhost:11434`
   - ❌ 잘못됨: Ollama 주소를 `OPENAI_BASE_URL`에 넣으면 URL path가 깨집니다(예: `…/api/generate/api/show`).

3. **모델명에 `ollama/` 접두사가 포함되어 있나요?**
   - ✅ 올바름: `LITELLM_MODEL=ollama/qwen3:8b`
   - ❌ 잘못됨: `LITELLM_MODEL=qwen3:8b`(접두사 누락 — litellm이 Ollama로 route할 수 없음)

4. **모델을 로컬에 pull했나요?**
   ```bash
   ollama list           # 다운로드된 모델 목록
   ollama pull qwen3:8b  # 없으면 pull
   ```

5. **원격 또는 Docker 배포의 네트워크 / 방화벽**
   - Ollama가 다른 호스트에서 실행 중이면 `OLLAMA_API_BASE`를 실제 IP로 설정하세요. 예: `http://192.168.1.100:11434`
   - 11434 포트가 열려 있고 Ollama가 올바른 주소에 bind되어 있는지 확인하세요(`OLLAMA_HOST=0.0.0.0:11434`).

> 전체 설정 예시는 [LLM 설정 가이드 → 예시 4 (Ollama)](LLM_CONFIG_GUIDE_KO.md#예시-4-ollama-로컬-모델-사용)를 참고하세요.

---

## Docker 관련

### Q13: Docker 컨테이너가 시작 직후 종료되나요?

**해결 방법**:
1. 컨테이너 로그를 봅니다.
   ```bash
   docker logs <container_id>
   ```
2. 일반적인 원인:
   - 환경 변수가 올바르게 설정되지 않음
   - `.env` 파일 형식 오류(예: 불필요한 공백)
   - 의존성 패키지 버전 충돌

---

### Q14: Docker에서 API 서비스에 접근할 수 없나요?

**해결 방법**:
1. 시작 명령에 `--host 0.0.0.0`이 포함되어 있는지 확인하세요(127.0.0.1이면 안 됨).
2. 포트 매핑이 올바른지 확인하세요.
   ```yaml
    ports:
      - "8000:8000"
    ```

---

### Q14.1: Docker로 설치했을 때 소프트웨어 버전은 어디에 저장되나요?

**짧은 답:** Docker 사용자의 authoritative version은 Python 소스 파일에 하드코딩된 상수가 아니라 **실제로 배포한 이미지 태그**입니다.

**이유**:
1. Docker publish는 `.github/workflows/docker-publish.yml`에 의해 구동되며, `v*.*.*`와 일치하는 Git tag(예: `v3.12.0`)에 대해서만 release image를 publish합니다.
2. 따라서 Docker 이미지 버전은 `main.py`, `server.py` 또는 다른 backend 모듈의 고정값이 아니라 **GitHub Release / Git tag**를 따릅니다.
3. `apps/dsa-web/package.json`의 `version` 필드는 현재 placeholder `0.0.0`입니다. WebUI version/build 카드는 frontend assets가 다시 빌드되었는지 확인하는 데 유용하지만 Docker release version은 아닙니다.
4. 데스크톱 앱은 `apps/dsa-desktop/package.json`에 자체 버전이 있으며, 이는 Electron 데스크톱 빌드에만 적용되고 Docker 이미지에는 적용되지 않습니다.

**현재 Docker 버전 확인 방법**:
1. **배포 명령 또는 Compose 파일의 이미지 태그를 확인하세요.** 예를 들어 `ghcr.io/zhulinsen/daily_stock_analysis:v3.12.0`라면 배포된 버전은 `v3.12.0`입니다.
2. **`latest`를 사용했다면**, 원래의 `docker pull`, `docker-compose.yml` 또는 배포 스크립트를 확인한 뒤 [GitHub Releases](https://github.com/ZhuLinsen/daily_stock_analysis/releases)와 비교하세요.
3. **frontend가 갱신되었는지만 확인하려면**, WebUI → Settings를 열어 `Build ID` / `Build Time`을 확인하세요. 이는 정적 asset freshness를 확인할 뿐 Docker release version은 아닙니다.

**권장:** 반복 업데이트를 피하려면 `latest`에 의존하기보다 `v3.12.0` 같은 고정 버전 태그를 사용하는 편이 좋습니다.

---

## 기타 문제

### Q15: 종목 분석 없이 시장 리뷰만 실행하려면 어떻게 하나요?

**방법**:
```bash
# 로컬 실행
python main.py --market-only

# GitHub Actions
# 수동 트리거 시 mode: market-only 선택
```

---

### Q16: 분석 결과의 Buy/Hold/Sell 개수가 잘못 표시되나요?

**원인**: 이전 버전은 통계에 regex matching을 사용해 실제 추천과 일치하지 않을 수 있었습니다.

**해결 방법**: 최신 버전에서 수정되었으며, AI 모델이 정확한 통계를 위해 `decision_type` 필드를 직접 출력합니다.

---

## 아직 질문이 있나요?

위 내용으로 문제가 해결되지 않았다면 다음을 이용하세요.
1. [전체 설정 가이드](full-guide_KO.md) 확인
2. [GitHub Issue](https://github.com/ZhuLinsen/daily_stock_analysis/issues) 검색 또는 제출
3. 최신 수정 사항은 [Changelog](CHANGELOG.md) 확인

---

*마지막 업데이트: 2026-04-20*
