---
name: bookwriting-insight-synthesis-surprise-evaluation
description: 부모 bookwriting-insight-synthesis-master의 INTERNAL sub ⭐ 저자 진북 *깜짝놀랄만한* 단면 선택 핵심. Surprise Hunter 페르소나. 통찰 놀라움 점수 0-1 결정론 평가 — 4 유형 (통념 깨기·프레임 전복·수렴의 놀라움·역사 평행 놀라움) 분류 + 저자 시그니처 패턴 활용 기회 식별.
when_to_use: bookwriting-insight-synthesis-master에서 candidate-generation 통과 후 triad-evaluation 전에 자동 호출. 부모 §13 페르소나 4 ⭐. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-insight-synthesis-surprise-evaluation

## TLDR

부모 bookwriting-insight-synthesis-master의 ⭐ Surprise Hunter sub. 저자 진북 *깜짝놀랄만한 미래의 단면 선택* 핵심. 통찰의 놀라움을 4 유형 (통념 깨기·프레임 전복·수렴의 놀라움·역사 평행)으로 결정론 분류하고 0-1 점수화한다. 저자 시그니처 패턴 활용 기회 식별.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- candidate-generation 통과 후 자동
- triad-evaluation의 입력으로 surprise_score 제공
- C5 Surprise Priority 모드 (`--surprise-weight 0.5`) 시 가중치 증가

## Detailed Methodology

### 1. 결정론 chain — 4 놀라움 유형 분류

