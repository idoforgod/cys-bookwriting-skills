---
name: bookwriting-absorb-type-classifier
description: 부모 bookwriting-absorb-master의 INTERNAL sub. frontmatter type 누락 시 4 type (seed·evidence·insight·cycle-input) 자동 추측. 결정론 규칙 매칭 + Claude 의미 평가 fallback. confidence < 0.7 시 저자 묶음 escalate.
when_to_use: bookwriting-absorb-master Step 3 (Type Classifier 페르소나)에서 자동 호출. Frontmatter Parser가 type 필드 누락 보고 시. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-absorb-type-classifier

## TLDR

부모 bookwriting-absorb-master의 type 추측 sub. frontmatter `type` 필드가 누락된 자산을 4 type (seed·evidence·insight·cycle-input) 중 하나로 *결정론 규칙 매칭* 후 모호 시 *Claude 의미 평가 fallback*. confidence < 0.7 시 저자 묶음 강제.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Frontmatter Parser가 `missing=["type", ...]` 반환 시 Step 3 자동
- `/bookwriting-absorb classify <path>` 모드는 type 추측만 단독 실행

## Detailed Methodology

### 1. 결정론 chain (규칙 우선·LLM fallback)

```python
from dataclasses import dataclass

@dataclass
class TypeGuess:
    type_value: str         # seed | evidence | insight | cycle-input
    confidence: float       # 0.0-1.0
    method: str             # "rule" | "llm_eval"

def classify(text: str, partial_meta: dict) -> TypeGuess:
    """저자 Q13-D-2 (c) 자동 추측 옵션 결정론 환원."""
    # Step 1: 규칙 매칭 (결정론 우선)
    # 짧은 명제·통찰 → seed
    if len(text) < 500 and any(kw in text for kw in ["라고 본다", "예측", "주장"]):
        return TypeGuess("seed", 0.85, "rule")

    # 출처·인용·통계 풍부 → evidence
    citation_count = text.count("출처") + text.count("Source") + text.count("doi")
    stat_count = sum(1 for kw in ["%", "배", "년", "$"] if kw in text)
    if citation_count >= 2 or stat_count >= 5:
        return TypeGuess("evidence", 0.80, "rule")

    # "통찰·결론·해석" 단어 → insight
    if any(kw in text for kw in ["통찰", "결론", "해석", "의미"]):
        return TypeGuess("insight", 0.78, "rule")

    # 외골격·구조·flow 단어 → cycle-input
    if any(kw in text for kw in ["외골격", "구조", "flow", "skeleton", "흐름 조정"]):
        return TypeGuess("cycle-input", 0.82, "rule")

    # Step 2: 규칙 모호 → Claude 의미 평가 (fallback)
    # (LLM 호출은 부모 마스터가 담당. 본 sub는 confidence 점수만 결정론 산출)
    return TypeGuess("seed", 0.55, "llm_eval")  # default seed, low confidence

# Step 3: confidence 게이트
def gate_confidence(guess: TypeGuess) -> str:
    if guess.confidence < 0.7:
        return "ESCALATE_BUNDLE"   # 저자 묶음 강제 (자동 결정 금지)
    return "PROCEED"
```

### 2. 명세 §출처 (SPEC: bookwriting-absorb-subs.md SUB 2)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 본문 텍스트 + frontmatter 부분 정보 로드 | `classify(text, partial_meta)` |
| Step 2: 규칙 매칭 (짧은 명제·통계·통찰·외골격) | 4 규칙 분기 결정론 |
| Step 3: 규칙 모호 시 Claude 의미 평가 | `method="llm_eval"` 분기 |
| Step 4: confidence 0-1 점수 | `TypeGuess.confidence: float` |
| Step 5: < 0.7 → 저자 묶음 escalate | `gate_confidence()` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | text (str) + partial_meta (dict, Frontmatter Parser 산출) |
| Output | TypeGuess (type_value, confidence, method) |
| 후속 sub | `bookwriting-absorb-route-cascade` (PROCEED) 또는 저자 묶음 (ESCALATE_BUNDLE) |
| Dependencies | `bookwriting-absorb-frontmatter-parser` 통과 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 규칙 매칭 결정론 우선·LLM fallback도 confidence 결정론 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 + Q13-D-2 (c) 옵션 명시 |
| #4 저자 작가성 | confidence < 0.7 저자 묶음 강제 (자동 결정 차단) |
| #7 결정론 환원 | confidence 점수 산출 100% 결정론·LLM은 의미 평가만 |

### 5. Verification (명세 §7)

- type 추측 정확도 85%+ (규칙 4 분기 + LLM fallback)
- confidence < 0.7 시 저자 묶음 100% 강제 (자동 결정 0건)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-absorb-subs.md` §SUB 2
부모 마스터 SPEC: `specs/bookwriting-absorb-master.md` §7 Step 3 + §12 Guards (confidence < 0.7 묶음) + §13 페르소나 2
저자 옵션: Q13-D-2 (c) 자동 추측
