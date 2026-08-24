---
name: bookwriting-cross-chapter-relink-cross-ref-suggester
description: 부모 bookwriting-cross-chapter-relink-master의 INTERNAL sub. 시드의 secondary 챕터 매핑 후보 결정론 발견 — 각 시드의 다른 챕터 관련성 평가 + M6 BM25 confidence 점수 + cross_reference 추가 후보 제시.
when_to_use: bookwriting-cross-chapter-relink-master에서 conflict-detector 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-cross-chapter-relink-cross-ref-suggester

## TLDR

부모 bookwriting-cross-chapter-relink-master의 cross-reference 발견 sub. 각 시드의 primary 챕터 외 다른 챕터와의 관련성을 M6 BM25로 결정론 평가하고 cross_reference 추가 후보를 제시한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- conflict-detector 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — secondary 챕터 매핑

```python
from dataclasses import dataclass, field

@dataclass
class CrossRefCandidate:
    seed_id: str
    primary_chapter: str
    suggested_secondary_chapters: list[tuple[str, float]]   # (chapter, confidence)

def suggest_cross_references(graph, min_confidence: float = 0.5) -> list[CrossRefCandidate]:
    """secondary 챕터 매핑 후보 결정론 발견."""
    # 시드 단위로 그룹화
    seed_nodes = [n for n in graph.nodes if n.item_type == "seed"]
    nodes_by_id = {n.item_id: n for n in graph.nodes}

    results: list[CrossRefCandidate] = []
    for seed in seed_nodes:
        # 시드와 연결된 모든 cross-chapter edge 수집
        related_chapters: dict[str, float] = {}
        for edge in graph.edges:
            if edge.node_a == seed.item_id:
                other = nodes_by_id.get(edge.node_b)
            elif edge.node_b == seed.item_id:
                other = nodes_by_id.get(edge.node_a)
            else:
                continue
            if not other or other.chapter_id == seed.chapter_id:
                continue
            # 챕터별 최고 relevance 유지
            existing = related_chapters.get(other.chapter_id, 0.0)
            if edge.relevance > existing:
                related_chapters[other.chapter_id] = edge.relevance

        # confidence >= min_confidence 챕터만 후보로
        suggestions = sorted(
            [(ch, conf) for ch, conf in related_chapters.items() if conf >= min_confidence],
            key=lambda x: x[1],
            reverse=True,
        )

        if suggestions:
            results.append(CrossRefCandidate(
                seed_id=seed.item_id,
                primary_chapter=seed.chapter_id,
                suggested_secondary_chapters=suggestions,
            ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-cross-chapter-relink-subs.md SUB 3)

| 명세 항목 | 본 sub 구현 |
|---|---|
| 각 시드의 *다른 챕터 관련성* 평가 | `for seed in seed_nodes` + edge iteration |
| confidence 점수 | `edge.relevance` (M6 BM25) |
| cross_reference 추가 후보 제시 | `suggested_secondary_chapters` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | graph (cross-checker 산출) + min_confidence |
| Output | List[CrossRefCandidate] — primary + suggested_secondary 목록 |
| 후속 sub | reroute-recommender |
| Dependencies | conflict-detector 통과 |
| 결정론 모듈 | 자체 dict 집계 + 정렬 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M6 + dict 결정론 |
| #2 grill-me 원문 일치 | 명세 3 항목 1:1 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- cross-ref 후보 정확도 75%+

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-cross-chapter-relink-subs.md` §SUB 3
부모 마스터 SPEC: `specs/bookwriting-cross-chapter-relink-master.md`
M6 BM25 정합: cross-checker가 산출한 edge.relevance 활용
