---
name: bookwriting-structure-review-layer-ratio-measurer
description: 부모 bookwriting-structure-review-master의 INTERNAL sub. 1·2·3층 분량 비율 결정론 측정 — M5 LayerRatioMeasurer로 narrative.md·analysis.md·implications.md 단어 수 측정 + book-config.layer_ratios range (10-15% / 60-70% / 15-25%) 비교 + 위반 severity (low·medium·high) 분류 + 저자 v1 정합.
when_to_use: bookwriting-structure-review-master cycle 진입 시 자동 첫 단계. ⑨ 풀 사이클 진입.
disable-model-invocation: true
---

# bookwriting-structure-review-layer-ratio-measurer

## TLDR

부모 bookwriting-structure-review-master의 ① 진입 sub. M5 LayerRatioMeasurer로 chapters/<ch>의 3 layer 파일 단어 수를 결정론 측정하고 book-config.layer_ratios range (1층 13/65/22 또는 v1 10-15·60-70·15-25)와 비교하여 위반 severity를 분류한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- ⑨ structure-review cycle 진입 시 자동 첫 단계
- 다른 sub의 입력 (resize-recommender 등)

## Detailed Methodology

### 1. 결정론 chain — M5 LayerRatioMeasurer

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from layer_ratio_measurer import LayerRatioMeasurer   # M5

class Severity(str, Enum):
    NONE = "none"
    LOW = "low"          # < 5% 차이
    MEDIUM = "medium"    # 5-15% 차이
    HIGH = "high"        # > 15% 차이

@dataclass
class LayerMeasurement:
    chapter_id: str
    total_words: int
    layer1_words: int
    layer2_words: int
    layer3_words: int
    layer1_ratio: float       # 0-1
    layer2_ratio: float
    layer3_ratio: float
    layer1_violation: Severity
    layer2_violation: Severity
    layer3_violation: Severity

def measure_layer_ratios(
    chapter_id: str,
    chapter_dir: Path,
    book_config_path: Path,
) -> LayerMeasurement:
    """3 layer 분량 결정론 측정."""
    measurer = LayerRatioMeasurer()

    # Step 1: wc -w narrative.md / analysis.md / implications.md
    layer_files = {
        "1": chapter_dir / "narrative.md",
        "2": chapter_dir / "analysis.md",
        "3": chapter_dir / "implications.md",
    }
    word_counts = {}
    for layer, path in layer_files.items():
        word_counts[layer] = measurer.count_words(path) if path.exists() else 0

    total = sum(word_counts.values())

    # Step 2: 각 layer 비율 계산
    ratios = {
        layer: (count / total if total > 0 else 0.0)
        for layer, count in word_counts.items()
    }

    # Step 3: book-config.layer_ratios range 비교
    with book_config_path.open(encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    target_ratios = config.get("voice_guidelines", {}).get("structure", {}).get("layer_ratios", {})

    # Step 4: 위반 severity 분류
    violations = {}
    for layer in ("1", "2", "3"):
        target = target_ratios.get(f"layer{layer}", {})
        target_min = target.get("min", 0.0)
        target_max = target.get("max", 1.0)
        actual = ratios[layer]
        if actual < target_min:
            diff = target_min - actual
        elif actual > target_max:
            diff = actual - target_max
        else:
            diff = 0.0

        if diff == 0.0:
            violations[layer] = Severity.NONE
        elif diff < 0.05:
            violations[layer] = Severity.LOW
        elif diff < 0.15:
            violations[layer] = Severity.MEDIUM
        else:
            violations[layer] = Severity.HIGH

    return LayerMeasurement(
        chapter_id=chapter_id,
        total_words=total,
        layer1_words=word_counts["1"],
        layer2_words=word_counts["2"],
        layer3_words=word_counts["3"],
        layer1_ratio=ratios["1"],
        layer2_ratio=ratios["2"],
        layer3_ratio=ratios["3"],
        layer1_violation=violations["1"],
        layer2_violation=violations["2"],
        layer3_violation=violations["3"],
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-structure-review-subs.md SUB 1)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: wc -w narrative.md / analysis.md / implications.md | M5 `measurer.count_words()` |
| Step 2: 총 단어 수 + 각 layer 비율 계산 | `ratios` dict |
| Step 3: book-config.layer_ratios range 비교 | `target_ratios` lookup |
| Step 4: 위반 severity (low·medium·high) | `Severity` enum 4종 (none 포함) |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + chapter_dir + book_config path |
| Output | LayerMeasurement — counts·ratios·violations 3 layer |
| 후속 sub | element-checker-layer2/3 + resize-recommender |
| Dependencies | book-config.voice_guidelines.structure.layer_ratios |
| 결정론 모듈 | M5 LayerRatioMeasurer |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M5 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 분량 측정 정확도 99%+ (M5 회귀)
- range 검증 정합 (book-config 정합)
- severity 분류 정확 (4단계)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-structure-review-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-structure-review-master.md`
결정론 모듈: `lib/layer_ratio_measurer.py` (M5)
저자 v1 layer_ratios: book-config.voice_guidelines.structure.layer_ratios (변경 영구 금지 — PHASE3B_HANDOFF §8)
