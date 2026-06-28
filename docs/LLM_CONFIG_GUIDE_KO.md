# LLM 설정 가이드

환영합니다. AI를 처음 접하는 초보자든 다양한 API에 익숙한 사용자든, 이 가이드는 Large Language Model(LLM)을 빠르게 설정할 수 있도록 돕습니다.

이 프로젝트는 공식 API, OpenAI 호환 플랫폼, 로컬 모델을 지원하는 통합 AI 모델 접근 흐름을 제공합니다. 내부적으로는 [LiteLLM](https://docs.litellm.ai/)을 사용하지만, 대부분의 사용자는 공급자를 고르고 API 키를 추가한 뒤 필요하면 기본 모델이나 채널을 선택하는 정도만 이해하면 됩니다. 경험 수준에 맞게 3단계 설정 체계를 제공합니다. 자신에게 맞는 방법을 선택하세요.

구체적인 공급자를 선택하거나, GitHub Actions Secrets / Variables를 설정하거나, `details.reason` 오류를 해결하거나, LLM 설정을 롤백해야 한다면 [공급자 설정 가이드](./llm-providers.md)부터 보세요. 공급자 preset, Actions 변수 매핑, 런타임 capability check 경계, 일반적인 오류 처리에 대한 유지보수 기준 문서입니다.

---

## 빠른 탐색: 어떤 섹션을 읽어야 하나요?

1. **[초보자]** "최대한 단순하게, 일단 시스템을 빨리 실행하고 싶어요!" -> [방법 1: 단순 모델 설정](#방법-1-단순-모델-설정초보자용)
2. **[고급 사용자]** "키가 여러 개 있고 fallback 모델과 custom Base URL을 설정하고 싶어요." -> [방법 2: 채널 모드 설정](#방법-2-채널-모드-설정고급다중-모델)
3. **[전문 사용자]** "복잡한 load balancing, request routing, enterprise급 고가용성을 원해요!" -> [방법 3: 고급 YAML 설정](#방법-3-고급-yaml-설정전문가용)
4. **[로컬 모델]** "Ollama 로컬 모델을 쓰고 싶어요!" -> [예시 4: Ollama 로컬 모델 사용](#예시-4-ollama-로컬-모델-사용)
5. **[Vision 모델]** "이미지에서 종목 코드를 추출하고 싶어요!" -> [Vision 모델 설정](#고급-기능-vision-모델-설정)

---

## 생성 백엔드(Phase 2)

생성 백엔드는 일반 종목 분석, 시장 리뷰, `generate_text()`를 위한 외부 런타임 선택자입니다. 기본값은 여전히 `litellm`이며 regression은 없습니다. `codex_cli`는 명시적으로 opt-in해야 하는 로컬 CLI 백엔드이고 현재는 **실험적/제한적**입니다.

```env
GENERATION_BACKEND=litellm
GENERATION_FALLBACK_BACKEND=litellm
GENERATION_BACKEND_TIMEOUT_SECONDS=300
GENERATION_BACKEND_MAX_OUTPUT_BYTES=1048576
GENERATION_BACKEND_MAX_CONCURRENCY=1
LOCAL_CLI_BACKEND_MAX_CONCURRENCY=1
AGENT_GENERATION_BACKEND=auto
```

- `GENERATION_BACKEND=litellm|codex_cli`. `codex_cli`는 생성 백엔드이지 LiteLLM 공급자가 아닙니다. `LITELLM_MODEL=codex_cli/...`로 설정하지 마세요.
- `GENERATION_FALLBACK_BACKEND`가 설정되지 않으면 기본값은 `litellm`입니다. 로컬 `.env`에서 명시적으로 빈 값을 넣으면 backend-level fallback이 비활성화됩니다. fallback이 primary backend와 같으면 no-op으로 취급됩니다. 번들 GitHub Actions workflow는 이 변수가 설정되지 않았을 때 명시적으로 `litellm`을 export합니다. Actions에서 backend fallback을 끄려면 `GENERATION_BACKEND=codex_cli` + `GENERATION_FALLBACK_BACKEND=codex_cli`처럼 fallback을 primary backend와 같게 설정하세요.
- `GENERATION_BACKEND=codex_cli`에서는 일반 분석과 시장 리뷰에 Gemini/OpenAI/Anthropic/DeepSeek API 키가 필요 없습니다. `codex` 실행 파일이 없으면 DSA는 “API key not configured” 대신 구조화된 `command_not_found`를 반환합니다.
- 현재 `codex_cli` preset은 `codex exec --output-last-message <temp-file> -`를 통해 최종 응답을 읽습니다. Codex CLI는 같은 최종 응답을 stdout에도 출력합니다. DSA는 stdout diagnostics preview와 output-size accounting에서 이 중복을 제거하고, main-analysis JSON parsing에는 stdout을 사용하지 않습니다. 공식 참고: [Codex non-interactive mode](https://developers.openai.com/codex/noninteractive), [Codex CLI command line options](https://developers.openai.com/codex/cli/reference). 이 저장소는 현재 `codex-cli 0.142.0`만 검증하며 더 넓은 최소 버전 범위를 주장하지 않습니다. 설치된 CLI가 preset 인자를 지원하지 않으면 DSA는 구조화된 `non_zero_exit` / `cli_contract_unsupported` 진단을 반환하고, backend fallback이 설정되어 있으면 `litellm`으로 fallback합니다.
- `codex_cli`는 streaming을 지원하지 않습니다. Stream 요청은 non-stream으로 degrade되며 `capability_unsupported`를 반환하지 않습니다.
- 로컬 CLI 사용은 일반적으로 unavailable입니다. DSA는 가짜 0-token, 가짜 비용, 가짜 cache telemetry를 저장하지 않습니다.
- 로컬 CLI 실행에는 hard cap이 있습니다. `GENERATION_BACKEND_TIMEOUT_SECONDS` 최대 `3600`, `GENERATION_BACKEND_MAX_OUTPUT_BYTES` 최대 `33554432`, `GENERATION_BACKEND_MAX_CONCURRENCY` 최대 `16`, `LOCAL_CLI_BACKEND_MAX_CONCURRENCY` 최대 `4`입니다. 진단 stdout/stderr와 최종 응답은 함께 계산됩니다. `--output-last-message` preset에서는 stdout에 중복 출력된 최종 응답을 두 번 계산하지 않고 `stdout_preview`에도 노출하지 않습니다.
- 로컬 CLI 기본 동시성은 1입니다. 실제 로컬 CLI 동시성은 `min(LOCAL_CLI_BACKEND_MAX_CONCURRENCY, GENERATION_BACKEND_MAX_CONCURRENCY)`이며 `MAX_WORKERS`를 상속하지 않습니다.
- `AGENT_GENERATION_BACKEND=auto`는 `GENERATION_BACKEND=codex_cli`를 무작정 상속하지 않습니다. Agent tool calling은 LiteLLM에 남아 있습니다. Web 설정 페이지는 `auto|litellm`만 노출합니다. 손으로 `AGENT_GENERATION_BACKEND=codex_cli`를 작성해도 Phase 2에서 Agent text-only mode가 활성화되지 않으며 명시적인 unsupported tool-calling 진단을 반환합니다.

### Codex CLI 개인정보 및 경계

- 로컬 CLI 백엔드는 오프라인 모델이 아닙니다. Codex CLI 뒤의 서비스가 종목 코드, 뉴스, 포지션 컨텍스트, 분석 프롬프트, 리포트 초안을 처리할 수 있습니다.
- Docker, 클라우드 서버, CI에는 로컬 CLI 로그인 상태가 자동으로 존재하지 않습니다.
- GitHub Actions는 설정값만 전달합니다. Codex CLI를 설치하거나 로그인하지 않습니다. Actions에서 `GENERATION_BACKEND=codex_cli`를 opt-in했는데 runner에 실행 파일이나 로그인 상태가 없으면 구조화된 실패를 반환해야 합니다.
- DSA는 Codex credential 파일을 읽지 않지만, subprocess는 CLI 자체 로그인 상태를 사용할 수 있습니다.
- Web 설정 페이지는 안전한 preset만 노출하며 임의 command, argv, shell string을 받지 않습니다.
- `codex_cli`는 계속 실험적/제한적입니다. CLI 버전이 안정적인 non-interactive `--output-last-message` 출력을 지원하지 않으면 `GENERATION_BACKEND=litellm`을 유지하세요.

## 방법 1: 단순 모델 설정(초보자용)

**목표:** API Key와 모델명만 붙여 넣고 바로 사용합니다. 복잡한 개념을 다룰 필요가 없습니다.

단일 모델만 사용할 계획이라면 이 방법이 가장 빠릅니다. 프로젝트 루트 디렉터리의 `.env` 파일을 여세요. 없다면 `.env.example`을 복사해 `.env`로 이름을 바꾸세요.

### Anspire Open 예시:

> 💡 **[Anspire Open](https://open.anspire.cn/?share_code=QFBC0FYC)**: 공유 키로 중국어 최적화 검색과 OpenAI 호환 모델 접근을 지원합니다.
> - 아래 값은 설정 예시일 뿐이며, 모델 사용 가능 여부는 계정과 Anspire console에 따라 달라집니다.
> - 문서 예시는 연결성 검증을 대체하지 않습니다. production traffic에 의존하기 전에 Web의 "Test connection" 흐름으로 검증하세요.

```env
# Anspire Open API keys (multiple keys supported, separated by commas)
# Get your key at: https://open.anspire.cn/?share_code=QFBC0FYC
# When no higher-priority OpenAI-compatible source is set, this key is reused for Anspire search + LLM path (example fallback behavior only).
# Example model: Doubao-Seed-2.0-lite; example gateway: https://open-gateway.anspire.cn/v6
ANSPIRE_API_KEYS=sk-xxxxxxxxxxxxxxxx
# Optional: switch example model or gateway according to your Anspire account and official docs.
# ANSPIRE_LLM_MODEL=Doubao-Seed-2.0-pro
# ANSPIRE_LLM_BASE_URL=https://open-gateway.anspire.ai/v6
```

### 예시 1: 타사 OpenAI 호환 플랫폼 사용(강력 권장)

대부분의 타사 relay 플랫폼과 로컬 API 공급자는 OpenAI interface 형식을 지원합니다. 플랫폼이 API Key와 Base URL을 제공한다면 다음 패턴으로 쉽게 설정할 수 있습니다.

```env
# Fill in the API Key provided by your platform
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
# Fill in the platform's API Base URL (Very Important: Usually must end with /v1)
OPENAI_BASE_URL=https://api.siliconflow.cn/v1
# Fill in the specific model name (Very Important: You must add the "openai/" prefix so the system recognizes it)
LITELLM_MODEL=openai/deepseek-ai/DeepSeek-V3 
```

### 예시 2: 공식 DeepSeek API 사용
```env
# Fill in the API Key requested from the official DeepSeek platform
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxx
```
*호환성 참고: 이 줄만 있어도 시스템은 여전히 기본값 `deepseek/deepseek-chat`을 사용하고 migration warning을 기록합니다.*
`deepseek-chat` / `deepseek-reasoner`는 예전 설정과의 호환을 위해 계속 작동하지만, DeepSeek는 2026/07/24 이후 이를 deprecated로 표시합니다. 새 설정은 Web quick channel을 통해 마이그레이션하거나 `deepseek-v4-flash` / `deepseek-v4-pro`용으로 `LITELLM_MODEL=deepseek/deepseek-v4-flash`를 명시적으로 설정해야 합니다.

### 예시 3: 무료 Gemini API 사용
```env
# Fill in your Google Gemini Key
GEMINI_API_KEY=AIzac...
```

### 예시 4: Ollama 로컬 모델 사용
```env
# Ollama requires no API Key; works after running ollama serve locally
OLLAMA_API_BASE=http://localhost:11434
LITELLM_MODEL=ollama/qwen3:8b
```

> **중요**: Ollama는 반드시 `OLLAMA_API_BASE`로 설정해야 합니다. `OPENAI_BASE_URL`을 사용하지 마세요. 그러면 시스템이 URL을 잘못 이어 붙일 수 있습니다(예: 404, `api/generate/api/show`). 원격 Ollama는 실제 주소(예: `http://192.168.1.100:11434`)를 `OLLAMA_API_BASE`에 설정하세요. 현재 의존성 제약은 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`입니다(`requirements.txt`와 일치).

> **축하합니다! 초보자라면 여기서 읽기를 멈추고 프로그램을 실행해도 됩니다.**
> 연결을 테스트하고 싶다면 루트 디렉터리에서 터미널을 열고 `python scripts/check_env.py --llm`을 실행하세요.

---

## 방법 2: 채널 모드 설정(고급/다중 모델)

**목표:** 여러 플랫폼의 키를 함께 사용합니다. 기본 모델이 실패하거나 네트워크가 끊기면 fallback 모델로 자동 전환되게 하고 싶습니다.

**Web UI에서 직접 설정:** 애플리케이션 시작 후 Web UI의 **System Settings -> AI Model -> AI Model Access**에서 시각적으로 설정할 수 있습니다.

> **새 editor 동작**: DeepSeek, DashScope 등 `/v1/models`를 노출하는 OpenAI 호환 공급자의 경우, 설정 페이지가 `{base_url}/models`에서 모델을 직접 가져와 여러 항목을 시각적으로 선택할 수 있습니다. 내부 저장 형식은 여전히 기존 쉼표 구분 값 `LLM_{CHANNEL}_MODELS=model1,model2`입니다. 공급자가 `/models`를 지원하지 않거나, 인증 실패 또는 endpoint 일시 장애가 있으면 모델 목록을 수동 입력해 정상 저장할 수 있습니다.

### 최초 실행 설정 상태

백엔드는 읽기 전용 상태 endpoint `GET /api/v1/system/config/setup/status`를 제공합니다. primary LLM, Agent 모델 상속/설정, 종목 목록, 선택적 알림 채널, 로컬 스토리지처럼 최초 실행에 필요한 최소 요소가 있는지 보고합니다. 이 endpoint는 저장된 `.env`와 현재 프로세스 환경만 읽습니다. 런타임 설정을 reload하거나, `.env`를 쓰거나, 실제 모델을 테스트하거나, 데이터베이스 파일을 만들지 않습니다. Frontend onboarding과 이후 smoke-run 흐름은 이 endpoint를 기반으로 점진적으로 확장할 수 있습니다.

### Web channel editor: 호환성, 마이그레이션, 롤백 규칙

- preset provider / Base URL / sample models는 **form defaults only**입니다. 실제 저장되는 것은 `LLM_{CHANNEL}_PROTOCOL`, `LLM_{CHANNEL}_BASE_URL`, `LLM_{CHANNEL}_MODELS`, `LLM_{CHANNEL}_API_KEY(S)`에 제출한 값 그대로입니다. editor가 이를 다른 provider name이나 URL로 조용히 다시 쓰지 않습니다.
- "Discover models"는 `OpenAI Compatible` / `DeepSeek` 채널에 대해서만 `{base_url}/models`를 호출합니다. 기본 "Test connection" 동작은 목록의 첫 모델에 대해 최소 chat completion 요청을 보내고 결과에 backend-normalized `resolved_model`을 표시합니다. 응답에 `details.reason=model_access_denied`가 포함되면(예: 관찰된 Issue #1208 SiliconFlow / OpenAI Compatible sample이 LiteLLM을 통해 `Model disabled`를 반환), 공급자 문구에 기반한 best-effort 모델 가용성 진단으로 보세요. 먼저 테스트 모델이 현재 계정/키에서 활성화되어 있는지 확인하고, 재시도 전에 모델 순서를 조정하거나 사용할 수 없는 모델을 제거하세요. 이 보수적 규칙에 포함되지 않는 공급자 메시지나 의미가 다른 메시지는 fallback 진단 경로를 계속 사용합니다. 선택적 runtime capability check는 사용자가 명시적으로 선택해야 하며 추가 JSON / tools / stream / vision smoke 요청을 보냅니다. 결과는 그 순간의 계정, 모델, endpoint에 대한 best-effort check일 뿐입니다. 반환된 `stage / error_code / details / latency_ms / capability_results` 필드는 구조화 진단용이며, `.env`에 **절대 저장되지 않고** 저장을 막지 않습니다.
- 응답에 `details.reason=provider_blocked`가 포함되면 공급자 또는 relay gateway가 이 요청을 명시적으로 차단한 것입니다. 이는 로컬 네트워크 / TLS 실패 및 `model_access_denied`와 다릅니다. 먼저 계정 risk control, 지역 또는 요청 출처 제한, 모델 entitlement, relay gateway policy, content-safety policy를 확인하세요.
- Runtime capability check는 실제 LLM 요청을 보내며 token / image-input 비용, RPM/TPM rate limit, 잔액 부족 오류, timeout이 발생할 수 있습니다. check 실패는 계정 권한, 모델 entitlement, endpoint 지역, 잔액, 공급자 호환 layer, LiteLLM translation 동작에서 비롯될 수 있으며, 공급자가 전역적으로 해당 capability를 지원하지 않는다는 증거는 아닙니다. P3는 모든 실제 공급자에 대한 online smoke coverage를 포함하지 않습니다. 호환성 근거는 저장소 의존성 제약 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`, LiteLLM `completion()` / OpenAI I/O format / streaming / exception mapping, 그리고 JSON mode, tool calling, streaming, vision input에 대한 OpenAI Chat Completions shape입니다.
- 외부 참고: LiteLLM Python SDK / OpenAI I/O format / streaming / exception mapping: <https://docs.litellm.ai/>; LiteLLM OpenAI-compatible routing: <https://docs.litellm.ai/docs/providers/openai_compatible>; OpenAI Chat Completions: <https://platform.openai.com/docs/api-reference/chat/create>; JSON mode: <https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat>; tool calling: <https://platform.openai.com/docs/guides/function-calling?api-mode=chat>; streaming: <https://platform.openai.com/docs/guides/streaming-responses?api-mode=chat>; vision input: <https://platform.openai.com/docs/guides/images-vision?api-mode=chat>.
- 채널 저장은 해당 저장 작업에서 제출한 키만 업데이트합니다. 채널 설정을 전환할 때 whole-config silent migration은 없습니다. 의도된 cleanup은 runtime model reference뿐입니다. `LITELLM_MODEL`, `AGENT_LITELLM_MODEL`, `VISION_MODEL`, `LITELLM_FALLBACK_MODELS`가 현재 활성 채널에 더 이상 존재하지 않는 모델을 가리키면, editor는 저장 전에 stale reference를 clear/remove하여 런타임 호출이 invalid model을 계속 target하지 않도록 합니다. 활성 채널이 selectable model을 전혀 노출하지 않아도, 일치하는 legacy key가 없는 stale managed-provider 값은 cleanup됩니다. `cohere/*`, `google/*`, `xai/*`는 legacy retention 동작을 설명하는 explicit direct-env compatibility 예시로만 유지되며 runtime availability guarantee가 아닙니다.
- Backend consistency 근거: `SystemConfigService._validate_llm_runtime_selection`(`src/services/system_config_service.py`)의 runtime validation은 `_uses_direct_env_provider`(`src/config.py`)에 의존합니다. `gemini`, `vertex_ai`, `anthropic`, `openai`, `deepseek`만 managed key-backed provider로 취급됩니다. `cohere`, `google`, `xai`는 allowlist에 없으므로 valid direct provider runtime entry로 남습니다.
- 롤백은 최소로 유지됩니다. 이전 channel model list를 복원하고 runtime model을 다시 선택하거나, desktop export / 수동 `.env` backup에서 이전 `LLM_*`, `LITELLM_MODEL`, `AGENT_LITELLM_MODEL`, `VISION_MODEL`, `LLM_TEMPERATURE`, `LLM_USAGE_HMAC_*` 값을 복원하세요. 추가 migration script는 필요 없습니다.
- 이 흐름의 현재 저장소 의존성 제약은 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`입니다(`requirements.txt` 참고). Regression coverage는 `tests/test_system_config_service.py`, `tests/test_system_config_api.py`, `apps/dsa-web/src/components/settings/__tests__/LLMChannelEditor.test.tsx`에 있습니다.

> **외부 공급자 모델 예시 안내**: `cohere/*`, `google/*`, `xai/*` provider-prefixed 값은 현재 runtime retention 동작을 설명하기 위해서만 포함되며 **전역 가용성 보장이 아닙니다**. 문서나 테스트의 특정 모델명은 configuration-retention 예시이지 production recommendation이 아닙니다. production 사용 전 공급자의 공식 모델/API 문서를 확인하고 저장소 의존성 제약 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`에서 검증하세요.

### 롤백 및 호환성 증거

- `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`에서 범위와 cleanup 동작: 저장 중 runtime reference(`LITELLM_MODEL`, `AGENT_LITELLM_MODEL`, `VISION_MODEL`, `LITELLM_FALLBACK_MODELS`)만 sanitize됩니다. `cohere/*`, `google/*`, `xai/*` 같은 non-channel direct provider는 보존됩니다.
- 롤백 경로: desktop config를 export한 뒤 `POST /api/v1/system/config/import`로 backup을 restore하세요. 또는 과거 `.env` 항목(`LITELLM_*`, `AGENT_LITELLM_MODEL`, `VISION_MODEL`, `LLM_TEMPERATURE`, `LLM_USAGE_HMAC_*`)을 수동 복원하고 재시작하세요.
- 롤백 증거: `tests/test_system_config_service.py::test_import_desktop_env_restores_runtime_models_after_cleanup`는 runtime cleanup 후 export된 desktop backup에서 restore하는 경로를 다룹니다.
- Direct-provider 증거: `tests/test_system_config_service.py::SystemConfigServiceTestCase::test_validate_accepts_minimax_model_as_direct_env_provider`, `test_validate_accepts_cohere_model_as_direct_env_provider`, `test_validate_accepts_google_model_as_direct_env_provider`, `test_validate_accepts_xai_model_as_direct_env_provider`는 보존되는 direct-provider 동작을 다룹니다.
- Frontend regression commands: `cd apps/dsa-web && npm run lint && npm run build && npm run test -- src/components/settings/__tests__/LLMChannelEditor.test.tsx`.
- 권장 롤백 순서(UI reload 포함): desktop backup export, `POST /api/v1/system/config/import`로 restore, 그다음 `GET /api/v1/system/config`를 호출해 설정 페이지를 refresh하고 계속 진행하기 전에 `LITELLM_MODEL` / `AGENT_LITELLM_MODEL` / `VISION_MODEL` / `LLM_TEMPERATURE`를 확인하세요.

### 공급자 preset / Base URL / 모델 명명 공식 참고 자료

- OpenAI-compatible routing in LiteLLM: <https://docs.litellm.ai/docs/providers/openai_compatible>
- OpenAI official API docs: <https://platform.openai.com/docs/api-reference/chat>
- DeepSeek official API docs: <https://api-docs.deepseek.com/>
- Anspire Open: <https://open.anspire.cn/?share_code=QFBC0FYC>
- DashScope OpenAI-compatible mode: <https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope>
- Moonshot / Kimi official compatibility docs: <https://platform.moonshot.ai/docs/guide/compatibility>
- Anthropic official Messages API: <https://docs.anthropic.com/en/api/messages>
- Gemini official OpenAI compatibility docs: <https://ai.google.dev/gemini-api/docs/openai>
- Cohere official: <https://docs.cohere.com/>
- Cohere API reference: <https://docs.cohere.com/reference/>
- Cohere LiteLLM provider page: <https://docs.litellm.ai/docs/providers/cohere>
- Google Gemini API and model list: <https://ai.google.dev/gemini-api/docs/openai>, <https://ai.google.dev/gemini-api/docs/models>
- Google LiteLLM provider page: <https://docs.litellm.ai/docs/providers/gemini>
- xAI official: <https://docs.x.ai/docs>
- xAI LiteLLM provider page: <https://docs.litellm.ai/docs/providers/xai>
- Ollama API docs: <https://github.com/ollama/ollama/blob/main/docs/api.md>

파일을 직접 수정하는 편이 좋다면 `.env` 파일에 설정하는 것도 매끄럽습니다. 여러 플랫폼을 동시에 관리할 수 있습니다. 규칙은 다음과 같습니다.

1. **먼저 채널 선언**: `LLM_CHANNELS=channel_name_1,channel_name_2`
2. **각 채널 설정 제공**(대문자 주의): `LLM_{CHANNEL_NAME}_XXX`

### 예시: DeepSeek와 타사 Relay를 fallback과 함께 설정
```env
# 1. Enable channel mode, declare two channels here: deepseek and aihubmix
LLM_CHANNELS=deepseek,aihubmix

# 2. Channel 1: Configure Official DeepSeek
LLM_DEEPSEEK_BASE_URL=https://api.deepseek.com
LLM_DEEPSEEK_API_KEY=sk-1111111111111
LLM_DEEPSEEK_MODELS=deepseek-v4-flash,deepseek-v4-pro

# 3. Channel 2: Configure a common relay/proxy API
LLM_AIHUBMIX_BASE_URL=https://api.aihubmix.com/v1
LLM_AIHUBMIX_API_KEY=sk-2222222222222
LLM_AIHUBMIX_MODELS=gpt-5.5,claude-sonnet-4-6

# 4. [Key Step] Specify the primary model and fallback list
# Set your primary model:
LITELLM_MODEL=deepseek/deepseek-v4-flash
# Optional: set an Agent-only primary model (empty = inherit the primary model)
AGENT_LITELLM_MODEL=deepseek/deepseek-v4-pro
# If the primary model crashes, try these fallbacks sequentially:
LITELLM_FALLBACK_MODELS=openai/gpt-5.4-mini,anthropic/claude-sonnet-4-6
```

### 예시: Ollama 채널 모드(로컬 모델, API 키 없음)
```env
# 1. Enable channel mode, declare ollama channel
LLM_CHANNELS=ollama

# 2. Configure Ollama address (default local port 11434)
LLM_OLLAMA_BASE_URL=http://localhost:11434
LLM_OLLAMA_MODELS=qwen3:8b,llama3.2

# 3. Specify primary model
LITELLM_MODEL=ollama/qwen3:8b
```

### 채널 모드의 MiniMax 모델 명명

- OpenAI 호환 채널을 통해 MiniMax에 접근하는 경우, 채널 모델 목록에는 `minimax/<model-name>` 형식으로 입력하세요. 예: `minimax/MiniMax-M1`.
- Web 설정 페이지는 이제 Primary, Agent Primary, Fallback, Vision selector에서 이 값을 `openai/minimax/<model-name>`으로 다시 쓰지 않고 그대로 유지합니다.

### Ask-Stock Agent / LiteLLM 호환성 참고

- ask-stock Agent는 일반 analyzer와 같은 3단계 런타임 우선순위를 따릅니다. `LITELLM_CONFIG`(LiteLLM YAML) > `LLM_CHANNELS` > legacy provider keys. 상위 tier가 valid하고 active이면 해당 요청에서 하위 tier는 무시됩니다.
- YAML 모드에서 Agent는 LiteLLM `model_list` / `model_name` routing semantics를 직접 재사용합니다. 채널 모드에서는 먼저 `AGENT_LITELLM_MODEL`을 읽고, 비어 있으면 `LITELLM_MODEL`을 상속한 뒤 `LITELLM_FALLBACK_MODELS`를 이어서 사용합니다.
- YAML 또는 Channels를 사용하지 않고 `AGENT_LITELLM_MODEL`을 비워두며 legacy provider env vars에 의존하는 경우, ask-stock Agent는 계속 이를 상속합니다. `GEMINI_API_KEY + GEMINI_MODEL` -> `gemini/<model>`, `OPENAI_API_KEY + OPENAI_MODEL` -> `openai/<model>`, `ANTHROPIC_API_KEY + ANTHROPIC_MODEL` -> `anthropic/<model>`.
- 이 수정은 두 가지만 개선합니다. backend의 실제 실패 이유를 보존하고 사용 가능한 Agent LLM이 설정되지 않았을 때 더 구체적인 진단을 반환합니다. 기존 `GEMINI_*`, `OPENAI_*`, `ANTHROPIC_*`, `LITELLM_*` 설정을 조용히 삭제, clear, migrate, rewrite하지 **않습니다**.
- 현재 환경에 valid Agent model path가 전혀 없으면 ask-stock 페이지는 여전히 실패를 반환하지만, 이제 backend의 실제 설정 진단을 표시합니다. valid model source를 하나라도 복원하면 migration step 없이 흐름이 회복됩니다.
- 권장 forward path는 여전히 `LITELLM_MODEL` / `AGENT_LITELLM_MODEL`을 명시적으로 설정하거나 `LLM_CHANNELS`로 이동하는 것입니다. legacy provider keys는 오래된 `.env` 파일, 로컬 macOS 개발, 기존 배포를 위한 compatibility fallback으로 남습니다.

single-agent ask-stock 경로에서 backend는 DeepSeek V4 thinking + tool-call roundtrip을 위한 provider-aware trace track도 유지합니다. 같은 실행에 `tool_calls`와 `reasoning_content`가 모두 있을 때만 trace가 저장됩니다. `session_id + provider + model`별 마지막 3개의 최소 protocol slice가 anchored visible assistant reply 앞에 다음 요청으로 splice됩니다. Provider trace는 정확히 보존되거나 통째로 drop됩니다. 요약되지 않고, Web session-history API로 반환되지 않으며, `.env` 설정을 추가하지 않습니다. Model/provider mismatch, summarized anchors, insufficient budget은 trace 전체를 drop합니다. Claude extended thinking은 이 PR에서 adapter/storage-level opaque `thinking` / `redacted_thinking` / `signature` block plumbing과 offline fixture로 제한됩니다. production end-to-end Claude와 multi-agent trace injection은 follow-up입니다. Protocol references: DeepSeek thinking mode (<https://api-docs.deepseek.com/guides/thinking_mode>) and Anthropic Claude extended thinking (<https://platform.claude.com/docs/en/docs/build-with-claude/extended-thinking>). LiteLLM compatibility window는 `requirements.txt`의 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`입니다.

### Strict Temperature Model 호환성 참고

- Moonshot은 Kimi를 OpenAI-compatible API로 공식 문서화하며, base URL은 `https://api.moonshot.ai/v1`입니다: <https://platform.kimi.ai/docs/guide/kimi-k2-6-quickstart>
- LiteLLM은 OpenAI-compatible model routing에 `openai/` 접두사를 공식적으로 요구합니다: <https://docs.litellm.ai/docs/providers/openai_compatible>
- Moonshot의 compatibility docs는 두 고정 값을 구분합니다. **thinking mode는 `1.0`을 사용해야 하고, non-thinking mode는 `0.6`을 사용해야 합니다**. 다른 값은 API에서 거부됩니다: <https://platform.moonshot.ai/docs/guide/compatibility#parameters-differences-in-request-body>
- OpenAI Chat Completions API는 `temperature`를 optional로 취급합니다. provider default temperature만 허용하는 GPT-5 / o-series 스타일 모델의 경우, 이 프로젝트는 저장된 `LLM_TEMPERATURE`를 다시 쓰지 않고 request time에 `temperature`를 생략합니다: <https://platform.openai.com/docs/api-reference/chat/create>
- 이 저장소의 현재 런타임 의존성 제약은 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`입니다(`requirements.txt` 참고). 이 호환성 수정은 main analyzer, market review, direct Agent LiteLLM calls, system-settings channel connectivity test path 전반에서 해당 제약 아래 regression-covered입니다.
- 따라서 이 저장소는 dispatch 직전에 **실제 요청 모드**에 따라 `kimi-k2.6`과 `kimi-k2.6-*`를 normalize합니다. default / thinking 요청은 `temperature=1.0`을 사용합니다. LiteLLM YAML route alias가 `litellm_params.extra_body.thinking.type: disabled`(또는 동등한 non-thinking override)를 명시적으로 설정하면 자동으로 `temperature=0.6`으로 전환합니다. `.env` 또는 Web 설정의 저장된 `LLM_TEMPERATURE` 값은 다시 쓰지 않습니다.
- 아직 profile되지 않은 모델에 대해 compatible platform이 unsupported `temperature`, default-only `1.0`, unsupported `top_p` 같은 명시적 parameter error를 반환하면, runtime은 **현재 요청**을 repair하고 한 번 retry합니다. retry 성공 후 전략은 현재 프로세스에서만 cache됩니다. `.env`에 write back되지 않으며 서비스 재시작 시 설정된 규칙을 정상적으로 다시 평가합니다.
- partial content를 이미 생성한 streaming response의 경우 runtime은 mid-output에 parameter를 전환하지 않습니다. 서로 일관되지 않는 답변을 이어 붙이지 않기 위해 기존 same-model non-stream retry / fallback-model 경로를 유지합니다.
- `SystemConfigService`는 Web 설정 페이지에서 저장하거나 desktop `.env`를 import할 때 실제 제출한 키만 업데이트합니다. strict-temperature model로 전환해도 기존 `LLM_TEMPERATURE`를 조용히 clear, migrate, rewrite하지 않습니다. 임시 request-time parameter strategy는 config 파일에 저장되지 않습니다.
- non-strict primary model, non-strict fallback, 일반 모델로 다시 전환한 뒤의 요청은 모두 설정된 temperature를 계속 사용합니다. 기존 설정은 migration이 필요 없으며 모델을 바꾸면 원래 동작이 자동으로 복원됩니다.
- 저장소 측 호환성 coverage는 `tests/test_llm_channel_config.py`, `tests/test_market_analyzer_generate_text.py`, `tests/test_agent_pipeline.py`, `tests/test_system_config_service.py`에 있습니다.
- 최소 롤백: LLM generation-parameter adaptation change set만 revert하면 됩니다. 별도 `LLM_TEMPERATURE` migration은 필요 없습니다.

> **중요 경고**: `LLM_CHANNELS`를 활성화하면 독립적으로 선언된 표준 `DEEPSEEK_API_KEY` 또는 `OPENAI_API_KEY`는 **완전히 무시됩니다**. 설정 충돌을 방지하려면 **하나의 모드만** 사용하세요.
> **Docker 참고**: `LITELLM_MODEL`, `LLM_CHANNELS`, `LLM_DEEPSEEK_MODELS` 또는 관련 변수가 `docker compose environment:`나 `docker run -e`로 명시 전달되면, 컨테이너 재시작 후 Web 설정 페이지가 작성한 `.env`를 override합니다. 배포 환경도 동시에 업데이트하세요.

### 호환성 증거 및 롤백 감사 참고(이 recovery 변경용)

- 호환성은 두 layer로 검증됩니다. 첫째, first-party provider/API contract references(LiteLLM OpenAI-compatible routing, OpenAI Chat Completions, Moonshot/Kimi docs and model notes), 둘째, `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0` 아래 이 저장소의 현재 runtime implementation입니다.
- 이 recovery path는 runtime-only이며 의도적으로 local입니다. exception classification + one in-request repair retry + in-process cache입니다. `.env`를 다시 쓰거나, 저장된 config keys를 migrate하거나, legacy values를 바꾸지 않습니다. 현재 call에 대해 request parameter(`temperature`, `top_p`, `presence_penalty`, `frequency_penalty`, `seed`)만 omit/adjust합니다. 롤백에는 migration이 필요 없으며 이전 설정과 model/provider selection을 복원하면 됩니다.
- 이 경로의 regression evidence는 `tests/test_llm_param_recovery.py`, `tests/test_system_config_service.py`, `tests/test_llm_channel_config.py`, `tests/test_system_config_api.py`, `tests/test_market_analyzer_generate_text.py`, `tests/test_agent_pipeline.py`에 있습니다. desktop backup import restore는 `test_import_desktop_env_restores_runtime_models_after_cleanup`이 직접 다룹니다.

---

## 방법 3: 고급 YAML 설정(전문가용)

**목표:** enterprise급 고가용성을 위해 최대한의 제어와 origin-level routing rule을 원합니다.

이 layer는 high concurrency, automatic retries, TPM/RPM 기반 load balancing을 포함한 underlying LiteLLM routing capability에 직접 매핑됩니다.

1. `.env`에는 선언 줄 하나만 남겨둡니다.
   ```env
   LITELLM_CONFIG=./litellm_config.yaml
   ```
2. 프로젝트 루트 디렉터리에 `litellm_config.yaml`을 만듭니다(`docs/examples/litellm_config.example.yaml` 참고 가능).

`litellm_config.yaml` 예시:
```yaml
model_list:
  - model_name: my-smart-model
    litellm_params:
      model: deepseek/deepseek-v4-flash
      api_base: https://api.deepseek.com
      api_key: "os.environ/MY_CUSTOM_SECRET_KEY"  # Fetch from environment vars for security

  # Ollama local model (no api_key needed)
  - model_name: ollama/qwen3:8b
    litellm_params:
      model: ollama/qwen3:8b
      api_base: http://localhost:11434
```

> **우선순위 규칙**: YAML이 왕입니다. YAML이 설정되면 **Channels Mode**와 **Simple Mode**는 모두 완전히 무시됩니다. 계층: `YAML > Channels > Simple`.

### LLM usage HMAC telemetry

P0a usage telemetry는 모델에 실제로 전송된 메시지의 HMAC-SHA256 fingerprint를 생성합니다. 이는 로컬 `llm_usage` telemetry만 기록합니다. prompt, provider parameter, cache hint, model output, fallback order는 변경하지 않습니다.

Usage는 세 단계로 읽습니다.

- provider / LiteLLM public `usage` response field를 우선합니다.
- 그다음 LiteLLM public `usage_metadata` response field를 읽습니다.
- 마지막으로 `_hidden_params["usage"]`를 읽습니다. 이는 stable public contract가 아니라 LiteLLM private/internal best-effort fallback입니다. 없더라도 usage/cache telemetry가 불완전할 수 있을 뿐, 모델 요청 자체가 그 이유로 실패한 것은 아닙니다.

Cache-token normalization은 allowlisted best-effort normalization일 뿐입니다. Provider contract, 현재 LiteLLM normalization 동작, 저장소별 compatibility allowlist가 같은 것으로 취급되지 않도록 외부 field evidence와 runtime boundary를 아래에 분리했습니다.

| Provider / source | 읽는 필드 | 증거와 경계 | Coverage |
| --- | --- | --- | --- |
| OpenAI | `usage.prompt_tokens_details.cached_tokens` | 공식 Prompt Caching docs는 1024 token 미만 요청도 `cached_tokens=0`을 노출한다고 설명합니다: <https://developers.openai.com/api/docs/guides/prompt-caching> | unit/mock tests로 커버. 이 PR은 OpenAI live smoke를 포함하지 않음 |
| Anthropic | `cache_creation_input_tokens` / `cache_read_input_tokens` / `input_tokens` | 공식 Prompt Caching docs는 `total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens`로 정의합니다: <https://platform.claude.com/docs/en/build-with-claude/prompt-caching> | unit/mock tests로 커버. 이 PR은 Anthropic live smoke를 포함하지 않음 |
| Gemini / Vertex AI | Official source field: `UsageMetadata.cachedContentTokenCount`; runtime은 `cached_content_token_count`, `cache_read_input_tokens`, `prompt_tokens_details.cached_tokens` 같은 LiteLLM-exposed snake_case / normalized field를 소비 | Gemini `UsageMetadata` official field: <https://ai.google.dev/api/generate-content#UsageMetadata>. 이 저장소는 native camelCase runtime fallback을 추가하지 않습니다. runtime compatibility는 `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`로 제한됩니다. | unit/mock tests로 커버. 이 PR은 Gemini / Vertex live smoke를 포함하지 않음 |
| DeepSeek | `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens` | DeepSeek Chat Completion docs는 `prompt_tokens = prompt_cache_hit_tokens + prompt_cache_miss_tokens`라고 설명합니다: <https://api-docs.deepseek.com/api/create-chat-completion> | unit/mock tests로 커버. 이 PR은 redacted DeepSeek smoke 하나만 포함하며 전체 response를 저장하지 않음 |
| GLM / OpenAI-compatible / StepFun 및 유사 compatible platform | 공통 field로 normalize 가능한 modeled token/cache count allowlist 값 | stable official cache telemetry contract를 주장하지 않습니다. 현재 LiteLLM / OpenAI-compatible shape 아래 best-effort normalization입니다. unmodeled metadata는 저장되지 않습니다. | unit/fixture/mock tests로 커버. 이 PR은 이 공급자들의 live smoke를 포함하지 않음 |
| LiteLLM public response shape | `usage` / `usage_metadata` | 현재 의존성 window `litellm>=1.80.10,!=1.82.7,!=1.82.8,<2.0.0`의 response / `Usage` object shape에 따라 소비됩니다. LiteLLM 2.x compatibility guarantee가 아닙니다. | Analyzer / Agent / usage tests로 커버 |
| LiteLLM private fallback | `_hidden_params["usage"]` | Private/internal best-effort fallback이며 stable LiteLLM public contract가 아닙니다. public zero-only/no-signal usage 같은 좁은 streaming telemetry gap만 보완하고 provider request parameter를 변경하지 않습니다. | unit/mock tests로 커버. 부재는 telemetry completeness에만 영향, 모델 요청 성공에는 영향 없음 |

```env
LLM_USAGE_HMAC_SECRET=
LLM_USAGE_HMAC_KEY_VERSION=local-v1
```

- `LLM_USAGE_HMAC_SECRET`이 비어 있으면 backend는 로컬 deployment-scoped 비교를 위해 data 디렉터리에 `.llm_usage_hmac_secret`를 생성합니다.
- 여러 배포가 의도적으로 comparable HMAC을 필요로 할 때만 같은 high-entropy random secret을 설정하세요. `openssl rand -hex 32`로 생성할 수 있습니다.
- `.llm_usage_hmac_secret`는 로컬 secret artifact이며 `.gitignore`에서 파일명으로 무시됩니다.
- secret을 rotate할 때는 `LLM_USAGE_HMAC_KEY_VERSION`을 업데이트해 예전 fingerprint와 새 fingerprint가 같은 key를 사용한 것처럼 비교되지 않게 하세요.
- login session secret을 재사용하지 말고, 실제 secret을 version control, issues, logs, screenshots에 commit하거나 노출하지 마세요.

### Provider prompt cache configuration(P1 / P1.5)

Prompt-cache 설정은 이 프로젝트가 cache usage / diagnostics를 기록할지, main analysis path가 검증된 provider-specific hint를 능동적으로 보낼지를 제어할 뿐입니다. OpenAI, Gemini, DeepSeek 또는 다른 공급자의 implicit/provider-managed cache 동작을 제어하지 않습니다.

```env
LLM_PROMPT_CACHE_TELEMETRY_ENABLED=true
LLM_PROMPT_CACHE_HINTS_ENABLED=false
LLM_PROMPT_CACHE_DIAGNOSTICS_LEVEL=off
```

- `LLM_PROMPT_CACHE_TELEMETRY_ENABLED=false`이면 provider raw usage JSON, normalized cache fields, cache-decision diagnostics가 저장되지 않습니다. 기본 token usage는 호환됩니다.
- `LLM_PROMPT_CACHE_HINTS_ENABLED=true`는 main analysis / analyzer LiteLLM path가 registry에서 검증 또는 smoke-tested된 provider / route entry에 대해 `prompt_cache_key`, `cache_control`, `user_id` 및 유사 hint를 보내는 것만 허용합니다. ask-stock Agent path는 현재 capability / usage diagnostics만 기록하며 provider-specific hint를 능동적으로 보내지 않습니다. 알 수 없는 OpenAI-compatible gateway는 telemetry-only로 유지됩니다.
- `LLM_PROMPT_CACHE_DIAGNOSTICS_LEVEL=basic`은 provider, API surface, verification status, hint applied, disabled reason 같은 non-sensitive enum decision을 debug logs와 test-observable objects를 통해서만 제공합니다. `debug`는 같은 surface에 HMAC-derived route/cache diagnostics와 matched caps id를 추가하지만, raw prompts, request bodies, message content, raw stock/user values, webhooks, API keys를 포함해서는 안 됩니다. 이 diagnostics는 public Usage API나 일반 settings-page output이 아닙니다.
- Provider Cache Capability Registry는 `src/llm/provider_cache.py`의 code-level manual registry입니다. entry에는 `doc_sources`, `last_verified_at`, `verification_status`가 포함됩니다. provider를 추가하거나 LiteLLM을 업그레이드할 때 tests와 함께 업데이트하세요.
- Prompt cache key, route key, DeepSeek session isolation은 domain-separated HMAC과 함께 `LLM_USAGE_HMAC_SECRET` / `.llm_usage_hmac_secret`를 재사용합니다. prompt-cache-specific secret은 새로 도입하지 않습니다.

### Legacy message stability audit(P0.5a)

P0.5a는 일반 종목 분석 legacy `[system, user]` message path를 위한 내부 stability-audit field를 추가합니다. 이 field들은 로컬 `llm_usage` record에만 기록됩니다. 위 message HMAC pipeline을 재사용하며 prompt text, message order, provider request parameter, cache hint, model output, fallback order, public Usage API, Web page를 변경하지 않습니다.

추가 field는 maintainer diagnostics 전용입니다.

- `language`, `market_group`, `analysis_mode`, `legacy_prompt_mode`, `provider`, `transport`, `message_count`는 종목 분석 호출의 low-sensitivity routing context를 설명합니다.
- `skill_config_hmac`는 resolved skill prompt fragments, default skill policy, legacy prompt mode에 대한 HMAC-SHA256입니다. raw skill text를 저장하지 않고도 skill configuration에 따라 system message가 바뀌는지 maintainer가 알 수 있게 합니다.
- `known_dynamic_marker_positions`는 JSON string입니다. 각 entry는 `marker_name`, `message_role`, `char_offset`만 저장합니다. 종목 코드, 종목명, 날짜, 뉴스 본문, quote 값, headers, response text, prompt snippet은 저장하지 않습니다.
- `estimated_total_prompt_tokens`, `approx_common_prefix_chars`, `approx_common_prefix_tokens`는 저장소의 stable canonical render를 사용합니다. message는 고정 separator와 함께 `role + "\n" + content` 순서로 concat됩니다. provider wire bytes와 일치한다고 주장하지 않습니다.
- `char_offset`은 matching message `content` 내부에서 측정됩니다. `approx_common_prefix_chars`는 canonical-render 시작부터 첫 known dynamic marker까지의 character count입니다. marker를 찾지 못하면 common-prefix field는 `NULL`로 유지됩니다.
- Token estimate는 `ceil(chars / 3)`을 사용합니다. diagnostics일 뿐 provider usage를 대체하지 않으며 cache-threshold decision에 사용되지 않습니다. 중국어 텍스트는 과소평가될 수 있습니다.

P0.5a는 PromptBlock IR, `block_id`, `stability_class`, `static_prefix_hash`, `dynamic_context_hash`를 도입하지 않습니다. Agent, research, market-review path는 아직 이 audit에 연결되어 있지 않습니다.

### GitHub Actions 참고

번들 `00-daily-analysis.yml`은 일반 LLM runtime field를 job environment에 명시적으로 전달합니다.

- Runtime selection: `GENERATION_BACKEND`, `GENERATION_FALLBACK_BACKEND`, `GENERATION_BACKEND_TIMEOUT_SECONDS`, `GENERATION_BACKEND_MAX_OUTPUT_BYTES`, `GENERATION_BACKEND_MAX_CONCURRENCY`, `LOCAL_CLI_BACKEND_MAX_CONCURRENCY`, `AGENT_GENERATION_BACKEND`, `LLM_CHANNELS`, `LITELLM_MODEL`, `LITELLM_FALLBACK_MODELS`, `AGENT_LITELLM_MODEL`, `VISION_MODEL`, `VISION_PROVIDER_PRIORITY`, `LLM_TEMPERATURE`, `LLM_USAGE_HMAC_SECRET`, `LLM_USAGE_HMAC_KEY_VERSION`, `LLM_PROMPT_CACHE_TELEMETRY_ENABLED`, `LLM_PROMPT_CACHE_HINTS_ENABLED`, `LLM_PROMPT_CACHE_DIAGNOSTICS_LEVEL`
- Multiple keys: `GEMINI_API_KEYS`, `ANTHROPIC_API_KEYS`, `OPENAI_API_KEYS`, `DEEPSEEK_API_KEYS`(현재 workflow는 이를 repository Secrets에서만 import하며 같은 이름의 Variables에서는 import하지 않음)
- Common channel names: `primary`, `secondary`, `aihubmix`, `deepseek`, `dashscope`, `zhipu`, `moonshot`, `minimax`, `volcengine`, `siliconflow`, `openrouter`, `gemini`, `anthropic`, `openai`, `ollama`

예를 들어 GitHub Actions에서 `LLM_CHANNELS=primary,deepseek`를 설정하면 해당하는 `LLM_PRIMARY_*`와 `LLM_DEEPSEEK_*` 항목도 설정하세요. `LLM_<NAME>_API_KEY` / `LLM_<NAME>_API_KEYS` field 역시 현재는 repository Secrets에서만 import되므로 Variables에 저장하면 runtime에서 작동하지 않습니다. `my_proxy` 같은 custom channel name을 사용한다면 GitHub Actions workflow `env:` block에 matching `LLM_MY_PROXY_*` mapping을 명시적으로 추가해야 합니다. 로컬 `.env`와 Docker 실행에는 이 제한이 없습니다.

---

## 고급 기능: Vision 모델 설정

시스템의 특정 기능(예: 주식 차트 스크린샷을 업로드해 종목 코드 추출)은 computer vision이 가능한 모델을 필요로 합니다. `.env`에 전용 vision model을 지정해야 합니다.

```env
# Specify your dedicated vision model name
VISION_MODEL=openai/gpt-5.5
# Make sure to provide its corresponding provider API KEY (e.g., OPENAI_API_KEY):
# OPENAI_API_KEY=xxx
```

**Vision Fallback Mechanism:** 예기치 않은 실패를 방지하기 위해 시스템에는 fallback strategy가 내장되어 있습니다. primary vision model이 실패하면 다음 순서로 대체 vision-capable provider key 사용을 시도합니다.
```env
# Default fallback sequence:
VISION_PROVIDER_PRIORITY=gemini,anthropic,openai
```

---

## 문제 해결

설정이 잘못되었는지 걱정된다면 터미널에서 다음 명령으로 진단하세요.

- `python scripts/check_env.py --config`: `.env`의 로직이 구조적으로 올바른지만 확인합니다. 즉시 결과를 제공하고 네트워크 호출은 없으며 syntax omission을 엄격히 검사합니다.
- `python scripts/check_env.py --llm`: LLM에 실제 인사 메시지를 보내 endpoint를 테스트합니다. **네트워크가 작동하는지**와 **계정 잔액이 충분한지**를 철저히 확인합니다.

### 흔한 함정

| 발생한 이상한 오류 | 가능성 높은 원인 | 해결 방법 |
|----------------------|----------------|----------------|
| **UI가 primary model이 설정되지 않았다고 말함** | 시스템이 어떤 provider/model을 쓰고 싶은지 모릅니다. | `.env`에 명확한 지시를 추가하세요: `LITELLM_MODEL=provider/your_model_name`. 예: `openai/gpt-5.5`. |
| **여러 provider Key를 추가했는데 왜 하나만 작동하나요?** | **Simple Mode**와 **Channels Mode**를 섞었습니다. | 하나의 경로를 선택하세요. 단순 설정이라면 `LLM_CHANNELS`로 시작하는 것을 삭제하세요. 다중 모델 fallback을 쓰려면 모든 Key를 `LLM_CHANNELS` 설정으로 옮기세요. |
| **400, 401, Invalid API Key 반환** | API Key가 틀렸거나, 불완전하게 복사되었거나, 계정 크레딧이 부족하거나, 모델명을 잘못 입력했습니다(매우 흔함). | 1. Key 앞뒤에 공백이 없는지 확인하세요.<br> 2. Base URL이 `/v1`로 끝나는지 확인하세요.<br> 3. 모델명에 `openai/` 접두사를 빠뜨리지 않았는지 확인하세요. |
| **Kimi K2.6이 `invalid temperature`를 반환함(`1.0` 또는 `0.6`만 허용한다고 할 수 있음)** | 모델이 thinking vs non-thinking mode에 서로 다른 고정 temperature를 요구하지만, 오래된 config 또는 call path가 여전히 `0.7`을 전달할 수 있습니다. | 이 수정 후 default / thinking `kimi-k2.6` 요청은 자동으로 `temperature=1.0`을 사용합니다. LiteLLM YAML route에서 thinking을 명시적으로 비활성화하면 요청은 자동으로 `0.6`을 사용합니다. Moonshot 또는 relay OpenAI-compatible Base URL 및 API key와 함께 `openai/kimi-k2.6`을 선호하세요. Non-Kimi fallback은 설정된 `LLM_TEMPERATURE`를 계속 유지합니다. |
| **GPT-5 / o-series가 `temperature`를 지원하지 않거나 default만 허용한다고 반환함** | 이 모델들은 provider default sampling parameter만 허용하지만, 오래된 call path가 여전히 `0.7`을 보낼 수 있습니다. | request layer가 이제 `temperature`를 생략해 provider default를 사용합니다. `.env` / Web `LLM_TEMPERATURE`는 다시 쓰이지 않으며, 일반 모델로 되돌리면 계속 사용됩니다. |
| **계속 돌다가 결국 Timeout/ConnectionRefused 발생** | 차단된 지역에서 proxy 없이 Google/OpenAI 같은 제한 API를 사용하거나, 클라우드 서버에 외부 인터넷 접근이 없습니다. | **공식 지역 API**(예: DeepSeek) 또는 **OpenAI-compatible relay platform** 사용을 강력 권장합니다. 타사 플랫폼은 이런 네트워크 제약을 우회합니다. |
| **Ollama가 404, `Could not get model info`, `api/generate/api/show` 반환** | Ollama에 `OPENAI_BASE_URL`을 사용해 시스템이 URL을 잘못 이어 붙입니다. | 대신 `OLLAMA_API_BASE=http://localhost:11434` 또는 채널 모드(`LLM_CHANNELS=ollama` + `LLM_OLLAMA_BASE_URL`)를 사용하세요. |

*숙련자 팁: **Agent Mode(Deep-thinking & web-search)**를 활성화한다면 경험상 `deepseek-v4-pro` 같은 더 강한 모델을 사용하는 것이 좋습니다. 비용을 아끼려고 약한 mini-model을 agent에 쓰면 무한 루프나 목표 누락이 생길 가능성이 큽니다.*
