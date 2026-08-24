---
name: bookwriting-evidence-link-edge-detector
description: 부모 bookwriting-evidence-link-master의 INTERNAL sub. 그래프 노드 간 3 엣지 타입 (논리 causal·시간 temporal·인과 causation) 결정론 자동 발견 + weight·confidence 부여 + label 명확 표기. 정규식 + 시간 비교 + 인과 키워드 매칭 결정론 (LLM 의미 검증은 부모 §부록 허용 영역).
when_to_use: bookwriting-evidence-link-master Step 3 (Edge Detector 페르소나)에서 자동 호출. Graph Builder 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-evidence-link-edge-detector

## TLDR

부모 bookwriting-evidence-link-master의 엣지 검출 sub. 그래프 노드 간 3 엣지 타입 (logical·temporal·causal)을 결정론 매칭 (정규식 + 시간 비교 + 인과 키워드)으로 발견하고 weight·confidence·label을 부여한다. LLM 의미 검증은 부모 §부록 허용 (부모 양식 1:1).

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Graph Builder 통과 후 → Step 3 자동

## Detailed Methodology

### 1. 결정론 chain — 3 엣지 타입 매칭

```python
import re
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class EdgeType(str, Enum):
    LOGICAL = "logical"       # A 주장 → B 결론
    TEMPORAL = "temporal"     # 1990 → 2024
    CAUSAL = "causal"         # 원인 → 결과

@dataclass
class Edge:
    edge_id: str
    source_node: str          # N-NNN
    target_node: str
    edge_type: EdgeType
    label: str
    weight: float             # 0-1
    confidence: float

# 인과·논리 키워드 (한국어 v1 양식)
CAUSAL_KEYWORDS = ["때문", "원인", "결과", "초래", "야기", "leads to", "causes"]
LOGICAL_KEYWORDS = ["따라서", "그러므로", "결론", "implies", "결국"]

def detect_edges(nodes: list, evidence_texts: dict) -> list[Edge]:
    """N×N 결정론 엣지 검출."""
    edges: list[Edge] = []
    counter = 0

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j:
                continue
            src, tgt = nodes[i], nodes[j]

            # Step 1: 시간 엣지 (temporal) — timestamp 비교
            edge = _detect_temporal(src, tgt)
            if edge:
                counter += 1
                edges.append(_finalize(counter, src, tgt, edge, "temporal"))
                continue

            # Step 2: 인과 엣지 (causal) — evidence 텍스트 키워드
            src_text = evidence_texts.get(src.evidence_id, "")
            tgt_text = evidence_texts.get(tgt.evidence_id, "")
            edge = _detect_causal(src_text, tgt_text)
            if edge:
                counter += 1
                edges.append(_finalize(counter, src, tgt, edge, "causal"))
                continue

            # Step 3: 논리 엣지 (logical) — implication 키워드
            edge = _detect_logical(src_text, tgt_text)
            if edge:
                counter += 1
                edges.append(_finalize(counter, src, tgt, edge, "logical"))

    return edges

def _detect_temporal(src, tgt) -> dict | None:
    """timestamp 비교로 시간 엣지 검출."""
    if not src.timestamp or not tgt.timestamp:
        return None
    try:
        src_year = int(src.timestamp[:4])
        tgt_year = int(tgt.timestamp[:4])
    except (ValueError, IndexError):
        return None
    if src_year < tgt_year:
        delta = tgt_year - src_year
        return {
            "label": f"{src_year} → {tgt_year} ({delta}년)",
            "weight": min(1.0, 1.0 / max(delta, 1)),   # 가까울수록 강함
            "confidence": 0.9,
        }
    return None

def _detect_causal(src_text: str, tgt_text: str) -> dict | None:
    """인과 키워드 매칭."""
    combined = src_text + " " + tgt_text
    matches = [kw for kw in CAUSAL_KEYWORDS if kw in combined]
    if not matches:
        return None
    return {
        "label": f"causal: {matches[0]}",
        "weight": min(1.0, 0.5 + 0.1 * len(matches)),
        "confidence": 0.75,
    }

def _detect_logical(src_text: str, tgt_text: str) -> dict | None:
    """논리 implication 키워드."""
    combined = src_text + " " + tgt_text
    matches = [kw for kw in LOGICAL_KEYWORDS if kw in combined]
    if not matches:
        return None
    return {
        "label": f"logical: {matches[0]}",
        "weight": min(1.0, 0.5 + 0.1 * len(matches)),
        "confidence": 0.7,
    }

def _finalize(counter: int, src, tgt, edge: dict, etype: str) -> Edge:
    return Edge(
        edge_id=f"E-{counter:03d}",
        source_node=src.node_id,
        target_node=tgt.node_id,
        edge_type=EdgeType(etype),
        label=edge["label"],
        weight=edge["weight"],
        confidence=edge["confidence"],
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-link-subs.md SUB 2)

| 명세 항목 | 본 sub 구현 |
|---|---|
| 논리: A 주장 → B 결론 (causal·implication) | `_detect_logical` + `LOGICAL_KEYWORDS` |
| 시간: 1990 사건 → 2024 결과 (temporal) | `_detect_temporal` (timestamp 비교) |
| 인과: 원인 evidence → 결과 evidence (causation) | `_detect_causal` + `CAUSAL_KEYWORDS` |
| 엣지에 weight·confidence 부여 | Edge dataclass — `weight`·`confidence` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | nodes (Graph Builder 산출) + evidence_texts (evidence_id → text dict) |
| Output | List[Edge] — edge_id·source·target·type·label·weight·confidence |
| 후속 sub | `bookwriting-evidence-link-authority-mapper` |
| Dependencies | Graph Builder 통과 |
| 결정론 모듈 | 자체 정규식 + 시간 비교 + 키워드 dict |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 결정론 매칭 + LLM은 의미 검증만 (부모 §부록 허용) |
| #2 grill-me 원문 일치 | 명세 4 항목 1:1 환원 + 3 엣지 타입 그대로 |
| #7 결정론 환원 | 정규식 + 시간 비교 100% 결정론 |

### 5. Verification (명세 §5)

- 엣지 검출 정확도 75%+ (부모 §10 — 저자 spot-check)
- 각 엣지 label 명확 (label 필드 — temporal 양식 "YEAR → YEAR (N년)")

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-link-subs.md` §SUB 2
부모 마스터 SPEC: `specs/bookwriting-evidence-link-master.md` §7 Step 3 + §13 페르소나 2 + 부록 결정론 (정규식·시간 비교·인과 키워드)
LLM 위임: 부모 §부록 — 엣지 *논리 검증* 저자 v1 양식 1:1 준수 시만 허용
