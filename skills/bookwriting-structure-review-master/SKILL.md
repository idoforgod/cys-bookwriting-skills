---
name: bookwriting-structure-review-master
description: 저자 책 ⑨ 단계 마스터 — 장·절·소절 구조 결정론 리뷰. forecast-registry P-NNN R1-R5 정합 + system_loops L1-L7 균형 분포 + chapter_role 1층·2층·3층 비율 + seed-registry 누락 시드 detect. M12 ForecastRegistrySyncer + M5 LayerRatioMeasurer + M6 RelevanceScorer.
when_to_use: "`/bookwriting cycle` Step 9 자동. micro_since_last_structure ≥6 자동 발동."
---

# bookwriting-structure-review-master (⑨ 단계 마스터)

## TLDR

장·절 구조의 정합성 결정론 리뷰. R1-R5 + L1-L7 분포 + 시드 누락·중복 + chapter_role 비율 통합 게이트.

## Triggers

- `/bookwriting cycle <target>` Step 9 자동
- `micro_since_last_structure >= 6` 자동 발동 (cycle-registry global counter)
- `/bookwriting-structure-review <chapter_id>` — 저자 직접
- `/bookwriting-structure-review loop-balance` — L1-L7 분포만
- `/bookwriting-structure-review seed-coverage` — 누락 시드 detect만

## Detailed Methodology

### 1. 결정론 chain

```python
import paths
from forecast_registry_syncer import ForecastRegistrySyncer
from layer_ratio_measurer import LayerRatioMeasurer
from relevance_scorer import RelevanceScorer
from pathlib import Path
import yaml

# Step 1: forecast-registry R1-R5 전면 검증
syncer = ForecastRegistrySyncer(paths.forecast_registry_path())
violations = syncer.verify_all()
total_violations = sum(len(v) for v in violations.values())

# Step 2: system_loops L1-L7 분포 균형 검사
loop_distribution = {f"L{i}": 0 for i in range(1, 8)}
for p in syncer.registry["predictions"]:
    for loop in p.get("system_loops", []):
        loop_id = loop.get("loop_id") if isinstance(loop, dict) else loop
        if loop_id in loop_distribution:
            loop_distribution[loop_id] += 1

# 저자 v15 균형 임계 — 각 L_n 최소 3건
sparse_loops = [l for l, c in loop_distribution.items() if c < 3]

# Step 3: chapter_role 비율 검사 — 1층 13% / 2층 65% / 3층 22%
role_counts = {"1층_콜드오픈": 0, "2층_분석": 0, "3층_함의": 0}
for p in syncer.registry["predictions"]:
    role = p.get("chapter_role")
    if role in role_counts:
        role_counts[role] += 1
total = sum(role_counts.values())
ratios = {k: v / total for k, v in role_counts.items()} if total else {}

# Step 4: seed-registry 시드 누락·중복 검사
with open(paths.seed_registry_path()) as f:
    seed_reg = yaml.safe_load(f.read())
seed_ids = [s["id"] for s in seed_reg.get("seeds") or []]
duplicates = [sid for sid in seed_ids if seed_ids.count(sid) > 1]

# Step 5: M6 BM25 chapter간 유사도 — 중복 콘텐츠 detect
scorer = RelevanceScorer(corpus=chapter_drafts)
similarity_matrix = scorer.pairwise_similarity()
dup_pairs = [(a, b) for a, b in similarity_matrix if similarity_matrix[(a, b)] > 0.85]
```

### 2. 게이트 매트릭스

| 검사 | 통과 조건 |
|---|---|
| R1-R5 total_violations | == 0 |
| L1-L7 sparse_loops | 빈 loop ≤1 (저자 6 임계) |
| chapter_role 1층 | 0.08 ≤ ratio ≤ 0.18 |
| chapter_role 2층 | 0.60 ≤ ratio ≤ 0.70 |
| chapter_role 3층 | 0.17 ≤ ratio ≤ 0.27 |
| seed duplicates | == [] |
| chapter dup_pairs | == [] (BM25 ≥0.85) |

### 3. micro_since_last_structure 자동 reset

```python
# 통과 후 cycle-registry global counter 결정론 reset
cycle_reg["global_counters"]["micro_since_last_structure"] = 0
```

### 4. 저자 escalate 조건

- R1-R5 위반 ≥1 → 즉시 저자 escalate
- L1-L7 sparse ≥2 → "이 loop들을 채울 시드 추가 필요" escalate
- chapter_role 비율 ±5% 초과 이탈 → 저자 결정 호출

### 5. lifecycle 유지

