---
name: bookwriting-cross-chapter-relink-loop-coherence-checker
description: 부모 bookwriting-cross-chapter-relink-master의 INTERNAL sub. 저자 v1 L1-L7 시스템 루프 책 전체 정합 검증 — 모든 챕터의 system_loops 매핑 로드 + 같은 루프 변수가 챕터 간 일관성 유지하는지 결정론 검증 + 변수 누락·정의 모순 발견 시 저자 묶음 + 매핑률 90%+ 목표.
when_to_use: bookwriting-cross-chapter-relink-master에서 reroute-recommender 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-cross-chapter-relink-loop-coherence-checker

## TLDR

부모 bookwriting-cross-chapter-relink-master의 시스템 루프 정합 sub. 저자 v1 L1-L7 루프가 책 전체 13장에서 일관성 유지하는지 결정론 검증한다. 같은 변수 정의 모순·변수 누락 발견 시 저자 묶음 강제. 매핑률 90%+ 목표.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- reroute-recommender 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — L1-L7 책 전체 정합

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class LoopCoherenceResult:
    total_chapters: int
    mapped_chapters: int
    mapping_rate: float
    variable_inconsistencies: list[dict]   # 같은 변수 다른 정의
    missing_variables: list[dict]          # 챕터에서 호명됐으나 정의 없음
    needs_bundle: bool

def check_loop_coherence(
    chapters_dir: Path,
    forecast_registry_path: Path,
    target_mapping_rate: float = 0.9,
) -> LoopCoherenceResult:
    """L1-L7 일관성 결정론 검증."""
    # Step 1: 모든 챕터의 system_loops 매핑 로드
    with forecast_registry_path.open(encoding="utf-8") as f:
        forecast = yaml.safe_load(f) or {}
    system_loops_def = forecast.get("system_loops", {})

    # 변수 정의 인덱스 — 챕터 간 변수 사용 추적
    variable_usage: dict[tuple[str, str], list[dict]] = {}    # (loop_id, var_name) → [{chapter, definition}]

    total_chapters = 0
    mapped_chapters = 0

    for chapter_dir in chapters_dir.iterdir():
        if not chapter_dir.is_dir():
            continue
        total_chapters += 1

        # chapter의 system_loops 매핑 — seed-track.system_loops 필드
        seed_track = chapter_dir / "seed-track.yaml"
        if not seed_track.exists():
            continue

        with seed_track.open(encoding="utf-8") as f:
            track = yaml.safe_load(f) or {}

        has_loop_mapping = False
        for seed in track.get("seeds", []):
            loop_mapping = seed.get("system_loops", []) or seed.get("connections", {}).get("system_loops", [])
            if not loop_mapping:
                continue
            has_loop_mapping = True

            for mapping in loop_mapping if isinstance(loop_mapping, list) else [loop_mapping]:
                if not isinstance(mapping, dict):
                    continue
                loop_id = mapping.get("loop_id")
                var_name = mapping.get("variable") or mapping.get("variable_name")
                if not loop_id or not var_name:
                    continue
                key = (loop_id, var_name)
                variable_usage.setdefault(key, []).append({
                    "chapter": chapter_dir.name,
                    "definition": mapping.get("definition", ""),
                })

        if has_loop_mapping:
            mapped_chapters += 1

    # Step 2-3: 같은 루프 변수가 챕터 간 *일관성 유지*하는지
    inconsistencies: list[dict] = []
    for (loop_id, var_name), usages in variable_usage.items():
        # 같은 변수에 다른 정의
        definitions = {u["definition"] for u in usages if u["definition"]}
        if len(definitions) > 1:
            inconsistencies.append({
                "loop_id": loop_id,
                "variable": var_name,
                "definitions": list(definitions),
                "chapters": [u["chapter"] for u in usages],
            })

    # 변수 누락 — system_loops_def에 정의된 변수가 챕터에서 호명 안 됨
    missing: list[dict] = []
    for loop_id, loop_def in system_loops_def.items():
        for var in loop_def.get("variables", []):
            if not isinstance(var, dict):
                continue
            var_name = var.get("name")
            if not var_name:
                continue
            if (loop_id, var_name) not in variable_usage:
                missing.append({"loop_id": loop_id, "variable": var_name})

    # Step 4: 매핑률 + 저자 묶음
    mapping_rate = mapped_chapters / max(total_chapters, 1)
    needs_bundle = bool(inconsistencies) or mapping_rate < target_mapping_rate

    return LoopCoherenceResult(
        total_chapters=total_chapters,
        mapped_chapters=mapped_chapters,
        mapping_rate=mapping_rate,
        variable_inconsistencies=inconsistencies,
        missing_variables=missing,
        needs_bundle=needs_bundle,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-cross-chapter-relink-subs.md SUB 5)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 모든 챕터의 system_loops 매핑 로드 | `for chapter_dir` + seed-track yaml read |
| Step 2: 같은 루프 변수가 챕터 간 *일관성 유지*하는지 검증 | `variable_usage` dict + `definitions` set |
| Step 3: 변수 누락·정의 모순 발견 시 저자 묶음 | `inconsistencies` + `missing_variables` |
| Step 4: 매핑률 90%+ 목표 | `mapping_rate >= target` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapters_dir + forecast_registry_path + target_mapping_rate |
| Output | LoopCoherenceResult — mapping_rate·inconsistencies·missing·bundle |
| 후속 sub | registry-coherence-validator |
| Dependencies | reroute-recommender 통과 + forecast-registry.system_loops + 모든 챕터 seed-track |
| 결정론 모듈 | yaml.safe_load + dict 집계 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | yaml + dict 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 |
| #4 저자 작가성 | 모순·누락 저자 묶음 강제 |
| R3 강제 | system_loops 호명 책 전체 정합 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- L1-L7 일관성 90%+ (`mapping_rate >= 0.9`)
- 변수 모순 검출 (`variable_inconsistencies`)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-cross-chapter-relink-subs.md` §SUB 5
부모 마스터 SPEC: `specs/bookwriting-cross-chapter-relink-master.md`
③ systemlink-system-loop-mapper + ⑤ evidence-link-loop-integrator 정합 — 본 sub는 *책 전체 단위*
영속 자산 보호: PHASE3B_HANDOFF §8 (forecast-registry read-only)
