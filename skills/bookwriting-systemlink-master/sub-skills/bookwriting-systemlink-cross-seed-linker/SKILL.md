---
name: bookwriting-systemlink-cross-seed-linker
description: 부모 bookwriting-systemlink-master의 INTERNAL sub. 시드 N×N 의미·논리 연결 평가 + relation_type (extends·contrasts·examples·depends_on·pairs_with) 결정론 매핑 + seed-registry linked_seeds 갱신. M6 BM25 의미 유사도 + 부모 마스터 LLM 의미 평가 위임 (confidence 점수 결정론).
when_to_use: bookwriting-systemlink-master Step 4 (Cross-Seed Linker 페르소나)에서 자동 호출. Asset Linker 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-systemlink-cross-seed-linker

## TLDR

부모 bookwriting-systemlink-master의 시드 간 연결 sub. 모든 시드 N×N으로 비교하여 5 relation_type (extends·contrasts·examples·depends_on·pairs_with)을 결정론 매핑한다. M6 BM25 의미 유사도 + 정규식 패턴으로 1차 판별 + 모호 시 부모 마스터의 LLM 의미 평가에 위임 (confidence 점수는 결정론).

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Asset Linker 통과 후 → Step 4 자동

## Detailed Methodology

### 1. 결정론 chain — N×N relation_type 매핑

```python
import re
from enum import Enum
from dataclasses import dataclass
from relevance_scorer import RelevanceScorer   # M6 BM25

class RelationType(str, Enum):
    EXTENDS = "extends"          # A → B (B가 A 확장)
    CONTRASTS = "contrasts"      # A vs B (대비)
    EXAMPLES = "examples"        # A의 예시 B
    DEPENDS_ON = "depends_on"    # B는 A에 의존
    PAIRS_WITH = "pairs_with"    # A·B 짝

@dataclass
class SeedRelation:
    seed_a_id: str
    seed_b_id: str
    relation_type: RelationType
    confidence: float        # 0.0-1.0
    method: str              # "pattern" | "semantic_similarity" | "llm_eval"

# 5 relation 정규식 패턴 (결정론 1차 판별)
PATTERN_EXTENDS = re.compile(r"(확장|발전|진화|extends)")
PATTERN_CONTRASTS = re.compile(r"(대비|반대|상반|contrast|but)")
PATTERN_EXAMPLES = re.compile(r"(예시|예를 들어|일례|case|example)")
PATTERN_DEPENDS = re.compile(r"(의존|기반|전제|depends|requires)")
PATTERN_PAIRS = re.compile(r"(짝|쌍|함께|together|pair)")

def link_cross_seeds(seeds: list[dict]) -> list[SeedRelation]:
    """모든 시드 N×N 비교 + relation_type 결정론 매핑."""
    scorer = RelevanceScorer()
    relations = []

    # Step 1: 모든 시드 N×N 비교 (i < j 트라이앵글)
    for i in range(len(seeds)):
        for j in range(i + 1, len(seeds)):
            seed_a, seed_b = seeds[i], seeds[j]

            # Step 2: 의미 유사도 (M6 BM25)
            similarity = scorer.score(
                seed_a.get("text", ""),
                seed_b.get("text", "").split(),
            )
            if similarity < 0.3:
                continue   # 무관 — relation 매핑 skip

            # Step 3: relation_type 매핑 (정규식 패턴 우선)
            combined_text = seed_a.get("text", "") + " " + seed_b.get("text", "")
            rtype, confidence = _classify_relation(combined_text, similarity)

            if rtype is None:
                continue

            relations.append(SeedRelation(
                seed_a_id=seed_a["id"],
                seed_b_id=seed_b["id"],
                relation_type=rtype,
                confidence=confidence,
                method="pattern" if confidence >= 0.7 else "semantic_similarity",
            ))

    # Step 4: seed-registry linked_seeds 갱신 — 부모 마스터가 yaml write
    return relations

def _classify_relation(text: str, similarity: float) -> tuple:
    """5 relation 정규식 분기 — 첫 매치 우선."""
    for rtype, pattern in [
        (RelationType.EXTENDS, PATTERN_EXTENDS),
        (RelationType.CONTRASTS, PATTERN_CONTRASTS),
        (RelationType.EXAMPLES, PATTERN_EXAMPLES),
        (RelationType.DEPENDS_ON, PATTERN_DEPENDS),
        (RelationType.PAIRS_WITH, PATTERN_PAIRS),
    ]:
        if pattern.search(text):
            return (rtype, min(0.95, similarity + 0.2))
    # 패턴 미발견 시 default pairs_with + 낮은 confidence
    if similarity >= 0.6:
        return (RelationType.PAIRS_WITH, similarity)
    return (None, 0.0)
```

### 2. 명세 §출처 (SPEC: bookwriting-systemlink-subs.md SUB 4)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 모든 시드 N×N 비교 | `for i in range(...): for j in range(i+1, ...)` |
| Step 2: 의미 유사도·논리 연결 평가 | M6 BM25 `scorer.score()` |
| Step 3: relation_type 매핑 (5종) | `_classify_relation()` 정규식 분기 |
| Step 4: seed-registry linked_seeds 갱신 | 부모 마스터 yaml write 위임 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | seeds (list[dict]) — seed-registry 로드 |
| Output | List[SeedRelation] — seed_a_id·seed_b_id·relation_type·confidence·method |
| 후속 sub | `bookwriting-systemlink-system-loop-mapper` |
| Dependencies | Asset Linker 통과 |
| 결정론 모듈 | M6 RelevanceScorer (BM25) + 정규식 5 패턴 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M6 + 정규식 결정론 — LLM은 confidence 점수만 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 환원 + 5 relation 그대로 |
| #7 결정론 환원 | confidence 100% 결정론·LLM 의미 평가는 부모 §부록 허용 영역 |

### 5. Verification (명세 §7)

- 시드 간 관계 정확도 80%+ (부모 §10 정량 — relevance ≥ 0.7 채택률)
- relation_type 올바른 매핑 (5종 정규식 회귀)
- N×N 트라이앵글 시간복잡도 O(N²/2) — 시드 100개에 5000 비교 (실용)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-systemlink-subs.md` §SUB 4
부모 마스터 SPEC: `specs/bookwriting-systemlink-master.md` §7 Step 4 + §13 페르소나 3 + 부록 결정론 (LLM 의미 평가 허용)
결정론 모듈: `lib/relevance_scorer.py` (M6 BM25)
LLM 위임: 부모 마스터 §부록 — confidence 점수만 결정론, 의미 평가는 LLM 허용
