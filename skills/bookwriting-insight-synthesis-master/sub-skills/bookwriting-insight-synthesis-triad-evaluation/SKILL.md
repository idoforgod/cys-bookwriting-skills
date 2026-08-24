---
name: bookwriting-insight-synthesis-triad-evaluation
description: 부모 bookwriting-insight-synthesis-master의 INTERNAL sub. 저자 진북 *3 기준* (의미 0.35 + 영향력 0.35 + 놀라움 0.30) 통합 평가 + 종합 점수 ≥ 2.7 시 ★ 추천 자동 부여. meaning·impact·surprise sub-skill 3개 산출을 wrapper로 통합. book-config의 surprise_weight 정합.
when_to_use: bookwriting-insight-synthesis-master에서 meaning·impact·surprise 3 sub 통과 후 자동 호출. candidate-generation 다음 단계. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-insight-synthesis-triad-evaluation

## TLDR

부모 bookwriting-insight-synthesis-master의 저자 진북 *3 기준* wrapper sub. meaning·impact·surprise 3 sub-skill 산출을 결정론 통합하여 종합 점수 (0.35·meaning + 0.35·impact + 0.30·surprise)를 산출하고 ≥ 2.7 후보에 ★ 추천을 자동 부여한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- meaning-evaluation + impact-evaluation + surprise-evaluation 3 sub 통과 후 자동
- `/bookwriting-insight-synthesis evaluate <insight-id>` 모드는 본 sub 단독

## Detailed Methodology

### 1. 결정론 chain — 가중합 + ★ 추천 임계

```python
from dataclasses import dataclass

@dataclass
class TriadScore:
    insight_id: str
    meaning_score: float        # 0-1 (Meaning Synthesizer 산출)
    impact_score: float          # 0-1 (Impact Assessor)
    surprise_score: float        # 0-1 (Surprise Hunter)
    weighted_score: float        # 0.35·meaning + 0.35·impact + 0.30·surprise (0-1)
    total_score: float           # weighted × 3 (0-3 범위 — 저자 진북 양식)
    is_recommended: bool         # ★ 추천 (total ≥ 2.7)

# 저자 진북 가중치 (book-config·부모 §10)
WEIGHT_MEANING = 0.35
WEIGHT_IMPACT = 0.35
WEIGHT_SURPRISE = 0.30
RECOMMEND_THRESHOLD = 2.7    # 명세 SUB 2 — 종합 ≥ 2.7 ★ 추천

def evaluate_triad(
    candidates: list,
    meaning_scores: dict,    # insight_id → 0-1
    impact_scores: dict,
    surprise_scores: dict,
) -> list[TriadScore]:
    """3 기준 통합 평가 + ★ 추천 자동 부여."""
    results: list[TriadScore] = []

    # Step 1: 후보 풀 로드 (candidates)
    for c in candidates:
        # Step 2-4: 각 sub-skill 산출 점수 통합
        m = meaning_scores.get(c.insight_id, 0.0)
        i = impact_scores.get(c.insight_id, 0.0)
        s = surprise_scores.get(c.insight_id, 0.0)

        # Step 5: 종합 점수 계산
        weighted = WEIGHT_MEANING * m + WEIGHT_IMPACT * i + WEIGHT_SURPRISE * s
        total = m + i + s   # 0-3 양식 (저자 진북 ≥ 2.7)

        results.append(TriadScore(
            insight_id=c.insight_id,
            meaning_score=m,
            impact_score=i,
            surprise_score=s,
            weighted_score=weighted,
            total_score=total,
            is_recommended=(total >= RECOMMEND_THRESHOLD),
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-insight-synthesis-subs.md SUB 2)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 후보 풀 로드 | `candidates` 입력 |
| Step 2: meaning-evaluation 페르소나 통합 | `meaning_scores` dict 입력 |
| Step 3: impact-evaluation 페르소나 통합 | `impact_scores` dict 입력 |
| Step 4: surprise-evaluation 페르소나 통합 | `surprise_scores` dict 입력 |
| Step 5: 종합 점수 + ≥ 2.7 ★ 추천 자동 | `total >= RECOMMEND_THRESHOLD` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | candidates + 3 score dicts (meaning·impact·surprise) |
| Output | List[TriadScore] — insight_id·3 scores·weighted·total·is_recommended |
| 후속 sub | `bookwriting-insight-synthesis-voice-craft` (★ 추천 통찰만) |
| Dependencies | meaning·impact·surprise 3 sub 통과 |
| 결정론 모듈 | 가중합 dict lookup |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 가중합 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 + 가중치 0.35·0.35·0.30 부모 §10 |
| #4 저자 작가성 | 저자 진북 *의미·영향력·놀라움* 동시 평가 — 저자 본업 평가 양식 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- 모든 후보 평가 (meaning 평균 0.72 / impact 0.61 / surprise 0.55 — 부모 §17 기준)
- ★ 추천 자동 부여 (종합 ≥ 2.7 → 3개 정도)
- 점수 0-1 범위 100%
- 부모 §15 G3 게이트 — 모든 후보의 3 점수 계산 완료

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-insight-synthesis-subs.md` §SUB 2
부모 마스터 SPEC: `specs/bookwriting-insight-synthesis-master.md` §10 (가중치) + §13 페르소나 5·6 + §15 G3 + book-config surprise_weight (기본 0.30)
저자 진북: 부모 §2 (의미·영향력·놀라움 3 기준)
