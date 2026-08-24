---
name: bookwriting-systemlink-master
description: 저자 책 ③ 단계 마스터 — 글쓰기 차원 시스템 사고 연관화. search_paths($BOOK_ROOT + Obsidian vault + 등록 자료 폴더)에서 시드 관련 자산 결정론 발견·연결. M6 RelevanceScorer (BM25) + M3 권위 등급화. system_loops L1-L7 매핑·빈 고리 발견. 옵션 A+ 자기완결.
when_to_use: "`/bookwriting cycle` Step 3 자동 발동. 저자 명시 `/bookwriting-systemlink cycle <target>` 호출도 가능."
---

# bookwriting-systemlink-master (③ 단계 마스터)

## TLDR

저자 v15 시스템 사고를 *글쓰기 차원*에서 구현. 시드와 search_paths 자산을 BM25 결정론 매칭 + system_loops L1-L7 매핑 + 빈 고리 발견.

## Triggers

- `/bookwriting cycle <target>` Step 3 자동
- `/bookwriting-systemlink cycle <target>` — 저자 직접
- `/bookwriting-systemlink search <query>` — 단순 검색
- `/bookwriting-systemlink loop-map <target>` — L1-L7 매핑만
- `/bookwriting-systemlink gap-detect <target>` — 빈 고리만

## Detailed Methodology

### 1. 결정론 chain (LLM 추론 영구 금지)

```python
import paths
from relevance_scorer import RelevanceScorer
from authority_grader import AuthorityGrader, Grade
from lifecycle_state_machine import LifecycleStateMachine, LifecycleState
from pathlib import Path
import yaml

# Step 1: search_paths 로드
with open(paths.book_config_path()) as f:
    config = yaml.safe_load(f.read())
tier1 = config["search_paths"]["tier_1_always"]
tier2 = config["search_paths"]["tier_2_explicit"]

# Step 2: corpus 구성 (옵션 A+ 자기완결 — search_paths 외 영구 금지)
corpus = []
for path_str in tier1 + tier2:
    p = Path(path_str)
    if p.is_dir():
        corpus.extend(p.glob("**/*.md"))

# Step 3: BM25 결정론 매칭
scorer = RelevanceScorer(corpus[:1000])  # N → 상위 1000 (성능)
ranked = scorer.rank(seed_text, top_n=20)
relevant = [(p, s) for p, s in ranked if s >= 0.7]

# Step 4: lifecycle SEED → LINKED 전환
fsm = LifecycleStateMachine()
new_state = fsm.transition(LifecycleState.SEED, LifecycleState.LINKED)
```

### 2. system_loops L1-L7 매핑 (저자 v15)

| Loop | 정의 |
|---|---|
| L1 | 지능대체나선 (자동화→실업→소비감소→더 큰 자동화) |
| L2 | 정치내파루프 |
| L3 | 봉건제·풍요 분기 (정치 변수) |
| L4 | 인구비용 전환 |
| L5 | 도덕비용 증발 |
| L6 | 우주척도 종결자 |
| L7 | 의미위기 신경학 루프 |

### 3. 빈 고리 검출

system_loops 매핑 후 *시드 ↔ L_n*의 *연결 누락 패턴* 자동 발견 — 저자 묶음 escalate ("이 빈 고리를 채울 시드 추가? 외부 호출?").

### 4. search_paths 외 검색 영구 금지 (옵션 A+)

```python
def validate_path(p: Path) -> bool:
    """search_paths 외 경로 검출 시 즉시 거부 (Round 8 #D5.2)."""
    resolved = p.resolve(strict=True)
    for root_str in tier1 + tier2:
        if str(resolved).startswith(str(Path(root_str).resolve())):
            return True
    return False
```

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ search_paths 외 결과 0 |
| #3 출처 명시 | ✅ M3 권위 등급화 |
| #4 저자 작가성 | ✅ Obsidian vault 저자 기존 사고 직접 연결 |
| #7 결정론 환원 | ✅ M6 BM25 pure Python + M11 lifecycle |

## 출처

SPEC: `specs/bookwriting-systemlink-master.md` (17 항목 풀)
실행 모듈: `lib/relevance_scorer.py` + `lib/authority_grader.py` + `lib/lifecycle_state_machine.py`

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 6개 sub-skill을 자동 orchestration.

| 순서 | Sub-skill | 호출 시점 | 페르소나 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-systemlink-asset-searcher` | Step 2 | Asset Searcher | M6 BM25 + subprocess·pathlib |
| 2 | `bookwriting-systemlink-obsidian-vault-searcher` ⭐ | Step 2 (Obsidian path) | Asset Searcher (Obsidian 전용) | M6 + 정규식 wikilinks·tags |
| 3 | `bookwriting-systemlink-asset-linker` | Step 3 | Asset Linker | M3 AuthorityGrader + yaml.safe_load |
| 4 | `bookwriting-systemlink-cross-seed-linker` | Step 4 | Cross-Seed Linker | M6 + 5 relation 정규식 |
| 5 | `bookwriting-systemlink-system-loop-mapper` | Step 5 | System Loop Mapper | yaml + L1-L7 dict lookup |
| 6 | `bookwriting-systemlink-gap-detector` ⭐ | Step 6 | Gap Detector | 그래프 알고리즘 + set 연산 |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-systemlink cycle <target>
↓ Step 2 자산 검색
bookwriting-systemlink-asset-searcher (search_paths grep·glob)
+ bookwriting-systemlink-obsidian-vault-searcher (Obsidian vault .md)
↓ Step 3 자산 연결
bookwriting-systemlink-asset-linker (citation 메타 + Grade)
↓ Step 4 시드 간 cross-reference
bookwriting-systemlink-cross-seed-linker (5 relation: extends·contrasts·examples·depends_on·pairs_with)
↓ Step 5 시스템 루프 호명
bookwriting-systemlink-system-loop-mapper (L1-L7 매핑 + 변수·피드백)
↓ Step 6 빈 고리 발견 ⭐
bookwriting-systemlink-gap-detector (3 빈 고리 패턴 + 저자 묶음 4 옵션)
↓
Master Synthesis: seed-registry connections 갱신 + lifecycle SEED→LINKED 또는 LINKED→EXPANDED
```

### 저자 결정 묶음 강제
- Gap Detector 빈 고리 발견 시 저자 묶음 4 옵션 (신 시드·외부 manual·재검색·defer)
- Cross-Seed Linker confidence < 0.7 시 LLM 의미 평가 fallback (단, confidence는 결정론)

### OrchestratorTracer (M18) 자동 기록
6 sub-skill 호출 시점·입력·산출물·deterministic_modules_used를 cycle-registry.outputs.orchestrator_trace에 영속.
