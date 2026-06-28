# 기여 가이드

기여에 관심을 가져주셔서 감사합니다. 모든 종류의 기여를 환영합니다.

## 🐛 버그 제보

1. 먼저 [Issues](https://github.com/ZhuLinsen/daily_stock_analysis/issues)를 검색해 이미 보고된 문제인지 확인하세요.
2. **Bug Report** 템플릿을 사용해 새 Issue를 생성하세요.
3. 자세한 재현 단계와 환경 정보를 제공하세요.

## 💡 기능 제안

1. Issues를 검색해 같은 제안이 이미 올라왔는지 확인하세요.
2. **Feature Request** 템플릿을 사용해 새 Issue를 생성하세요.
3. 사용 사례와 기대 동작을 자세히 설명하세요.

## 🔧 코드 제출

### 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 가상 환경 생성
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env
# .env를 편집해 필요한 API 키를 입력하세요
```

### 기여 워크플로

1. 이 저장소를 Fork합니다.
2. 기능 브랜치를 만듭니다: `git checkout -b feature/your-feature`
3. 변경 사항을 커밋합니다: `git commit -m 'feat: add some feature'`
4. 브랜치를 push합니다: `git push origin feature/your-feature`
5. `main` 브랜치 대상으로 Pull Request를 엽니다.

### 커밋 메시지 규칙

이 프로젝트는 [Conventional Commits](https://www.conventionalcommits.org/)를 따릅니다.

```
feat:     새 기능
fix:      버그 수정
docs:     문서 업데이트
style:    코드 포맷팅(로직 변경 없음)
refactor: 코드 리팩터링
perf:     성능 개선
test:     테스트 관련 변경
chore:    빌드 / 도구 변경
```

예시:

```
feat: add DingTalk bot support
fix: handle 429 rate-limit with retry backoff
docs: update README deployment section
```

### 코드 스타일

- Python 코드는 PEP 8을 따릅니다(줄 길이: 120).
- 함수와 클래스에 docstring을 추가하세요.
- 바로 이해하기 어려운 로직에는 주석을 추가하세요.
- 새 기능을 추가할 때 관련 문서도 업데이트하세요.

### CI 검사

PR을 열면 CI가 다음 PR 검사를 자동으로 실행합니다.

| 검사 | 설명 | 필수 |
|-------|-------------|:--------:|
| `backend-gate` | `scripts/ci_gate.sh` — py_compile + flake8 치명 오류 + `./scripts/test.sh code` + `./scripts/test.sh yfinance` + 오프라인 pytest | ✅ |
| `docker-build` | Docker 이미지 빌드 및 핵심 모듈 import smoke test | ✅ |
| `web-gate` | `npm run lint` + `npm run build` (`apps/dsa-web/` 변경 시 트리거) | ✅ (트리거된 경우) |

별도로 저장소에는 `.github/workflows/network-smoke.yml`의 비차단 `network-smoke` 워크플로도 있지만, Pull Request가 아니라 `schedule`과 `workflow_dispatch`에서만 트리거됩니다.

**로컬에서 검사 실행:**

```bash
# Backend gate(권장)
pip install -r requirements.txt
pip install flake8 pytest
./scripts/ci_gate.sh

# Frontend gate(apps/dsa-web/를 변경한 경우에만)
cd apps/dsa-web
npm ci
npm run lint
npm run build
```

### 문서 동기화 규칙

중국어 핵심 문서(예: `docs/full-guide.md`)를 수정하는 경우, PR 설명에 해당 영어 문서를 업데이트했는지 **반드시 명시**해야 합니다. 업데이트하지 않았다면 이유를 설명하세요.

## 📋 기여 우선 영역

- 🔔 새 알림 채널(예: Slack, Matrix)
- 🤖 새 AI 모델 연동
- 📊 새 데이터 소스 어댑터
- 🐛 버그 수정 및 성능 개선
- 📖 문서 개선 및 번역

## ❓ 질문

다음 방법을 자유롭게 이용하세요.
- 토론을 위해 Issue 열기
- 기존 Issues와 Discussions 살펴보기

기여해 주셔서 감사합니다! 🎉
