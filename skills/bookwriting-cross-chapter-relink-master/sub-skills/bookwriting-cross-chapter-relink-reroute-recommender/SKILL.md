---
name: bookwriting-cross-chapter-relink-reroute-recommender
description: 부모 bookwriting-cross-chapter-relink-master의 INTERNAL sub. 시드의 primary 챕터 재라우팅 권장 — 원래 primary와 실제 cross-chapter 관련성 결정론 비교 + 다른 챕터 관련성이 더 높으면 재라우팅 권장 + confidence < 0.7 저자 묶음 강제 + confidence ≥ 0.7 저자 묶음에 ★ 추천.
when_to_use: bookwriting-cross-chapter-relink-master에서 cross-ref-suggester 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-cross-chapter-relink-reroute-recommender

## TLDR

부모 bookwriting-cross-chapter-relink-master의 재라우팅 권장 sub. 시드의 원래 primary 챕터보다 다른 챕터의 cross-chapter 관련성이 더 높을 때 재라우팅을 권장한다. confidence < 0.7 시 저자 묶음 강제, ≥ 0.7 시 ★ 추천.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- cross-ref-suggester 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — primary 재평가 + confidence 분기

```python
from dataclasses import dataclass, field

@dataclass
class RerouteRecommendation:
    seed_id: str
    current_primary: str
    recommended_primary: str
    confidence: float
    is_starred: bool          # ★ 추천 (confidence ≥ 0.7)
    needs_bundle: bool        # confidence < 0.7 저자 묶음 강제
    primary_relevance: float
    new_primary_relevance: float

def recommend_reroute(
    cross_ref_candidates: list,    # cross-ref-suggester 산출
    seed_primary_relevance: dict,  # seed_id → 원래 primary 챕터 관련성
) -> list[RerouteRecommendation]:
    """primary 재라우팅 결정론 권장."""
    results: list[RerouteRecommendation] = []

    for c in cross_ref_candidates:
        # Step 1: 원래 primary 관련성 vs 다른 챕터 관련성 비교
        original_relevance = seed_primary_relevance.get(c.seed_id, 0.0)
        if not c.suggested_secondary_chapters:
            continue

        best_chapter, best_score = c.suggested_secondary_chapters[0]

        # Step 2: 다른 챕터 관련성이 더 높으면 재라우팅 권장
        if best_score <= original_relevance:
            continue

        # Step 3-4: confidence 분기
        starred = best_score >= 0.7
        needs_bundle = best_score < 0.7

        results.append(RerouteRecommendation(
            seed_id=c.seed_id,
            current_primary=c.primary_chapter,
            recommended_primary=best_chapter,
            confidence=best_score,
            is_starred=starred,
            needs_bundle=needs_bundle,
            primary_relevance=original_relevance,
            new_primary_relevance=best_score,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-cross-chapter-relink-subs.md SUB 4)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 각 시드의 *원래 primary*와 *실제 cross-chapter 관련성* 비교 | `original_relevance` vs `best_score` |
| Step 2: primary 챕터보다 *다른 챕터 관련성*이 더 높으면 재라우팅 권장 | `if best_score > original_relevance` |
| Step 3: confidence < 0.7 → 저자 묶음 강제 | `needs_bundle = True` |
| Step 4: confidence ≥ 0.7 → 저자 묶음에 ★ 추천 | `is_starred = True` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | cross_ref_candidates + seed_primary_relevance dict |
| Output | List[RerouteRecommendation] — current·recommended·confidence·★/bundle |
| 후속 sub | loop-coherence-checker |
| Dependencies | cross-ref-suggester 통과 |
| 결정론 모듈 | 자체 dict 분기 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | dict 분기 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step + confidence 0.7 분기 1:1 |
| #4 저자 작가성 | 저자 묶음·★ 추천 — 저자 결정권 보장 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 재라우팅 정확도 85%+
- confidence < 0.7 저자 묶음 강제 (`needs_bundle = True`)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-cross-chapter-relink-subs.md` §SUB 4
부모 마스터 SPEC: `specs/bookwriting-cross-chapter-relink-master.md`
