---
name: bookwriting-cross-chapter-relink-cross-checker
description: 부모 bookwriting-cross-chapter-relink-master의 INTERNAL sub. 모든 챕터의 seed-track·evidence-track 결정론 로드 + N×N 비교 + 시드·근거 중복 검출 + 시드 cross-chapter 풀 구축 + M6 BM25 relevance 점수.
when_to_use: bookwriting-cross-chapter-relink-master cycle 진입 시 자동 첫 단계.
disable-model-invocation: true
---

# bookwriting-cross-chapter-relink-cross-checker

## TLDR

부모 bookwriting-cross-chapter-relink-master의 ① 진입 sub. 모든 챕터의 seed/evidence 트랙을 결정론 로드하여 N×N 비교로 cross-chapter 그래프를 구축하고 시드·근거 중복을 검출한다. M6 BM25 relevance 활용.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- ⑪ cross-chapter-relink cycle 진입 시 자동 첫 단계

## Detailed Methodology

### 1. 결정론 chain — N×N + M6 BM25

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from relevance_scorer import RelevanceScorer   # M6 BM25

@dataclass
class CrossChapterNode:
    item_id: str             # S-NNN | F-NNN | INS-NNN
    chapter_id: str
    item_type: str           # "seed" | "evidence" | "insight"
    text: str

@dataclass
class CrossChapterEdge:
    node_a: str
    node_b: str
    relevance: float
    edge_type: str           # "duplicate" | "related"

@dataclass
class CrossChapterGraph:
    nodes: list[CrossChapterNode]
    edges: list[CrossChapterEdge]
    duplicates: list[tuple[str, str]]    # 중복 페어

def build_cross_chapter_graph(
    chapters_dir: Path,
    min_relevance: float = 0.7,
) -> CrossChapterGraph:
    """모든 챕터 N×N 결정론 비교 + 그래프 구축."""
    scorer = RelevanceScorer()
    nodes: list[CrossChapterNode] = []

    # Step 1: 모든 챕터의 seed-track·evidence-track 로드
    for chapter_dir in chapters_dir.iterdir():
        if not chapter_dir.is_dir():
            continue
        chapter_id = chapter_dir.name

        seed_track = chapter_dir / "seed-track.yaml"
        if seed_track.exists():
            with seed_track.open(encoding="utf-8") as f:
                track = yaml.safe_load(f) or {}
            for seed in track.get("seeds", []):
                nodes.append(CrossChapterNode(
                    item_id=seed.get("id", ""),
                    chapter_id=chapter_id,
                    item_type="seed",
                    text=seed.get("text", ""),
                ))

        evidence_track = chapter_dir / "evidence-track.yaml"
        if evidence_track.exists():
            with evidence_track.open(encoding="utf-8") as f:
                track = yaml.safe_load(f) or {}
            for ev in track.get("evidence", []):
                nodes.append(CrossChapterNode(
                    item_id=ev.get("id", ev.get("source_file", "")),
                    chapter_id=chapter_id,
                    item_type="evidence",
                    text=ev.get("excerpt", "") or ev.get("text", ""),
                ))

    # Step 2: N×N 비교
    edges: list[CrossChapterEdge] = []
    duplicates: list[tuple[str, str]] = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            n1, n2 = nodes[i], nodes[j]
            if n1.chapter_id == n2.chapter_id:
                continue   # 같은 챕터는 cross-chapter 아님
            score = scorer.score(n1.text, n2.text.split())
            if score >= min_relevance:
                edge_type = "duplicate" if score >= 0.9 else "related"
                edges.append(CrossChapterEdge(
                    node_a=n1.item_id,
                    node_b=n2.item_id,
                    relevance=score,
                    edge_type=edge_type,
                ))
                if edge_type == "duplicate":
                    duplicates.append((n1.item_id, n2.item_id))

    return CrossChapterGraph(nodes=nodes, edges=edges, duplicates=duplicates)
```

### 2. 명세 §출처 (SPEC: bookwriting-cross-chapter-relink-subs.md SUB 1)

| 명세 항목 | 본 sub 구현 |
|---|---|
| 모든 챕터의 seed-track·evidence-track 로드 | `for chapter_dir in chapters_dir.iterdir()` + yaml.safe_load |
| N×N 비교 | `for i in range(...): for j in range(i+1, ...)` |
| 시드·근거 중복 검출 | `score >= 0.9 → "duplicate"` |
| 시드 cross-chapter 풀 구축 | `CrossChapterGraph` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapters_dir (모든 챕터) + min_relevance |
| Output | CrossChapterGraph — nodes·edges·duplicates |
| 후속 sub | conflict-detector + cross-ref-suggester |
| Dependencies | 모든 챕터의 seed-track·evidence-track 존재 |
| 결정론 모듈 | M6 RelevanceScorer + yaml.safe_load |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M6 + yaml 결정론 |
| #2 grill-me 원문 일치 | 명세 항목 1:1 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 중복·연결 정확도 80%+ (M6 BM25 임계 정합)
- 그래프 정합 (`nodes`·`edges` 정합)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-cross-chapter-relink-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-cross-chapter-relink-master.md`
결정론 모듈: `lib/relevance_scorer.py` (M6 BM25)
영속 자산 보호: PHASE3B_HANDOFF §8 (chapter tracks read-only)
