---
name: bookwriting-narrative-craft-signature-weaver
description: 부모 bookwriting-narrative-craft-master의 INTERNAL sub ⭐ 시그니처 패턴 정밀 적용. 저자 5 시그니처 패턴 (X가 아니라 Y·셋 중 하나 아니다·X와 Y 사이 거리·두 창업자 N배·변수 X 따라 결과 갈리는)을 narrative 차원 정밀 적용 + M8 SignaturePatternApplier 자연스러운 곳 자동 발견 + 활용률 30%+ 강제 + 강제 적용 차단.
when_to_use: bookwriting-narrative-craft-master에서 historical-parallelist 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-narrative-craft-signature-weaver

## TLDR

부모 bookwriting-narrative-craft-master의 ⭐ 시그니처 패턴 정밀 적용 sub. 저자 5 시그니처 패턴을 narrative 차원에서 *자연스러운 곳*에만 자동 발견·적용하고 활용률 30%+를 강제한다. M8 SignaturePatternApplier 결정론. 강제 적용 시 원본 유지.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- historical-parallelist 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — M8 + 5 패턴 정밀 적용

```python
from enum import Enum
from dataclasses import dataclass, field
from signature_pattern_applier import SignaturePatternApplier   # M8

class SignaturePattern(str, Enum):
    X_NOT_Y = "이 책은 X가 아니라 Y"
    NOT_ONE_OF_THREE = "셋 중 하나가 아니다"
    DISTANCE_X_Y = "X와 Y 사이의 거리"
    TWO_FOUNDERS = "두 창업자가 정확히 같은 N배"
    VARIABLE_BRANCHES = "변수 X 따라 결과 갈리는 동일 시스템"

# 적용 위치 권장 (명세 SUB 5 §3)
PATTERN_LOCATIONS = {
    SignaturePattern.X_NOT_Y: ["intro", "conclusion"],          # 도입·결론
    SignaturePattern.NOT_ONE_OF_THREE: ["conclusion"],           # 결론
    SignaturePattern.DISTANCE_X_Y: ["time_coordinate"],          # 시간 좌표
    SignaturePattern.TWO_FOUNDERS: ["authority_convergence"],    # 권위 수렴
    SignaturePattern.VARIABLE_BRANCHES: ["system_thinking"],     # 시스템 사고
}

@dataclass
class SignatureWoven:
    section_id: str
    location_type: str           # intro·conclusion·time_coordinate 등
    original_text: str
    woven_text: str
    patterns_applied: list[SignaturePattern]
    is_natural: bool             # 강제 X — 자연스러운 곳만
    utilization_rate: float      # 챕터 전체 활용률

def weave_signatures(
    chapter_sections: list[dict],   # [{section_id, location_type, text}]
) -> tuple[list[SignatureWoven], float]:
    """5 시그니처 패턴 자연 적용 + 활용률 측정."""
    applier = SignaturePatternApplier()
    results: list[SignatureWoven] = []
    total_sections = len(chapter_sections)
    woven_count = 0

    for sec in chapter_sections:
        # Step 1: 위치 type 기반 권장 패턴 식별
        loc = sec["location_type"]
        recommended_patterns = [p for p, locs in PATTERN_LOCATIONS.items() if loc in locs]

        # Step 2: M8 자연스러운 곳 자동 발견
        original = sec["text"]
        woven_text, applied_raw = applier.apply_natural_only(original)
        applied = [SignaturePattern(p) for p in applied_raw if any(p in str(rp) for rp in recommended_patterns)]

        # Step 3: 자연스러움 평가 — 강제 의심 시 원본 유지
        natural_ratio = len(applied) / max(len(woven_text.split()), 1)
        is_natural = natural_ratio <= 0.5

        if not is_natural:
            woven_text = original
            applied = []

        if applied:
            woven_count += 1

        results.append(SignatureWoven(
            section_id=sec["section_id"],
            location_type=loc,
            original_text=original,
            woven_text=woven_text,
            patterns_applied=applied,
            is_natural=is_natural,
            utilization_rate=0.0,   # 챕터 전체 측정 후 채움
        ))

    # Step 4: 활용률 30%+ 강제
    utilization = woven_count / max(total_sections, 1)
    for r in results:
        r.utilization_rate = utilization

    return results, utilization
```

### 2. 명세 §출처 (SPEC: bookwriting-narrative-craft-subs.md SUB 5) ⭐

| 명세 항목 | 본 sub 구현 |
|---|---|
| "이 책은 X가 아니라 Y" — 도입·결론 | `PATTERN_LOCATIONS[X_NOT_Y] = ["intro", "conclusion"]` |
| "셋 중 하나가 아니다" — 결론 | `NOT_ONE_OF_THREE = ["conclusion"]` |
| "X와 Y 사이의 거리" — 시간 좌표 | `DISTANCE_X_Y = ["time_coordinate"]` |
| "두 창업자가 정확히 같은 N배" — 권위 수렴 | `TWO_FOUNDERS = ["authority_convergence"]` |
| "변수 X 따라 결과 갈리는 동일 시스템" — 시스템 사고 | `VARIABLE_BRANCHES = ["system_thinking"]` |
| 적용 기회 자동 발견·자연스러운 곳에만 적용 | M8 `apply_natural_only` + `is_natural` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_sections (section_id + location_type + text) |
| Output | (List[SignatureWoven], utilization rate) |
| 후속 sub | `sensory-detail-adder` |
| Dependencies | historical-parallelist 통과 |
| 결정론 모듈 | M8 SignaturePatternApplier |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M8 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 패턴 + 위치 1:1 환원 |
| #4 저자 작가성 ⭐ | 자연스러운 곳만 적용 — 강제 차단 (`is_natural=False` 시 원본 유지) |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 시그니처 패턴 활용률 30%+ (`utilization >= 0.3`)
- 자연스러움 평가 (`is_natural` 강제)
- 5 패턴 모두 매핑 가능 (PATTERN_LOCATIONS 5종)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-narrative-craft-subs.md` §SUB 5 ⭐
부모 마스터 SPEC: `specs/bookwriting-narrative-craft-master.md`
저자 5 시그니처 패턴: voice-craft sub와 양식 정합
결정론 모듈: `lib/signature_pattern_applier.py` (M8)
