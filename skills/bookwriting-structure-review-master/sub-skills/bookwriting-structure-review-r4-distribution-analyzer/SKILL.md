---
name: bookwriting-structure-review-r4-distribution-analyzer
description: "부모 bookwriting-structure-review-master의 INTERNAL sub. chapters/<ch>/evidence-track.yaml 권위 등급 분포 결정론 분석 + Layer 1-5 카운트 + 어느 한 층 *과편중* 검출 (예: Layer 1만 80%) + 저자 R4 권장 (다층 균형). M3 AuthorityGrader 정합."
when_to_use: bookwriting-structure-review-master에서 flow-validator 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-structure-review-r4-distribution-analyzer

## TLDR

부모 bookwriting-structure-review-master의 권위 분포 sub. evidence-track.yaml의 Layer 1-5 (Grade A-E) 카운트를 결정론 집계하고 한 층 *과편중 50%+* 검출 시 저자 R4 다층 균형 권장한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- flow-validator 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — 권위 분포 집계 + 편중 검출

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field

OVERWEIGHT_THRESHOLD = 0.5   # 50%+ 시 편중

@dataclass
class AuthorityDistribution:
    chapter_id: str
    total_evidence: int
    layer_counts: dict[str, int]    # {"A": N, "B": N, ...}
    layer_ratios: dict[str, float]
    overweighted_layer: str | None  # "A" 등 과편중 층
    needs_balance_recommendation: bool

def analyze_r4_distribution(chapter_id: str, evidence_track_path: Path) -> AuthorityDistribution:
    """권위 5층 분포 결정론 분석 + 편중 검출."""
    # Step 1: chapters/<ch>/evidence-track.yaml 로드
    if not evidence_track_path.exists():
        return AuthorityDistribution(
            chapter_id=chapter_id,
            total_evidence=0,
            layer_counts={},
            layer_ratios={},
            overweighted_layer=None,
            needs_balance_recommendation=False,
        )

    with evidence_track_path.open(encoding="utf-8") as f:
        track = yaml.safe_load(f) or {}

    # Step 2: Layer 1-5 카운트 (Grade A·B·C·D·E)
    counts: dict[str, int] = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    for ev in track.get("evidence", []):
        grade = ev.get("grade", "C")
        if grade in counts:
            counts[grade] += 1

    total = sum(counts.values())
    ratios = {g: (c / total if total > 0 else 0.0) for g, c in counts.items()}

    # Step 3: 어느 한 층 *과편중* 검출
    overweighted = None
    for grade, ratio in ratios.items():
        if ratio >= OVERWEIGHT_THRESHOLD:
            overweighted = grade
            break

    # Step 4: 저자 R4 권장 (다층 균형)
    return AuthorityDistribution(
        chapter_id=chapter_id,
        total_evidence=total,
        layer_counts=counts,
        layer_ratios=ratios,
        overweighted_layer=overweighted,
        needs_balance_recommendation=overweighted is not None,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-structure-review-subs.md SUB 5)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: chapters/<ch>/evidence-track.yaml 권위 등급 분포 분석 | `yaml.safe_load(evidence_track_path)` |
| Step 2: Layer 1-5 카운트 | `counts` dict (A·B·C·D·E) |
| Step 3: 어느 한 층 *과편중* 검출 (예: Layer 1만 80%) | `OVERWEIGHT_THRESHOLD = 0.5` |
| Step 4: 저자 R4 권장 (다층 균형) | `needs_balance_recommendation` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + evidence_track_path |
| Output | AuthorityDistribution — counts·ratios·overweighted·recommendation |
| 후속 sub | r5-verifier + resize-recommender |
| Dependencies | flow-validator 통과 + ④ evidence-collect의 권위 등급화 |
| 결정론 모듈 | yaml.safe_load + dict 집계 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | yaml + dict 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 |
| #3 출처 명시 | 권위 등급 분포 정확 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 분포 측정 정합 (`layer_counts` 합 = total)
- 편중 알림 정확 (`overweighted_layer` 50%+ 시 트리거)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-structure-review-subs.md` §SUB 5
부모 마스터 SPEC: `specs/bookwriting-structure-review-master.md`
④ evidence-collect-authority-grader 정합: Grade A-E 5층 매핑
