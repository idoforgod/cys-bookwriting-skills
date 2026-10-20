# cys-bookwriting-skills

**책 한 권을 끝까지 쓰기 위한 Claude Code 스킬 묶음.**
착상 하나를 원고 한 문단으로 바꾸는 11단계를, 문체 검문과 출처 검문을 통과시키며 반복한다.

[English](README.en.md) · [MIT License](LICENSE)

---

## 이게 왜 필요한가

AI에게 "이 주제로 한 챕터 써줘"라고 하면 그럴듯한 글이 나온다. 문제는 그다음이다.

- **문체가 내 것이 아니다.** 세 챕터를 쓰면 세 사람이 쓴 것처럼 읽힌다.
- **출처가 없거나, 있는데 가짜다.** "한 보고서에 따르면"으로 시작하는 문장이 늘어난다.
- **예측이 반증 불가능하다.** "크게 변할 것이다"는 예측이 아니라 수사다.
- **책 전체가 안 보인다.** 12장을 쓸 때쯤 3장에 뭐라고 썼는지 기억나지 않는다.

이 스킬 묶음은 그 네 가지를 **기계가 검사하게** 만든다. LLM에게 "문체가 비슷한 것 같아?"라고 묻지 않는다.
점수를 계산하는 파이썬 모듈이 따로 있고, 임계값에 미달하면 진행이 막힌다.

> 이 도구는 한 미래학자가 자기 책을 쓰려고 만들어 실제로 쓰던 시스템을, 누구나 자기 책에 쓸 수 있도록 정리한 것이다.
> 문서와 문체 규칙은 **한국어 산문**을 전제로 한다.

---

## 무엇이 들어 있나

### 11단계 파이프라인

착상(시드) 하나가 원고가 되기까지의 경로다. 각 단계는 독립된 스킬이며, 앞 단계 산출을 입력으로 받는다.

| # | 스킬 | 하는 일 |
|---|---|---|
| ① | `bookwriting-absorb-master` | 읽은 자료를 4종으로 분류하고 시드로 등록·라우팅 |
| ② | `bookwriting-fact-anchor-master` | 사실·수치를 앵커로 고정, 중복·충돌 검출 |
| ③ | `bookwriting-systemlink-master` | 등록된 자료 풀에서 관련 자산을 찾아 연결 (BM25) |
| ④ | `bookwriting-evidence-collect-master` | 인용 근거 수집 + 권위 등급화 (최소 2층 강제) |
| ⑤ | `bookwriting-evidence-link-master` | 주장마다 근거를 연결, 고립된 주장 검출 |
| ⑥ | `bookwriting-insight-synthesis-master` | 근거를 통찰 명제로 종합 |
| ⑦ | `bookwriting-content-expand-master` | 통찰을 본문으로 확장 (당신이 개입하는 지점) |
| ⑧ | `bookwriting-narrative-craft-master` | 장면·서사로 읽히게 조립 |
| ⑨ | `bookwriting-structure-review-master` | 장 구조·층 비율·누락 시드 점검 |
| ⑩ | `bookwriting-line-edit-master` | 문장 단위 첨삭, AI 어조 제거 |
| ⑪ | `bookwriting-cross-chapter-relink-master` | 장간 연결·중복 정리 |

`bookwriting-master`가 이 11개를 오케스트레이션하는 진입점이고, 그 아래 **70개의 서브스킬**이 세부를 담당한다.

여기에 선택 스킬 하나가 더 있다. `bookwriting-notebooklm-bridge` — NotebookLM 자료를 끌어오는 유일한 외부 통로이며, **당신이 명시적으로 부를 때만** 동작한다. 기본값은 꺼짐이다.

마지막 스킬은 `bookwriting-sentence-edit-master` — 원고를 붙여 넣으면 AI 말투와 자기반박을 걷어 내고 각주 번호·표·인용 출처를 지킨 채 다듬은 전문을 파일로 돌려주는 **최종 다듬기** 단계다. 파이프라인 밖에서 단독으로 부르며, 장르·분야·독자층과 무관한 범용 스킬이다.

합계 16개 = 11단계 + 상시 검문 2 + 오케스트레이터 1 + 선택 브리지 1 + 최종 다듬기 1.

### 상시 검문 2종

단계와 무관하게 **모든 산출물**에 걸린다.

| 스킬 | 막는 것 |
|---|---|
| `voice-gate` | 당신의 문체에서 벗어난 문장. `voice_score < 0.7`이면 재작성, 최종 원고는 `0.85` 이상 |
| `citation-gate` | 할루시네이션. 출처 파일 부재·모호한 출처·메타데이터 누락·URL/DOI 오류·출처 없는 통계 5종 신호를 감지해 **Critical이면 즉시 차단** |

