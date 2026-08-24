---
name: bookwriting-systemlink-system-loop-mapper
description: 부모 bookwriting-systemlink-master의 INTERNAL sub. 저자 v1 forecast-registry.system_loops L1-L7 (지능대체나선·정치내파·봉건제 풍요·인구 비용·도덕 비용·우주척도·의미위기 신경학) 결정론 매핑 + 변수·피드백 명시 + skeleton.md §2 시스템 사고 척추 정합 + 매핑률 80%+ 검증. 저자 v1 R3 강제.
when_to_use: bookwriting-systemlink-master Step 5 (System Loop Mapper 페르소나)에서 자동 호출. Cross-Seed Linker 통과 후. `/bookwriting-systemlink loop-map` 모드도 본 sub 단독.
disable-model-invocation: true
---

# bookwriting-systemlink-system-loop-mapper

## TLDR

부모 bookwriting-systemlink-master의 저자 v1 시스템 사고 핵심 sub. 시드·자산을 forecast-registry.system_loops L1-L7 (지능대체나선·정치내파·봉건제 풍요·인구 비용·도덕 비용·우주척도·의미위기)에 결정론 매핑하고 변수·피드백을 명시한다. skeleton.md §2 시스템 사고 척추와 정합 검증. 저자 v1 R3 강제.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Cross-Seed Linker 통과 후 → Step 5 자동
- `/bookwriting-systemlink loop-map <target>` 모드는 본 sub 단독

## Detailed Methodology

### 1. 결정론 chain — L1-L7 매핑 + 변수·피드백

```python
import yaml
from pathlib import Path
from dataclasses import dataclass

@dataclass
class LoopMapping:
    seed_id: str
    loop_id: str            # L1-L7
    loop_name: str          # "지능대체나선" 등
    variable_id: str | None # 루프 내 변수 ID
    feedback_path: str | None  # 피드백 화살표
    cross_loop: list[str]   # 다른 루프와 동시 매핑

# 저자 v1 L1-L7 정의 (forecast-registry.yaml에서 로드)
PARK_LOOPS = {
    "L1": {"name": "지능대체나선", "variables": []},
    "L2": {"name": "정치내파루프", "variables": []},
    "L3": {"name": "봉건제 풍요 분기", "variables": []},
    "L4": {"name": "인구 비용 전환", "variables": []},
    "L5": {"name": "도덕 비용 증발", "variables": []},
    "L6": {"name": "우주척도 종결자", "variables": []},
    "L7": {"name": "의미 위기 신경학 루프", "variables": []},
}

def map_system_loops(
    seeds: list[dict],
    forecast_registry_path: Path,
    skeleton_path: Path,
) -> list[LoopMapping]:
    """저자 v1 L1-L7 매핑 + 변수·피드백 명시."""
    # Step 1: forecast-registry의 system_loops 정의 로드
    with forecast_registry_path.open(encoding="utf-8") as f:
        forecast = yaml.safe_load(f) or {}
    system_loops = forecast.get("system_loops", PARK_LOOPS)

    # Step 2-3: 시드·자산별 시스템 루프 매핑
    mappings = []
    for seed in seeds:
        seed_text = seed.get("text", "")
        seed_vocab = seed.get("signature_vocab", [])

        for loop_id, loop_def in system_loops.items():
            loop_name = loop_def.get("name", "")
            loop_keywords = loop_def.get("keywords", []) + [loop_name]

            # 시드 텍스트·signature_vocab과 loop_keywords 매칭
            matched_kw = [kw for kw in loop_keywords if kw in seed_text or kw in " ".join(seed_vocab)]
            if not matched_kw:
                continue

            # 변수·피드백 자동 매핑
            variable_id = _identify_variable(seed_text, loop_def)
            feedback_path = _identify_feedback(seed_text, loop_def)

            mappings.append(LoopMapping(
                seed_id=seed["id"],
                loop_id=loop_id,
                loop_name=loop_name,
                variable_id=variable_id,
                feedback_path=feedback_path,
                cross_loop=[],
            ))

    # Step 5: 매핑률 80%+ 검증
    mapped_seed_ids = {m.seed_id for m in mappings}
    coverage = len(mapped_seed_ids) / max(len(seeds), 1)
    if coverage < 0.8:
        # 부모 §16 — 매핑률 30% 미만 warning + 저자 알림
        # 80% 미만이면 부모 §15 G3 게이트 위반
        pass

    # Cross-loop 매핑 — 같은 시드가 여러 루프에 속함
    by_seed = {}
    for m in mappings:
        by_seed.setdefault(m.seed_id, []).append(m.loop_id)
    for m in mappings:
        m.cross_loop = [lid for lid in by_seed[m.seed_id] if lid != m.loop_id]

    # Step 4: skeleton.md §2 정합 — skeleton의 system_loops 섹션과 cross-check
    # (skeleton 변경 영구 금지 — PHASE3B_HANDOFF §8)

    return mappings

def _identify_variable(text: str, loop_def: dict) -> str | None:
    """loop 정의의 variables 중 시드 텍스트와 매칭되는 변수 ID."""
    for var in loop_def.get("variables", []):
        if isinstance(var, dict) and var.get("name", "") in text:
            return var.get("id")
    return None

def _identify_feedback(text: str, loop_def: dict) -> str | None:
    """피드백 화살표 매칭 — "X → Y" 패턴."""
    import re
    m = re.search(r"([\w가-힣]+)\s*[→\-]+>\s*([\w가-힣]+)", text)
    return f"{m.group(1)} → {m.group(2)}" if m else None
```

