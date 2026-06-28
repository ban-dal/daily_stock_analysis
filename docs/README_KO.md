<div align="center">

# AI 주식 분석 시스템

[![GitHub stars](https://img.shields.io/github/stars/ZhuLinsen/daily_stock_analysis?style=social)](https://github.com/ZhuLinsen/daily_stock_analysis/stargazers)
[![CI](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/ZhuLinsen/daily_stock_analysis/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Ready-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://hub.docker.com/r/zhulinsen/daily_stock_analysis)

<p align="center">
  <img src="https://trendshift.io/api/badge/trendshift/repositories/18527/daily?language=Python" alt="#1 Python Repository Of The Day | Trendshift" width="250" height="55"/>&nbsp;<a href="https://hellogithub.com/repository/ZhuLinsen/daily_stock_analysis" target="_blank"><img src="https://api.hellogithub.com/v1/widgets/recommend.svg?rid=6daa16e405ce46ed97b4a57706aeb29f&claim_uid=pfiJMqhR9uvDGlT&theme=neutral" alt="Featured｜HelloGitHub" width="230" /></a>
</p>

**A주 / 홍콩 / 미국 / 일본 / 한국 주식을 위한 AI 기반 주식 분석 시스템**

관심 종목을 매일 분석 -> 의사결정 대시보드 생성 -> Telegram / Discord / Slack / Email / WeChat Work / Feishu로 알림 전송.

[**제품 미리보기**](#-제품-미리보기) · [**주요 기능**](#-주요-기능) · [**빠른 시작**](#-빠른-시작) · [**샘플 출력**](#-샘플-출력) · [**문서 색인**](./INDEX_KO.md) · [**전체 가이드**](./full-guide_KO.md)

[English](README_EN.md) | [简体中文](../README.md) | [繁體中文](README_CHT.md) | 한국어

</div>

## 💖 후원사

<div align="center">
  <p align="center">
    <a href="https://open.anspire.cn/?share_code=QFBC0FYC" target="_blank"><img src="assets/anspire.png" alt="Anspire Open all-in-one model and search service" width="300" height="141" style="width: 300px; height: 141px; object-fit: contain;"></a>
    <a href="https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis" target="_blank"><img src="assets/serpapi_banner_en.png" alt="Easily scrape real-time financial news data from search engines - SerpApi" width="300" height="141" style="width: 300px; height: 141px; object-fit: contain;"></a>
  </p>
</div>

## 🖥️ 제품 미리보기

<p align="center">
  <img src="assets/readme_workspace_tour_20260510.gif" alt="DSA Web workspace demo" width="720">
</p>

## ✨ 주요 기능

| 기능 | 지원 범위 |
|------------|----------|
| AI 의사결정 리포트 | 핵심 결론, 점수, 추세, 진입/청산 구간, 리스크 알림, 촉매 요인, 실행 체크리스트 |
| 다중 시장 데이터 | A주, 홍콩, 미국, ETF: 시세, K라인, 기술 지표, 자금 흐름, 칩 분포, 뉴스, 공시, 펀더멘털. 일본/한국(Yahoo `.T` / `.KS` / `.KQ`): 현재 MVP는 YFinance 기본/시세 + 일봉 데이터와 기술 지표만 지원하며, 자금 흐름, dragon_tiger, 섹터, 관련 고급 블록은 `not_supported`를 반환할 수 있습니다. 자세한 내용은 [시장 지원 범위](market-support.md)를 참고하세요. |
| Web / 데스크톱 작업공간 | 수동 분석, 작업 진행률, 히스토리, 전체 Markdown 리포트, 백테스트, 포트폴리오, 설정, 라이트/다크 테마 |
| Agent 전략 채팅 | Web/Bot/API에서 15개 내장 전략을 활용한 멀티턴 Q&A |
| 스마트 가져오기 및 자동완성 | 이미지, CSV/Excel, 클립보드 가져오기. 코드/이름/병음/별칭 자동완성 |
| 자동화 및 알림 | GitHub Actions, Docker, 로컬 스케줄러, FastAPI 서비스, WeChat Work / Feishu / Telegram / Discord / Slack / Email 전송 |

> 상세 필드, 펀더멘털 P0 타임아웃 의미, 거래 규칙, 데이터 소스 우선순위, Web/API 동작, 문제 해결은 [전체 가이드](./full-guide_KO.md)에 정리되어 있습니다.

### 기술 스택 및 데이터 소스

| 유형 | 지원 항목 |
|------|-----------|
| AI 모델 | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC), [AIHubMix](https://aihubmix.com/?aff=CfMq), Gemini, OpenAI 호환 공급자, DeepSeek, Qwen, Claude, Ollama |
| 시장 데이터 | [TickFlow](https://tickflow.org/auth/register?ref=WDSGSPS5XC), AkShare, Tushare, Pytdx, Baostock, YFinance, Longbridge |
| 뉴스 검색 | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC), [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis), [Tavily](https://tavily.com/), [Bocha](https://open.bocha.cn/), [Brave](https://brave.com/search/api/), [MiniMax](https://platform.minimaxi.com/), SearXNG |
| 소셜 감성 | Reddit / X / Polymarket용 [Stock Sentiment API](https://api.adanos.org/docs), 미국 주식만 지원 |

> 전체 동작은 [데이터 소스 설정](./full-guide_KO.md#데이터-소스-설정)에 문서화되어 있습니다.

## 🚀 빠른 시작

### 옵션 1: GitHub Actions(권장)

> 서버나 인프라 비용 없이 약 5분 만에 배포할 수 있습니다.

#### 1. 이 저장소 Fork

오른쪽 위의 `Fork`를 클릭하세요. 이 프로젝트가 도움이 되었다면 Star도 큰 힘이 됩니다.

#### 2. Secrets 설정

Fork한 저장소를 열고 `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`으로 이동합니다.

**AI 모델 설정(최소 하나 설정)**

하나의 공급자와 하나의 API 키로 시작하세요. 멀티 모델 라우팅, 이미지 인식, 로컬 모델, 고급 라우팅은 [LLM 설정 가이드](./LLM_CONFIG_GUIDE_KO.md)를 참고하세요.

| Secret 이름 | 설명 | 필수 여부 |
|-------------|-------------|:--------:|
| `ANSPIRE_API_KEYS` | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC) API 키. 주요 LLM과 웹 검색을 하나의 키로 사용할 수 있으며 이 프로젝트용 무료 할당량이 있습니다. | **권장** |
| `AIHUBMIX_KEY` | [AIHubMix](https://aihubmix.com/?aff=CfMq) API 키. 여러 모델 계열을 하나의 키로 사용할 수 있으며 이 프로젝트용 10% 충전 할인 혜택이 있습니다. | **권장** |
| `GEMINI_API_KEY` | Google Gemini API 키 | 선택 |
| `ANTHROPIC_API_KEY` | Anthropic Claude API 키 | 선택 |
| `OPENAI_API_KEY` | DeepSeek, Qwen 호환 서비스를 포함한 OpenAI 호환 API 키 | 선택 |
| `OPENAI_BASE_URL` / `OPENAI_MODEL` | OpenAI 호환 공급자를 사용할 때 입력 | 선택 |

> Ollama는 로컬 또는 Docker 배포에 더 적합합니다. GitHub Actions에서는 일반적으로 클라우드 API가 더 매끄럽습니다.

**알림 채널(최소 하나 설정)**

| Secret 이름 | 설명 |
|-------------|-------------|
| `WECHAT_WEBHOOK_URL` | WeChat Work 봇 |
| `FEISHU_WEBHOOK_URL` | Feishu 봇 |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | Telegram |
| `DISCORD_WEBHOOK_URL` | Discord 웹훅 |
| `SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID` | Slack 봇 |
| `EMAIL_SENDER` + `EMAIL_PASSWORD` | 이메일 알림 |

추가 채널, 서명, 이메일 그룹, Markdown 이미지 변환 설정은 [알림 설정](./full-guide_KO.md#알림-채널-설정)에 있습니다.

**관심 종목(필수)**

| Secret 이름 | 설명 | 필수 여부 |
|-------------|-------------|:--------:|
| `STOCK_LIST` | 관심 종목 코드. 예: `600519,hk00700,AAPL,7203.T,005930.KS` | ✅ |

**뉴스 소스(권장)**

뉴스 검색은 감성, 공시, 이벤트, 촉매 요인의 품질을 크게 높입니다. 가능하다면 검색 공급자를 최소 하나 설정하세요.

| Secret 이름 | 설명 | 필수 여부 |
|-------------|-------------|:--------:|
| `ANSPIRE_API_KEYS` | [Anspire AI Search](https://aisearch.anspire.cn/). 중국어 콘텐츠와 A주 분석에 최적화되어 있으며, 같은 키를 Anspire LLM fallback 예시에도 사용할 수 있습니다. | **권장** |
| `SERPAPI_API_KEYS` | [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis). 실시간 금융 뉴스용 검색엔진 결과 | **권장** |
| `TAVILY_API_KEYS` | [Tavily](https://tavily.com/). 범용 뉴스 검색 API | 선택 |
| `NAVER_CLIENT_ID` / `NAVER_CLIENT_SECRET` | [Naver Search](https://developers.naver.com/docs/serviceapi/search/news/news.md). 한국 `.KS`/`.KQ` 종목 뉴스 우선 검색 | 선택 |
| `BOCHA_API_KEYS` | [Bocha](https://open.bocha.cn/). AI 요약을 제공하는 중국어 검색 | 선택 |
| `BRAVE_API_KEYS` | [Brave Search](https://brave.com/search/api/). 프라이버시 우선 검색 및 미국 주식 뉴스 보강 | 선택 |
| `MINIMAX_API_KEYS` | [MiniMax](https://platform.minimaxi.com/). 구조화된 검색 결과 | 선택 |
| `SEARXNG_BASE_URLS` | 할당량 없는 fallback을 위한 자체 호스팅 SearXNG 인스턴스 | 선택 |

추가 검색 공급자, 소셜 감성, fallback 동작은 [검색 설정](./full-guide_KO.md#검색-서비스-설정)에 있습니다.

#### 3. Actions 활성화

`Actions` 탭을 열고 `I understand my workflows, go ahead and enable them`을 클릭합니다.

#### 4. 수동 테스트

`Actions` -> `Daily Stock Analysis` -> `Run workflow` -> `Run workflow`.

#### 완료

기본적으로 워크플로는 매주 평일 베이징 시간 18:00에 실행되며 비거래일은 건너뜁니다. 강제 실행, 거래일 확인, 재개 규칙은 [전체 가이드](./full-guide_KO.md#스케줄-작업-설정)에 설명되어 있습니다.

### 옵션 2: 로컬 / Docker 배포

```bash
# 프로젝트 클론
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git && cd daily_stock_analysis

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env && vim .env

# 분석 실행
python main.py
```

자주 쓰는 명령:

```bash
python main.py --debug
python main.py --dry-run
python main.py --stocks 600519,hk00700,AAPL
python main.py --market-review
python main.py --schedule
python main.py --serve-only
```

> Docker 배포, 스케줄링, 클라우드 서버 WebUI 접속은 [전체 가이드](./full-guide_KO.md)에 문서화되어 있습니다.

## 📱 샘플 출력

### 의사결정 대시보드

```markdown
🎯 2026-02-08 의사결정 대시보드
분석 종목 3개 | 🟢 매수:0 🟡 관망:2 🔴 매도:1

📊 요약
🟡 000657: 관망 | 점수 65 | 상승 우위
🟡 600105: 관망 | 점수 48 | 박스권
🔴 300260: 매도 | 점수 35 | 하락 우위

🚨 리스크 알림:
리스크 1: 주력 자금의 뚜렷한 유출이 확인되었습니다.
리스크 2: 칩 집중도상 단기 저항이 예상됩니다.

✨ 긍정 촉매:
촉매 1: AI 서버 공급망 노출도가 여전히 시장의 관심사입니다.
촉매 2: 최근 실적 성장이 펀더멘털을 뒷받침합니다.
```

### 시장 리뷰

```markdown
🎯 2026-01-10 시장 리뷰

📊 주요 지수
- SSE Composite: 3250.12 (+0.85%)
- SZSE Component: 10521.36 (+1.02%)
- ChiNext: 2156.78 (+1.35%)

📈 시장 폭
상승: 3920 | 하락: 1349 | 상한가: 155 | 하한가: 3
```

## ⚙️ 설정

전체 환경 변수, 모델 라우팅, 알림 채널, 데이터 소스 우선순위, 거래 규칙, 펀더멘털 P0 의미, 배포 세부 사항은 [전체 가이드](./full-guide_KO.md)에 있습니다.

## 🖥️ Web UI

Web 작업공간은 설정, 작업 모니터링, 수동 분석, 히스토리 리포트, 전체 Markdown 리포트, Agent 전략 채팅, 백테스트, 포트폴리오 관리, 스마트 가져오기, 라이트/다크 테마를 지원합니다.

```bash
python main.py --webui
python main.py --webui-only
```

`http://127.0.0.1:8000`에 접속하세요. 인증, 스마트 가져오기, 자동완성, 리포트 복사, 클라우드 서버 접속은 [로컬 WebUI 관리](./full-guide_KO.md#로컬-webui-관리-인터페이스)에 문서화되어 있습니다.

## 🤖 Agent 전략 채팅

사용 가능한 AI API 키를 하나라도 설정하면 Web `/chat` 페이지에서 전략 채팅을 사용할 수 있습니다. 명시적으로 끄고 싶을 때만 `AGENT_MODE=false`를 설정하세요.

- 내장 전략에는 이동평균선 교차, Chan 이론, 엘리엇 파동, 강세 추세, 핫 테마, 이벤트 드리븐, 성장 품질, 기대 재평가 등이 포함됩니다.
- 실시간 시세, K라인 데이터, 기술 지표, 뉴스, 리스크 컨텍스트를 호출합니다.
- 후속 질문, 세션 내보내기, 알림 전송, 백그라운드 실행을 지원합니다.
- 커스텀 전략 파일과 실험적 멀티 에이전트 오케스트레이션을 지원합니다.

> Agent 파라미터, `skill` 명명 호환성, 멀티 에이전트 모드, 예산 보호 장치는 [전체 가이드](./full-guide_KO.md#로컬-webui-관리-인터페이스)와 [LLM 설정 가이드](./LLM_CONFIG_GUIDE_KO.md)에 정리되어 있습니다.

## 🧩 관련 프로젝트

> DSA는 일일 분석 리포트에 집중합니다. 아래 형제 프로젝트들은 워크플로를 확장하려는 사용자를 위해 종목 스크리닝, 전략 검증, 전략 진화를 다룹니다. 현재는 독립적으로 유지되고 있으며, 후보 종목 가져오기, 백테스트 검증, 리포트 인계가 향후 통합 방향으로 계획되어 있습니다.

| 프로젝트 | 초점 |
|---------|-------|
| [AlphaSift](https://github.com/ZhuLinsen/alphasift) | 후보 관심 종목 구성을 위한 멀티팩터 종목 스크리닝 및 전체 시장 스캔 |
| [AlphaEvo](https://github.com/ZhuLinsen/alphaevo) | 규칙 검증과 전략 파라미터/조합의 반복 탐색을 위한 전략 백테스팅 및 자기 진화 실험 |

## 📞 연락처

<table>
  <tr>
    <td width="92" valign="top"><strong>Email</strong></td>
    <td valign="top">
      <a href="mailto:zhuls345@gmail.com">zhuls345@gmail.com</a><br>
      프로젝트 컨설팅, 배포 지원, 기능 확장
    </td>
    <td align="center" rowspan="3" valign="middle" width="148">
      <a href="http://xhslink.com/m/tU520DWCKT" target="_blank"><img src="assets/xiaohongshu_tick.jpg" width="112" alt="Xiaohongshu QR code"></a><br>
      <sub>Xiaohongshu 팔로우</sub>
    </td>
  </tr>
  <tr>
    <td width="92" valign="top"><strong>Xiaohongshu</strong></td>
    <td valign="top"><a href="http://xhslink.com/m/tU520DWCKT">Xiaohongshu 팔로우</a></td>
  </tr>
  <tr>
    <td width="92" valign="top"><strong>피드백</strong></td>
    <td valign="top"><a href="https://github.com/ZhuLinsen/daily_stock_analysis/issues">GitHub Issues</a> · <a href="https://github.com/ZhuLinsen/daily_stock_analysis/discussions">Discussions</a></td>
  </tr>
</table>

## 📄 라이선스

[MIT License](../LICENSE) © 2026 ZhuLinsen

이 프로젝트를 사용하거나 기반으로 개발한다면 이 저장소로 돌아오는 링크와 함께 출처를 밝혀주시면 감사하겠습니다.

## ⚠️ 면책 조항

이 프로젝트는 정보 제공 및 교육 목적만을 위한 것입니다. AI가 생성한 분석은 투자 조언이 아닙니다. 주식시장 투자는 위험을 수반하므로 직접 조사하고 필요하면 공인 금융 전문가와 상담하세요.