### 결정론 모듈 18개

판단을 LLM에게 맡기지 않는 지점들이다. `lib/` 아래 파이썬 모듈로 구현되어 있다.

`VoiceScorer` · `HallucinationDetector` · `AuthorityGrader` · `QuantitativeExtraction` · `LayerRatioMeasurer` ·
`RelevanceScorer(BM25)` · `IdGenerator` · `SignaturePatternApplier` · `AITonePurger` · `AtomicWriter` ·
`ForecastRegistrySyncer` · `R4MultiLayerVerifier` · `LifecycleStateMachine` · `OrchestratorTracer` ·
`TraumaWitnessDetector` · `RiskAssessor` · `FactExtractor` · `AuthorWellnessGatekeeper`

### 예측 5규칙 (R1~R5)

미래를 다루는 책이라면 이게 핵심이다. 예측을 등록할 때 다섯 가지를 강제한다.

- **R1 정량 앵커** — "크게 늘어난다"가 아니라 "10년 내 3배"
- **R2 장 역할** — 1층 콜드오픈 / 2층 분석 / 3층 함의
- **R3 시스템 루프** — L1~L7 중 어느 되먹임 고리인가
- **R4 다층 권위** — 서로 다른 등급의 권위 2층 이상
- **R5 검증 신호·반증 조건** — **무엇이 관측되면 이 예측은 틀린 것인가**

R5를 쓸 수 없는 예측은 책에 넣지 않는다. 이 규칙 하나가 미래서와 점집을 가른다.

---

## 요구 사항

- **Python 3.9+** 와 **PyYAML**
- **Claude Code** (스킬을 읽어 실행하는 쪽)

---

## 설치

```bash
git clone https://github.com/idoforgod/cys-bookwriting-skills.git
cd cys-bookwriting-skills
./install.sh --book-root ~/my-book
```

`install.sh`가 하는 일은 셋뿐이다.

1. Python·PyYAML 확인 (없으면 PyYAML 설치 시도)
2. `skills/` 아래 16개를 `~/.claude/skills/`에 **심볼릭 링크** (`--copy`로 복사 가능)
3. `--book-root`를 주면 그 자리에 빈 책 프로젝트를 만든다

설치 후 셸 설정(`~/.zshrc` 등)에 추가해 두면 편하다.

```bash
export BOOKWRITING_HOME="$HOME/cys-bookwriting-skills"
export BOOKWRITING_BOOK_ROOT="$HOME/my-book"
alias bookwriting="python3 $BOOKWRITING_HOME/bin/bookwriting.py"
```

되돌리려면 `./install.sh --uninstall` — **스킬 링크만 지우고 원고는 손대지 않는다.**

---

## 시작하기

### 1. 책 프로젝트를 만든다

```bash
bookwriting init --root ~/my-book --title "내 책 제목" --author "내 이름"
```

이렇게 생긴다.

```
~/my-book/
├── master/
│   ├── book-config.yaml          ← 설정의 전부. 여기가 중심이다
│   ├── seed-registry.yaml        ← 착상 대장 (S-001, S-002 …)
│   ├── cycle-registry.yaml       ← 집필 사이클 대장 (C-001 …)
│   ├── forecast-registry.yaml    ← 예측 대장 (P-001 …)
│   └── sim-registry.yaml         ← 자동 시뮬레이션 대장 (SIM-001 …)
├── chapters/                     ← 장별 원고
├── inbox/                        ← 아직 분류 안 한 자료를 던져 넣는 곳
├── bookidea/skeleton.md          ← 목차와 사상적 척추
└── workflows/book-planning.md    ← 11단계 파이프라인 설명
```

### 2. 두 파일을 채운다 — 이 단계를 건너뛰면 도구가 작동하지 않는다

**`master/book-config.yaml`의 `voice_guidelines`** — 문체 검문의 **유일한 근거**다. 비워 두면 검문이 사실상 꺼진다.

```yaml
voice_guidelines:
  vocabulary:
    preferred: ["당신이 즐겨 쓰는 개념어", "..."]   # 5개 이상 권장
    avoid:     ["당신이 피하는 표현", "..."]
  sentence:
    max_length_chars: 80
  signature_expressions:                           # 당신만의 문장 패턴
    - "이 책은 X가 아니라 Y를 다룬다"
```

