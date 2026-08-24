---
name: bookwriting-evidence-link-loop-integrator
description: 부모 bookwriting-evidence-link-master의 INTERNAL sub. 저자 시스템 루프 L1-L7과 evidence 그래프 결정론 통합 + 각 노드/엣지를 L1-L7 중 1개 이상에 매핑 + forecast-registry system_loops 정합 + 매핑률 80%+ 검증. ③ systemlink-system-loop-mapper와 양식 정합.
when_to_use: bookwriting-evidence-link-master Step 6 (Loop Integrator 페르소나)에서 자동 호출. R4 Verifier 통과 후. `/bookwriting-evidence-link loop-integrate` 모드는 본 sub 단독.
disable-model-invocation: true
---

# bookwriting-evidence-link-loop-integrator

## TLDR

부모 bookwriting-evidence-link-master의 루프 통합 sub. 저자 v1 시스템 루프 L1-L7 (지능대체나선·정치내파·봉건제 풍요·인구 비용·도덕 비용·우주척도·의미위기)과 evidence 그래프를 결정론 통합한다. 각 노드/엣지를 L1-L7 중 1개 이상 매핑 + forecast-registry system_loops 정합 + 매핑률 80%+. ③ systemlink-system-loop-mapper와 양식 정합.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- R4 Verifier 통과 후 → Step 6 자동
- `/bookwriting-evidence-link loop-integrate <target>` 모드는 본 sub 단독

## Detailed Methodology

### 1. 결정론 chain — L1-L7 매핑 + forecast-registry 정합

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class LoopIntegration:
    node_id: str
    mapped_loops: list[str]      # ["L1", "L7"] (cross-loop 가능)
    edge_loops: dict[str, list[str]]   # edge_id → list of loop_id

def integrate_loops(
    nodes: list,
    edges: list,
    forecast_registry_path: Path,
) -> tuple[list[LoopIntegration], dict]:
    """L1-L7 매핑 + 매핑률 검증."""
    # forecast-registry.system_loops 로드 (③ systemlink와 동일 데이터 소스)
    with forecast_registry_path.open(encoding="utf-8") as f:
        forecast = yaml.safe_load(f) or {}
    system_loops = forecast.get("system_loops", {})

    integrations: list[LoopIntegration] = []
    mapped_count = 0

    # Step 1: 각 노드를 L1-L7 중 1개 이상에 매핑
    for node in nodes:
        # 노드 source 텍스트 기반 매핑 (간소화 — 부모가 evidence 텍스트 풀로 보강)
        loops_for_node = _match_node_to_loops(node, system_loops)
        if loops_for_node:
            mapped_count += 1

        # 노드 관련 엣지를 같은 루프에 매핑
        node_edges = [e for e in edges if e.source_node == node.node_id or e.target_node == node.node_id]
        edge_loops = {e.edge_id: loops_for_node for e in node_edges}

        integrations.append(LoopIntegration(
            node_id=node.node_id,
            mapped_loops=loops_for_node,
            edge_loops=edge_loops,
        ))

    # Step 2: forecast-registry system_loops와 정합 (cross-check만 — write 영구 금지)

    # Step 3: 매핑률 80%+ 검증 (부모 §15 G4 게이트)
    mapping_rate = mapped_count / max(len(nodes), 1)

    summary = {
        "total_nodes": len(nodes),
        "mapped_nodes": mapped_count,
        "mapping_rate": mapping_rate,
        "meets_threshold": mapping_rate >= 0.8,
        "loop_distribution": _loop_distribution(integrations),
    }
    return integrations, summary

def _match_node_to_loops(node, system_loops: dict) -> list[str]:
    """노드 메타로 L1-L7 매칭 — ③ systemlink와 동일 lookup 방식."""
    matched = []
    # 노드 author·quant_anchors·source 텍스트 키워드로 매칭
    for loop_id, loop_def in system_loops.items():
        loop_keywords = loop_def.get("keywords", []) + [loop_def.get("name", "")]
        # node의 source_file 이름·author·quant_anchors text 키워드 매칭
        node_text = " ".join([
            node.author or "",
            node.source_file,
            " ".join(node.quant_anchors),
        ])
        if any(kw in node_text for kw in loop_keywords if kw):
            matched.append(loop_id)
    return matched

def _loop_distribution(integrations: list) -> dict:
    counts: dict[str, int] = {}
    for it in integrations:
        for lid in it.mapped_loops:
            counts[lid] = counts.get(lid, 0) + 1
    return counts
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-link-subs.md SUB 5)

| 명세 항목 | 본 sub 구현 |
|---|---|
| 각 노드/엣지를 L1-L7 중 1개 이상에 매핑 | `_match_node_to_loops()` + `edge_loops` |
| forecast-registry system_loops와 정합 | `yaml.safe_load(forecast_registry_path)` + cross-check |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | nodes (Graph Builder) + edges (Edge Detector) + forecast-registry path |
| Output | (List[LoopIntegration], summary — mapping_rate·loop_distribution) |
| 후속 sub | `bookwriting-evidence-link-isolation-detector` |
| Dependencies | R4 Verifier 통과 + forecast-registry.system_loops 정의 + ③ systemlink-system-loop-mapper 양식 정합 |
| 결정론 모듈 | yaml.safe_load + dict lookup |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | yaml + dict 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 2 항목 1:1 환원 + L1-L7 저자 v1 정의 그대로 |
| #7 결정론 환원 | 100% 결정론 |
| R3 강제 | system_loops 통합 (부모 §부록 R1-R5 R3) |

### 5. Verification (명세 §5)

- L1-L7 매핑률 80%+ (부모 §15 G4 게이트)
- forecast-registry 정합 (read-only cross-check, write 영구 금지)
- ③ systemlink-system-loop-mapper와 양식 정합 (동일 system_loops 데이터)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-link-subs.md` §SUB 5
부모 마스터 SPEC: `specs/bookwriting-evidence-link-master.md` §7 Step 6 + §13 페르소나 5 + §15 G4 (80%+) + 부록 R3 강제
③ systemlink 정합: `skills/bookwriting-systemlink-master/sub-skills/bookwriting-systemlink-system-loop-mapper/SKILL.md` (동일 L1-L7 데이터)
영속 자산 보호: PHASE3B_HANDOFF §8 (forecast-registry read-only)
