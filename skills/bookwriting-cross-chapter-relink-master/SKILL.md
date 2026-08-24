---
name: bookwriting-cross-chapter-relink-master
description: 저자 책 ⑪ 최종 단계 마스터 — POLISHED 장간 결정론 연결. M6 RelevanceScorer cross-chapter BM25 + system_loops L1-L7 전 권역 연결 검증 + 저자 5 시그니처 분포 글로벌 균형 + forecast P-NNN cross-reference 일관성. micro_since_last_relink ≥10 자동 발동.
when_to_use: "`/bookwriting cycle` Step 11 자동. micro_since_last_relink ≥10 자동 발동."
---

# bookwriting-cross-chapter-relink-master (⑪ 최종 단계 마스터)

## TLDR

POLISHED 장들 간 cross-reference·시그니처 분포·L1-L7 권역 연결 결정론 검증. 단행본 차원 정합성 최종 가드.

## Triggers

- `/bookwriting cycle <target>` Step 11 자동
- `micro_since_last_relink >= 10` 자동 발동 (cycle-registry global counter)
- `/bookwriting-cross-chapter-relink <target>` — 저자 직접
- `/bookwriting-cross-chapter-relink loop-trace <loop_id>` — 단일 loop 전 chapter 추적
- `/bookwriting-cross-chapter-relink signature-balance` — 시그니처 글로벌 분포만

## Detailed Methodology

### 1. 결정론 chain

```python
import paths
from relevance_scorer import RelevanceScorer
from signature_pattern_applier import SignaturePatternApplier
from forecast_registry_syncer import ForecastRegistrySyncer
from lifecycle_state_machine import LifecycleStateMachine, LifecycleState
from pathlib import Path

# Step 1: POLISHED 장 모음 로드
polished_chapters = load_polished_chapters()

# Step 2: M6 cross-chapter BM25 — 의미적 연결 강도
scorer = RelevanceScorer(corpus=polished_chapters)
chapter_links = []
for ch_a, ch_b in itertools.combinations(polished_chapters, 2):
    score = scorer.bm25(ch_a.text, ch_b.text)
    if score >= 0.5:  # 의미적 연결 임계
        chapter_links.append({"from": ch_a.id, "to": ch_b.id, "score": score})

# Step 3: system_loops L1-L7 전 권역 chapter 추적
syncer = ForecastRegistrySyncer(paths.forecast_registry_path())
loop_to_chapters = {f"L{i}": [] for i in range(1, 8)}
for p in syncer.registry["predictions"]:
    for loop in p.get("system_loops", []):
        loop_id = loop.get("loop_id") if isinstance(loop, dict) else loop
        chapter = p.get("chapter_id")
        if loop_id in loop_to_chapters and chapter:
            loop_to_chapters[loop_id].append(chapter)

# 저자 v15: 각 L_n은 최소 2 chapter cross-reference
sparse_loops = [l for l, chs in loop_to_chapters.items() if len(set(chs)) < 2]

# Step 4: 저자 5 시그니처 글로벌 분포 균형
applier = SignaturePatternApplier()
sig_by_chapter = {ch.id: applier.count_in_draft(ch.text) for ch in polished_chapters}
# 표준편차로 균형 측정
import statistics
sig_stdev = statistics.stdev(sig_by_chapter.values()) if len(sig_by_chapter) > 1 else 0
if sig_stdev > 2.5:  # 분포 너무 흩어짐
    imbalance = {ch_id: cnt for ch_id, cnt in sig_by_chapter.items()
                 if abs(cnt - statistics.mean(sig_by_chapter.values())) > 2.5}
else:
    imbalance = {}

# Step 5: forecast cross_reference 일관성 — 두 chapter 모두 P-NNN 등록 필수
cross_ref_violations = []
for p in syncer.registry["predictions"]:
    refs = p.get("cross_references", [])
    for ref in refs:
        ref_chapter = ref.get("chapter_id") if isinstance(ref, dict) else ref
        if not any(p2.get("chapter_id") == ref_chapter for p2 in syncer.registry["predictions"]):
            cross_ref_violations.append({"from": p["id"], "missing_chapter": ref_chapter})

# Step 6: lifecycle POLISHED 유지
fsm = LifecycleStateMachine()
new_state = fsm.transition(LifecycleState.POLISHED, LifecycleState.POLISHED)
# is_terminal=True 확인
assert fsm.is_terminal(new_state)
```

### 2. 게이트 매트릭스

| 검사 | 통과 조건 |
|---|---|
| BM25 chapter_links | 모든 chapter ≥1 link |
| L1-L7 sparse_loops | 빈 loop ≤1 |
| 시그니처 stdev | ≤ 2.5 |
| cross_ref_violations | == [] |

