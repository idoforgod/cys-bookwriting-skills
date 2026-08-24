---
name: bookwriting-evidence-link-isolation-detector
description: 부모 bookwriting-evidence-link-master의 INTERNAL sub. 그래프 degree 0 (고립) 노드 + degree 1 (약한 연결) 노드 결정론 검출 + 저자 묶음 3 옵션 (풀 제외·연결 추가 시도·미해결 보관) escalate. 고립 노드 100% 검출 강제. 부모 §12 Isolated Node Gate cross-cutting.
when_to_use: bookwriting-evidence-link-master Step 6 (Isolation Detector 페르소나) 추가 단계에서 자동 호출. Loop Integrator 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-evidence-link-isolation-detector

## TLDR

부모 bookwriting-evidence-link-master의 고립 검출 sub. 그래프 degree 0 (고립) 노드와 degree 1 (약한 연결) 노드를 결정론 dict 카운트로 100% 검출하고 저자 묶음 3 옵션 (풀 제외·연결 추가 시도·미해결 보관)을 escalate한다. 부모 §12 Isolated Node Gate cross-cutting.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Loop Integrator 통과 후 → Isolation Detector 자동
- 부모 §16 — 고립 노드 다수 (5+) 발견 시 저자 일괄 묶음

## Detailed Methodology

### 1. 결정론 chain — degree 카운트 + 저자 묶음 3 옵션

```python
from enum import Enum
from dataclasses import dataclass, field

class IsolationOption(str, Enum):
    EXCLUDE = "exclude"               # evidence 풀에서 제외
    ADD_LINK = "add_link"             # 연결 추가 시도
    KEEP_UNRESOLVED = "keep_unresolved"   # 미해결로 보관

@dataclass
class IsolatedNode:
    node_id: str
    degree: int                       # 0 (고립) | 1 (약한 연결)
    is_isolated: bool                 # degree == 0
    is_weakly_linked: bool            # degree == 1
    bundle_options: list[IsolationOption] = field(default_factory=lambda: list(IsolationOption))

def detect_isolations(nodes: list, edges: list) -> tuple[list[IsolatedNode], dict]:
    """degree 0·degree 1 결정론 검출."""
    # Step 1: degree 카운트 (in + out)
    degree: dict[str, int] = {n.node_id: 0 for n in nodes}
    for e in edges:
        degree[e.source_node] = degree.get(e.source_node, 0) + 1
        degree[e.target_node] = degree.get(e.target_node, 0) + 1

    # Step 2: degree 0·1 노드 식별
    isolated: list[IsolatedNode] = []
    for n in nodes:
        d = degree.get(n.node_id, 0)
        if d == 0:
            # Step 3: 저자 묶음 (3 옵션 — 명세 SUB 6)
            isolated.append(IsolatedNode(
                node_id=n.node_id,
                degree=0,
                is_isolated=True,
                is_weakly_linked=False,
            ))
        elif d == 1:
            isolated.append(IsolatedNode(
                node_id=n.node_id,
                degree=1,
                is_isolated=False,
                is_weakly_linked=True,
            ))

    isolated_count = sum(1 for i in isolated if i.is_isolated)
    weak_count = sum(1 for i in isolated if i.is_weakly_linked)

    summary = {
        "total_nodes": len(nodes),
        "isolated_count": isolated_count,
        "weakly_linked_count": weak_count,
        "isolated_gate_pass": isolated_count == 0,
        "bulk_bundle_required": isolated_count >= 5,    # 부모 §16 일괄 묶음
    }
    return isolated, summary
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-link-subs.md SUB 6)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: degree 0 노드 (고립) 발견 | `if d == 0: is_isolated=True` |
| Step 2: degree 1 노드 (약한 연결) 발견 | `elif d == 1: is_weakly_linked=True` |
| Step 3: 저자 묶음 (a) evidence 풀 제외 / (b) 연결 추가 / (c) 미해결 보관 | `IsolationOption` 3 enum 자동 부착 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | nodes (Graph Builder) + edges (Edge Detector) |
| Output | (List[IsolatedNode], summary — isolated_count·gate_pass·bulk_bundle_required) |
| 후속 sub | `bookwriting-evidence-link-graph-visualizer` |
| Dependencies | Loop Integrator 통과 |
| 결정론 모듈 | 자체 dict degree 카운트 + 그래프 알고리즘 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | dict 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 3 Step + 3 옵션 1:1 환원 |
| #4 저자 작가성 | 저자 묶음 *강제* — 자동 결정 영구 금지 (Mode 2 예외만 부모 §부록) |
| #7 결정론 환원 | dict 100% 결정론 |

### 5. Verification (명세 §5)

- 고립 노드 100% 검출 (degree 0 모두 식별)
- 약한 연결 검출 (degree 1 모두 식별)
- 부모 §12 Isolated Node Gate cross-cutting 정합
- 고립 5+ 일괄 묶음 (부모 §16)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-link-subs.md` §SUB 6
부모 마스터 SPEC: `specs/bookwriting-evidence-link-master.md` §7 Step 6 (Isolation Detector 추가) + §12 Isolated Node Gate + §13 페르소나 6 + §16 (5+ 일괄 묶음)
결정론 알고리즘: pure Python dict degree 카운트
