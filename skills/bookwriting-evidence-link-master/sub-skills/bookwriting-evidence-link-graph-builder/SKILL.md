---
name: bookwriting-evidence-link-graph-builder
description: 부모 bookwriting-evidence-link-master의 INTERNAL sub. ④ evidence-collect 산출 evidence-track.yaml의 각 evidence를 결정론 그래프 노드로 변환 + 노드 ID (N-NNN) 발급 + source·grade·timestamp meta 부여. pure Python dict 그래프 (networkx 의존 없음).
when_to_use: bookwriting-evidence-link-master Step 2 (Graph Builder 페르소나)에서 자동 호출. ④ evidence-collect 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-evidence-link-graph-builder

## TLDR

부모 bookwriting-evidence-link-master의 ① 진입 sub. ④ evidence-collect의 evidence-track.yaml을 로드하여 각 evidence를 결정론 그래프 노드로 변환한다. 노드 ID (N-NNN) 발급 + meta (source·grade·timestamp·quant_anchors·verification_signals) 부여. pure Python dict 그래프.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- ④ evidence-collect 통과 후 → Step 2 자동
- `/bookwriting-evidence-link graph <target>` 모드는 본 sub 진입

## Detailed Methodology

### 1. 결정론 chain — pure Python dict 그래프 노드

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class GraphNode:
    node_id: str            # N-NNN
    evidence_id: str
    source_file: str
    grade: str              # "A"|"B"|"C"|"D"|"E"
    author: str | None
    timestamp: str | None   # ISO date
    quant_anchors: list[str] = field(default_factory=list)
    verification_signals: list[str] = field(default_factory=list)
    chapter_id: str | None = None

def build_evidence_graph(evidence_track_path: Path) -> list[GraphNode]:
    """evidence-track.yaml → 결정론 노드 풀."""
    with evidence_track_path.open(encoding="utf-8") as f:
        track = yaml.safe_load(f) or {}

    nodes: list[GraphNode] = []
    counter = 0

    # Step 1: ④ evidence-track의 evidence 항목 순회
    for ev in track.get("evidence", []):
        counter += 1

        # Step 2: 노드 ID 발급 (N-NNN)
        node_id = f"N-{counter:03d}"

        # Step 3: source·grade·timestamp meta 부여
        nodes.append(GraphNode(
            node_id=node_id,
            evidence_id=ev.get("id", ""),
            source_file=ev.get("source_file", ""),
            grade=ev.get("grade", "C"),
            author=ev.get("author"),
            timestamp=ev.get("date") or ev.get("timestamp"),
            quant_anchors=ev.get("quant_anchors", []),
            verification_signals=ev.get("verification_signals", []),
            chapter_id=track.get("chapter_id"),
        ))

    return nodes
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-link-subs.md SUB 1)

| 명세 Step | 본 sub 구현 |
|---|---|
| ④ evidence-track의 evidence를 노드로 변환 | `for ev in track.get("evidence", [])` |
| source·grade·timestamp meta 부여 | GraphNode 8 필드 |
| 노드 ID 발급 | `f"N-{counter:03d}"` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | evidence_track_path (Path) — chapters/<ch>/evidence-track.yaml |
| Output | List[GraphNode] — node_id·evidence_id·source·grade·meta |
| 후속 sub | `bookwriting-evidence-link-edge-detector` |
| Dependencies | ④ evidence-collect 통과 (evidence-track.yaml 존재) |
| 결정론 모듈 | yaml.safe_load + dataclass |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | yaml.safe_load 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 항목 1:1 환원 |
| #3 출처 명시 | source_file·author·timestamp 필수 meta |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 모든 evidence 노드 변환 (100%)
- meta 완전성 (source·grade·timestamp 3 필드 강제)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-link-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-evidence-link-master.md` §7 Step 2 + §13 페르소나 1 + 부록 결정론 (pure Python dict 그래프)
영속 자산 보호: PHASE3B_HANDOFF §8 (evidence-track yaml read-only, write는 부모 위임)