### 3. micro_since_last_relink 자동 reset

```python
cycle_reg["global_counters"]["micro_since_last_relink"] = 0
```

### 4. 저자 escalate 조건

- BM25 isolated chapter (모든 다른 chapter와 < 0.3) → "이 장은 다른 장과 의미적으로 단절. 시드 추가 필요"
- L1-L7 sparse loop ≥2 → "이 loop 권역 결손. 시드·근거 추가 필요"
- 시그니처 분포 stdev > 2.5 → "저자 5 시그니처 글로벌 분포 불균형"
- cross_ref_violation ≥1 → "P-NNN cross_reference가 등록되지 않은 chapter를 참조"

### 5. lifecycle 유지

```python
# POLISHED → POLISHED (terminal state, cross-chapter-relink는 단행본 차원 메타 검증)
# 추가 시드·사이클 발생 시 다시 SEED 진입
```

### 6. 단행본 차원 게이트 (전체 chapter 풀이 POLISHED일 때만 발동)

```python
all_polished = all(ch.lifecycle == "POLISHED" for ch in chapters)
if not all_polished:
    return {"action": "defer", "message": "POLISHED 미완 chapter 있음 — 부분 relink 건너뜀"}
```

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ forecast cross_reference 일관성 검증 |
| #4 저자 작가성·정체성 | ✅ 시그니처 글로벌 분포 + L1-L7 권역 연결 |
| #7 결정론 환원 | ✅ M6·M8·M12·M11 pure Python |

## 출처

SPEC: `specs/bookwriting-cross-chapter-relink-master.md`
실행 모듈: `lib/relevance_scorer.py` + `lib/signature_pattern_applier.py` + `lib/forecast_registry_syncer.py` + `lib/lifecycle_state_machine.py`

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 6개 sub-skill을 자동 orchestration — 저자 책 13장 cross-reference·횡단 backbone.

| 순서 | Sub-skill | 호출 시점 | 페르소나 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-cross-chapter-relink-cross-checker` | Step 1 | Cross Checker | M6 BM25 + N×N |
| 2 | `bookwriting-cross-chapter-relink-conflict-detector` ⭐ | Step 2 | Conflict Detector (챕터 간) | 정규식 3 모순 (수치·시점·논리) |
| 3 | `bookwriting-cross-chapter-relink-cross-ref-suggester` | Step 3 | Cross-ref Suggester | M6 BM25 + dict 집계 |
| 4 | `bookwriting-cross-chapter-relink-reroute-recommender` | Step 4 | Reroute Recommender | confidence 0.7 분기 |
| 5 | `bookwriting-cross-chapter-relink-loop-coherence-checker` | Step 5 | Loop Coherence Checker | yaml + variable_usage dict |
| 6 | `bookwriting-cross-chapter-relink-registry-coherence-validator` | Step 6 | Registry Coherence Validator | M12 + M13 + R1-R5 |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-cross-chapter-relink cycle
↓ Step 1
bookwriting-cross-chapter-relink-cross-checker (모든 챕터 N×N + M6 BM25)
↓ Step 2
bookwriting-cross-chapter-relink-conflict-detector ⭐ (수치 30%vs25%·시점 2030vs2035·논리 X→Y vs X→Z)
↓ Step 3
bookwriting-cross-chapter-relink-cross-ref-suggester (secondary 챕터 매핑 후보)
↓ Step 4
bookwriting-cross-chapter-relink-reroute-recommender (primary 재라우팅 ★ 추천)
↓ Step 5
bookwriting-cross-chapter-relink-loop-coherence-checker (L1-L7 책 전체 일관성 90%+)
↓ Step 6
bookwriting-cross-chapter-relink-registry-coherence-validator (R1-R5 책 전체 정합 — 마지막 검증)
↓
Master Synthesis: 책 전체 cross-reference 그래프 + Phase 3-C 진입 게이트
```

### 저자 결정 묶음 강제
- Conflict Detector 챕터 간 모순 발견 시 저자 묶음 *강제* (자동 결정 영구 금지)
- Reroute Recommender confidence < 0.7 저자 묶음 / ≥0.7 ★ 추천
- Loop Coherence Checker 변수 정의 모순 시 저자 묶음
- Registry Coherence Validator R1-R5 위반 시 ④·⑤·⑥ 재호출 권장

### OrchestratorTracer (M18) 자동 기록
deterministic_modules_used 누적: M6·M12·M13 + 자체 정규식·dict. Phase 3-B 결정론 backbone 완성 단계.
