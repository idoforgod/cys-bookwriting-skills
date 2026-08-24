---
name: bookwriting-content-expand-system-loop-narrator
description: 부모 bookwriting-content-expand-master의 INTERNAL sub. 저자 2층 골격 요소 4 (시스템 루프 호명) 담당. 저자 v1 forecast-registry.system_loops L1-L7 결정론 로드 + "L1 지능대체나선의 변수 1 — 인지 외주화" 형식 명시 호명 + 변수 간 피드백 명시 + 300-600자 본문 골격 + 저자 v1 chapter-pipeline 2층 요소 4 양식 정합.
when_to_use: bookwriting-content-expand-master에서 driving-force-synthesizer 통과 후 자동 호출. ③ systemlink-system-loop-mapper의 매핑을 활용.
disable-model-invocation: true
---

# bookwriting-content-expand-system-loop-narrator

## TLDR

부모 bookwriting-content-expand-master의 저자 2층 골격 *요소 4* 담당. forecast-registry.system_loops L1-L7을 결정론 로드하여 "L1 지능대체나선의 변수 1 — 인지 외주화" 형식으로 명시 호명한다. 변수 간 피드백 + 300-600자 본문 골격. ③ systemlink-system-loop-mapper 매핑 활용.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- driving-force-synthesizer 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — L1-L7 명시 호명 + 변수·피드백

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class SystemLoopNarrative:
    insight_id: str
    loops_named: list[str]              # ["L1", "L7"] 등
    variables_named: list[dict]          # [{"loop": "L1", "variable_id": "v1", "name": "인지 외주화"}]
    feedback_paths: list[str]            # ["변수 1 → 변수 2 → 변수 1 강화"]
    body_text: str                       # 300-600자 골격

def narrate_system_loop(
    insight: dict,
    system_loop_mappings: list[dict],    # ③ systemlink-system-loop-mapper 산출
    forecast_registry_path: Path,
) -> SystemLoopNarrative:
    """L1-L7 명시 호명 + 변수·피드백 결정론 narration."""
    # Step 1: 통찰·시드의 system_loops 매핑 로드
    with forecast_registry_path.open(encoding="utf-8") as f:
        forecast = yaml.safe_load(f) or {}

    # Step 2: 저자 L1-L7 정의 참조 (forecast-registry)
    system_loops_def = forecast.get("system_loops", {})

    loops_named: list[str] = []
    variables_named: list[dict] = []
    feedback_paths: list[str] = []

    for mapping in system_loop_mappings:
        if mapping.get("seed_id") != insight.get("id") and mapping.get("source_id") != insight.get("id"):
            continue
        loop_id = mapping.get("loop_id", "")
        if not loop_id:
            continue

        if loop_id not in loops_named:
            loops_named.append(loop_id)

        # Step 3: "L1 지능대체나선의 변수 1 — 인지 외주화" 형식 명시 호명
        loop_def = system_loops_def.get(loop_id, {})
        var_id = mapping.get("variable_id")
        var_name = ""
        if var_id:
            for v in loop_def.get("variables", []):
                if isinstance(v, dict) and v.get("id") == var_id:
                    var_name = v.get("name", "")
                    break
        variables_named.append({
            "loop": loop_id,
            "variable_id": var_id,
            "name": var_name,
            "loop_name": loop_def.get("name", ""),
        })

        # Step 4: 변수 간 피드백 명시
        feedback = mapping.get("feedback_path")
        if feedback:
            feedback_paths.append(feedback)

    # Step 5: 본문 골격 작성 + 저자 시스템 사고 어휘 풍부 사용
    body = _assemble_loop_narrative(insight, loops_named, variables_named, feedback_paths)

    return SystemLoopNarrative(
        insight_id=insight.get("id", ""),
        loops_named=loops_named,
        variables_named=variables_named,
        feedback_paths=feedback_paths,
        body_text=body,
    )

def _assemble_loop_narrative(insight, loops, variables, feedbacks) -> str:
    lines = ["[2층 요소 4 — 시스템 루프 호명]"]
    for v in variables:
        lines.append(f"- {v['loop']} {v['loop_name']}의 변수 {v['variable_id']} — {v['name']}")
    for fb in feedbacks:
        lines.append(f"- 피드백: {fb}")
    lines.append("[저자 본문 300-600자 채워넣기 — 저자 시스템 사고 어휘 풍부]")
    return "\n".join(lines)
```

### 2. 명세 §출처 (SPEC: bookwriting-content-expand-subs.md SUB 3)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 통찰·시드의 system_loops 매핑 로드 | `system_loop_mappings` 입력 (③ sub 산출) |
| Step 2: 저자 L1-L7 정의 (forecast-registry) 참조 | `yaml.safe_load(forecast_registry_path)` |
| Step 3: "L1 지능대체나선의 변수 1 — 인지 외주화" 형식 호명 | `variables_named` 4 필드 |
| Step 4: 변수 간 피드백 명시 | `feedback_paths` 리스트 |
| Step 5: 본문 작성 + 저자 시스템 사고 어휘 | `_assemble_loop_narrative()` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | insight + system_loop_mappings (③ systemlink 산출) + forecast-registry path |
| Output | SystemLoopNarrative — loops_named·variables_named·feedback_paths·body_text |
| 후속 sub | `bookwriting-content-expand-voice-aligner` (또는 scenario-brancher 분기) |
| Dependencies | driving-force-synthesizer 통과 + ③ systemlink-system-loop-mapper 산출 |
| 결정론 모듈 | yaml.safe_load + dict lookup |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | yaml + dict 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step + 호명 양식 1:1 환원 |
| #4 저자 작가성 | 본문 300-600자는 저자 직접 — sub는 골격 + 호명만 |
| #7 결정론 환원 | 100% 결정론 |
| R3 강제 | system_loops 호명 — 저자 v1 chapter-pipeline 2층 요소 4 |

### 5. Verification (명세 §7)

- L1-L7 중 1개 이상 명시적 호명 (`loops_named` ≥ 1)
- 변수·피드백 명시 (`variables_named` + `feedback_paths`)
- 저자 v1 chapter-pipeline.md 2층 요소 4 양식 정합

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-content-expand-subs.md` §SUB 3
부모 마스터 SPEC: `specs/bookwriting-content-expand-master.md` (2층 요소 4 시스템 루프)
③ systemlink 정합: `skills/bookwriting-systemlink-master/sub-skills/bookwriting-systemlink-system-loop-mapper/SKILL.md` (동일 L1-L7 데이터)
영속 자산 보호: PHASE3B_HANDOFF §8 (forecast-registry read-only)
