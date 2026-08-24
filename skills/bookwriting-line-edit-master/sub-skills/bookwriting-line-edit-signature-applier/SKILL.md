---
name: bookwriting-line-edit-signature-applier
description: 부모 bookwriting-line-edit-master의 INTERNAL sub ⭐ strict 시그니처 패턴 정밀 적용. 저자 5 시그니처 패턴 적용 기회 자동 발견 + 자연 흐름 보존 (강제 X) + 활용률 35%+ 강제 (cross-cutting 30% 보다 엄격). M8 SignaturePatternApplier 결정론.
when_to_use: bookwriting-line-edit-master에서 vocabulary-refiner 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-line-edit-signature-applier

## TLDR

부모 bookwriting-line-edit-master의 ⭐ 시그니처 정밀 적용 sub. M8 SignaturePatternApplier로 저자 5 시그니처 패턴을 강제 적용 차단 + 자연 흐름 보존 + 활용률 35%+ 강제한다. ⑥·⑧ sub들의 30%보다 엄격.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- vocabulary-refiner 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — M8 + 35%+ 강제

```python
from pathlib import Path
from dataclasses import dataclass, field
from signature_pattern_applier import SignaturePatternApplier   # M8

STRICT_UTILIZATION_TARGET = 0.35   # cross-cutting 0.30 보다 엄격
NATURAL_FLOW_LIMIT = 0.5

@dataclass
class SignatureApplyResult:
    section_id: str
    original_text: str
    applied_text: str
    patterns_used: list[str]
    is_natural: bool
    utilization_rate: float

def apply_signatures_strict(
    sections: list[dict],
) -> tuple[list[SignatureApplyResult], float]:
    """5 시그니처 패턴 strict 35%+ 적용."""
    applier = SignaturePatternApplier()
    results: list[SignatureApplyResult] = []
    applied_count = 0

    for sec in sections:
        original = sec["text"]

        # Step 1-2: 본문 구조 분석 + 5 시그니처 패턴 적용 기회 발견
        applied_text, patterns = applier.apply_natural_only(original)

        # Step 3: 자연 흐름 보존 (강제 X) — natural_ratio 검사
        natural_ratio = len(patterns) / max(len(applied_text.split()), 1)
        is_natural = natural_ratio <= NATURAL_FLOW_LIMIT
        if not is_natural:
            applied_text = original
            patterns = []

        if patterns:
            applied_count += 1

        results.append(SignatureApplyResult(
            section_id=sec["section_id"],
            original_text=original,
            applied_text=applied_text,
            patterns_used=patterns,
            is_natural=is_natural,
            utilization_rate=0.0,
        ))

    # Step 4: 활용률 35%+ 도달 확인
    utilization = applied_count / max(len(sections), 1)
    for r in results:
        r.utilization_rate = utilization

    return results, utilization
```

### 2. 명세 §출처 (SPEC: bookwriting-line-edit-subs.md SUB 2) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 본문 구조 분석 (단락·문장) | `for sec in sections` |
| Step 2: 5 시그니처 패턴 적용 기회 발견 | M8 `applier.apply_natural_only` |
| Step 3: 적용 시도 (자연 흐름 보존 — 강제 X) | `NATURAL_FLOW_LIMIT = 0.5` |
| Step 4: 활용률 35%+ 도달 확인 | `STRICT_UTILIZATION_TARGET = 0.35` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | sections (vocabulary-refiner 통과) |
| Output | (List[SignatureApplyResult], utilization rate) |
| 후속 sub | ai-tone-purger |
| Dependencies | vocabulary-refiner 통과 |
| 결정론 모듈 | M8 SignaturePatternApplier |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M8 결정론 |
| #2 grill-me 원문 일치 | 명세 5 패턴 + 35%+ 1:1 |
| #4 저자 작가성 ⭐ | 자연 흐름 보존 — 강제 차단 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- 시그니처 패턴 활용률 35%+ (`utilization >= 0.35`)
- 자연스러운 곳에만 적용 (억지 0건)
- 저자 spot-check 통과
- 저자 책 *고유 voice* 강화

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-line-edit-subs.md` §SUB 2 ⭐
부모 마스터 SPEC: `specs/bookwriting-line-edit-master.md`
결정론 모듈: `lib/signature_pattern_applier.py` (M8)
⑥·⑧ signature-weaver와 다른 sub: line-edit이 strict 35%+ (다른 sub 30%)
