# 한국어 문서 색인

이 문서는 프로젝트 문서의 시작점입니다. README는 프로젝트 개요와 빠른 시작을 다루고, 상세 설정, 구성, 배포, 기능 사용법, 문제 해결 문서는 아래 링크에서 확인할 수 있습니다.

> 중국어 문서는 [docs/INDEX.md](INDEX.md)를 참고하세요. 영어 문서는 [docs/INDEX_EN.md](INDEX_EN.md)를 참고하세요.

## 목적별로 선택하기

| 하고 싶은 일 | 먼저 읽기 | 이어서 읽기 |
| --- | --- | --- |
| 프로젝트가 무엇을 하는지 이해하기 | [README (KO)](README_KO.md) | [전체 가이드 (KO)](full-guide_KO.md) |
| 프로젝트를 처음 실행하기 | [README (KO)](README_KO.md) | [전체 가이드 (KO)](full-guide_KO.md) |
| 모델 공급자 설정하기 | [LLM 설정 가이드 (KO)](LLM_CONFIG_GUIDE_KO.md) | [공급자 설정 가이드](llm-providers.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) |
| 알림 설정하기 | [알림 기본 문서](notifications.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | [전체 가이드 (KO)](full-guide_KO.md) |
| 서버 또는 클라우드 플랫폼에 배포하기 | [배포 가이드 (KO)](DEPLOY_KO.md) | [클라우드 WebUI 배포](deploy-webui-cloud.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용), [Zeabur 배포](docker/zeabur-deployment.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) |
| Bot / IM 연동 사용하기 | [Bot 명령어 (KO)](bot-command_KO.md) | [Bot 플랫폼 문서](bot/) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) |
| 런타임 문제 해결하기 | [FAQ (KO)](FAQ_KO.md) | [변경 로그](CHANGELOG.md) |
| 코드 또는 문서에 기여하기 | [기여 가이드 (KO)](CONTRIBUTING_KO.md) | [API 명세](architecture/api_spec.json) |

## 시작하기

| 문서 | 내용 |
| --- | --- |
| [README (KO)](README_KO.md) | 프로젝트 개요, 주요 기능, 빠른 시작, 샘플 출력 |
| [전체 가이드 (KO)](full-guide_KO.md) | 환경 설정, 실행 모드, 구성, 배포 경로, 일반적인 문제 |
| [FAQ (KO)](FAQ_KO.md) | 설정, 모델, 알림, 배포, 런타임 관련 자주 묻는 질문 |
| [변경 로그](CHANGELOG.md) | 릴리스 노트, 기능 변경, 마이그레이션 참고 사항 |

## 설정

