---
name: bookwriting-structure-review-resize-recommender
description: 부모 bookwriting-structure-review-master의 INTERNAL sub. layer ratio 위반 분석 + 5% 범위 내 자동 resize 시도 + 큰 위반은 저자 묶음 (확장·축약·재호출 3 옵션) escalate. layer-ratio-measurer 산출 활용.
when_to_use: bookwriting-structure-review-master에서 r5-verifier 통과 후 마지막 자동 호출 (⑨ 마지막 sub).
disable-model-invocation: true
---

# bookwriting-structure-review-resize-recommender

## TLDR

부모 bookwriting-structure-review-master의 마지막 sub. layer ratio 위반 severity 분석 후 5% 범위 내 (low)는 자동 resize 시도, 그 이상 (medium·high)는 저자 묶음 escalate (확장·축약·재호출 3 옵션).

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- r5-verifier 통과 후 자동 (⑨ structure-review 마지막 sub)

## Detailed Methodology

### 1. 결정론 chain — severity 분기 + 저자 묶음

```python
from enum import Enum
from dataclasses import dataclass, field

class ResizeOption(str, Enum):
    EXPAND = "expand"
    SHRINK = "shrink"
    REINVOKE = "reinvoke"    # ⑦ content-expand 재호출

@dataclass
class ResizeRecommendation:
    chapter_id: str
    auto_resize_attempted: list[str]      # 자동 시도된 layer
    bundle_required_layers: list[str]     # 저자 묶음 필요 layer
    bundle_options: list[ResizeOption] = field(default_factory=lambda: list(ResizeOption))

def recommend_resize(
    chapter_id: str,
    layer_measurement,        # bookwriting-structure-review-layer-ratio-measurer 산출
) -> ResizeRecommendation:
    """layer ratio 위반 → 자동 resize 또는 저자 묶음."""
    auto_resized: list[str] = []
    bundle_layers: list[str] = []

    # Step 1: layer ratio 위반 분석
    violations = {
        "1": layer_measurement.layer1_violation,
        "2": layer_measurement.layer2_violation,
        "3": layer_measurement.layer3_violation,
    }

    for layer, severity in violations.items():
        sev_str = severity.value if hasattr(severity, "value") else str(severity)
        # Step 2: 5% 범위 내 (low) → 자동 resize 시도
        if sev_str == "low":
            auto_resized.append(layer)
        # Step 3: medium·high → 저자 묶음 (확장·축약·재호출)
        elif sev_str in ("medium", "high"):
            bundle_layers.append(layer)

    return ResizeRecommendation(
        chapter_id=chapter_id,
        auto_resize_attempted=auto_resized,
        bundle_required_layers=bundle_layers,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-structure-review-subs.md SUB 7)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: layer ratio 위반 분석 | `violations` dict |
| Step 2: 5% 범위 내 → 자동 resize 시도 | `severity == "low"` 분기 |
| Step 3: 큰 위반 → 저자 묶음 (확장·축약·재호출) | `ResizeOption` 3 enum |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + layer_measurement (layer-ratio-measurer 산출) |
| Output | ResizeRecommendation — auto_resized·bundle_required·bundle_options |
| 후속 단계 | 저자 묶음 또는 ⑦ 재호출 |
| Dependencies | layer-ratio-measurer 통과 |
| 결정론 모듈 | enum + dict 분기 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | enum 결정론 |
| #2 grill-me 원문 일치 | 명세 3 Step + 3 옵션 1:1 |
| #4 저자 작가성 | 큰 위반 저자 묶음 강제 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 자동 resize 정확도 (`auto_resize_attempted` low severity만)
- 저자 묶음 명확 (`bundle_options` 3 enum)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-structure-review-subs.md` §SUB 7
부모 마스터 SPEC: `specs/bookwriting-structure-review-master.md`
layer-ratio-measurer 정합: `bookwriting-structure-review-layer-ratio-measurer`