```python
# INSIGHTED → INSIGHTED (structure-review는 메타 검증, 상태 변경 없음)
```

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ R1-R5 결정론 일괄 검증 |
| #4 저자 작가성·정체성 | ✅ chapter_role 13/65/22 + L1-L7 균형 강제 |
| #7 결정론 환원 | ✅ M12·M5·M6·M11 pure Python |

## 출처

SPEC: `specs/bookwriting-structure-review-master.md`
실행 모듈: `lib/forecast_registry_syncer.py` + `lib/layer_ratio_measurer.py` + `lib/relevance_scorer.py` + `lib/lifecycle_state_machine.py`

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 7개 sub-skill을 자동 orchestration — 저자 v1 1·2·3층 + R4·R5 검증 backbone.

| 순서 | Sub-skill | 호출 시점 | 검증 영역 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-structure-review-layer-ratio-measurer` | Step 1 | 1·2·3층 분량 비율 | M5 LayerRatioMeasurer |
| 2 | `bookwriting-structure-review-element-checker-layer2` | Step 2 | 저자 v1 2층 7요소 | 7 정규식 |
| 3 | `bookwriting-structure-review-element-checker-layer3` | Step 3 | 저자 v1 3층 6요소 | 6 정규식 |
| 4 | `bookwriting-structure-review-flow-validator` | Step 4 | 1→2→3 흐름 일관성 | M6 BM25 |
| 5 | `bookwriting-structure-review-r4-distribution-analyzer` | Step 5 | 권위 5층 분포·편중 | yaml + dict 분포 |
| 6 | `bookwriting-structure-review-r5-verifier` | Step 6 | R5 verification_signal 누락 | yaml + P-NNN lookup |
| 7 | `bookwriting-structure-review-resize-recommender` | Step 7 | 분량 위반 자동 resize | severity 분기 |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-structure-review cycle <chapter>
↓ Step 1
bookwriting-structure-review-layer-ratio-measurer (M5 — 13/65/22 target 비율 검증)
↓ Step 2
bookwriting-structure-review-element-checker-layer2 (7 요소 ✅/⚠️)
↓ Step 3
bookwriting-structure-review-element-checker-layer3 (6 요소 ✅/⚠️)
↓ Step 4
bookwriting-structure-review-flow-validator (M6 BM25 1→2→3 흐름)
↓ Step 5
bookwriting-structure-review-r4-distribution-analyzer (Grade A-E 분포·50%+ 편중 검출)
↓ Step 6
bookwriting-structure-review-r5-verifier (verification_signal·falsifies_if 누락)
↓ Step 7
bookwriting-structure-review-resize-recommender (low → 자동 resize, medium·high → 저자 묶음 3옵션)
↓
Master Synthesis: 챕터 구조 종합 보고 + 저자 묶음 (위반 시)
```

### 저자 결정 묶음 강제
- Flow Validator 흐름 끊김 시 저자 묶음 (자동 결정 영구 금지)
- R4 Distribution 편중 50%+ 시 저자 R4 권장
- R5 Verifier 누락 시 ④ verification-signal-finder 재호출 권장
- Resize Recommender medium·high severity 시 저자 묶음 3 옵션 (확장·축약·재호출)

### OrchestratorTracer (M18) 자동 기록
deterministic_modules_used: M5·M6 + yaml·dict·정규식.

### PROH-006 마크다운 위반 게이트 (2026-05-25 신설 — 8번째 게이트)

기존 7 게이트(Layer Ratio·Layer-2·Layer-3·Flow·R4·R5·Resize)에 8번째 게이트 추가.

```python
# Step 8: 마크다운 기호 위반 검출
import re
MD_PATTERNS = [
    (r'^#{1,6}\s+', 'heading'),
    (r'\*\*.+?\*\*', 'bold'),
    (r'(?<!\*)\*(?!\*).+?\*(?!\*)', 'italic'),
    (r'^>\s', 'blockquote'),
    (r'^\s*[-*]\s', 'bullet'),
    (r'^---+$', 'hr'),
    (r'^```', 'code_fence'),
]
violations = {}
for pat, name in MD_PATTERNS:
    hits = re.findall(pat, manuscript_text, re.MULTILINE | re.DOTALL)
    if hits:
        violations[name] = len(hits)
```

게이트 매트릭스 추가:

| 검사 | 통과 조건 |
|---|---|
| markdown_violations (표 제외) | == 0 |

위반 발견 시:
- 즉시 line-edit-master 자동 재호출 (PROH-006 집행)
- structure-review 재발동
- 저자 묶음 발동 (위반 종류·위치 명시)

book-config :: PROH-006 critical 일치. 진북 #1·#4·#7 동시 보호.