```python
import re
from enum import Enum
from dataclasses import dataclass, field

class SurpriseType(str, Enum):
    CONVENTION_BREAK = "convention_break"      # 통념 깨기 (AGI는 도구가 아니라 메타도구)
    FRAME_FLIP = "frame_flip"                  # 프레임 전복 (셋 중 하나가 아니라 공진화)
    CONVERGENCE = "convergence"                # 수렴의 놀라움 (두 창업자 같은 100배)
    HISTORICAL_PARALLEL = "historical_parallel"   # 역사 평행 (1930s 대공황 패턴 재현)

@dataclass
class SurpriseScore:
    insight_id: str
    text: str
    detected_types: list[SurpriseType] = field(default_factory=list)
    surprise_score: float = 0.0
    signature_opportunities: list[str] = field(default_factory=list)

# 4 놀라움 유형 패턴
PATTERN_CONVENTION = re.compile(r"(?:가 아니라|이 아니라|만이 아닌|뿐만 아닌|단순한.+?이 아닌)")
PATTERN_FRAME_FLIP = re.compile(r"(?:셋 중 하나|둘 중 하나)\s*(?:가 아니|이 아니)|공진화")
PATTERN_CONVERGENCE = re.compile(r"(?:두|세|네)\s*(?:창업자|학자|기관)[^.]*(?:정확히|똑같이|같은)")
PATTERN_HIST_PARALLEL = re.compile(r"(\d{4}|\d{2,3}0\s*년대)\s*(?:대공황|혁명|전쟁|위기|패턴)")

# 저자 시그니처 패턴 (voice-craft sub와 양식 정합)
SIGNATURE_PATTERNS = {
    "X_NOT_Y": "X가 아니라 Y",
    "NOT_ONE_OF_THREE": "셋 중 하나가 아니다",
    "DISTANCE_X_Y": "X와 Y 사이 거리",
    "TWO_FOUNDERS": "두 창업자 N배",
    "VARIABLE_X_BRANCHES": "변수 X 따라 결과 갈리는",
}

def evaluate_surprise(candidates: list) -> list[SurpriseScore]:
    """4 놀라움 유형 + 저자 시그니처 기회 결정론 식별."""
    results: list[SurpriseScore] = []

    for c in candidates:
        text = c.text
        detected: list[SurpriseType] = []
        sig_ops: list[str] = []

        # Step 1: 통찰 후보를 *독자 예상* vs *실제 명제* 차이 평가
        # Step 2: 놀라움 유형 분류
        if PATTERN_CONVENTION.search(text):
            detected.append(SurpriseType.CONVENTION_BREAK)
            sig_ops.append(SIGNATURE_PATTERNS["X_NOT_Y"])
        if PATTERN_FRAME_FLIP.search(text):
            detected.append(SurpriseType.FRAME_FLIP)
            sig_ops.append(SIGNATURE_PATTERNS["NOT_ONE_OF_THREE"])
        if PATTERN_CONVERGENCE.search(text):
            detected.append(SurpriseType.CONVERGENCE)
            sig_ops.append(SIGNATURE_PATTERNS["TWO_FOUNDERS"])
        if PATTERN_HIST_PARALLEL.search(text):
            detected.append(SurpriseType.HISTORICAL_PARALLEL)

        # Step 3: surprise_score 0-1 정규화
        # 유형 1개 = 0.4 / 2개 = 0.7 / 3개 = 0.9 / 4개 = 1.0
        type_count = len(detected)
        if type_count == 0:
            score = 0.0
        elif type_count == 1:
            score = 0.4
        elif type_count == 2:
            score = 0.7
        elif type_count == 3:
            score = 0.9
        else:
            score = 1.0

        # Step 4: 저자 시그니처 패턴 활용 기회 표시 (voice-craft sub와 cross-reference)
        results.append(SurpriseScore(
            insight_id=c.insight_id,
            text=text,
            detected_types=detected,
            surprise_score=score,
            signature_opportunities=sig_ops,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-insight-synthesis-subs.md SUB 7) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: *독자 예상* vs *실제 명제* 차이 평가 | 4 패턴 매칭 |
| Step 2 통념 깨기 ("AGI는 도구가 아니라 메타도구") | `PATTERN_CONVENTION` |
| Step 2 프레임 전복 ("셋 중 하나가 아니라 공진화") | `PATTERN_FRAME_FLIP` |
| Step 2 수렴의 놀라움 ("두 창업자가 같은 100배") | `PATTERN_CONVERGENCE` |
| Step 2 역사 평행 ("1930년대 대공황 패턴 재현") | `PATTERN_HIST_PARALLEL` |
| Step 3: surprise_score 0-1 정규화 | type_count 분기 0.0~1.0 |
| Step 4: 저자 시그니처 패턴 활용 기회 표시 | `signature_opportunities` (voice-craft cross-reference) |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | candidates (InsightCandidate) |
| Output | List[SurpriseScore] — insight_id·detected_types·surprise_score·signature_opportunities |
| 후속 sub | `triad-evaluation` (surprise_score 입력) + `voice-craft` (signature_opportunities cross-reference) |
| Dependencies | candidate-generation 통과 |
| 결정론 모듈 | 자체 정규식 4 패턴 + type_count 분기 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 정규식 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 4 Step + 4 유형 + 저자 인용 1:1 환원 |
| #4 저자 작가성 ⭐ | 저자 진북 *깜짝놀랄만한 미래의 단면 선택* 핵심 (부모 §13 페르소나 4) |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- surprise_score 0-1 범위 (type_count 분기 결정론)
- 놀라움 유형 명확 (4 enum)
- 시그니처 활용 기회 식별 (voice-craft sub와 cross-reference)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-insight-synthesis-subs.md` §SUB 7 ⭐
부모 마스터 SPEC: `specs/bookwriting-insight-synthesis-master.md` §13 페르소나 4 Surprise Hunter ⭐ (저자 진북 핵심) + §14 C5 Surprise Priority + 부록 A 저자 진북 인용
저자 진북: *"깜짝놀랄만한 미래의 단면을 선택하여 매력적인 글로 쓰는 방식이 핵심이다"*
voice-craft cross-reference: signature_opportunities → `bookwriting-insight-synthesis-voice-craft` M8 호출