| 문서 | 내용 |
| --- | --- |
| [LLM 설정 가이드 (KO)](LLM_CONFIG_GUIDE_KO.md) | 모델 공급자, 3단계 구성, Web 설정, 일반적인 모델 설정 |
| [공급자 설정 가이드](llm-providers.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | 공급자 preset, GitHub Actions 매핑, 오류 분류, 진단 |
| [LiteLLM YAML 예시](examples/litellm_config.example.yaml) | LiteLLM 다중 공급자 구성 예시 |
| [알림 기본 문서](notifications.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | WeChat Work, Feishu, Telegram, Discord, Slack, Email 등 알림 채널 |
| [Tushare 종목 목록 가이드](TUSHARE_STOCK_LIST_GUIDE.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | Tushare 종목 목록 설정 및 사용 참고 사항 |

## 사용 주제

| 문서 | 내용 |
| --- | --- |
| [Bot 명령어 (KO)](bot-command_KO.md) | Bot 명령어, 웹훅, 플랫폼 연동, 콜백 동작 |
| [Bot 플랫폼 문서](bot/) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | Feishu, DingTalk, Discord 등 Bot 설정 스크린샷과 참고 사항 |
| [실시간 알림 센터](alerts.md) <sub><sub>![P4 Badge](https://img.shields.io/badge/P4-yellow?style=flat)</sub></sub> (중국어 전용) | EventMonitor 기준선, Web 규칙 관리, 알림 시도, 쿨다운 상태, 단계별 경계 |
| [DecisionSignal 주제](decision-signals.md) <sub><sub>![P7 Badge](https://img.shields.io/badge/P7-orange?style=flat)</sub></sub> (중국어 전용) | AI 신호 필드, API, Web 표시, 알림/통지/포트폴리오 리스크 연계, 결과 평가, redaction, 마이그레이션, 롤백 |
| [Analysis Context Pack 계약, 런타임 소비, 가시성](analysis-context-pack.md) <sub><sub>![P6 Badge](https://img.shields.io/badge/P6-orange?style=flat)</sub></sub> (중국어 전용) | AnalysisContextPack 1차 범위 경계, 필드 품질 상태, P1/P2 내부 계약, P3 prompt-summary 소비, P4 history/API/Web 저민감도 가시성, P5 데이터 품질 점수, P6 마이그레이션/롤백 참고 및 소스 앵커. 전체 가이드에는 #1386 시장 국면 분석, 마이그레이션, 롤백 진입점이 추가되어 있습니다. |
| [이미지 추출 프롬프트](image-extract-prompt.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | 이미지에서 주식 정보를 추출하기 위한 프롬프트와 경계 |
| [OpenClaw Skill 통합](openclaw-skill-integration.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | OpenClaw / Skill 외부 통합 참고 사항 |

## 배포 및 패키징

| 문서 | 내용 |
| --- | --- |
| [배포 가이드 (KO)](DEPLOY_KO.md) | 서버 배포, Docker, systemd, Supervisor 및 관련 옵션 |
| [클라우드 WebUI 배포](deploy-webui-cloud.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | 클라우드 서버 WebUI 접속 및 배포 참고 사항 |
| [Zeabur 배포](docker/zeabur-deployment.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | Zeabur 플랫폼 배포 |
| [데스크톱 패키징](desktop-package.md) <sub><sub>![P2 Badge](https://img.shields.io/badge/P2-yellow?style=flat)</sub></sub> (중국어 전용) | Electron 데스크톱 앱 및 Web 산출물 패키징 |

## 레퍼런스 및 개발

| 문서 | 내용 |
| --- | --- |
| [API 명세](architecture/api_spec.json) | FastAPI OpenAPI 산출물 |
| [기여 가이드 (KO)](CONTRIBUTING_KO.md) | Issue, Pull Request, 테스트, 문서 동기화, 협업 기대 사항 |

## 언어

| 문서 | 내용 |
| --- | --- |
| [중국어 문서 색인](INDEX.md) | 중국어 문서 진입점 |
| [영어 문서 색인](INDEX_EN.md) | 영어 문서 진입점 |
| [번체 중국어 README](README_CHT.md) | 번체 중국어 프로젝트 개요와 빠른 시작 |

## 중국 시장 용어집

| 용어 | 의미 |
| --- | --- |
| **A주** | 상하이 또는 선전 증권거래소에 상장되고 CNY로 표시되는 주식 |
| **북향 자금 흐름** | Stock Connect 프로그램을 통한 외국인 투자자의 순매수/순매도 흐름 |
| **용호방** | 거래가 활발한 종목과 주요 거래 좌석에 대한 SSE/SZSE의 일일 공시 |
| **칩 분포** | 유통주식의 원가 분포로, 지지선과 저항선을 추정하는 데 자주 사용됩니다. |
| **Tushare** | 토큰이 필요한 중국 금융 데이터 API |
| **AkShare** | 오픈소스 Python 시장 데이터 라이브러리 |
| **Baostock** | A주 과거 데이터를 위한 무료 Python SDK |
| **WeChat Work** | 웹훅 알림을 지원하는 Tencent 기업용 메신저 플랫폼 |
| **Feishu** | 웹훅 알림을 지원하는 ByteDance 기업 협업 플랫폼 |
| **PushPlus / ServerChan** | 중국 모바일 push 알림 서비스 |
