---
name: bookwriting-absorb-master
description: 저자 책 ① 단계 마스터 — 진입 정밀도. inbox/import 자산을 4 type (seed·evidence·insight·cycle-input)으로 분류·시드 등록·라우팅 제안. frontmatter 우선 + 자동 추측 fallback. M7 IdGenerator 결정론 호출. 옵션 A+ 자기완결.
when_to_use: "`/bookwriting cycle` 진행 Step 2 자동 발동. 저자 명시 `/bookwriting absorb` 또는 `/bookwriting import <path>` 호출."
---

# bookwriting-absorb-master (① 진입 마스터)

## TLDR

저자 외부 manual 호출 결과 (foresight 사슬·NotebookLM bridge·시드 입력)를 *진입 정밀도*로 분류·등록. 모든 후속 단계의 *입력 품질*이 ① absorb의 정밀도로 결정.

## Triggers

- `/bookwriting cycle <target>` Step 2 자동
- `/bookwriting absorb` 또는 `/bookwriting inbox process` — inbox 일괄 흡수
- `/bookwriting import <path> --as <type> [--to|--link]` — 즉시 import
- `/bookwriting-absorb classify <path>` — 분류만

## Detailed Methodology

### 1. 4 type 자동 분류 (Q13-D-2)

| type | 트리거 키워드·패턴 | 라우팅 |
|---|---|---|
| seed | 짧은 명제·통찰·1문장 | seed-registry |
| evidence | 출처·인용·통계 풍부 | chapters/<ch>/evidence-track |
| insight | "통찰·결론·해석" 단어 | chapter pending-insights |
| cycle-input | 외골격·구조·flow | bookwriting-master 직접 전달 |

frontmatter `type` 명시 시 → 즉시 사용
frontmatter 없음 → 자동 추측 (confidence 점수) → < 0.7 시 저자 묶음

### 2. 라우팅 cascade L1·L2·L3 (Q20-D-3)

```python
import paths
from relevance_scorer import RelevanceScorer
from pathlib import Path

# L1: skeleton.md 키워드 매칭
skeleton = paths.skeleton_path()
scorer = RelevanceScorer([skeleton])
score_l1 = scorer.score(seed_text, skeleton)

if score_l1 >= 0.8:
    # 명확 → 라우팅 결정
    ...
elif score_l1 < 0.8:
    # L2 Claude 의미 평가 → L3 Obsidian 풀
    ...
```

### 3. Citation Gate Medium만 적용 (예외)

저자 흡수 결정 자유 보장 — Critical 즉시 차단 *유일한 예외*. citation-gate.md §3 Philosophy 명시. 후속 ② fact-anchor 이후로는 Critical 즉시 차단.

### 4. ID 발급 (M7 결정론)

```python
import paths
from id_generator import IdGenerator
import yaml
from pathlib import Path

registry_path = paths.seed_registry_path()
with open(registry_path) as f:
    registry = yaml.safe_load(f.read())

current_ids = [s.get("id") for s in (registry.get("seeds") or [])]
max_num = IdGenerator.compute_max_num(current_ids, "S")

gen = IdGenerator(registry_path)
new_seed_id = gen.issue("seed", current_max_num=max_num)
```

### 5. inbox 정리 (atomic write)

```python
from atomic_writer import AtomicWriter
import shutil

# 처리 완료 → _processed/ 이동
processed_dir = inbox_dir / "_processed"
processed_dir.mkdir(exist_ok=True)
shutil.move(str(inbox_file), str(processed_dir / inbox_file.name))
```

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ M2 Medium 감지 + 흡수 자유 명시 예외 |
| #3 출처 명시 | ✅ frontmatter `source`·`citation` 메타 추출 |
| #4 저자 작가성 | ✅ 저자 명시 호출 우선 (`--as`·`--to`) |
| #7 결정론 환원 | ✅ M7 IdGenerator + M6 RelevanceScorer 결정론 cascade |

## 출처

SPEC: `specs/bookwriting-absorb-master.md` (17 항목 풀)
실행 모듈: `lib/id_generator.py` + `lib/relevance_scorer.py` + `lib/citation_detection.py`
호출자: `bookwriting-master` Step 2

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 4개 sub-skill을 자동 orchestration. M18 OrchestratorTracer가 각 호출을 결정론 기록.

| 순서 | Sub-skill | 호출 시점 | AI Agent 페르소나 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-absorb-frontmatter-parser` | Step 2 | Frontmatter Parser | yaml.safe_load |
| 2 | `bookwriting-absorb-type-classifier` | Step 3 (frontmatter `type` 누락 시) | Type Classifier | 규칙 매칭 + LLM eval fallback |
| 3 | `bookwriting-absorb-route-cascade` ⭐ | Step 6 | Route Cascade | M6 RelevanceScorer (BM25) |
| 4 | `bookwriting-absorb-inbox-organizer` | Step 9 | Inbox Organizer | pathlib·shutil |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-absorb <mode> [target]
↓
Step 2: bookwriting-absorb-frontmatter-parser 자동 호출
  Input: inbox/*.md 또는 --target <path>
  Output: frontmatter dict + 누락 필드 목록
↓ (type 누락 시)
Step 3: bookwriting-absorb-type-classifier 자동 호출
  Input: 본문 + partial frontmatter
  Output: TypeGuess (type_value, confidence, method)
  ⚠ confidence < 0.7 → 저자 묶음 escalate
↓ (--to·--link 명시 없을 시)
Step 6: bookwriting-absorb-route-cascade 자동 호출
  Input: type 분류된 자산 + book-config search_paths
  Output: RouteCandidate (chapter, layer, section, cascade_layer L1/L2/L3)
↓
Step 9: bookwriting-absorb-inbox-organizer 자동 호출
  Input: 처리 결과 list[dict]
  Output: _processed/·_failed/ 이동 + 통계
↓
Master Synthesis: cycle-registry.outputs 갱신 + 저자 화면 출력
```

### 저자 결정 묶음 강제 (자동 결정 영구 금지)
- Type Classifier confidence < 0.7 → 저자 묶음
- Route Cascade L3까지도 confidence < 0.5 → unrouted + 저자 묶음

### OrchestratorTracer (M18) 자동 기록 양식

```python
from orchestrator_tracer import OrchestratorTracer
tracer = OrchestratorTracer(master_name="bookwriting-absorb-master")
tracer.record(skill_name="bookwriting-absorb-frontmatter-parser", sequence=1, ...)
tracer.record(skill_name="bookwriting-absorb-type-classifier", sequence=2, ...)
tracer.record(skill_name="bookwriting-absorb-route-cascade", sequence=3, ...)
tracer.record(skill_name="bookwriting-absorb-inbox-organizer", sequence=4, ...)
cycle_entry["orchestrator_trace"] = tracer.export()
```