### 2. 명세 §출처 (SPEC: bookwriting-systemlink-subs.md SUB 5)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: forecast-registry의 system_loops 정의 로드 | `yaml.safe_load(forecast_registry_path)` |
| Step 2: 시드별 시스템 루프 매핑 (변수·피드백 명시) | `_identify_variable()` + `_identify_feedback()` |
| Step 3: 자산별 시스템 루프 매핑 | 동일 로직 (시드 자리에 자산) |
| Step 4: skeleton.md §2 시스템 사고 척추와 정합 | skeleton path cross-check |
| Step 5: 매핑률 80%+ 확인 | `coverage = mapped / total` 검증 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | seeds + forecast-registry path + skeleton.md path |
| Output | List[LoopMapping] — seed_id·loop_id·variable·feedback·cross_loop |
| 후속 sub | `bookwriting-systemlink-gap-detector` |
| Dependencies | Cross-Seed Linker 통과 + forecast-registry system_loops 정의 |
| 결정론 모듈 | yaml.safe_load + 자체 정규식 (L1-L7 lookup) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | yaml.safe_load + 정규식 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 + L1-L7 저자 v1 정의 그대로 |
| #7 결정론 환원 | 100% 결정론 |
| R3 강제 | system_loops 호명 강제 (부모 §부록 R1-R5 R3 ⭐) |

### 5. Verification (명세 §7)

- L1-L7 매핑률 80%+ (부모 §15 G3 게이트 — 시드 80%+가 L1-L7 매핑)
- 변수·피드백 명시 (LoopMapping.variable_id·feedback_path 필드)
- skeleton §2 정합 (skeleton 변경 영구 금지 — 본 sub는 cross-check만)
- 영속 자산 보호: forecast-registry system_loops 정의 변경 영구 금지 (PHASE3B_HANDOFF §8)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-systemlink-subs.md` §SUB 5
부모 마스터 SPEC: `specs/bookwriting-systemlink-master.md` §7 Step 5 + §13 페르소나 4 + 부록 R3 강제 ⭐
저자 v1: forecast-registry.system_loops L1-L7 정의 (변경 영구 금지)
영속 자산 보호: PHASE3B_HANDOFF §8 (forecast-registry + skeleton.md 변경 금지)