**`bookidea/skeleton.md`** — 목차와 사상적 척추. 각 장이 어느 명제에 매여 있는지 적는다.

### 3. 착상을 등록하고 굴린다

```bash
bookwriting seed register --text "지식노동의 단가가 0에 수렴할 때 무엇이 남는가" \
                          --chapter ch01 --role 2층_분석
bookwriting status
```

### 4. Claude Code에서 부른다

```
bookwriting-master 스킬로 S-001을 사이클 돌려줘
```

---

## 명령어

| 명령 | 하는 일 |
|---|---|
| `bookwriting init` | 책 프로젝트 부트스트랩 (최초 1회) |
| `bookwriting status` | 전체 자산 현황 |
| `bookwriting list seeds\|cycles\|forecasts\|sims` | 목록 조회 |
| `bookwriting seed register\|status\|reroute` | 시드 등록·조회·재라우팅 |
| `bookwriting cycle progress\|expand\|simulate\|polish` | 사이클 진행 |
| `bookwriting forecast register\|list` | 예측 등록 (R1~R5 강제) |
| `bookwriting chapter list\|init\|status` | 장 관리 |
| `bookwriting cite list\|grade` | 권위 DB 조회·등급 판정 |
| `bookwriting search` | 등록 자료 풀 BM25 검색 |
| `bookwriting validate` | 정합성 검증 |
| `bookwriting completion` | 책 전체 진척률 |
| `bookwriting trace` | 사이클 실행 추적 |
| `bookwriting backup\|restore\|prune` | 자산 백업·복구·정리 |
| `bookwriting healthcheck` | 설치·설정 종합 점검 |
| `bookwriting export` | 자산 마크다운 덤프 |

---

## 설정

| 환경변수 | 뜻 | 기본값 |
|---|---|---|
| `BOOKWRITING_BOOK_ROOT` | 책 프로젝트 루트 | 상위 폴더 탐색 → `~/bookwriting` |
| `BOOKWRITING_REFERENCE_PATHS` | 개인 참고자료 경로 (`:` 구분) | 없음 |
| `BOOKWRITING_HOME` | 이 저장소 위치 (셸 alias용) | — |
| `CLAUDE_SKILLS_DIR` | 스킬 설치 위치 | `~/.claude/skills` |

경로가 어떻게 잡혔는지 확인하려면:

```bash
python3 lib/paths.py
```

**절대 경로를 코드에 박지 않는다.** 모든 경로는 `lib/paths.py` 한 곳에서 해석된다.

---

## 알아 둘 것

- **문체 검문은 당신이 채운 만큼만 작동한다.** `voice_guidelines`가 비면 `voice_score`는 의미 없는 숫자가 된다.
- **`expert_pool/citation-authority-db.yaml`은 예시다.** 57개 항목이 들어 있지만 AI·미래학 분야에 치우쳐 있다. **자기 분야에 맞게 갈아 끼우고 쓰라.**
- **자기완결 원칙.** `book-config.yaml`의 `search_paths`에 등록되지 않은 경로는 읽지 않는다. 자격증명·키 파일은 `exclude_patterns`가 별도로 차단한다.
- **AI 협업 명시.** AI 생성 비율이 임계를 넘으면 발문에 협업 사실을 밝히도록 강제한다(`authorship_policy`). 이건 기능이지 버그가 아니다.
- **집필자 건강 게이트.** 심야 작업·연속 작업·일일 사이클 상한을 막는다. 끄고 싶으면 `author_wellness_policy.enabled: false`.
- **문서는 한국어다.** 문체 규칙도 한국어 산문을 전제한다. 다른 언어에서는 `voice-gate`의 문장 규칙을 손봐야 한다.

---

## 폴더 구조

```
cys-bookwriting-skills/
├── skills/          16개 스킬 (+ 70개 서브스킬)
├── lib/             결정론 모듈 18개 + paths.py
├── bin/             bookwriting.py (CLI)
├── templates/       init 이 펼치는 책 프로젝트 뼈대
├── specs/           설계 명세
├── docs/            설계 배경
├── expert_pool/     인용 권위 DB · 모듈 명세
└── install.sh
```

---

## 기여

이슈와 PR을 환영한다. 특히 다음이 반갑다.

- 다른 분야의 인용 권위 DB (의학·법학·경영·인문 등)
- 한국어 외 언어를 위한 문체 규칙
- 결정론 모듈의 정확도 개선

---

## 라이선스

MIT — Copyright (c) 2026 최윤식 (Yoonsik Choi). 자유롭게 쓰고, 고치고, 재배포하라.
