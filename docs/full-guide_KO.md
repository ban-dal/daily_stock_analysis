# 전체 설정 및 배포 가이드

이 문서는 AI 주식 분석 시스템의 전체 설정 가이드입니다. 고급 기능이나 특수한 배포 방식이 필요한 사용자를 대상으로 합니다.

> 빠른 시작 가이드는 [README_KO.md](README_KO.md)를 참고하세요. 이 문서는 고급 설정을 다룹니다.

## 프로젝트 구조

```
daily_stock_analysis/
├── main.py              # 메인 진입점
├── src/                 # 핵심 비즈니스 로직
│   ├── analyzer.py      # AI 분석기
│   ├── config.py        # 설정 관리
│   ├── notification.py  # 메시지 push 알림
│   └── ...
├── data_provider/       # 다중 소스 데이터 어댑터
├── bot/                 # Bot 상호작용 모듈
├── api/                 # FastAPI 백엔드 서비스
├── apps/dsa-web/        # React 프론트엔드
├── docker/              # Docker 설정
├── docs/                # 프로젝트 문서
└── .github/workflows/   # GitHub Actions
```

## 목차

- [프로젝트 구조](#프로젝트-구조)
- [GitHub Actions 설정](#github-actions-설정)
- [전체 환경 변수 목록](#전체-환경-변수-목록)
- [Docker 배포](#docker-배포)
- [로컬 배포](#로컬-배포)
- [스케줄 작업 설정](#스케줄-작업-설정)
- [알림 채널 설정](#알림-채널-설정)
- [데이터 소스 설정](#데이터-소스-설정)
- [고급 기능](#고급-기능)
- [백테스팅](#백테스팅)
- [로컬 WebUI 관리 인터페이스](#로컬-webui-관리-인터페이스)

---

## GitHub Actions 설정

### 1. 이 저장소 Fork

오른쪽 위의 `Fork` 버튼을 클릭합니다.

### 2. Secrets 설정

Fork한 repo → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`으로 이동합니다.

<div align="center">
  <img src="assets/secret_config.png" alt="GitHub Secrets Configuration" width="600">
</div>

#### AI 모델 설정(최소 하나 설정)

| Secret 이름 | 설명 | 필수 여부 |
|------------|------|:----:|
| `ANSPIRE_API_KEYS` | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC) API 키. 주요 LLM과 중국어 최적화 웹 검색을 하나의 키로 사용할 수 있으며, 이 프로젝트용 무료 할당량이 있습니다. | 권장 |
| `AIHUBMIX_KEY` | [AIHubMix](https://aihubmix.com/?aff=CfMq) API 키. 여러 모델 계열을 하나의 키로 사용할 수 있으며, 이 프로젝트용 10% 충전 할인 혜택이 있습니다. | 권장 |
| `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/)에서 무료 키 발급 | 선택 |
| `ANTHROPIC_API_KEY` | Anthropic Claude API Key | 선택 |
| `OPENAI_API_KEY` | OpenAI 호환 API Key(DeepSeek, Qwen 등 지원) | 선택 |
| `OPENAI_BASE_URL` | OpenAI 호환 API endpoint(예: `https://api.deepseek.com`) | 선택 |
| `OPENAI_MODEL` | 모델명(예: `deepseek-v4-flash`) | 선택 |

> *참고: 모델 키 또는 채널을 최소 하나 설정하세요. Anspire 또는 AIHubMix는 원키 다중 모델 접근을 시작하기 가장 단순한 선택입니다. 사용 가능한 AI 모델 키나 모델 채널이 없으면 startup validation이 명확한 오류를 보고합니다.

#### 알림 채널(여러 개 설정 가능, 모두 알림 수신)

> 알림 채널 매트릭스, 최소/고급 키 구분, 생성된 Actions 매핑, `--check-notify` CLI 동작, Web 원클릭 알림 테스트, local / Docker / GitHub Actions / Desktop 설정 참고 사항은 [알림 가이드](notifications.md)에서 추적합니다.

| Secret 이름 | 설명 | 필수 여부 |
|------------|------|:----:|
| `WECHAT_WEBHOOK_URL` | WeChat Work Webhook URL | 선택 |
| `FEISHU_WEBHOOK_URL` | Feishu Webhook URL | 선택 |
| `FEISHU_WEBHOOK_SECRET` | Feishu Webhook 서명 secret("Signature" 보안 활성화 시 필요) | 선택 |
| `FEISHU_WEBHOOK_KEYWORD` | Feishu Webhook keyword("Keyword" 보안 활성화 시 필요) | 선택 |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token(@BotFather에서 발급) | 선택 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 선택 |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID(topic으로 전송할 때 사용) | 선택 |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL([생성 방법](https://support.discord.com/hc/en-us/articles/228383668)) | 선택 |
| `DISCORD_BOT_TOKEN` | Discord Bot Token(Webhook과 둘 중 하나 선택) | 선택 |
| `DISCORD_MAIN_CHANNEL_ID` | Discord Channel ID(Bot 사용 시 필요) | 선택 |
| `DISCORD_INTERACTIONS_PUBLIC_KEY` | Discord Public Key(인바운드 Interaction/Webhook 서명 검증에만 필요) | 선택 |
| `SLACK_BOT_TOKEN` | Slack Bot Token(권장, 이미지 업로드 지원. Webhook과 함께 설정되면 우선) | 선택 |
| `SLACK_CHANNEL_ID` | Slack Channel ID(Bot 사용 시 필요) | 선택 |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL(텍스트 전용, 이미지 미지원) | 선택 |
| `EMAIL_SENDER` | 발신 이메일(예: `xxx@qq.com`) | 선택 |
| `EMAIL_PASSWORD` | 이메일 authorization code(로그인 비밀번호 아님) | 선택 |
| `EMAIL_RECEIVERS` | 수신 이메일(쉼표 구분, 비워두면 자신에게 전송) | 선택 |
| `EMAIL_SENDER_NAME` | 발신자 표시 이름 | 선택 |
| `STOCK_GROUP_N` / `EMAIL_GROUP_N` | 이메일 라우팅 그룹(Issue #268): `STOCK_GROUP_N`은 `STOCK_LIST`의 부분집합이어야 하며, 분석 범위나 다른 채널이 아니라 이메일 수신자에만 영향을 줍니다. | 선택 |
| `PUSHPLUS_TOKEN` | PushPlus Token([여기서 발급](https://www.pushplus.plus), 중국 push 서비스) | 선택 |
| `SERVERCHAN3_SENDKEY` | ServerChan v3 Sendkey([여기서 발급](https://sc3.ft07.com/), 모바일 앱 push 서비스) | 선택 |
| `ASTRBOT_URL` | AstrBot Webhook URL | 선택 |
| `ASTRBOT_TOKEN` | 선택적 AstrBot Bearer Token | 선택 |
| `NTFY_URL` | 전체 ntfy topic endpoint. topic path를 포함해야 함. 예: `https://ntfy.sh/my-topic` | 선택 |
| `NTFY_TOKEN` | 선택적 ntfy Bearer Token | 선택 |
| `GOTIFY_URL` | Gotify server base URL. `/message` 제외. sender가 `/message`를 붙입니다. | 선택 |
| `GOTIFY_TOKEN` | `X-Gotify-Key` header로 전송되는 Gotify application token | 선택 |
| `CUSTOM_WEBHOOK_URLS` | Custom Webhook(DingTalk 등 지원, 쉼표 구분) | 선택 |
| `CUSTOM_WEBHOOK_BEARER_TOKEN` | custom webhook용 Bearer Token(인증 webhook용) | 선택 |
| `CUSTOM_WEBHOOK_BODY_TEMPLATE` | AstrBot, NapCat, 자체 호스팅 서비스처럼 특수 payload가 필요한 custom webhook JSON body template | 선택 |
| `WEBHOOK_VERIFY_SSL` | 이 설정을 읽는 webhook-style 알림 요청의 HTTPS 인증서 검증(default true). self-signed cert에는 false 설정 가능. 경고: 비활성화는 심각한 보안 위험(MITM)이 있으므로 신뢰된 내부망에서만 사용하세요. | 선택 |

> *참고: 채널을 최소 하나 설정하세요. 여러 채널을 설정하면 모두 알림을 받습니다. Startup validation은 누락된 Telegram / email paired field와 `http://` 또는 `https://`로 시작하지 않는 흔한 Webhook URL을 보고합니다.
>
> 이 저장소의 기본 `00-daily-analysis.yml`은 고정된 Secret / Variable 이름만 export합니다. `STOCK_GROUP_1`, `EMAIL_GROUP_1` 같은 임의 번호 env var는 job에 자동 주입되지 않으므로, 자신의 fork에서 workflow의 `env:` 매핑을 명시적으로 확장하지 않는 한 stock workflow에서 grouped email routing을 사용할 수 없습니다. Actions는 이제 `CUSTOM_WEBHOOK_BODY_TEMPLATE`, `WEBHOOK_VERIFY_SSL`, `FEISHU_WEBHOOK_SECRET`, `FEISHU_WEBHOOK_KEYWORD`, `PUSHPLUS_TOPIC`, `NTFY_URL`, `NTFY_TOKEN`, `GOTIFY_URL`, `GOTIFY_TOKEN`, P3 notification route keys, P4 notification noise-control keys를 매핑합니다. `MARKDOWN_TO_IMAGE_CHANNELS`와 `MERGE_EMAIL_NOTIFICATION`은 기본 workflow mapping 밖의 동작 toggle로 남습니다.

#### Push 동작 설정

| Secret 이름 | 설명 | 필수 여부 |
|------------|------|:----:|
| `SINGLE_STOCK_NOTIFY` | 단일 종목 push 모드. `true`로 설정하면 각 종목 분석 직후 push | 선택 |
| `REPORT_TYPE` | 리포트 유형: `simple`(간결), `full`(전체), `brief`(3-5문장), Docker 권장: `full` | 선택 |
| `REPORT_LANGUAGE` | 리포트 출력 언어: `zh`(기본 중국어) / `en`(영어). prompt instructions, templates, notification fallback, Web report view의 고정 문구도 함께 업데이트합니다. 번들 `00-daily-analysis.yml`은 이미 이 변수를 매핑하므로 Actions Secrets/Variables에 설정하면 바로 동작합니다. | 선택 |
| `REPORT_SHOW_LLM_MODEL` | 알림 리포트 footer에 분석에 사용된 LLM model을 표시할지 여부. 기본값은 `true`; runtime model metadata를 숨기려면 `false`로 설정합니다. 이 switch는 표시만 바꾸며 provider/model/Base URL, LiteLLM routing, runtime model save/migration/cleanup 동작은 변경하지 않습니다. | 선택 |
| `REPORT_TEMPLATES_DIR` | Jinja2 template directory(프로젝트 루트 기준 상대 경로, 기본값 `templates`) | 선택 |
| `REPORT_RENDERER_ENABLED` | Jinja2 template rendering 활성화(default `false`, zero regression) | 선택 |
| `REPORT_INTEGRITY_ENABLED` | report integrity check 활성화, 누락 field에 retry 또는 placeholder(default `true`) | 선택 |
| `REPORT_INTEGRITY_RETRY` | integrity retry 횟수(default `1`, `0` = placeholder only) | 선택 |
| `REPORT_HISTORY_COMPARE_N` | history signal 비교 개수. `0`이면 off(default), `>0`이면 enable | 선택 |
| `ANALYSIS_DELAY` | API rate limit을 피하기 위한 종목 분석과 시장 리뷰 사이 지연(초). 예: `10` | 선택 |
| `SAVE_CONTEXT_SNAPSHOT` | analysis-history `context_snapshot`을 저장할지 여부. 기본값 `true`. 전체 snapshot 저장을 중단하려면 `false` 또는 `--no-context-snapshot` 사용 | 선택 |
| `NOTIFICATION_REPORT_CHANNELS` | 단일 종목, 집계 daily, market review, merged push, Feishu document success 알림의 report route channels. 비어 있으면 설정된 모든 채널 | 선택 |
| `NOTIFICATION_ALERT_CHANNELS` | EventMonitor 알림용 alert route channels. 비어 있으면 설정된 모든 채널 | 선택 |
| `NOTIFICATION_SYSTEM_ERROR_CHANNELS` | 예약된 system_error route channels. P3에서는 자동 system error producer를 추가하지 않습니다. 비어 있으면 설정된 모든 채널 | 선택 |
| `NOTIFICATION_DEDUP_TTL_SECONDS` | Dedup TTL(초). `0`이면 dedup 비활성화. 같은 stable dedup key는 TTL 안에서 한 번만 전송 | 선택 |
| `NOTIFICATION_COOLDOWN_SECONDS` | Cooldown window(초). `0`이면 cooldown 비활성화. 같은 cooldown key는 window 안에서 rate-limit | 선택 |
| `NOTIFICATION_QUIET_HOURS` | `HH:MM-HH:MM` 형식의 quiet-hours window. 자정 넘김 범위 지원. 비어 있으면 비활성화 | 선택 |
| `NOTIFICATION_TIMEZONE` | quiet hours용 IANA timezone. 예: `Asia/Shanghai`. 비어 있으면 `TZ` 또는 로컬 시스템 timezone 사용 | 선택 |
| `NOTIFICATION_MIN_SEVERITY` | 최소 severity: `info`, `warning`, `error`, `critical`. 비어 있으면 현재 동작 유지 | 선택 |
| `NOTIFICATION_DAILY_DIGEST_ENABLED` | 예약된 daily digest flag. 현재 구현은 digest를 전송하거나 저장하지 않습니다. | 선택 |

> 호환성 참고: `REPORT_SHOW_LLM_MODEL`은 이전 기본 표시 동작(`true`)을 유지하며 report footer rendering만 변경합니다. provider/model/Base URL, LiteLLM routing, runtime model persistence/migration/cleanup semantics는 변경하지 않습니다. 롤백은 변수를 제거하거나 `true`로 되돌리면 됩니다.

> `REPORT_LANGUAGE`는 report text와 report page fixed copy에만 영향을 줍니다. Web UI chrome language(navigation, login, settings, shell labels, shared controls)는 의도적으로 독립적이며 browser `localStorage`의 `dsa.uiLanguage`에 저장됩니다.
> UI language resolution은 explicit localStorage value(`zh` 또는 `en`) -> browser language(`navigator.languages` / `navigator.language`) -> default `zh`입니다.

#### 기타 설정

| Secret 이름 | 설명 | 필수 여부 |
|------------|------|:----:|
| `STOCK_LIST` | 관심 종목 코드. 예: `600519,300750,002594,7203.T,005930.KS` | ✅ |
| `ANSPIRE_API_KEYS` | [Anspire AI Search](https://aisearch.anspire.cn/) 중국어 콘텐츠 최적화. 같은 키를 Anspire LLM fallback 시나리오에도 사용할 수 있습니다(예시 모델: `Doubao-Seed-2.0-lite`). | 권장 |
| `SERPAPI_API_KEYS` | [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis) 실시간 금융 뉴스용 검색엔진 결과 | 권장 |
| `TAVILY_API_KEYS` | [Tavily](https://tavily.com/) Search API(뉴스 검색용) | 선택 |
| `NAVER_CLIENT_ID` / `NAVER_CLIENT_SECRET` | [Naver Search](https://developers.naver.com/docs/serviceapi/search/news/news.md) 한국 `.KS`/`.KQ` 종목 뉴스 우선 검색. 두 값을 함께 설정해야 합니다. | 선택 |
| `BOCHA_API_KEYS` | [Bocha Search](https://open.bocha.cn/) Web Search API(중국어 검색 최적화, AI summary 지원, 여러 키 쉼표 구분) | 선택 |
| `BRAVE_API_KEYS` | [Brave Search](https://brave.com/search/api/) API(privacy-first, 미국 주식 뉴스 보강, 여러 키 쉼표 구분) | 선택 |
| `MINIMAX_API_KEYS` | [MiniMax](https://platform.minimax.io/) Coding Plan Web Search(구조화된 검색 결과) | 선택 |
| `SEARXNG_BASE_URLS` | SearXNG self-hosted instances(할당량 없는 fallback, settings.yml에서 format: json 활성화). 비어 있으면 app이 public instances를 auto-discover | 선택 |
| `SEARXNG_PUBLIC_INSTANCES_ENABLED` | `SEARXNG_BASE_URLS`가 비어 있을 때 `searx.space`에서 public SearXNG instances auto-discover(default `true`) | 선택 |
| `TUSHARE_TOKEN` | [Tushare Pro](https://tushare.pro/weborder/#/login?reg=834638) Token | 선택 |
| `TICKFLOW_API_KEY` | CN market review index enhancement용 [TickFlow](https://tickflow.org) API key. plan이 universe queries를 지원할 때 market breadth도 TickFlow를 사용합니다. | 선택 |

#### ✅ 최소 설정 예시

빠르게 시작하려면 최소한 다음이 필요합니다.

1. **AI Model**: `ANSPIRE_API_KEYS`(LLM과 search용 원키), `AIHUBMIX_KEY`(여러 모델 계열용 원키), `GEMINI_API_KEY`, 또는 `OPENAI_API_KEY`
2. **Notification Channel**: 최소 하나. 예: `WECHAT_WEBHOOK_URL` 또는 `EMAIL_SENDER` + `EMAIL_PASSWORD`
3. **Stock List**: `STOCK_LIST`(필수)
4. **Search API**: `ANSPIRE_API_KEYS` 또는 `SERPAPI_API_KEYS`(뉴스와 감성 검색에 권장)

> 이 4가지를 설정하면 바로 시작할 수 있습니다.

### 3. Actions 활성화

1. Fork한 저장소로 이동
2. 위쪽의 `Actions` 탭 클릭
3. 메시지가 표시되면 `I understand my workflows, go ahead and enable them` 클릭

### 4. 수동 테스트

1. `Actions` 탭으로 이동
2. 왼쪽에서 `Daily Stock Analysis` workflow 선택
3. 오른쪽의 `Run workflow` 버튼 클릭
4. 실행 모드 선택
5. 초록색 `Run workflow`를 클릭해 확인

### 5. 완료

기본 스케줄: 매주 평일 **18:00(베이징 시간)** 자동 실행.

---

## 전체 환경 변수 목록

### AI 모델 설정

> 전체 상세 내용: [LLM 설정 가이드](LLM_CONFIG_GUIDE_KO.md)(3단계 설정, channels, Vision, Agent, 문제 해결).
> Issue #1306 호환성 참고: 이 변경은 기존 market-review 출력을 history path를 통해 저장하고 노출할 뿐이며, model name, provider, base URL, LiteLLM cleanup rules, `.env` runtime migration semantics를 변경하지 않습니다. 롤백은 이 change set을 revert하는 것입니다. Runtime compatibility references는 `requirements.txt`(`litellm` constraints), `docs/LLM_CONFIG_GUIDE_KO.md`, `tests/test_analysis_api_contract.py`, `tests/test_analysis_history.py`, `tests/test_market_review.py`의 regression tests입니다. 공식 참고: [LiteLLM OpenAI-compatible](https://docs.litellm.ai/docs/providers/openai_compatible), [OpenAI Chat Completion API](https://platform.openai.com/docs/api-reference/chat).

| 변수 | 설명 | 기본값 | 필수 |
|--------|------|--------|:----:|
| `GENERATION_BACKEND` | 일반 분석용 generation backend. `litellm` 또는 명시적 opt-in `codex_cli`(experimental/limited) 지원 | `litellm` | No |
| `GENERATION_FALLBACK_BACKEND` | Backend-level fallback. 미설정 시 `litellm`; 빈 값은 fallback 비활성화; 자기 자신 fallback은 no-op | `litellm` | No |
| `GENERATION_BACKEND_TIMEOUT_SECONDS` | 호출별 generation backend timeout(초), 주로 local CLI backend용. 범위 `1-3600` | `300` | No |
| `GENERATION_BACKEND_MAX_OUTPUT_BYTES` | local CLI backend 1회 호출의 diagnostic stdout/stderr와 final-response 전체 크기 제한. `--output-last-message`로 stdout에 중복 출력된 final response는 두 번 계산하지 않음. 범위 `1-33554432` | `1048576` | No |
| `GENERATION_BACKEND_MAX_CONCURRENCY` | 전역 generation backend concurrency cap. 범위 `1-16`; LiteLLM Router 또는 `MAX_WORKERS` 동작을 변경하지 않음 | `1` | No |
| `LOCAL_CLI_BACKEND_MAX_CONCURRENCY` | Local CLI backend concurrency cap. 범위 `1-4`; effective concurrency는 이 값과 `GENERATION_BACKEND_MAX_CONCURRENCY` 중 더 낮은 값 | `1` | No |
| `AGENT_GENERATION_BACKEND` | Agent Chat generation backend. Web settings는 `auto|litellm`만 노출. 손으로 쓴 `codex_cli`는 unsupported tool-calling diagnostic 반환 | `auto` | No |
| `LITELLM_MODEL` | primary model, 형식 `provider/model`(예: `gemini/gemini-3.1-pro-preview`), 권장 | - | No |
| `AGENT_LITELLM_MODEL` | 선택적 Agent-only primary model. 비어 있으면 primary model 상속, bare name은 `openai/<model>`로 normalize | - | No |
| `LITELLM_FALLBACK_MODELS` | fallback models, 쉼표 구분 | - | No |
| `LLM_CHANNELS` | Channel names(쉼표 구분). `LLM_{NAME}_*`와 함께 사용. [LLM 설정 가이드](LLM_CONFIG_GUIDE_KO.md) 참고 | - | No |
| `LITELLM_CONFIG` | 고급 model routing YAML path(전문가용) | - | No |
| `LLM_USAGE_HMAC_SECRET` | LLM usage telemetry message HMAC용 secret. 비워두면 생성된 local data-dir secret file 사용 | - | No |
| `LLM_USAGE_HMAC_KEY_VERSION` | LLM usage HMAC key 버전 label. secret rotate 시 업데이트 | `local-v1` | No |
| `ANSPIRE_API_KEYS` | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC) API key, LLM gateway와 search용 원키 | - | Optional |
| `AIHUBMIX_KEY` | [AIHubMix](https://aihubmix.com/?aff=CfMq) API key, 여러 모델 계열용 원키 | - | Optional |
| `GEMINI_API_KEY` | Google Gemini API Key | - | Optional |
| `GEMINI_MODEL` | primary model name(legacy, `LITELLM_MODEL` 권장) | `gemini-3.1-pro-preview` | No |
| `GEMINI_MODEL_FALLBACK` | fallback model(legacy) | `gemini-3-flash-preview` | No |
| `ANTHROPIC_API_KEY` | Anthropic Claude API Key | - | Optional |
| `OPENAI_API_KEY` | OpenAI-compatible API Key | - | Optional |
| `OPENAI_BASE_URL` | OpenAI-compatible API endpoint | - | Optional |
| `OLLAMA_API_BASE` | Ollama local service address(예: `http://localhost:11434`), [LLM 설정 가이드](LLM_CONFIG_GUIDE_KO.md) 참고 | - | Optional |
| `OPENAI_MODEL` | OpenAI model name(legacy) | `gpt-5.5` | Optional |

> GitHub Actions 참고: 번들 `00-daily-analysis.yml`은 `GENERATION_FALLBACK_BACKEND`가 설정되지 않았을 때 명시적으로 `litellm`을 사용하므로, 미설정 Secret/Variable이 backend fallback을 비활성화하는 빈 값으로 export되지 않습니다. Actions에서 backend fallback을 끄려면 fallback을 primary backend와 같게 설정하고 resolver가 self no-op으로 처리하게 하세요.

> *참고: `ANSPIRE_API_KEYS`, `AIHUBMIX_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `OLLAMA_API_BASE`, `LLM_CHANNELS` / `LITELLM_CONFIG` 중 최소 하나를 설정하세요. `ANSPIRE_API_KEYS`와 `AIHUBMIX_KEY`는 `OPENAI_BASE_URL` 없이도 자동 적응됩니다.

### 알림 채널 설정

알림 baseline, diagnostics, deployment notes는 [알림 가이드](notifications.md)를 참고하세요.

| 변수 | 설명 | 필수 |
|--------|------|:----:|
| `WECHAT_WEBHOOK_URL` | WeChat Work Bot Webhook URL | Optional |
| `FEISHU_WEBHOOK_URL` | Feishu Bot Webhook URL | Optional |
| `FEISHU_WEBHOOK_SECRET` | Feishu bot signing secret(Signature security가 활성화된 webhook bot에만 필요) | Optional |
| `FEISHU_WEBHOOK_KEYWORD` | Feishu bot keyword(Keyword security가 활성화된 webhook bot에만 필요) | Optional |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | Optional |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | Optional |
| `TELEGRAM_MESSAGE_THREAD_ID` | Telegram Topic ID | Optional |
| `DISCORD_WEBHOOK_URL` | Discord Webhook URL | Optional |
| `DISCORD_BOT_TOKEN` | Discord Bot Token(Webhook과 둘 중 하나 선택) | Optional |
| `DISCORD_MAIN_CHANNEL_ID` | Discord Channel ID(Bot 사용 시 필요) | Optional |
| `DISCORD_INTERACTIONS_PUBLIC_KEY` | Discord Public Key(인바운드 Interaction/Webhook 서명 검증에만 필요) | Optional |
| `DISCORD_MAX_WORDS` | Discord Word Limit(업그레이드되지 않은 서버 기본값 2000) | Optional |
| `SLACK_BOT_TOKEN` | Slack Bot Token(권장, 이미지 업로드 지원. Webhook과 함께 설정되면 우선) | Optional |
| `SLACK_CHANNEL_ID` | Slack Channel ID(Bot 사용 시 필요) | Optional |
| `SLACK_WEBHOOK_URL` | Slack Incoming Webhook URL(텍스트 전용, 이미지 미지원) | Optional |
| `EMAIL_SENDER` | 발신 이메일 | Optional |
| `EMAIL_PASSWORD` | 이메일 authorization code(로그인 비밀번호 아님) | Optional |
| `EMAIL_RECEIVERS` | 수신 이메일(쉼표 구분, 비워두면 자신에게 전송) | Optional |
| `EMAIL_SENDER_NAME` | 발신자 표시 이름 | Optional |
| `STOCK_GROUP_N` / `EMAIL_GROUP_N` | 이메일 라우팅 그룹(Issue #268): `STOCK_GROUP_N`은 `STOCK_LIST` 안에 있어야 하며 이메일 수신자만 변경 | Optional |
| `CUSTOM_WEBHOOK_URLS` | Custom Webhook(쉼표 구분) | Optional |
| `CUSTOM_WEBHOOK_BEARER_TOKEN` | Custom Webhook Bearer Token | Optional |
| `WEBHOOK_VERIFY_SSL` | 이 설정을 읽는 webhook-style 알림 요청의 HTTPS 인증서 검증(default true). self-signed cert에는 false 가능. 경고: 비활성화는 심각한 보안 위험 | Optional |
| `PUSHOVER_USER_KEY` | Pushover User Key | Optional |
| `PUSHOVER_API_TOKEN` | Pushover API Token | Optional |
| `NTFY_URL` | 전체 ntfy topic endpoint. topic path 포함 필요. 예: `https://ntfy.sh/my-topic` | Optional |
| `NTFY_TOKEN` | 선택적 ntfy Bearer Token | Optional |
| `GOTIFY_URL` | Gotify server base URL, `/message` 제외 | Optional |
| `GOTIFY_TOKEN` | `X-Gotify-Key`로 전송되는 Gotify application token | Optional |
| `PUSHPLUS_TOKEN` | PushPlus Token(중국 push 서비스) | Optional |
| `SERVERCHAN3_SENDKEY` | ServerChan v3 Sendkey | Optional |
| `ASTRBOT_URL` | AstrBot Webhook URL | Optional |
| `ASTRBOT_TOKEN` | 선택적 AstrBot Bearer Token | Optional |
| `NOTIFICATION_REPORT_CHANNELS` | report route channels, 쉼표 구분. 허용값: wechat,feishu,telegram,email,pushover,ntfy,gotify,pushplus,serverchan3,custom,discord,slack,astrbot | Optional |
| `NOTIFICATION_ALERT_CHANNELS` | alert route channels, 쉼표 구분. 비어 있으면 설정된 모든 채널 유지 | Optional |
| `NOTIFICATION_SYSTEM_ERROR_CHANNELS` | 예약된 system_error route channels, 쉼표 구분. 비어 있으면 설정된 모든 채널 유지 | Optional |
| `NOTIFICATION_DEDUP_TTL_SECONDS` | Dedup TTL(초). `0`은 dedup 비활성화 | Optional |
| `NOTIFICATION_COOLDOWN_SECONDS` | Cooldown window(초). `0`은 cooldown 비활성화 | Optional |
| `NOTIFICATION_QUIET_HOURS` | `HH:MM-HH:MM` 형식의 quiet-hours window, 자정 넘김 범위 지원 | Optional |
| `NOTIFICATION_TIMEZONE` | quiet-hours timezone. 예: `Asia/Shanghai`; 비어 있으면 `TZ` 또는 local system timezone 사용 | Optional |
| `NOTIFICATION_MIN_SEVERITY` | 최소 severity: info, warning, error, critical. 비어 있으면 현재 동작 유지 | Optional |
| `NOTIFICATION_DAILY_DIGEST_ENABLED` | 예약된 daily digest flag. 아직 digest를 보내지 않음 | Optional |

> 참고: 기본 `00-daily-analysis.yml` GitHub Actions workflow는 고정 변수명만 매핑합니다. `STOCK_GROUP_N` / `EMAIL_GROUP_N` 같은 임의 번호 변수는 자동 import하지 않습니다. 따라서 이 기능은 local `.env`, Docker 또는 해당 변수를 명시적으로 주입하는 런타임에서만 작동합니다.

#### Feishu Cloud Document 설정(선택, 메시지 잘림 문제 해결)

| 변수 | 설명 | 필수 |
|--------|------|:----:|
| `FEISHU_APP_ID` | Feishu App ID | Optional |
| `FEISHU_APP_SECRET` | Feishu App Secret | Optional |
| `FEISHU_FOLDER_TOKEN` | Feishu Cloud Drive Folder Token | Optional |

> Feishu Cloud Document 설정 단계:
> 1. [Feishu Developer Console](https://open.feishu.cn/app)에서 app 생성
> 2. GitHub Secrets 설정
> 3. group 생성 후 app bot 추가
> 4. cloud drive folder에 해당 group을 collaborator로 추가(manage 권한)
>
> 참고: `FEISHU_APP_ID` / `FEISHU_APP_SECRET`은 Feishu app mode, cloud documents, Stream Bot mode용입니다. 이것만으로 group webhook notification이 활성화되지 않습니다. 단순 group push notification은 `FEISHU_WEBHOOK_URL`을 먼저 사용하세요.
>
> 보충: `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, `FEISHU_CHAT_ID`가 모두 설정되면 group webhook에 의존하지 않고 Feishu App Bot active notification channel을 활성화합니다. `FEISHU_RECEIVE_ID_TYPE` 기본값은 `chat_id`이며 P2P delivery에는 `open_id`로 설정하세요. 이는 group webhook path와 독립적인 Feishu OpenAPI Bot session route를 사용합니다.

### 검색 서비스 설정

| 변수 | 설명 | 필수 |
|--------|------|:----:|
| `ANSPIRE_API_KEYS` | Anspire Open API Key(search 및 LLM fallback 예시와 공유. 사용 가능 여부는 account/model entitlement에 따라 달라지며 A주 분석을 실질적으로 강화할 수 있음) | 권장 |
| `SERPAPI_API_KEYS` | 실시간 금융 뉴스용 SerpAPI 검색엔진 결과 | 권장 |
| `TAVILY_API_KEYS` | Tavily Search API Key | 선택 |
| `NAVER_CLIENT_ID` / `NAVER_CLIENT_SECRET` | 한국 `.KS`/`.KQ` 종목 뉴스 우선 검색용 Naver Search Client ID/Secret | 선택 |
| `BOCHA_API_KEYS` | Bocha Search API Key(중국어 최적화) | 선택 |
| `BRAVE_API_KEYS` | Brave Search API Key(미국 주식 최적화) | 선택 |
| `MINIMAX_API_KEYS` | MiniMax Coding Plan Web Search(구조화 결과) | 선택 |
| `SOCIAL_SENTIMENT_API_KEY` | Stock Sentiment API Key(Reddit / X / Polymarket, 미국 주식 선택 사항) | 선택 |
| `SOCIAL_SENTIMENT_API_URL` | Stock Sentiment API endpoint(기본값 `https://api.adanos.org`) | 선택 |
| `SEARXNG_BASE_URLS` | SearXNG self-hosted instances(할당량 없는 fallback, settings.yml에서 format: json 활성화). 비어 있으면 app이 public instances를 auto-discover | 선택 |
| `SEARXNG_PUBLIC_INSTANCES_ENABLED` | `SEARXNG_BASE_URLS`가 비어 있을 때 `searx.space`에서 public SearXNG instances auto-discover(default `true`) | 선택 |

> 동작 참고: Search와 social sentiment는 선택적 enhancement service입니다. 둘 중 하나가 초기화에 실패해도 시스템은 warning을 log하고 core analysis flow를 막지 않고 해당 stage를 건너뛰며 graceful degrade합니다.

### 데이터 소스 설정

| 변수 | 설명 | 기본값 | 필수 |
|--------|------|--------|:----:|
| `TUSHARE_TOKEN` | Tushare Pro Token | - | 선택 |
| `TICKFLOW_API_KEY` | TickFlow API key. CN market review indices는 설정 시 TickFlow를 우선하며, market breadth는 plan이 universe queries를 지원할 때만 사용 | - | 선택 |
| `ENABLE_REALTIME_QUOTE` | 실시간 시세 활성화(비활성화 시 분석에 과거 종가 사용) | `true` | 선택 |
| `ENABLE_REALTIME_TECHNICAL_INDICATORS` | Intraday realtime technicals: 활성화 시 real-time prices로 MA5/MA10/MA20 및 bull trend 계산(Issue #234). 비활성화 시 전일 종가 사용 | `true` | 선택 |
| `ENABLE_CHIP_DISTRIBUTION` | chip distribution analysis 활성화(API가 불안정하므로 cloud deployment에서는 비활성화 권장). GitHub Actions 사용자는 활성화하려면 Repository Variables에 `ENABLE_CHIP_DISTRIBUTION=true` 설정 필요. workflows에서는 기본 비활성화 | `true` | 선택 |
| `ENABLE_EASTMONEY_PATCH` | Eastmoney API patch. Eastmoney API가 자주 실패할 때(RemoteDisconnected, connection closed 등) `true` 권장. NID token과 random User-Agent를 주입해 rate limit 가능성을 낮춤 | `false` | 선택 |
| `REALTIME_SOURCE_PRIORITY` | 실시간 시세 source priority(쉼표 구분). 예: `tencent,akshare_sina,efinance,akshare_em` | .env.example 참고 | 선택 |
| `ENABLE_FUNDAMENTAL_PIPELINE` | fundamental aggregation master switch. 비활성화 시 원래 analysis pipeline을 바꾸지 않고 `not_supported` block만 반환 | `true` | 선택 |
| `FUNDAMENTAL_STAGE_TIMEOUT_SECONDS` | fundamental stage 전체 latency budget(초) | `8.0` | 선택 |
| `FUNDAMENTAL_FETCH_TIMEOUT_SECONDS` | 단일 capability source call timeout(초) | `3.0` | 선택 |
| `FUNDAMENTAL_RETRY_MAX` | fundamental capabilities retry count(첫 시도 포함) | `1` | 선택 |
| `FUNDAMENTAL_CACHE_TTL_SECONDS` | fundamental aggregation cache TTL(초). 짧은 cache로 반복 API pull 감소 | `120` | 선택 |
| `FUNDAMENTAL_CACHE_MAX_ENTRIES` | fundamental cache 최대 entry 수(TTL 안에서 시간 기준 eviction) | `256` | 선택 |

> **동작 참고:**
> - **A주**: `valuation/growth/earnings/institution/capital_flow/dragon_tiger/boards`별 aggregated capabilities 반환.
> - **ETF**: 사용 가능한 항목을 반환하고 누락 capability는 `not_supported`로 표시하며 전체 original flow에는 영향을 주지 않습니다.
> - **미국/HK 주식**: yfinance adapter를 통해 `valuation/growth/earnings/belong_boards`(`info.sector`/`info.industry` 기반)를 반환합니다. 오늘 기준 offshore data feed가 없으므로 `institution/capital_flow/dragon_tiger/boards`는 `not_supported`로 유지됩니다. yfinance가 없거나 empty payload를 반환하면 전체 `not_supported` block으로 fallback합니다. 여전히 fail-open입니다.
> - **일본/한국 주식**: 현재 MVP는 Yfinance daily/basic quote coverage만 사용합니다. `institution`, `capital_flow`, `dragon_tiger`, `boards`는 완전 지원되지 않으며 `not_supported`로 degrade됩니다([시장 경계](market-support.md) 참고).
> - 모든 예외는 fail-open logic을 사용하며, main technical/news/chip pipeline에 영향을 주지 않고 오류만 log합니다.
> - **Field contracts**:
>   - `fundamental_context.belong_boards` = 종목 관련 board list. A주는 AkShare board membership, 미국/HK는 yfinance `info.sector`/`info.industry`에서 가져오며 unavailable이면 `[]`;
>   - `fundamental_context.boards.data` = `sector_rankings`(섹터 등락 leaderboard, 구조 `{top, bottom}`; 현재 미국/HK에는 제공되지 않음);
>   - `fundamental_context.concept_boards.data` = `concept_rankings`(concept/theme 등락 leaderboard, 구조 `{top, bottom}`; 현재 A주 전용이며 fail-open 시 omitted 또는 empty);
>   - `fundamental_context.earnings.data.financial_report.currency` = 재무제표 통화(`info.financialCurrency`; HK ADRs는 여기서 CNY를 보고하는 경우가 흔함);
>   - `fundamental_context.earnings.data.dividend.currency` = 거래 / 배당 통화(`info.currency`; HK ADRs는 statement currency가 CNY여도 여기서는 HKD 사용). renderer는 단일 global currency를 가정하지 않고 각 block의 자체 currency를 읽습니다;
>   - `fundamental_context.earnings.data.dividend.ttm_dividend_yield_pct` = `ttm_cash_dividend_per_share / latest_price * 100`, 양쪽 모두 trading currency 기준. TTM cash 또는 latest price가 없을 때만 `info.trailingAnnualDividendYield`(decimal) 또는 `info.dividendYield`(이미 percent인 값 passthrough)로 fallback;
>   - `get_stock_info.belong_boards` = 개별 종목이 속한 sector 목록;
>   - `get_stock_info.boards`는 compatibility alias이며 값은 `belong_boards`와 동일(제거는 major version update에서만 고려);
>   - `get_stock_info.sector_rankings`는 `fundamental_context.boards.data`와 일관성을 유지합니다.
>   - `AnalysisReport.details.belong_boards` = structured report details의 관련 board list;
>   - `AnalysisReport.details.sector_rankings` = board-linkage display용 structured report details의 sector leaderboard.
>   - `AnalysisReport.details.concept_rankings` = Web related-board signal matching과 notification table type label용 structured report details의 concept/theme leaderboard.
> - **Sector leaderboard**는 고정 fallback order를 사용합니다. global priority와 일치합니다.
> - **Timeout control**은 `best-effort` soft timeout입니다. stage는 budget에 따라 빠르게 degrade하고 실행을 계속하지만, underlying third-party network call의 hard interrupt를 보장하지 않습니다.
> - `FUNDAMENTAL_STAGE_TIMEOUT_SECONDS=8.0`은 새로 추가된 fundamental stage의 target budget을 의미하며 엄격한 hard SLA가 아닙니다. Windows, Docker 또는 rate-limited free data source에서는 `12-15s`로 올릴 수 있습니다.
> - hard SLA가 필요하면 향후 버전에서 isolated child process execution으로 upgrade해 timeout task를 강제 종료해야 합니다.

### 기타 설정

| 변수 | 설명 | 기본값 |
|--------|------|--------|
| `STOCK_LIST` | 관심 종목 코드(쉼표 구분) | - |
| `MAX_WORKERS` | 동시 thread 수 | `3` |
| `MARKET_REVIEW_ENABLED` | 시장 리뷰 활성화 | `true` |
| `DAILY_MARKET_CONTEXT_ENABLED` | 일일 시장 context를 stock-analysis prompt에 주입하고 high-risk/risk-off market에서 aggressive buy advice를 완화. 기본 활성화이며, 이 값이 `false`여도 market review는 실행 가능 | `true` |
| `MARKET_REVIEW_REGION` | market review region: cn(A주), hk(HK stocks), us(US stocks), both(세 시장 모두) | `cn` |
| `MARKET_REVIEW_COLOR_SCHEME` | market review의 index change color style: `green_up` = 상승 초록/하락 빨강(default), `red_up` = 상승 빨강/하락 초록 | `green_up` |
| `SCHEDULE_ENABLED` | scheduled tasks 활성화 | `false` |
| `SCHEDULE_TIME` | scheduled execution time | `18:00` |
| `SCHEDULE_TIMES` | 여러 scheduled execution times, 쉼표 구분. 비어 있으면 `SCHEDULE_TIME`으로 fallback | empty |
| `SCHEDULE_RUN_IMMEDIATELY` | scheduler mode 시작 시 즉시 1회 실행. unset이면 legacy `RUN_IMMEDIATELY` runtime override를 계속 따름 | `true` |
| `RUN_IMMEDIATELY` | non-scheduler startup에서 즉시 1회 실행. `SCHEDULE_RUN_IMMEDIATELY`가 unset일 때 legacy fallback으로도 작동 | `true` |
| `LOG_DIR` | 로그 디렉터리 | `./logs` |
| `SAVE_CONTEXT_SNAPSHOT` | analysis-history `context_snapshot` 저장. false이면 새 history record는 enhanced_context, market_phase_summary, AnalysisContextPack overview, diagnostic snapshots를 저장하지 않지만 current-run prompt summaries는 활성 유지 | `true` |

> 동작 참고:
> - `TICKFLOW_API_KEY`가 설정되면 CN market review는 main indices에 TickFlow를 먼저 시도합니다. Market breadth도 현재 TickFlow plan이 universe queries를 지원할 때만 TickFlow를 시도합니다.
> - TickFlow 동작은 key 기반만이 아니라 capability 기반입니다. 제한된 plan도 main CN indices는 강화할 수 있고, `CN_Equity_A` universe query 지원 plan은 market breadth도 강화합니다.
> - 공식 quickstart는 `quotes.get(universes=["CN_Equity_A"])`를 문서화하지만, online smoke test에서 두 가지 real-world constraint가 추가로 확인되었습니다. universe access는 plan 권한에 의존하고, `quotes.get(symbols=[...])`에는 per-request symbol limit이 있습니다.
> - TickFlow는 현재 `change_pct` / `amplitude`를 ratio value로 반환합니다. 이 integration은 AkShare / Tushare / efinance semantics와 맞도록 프로젝트의 percent convention으로 normalize합니다.
> - scheduler mode에서 runtime env가 `RUN_IMMEDIATELY`를 명시하지만 `SCHEDULE_RUN_IMMEDIATELY`를 설정하지 않으면, scheduler는 persisted `.env` alias 값으로 되돌리지 않고 legacy runtime override를 계속 상속합니다.
> - CN market review report는 이제 market signal, index detail, sector Top tables, news catalysts, next-session plan, risk sections를 포함한 post-market workstation layout을 사용합니다. market signal은 terminal과 notification client 전반에서 일관되게 렌더링되도록 block bar 대신 `66/100 (constructive, risk-on)` 같은 plain-text score를 사용합니다. News catalysts는 mixed-language noise를 줄이기 위해 search snippet 대신 headline, source, link만 나열합니다. 누락 data source는 영향을 받는 block만 생략하거나 단순화하는 방식으로 degrade됩니다.
> - Per-stock analysis, realtime quote priority, sector rankings fallback은 변경되지 않았습니다.

---

## Docker 배포

이미지는 런타임에 `/app/static` 아래 prebuilt frontend assets를 사용하므로, 실행 중인 `server` 컨테이너에는 `apps/dsa-web` source tree나 runtime `npm`이 필요 없습니다. Docker 배포 후 WebUI가 열리지 않으면 먼저 컨테이너 내부에 `/app/static/index.html`이 존재하는지 확인하세요.

공식 이미지 registry:

- GHCR: `ghcr.io/zhulinsen/daily_stock_analysis:<tag>`
- Docker Hub: `<DOCKERHUB_USERNAME>/daily_stock_analysis:<tag>`(publisher의 `DOCKERHUB_USERNAME` secret으로 구동. 공식 release는 `zhulinsen/daily_stock_analysis` 사용)

### 빠른 시작

```bash
# 1. Clone repository
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 2. Configure environment variables
cp .env.example .env
vim .env  # Fill in API Keys and configuration

# 3. Start container
docker-compose -f ./docker/docker-compose.yml up -d server     # Web service mode (recommended, provides API & WebUI)
docker-compose -f ./docker/docker-compose.yml up -d analyzer   # Scheduled task mode
docker-compose -f ./docker/docker-compose.yml up -d            # Start both modes

# 4. Access WebUI
# http://localhost:8000

# 5. View logs
docker-compose -f ./docker/docker-compose.yml logs -f server
```

기본 Compose 파일은 각 서비스에 `limits.memory: 1G`, `reservations.memory: 512M`을 설정합니다. `512M`은 가벼운 Web/API 사용, 단일 종목 실행, `MAX_WORKERS=1`의 낮은 동시성에만 사용하세요. 일반 full analysis에는 `1G`, `server + analyzer` 동시 실행, 다중 종목 분석, market review, news expansion, image reports, AlphaSift에는 `2G+`를 사용하세요. `512M`로 제한된다면 두 서비스를 동시에 시작하지 말고 무거운 기능을 줄이세요.

### 공식 이미지 직접 실행

대상 머신에 source tree를 유지하고 싶지 않다면 published image를 직접 실행할 수 있습니다.

```bash
# Web/API mode
docker pull zhulinsen/daily_stock_analysis:latest
docker run -d \
  --name dsa-server \
  --env-file .env \
  -p 8000:8000 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/reports:/app/reports" \
  zhulinsen/daily_stock_analysis:latest \
  python main.py --serve-only --host 0.0.0.0 --port 8000

# Scheduled-task mode
docker run -d \
  --name dsa-analyzer \
  --env-file .env \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/reports:/app/reports" \
  zhulinsen/daily_stock_analysis:latest
```

pinned deployment 또는 쉬운 rollback을 위해 `latest` 대신 `v3.13.0` 같은 구체적 version tag를 사용하세요.

### 실행 모드 설명

| 명령 | 설명 | 포트 |
|------|------|------|
| `docker-compose -f ./docker/docker-compose.yml up -d server` | Web service mode, API & WebUI 제공 | 8000 |
| `docker-compose -f ./docker/docker-compose.yml up -d analyzer` | scheduled task mode, 매일 자동 실행 | - |
| `docker-compose -f ./docker/docker-compose.yml up -d` | 두 모드를 동시에 시작 | 8000 |

### Docker Compose 설정

`docker-compose.yml`은 YAML anchors로 설정을 재사용합니다.

```yaml
version: '3.8'

x-common: &common
  build:
    context: ..
    dockerfile: docker/Dockerfile
  restart: unless-stopped
  env_file:
    - ../.env
  environment:
    - TZ=Asia/Shanghai
  volumes:
    - ../data:/app/data
    - ../logs:/app/logs
    - ../reports:/app/reports
    - ../strategies:/app/strategies:ro
  deploy:
    resources:
      limits:
        memory: 1G
      reservations:
        memory: 512M

services:
  # Scheduled task mode
  analyzer:
    <<: *common
    container_name: stock-analyzer

  # FastAPI mode
  server:
    <<: *common
    container_name: stock-server
    command: ["python", "main.py", "--serve-only", "--host", "0.0.0.0", "--port", "${API_PORT:-8000}"]
    ports:
      - "${API_PORT:-8000}:${API_PORT:-8000}"
```

### `.env`와 Volume Mapping

`docker run`과 Compose 모두에서 startup environment injection과 runtime file writes를 분리하세요.

- Environment injection: `--env-file .env` 또는 Compose `env_file`
  이는 `.env`의 key/value pair를 컨테이너 process environment로 전달합니다.
- Runtime config writes: host `.env`를 컨테이너 `.env` path 위에 단일 파일로 bind-mount하지 마세요. Docker는 target을 mount point로 취급하므로 config save 중 사용하는 `os.replace()` atomic update가 `Device or resource busy`로 실패할 수 있습니다. fallback in-place write도 권한 문제로 실패할 수 있습니다.

기본 Compose와 `docker run` 예시는 startup config injection에만 `env_file` / `--env-file`을 사용하고, host `.env` 파일을 컨테이너에 더 이상 mount하지 않습니다. 활성 `.env` 파일에 key가 없으면 WebUI Settings page는 startup-injected process environment variables에서 같은 key를 fallback으로 표시하므로, Docker 사용자는 먼저 import하지 않아도 injected config를 볼 수 있습니다. raw `.env` export에는 여전히 활성 config file content만 포함됩니다.

WebUI에서 저장한 runtime config는 기본적으로 container-local config file에 기록되며 host `.env`에 다시 쓰는 것과 다릅니다. 컨테이너를 삭제하거나 재생성하면 startup은 여전히 주입된 `.env` 파일을 사용합니다. persistent runtime config가 필요하면 single-file `.env` bind mount 대신 `ENV_FILE`을 `/app/data/runtime.env` 같은 writable data volume file로 지정하세요. restart 시 startup `env_file`, `--env-file`, `docker run -e`, Compose `environment:`에 여전히 같은 이름의 값이 있으면 runtime file을 override할 수 있습니다. WebUI 저장 값이 적용되게 하려면 startup override를 업데이트하거나 제거하세요.

권장 host mapping:

- `./data:/app/data` runtime data 및 database files
- `./logs:/app/logs` logs
- `./reports:/app/reports` generated reports
- `./strategies:/app/strategies:ro` custom strategy YAML files

공식 Docker 이미지는 startup 중 `/app/data`, `/app/logs`, `/app/reports` mount의 ownership을 자동 생성/수정한 뒤 컨테이너 내부 non-root `dsa` user(UID/GID `1000:1000`)로 권한을 낮춥니다. 일반 Docker / Compose 배포에서는 host-side `chown` 또는 `chmod`가 필요 없습니다.

`--user` 또는 Compose `user:`로 runtime user를 override하거나, read-only mounts, rootless Docker, NFS 또는 `chown`을 막는 다른 storage environment를 사용하면 자동 repair가 적용되지 않을 수 있습니다. 이 경우 실제 runtime user가 `data`, `logs`, `reports`에 쓸 수 있는지 확인하거나 writable volumes를 사용하세요.

선택적 static asset override:

- `./static:/app/static:ro`

### 자주 쓰는 명령

```bash
# View running status
docker-compose -f ./docker/docker-compose.yml ps

# View logs
docker-compose -f ./docker/docker-compose.yml logs -f server

# Stop services
docker-compose -f ./docker/docker-compose.yml down

# Rebuild image (after code update)
docker-compose -f ./docker/docker-compose.yml build --no-cache
docker-compose -f ./docker/docker-compose.yml up -d server
```

### 수동 이미지 빌드

```bash
docker build -f docker/Dockerfile -t stock-analysis .
docker run -d \
  --name dsa-server-local \
  --env-file .env \
  -p 8000:8000 \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/logs:/app/logs" \
  -v "$(pwd)/reports:/app/reports" \
  stock-analysis \
  python main.py --serve-only --host 0.0.0.0 --port 8000
```

---

## 로컬 배포

### 의존성 설치

```bash
# Python 3.10+ recommended
pip install -r requirements.txt

# Or use conda
conda create -n stock python=3.10
conda activate stock
pip install -r requirements.txt
```

Windows PowerShell에서 Python 또는 pip가 여전히 시스템 기본 code page를 사용한다면, 첫 의존성 설치나 환경 검사 전에 UTF-8을 활성화하세요. 이렇게 하면 terminal output과 third-party tooling이 non-ASCII text에서 실패하는 일을 줄일 수 있습니다.

```powershell
$env:PYTHONUTF8='1'
$env:PYTHONIOENCODING='utf-8'
python -m pip install -r requirements.txt
python scripts/check_env.py --config
```

### 명령줄 인자

```bash
python main.py                        # Full analysis (stocks + market review)
python main.py --market-review        # Market review only
python main.py --no-market-review     # Stock analysis only
python main.py --stocks 600519,300750 # Specify stocks
python main.py --dry-run              # Fetch data only, no AI analysis
python main.py --no-notify            # Don't send notifications
python main.py --schedule             # Scheduled task mode
python main.py --debug                # Debug mode (verbose logging)
python main.py --workers 5            # Specify concurrency
```

---

## 스케줄 작업 설정

### GitHub Actions 스케줄

`.github/workflows/00-daily-analysis.yml`을 편집합니다.

```yaml
schedule:
  # UTC time, Beijing time = UTC + 8
  - cron: '0 10 * * 1-5'   # Monday to Friday 18:00 (Beijing Time)
```

자주 쓰는 시간 참고:

| 베이징 시간 | UTC cron expression |
|---------|----------------|
| 09:30 | `'30 1 * * 1-5'` |
| 12:00 | `'0 4 * * 1-5'` |
| 15:00 | `'0 7 * * 1-5'` |
| 18:00 | `'0 10 * * 1-5'` |
| 21:00 | `'0 13 * * 1-5'` |

### 로컬 스케줄 작업

```bash
# Start scheduled mode (default 18:00 execution)
python main.py --schedule

# Or use crontab
crontab -e
# Add: 0 18 * * 1-5 cd /path/to/project && python main.py
```

> 참고: scheduled mode는 매 실행 전에 저장된 `STOCK_LIST`를 reload합니다. `--stocks`도 함께 전달하더라도 이후 scheduled execution이 startup snapshot에 고정되지 않습니다. 임시 종목 목록을 분석하려면 일반 one-off run을 사용하세요.
>
> built-in scheduler가 `python main.py --schedule` 또는 동등한 CLI-only mode로 시작된 경우, WebUI에서 새 `SCHEDULE_TIME` / `SCHEDULE_TIMES`를 저장하면 프로세스를 재시작하지 않아도 다음 scheduler poll에서 daily job을 rebind합니다. 이전 trigger time은 새 값과 함께 유지되지 않고 제거됩니다. `python main.py --serve --schedule`은 Web/API runtime scheduler가 소유하므로, 장기 실행 WebUI/API/Desktop 프로세스는 `SCHEDULE_ENABLED`, `SCHEDULE_TIME`, `SCHEDULE_TIMES` 저장 후 runtime scheduler를 시작, 중지 또는 재구성합니다.
>
> Web/API runtime scheduler run-now endpoint는 이미 분석이 실행 중이 아닐 때만 요청을 받습니다. 분석 중이면 queued run을 보고하는 대신 busy response를 반환합니다.

### 시장 국면 기준선(Issue #1386 P0)

P0는 내부 market-phase inference baseline만 추가합니다. 기존 일일 장마감 리포트, 거래일 skip 동작, effective trading date resolution, API, Web, Bot, Agent, GitHub Actions 기본값은 변경하지 않습니다. phase inference는 P1+ context contract를 위한 준비입니다. `exchange-calendars`를 사용할 수 없거나 calendar lookup이 실패하면 phase는 `unknown`을 반환합니다. 기존 trading-day filter와 effective-date helper는 현재 fail-open 동작을 유지합니다.

phase label은 regular-session 상태를 설명합니다.

| Phase | 의미 |
| --- | --- |
| `premarket` | 정규장이 열리기 전. extended-hours quotes를 가져왔다는 뜻은 아님 |
| `intraday` | 정규장 중이며 lunch break 또는 near-close window 밖 |
| `lunch_break` | market calendar가 제공하는 lunch break window. lunch break가 없는 시장은 이 phase를 건너뜀 |
| `closing_auction` | near-close heuristic window: CN 3분, HK 10분, US 5분. 전체 exchange auction model은 아님 |
| `postmarket` | 정규장 종료 후. post-market quotes를 가져왔다는 뜻은 아님 |
| `non_trading` | 현재 market-local date가 trading session이 아님 |
| `unknown` | 알 수 없는 market, calendar unavailable 또는 calendar error로 phase를 신뢰성 있게 추론할 수 없음 |

현재 entrypoint 기준선:

- Regular stock analysis, Agent analysis, Web manual analysis, Bot `/analyze` / `/ask`, schedule mode, GitHub Actions는 여전히 기존 analysis path와 post-market recap wording을 사용합니다. P0는 prompt나 output schema를 자동 전환하지 않습니다.
- Market review는 계속 `MARKET_REVIEW_REGION`과 trading-day filtering을 따르며, market phase label을 소비하지 않습니다.
- Mixed-market watchlist는 symbol market별 phase를 추론해야 합니다. aggregate report에서 phase가 일관되지 않게 표시되는 문제는 P1+에 남겨둡니다.

알려진 문제 기준선:

- Intraday run이 아직 unfinished intraday data를 완성된 daily recap처럼 설명할 수 있습니다.
- Output이 current intraday observation 대신 "today's recap / watch tomorrow"에 집중할 수 있습니다.
- Quote timestamp, source, cache, stale state가 아직 phase context로 통합되지 않았습니다.
- Lunch break, near-close, forced non-trading-day run이 prompt나 report structure에 아직 명시되지 않았습니다.

P0는 이 기준선을 pipeline / Agent / API / Web / Bot에 연결하지 않고, report schema를 바꾸지 않으며, alert technical-indicator partial-bar handling을 바꾸지 않고, config key를 추가하지 않습니다.

### Runtime Market Phase Context(Issue #1386 P1a)

P1a는 regular stock-analysis pipeline, legacy Agent context, multi-agent `ctx.meta`를 통해 내부 `market_phase_context`를 구성하고 전달합니다. 이 context에는 market, phase, market-local date, effective daily-bar date, trading-day / market-open / partial-bar tristate flag, best-effort open/close minute estimate, `unknown_market`, `calendar_unavailable`, `calendar_error` 같은 degradation warning code가 포함됩니다.

P1a 자체는 prompt wording, API/Web/Bot parameters, report schemas, stable history/task-status metadata, quote freshness/data quality semantics를 변경하지 않습니다. Regular history snapshot과 Agent history snapshot은 runtime-only field를 제거합니다. P1b가 persistent metadata와 task-status display contract를 정의하도록 남겨둡니다.

### Market Phase Low-Sensitivity Metadata(Issue #1386 P1b)

P1b는 P1a runtime `market_phase_context`를 안정적인 low-sensitivity public `market_phase_summary`로 project하고, 이를 `analysis_history.context_snapshot` top level에 저장합니다. History detail, sync analysis responses, completed `/api/v1/analysis/status/{task_id}` responses는 같은 market-phase metadata를 `report.meta.market_phase_summary`에서 반환합니다. completed task status는 top-level `TaskStatus` field를 추가하지 않고 `status.result.report.meta.market_phase_summary`를 통해서만 노출합니다.

`market_phase_summary`에는 market, phase, market-local time, session date, effective daily-bar date, trading-day / market-open / partial-bar flags, open/close minute estimates, trigger source, analysis intent, warning codes만 포함됩니다. full `market_phase_context`는 노출하지 않으며 quote freshness, fallback, stale, data-quality scoring field를 추가하지 않습니다. `report.details.analysis_context_pack_overview`는 #1389 input data-block quality overview로 남습니다. API `details.context_snapshot`은 raw snapshot이 stable public field를 중복하지 않도록 top-level `market_phase_summary`와 `analysis_context_pack_overview`를 제거합니다. `SAVE_CONTEXT_SNAPSHOT=false`이면 full `analysis_history.context_snapshot`이 저장되지 않습니다. 오래된 history record에 summary가 없어도 field는 empty이고 report는 계속 로드됩니다.

P1b는 prompt를 변경하지 않고, `analysis_phase` request parameter를 추가하지 않으며, Web phase label이나 rendering을 추가하지 않습니다. pending/processing TaskPanel state, in-progress SSE events, Bot, notifications, `market_review`, P3 intraday data-quality fields도 다루지 않습니다.

### Market Phase Prompt Injection(Issue #1386 P2-min)

P2-min은 이미 `market_phase_context`를 받는 analysis path에 runtime market phase를 LLM-readable prompt section으로 렌더링하기 시작합니다. Regular analysis, single Agent, multi-agent prompt는 이제 current phase, market-local time, latest reusable complete daily-bar date, 최소 phase constraints를 볼 수 있습니다. pre-market run은 오늘의 price action을 이미 발생한 사실처럼 설명하면 안 되고, intraday / lunch-break / near-close run은 latest daily bar를 잠재적으로 unfinished로 취급해야 하며, post-market run은 complete-session recap style을 유지할 수 있고, non-trading 또는 unknown phase는 보수적으로 유지해야 합니다.

P2-min은 여전히 API/Web/Bot parameter를 추가하지 않고, phase를 history/task status/report metadata에 저장하지 않으며, report JSON schema를 변경하지 않고, full quote freshness, fallback, stale, data-quality contract를 도입하지 않습니다. P1a pipeline을 거쳐 `market_phase_context`를 만들지 않는 Bot/API direct Agent entrypoint는 이전 동작을 유지합니다. entrypoint propagation과 visible label은 이후 P4+ 작업으로 남습니다.

### Intraday Data Packet 및 Realtime Quality Control(Issue #1386 P3)

P3는 regular analysis path에 realtime quote quality metadata를 추가하지만, 여전히 `analysis_phase` parameter를 추가하거나, API/Web/Bot phase entrypoint를 변경하거나, report JSON schema를 바꾸거나, #1389 P5 data-quality scoring 또는 model confidence limit을 구현하지 않습니다. Realtime quote는 `fetched_at`, `provider_timestamp`, `is_stale`, `stale_seconds`, `fallback_from`을 포함할 수 있습니다. `fetched_at`은 system fetch time이고, `provider_timestamp`는 provider가 quote timestamp를 실제 반환할 때만 채워집니다. provider time을 사용할 수 없으면 system은 freshness를 fabrication하지 않고 `stale_seconds` / `is_stale`를 empty로 유지합니다.

Whole-source fallback semantics는 고정되어 있습니다. `source`는 실제 성공 provider token을 유지하고, `fallback_from`은 현재 시도에서 실패한 highest-priority whole source를 기록합니다. primary source가 성공하고 이후 provider가 누락 field만 보완했다면 `fallback_from`은 설정되지 않습니다. `AnalysisContextBuilder`는 upstream artifacts만 mapping하고 추가 fetch나 quality scoring을 하지 않습니다. quote block status는 `STALE > FALLBACK > AVAILABLE`로 collapse됩니다. realtime price가 `today`를 overlay하면 pipeline은 `is_partial_bar`, `is_estimated`, `estimated_fields`, `realtime_source`, quote metadata를 표시합니다. `daily_bars` block은 storage에서 complete daily-bar window를 계속 나타냅니다. partial/estimated marker는 technical block에만 들어갑니다. Freshness scoring, intraday cache TTL tiers, Agent tool-level reuse, API/Web display는 follow-up입니다.

### Analysis Phase Entrypoint 및 Task Queue Pass-Through(Issue #1386 P4a)

P4a는 `analysis_phase=auto|premarket|intraday|postmarket` request parameter를 추가하며 기본값은 `auto`입니다. API caller는 현재 분석의 phase를 명시적으로 override할 수 있습니다. 이 parameter는 `POST /api/v1/analysis/analyze`, async task queue, `AnalysisService`, regular analysis pipeline, market-phase context construction을 통해 연결됩니다. Web frontend types와 API mapping은 field를 받지만 page selector는 추가하지 않습니다. Bot, schedule, GitHub Actions, DB migration은 scope 밖입니다.

`analysis_phase`는 requested override value입니다. 최종 report phase는 여전히 `report.meta.market_phase_summary.phase`입니다. Async accepted responses, in-memory task status, task list responses, SSE payloads는 requested phase를 echo합니다. DB history fallback은 persisted phase field를 추가하지 않으므로 오래된 record는 여전히 empty를 반환할 수 있습니다. Duplicate detection은 stock-only로 남아 같은 stock을 서로 다른 phase로 제출해도 in-flight duplicate로 취급됩니다.

Market-phase context construction은 legacy internal `analysis_intent` argument도 계속 지원합니다. `analysis_phase`가 `auto`로 남아 있을 때만 non-`auto` `analysis_intent`가 이 run의 requested phase로 normalize됩니다. External caller는 `analysis_phase`를 선호해야 합니다.

`auto`는 기존 calendar inference를 보존합니다. Non-`auto` 값은 phase만 override하고 `is_trading_day`, `is_market_open_now`, `is_partial_bar`, `minutes_to_open`, `minutes_to_close`를 다시 계산합니다. override는 실제 `market_local_time`이나 `effective_daily_bar_date`를 rewrite하지 않습니다. 현재 날짜가 trading session이 아니거나 calendar가 session을 지원할 수 없으면 minute field가 empty일 수 있습니다.

### Web Phase Labels(Issue #1386 P4b)

P4b는 phase override selector를 추가하지 않고 Web visibility slice를 완성합니다. 진행 중 TaskPanel은 P4a가 echo한 requested `analysis_phase`만 표시합니다. 현재 task-panel UI에서 `auto`는 requested automatic phase(`请求阶段: 自动阶段`)로 명시 label되며 최종 inferred phase처럼 표시되지 않습니다. 최종 report page는 `report.meta.market_phase_summary.phase`의 실제 market phase를 렌더링하고, `is_partial_bar=true`일 때 `Partial bar` marker를 표시합니다.

Data-quality visibility는 계속 `report.details.analysis_context_pack_overview.data_quality`와 기존 `AnalysisContextSummary` component를 재사용합니다. Web UI는 low-sensitivity data-quality summary 옆에 phase label만 표시합니다. full `AnalysisContextPack`, prompt summary, raw payloads, stripped snapshot internals는 노출하지 않습니다. History-list fields, Bot, schedule, GitHub Actions, Desktop, notification summaries, advanced phase override UI는 follow-up입니다.

### AnalysisContextPack Prompt Summary(Issue #1389 P3)

P3는 low-sensitivity `AnalysisContextPack` summary를 regular analysis와 Agent initial prompt에 주입합니다. pipeline은 이미 fetch된 quote, daily-bar, trend, chip, fundamentals, news, market-phase artifacts에서 pack을 구성하고 `analysis_context_pack_summary`를 downstream에 전달합니다. 새 pack-summary section에서 LLM은 subject, version, data-block status/source/warnings/missing reason, news result count만 봅니다. full `news.content`, `trend_result`, chip, fundamentals raw payload는 이 section을 통해 보지 않습니다. Agent path에서는 pipeline이 history prefetch 후 `storage.get_analysis_context()`를 한 번 읽어 daily-bars status를 구동하고, 해당 read에 usable context가 없을 때만 `daily_bars_missing`을 표시합니다. 기존 `news_context`, Agent pre-fetched JSON, `enhanced_context` raw-payload channel은 pre-P3 동작을 유지하며 이 summary로 대체되거나 sanitize되지 않습니다.

P3 자체는 API/Web/Bot parameters를 추가하지 않고, history/task status/report metadata에 field를 저장하지 않으며, report JSON schema를 변경하지 않고, history, notifications, Web surface를 통해 full pack을 노출하지 않습니다. Agent tool-level reuse of pack data와 P5 data-quality scoring은 이후 phase로 남습니다.

### AnalysisContextPack Low-Sensitivity Visibility(Issue #1389 P4)

P4는 `report.details.analysis_context_pack_overview`를 추가합니다. History detail과 completed `/api/v1/analysis/status/{task_id}` responses는 persisted `context_snapshot`에서 같은 low-sensitivity overview를 읽습니다. sync analysis responses도 방금 persisted된 `analysis_history.context_snapshot`에서 overview를 추출하므로, `SAVE_CONTEXT_SNAPSHOT=false`일 때 새 record가 이 field를 보장하지 않습니다. Web report page는 Strategy와 News 뒤에 collapsed data-block summary를 렌더링하며, header에는 available/missing counts, non-zero other status counts, trigger source를 표시하고 expansion 후 data-block status, source, warnings, missing reasons, status counts, news result count를 표시합니다. API `details.context_snapshot`은 raw snapshot panel이 public overview를 중복하지 않도록 top-level `analysis_context_pack_overview`를 제거합니다.

overview에는 full pack, `analysis_context_pack_summary` prompt string, `items.value`, news body text, `trend_result`, chip, fundamentals raw payload가 포함되지 않습니다. `SAVE_CONTEXT_SNAPSHOT=false`이면 full `analysis_history.context_snapshot`이 저장되지 않으므로 새 history record는 overview를 제공할 수 없습니다. overview가 없는 오래된 record는 empty field를 계속 반환하고 report는 로드됩니다. 이 phase는 pending/processing TaskPanel, in-progress SSE events, notification summaries, Bot/Desktop-specific rendering, `market_review` overview, data-quality scoring을 다루지 않습니다.

### AnalysisContextPack Data Quality Scoring 및 Prompt Limitations(Issue #1389 P5)

P5는 `PACK_VERSION = "1.0"`을 바꾸거나 data source를 추가하거나 report JSON schema를 변경하지 않고, `AnalysisContextPack`에 lightweight data-quality scoring과 model-readable data limitations를 추가합니다. `ContextFieldStatus`에는 이제 `fetch_failed`가 포함됩니다. 이는 field 또는 data block이 이번 run에서 명시적으로 fetch 실패했음을 뜻합니다. 첫 mapping은 `fundamental_context.status == "failed"`만 `fetch_failed`로 전환하며, empty news, unconfigured search, missing realtime quote, missing chip data는 기존 `missing` / `not_supported` semantics를 유지합니다.

`DataQuality`는 기존 `warnings` / `metadata` field를 보존하면서 `overall_score`, `level`, `block_scores`, `limitations`를 포함합니다. Scoring은 `quote`, `daily_bars`, `technical`, `news`, `fundamentals`, `chip` 6개 block으로 고정됩니다. auxiliary missing block은 다시 normalize되어 사라지지 않습니다. core block이 degraded되면 prompt의 `Data Limitations` section은 model에게 high confidence를 반환하지 말라고 지시합니다. auxiliary block 누락은 해당 analysis section만 제한하며 bullish 또는 bearish로 해석하면 안 됩니다. 이 section은 `format_analysis_context_pack_prompt_section()`이 생성하므로, regular analysis, single Agent, multi-agent path는 raw payload, news body text, raw trend values, secrets, tokens, webhooks를 노출하지 않고 같은 low-sensitivity summary를 재사용합니다.

History detail, sync analysis responses, completed task status responses는 여전히 `report.details.analysis_context_pack_overview`만 노출합니다. P5는 score, level, block_scores, limitations를 포함한 nested `data_quality` object만 추가하고 `warnings`를 중복하지 않습니다. Web report page는 기본 collapsed 상태를 유지하고, header에 quality score/level을 추가하며 expansion 후 limitations와 `fetch_failed` status를 표시합니다. API `details.context_snapshot`은 계속 top-level `analysis_context_pack_overview`를 제거합니다.

### AnalysisContextPack 문서, 마이그레이션, 롤백(Issue #1389 P6)

P6는 문서와 configuration-visibility closure일 뿐입니다. pack runtime behavior를 추가하지 않고, pack enable/disable feature flag를 추가하지 않으며, `PACK_VERSION = "1.0"`을 변경하지 않고, API parameter를 추가하지 않으며, report JSON schema를 바꾸지 않고, database migration을 실행하지 않습니다. 전체 contract, field states, low-sensitivity visibility, redaction boundary, migration notes, rollback path는 [AnalysisContextPack topic 문서](analysis-context-pack.md)를 참고하세요.

`SAVE_CONTEXT_SNAPSHOT`은 기존 환경 변수입니다. P6는 이를 `.env.example`, config registry, Web settings help에만 노출합니다. 기본값은 `true`입니다. `false`로 설정하거나 CLI에서 `--no-context-snapshot`을 사용하면 새 history record는 `enhanced_context`, `market_phase_summary`, `analysis_context_pack_overview`, diagnostic snapshots, raw snapshot fields를 포함한 full `analysis_history.context_snapshot`을 더 이상 저장하지 않습니다. 이 설정은 current-run `AnalysisContextPack` construction을 비활성화하지 않고, prompt에서 low-sensitivity `analysis_context_pack_summary`를 제거하지 않으며, report JSON schema나 API request parameter를 변경하지 않습니다.

runtime pack master switch는 없습니다. P3-P5 pack prompt summary, overview, data-quality integration을 비활성화하려면 release rollback 또는 code rollback이 필요합니다. `analysis_context_pack_overview` / `data_quality`가 없는 오래된 history record는 empty field를 계속 반환하며 읽을 수 있습니다.

### Intraday Decision Guardrails 및 Quality Checks(Issue #1386 P5)

P5는 개별 종목 분석 report에 `dashboard.phase_decision` 아래 phase-aware decision block을 추가합니다. field는 `phase_context`, `action_window`, `immediate_action`, `watch_conditions`, `next_check_time`, `confidence_reason`, `data_limitations`입니다. 이는 historical `raw_result`에 저장되는 backward-compatible report JSON addition이며, `analysis_phase` API parameter를 추가하거나, Web phase entrypoint를 변경하거나, 설정을 추가하거나, 기본 post-market daily review 동작을 변경하지 않습니다.

Regular analysis와 Agent analysis는 history 저장 전에 current `market_phase_summary`와 `analysis_context_pack_overview.data_quality`를 사용해 lightweight guardrail을 적용합니다. core quote / daily_bars / technical data가 stale, fallback, missing, fetch_failed, partial, estimated이면 high-confidence conclusion이 cap됩니다. Pre-market, non-trading, unknown phase는 high-confidence intraday buy/sell action을 내면 안 됩니다. Intraday, lunch-break, near-close output은 main conclusion과 action field에서 "after today's close" 또는 "focus tomorrow" 같은 post-market recap wording을 scan하고, 명백한 violation은 phase-safe wait/watch wording으로 대체됩니다. guardrail은 low-sensitivity `phase_context`와 data limitations만 채우며 watch condition이나 next-check time을 만들어내지 않습니다. Notification summaries, alerts, holdings, backtest linkage는 이후 P6 작업입니다.

### Signal Attribution Analysis(Issue #1742)

Issue #1742는 개별 종목 분석 report의 `dashboard.signal_attribution` 아래 signal attribution analysis block을 추가합니다. field는 `technical_indicators`, `news_sentiment`, `fundamentals`, `market_conditions`(네 contribution 값. 유효한 non-zero 값은 합이 100이 되도록 normalize, all-zero는 effective signal 없음), `strongest_bullish_signal`, `strongest_bearish_signal`입니다. 이 field는 recommendation reason의 구성을 설명해 사용자가 AI decision의 attribution weight를 이해하도록 돕습니다.

Signal attribution analysis는 모든 report path에서 렌더링됩니다.
- `generate_dashboard_report()`(기본 notification report)
- `generate_single_stock_report()`(single-stock push report)
- `templates/report_markdown.j2`(Jinja2 template)
- `HistoryService._generate_single_stock_markdown()`(Web history drawer)

Normalization function은 `_parse_response()`와 `parse_dashboard_json()`에서 명시적으로 호출되어 다음을 보장합니다.
- String percentage를 int로 변환(예: `"35%"` → `35`)
- 음수는 0으로 clamp
- 합이 100이 아닌 non-zero valid value는 합 100으로 normalize
- all-zero value는 effective signal 없음의 의미로 0 유지
- 값은 [0, 100]으로 clamp

`signal_attribution`은 optional display field이지 required integrity field가 아닙니다. 누락되어도 integrity check를 실패시키지 않고, `missing` list에 기록되지 않으며, completion prompt를 trigger하지 않습니다. 존재하면 normalize되어 지원 report path에서 렌더링됩니다.

### Alerts, Portfolio, History Linkage(Issue #1386 P6)

P6는 기존 `market_phase_summary`와 `analysis_context_pack_overview`를 alerts, portfolio, history, backtesting, notifications 전반에서 재사용합니다. 새 phase/pack protocol을 도입하지 않고 database migration도 필요 없습니다. Alert trigger row는 기존 text `diagnostics` field를 계속 사용합니다. diagnostics가 JSON으로 표현 가능하면 worker가 `analysis_visibility.market_phase_summary`, `analysis_visibility.analysis_context_pack_overview`, `analysis_visibility.source`를 triggered row에 merge합니다. Legacy plain-text diagnostics는 계속 읽을 수 있습니다. Alert API derived field는 empty로 남고 `analysis_visibility_source=legacy_text`가 됩니다.

Alert phase summary는 trigger-time context에서 생성됩니다. symbol target은 stock market을 추론하고, `target_scope=market`은 `cn|hk|us` region을 직접 사용하며, 단일 market에 매핑할 수 없는 account-level target은 `unknown`으로 fallback할 수 있습니다. pack overview는 evaluator-provided overview 또는 최근 30일의 low-sensitivity history snapshot에서만 가져옵니다. missing data는 `null`을 반환합니다. alert worker는 pack을 fabricate하지 않고 lightweight LLM analysis를 자동 실행하지 않습니다. Public source value는 `alert_trigger_market_context`, `analysis_history_snapshot`, `evaluator_snapshot`, `legacy_text`, `null`입니다.

Portfolio page는 `POST /api/v1/portfolio/positions/{symbol}/analysis` 기반의 per-position manual analysis action을 추가합니다. request는 `account_id`, `analysis_phase=auto|premarket|intraday|postmarket`, `force`를 받습니다. non-zero current holding만 제출할 수 있습니다. missing holding은 404를 반환하고, 같은 symbol이 여러 account에 있는데 `account_id`가 없으면 `400 ambiguous_position_account`를 반환합니다. endpoint는 기존 async accepted / duplicate semantics를 유지하고, `force`는 refresh behavior만 제어합니다. in-flight duplicate detection을 우회하지 않습니다. backend는 low-sensitivity `portfolio_context`만 내부적으로 pipeline과 optional context-pack `portfolio` block으로 전달합니다. 이 block은 기존 6개 data-quality weight에 영향을 주지 않으며 task list나 SSE payload를 통해 노출되지 않습니다.

History lists, same-stock history, StockBar items, details는 `context_snapshot`에서 `market_phase_summary`를 추출합니다. old rows, missing snapshots, parse failures는 `null`을 반환합니다. Backtest result item은 이제 `market_phase`와 `market_phase_summary`를 포함하며 result/performance/summary query는 `analysis_phase=premarket|intraday|postmarket|unknown`을 지원합니다. Statistics는 `intraday`, `lunch_break`, `closing_auction`을 intraday로 접고, `non_trading`, missing, invalid value를 unknown으로 접습니다. Phase-filtered backtest query는 repository를 통해 result와 snapshot을 batch-read하고 pagination 전에 bucket하며, summary diagnostics에 `phase_breakdown`과 `raw_phase_counts`를 노출합니다.

Notification summary는 하나의 public formatting helper를 사용하며 phase label, trigger source, partial-bar warning, data-quality level, 처음 두 limitations만 포함합니다. raw context pack, prompt, news body text, sensitive portfolio detail은 출력하지 않습니다. Web Alerts, Portfolio, History, StockBar, Backtest page는 새 phase badge, quality summary, phase filter, breakdown을 표시합니다.

### 문서, 설정, 마이그레이션 참고(Issue #1386 P7)

P7은 pre-market / intraday / post-market analysis에 대한 user-facing documentation closeout입니다. runtime behavior, configuration keys, API parameters, database migrations, Web phase override selector, Bot phase parameters, GitHub Actions intraday workflow를 추가하지 않습니다. 기본 daily post-market analysis, 기본 GitHub Actions run, 기존 schedule behavior는 변경되지 않습니다.

권장 사용법:

| 상황 | 권장 사용 | 참고 |
| --- | --- | --- |
| Pre-market | 개장 계획과 watch condition 구성 | 오늘 아직 거래되지 않은 price action을 사실처럼 설명하지 마세요. 마지막 complete trading day, overnight information, opening trigger에 집중하세요. |
| Intraday / lunch break / near close | live state, risk, opportunity alert 확인 | current price, realtime quote freshness, partial bars, data limitations, next watch conditions에 집중하세요. full post-market review를 대체하지 않습니다. |
| Post-market | full review와 next-day plan 유지 | complete trading-day semantics를 사용하며 기본 daily-analysis scenario에 가장 가깝습니다. |

Entrypoints와 visibility:

| Entrypoint | Phase behavior |
| --- | --- |
| `POST /api/v1/analysis/analyze` | `analysis_phase=auto|premarket|intraday|postmarket` 지원. 생략 시 `auto`. |
| Web main analysis / re-analysis / portfolio manual analysis | 현재 phase override selector는 없습니다. frontend는 `auto`를 기본값으로 사용하고, in-progress task panel은 requested phase를 표시하며, final report page는 final phase label을 표시합니다. |
| Bot / CLI / schedule / default GitHub Actions | `analysis_phase`를 전달하지 않습니다. 계속 `auto` inference를 사용하며 기본 post-market behavior는 변경되지 않습니다. |
| History / backtest / notifications / alerts | public `market_phase_summary`와 low-sensitivity `analysis_context_pack_overview`만 소비합니다. full pack, prompt summary, news body text, sensitive portfolio detail은 노출하지 않습니다. |

`analysis_phase`는 requested override value이고, final report phase는 여전히 `report.meta.market_phase_summary.phase`입니다. `analysis_phase`를 생략하는 오래된 caller는 호환됩니다. `market_phase_summary` 또는 `analysis_context_pack_overview`가 없는 오래된 history row는 empty field를 반환하고 정상 로드됩니다. Backtest query는 `analysis_phase=premarket|intraday|postmarket|unknown` filtering을 지원하며 P6는 lunch-break와 near-close phase를 intraday로 접습니다.

`SAVE_CONTEXT_SNAPSHOT=false` 또는 CLI `--no-context-snapshot`은 새 history row의 full `context_snapshot` 저장만 중단합니다. 따라서 새 history는 persisted phase summary / pack overview / diagnostics snapshot data를 더 이상 노출하지 않습니다. current-run `AnalysisContextPack` construction을 비활성화하지 않고, prompt의 low-sensitivity `analysis_context_pack_summary`를 제거하지 않으며, report JSON schema를 바꾸지 않습니다. 예전 post-market wording에 더 가까운 output이 필요한 caller는 임시로 `analysis_phase=postmarket`을 고정할 수 있습니다. P0-P6 phase/pack runtime integration을 완전히 제거하려면 release rollback 또는 code rollback이 필요합니다.

---

## 알림 채널 설정

알림 채널 matrix와 `--check-notify` CLI 상세는 [알림 가이드](notifications.md)에 문서화되어 있습니다.

### WeChat Work

1. WeChat Work group chat에서 "Group Bot" 추가
2. Webhook URL 복사
3. `WECHAT_WEBHOOK_URL` 설정

### Feishu

> ⚠️ **핵심 구분**: `FEISHU_WEBHOOK_SECRET`(webhook signing secret)과 `FEISHU_APP_SECRET`(Feishu App Secret)은 완전히 다른 설정 변수이며 서로 바꿔 쓸 수 없습니다.

**최소 동작 설정(보안 제한 없음):**

```env
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/your_hook_token
```

**단계별 설정:**

1. **대상 Feishu group에 Custom Bot 생성**:
   - group 열기 → settings icon(오른쪽 위) → **Group Bots** → **Add Bot** → **Custom Bot**
   - bot 이름 입력 후 생성된 **Webhook URL** 복사(형식: `https://open.feishu.cn/open-apis/bot/v2/hook/...`)
2. 방금 복사한 URL을 `FEISHU_WEBHOOK_URL`에 설정합니다.
3. bot의 **Security Settings**를 확인하고 추가 옵션이 활성화되어 있으면 대응 설정을 추가합니다.
   - **추가 보안 없음**: `FEISHU_WEBHOOK_URL`만 필요.
   - **Signature verification enabled**: Feishu에 표시된 secret을 `FEISHU_WEBHOOK_SECRET`에 복사합니다. **양쪽이 함께 켜지거나 함께 꺼져야 합니다**. Feishu signing이 켜져 있는데 `FEISHU_WEBHOOK_SECRET`이 없거나 반대인 경우 모든 요청이 거부됩니다.
   - **Keyword enabled**: 동일한 keyword를 `FEISHU_WEBHOOK_KEYWORD`에 복사합니다. app이 모든 메시지 앞에 자동으로 붙이므로 report template을 바꿀 필요가 없습니다.
   - **IP allowlist enabled**: runtime(local / Docker / GitHub Actions는 각각 IP가 다름)의 outbound IP가 allowlist에 있는지 확인하세요.
4. `FEISHU_APP_ID` / `FEISHU_APP_SECRET`은 Feishu app / Stream Bot / cloud document flow 전용입니다. group webhook notification을 trigger하지 않으며 `FEISHU_WEBHOOK_URL` 대신 단독으로 사용하면 안 됩니다.
5. `FEISHU_APP_ID` / `FEISHU_APP_SECRET`이 `FEISHU_CHAT_ID`와 함께 설정되면 Feishu App Bot이 group webhook 없이 지정 chat 또는 user로 직접 notification을 push할 수 있습니다. `FEISHU_RECEIVE_ID_TYPE` 기본값은 `chat_id`이며 P2P delivery에는 `open_id`로 설정하세요. 이는 group webhook path와 독립적인 Feishu OpenAPI Bot session route를 사용합니다.
6. App Bot send path는 `requirements.txt`에 이미 나열된 기존 `lark-oapi>=1.0.0` dependency를 재사용합니다. standard source install, Docker, GitHub Actions daily workflow, desktop build 모두 `pip install -r requirements.txt`를 통해 설치합니다. 참고: [Feishu message create OpenAPI](https://open.feishu.cn/document/server-docs/im-v1/message/create), [lark-oapi PyPI](https://pypi.org/project/lark-oapi/), [SDK repo](https://github.com/larksuite/oapi-sdk-python).

**흔한 실패 원인:**
- `FEISHU_APP_ID` / `FEISHU_APP_SECRET`만 설정하고 `FEISHU_WEBHOOK_URL`도 App Bot active-delivery target `FEISHU_CHAT_ID`도 설정하지 않음
- bot에 Signature security가 켜져 있지만 `FEISHU_WEBHOOK_SECRET`을 local에 설정하지 않음(또는 실수로 `FEISHU_APP_SECRET`을 설정)
- bot에 Keyword security가 켜져 있지만 `FEISHU_WEBHOOK_KEYWORD`를 local에 설정하지 않음
- bot이 대상 group에 추가되지 않았거나 group permission이 posting을 막음
- Feishu IP allowlist가 활성화되어 있고 runtime IP가 allowlist에 없음
- 메시지 내용이 너무 김: Feishu에는 per-message length limit이 있습니다. 시스템은 메시지를 자동 분할합니다. 전체 내용을 단일 문서로 보려면 Feishu Cloud Document(`FEISHU_APP_ID` / `FEISHU_APP_SECRET` / `FEISHU_FOLDER_TOKEN`)를 설정하세요.

그림이 포함된 전체 troubleshooting guide는 [docs/bot/feishu-bot-config.md](bot/feishu-bot-config.md)를 참고하세요.

### Telegram

1. @BotFather와 대화해 Bot 생성
2. Bot Token 받기
3. Chat ID 받기(@userinfobot 사용)
4. `TELEGRAM_BOT_TOKEN`과 `TELEGRAM_CHAT_ID` 설정
5. (선택) Topic으로 보내려면 `TELEGRAM_MESSAGE_THREAD_ID` 설정(Topic link에서 획득)

### Email

1. 이메일의 SMTP 서비스 활성화
2. authorization code 받기(로그인 비밀번호 아님)
3. `EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVERS` 설정

지원 이메일 공급자:
- QQ Mail: smtp.qq.com:465
- 163 Mail: smtp.163.com:465
- Gmail: smtp.gmail.com:587

**서로 다른 종목 그룹을 서로 다른 이메일 수신자에게 보내기**(Issue #268, 선택):
`STOCK_GROUP_N`과 `EMAIL_GROUP_N`을 설정해 서로 다른 종목 그룹을 서로 다른 inbox로 route할 수 있습니다. `STOCK_LIST`가 실제 분석 범위를 계속 정의하므로 각 `STOCK_GROUP_N`은 `STOCK_LIST`의 부분집합이어야 합니다. 이는 이메일 수신자만 변경하며 Telegram, WeChat, Webhook 등 다른 채널은 전체 `STOCK_LIST`에 대한 full report를 계속 받습니다. Market review email은 설정된 모든 group recipient에게 전송됩니다.

> GitHub Actions 제한: 2026-03-29 기준, 저장소의 기본 `00-daily-analysis.yml`은 임의 번호 `STOCK_GROUP_N` / `EMAIL_GROUP_N` 변수를 자동 import하지 않습니다. workflow `env:` block을 확장하지 않고 repository Secrets / Variables에만 추가하면 runtime process에 도달하지 않습니다.

```bash
STOCK_LIST=600519,300750,002594,AAPL
STOCK_GROUP_1=600519,300750
EMAIL_GROUP_1=user1@example.com
STOCK_GROUP_2=002594,AAPL
EMAIL_GROUP_2=user2@example.com
```

### Custom Webhook

다음을 포함한 모든 POST JSON Webhook을 지원합니다.
- DingTalk Bot
- Discord Webhook
- Slack Webhook
- Bark(iOS push)
- Self-hosted services

`CUSTOM_WEBHOOK_URLS`를 설정하고 여러 개는 쉼표로 구분합니다.

AstrBot, NapCat 또는 자체 호스팅 서비스가 custom request body를 필요로 하면 `CUSTOM_WEBHOOK_BODY_TEMPLATE`을 설정하세요. 이는 global template이며 Bark, Slack, Discord처럼 URL auto-detected payload보다 먼저 렌더링됩니다. 렌더링된 값이 JSON object가 아니면 DSA는 기본 payload로 fallback합니다. newline과 quote가 유효한 JSON으로 유지되도록 `$content_json` / `$title_json` 사용을 권장합니다.

```env
CUSTOM_WEBHOOK_BODY_TEMPLATE={"msg_type":"text","content":$content_json}
```

사용 가능한 placeholder: `$content_json`, `$content`, `$title_json`, `$title`.

Raw `$content` / `$title`은 JSON-escaped되지 않으므로 quote나 newline이 template을 invalid로 만들고 fallback을 trigger할 수 있습니다.

Docker Compose 배포에서 Web Settings로 이 값을 저장하면 app placeholder를 `$$content_json` / `$$title_json`로 쓰고 runtime에서 single `$` form으로 복원합니다. 이렇게 하면 Compose가 이를 empty value로 확장하는 것을 막습니다. Docker `.env`를 수동 편집한다면 같은 `$$content_json` style을 사용하세요.

Bark는 custom webhook baseline에 남습니다. `BARK_*` 설정은 필요 없습니다. Bark endpoint를 `CUSTOM_WEBHOOK_URLS`에 설정하세요. global template과 함께 Bark를 사용할 때는 Bark body를 명시적으로 포함하세요.

```env
CUSTOM_WEBHOOK_URLS=https://api.day.app/YOUR_BARK_KEY
```

```env
CUSTOM_WEBHOOK_BODY_TEMPLATE={"title":$title_json,"body":$content_json,"group":"stock"}
```

NapCat / OneBot 예시는 실제 endpoint, `user_id`, `group_id`에 맞게 조정해야 합니다.

```env
CUSTOM_WEBHOOK_BODY_TEMPLATE={"user_id":123456,"message":$content_json}
```

### ntfy / Gotify

ntfy와 Gotify는 first-class notification channel입니다. text / JSON만 전송하며 Markdown-to-image를 사용하지 않습니다.

ntfy는 full topic endpoint를 사용합니다. 마지막 path segment가 topic으로 취급됩니다.

```env
NTFY_URL=https://ntfy.sh/my-topic
NTFY_TOKEN=
```

Gotify는 server base URL을 사용합니다. sender는 고정 `/message` API를 붙이고 application token을 `X-Gotify-Key` header로 보냅니다. `GOTIFY_URL`은 reverse-proxy path prefix를 포함할 수 있지만 `/message`를 포함하면 안 됩니다.

```env
GOTIFY_URL=https://gotify.example
GOTIFY_TOKEN=app-token
```

```env
# Actual request URL: https://example.com/gotify/message
GOTIFY_URL=https://example.com/gotify
GOTIFY_TOKEN=app-token
```

`NTFY_URL`과 `GOTIFY_URL`은 두 서비스의 API가 다르기 때문에 의도적으로 서로 다른 URL semantics를 사용합니다. ntfy topic은 endpoint의 일부이고, Gotify는 `/message`를 고정 server API로 사용합니다.

### Discord

Discord는 두 가지 push method를 지원합니다.

**방법 1: Webhook(권장, 단순)**

1. Discord channel settings에서 Webhook 생성
2. Webhook URL 복사
3. 환경 변수 설정:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx/yyy
```

**방법 2: Bot API(더 많은 권한 필요)**

1. [Discord Developer Portal](https://discord.com/developers/applications)에서 application 생성
2. Bot 생성 후 Token 획득
3. Bot을 server에 초대
4. Channel ID 획득(developer mode에서 channel right-click)
5. 환경 변수 설정:

```bash
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_MAIN_CHANNEL_ID=your_channel_id
```

Discord로 알림을 보내는 것뿐 아니라 Discord Slash Command / Interaction callback을 받아야 한다면 `Discord Developer Portal -> General Information -> Public Key`에서 public key를 복사하고 다음을 설정하세요.

```bash
DISCORD_INTERACTIONS_PUBLIC_KEY=your_public_key
```

이 public key가 없으면 inbound Discord webhook request는 거부됩니다.

### Slack

Slack은 두 가지 push method를 지원합니다. 둘 다 설정되면 text와 image가 같은 channel에 도착하도록 Bot API가 우선합니다.

**방법 1: Bot API(권장, 이미지 업로드 지원)**

1. Slack App 생성: https://api.slack.com/apps → Create New App
2. Bot Token Scopes 추가: `chat:write`, `files:write`
3. workspace에 설치하고 Bot Token(xoxb-...) 획득
4. Channel ID 획득: channel details → 맨 아래 channel ID 복사
5. 환경 변수 설정:

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_CHANNEL_ID=C01234567
```

**방법 2: Incoming Webhook(간단한 설정, text only)**

1. Slack App management page에서 Incoming Webhook 생성
2. Webhook URL 복사
3. 환경 변수 설정:

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../xxx
```

### Pushover(iOS/Android Push)

[Pushover](https://pushover.net/)는 iOS와 Android를 지원하는 cross-platform push service입니다.

1. Pushover account 등록 및 App 다운로드
2. [Pushover Dashboard](https://pushover.net/)에서 User Key 획득
3. Application 생성해 API Token 획득
4. 환경 변수 설정:

```bash
PUSHOVER_USER_KEY=your_user_key
PUSHOVER_API_TOKEN=your_api_token
```

특징:
- iOS/Android 지원
- notification priority와 sound settings 지원
- 개인 사용에 충분한 무료 할당량(월 10,000 messages)
- 메시지 7일 보관

---

## 데이터 소스 설정

시스템은 기본적으로 AkShare(무료)를 사용하며, 다른 데이터 소스도 지원합니다.

### AkShare(기본)
- 무료, 설정 불필요
- 데이터 소스: Eastmoney scraper

### Tushare Pro
- Token 발급을 위한 등록 필요
- 더 안정적이고 더 포괄적인 데이터
- `TUSHARE_TOKEN` 설정

### Baostock
- 무료, 설정 불필요
- backup data source로 사용

### YFinance
- 무료, 설정 불필요
- 미국/HK 주식 데이터 지원
- 미국 주식 과거 및 실시간 데이터는 akshare의 미국 주식 adjustment 이슈로 인한 technical indicator 오류를 피하기 위해 모두 YFinance만 사용합니다.

### Longbridge
- 미국/HK 주식용 선택적 fallback이며, 주로 YFinance가 놓칠 수 있는 field를 보완하는 데 사용합니다.
- 새 integration은 Longbridge OAuth 2.0을 사용해야 합니다. client id는 `LONGBRIDGE_OAUTH_CLIENT_ID`에서 읽고, Legacy Access Token이 설정되지 않았으면 `LONGBRIDGE_APP_KEY`에서 읽습니다. interactive machine에서 `python scripts/generate_longbridge_oauth_token.py --client-id <client_id>`를 한 번 실행해 SDK token cache를 생성하세요.
- GitHub Actions / Docker headless run에서는 local `~/.longbridge/openapi/tokens/<client_id>` 파일을 base64로 변환해 `LONGBRIDGE_OAUTH_TOKEN_CACHE_B64`에 저장하세요.
- OAuth runtime support는 SDK API `OAuthBuilder`와 `Config.from_oauth`를 필요로 합니다. Linux/Docker 환경이 오래된 SDK만 설치할 수 있으면 app은 명확한 warning을 log하고 Longbridge를 건너뛰며 YFinance / AkShare fallback을 유지합니다.
- Legacy API Key는 `LONGBRIDGE_APP_KEY`, `LONGBRIDGE_APP_SECRET`, `LONGBRIDGE_ACCESS_TOKEN`으로 계속 지원됩니다. 이 Access Token은 legacy API-key credential이며 OAuth access token이 아닙니다.
- 선택적 knob: `LONGBRIDGE_STATIC_INFO_TTL_SECONDS`(기본 `86400`) 및 `LONGBRIDGE_CONNECTION_COOLDOWN_SECONDS`(기본 `15`)
- credential이 없으면 optional Longbridge fetcher가 instantiate되지 않습니다.
- `client is closed`, `context closed`, `connection closed` 같은 runtime error가 발생하면 Longbridge는 짧은 cooldown window에 들어가고, 미국/HK daily 또는 realtime request는 매번 reconnect하지 않고 자동으로 YFinance / AkShare로 fallback합니다.

---

## 고급 기능

### 홍콩 주식 지원

HK 주식 코드는 `hk` prefix를 사용합니다.

```bash
STOCK_LIST=600519,hk00700,hk01810
```

HK daily history는 HK daily data를 지원하지 않는 efinance, pytdx, baostock 및 기타 built-in provider를 건너뛰어 HK symbol과 non-HK market data의 불일치를 피합니다. AkShare/Tushare/YFinance/Longbridge는 HK fallback path를 계속 제공합니다. Longbridge가 connection cooldown window 안에 있으면 route는 일시적으로 이를 건너뛰고 남은 HK-capable fallback을 계속 사용합니다.

### 다중 모델 전환

여러 모델을 설정하면 시스템이 자동 전환합니다.

```bash
# Gemini (primary)
GEMINI_API_KEY=xxx
GEMINI_MODEL=gemini-3.1-pro-preview

# OpenAI compatible (backup)
OPENAI_API_KEY=xxx
OPENAI_BASE_URL=https://api.deepseek.com
OPENAI_MODEL=deepseek-v4-flash
# deepseek-chat / deepseek-reasoner remain compatible, but DeepSeek marks them deprecated after 2026/07/24
```

### 고급 모델 라우팅(LiteLLM 기반)

[LLM 설정 가이드](LLM_CONFIG_GUIDE_KO.md)를 참고하세요. 대부분의 사용자는 primary model, fallback model, channel 정도만 이해하면 충분합니다. 이 섹션은 underlying [LiteLLM](https://github.com/BerriAI/litellm) routing capability에 직접 접근하려는 전문가용입니다. 별도 Proxy service는 필요 없습니다.

**2-layer mechanism**: same-model multi-key rotation(Router)과 cross-model fallback은 독립적입니다.

**Multi-key + cross-model fallback 예시**:

```env
# Primary: 3 Gemini keys rotate; Router switches on 429
GEMINI_API_KEYS=key1,key2,key3
LITELLM_MODEL=gemini/gemini-3.1-pro-preview

# Cross-model fallback: when all primary keys fail, try Claude → GPT
# Requires ANTHROPIC_API_KEY, OPENAI_API_KEY
LITELLM_FALLBACK_MODELS=anthropic/claude-sonnet-4-6,openai/gpt-5.4-mini
```

> ⚠️ `LITELLM_MODEL`에는 provider prefix(예: `gemini/`, `anthropic/`, `openai/`)가 반드시 포함되어야 합니다. Legacy `GEMINI_MODEL`(prefix 없음)은 `LITELLM_MODEL`이 설정되지 않았을 때만 사용됩니다.

**Vision model(이미지 종목 코드 추출)**: [LLM 설정 가이드 - Vision](LLM_CONFIG_GUIDE_KO.md#고급-기능-vision-모델-설정)을 참고하세요.

### Debug Mode

```bash
python main.py --debug
```

로그 파일 위치:
- 일반 로그: `logs/stock_analysis_YYYYMMDD.log`
- Debug 로그: `logs/stock_analysis_debug_YYYYMMDD.log`

Debug logs는 app 자체 DEBUG message를 유지하지만, streaming generation 중 token-level third-party noise를 피하기 위해 LiteLLM internals는 기본적으로 `WARNING`입니다. LiteLLM internals를 임시로 조사하려면 `.env`에 `LITELLM_LOG_LEVEL=DEBUG`를 설정하세요.

### SQLite Write Stability

file-based SQLite database에 대해 app은 이제 connection startup에서 `WAL`을 활성화하고 `busy_timeout`을 설정합니다. `save_daily_data()`도 `(code, date)`에 대해 batch atomic upsert를 사용해 bulk writes와 concurrent callback 중 lock contention을 줄입니다.

`.env`에서 동작을 조정할 수 있습니다.

| 변수 | 기본값 | 설명 |
|----------|---------|-------------|
| `SQLITE_WAL_ENABLED` | `true` | file-based SQLite에 `journal_mode=WAL` 활성화 |
| `SQLITE_BUSY_TIMEOUT_MS` | `5000` | SQLite lock wait timeout(ms) |
| `SQLITE_WRITE_RETRY_MAX` | `3` | `database is locked` / `database table is locked` 오류의 최대 retry 수 |
| `SQLITE_WRITE_RETRY_BASE_DELAY` | `0.1` | exponential write retry의 base backoff delay(초) |

---

## Decision Actionability

단일 종목 리포트는 support/resistance, volume/chip context, main-force capital flow, risk event를 바탕으로 operation advice를 보정합니다. 이는 하루 price movement나 score threshold만으로 직접 buy/sell이 뒤집히는 일을 줄입니다. 가격이 support와 resistance 사이에 있고 capital flow가 명확하지 않을 때, report는 hold, range-bound watch, shakeout watch 같은 neutral actionable wording을 선호합니다. Buy call은 support confirmation 또는 volume/capital-flow confirmation이 있는 valid resistance breakout을 필요로 합니다. sell/reduce call은 support failure, sustained outflow, clearly elevated risk를 필요로 합니다.
이 post-processing update는 advisory wording과 stability logic만 조정하며 LiteLLM, providers, API model settings를 포함한 configured LLM model/provider routing semantics는 변경하지 않습니다.
호환성 검사 결과: decision operability와 runtime post-processing path는 변경되지만, model/provider/API configuration과 persistence semantics는 변경되지 않습니다. compatibility boundary는 analysis/pipeline/agent intent inference와 stabilization mapping에 있습니다.
검증 경로: runtime behavior는 `src/analyzer.py`, `src/core/pipeline.py`, `src/core/backtest_engine.py`, `src/report_language.py`, `src/agent` decision-path modules에 구현되어 있으며, 대응 테스트는 `tests/test_backtest_engine.py`, `tests/test_analyzer_news_prompt.py`, `tests/test_decision_stability.py`, `tests/test_agent_pipeline.py`에 있습니다. `src/config.py`나 persistence code path의 runtime config field 또는 config-cleanup logic을 추가/삭제하지 않습니다.

### Decision Action Taxonomy(#1390 P0)

단일 종목 리포트는 기존 free-text `operation_advice`를 유지하면서 Web history, StockBar, same-stock history, backtest result row의 structured display를 위해 optional `action` / `action_label` field를 추가합니다. `decision_type`은 legacy `buy|hold|sell` statistics contract로 남습니다. 빈 `action`은 기존 `decision_type` inference chain을 다시 쓰지 않습니다.

| `action` | 흔한 source text | `decision_type` bridge |
| --- | --- | --- |
| `buy` | `strong_buy`, `强烈买入`, `buy`, `买入`, `布局`, `建仓` | `buy` |
| `add` | `add`, `加仓`, `增持`, `accumulate` | `buy` |
| `hold` | `hold`, `持有`, `持有观察`, `洗盘观察` | `hold` |
| `watch` | `watch`, `观望`, `等待`, `wait` | `hold` |
| `reduce` | `reduce`, `减仓`, `trim` | `sell` |
| `sell` | `sell`, `卖出`, `清仓`, `strong_sell`, `强烈卖出` | `sell` |
| `avoid` | `avoid`, `回避`, `规避`, `不建议买入`, `避免买入`, `do not buy` | `hold` |
| `alert` | `alert`, `风险预警`, `警惕`, `触发告警`, `risk alert` | `hold` |

표의 `decision_type` bridge는 8-state action taxonomy와 legacy 3-state statistics contract 간 compatibility만 문서화합니다. #1390 P0는 `action`을 기존 `decision_type`에 자동으로 write back하지 않습니다. upstream이 explicit `action`과 의미상 다른 `decision_type`을 모두 보내면 legacy statistics, backtesting, old report semantics는 여전히 `decision_type` / 기존 inference chain을 따르고, `action/action_label`은 structured display metadata로 남습니다.

Unknown 또는 ambiguous advice는 `watch`나 `hold`로 강제되지 않고 empty `action/action_label`을 반환합니다. Web history cards, StockBar, same-stock history drawers, backtest result rows는 old record에 `action/action_label`이 없을 때 `operation_advice`를 display-only fallback으로 사용합니다. 이 fallback은 UI label에만 영향을 주며 stable API action이나 future signal asset이 아닙니다. Web이 `action`과 `action_label`을 모두 받으면 현재 UI language에서 `action` 기반 label을 먼저 렌더링합니다. API `action_label`은 non-Web client용 report-language display metadata 또는 `action` 부재 시 compatibility display로 남습니다. Market review와 기타 non-stock report는 trading `action` value를 emit하지 않고 `operation_advice` text만 유지합니다. `dashboard.phase_decision.immediate_action`은 market-phase guardrail report block에 속하며 #1390 P0 8-state action derivation에 사용되지 않습니다. final market phase는 여전히 `report.meta.market_phase_summary.phase`에서 옵니다.

#1390 P0는 future signal-asset field를 current report summaries, history lists, StockBar rows, backtest responses로 flatten하지 않습니다. #1390 P1은 이제 `horizon`, `plan_quality`, `status` 같은 더 세분화된 plan field를 독립 `DecisionSignal` resource를 통해 운반합니다. 그래도 기존 report contract를 변경하지 않고, history를 backfill하지 않으며, configuration을 추가하지 않습니다.

### Decision Signal Asset(#1390 P1/P2/P3/P4/P5)

`DecisionSignal`은 AI recommendation을 query 가능하고 deduplicated이며 status-updatable한 signal asset으로 저장하는 독립 backend resource입니다. `operation_advice`를 대체하지 않고 legacy `decision_type=buy|hold|sell` contract를 확장하지 않습니다. #1390 P2부터 regular stock analysis와 Agent stock analysis는 analysis history가 성공적으로 저장된 후 final `AnalysisResult`에서 `source_type=analysis` signal 하나를 best-effort로 추출합니다. explicit API와 service call은 계속 지원됩니다. #1390 P3는 public response schema를 바꾸지 않고 default lifecycle handling, narrow same-source relaxed deduplication, opposite-signal invalidation, stricter terminal-state transition을 추가합니다.

Automatic extraction은 completed report의 structured field만 소비합니다. Markdown을 parse하지 않고, old history를 backfill하지 않으며, configuration을 추가하거나 main report contract를 변경하지 않습니다. Extraction failure, unknown/ambiguous advice, non-stock report, unrecognized market은 signal write를 건너뛰며 report persistence에 영향을 주지 않습니다. `source_report_id`는 방금 저장된 `AnalysisHistory.id`입니다. `trace_id`는 runtime diagnostics trace를 우선하고 pipeline trace 또는 `query_id`로 fallback합니다. `stock_name`은 `AnalysisResult.name`에서 가져오고, `trigger_source`는 runtime entrypoint에서 가져오며 `system`으로 fallback합니다.

P2 automatic extraction에서 `market_phase`는 먼저 saved context snapshot의 `market_phase_summary.phase`를 읽고, 그다음 `AnalysisResult.market_phase_summary.phase`로 fallback합니다. data quality는 먼저 saved context snapshot의 `analysis_context_pack_overview.data_quality`를 읽고, 그다음 `AnalysisResult.analysis_context_pack_overview.data_quality`로 fallback합니다. Price-plan extraction은 history persistence와 같은 sniper-point parser를 재사용해 `dashboard.battle_plan.sniper_points.ideal_buy/secondary_buy/stop_loss/take_profit`을 `entry_low/entry_high/stop_loss/target_price`로 mapping합니다. `ideal_buy`만 있으면 `entry_low`, `secondary_buy`만 있으면 `entry_high`를 쓰고, 둘 다 있으면 `entry_low <= entry_high`가 되도록 정렬합니다. stop-loss 또는 target price가 없으면 field를 만들어내지 않고 service-computed `plan_quality`만 낮춥니다. `watch_conditions`는 먼저 `dashboard.phase_decision.watch_conditions`를 읽고 `dashboard.battle_plan.action_checklist`로 fallback합니다. `catalyst_summary`는 `dashboard.intelligence.positive_catalysts`가 list로 존재할 때만 기록합니다. `confidence`는 보수적인 report-level mapping을 사용합니다. `高/high=0.8`, `中/medium/mid=0.6`, `低/low=0.4`; 원래 report confidence level은 `metadata`에 남습니다.

P3부터 `DecisionSignalService`가 lifecycle default를 소유합니다. explicit `horizon` / `expires_at` 값은 항상 우선합니다. `horizon`이 생략되면 `alert` 또는 `premarket/intraday/lunch_break/closing_auction`은 기본 `intraday`, `postmarket/non_trading/unknown` 또는 missing phase context는 기본 `3d`가 됩니다. `expires_at`이 생략되면 `intraday`는 먼저 `metadata.market_phase_summary.minutes_to_close/minutes_to_open`을 사용합니다. context가 없으면 deterministic TTL fallback 값(CN 4h, HK 5.5h, US 6.5h, unknown 4h)을 사용합니다. `1d/3d/5d/10d`는 natural day를 사용하고, `swing/long`은 auto-expire하지 않습니다. fallback TTL은 no-context degradation path일 뿐 exchange-calendar close time이 아닙니다. Automatic extraction은 low-sensitive `market_phase_summary.phase/session_date/minutes_to_open/minutes_to_close` hint만 `metadata.market_phase_summary`에 씁니다. final `horizon/expires_at` 값은 여전히 service가 계산합니다.

Core field에는 `stock_code`, `stock_name`, `market`, `source_type`, `source_agent`, `source_report_id`, `trace_id`, `market_phase`, `trigger_source`, `action`, `action_label`, `confidence`, `score`, `horizon`, `entry_low`, `entry_high`, `stop_loss`, `target_price`, `invalidation`, `watch_conditions`, `reason`, `risk_summary`, `catalyst_summary`, `evidence`, `data_quality_summary`, `plan_quality`, `status`, `expires_at`, `created_at`, `updated_at`, `metadata`가 있습니다. `action`은 8-state action taxonomy를 재사용하고, `market_phase`는 market phase enum을 재사용하며, `source_type`은 `analysis|agent|alert|market_review|manual`을 지원합니다. `status`는 `active|expired|invalidated|closed|archived`, `horizon`은 `intraday|1d|3d|5d|10d|swing|long`을 지원합니다.

`confidence`는 `0.0-1.0`, `score`는 `0-100`이며 historical `sentiment_score`와 별개입니다. Price-plan field `entry_low`, `entry_high`, `stop_loss`, `target_price`는 finite positive number여야 합니다. `entry_low`와 `entry_high`가 모두 있으면 `entry_low <= entry_high`가 필요합니다. `plan_quality`는 `complete|partial|minimal|unknown`을 지원합니다. valid explicit value는 그대로 저장하고, 아니면 service가 계산합니다. entry range(`entry_low` 또는 `entry_high`)는 slot 하나로 계산하고, `stop_loss`, `target_price`, `invalidation`, `watch_conditions`가 각각 slot 하나로 계산됩니다. slot 2개는 `partial`, 4개 이상은 `complete`, action/reason은 있지만 slot이 충분하지 않으면 `minimal`입니다.

새 API endpoints:

- `POST /api/v1/decision-signals`: signal을 create 또는 deduplicate하고 HTTP 200으로 `{ item, created }` 반환. exact deduplication은 `source_report_id`가 있으면 `(source_report_id, source_type, market, stock_code, action, horizon, market_phase)`, `trace_id`만 있으면 `(trace_id, source_type, market, stock_code, action, horizon, market_phase)`를 사용합니다. 둘 다 없는 signal은 deduplicate하지 않습니다. exact miss 후 narrow relaxed fallback은 같은 source와 `source_type/market/stock_code/action`을 검색하고 오래된 blank `horizon/market_phase` 값만 채웁니다. `horizon`은 새 값이 service default로 생성된 경우에만 채울 수 있습니다. explicit different horizon 또는 이미 다른 phase는 별도 row로 남습니다. 같은 source key가 expired signal과 match하고 새 요청이 future `expires_at`을 가진 active이면 기존 row를 in-place refresh하고 여전히 `created=false`를 반환하며, renewal은 새 active activation event로 취급됩니다. bullish signal(`buy/add`)의 active creation 또는 expired renewal은 같은 stock의 이전 active defensive signal(`reduce/sell/avoid`)을 invalidates하고 반대도 동일합니다. active duplicate retry도 이전 partial create에서 signal은 저장됐지만 invalidation이 실패한 경우 복구하기 위해 이 repair를 다시 실행합니다. 일반 old duplicate/replay attempt는 새 activation event로 취급하지 않습니다. `hold/watch/alert`는 automatic invalidation을 trigger하지 않습니다. API response schema는 변경되지 않고 refreshed와 duplicate outcome 모두 `created=false`를 반환합니다. P3는 concurrent idempotency를 보장하지 않습니다.
- `GET /api/v1/decision-signals`: `market`, `stock_code`, `action`, `market_phase`, `source_type`, `source_report_id`, `trace_id`, `trigger_source`, `status`, time ranges, `holding_only`, `account_id`를 지원하는 paginated query.
- `POST /api/v1/decision-signals/outcomes/run`: signal-level outcome evaluation 명시 trigger. 기본적으로 completed와 terminal unable row를 건너뛰고 recoverable unable row를 다시 계산하며, `force=true`는 current key를 recompute/overwrite합니다.
- `GET /api/v1/decision-signals/outcomes`: signal outcome row paginated query.
- `GET /api/v1/decision-signals/outcomes/stats`: current outcome-engine stats aggregate. 기본적으로 archived signal 제외.
- `GET /api/v1/decision-signals/{signal_id}/outcomes`: 선택 signal의 current outcome engine outcome rows 조회.
- `GET /api/v1/decision-signals/{signal_id}/feedback`: 선택 signal의 user feedback 조회. 없으면 `feedback_value=null`.
- `PUT /api/v1/decision-signals/{signal_id}/feedback`: 선택 signal의 최신 `useful|not_useful` feedback upsert.
- `GET /api/v1/decision-signals/{signal_id}`: signal 하나 조회. missing ID는 404.
- `PATCH /api/v1/decision-signals/{signal_id}/status`: valid status와 optional `metadata` 업데이트. `metadata`가 제공되면 저장된 metadata object 전체를 대체합니다. `expired/invalidated/closed/archived` terminal state는 직접 `active`로 patch할 수 없습니다. expired renewal은 여전히 future `expires_at`가 있는 active data를 다시 post해야 합니다.
- `GET /api/v1/decision-signals/latest/{stock_code}`: stock의 latest active signals 반환, 기본 `limit=1`.

Read path는 list, detail, latest query 전에 `expires_at`이 지난 active signal을 lazy expire합니다. 이미 expired인 active signal을 생성하면 `expired`로 저장합니다. 같은 source expired signal은 future `expires_at`가 있는 active data를 다시 post해야만 연장할 수 있으며, `PATCH /status`는 `expires_at`을 받지 않습니다. `expired|invalidated|closed|archived`는 직접 active로 patch할 수 없고, `closed|invalidated|archived`는 create path로 reactivate되지 않습니다. Automatic opposite-signal invalidation은 old signal metadata에 `invalidated_by_signal_id`, `invalidated_reason`, `invalidated_at`, `previous_status`를 merge합니다. old metadata JSON이 corrupt이면 invalidation metadata와 `metadata_replaced_due_to_invalid_json=true`로 대체하며 새 signal creation은 차단하지 않습니다. Time field는 storage와 comparison을 위해 UTC naive datetime으로 normalize합니다. timezone-aware input은 UTC로 변환한 뒤 `tzinfo`를 제거하고, naive input은 UTC로 취급합니다. API response는 계속 timezone suffix 없는 ISO string을 반환합니다. Stock code는 `market`별로 결정적으로 normalize됩니다. CN variants(`600519`, `SH600519`, `600519.SH`)는 같은 stored code와 match하고, HK variants(`00700`, `HK00700`, `00700.HK`)는 `HK00700`과 match하며, US ticker는 uppercase됩니다. `holding_only=true`는 active account 아래 `quantity > 0`인 cached `portfolio_positions` row만 읽고 held `(market, stock_code)`로 signal을 match하며, active `account_id`로 optional scope할 수 있습니다. portfolio snapshot replay는 호출하지 않습니다. cache가 없으면 empty result를 반환하므로 caller는 먼저 portfolio snapshot API로 cache를 refresh해야 합니다.

`source_report_id`는 nullable이며 기존 history row를 참조해야 할 필요가 없습니다. history record 삭제는 실제 삭제된 ID와 match하는 `source_type=analysis` history-bound signal만 명시적으로 제거하므로, `manual/agent/alert/market_review` weak-reference signal은 ID collision만으로 삭제되지 않습니다. list endpoint는 `source_report_id`와 `trace_id` typed filter를 지원합니다. `task_id`, `alert_trigger_id` 같은 follow-up association field는 P1에서 `metadata`에 저장해야 합니다. P1은 dedicated column이나 typed filter를 추가하지 않으며 이는 이후 integration phase로 defer됩니다. JSON field, long text field, public short text field(`stock_name/source_agent/trigger_source/action_label`)는 persistence 전에 signal-specific sanitizer로 sanitize됩니다. sanitizer는 sensitive keys, Bearer values, Authorization/Cookie headers 또는 assignments, token-like strings, 기타 sensitive assignments, webhook URLs, URL userinfo, sensitive query 또는 fragment parameter가 있는 URL을 redact합니다. 일반 evidence URL은 source traceability를 위해 보존하고, long text는 diagnostics 300-character truncation을 사용하지 않습니다. `trace_id`는 same-source identity field입니다. 민감 credential이 포함되어 redact될 수 있는 경우 API는 손실 있는 redacted value를 저장하지 않고 요청을 reject합니다.

이 endpoints는 기존 `/api/v1/*` admin authentication middleware를 상속합니다. `ADMIN_AUTH_ENABLED=true`이면 caller는 valid admin session cookie를 보내야 합니다. DecisionSignal은 별도 auth scheme을 추가하지 않습니다.

#1390 P4는 backend contract, database table, configuration을 추가하지 않고 기존 `DecisionSignal` API를 Web UI에 연결합니다. sidebar "AI signals" entry(`/decision-signals`)는 structured decision signal의 중앙 query surface입니다. 페이지 기본값은 `status=active`이고, market, stock code, action, market phase, source, source report ID, status filtering을 지원하며 stock code별 latest-active lookup을 포함합니다. Signal detail은 action, confidence/score, horizon, plan_quality, market_phase, price plan, risk, watch conditions, source report, data quality를 보여줍니다. Web UI는 signal을 `closed`, `invalidated`, `archived`로 marking하는 것만 허용하며 terminal state를 active로 restore하지 않습니다.

#1390 P5는 signal-level feedback, forward outcome evaluation, stats sidecars를 추가합니다. `decision_signals` main table을 확장하지 않고, `analysis_history_id`에 묶인 `BacktestResult`를 재사용하지 않습니다. `decision_signal_feedback`은 `signal_id`별 최신 `useful|not_useful` feedback과 optional reason/note/source를 저장합니다. `decision_signal_outcomes`는 `(signal_id, horizon, engine_version)`별 idempotent row를 저장하며 현재 `engine_version=decision-signal-v1`입니다. 각 outcome은 evaluation time의 `action/market/market_phase/source_type/source_agent/plan_quality/data_quality_level/holding_state`를 freeze해 이후 live-join 변경으로 historical stats가 rewrite되지 않도록 합니다. history 삭제는 먼저 삭제된 history ID에 묶인 `source_type=analysis` signal을 찾고, 그 feedback/outcome sidecar를 제거합니다.

P5 outcome evaluation은 daily-bar로 검증 가능한 `1d/3d/5d/10d`만 지원합니다. window는 `DecisionSignalService._horizon_days()`의 natural-day expiration semantics가 아니라 anchor 이후 다음 1/3/5/10개의 `StockDaily` bar를 의미합니다. `anchor_date`는 먼저 `metadata.market_phase_summary.session_date`를 읽고, 그다음 `created_at.date()`로 fallback합니다. 정확한 anchor date에는 `StockDaily.close`가 있어야 하며 previous-trading-day fallback은 없습니다. Action mapping은 `buy/add -> up`, `hold -> not_down`, `reduce/sell/avoid -> not_up`입니다. `watch/alert`, `intraday/swing/long`, missing anchor price, insufficient forward bars는 explicit `unable_reason`과 함께 `eval_status=unable`을 저장합니다. missing/invalid anchor price, insufficient forward bars, missing/invalid window close는 recoverable unable state로, data가 도착한 뒤 default rerun에서 다시 평가됩니다. non-directional actions, unsupported horizons, missing anchor dates는 terminal unable state이며 기본적으로 idempotently skipped됩니다. Automatic extraction은 runtime `portfolio_context.quantity`를 받을 수 있지만, outcome snapshot metadata에는 low-sensitive `holding_state=holding|empty|unknown`만 쓰고 quantity, account, cost는 쓰지 않습니다.

P5는 새 navigation page나 BacktestPage entry를 추가하지 않고 기존 Web `/decision-signals` page를 확장합니다. filter area는 current outcome-engine stat cards를 보여주고, detail drawer는 outcomes를 lazy load하며 사용자가 useful/not useful feedback을 제출할 수 있게 합니다. P5는 background scheduler를 추가하지 않습니다. outcome 계산은 `POST /api/v1/decision-signals/outcomes/run`을 통해 명시적으로 trigger됩니다. Batch run은 missing outcome을 먼저 처리한 뒤 recoverable unable row를 retry하므로, completed 또는 terminal-unable newest signals가 계속 `limit`을 소비하지 않습니다.

Portfolio page는 AI signal을 non-blocking enhancement로 load합니다. portfolio snapshot과 risk card가 먼저 렌더링된 뒤, page는 current snapshot의 각 unique holding에 대해 `GET /api/v1/decision-signals/latest/{stock_code}?market=<market>&limit=1`를 호출해 latest active signal을 읽습니다. 더 이상 generic `holding_only=true` list endpoint를 scan하지 않고 fixed page-count cutoff도 없습니다. single latest lookup이 실패해도 page는 다른 loaded signal을 유지하고 visible degradation warning을 표시합니다. matching signal이 없는 row는 empty placeholder를 보여줍니다. Matching은 CN variants `600519/SH600519/600519.SH`, HK variants `00700/HK00700/00700.HK`, case-insensitive US tickers에 대한 Web stock-code equivalence rule을 재사용합니다.

#1390 P6는 table, migration, configuration을 추가하지 않고 alerts, notifications, portfolio risk 전반에서 `DecisionSignal`을 재사용합니다. 실제 stock-level alert trigger는 먼저 같은 symbol의 latest active signal을 link하고 low-sensitive `decision_signal_summary`를 `alert_triggers.diagnostics`에 씁니다. active signal이 없으면 worker는 최소 `source_type=alert`, `action=alert` signal만 생성합니다. `trace_id=alert-rule-<hash>`는 best-effort retry de-duplication용이지 active-signal overwrite용이 아니며, payload는 cross-phase duplicate를 피하려고 의도적으로 `market_phase`를 생략합니다. Alert와 analysis notification은 `action/horizon/reason/watch_conditions/risk_summary/source_report_id` 같은 public summary field만 참조하며, notification failure는 trigger 또는 signal write를 막지 않습니다. `GET /api/v1/portfolio/risk`는 이제 current holding의 active `sell/reduce/alert` signal을 count하는 `decision_signal_risk` block을 포함합니다. `avoid/buy/add/hold/watch`는 명시적으로 제외합니다. signal lookup이 실패하면 risk endpoint는 fail open하고 Web risk card는 degraded state를 표시합니다.

#1390 P7은 [DecisionSignal Topic](decision-signals.md)(중국어 전용)에 문서화되어 있습니다. P7은 `DECISION_SIGNAL_*` configuration, database migration, API field, runtime switch를 추가하지 않습니다. 롤백은 관련 code를 revert하는 것입니다. 롤백 후 signal extraction과 write는 중단되지만 report saving, alert triggering, notification sending, portfolio risk main flow는 기존 path를 통해 계속됩니다. Historical signal, feedback, outcome row는 자동 삭제되지 않습니다.

Regular stock history report details는 더 이상 추출된 `source_type=analysis` signal을 embed하지 않고, report detail open 시 `source_report_id=<recordId>` query를 발행하지 않습니다. structured AI recommendation을 확인하려면 `/decision-signals`를 사용하고 source report ID로 filter하거나, `/decision-signals?sourceReportId=<recordId>` deep link를 열거나, stock으로 검색하세요. source report ID가 채워졌거나 해당 URL parameter로 제공되면 Web UI는 default `status=active` 또는 다른 list filter를 추가하지 않고 정확한 `source_type=analysis + source_report_id=<recordId>` query를 보내 old report에 대한 best-effort lazy backfill semantics를 보존합니다.

## 백테스팅

백테스팅 모듈은 historical AI analysis record를 실제 price movement와 자동 검증해 analysis recommendation의 정확도를 평가합니다.

### 작동 방식

1. cooldown period(기본 14일)가 지난 `AnalysisHistory` record 선택
2. analysis date 이후 daily bar data(forward bars) 가져오기
3. operation advice에서 expected direction을 추론하고 actual movement와 비교
4. stop-loss/take-profit hit condition 평가 및 execution return simulation
5. overall 및 per-stock performance metrics로 집계

### Operation Advice Mapping

| Operation Advice | Position | Expected Direction | Win Condition |
|-----------------|----------|-------------------|---------------|
| Buy / Add / Strong Buy | long | up | Return >= neutral band |
| Sell / Reduce / Strong Sell | cash | down | Decline >= neutral band |
| Hold / Hold and Watch / Range-bound Watch / Shakeout Watch / Hold and watch | long | not_down | No significant decline |
| Wait / Observe | cash | flat | Price within neutral band |

### 설정

`.env`에 다음 변수를 설정합니다(모두 선택이며 기본값 있음).

| 변수 | 기본값 | 설명 |
|----------|---------|-------------|
| `BACKTEST_ENABLED` | `true` | daily analysis 후 backtest를 자동 실행할지 여부 |
| `BACKTEST_EVAL_WINDOW_DAYS` | `10` | 평가 window(거래일) |
| `BACKTEST_MIN_AGE_DAYS` | `14` | incomplete data를 피하기 위해 N일보다 오래된 record만 backtest |
| `BACKTEST_ENGINE_VERSION` | `v1` | logic update 시 result를 구분하기 위한 engine version |
| `BACKTEST_NEUTRAL_BAND_PCT` | `2.0` | neutral band threshold(%), ±2%를 range-bound로 취급 |

### 자동 실행

Backtesting은 daily analysis flow가 완료된 뒤 자동 trigger됩니다(non-blocking, 실패해도 notification에 영향 없음). API로 수동 trigger할 수도 있습니다.

### 평가 지표

| Metric | 설명 |
|--------|-------------|
| `direction_accuracy_pct` | 방향 예측 정확도(expected direction이 actual과 일치) |
| `win_rate_pct` | 승률(wins / (wins + losses), neutral 제외) |
| `avg_stock_return_pct` | 평균 stock return percentage |
| `avg_simulated_return_pct` | 평균 simulated execution return(SL/TP exits 포함) |
| `stop_loss_trigger_rate` | stop-loss trigger rate(SL 설정 record만 count) |
| `take_profit_trigger_rate` | take-profit trigger rate(TP 설정 record만 count) |

---

## 로컬 WebUI 관리 인터페이스

WebUI와 FastAPI API는 같은 service process를 공유합니다. 시작 후 browser workspace에서 configuration management, manual analysis, task progress, historical reports, backtesting, portfolio management, smart import를 사용할 수 있습니다. Authentication, cloud-server access, API usage detail은 아래에 정리되어 있습니다.

### FastAPI API Service

FastAPI는 configuration management와 analysis trigger를 위한 RESTful API service를 제공합니다.

### 시작 방법

| 명령 | 설명 |
|------|------|
| `python main.py --serve` | API service 시작 + full analysis 1회 실행 |
| `python main.py --serve-only` | API service만 시작, analysis는 수동 trigger |

### 기능

- **Configuration Management** - 관심 종목 확인/수정
- **UI Language Switch** - login page, shell/navigation, settings page, shared controls에서 UI language(`zh`/`en`) 전환. 이 switch는 `REPORT_LANGUAGE`와 독립적입니다.
- **Quick Analysis** - API로 stock analysis trigger. Home page에는 Docker/server mode에서 background market recap을 시작하는 Market Review 버튼도 있습니다.
- **Strategy selection** - Home page는 analysis strategy skills를 명시적으로 선택할 수 있습니다. `skills`가 생략되면 legacy client의 기존 동작 유지를 위해 server default strategy를 사용합니다.
- **First-run Setup Hint** - Home page는 read-only setup status를 읽고 primary LLM channel이나 watchlist 같은 필수 항목이 누락되면 Settings로 안내합니다.
- **Real-time Progress** - analysis task status가 realtime으로 업데이트되고 parallel task를 지원합니다. regular stock-analysis path는 이제 LLM stage에서 LiteLLM streaming을 선호하고 task SSE를 통해 더 세분화된 `message/progress` update를 push합니다.
- **Recoverable AlphaSift screening** - Screening page는 AlphaSift work를 background task로 제출하고 status를 poll합니다. snapshot, quote, LLM call이 느려도 페이지로 돌아오면 active task progress 또는 final result를 복원합니다.
- **Market Review visibility** - Market Review 클릭 후 API가 `task_id`를 반환하고 UI는 `GET /api/v1/analysis/status/{task_id}`를 poll해 progress를 표시합니다. completed/failure state는 명시적으로 렌더링되고 failure message는 UI error area에 직접 표시됩니다.
- **Market review history dedicated entry** - market review history는 전용 history entry에 표시되고 regular stock history와 분리됩니다. market-review record만 보고 replay하려면 `stock_code=MARKET`, `report_type=market_review`를 사용하세요.
- **Market review history replay** - market review result는 `report_type=market_review`로 저장되며 새 analysis run을 다시 trigger하지 않고 history list/detail 또는 Markdown endpoint에서 직접 다시 열 수 있습니다.
- **Input data-block visibility** - regular analysis report는 history detail, sync response, completed task status를 통해 low-sensitivity `AnalysisContextPack` overview를 노출합니다. Web report page는 Strategy와 News 뒤에 collapsed data-block summary를 표시하며, expansion에서 block status, source, missing reason, fallback summary를 볼 수 있습니다.
- **Ask-stock follow-up context** - historical report에서 Ask Stock을 열면 follow-up message가 active `stock_code/stock_name`을 계속 보냅니다. 기존 chat을 다시 열 때 loaded user message에서 base stock을 복구할 수 있고, comparison-style prompt는 current stock context를 덮어쓰지 않습니다.
- **Backtest Validation** - historical analysis accuracy 평가, direction win rate와 simulated return 조회
- **API Documentation** - Swagger UI는 `/docs`에서 확인

### Product behavior notes

이 기능의 제품 동작은 다음과 같습니다.

- UI language는 report language와 독립적입니다. `dsa.uiLanguage`(browser persistence)는 shell/login/settings text를 제어하고, `REPORT_LANGUAGE`는 report text와 report-page fixed copy(`zh`/`en`)를 제어합니다.
- `dsa.uiLanguage`는 local persistence -> browser language -> default `zh` 순서를 따릅니다.
- 이 변경은 request-scope report language override parameter만 추가합니다. `provider`, `model`, `base_url`, migration/cleanup behavior는 수정하지 않습니다.
- PR-level verification output, screenshots, command logs는 이 사용 가이드가 아니라 PR description에서 유지합니다.

### API Endpoints

| Endpoint | Method | 설명 |
|------|------|------|
| `/api/v1/analysis/analyze` | POST | stock analysis trigger |
| `/api/v1/analysis/market-review` | POST | background market review trigger. request body에 `{"send_notification": true}` 전달 가능. `main.py --market-review` 및 Bot command와 같은 `GeminiAnalyzer/SearchService/NotificationService` construction semantics 공유 |
| `/api/v1/analysis/tasks` | GET | task list 조회 |
| `/api/v1/analysis/tasks/stream` | GET (SSE) | realtime task update 구독 |
| `/api/v1/analysis/status/{task_id}` | GET | task status 조회 |
| `/api/v1/alphasift/screen/tasks` | POST | AlphaSift screening background task 제출(`ALPHASIFT_ENABLED` 먼저 활성화 필요) |
| `/api/v1/alphasift/screen/tasks/{task_id}` | GET | AlphaSift screening task status와 completed result 조회 |
| `/api/v1/history` | GET | analysis history 조회 |
| `/api/v1/history/{record_id}/diagnostics` | GET | historical report run diagnostic summary와 sanitized copy text 조회 |
| `/api/v1/decision-signals` | POST | decision signal을 명시적으로 create 또는 deduplicate하고 `{ item, created }` 반환 |
| `/api/v1/decision-signals` | GET | stock, market, action, phase, source, status, time-range, cache-only holdings filter가 있는 paginated decision-signal query |
| `/api/v1/decision-signals/outcomes/run` | POST | signal outcome evaluation 명시 trigger. 기본적으로 completed/terminal unable row skip, recoverable unable row recompute, `force=true` recompute |
| `/api/v1/decision-signals/outcomes` | GET | paginated signal outcome query |
| `/api/v1/decision-signals/outcomes/stats` | GET | current outcome-engine stats 조회. archived signal은 기본 제외 |
| `/api/v1/decision-signals/{signal_id}/outcomes` | GET | current outcome engine 아래 signal 하나의 outcomes 조회 |
| `/api/v1/decision-signals/{signal_id}/feedback` | GET | signal 하나의 user feedback 조회. 없으면 `feedback_value=null` |
| `/api/v1/decision-signals/{signal_id}/feedback` | PUT | signal 하나의 `useful|not_useful` feedback upsert |
| `/api/v1/decision-signals/{signal_id}` | GET | decision signal 하나를 fetch하고 읽기 전 lazy expiration 적용 |
| `/api/v1/decision-signals/{signal_id}/status` | PATCH | decision signal status와 optional metadata 업데이트 |
| `/api/v1/decision-signals/latest/{stock_code}` | GET | stock의 latest active decision signals 조회 |
| `/api/v1/usage/summary?period=today|month|all` | GET | call type과 model별 LLM call counts 및 token usage 조회 |
| `/api/v1/usage/dashboard?period=today|month|all&limit=50` | GET | token-usage dashboard data 반환: totals, prompt/completion split, model usage, call-type breakdown, recent call records. Web entry는 sidebar Usage page |
| `/api/v1/backtest/run` | POST | backtest trigger |
| `/api/v1/backtest/results` | GET | backtest results 조회(paginated) |
| `/api/v1/backtest/performance` | GET | overall backtest performance 조회 |
| `/api/v1/backtest/performance/{code}` | GET | per-stock backtest performance 조회 |
| `/api/health` | GET | health check |
| `/docs` | GET | API Swagger documentation |

> 참고: `POST /api/v1/analysis/analyze`는 `async_mode=false`일 때 한 종목만 지원합니다. batch `stock_codes`는 `async_mode=true`가 필요합니다. async `202` response는 한 종목이면 단일 `task_id`, batch request면 `accepted` / `duplicates` summary를 반환합니다.
> 참고: `POST /api/v1/analysis/analyze`는 strategy ID 배열로 `skills`를 받습니다. 생략하면 server default를 사용합니다. legacy field `strategies`도 backward compatibility를 위해 계속 받습니다.
> 참고: `POST /api/v1/analysis/analyze`는 `analysis_phase=auto|premarket|intraday|postmarket`를 받으며 기본값은 `auto`입니다. Non-`auto`는 해당 run의 phase와 derived phase flag만 override하고 실제 trading-calendar timestamp를 rewrite하지 않습니다. Accepted responses, in-memory task status, task lists, SSE는 requested phase를 echo하지만 final report phase는 `report.meta.market_phase_summary.phase`로 남습니다.
> 참고: `POST /api/v1/analysis/analyze`는 `report_language=zh|en`(legacy-compatible alias `reportLanguage`)을 받습니다. 생략하면 global `REPORT_LANGUAGE`로 fallback합니다. 이 parameter는 request-scoped이며 response의 `report.meta.report_language`를 포함한 해당 run의 report output language에 영향을 줍니다.
> 참고: Web Home page는 explicit strategy selector를 노출합니다. 사용자가 선택하지 않으면 `skills`를 보내지 않고 legacy behavior를 보존합니다. 선택하면 이 endpoint로 전달되고 task status/history snapshot에 저장됩니다.
> 참고: `POST /api/v1/analysis/market-review`는 CLI/Bot market review와 같은 runtime configuration path(`GeminiAnalyzer(config=...)`, search setup, prompt/rendering pipeline)를 따릅니다. provider compatibility path는 `litellm_model`과 `llm_model_list`를 우선하고, 없으면 기존 legacy keys(`GEMINI_*`, `OPENAI_*`, `ANTHROPIC_*`, `DEEPSEEK_*`)로 fallback합니다. provider name, Base URL, LiteLLM routing semantics는 그 외 변경되지 않습니다.
> 참고: `POST /api/v1/analysis/market-review`도 `report_language=zh|en` / `reportLanguage`를 받아 해당 request의 report language를 설정합니다. 생략하면 global `REPORT_LANGUAGE`로 fallback합니다. Bot/CLI/manual `/market-review` call은 global config를 계속 사용하며 request-level override를 전달하지 않습니다.
> 참고: `POST /api/v1/analysis/market-review`는 명시적 Web/desktop trigger이며 market-review task를 직접 제출합니다. `TRADING_DAY_CHECK_ENABLED=true`이거나 설정된 시장이 그날 닫혀 있어도 short-circuit하지 않습니다. scheduled jobs, GitHub Actions manual runs, CLI defaults는 `--force-run` 또는 workflow `force_run`을 사용하지 않는 한 trading-day gate를 계속 따릅니다.
> Audit note: priority와 fallback은 `src/config.py`의 `Config._load_from_env()`가 정의합니다(`LITELLM_CONFIG` > `LLM_CHANNELS` > legacy). Regression coverage는 `tests/test_llm_channel_config.py`(configuration source parsing)와 `tests/test_market_review_runtime.py`(shared runtime assembly)에 있습니다. endpoint lock은 process/host-level only이므로 multi-instance deployment는 external distributed idempotency control이 여전히 필요합니다.
> 참고: `/api/v1/analysis/market-review`가 완료되면 report는 `report_type=market_review`로 저장됩니다. analysis를 다시 실행하지 않고 보려면 `/api/v1/history`와 `/api/v1/history/{record_id}`(또는 Markdown history endpoints)를 여세요.
> 참고: `/api/v1/analysis/market-review` response와 persisted history에는 `market_scope`, `sections`, `sectors`, `concepts`, `news`, `market_light`, `indices` 같은 field가 있는 structured `market_review_payload`가 포함됩니다. Web rendering과 history detail은 같은 structure를 사용하고, structure가 unavailable일 때만 raw `markdown_report`로 fallback합니다.
> 참고: `market_review_payload.breadth`는 breadth data가 실제로 있을 때만 emit됩니다. usable breadth가 없는 market/feed에서는 field가 생략되고 UI는 misleading zero value가 아니라 `No data`를 표시해야 합니다.
> 참고: `/api/v1/analysis/market-review`가 `task_id`를 반환하면 WebUI는 `GET /api/v1/analysis/status/{task_id}`를 poll합니다. UI는 명확한 `pending/processing` progress를 렌더링하고, status가 `completed`가 되면 completion feedback을 표시하며, `failed`에서는 `error` content를 surface합니다.
> 참고: regular stock history와 섞이지 않으려면 `GET /api/v1/history`에 `stock_code=MARKET&report_type=market_review`를 사용해 market-review-only history를 filter하세요.
> 참고: `GET /api/v1/history/{record_id}/diagnostics`는 history primary key ID 또는 `query_id`를 받고, `normal/degraded/failed/unknown` summary, key pipeline components, sanitized `copy_text`를 반환합니다. `context_snapshot.diagnostics`가 없는 오래된 report는 normal report read에 영향 없이 `unknown`을 반환합니다.
> 참고: `GET /api/v1/history` list summary는 same-stock history용 `stock_code` pagination을 지원하고 optional trend, summary, model, analysis-time price/change field를 포함합니다. persisted snapshot이 없는 오래된 row는 empty value를 반환합니다. Web report page의 "History Trend" drawer는 이 endpoint를 재사용합니다.
> 참고: `GET /api/v1/usage/dashboard`는 기존 `llm_usage` audit table을 재사용하며 configuration key나 database migration을 추가하지 않습니다. persisted call counts, prompt/completion/total token aggregates, model-level usage, recent call records만 반환합니다. model context window나 provider metadata를 추론하지 않습니다.
> Issue #1520 호환성 참고: 여기서 반환되는 `model`/`model_used`는 각 record의 read-only historical snapshot metadata이며 trend drawer/history display에만 사용됩니다. analysis path의 runtime model/model-provider/base URL resolution, config migration, cleanup semantics를 변경하지 않습니다. 롤백은 이 commit을 revert하는 것입니다. history query, API response shape, UI drawer consumption은 compatible하게 유지됩니다.
> 참고: history detail, sync analysis responses, completed task status responses는 `report.details.analysis_context_pack_overview`에서 low-sensitivity input data-block overview를 노출합니다. sync analysis responses는 방금 persisted된 `analysis_history.context_snapshot`에 의존하므로 `SAVE_CONTEXT_SNAPSHOT=false`일 때 새 record가 overview를 보장하지 않습니다. `details.context_snapshot`은 해당 top-level field를 제거하며 full `AnalysisContextPack` 또는 prompt summary를 반환하지 않습니다.
> 참고: `POST /api/v1/agent/chat`와 `POST /api/v1/agent/chat/stream`은 server-side stock-scope resolution 이후 frontend가 제공한 `context.stock_code`를 active Ask Stock baseline으로 사용합니다. 각 turn은 `maintain`, `switch`, `compare`로 분류됩니다. unchanged follow-up은 current stock에 대해서만 stock-scoped tool을 호출할 수 있고, explicit switch는 stale stock summary와 prefetched context를 clear하며, compare/vs/difference 같은 comparison prompt는 current stock을 rewrite하지 않고 해당 turn에서 명시된 code를 허용합니다. model이 TTM, PE, MACD, KDJ 같은 financial abbreviation, moving-average prompt의 `MA` 같은 contextual indicator token, SH/SZ/BJ/HK/SS 같은 exchange fragment로 stock tool을 호출하려 하면 backend는 해당 stock tool을 실행하지 않고 non-retriable `stock_scope_violation` tool result를 반환합니다. Tool name은 exact registry name으로만 resolve되며 provider namespace나 suffix는 기존 tool로 route되지 않습니다.
> 참고: `POST /api/v1/backtest/run`은 candidate를 analysis date range로 filter하는 `analysis_date_from` / `analysis_date_to`(`YYYY-MM-DD`)를 추가합니다. `analysis_date_from > analysis_date_to`이면 400 `invalid_params`를 반환합니다.
> 참고: backtest가 성공적으로 실행됐지만 새 persisted row가 없으면 `BacktestRunResponse.message`는 readable diagnostic을 포함하고 `diagnostics`는 troubleshooting context(예: `empty_reason`, `analysis_date_from`, `analysis_date_to`, `eval_window_days`, `min_age_days`, `limit`)를 반환합니다.
> 참고: `GET /api/v1/backtest/results`, `GET /api/v1/backtest/performance`, `GET /api/v1/backtest/performance/{code}`는 모두 `analysis_date_from`과 `analysis_date_to`를 일관되게 지원합니다. 생략하면 historical default behavior를 유지합니다.

> Compatibility audit evidence:
> - 공식 참고: LiteLLM OpenAI-compatible provider documentation <https://docs.litellm.ai/docs/providers/openai_compatible>, OpenAI Chat API <https://platform.openai.com/docs/api-reference/chat/create>, DeepSeek API docs <https://api-docs.deepseek.com/>.
> - Dependency boundary: 이 repo는 현재 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`을 pin합니다(`requirements.txt` 참고). 이 path의 compatibility regression은 해당 dependency window에서 검증되었습니다.
> - 검증 가능한 tests:
>   - `tests/test_llm_channel_config.py`(configuration priority 및 provider/base URL mapping)
>   - `tests/test_market_review_runtime.py`(`build_market_review_runtime` shared assembly path)
>   - `tests/test_analysis_api_contract.py`(`/api/v1/analysis/market-review` contract 및 task status flow)
> - 롤백 경로: regression이 나타나면 historical `LITELLM_MODEL`, `LITELLM_FALLBACK_MODELS`, legacy `GEMINI_*` / `OPENAI_*` / `ANTHROPIC_*` / `DEEPSEEK_*`를 복원하거나 `POST /api/v1/system/config/import`로 desktop backup을 import하고 재시작하세요. runtime에서는 `LITELLM_CONFIG` / `LLM_CHANNELS`를 clear해 legacy fallback을 강제할 수도 있습니다.

> Progress-stream note: `GET /api/v1/analysis/tasks/stream`은 이제 `task_created / task_started / task_completed / task_failed` 외에 `task_progress`도 emit합니다. regular analysis path는 quote preparation, news retrieval, context assembly, LLM generation, report persistence 전반에서 `progress`와 `message`를 업데이트합니다. streaming chunk는 server side에만 accumulate됩니다. history는 final JSON parse가 성공한 뒤에만 저장됩니다. 첫 chunk 전에 streaming을 사용할 수 없으면 system은 이전 non-stream request로 fallback합니다. partial output이 이미 도착한 뒤 stream이 실패하면 system은 먼저 같은 model에 대해 non-stream retry를 하고, 이후 기존 fallback model을 원래 순서(primary + fallback list)대로 계속 진행합니다.
> progress callback이 실패해도 analysis flow는 계속되고, SSE delivery gap troubleshooting을 돕기 위해 exception은 warning level로 log됩니다.

> 참고: 이 동작은 상세 runtime SSE/fallback behavior이므로 README가 아니라 full guide(`full-guide*.md`)에 문서화되어 있습니다.

**사용 예시**:
```bash
# Health check
curl http://127.0.0.1:8000/api/health

# Trigger analysis (A-shares)
curl -X POST http://127.0.0.1:8000/api/v1/analysis/analyze \
  -H 'Content-Type: application/json' \
  -d '{"stock_code": "600519"}'

# pass strategy list (optional)
curl -X POST http://127.0.0.1:8000/api/v1/analysis/analyze \
  -H 'Content-Type: application/json' \
  -d '{"stock_code": "600519", "skills": ["bull_trend", "growth_quality"]}'

# Query task status
curl http://127.0.0.1:8000/api/v1/analysis/status/<task_id>

# Query today's LLM usage
curl "http://127.0.0.1:8000/api/v1/usage/summary?period=today"

# Query today's LLM usage dashboard
curl "http://127.0.0.1:8000/api/v1/usage/dashboard?period=today&limit=50"

# Trigger backtest (all stocks)
curl -X POST http://127.0.0.1:8000/api/v1/backtest/run \
  -H 'Content-Type: application/json' \
  -d '{"force": false}'

# Trigger backtest (specific stock)
curl -X POST http://127.0.0.1:8000/api/v1/backtest/run \
  -H 'Content-Type: application/json' \
  -d '{"code": "600519", "force": false}'

# Query overall backtest performance
curl http://127.0.0.1:8000/api/v1/backtest/performance

# Query per-stock backtest performance
curl http://127.0.0.1:8000/api/v1/backtest/performance/600519

# Paginated backtest results
curl "http://127.0.0.1:8000/api/v1/backtest/results?page=1&limit=20"
```

### Custom Configuration

기본 port를 수정하거나 LAN access를 허용하려면:

```bash
python main.py --serve-only --host 0.0.0.0 --port 8888
```

### 지원 종목 코드 형식

| 유형 | 형식 | 예시 |
|------|------|------|
| A주 | 6자리 숫자 | `600519`, `000001`, `300750` |
| BSE(베이징) | 8/4/92 prefix, 6자리. `BJ` prefix 또는 `.BJ` suffix 지원 | `920748`, `BJ920493`, `920493.BJ` |
| HK stocks | hk + 5자리 숫자 | `hk00700`, `hk09988` |
| US stocks | 1-5 letters, optional `.X` suffix | `AAPL`, `TSLA`, `BRK.B` |
| Japanese stocks | Yahoo `.T` suffix | `7203.T`, `6758.T` |
| Korean stocks | Yahoo `.KS` / `.KQ` suffix | `005930.KS`, `035720.KQ` |

### 참고

- Browser access: `http://127.0.0.1:8000`(또는 설정한 port)
- 분석 완료 후 설정된 채널로 notification이 자동 push됩니다.
- 이 기능은 GitHub Actions 환경에서 자동으로 비활성화됩니다.

---

## FAQ

### Q: Push message가 잘리나요?
A: WeChat Work/Feishu에는 message length limit이 있으며, system은 이미 message를 자동 분할합니다. 전체 내용을 보려면 Feishu Cloud Document 기능을 설정하세요.

### Q: Data fetch가 실패했나요?
A: AkShare는 scraping mechanism을 사용하므로 일시적으로 rate-limit될 수 있습니다. system에는 retry mechanism이 설정되어 있으므로 보통 몇 분 기다렸다가 재시도하면 됩니다.

### Q: 관심 종목은 어떻게 추가하나요?
A: `STOCK_LIST` 환경 변수를 수정하고 여러 code는 쉼표로 구분하세요.

### Q: GitHub Actions가 실행되지 않나요?
A: Actions가 활성화되어 있는지, cron expression이 올바른지 확인하세요(UTC time이라는 점 주의).

---

## Portfolio Web Notes

### `/portfolio`의 portfolio account archive

- `/portfolio` account toolbar는 기존 `DELETE /api/v1/portfolio/accounts/{account_id}` endpoint를 통해 선택된 단일 account를 삭제할 수 있습니다.
- Account deletion은 soft-delete/archive semantics를 사용합니다. Archived account는 default account lists, portfolio snapshots, risk summaries, entry forms, event lists에서 숨겨집니다.
- Historical trade, cash-ledger, corporate-action, daily snapshot row는 물리적으로 제거되지 않습니다. Web UI에서 특정 ledger row를 수정하려면 account를 archive하기 전에 해당 row를 삭제하세요.

### `/portfolio`의 manual FX refresh

- Web `/portfolio` page의 FX status card에는 manual refresh action이 포함됩니다.
- 버튼은 기존 `POST /api/v1/portfolio/fx/refresh` endpoint를 호출하고 snapshot/risk data만 reload합니다.
- upstream FX fetch가 실패하면 refresh 후에도 page가 stale로 남을 수 있으며 fallback result를 inline으로 설명합니다.
- `PORTFOLIO_FX_UPDATE_ENABLED=false`이면 refresh API는 explicit disabled status를 반환하고, page는 refreshable pair가 없다고 암시하지 않고 online FX refresh가 disabled임을 표시합니다.
- Portfolio snapshot `positions[]`는 `price_source`, `price_date`, `price_stale`, `price_available` 같은 price metadata를 포함합니다. 오늘 snapshot은 realtime quote를 먼저 시도하고, realtime quote가 unavailable 또는 non-positive이면 `as_of` 이전 최신 historical close로 fallback합니다. Historical `as_of` snapshot은 historical-close semantics를 유지하며 cost basis를 current price로 조용히 취급하지 않습니다. missing-price position은 `price_available=false`로 표시되고 market value / unrealized PnL total에서 제외됩니다.

## Agent Tool Data Cache And Persistence

- `get_daily_history`는 먼저 local `stock_daily` daily-bar cache 재사용을 시도합니다. cache가 fresh하고 dashboard default인 30 records 이상을 포함하면 추가 external data-source request를 피합니다.
- Agent가 local cache보다 더 많은 day를 요청하면 tool은 available record를 반환하고 response에 `partial_cache=true`, `requested_days`, `actual_records`를 표시합니다.
- cache가 없거나 stale이면 tool은 기존 data-source fetch path를 유지합니다. 성공한 fetch는 best-effort로 `stock_daily`에 write back되고, write failure는 Agent response를 막지 않습니다.
- `search_stock_news`와 `search_comprehensive_intel`은 성공한 result를 best-effort로 `news_intel`에 저장하며, 기존 URL / fallback-key deduplication logic을 재사용합니다.
- Stock news search는 이제 relevance ranking 후 domain-agnostic admission filter를 적용합니다. obvious download/install/app-rating page와 adult/escort spam page를 제거하고, 같은 batch에 direct-stock 또는 scored sector/market candidate가 이미 있으면 zero-score filler result를 drop합니다. 이는 hard-coded website blocklist가 아닙니다.
- 이 admission-filter 변경은 retrieval post-filtering에만 격리되어 있으며 model name, provider settings, Base URL, LiteLLM route semantics, runtime config migration/cleanup behavior를 바꾸지 않습니다.
- `get_realtime_quote`는 `stock_daily`를 realtime-quote cache로 사용하지 않고 intraday quote를 daily-bar table에 쓰지 않습니다. realtime quote caching이 필요하면 dedicated realtime store를 사용해야 합니다.

## Agent Event Monitor

`AGENT_EVENT_MONITOR_ENABLED=true`이면 schedule mode는 `AGENT_EVENT_MONITOR_INTERVAL_MINUTES`분마다 alert worker를 실행합니다. worker는 Alert API를 통해 생성된 enabled rule을 읽고, `AGENT_EVENT_ALERT_RULES_JSON`의 legacy rule도 계속 지원합니다. triggered alert는 기존 notification channel을 통해 전송됩니다. Alert API / Web persisted rule은 price, change-percent, volume, daily technical indicators, `watchlist`, `portfolio_holdings`, `portfolio_account`, `market` Market Light target을 지원합니다. legacy JSON은 여전히 세 가지 basic rule type만 지원합니다.

> 호환성 및 롤백 참고: 이 섹션은 `price_change_percent`를 포함한 현재 Event Monitor rule behavior를 문서화하며, model names, providers, Base URL, LiteLLM, `OPENAI_*`, `DEEPSEEK_*`, `GEMINI_*` configuration 같은 external model/provider API semantics를 변경하지 않습니다.
> Legacy JSON은 자동으로 migrate, delete, rewrite되지 않습니다. background alert worker를 rollback하려면 `AGENT_EVENT_MONITOR_ENABLED`/관련 rule config를 clear하거나 disable하세요.

| `alert_type` | Direction | Threshold | 설명 |
| --- | --- | --- | --- |
| `price_cross` | `above` / `below` | `price` | current price가 fixed threshold를 cross |
| `price_change_percent` | `up` / `down` | `change_pct` | intraday change percentage가 threshold에 도달 |
| `volume_spike` | - | `multiplier` | latest volume이 최근 20일 평균의 이 multiplier를 초과 |
| `ma_price_cross` | `above` / `below` | `window` | daily close가 MA(window)를 edge-cross |
| `rsi_threshold` | `above` / `below` | `period`, `threshold` | RSI가 threshold를 edge-cross |
| `macd_cross` | `bullish_cross` / `bearish_cross` | `fast_period`, `slow_period`, `signal_period` | DIF/DEA edge golden/death cross |
| `kdj_cross` | `bullish_cross` / `bearish_cross` | `period`, `k_period`, `d_period` | K/D edge golden/death cross |
| `cci_threshold` | `above` / `below` | `period`, `threshold` | CCI가 threshold를 edge-cross |
| `portfolio_stop_loss` | `mode=near|breach` | - | account-level stop-loss proximity 또는 breach |
| `portfolio_concentration` | - | - | account-level symbol concentration |
| `portfolio_drawdown` | - | - | account-level maximum drawdown alert |
| `portfolio_price_stale` | - | - | stale 또는 missing portfolio prices |
| `market_light_status` | - | `statuses` | current Market Light status가 설정된 `red/yellow` list와 match |
| `market_light_score_drop` | - | `min_drop` | Market Light score가 previous trading day 대비 threshold 이상 하락 |

예시:

```env
AGENT_EVENT_MONITOR_ENABLED=true
AGENT_EVENT_MONITOR_INTERVAL_MINUTES=5
AGENT_EVENT_ALERT_RULES_JSON=[{"stock_code":"600519","alert_type":"price_cross","direction":"above","price":1800},{"stock_code":"300750","alert_type":"price_change_percent","direction":"down","change_pct":3.0},{"stock_code":"000858","alert_type":"volume_spike","multiplier":2.5}]
```

worker는 evaluation history로 `triggered`, `skipped`, `degraded`, `failed` row를 `alert_triggers`에 씁니다. 일반 non-triggered check는 history를 쓰지 않습니다. DB-persisted rule의 경우 `triggered` history는 `rule_id + target + data_source + data_timestamp`로 best-effort deduplicate됩니다. 같은 data point에 대한 반복 hit는 가장 이른 trigger row를 재사용하고, `data_timestamp`가 없는 record는 deduplicate되지 않습니다. 실제 trigger는 per-channel attempt를 `alert_notifications`에 쓰고, Alert API persisted rule은 business cooldown state를 `alert_cooldowns`에 씁니다. persisted cooldown read가 실패하면 worker는 DB failure 중 반복 notification을 피하기 위해 일시적으로 in-process fingerprint guard로 fallback합니다. Legacy `AGENT_EVENT_ALERT_RULES_JSON` rule은 in-process fingerprint suppressor를 계속 사용하며 persisted cooldown state를 쓰지 않습니다. notification infrastructure `notification_noise.py` guard는 독립적으로 유지됩니다. Web rule list는 rule이 cooling down 중인지 판단할 때 browser-local timezone parsing 대신 backend-provided `cooldown_active` flag를 사용합니다.

Technical indicator rule은 daily-close edge trigger만 사용합니다. Partial-bar handling은 server-local-time + 16:00 heuristic이며 market-calendar precision을 구현하지 않습니다. `watchlist` rule은 각 worker run마다 `STOCK_LIST`를 refresh하고 expand합니다. `portfolio_holdings`는 non-zero snapshot positions를 symbol de-duplication과 함께 expand하고, `portfolio_account`는 account-level aggregate evaluation에 portfolio risk service를 재사용합니다. `market` rule은 `cn|hk|us` target만 받고 structured `MarketLightSnapshot` data를 사용합니다. `trade_date`는 current market overview에서 가져오며, `data_quality=unavailable`은 triggering을 건너뛰고, non-trading day는 trading-day gate로 skip되며, `market_light_score_drop`은 trading day끼리만 score를 비교합니다. WebUI "Alerts" page는 persisted rule 관리, one-shot dry-run test 실행, trigger history, notification attempt, read-only cooldown state 조회를 할 수 있습니다. batch rule의 cooldown은 parent-rule summary이고, child-target cooldown detail은 trigger history에서 볼 수 있습니다. 자세한 경계는 [실시간 알림 센터](alerts.md)를 참고하세요.

---

더 궁금한 점은 [Issue를 제출](https://github.com/ZhuLinsen/daily_stock_analysis/issues)해 주세요.
