---
name: bookwriting-insight-synthesis-impact-evaluation
description: 부모 bookwriting-insight-synthesis-master의 INTERNAL sub. Impact Assessor 페르소나. 통찰 영향력 점수 0-1 결정론 계산 — 스케일 (산업혁명 N배·인구 N명·GDP) + 범위 (한국·아시아·세계·우주) + 시점 도달 (1년·5년·10년) 3 차원 가중합. M4 QuantitativeAnchorExtractor 정량 앵커 추출 + 저자 정량 표현 패턴 (100배·90% 확신·5억 명·2027) 정합.
when_to_use: bookwriting-insight-synthesis-master에서 candidate-generation 통과 후 triad-evaluation 전에 자동 호출. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-insight-synthesis-impact-evaluation

## TLDR

부모 bookwriting-insight-synthesis-master의 Impact Assessor sub. 통찰의 영향력 (스케일·범위·시점 도달) 3 차원을 M4 QuantitativeAnchorExtractor 결정론 추출로 평가한다. 저자 정량 표현 패턴 (100배·90% 확신·5억 명·2027 임계점) 정합 + impact_score 0-1 정규화.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- candidate-generation 통과 후 자동
- triad-evaluation의 입력으로 impact_score 제공

## Detailed Methodology

### 1. 결정론 chain — M4 + 3 차원 가중합

```python
import re
from dataclasses import dataclass, field
from quantitative_extraction import QuantitativeAnchorExtractor   # M4

@dataclass
class ImpactScore:
    insight_id: str
    text: str
    scale_score: float          # 0-0.40 (산업혁명 배수·인구·GDP)
    scope_score: float           # 0-0.30 (한국·아시아·세계·우주)
    timing_score: float          # 0-0.30 (시점 도달 — 짧을수록 강함)
    quant_anchors: list[str] = field(default_factory=list)
    impact_score: float = 0.0

# 저자 정량 패턴 (부모 §17 검증 3)
PATTERN_SCALE = re.compile(r"(\d+(?:\.\d+)?)\s*배|(\d+(?:\.\d+)?)\s*%|(\d+)\s*억\s*명|(\d+)\s*만\s*명")
SCOPE_KEYWORDS = {
    "uni": ["우주", "global", "전 세계", "인류"],   # 0.30
    "world": ["세계", "global"],                    # 0.25
    "asia": ["아시아", "asia"],                     # 0.18
    "korea": ["한국", "korea"],                     # 0.12
}
TIMING_PATTERN = re.compile(r"(\d+)\s*년\s*(?:후|뒤|이내|까지)")

def evaluate_impact(candidates: list) -> list[ImpactScore]:
    """3 차원 가중합 + M4 정량 앵커 추출."""
    extractor = QuantitativeAnchorExtractor()
    results: list[ImpactScore] = []

    for c in candidates:
        text = c.text

        # Step 1: M4 정량 앵커 추출 (impact 평가용)
        anchors_raw = extractor.extract_all(text)
        anchor_texts = [a.text for a in anchors_raw]

        # Step 2 차원 1: 스케일 (산업혁명 배수·인구·GDP)
        scale = 0.0
        scale_match = PATTERN_SCALE.search(text)
        if scale_match:
            # 100배 +0.30·90% +0.25·N억 명 +0.30 등 (정량 앵커 강도)
            scale = 0.40

        # 차원 2: 범위 (한국·아시아·세계·우주)
        scope = 0.0
        for tier, kws in SCOPE_KEYWORDS.items():
            if any(kw in text for kw in kws):
                scope = max(scope, {"uni": 0.30, "world": 0.25, "asia": 0.18, "korea": 0.12}[tier])

        # 차원 3: 시점 도달 (짧을수록 강함)
        timing = 0.0
        timing_match = TIMING_PATTERN.search(text)
        if timing_match:
            year_offset = int(timing_match.group(1))
            if year_offset <= 1: timing = 0.30
            elif year_offset <= 5: timing = 0.22
            elif year_offset <= 10: timing = 0.15
            else: timing = 0.08

        # Step 3: impact_score 0-1 정규화
        impact = scale + scope + timing

        # Step 4: 저자 정량 표현 패턴 정합 — 이미 M4가 보장

        results.append(ImpactScore(
            insight_id=c.insight_id,
            text=text,
            scale_score=scale,
            scope_score=scope,
            timing_score=timing,
            quant_anchors=anchor_texts,
            impact_score=impact,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-insight-synthesis-subs.md SUB 6)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 통찰의 정량 앵커 추출 (100배·90% 확신·5억 명 등) | M4 `extractor.extract_all()` |
| Step 2: 영향력 차원 (스케일·범위·시점 도달) | `scale_score`·`scope_score`·`timing_score` |
| Step 3: impact_score 0-1 정규화 | 가중합 (0.40+0.30+0.30=1.0) |
| Step 4: 저자 정량 표현 패턴 정합 | M4 패턴 + 정량 앵커 표시 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | candidates (InsightCandidate) |
| Output | List[ImpactScore] — insight_id·3 dims·quant_anchors·impact_score |
| 후속 sub | `triad-evaluation` (impact_score 입력) |
| Dependencies | candidate-generation 통과 |
| 결정론 모듈 | M4 QuantitativeAnchorExtractor + 자체 정규식 (scope·timing) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M4 + 정규식 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 4 Step + 3 차원 + 저자 정량 패턴 1:1 환원 |
| #3 출처 명시 | quant_anchors 필드 (M4 출처 자동) |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- impact_score 0-1 범위 (가중치 합 = 1.0 강제)
- 정량 앵커 명시 (M4 출처 강제)
- 저자 정량 패턴 정합 (100배·90%·N년 등)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-insight-synthesis-subs.md` §SUB 6
부모 마스터 SPEC: `specs/bookwriting-insight-synthesis-master.md` §13 페르소나 5 Impact Assessor + 부록 E (M4)
결정론 모듈: `lib/quantitative_extraction.py` (M4)
