---
name: bookwriting-evidence-link-graph-visualizer
description: 부모 bookwriting-evidence-link-master의 INTERNAL sub. 완성 evidence 그래프를 markdown table (노드·엣지) + ASCII diagram (루프 그룹화)으로 결정론 시각화. 저자 spot-check 검토 용이성 우선. 외부 라이브러리 의존 없음 (pure Python str 조립).
when_to_use: bookwriting-evidence-link-master Step 9 (최종 산출 직전)에서 자동 호출. Isolation Detector 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-evidence-link-graph-visualizer

## TLDR

부모 bookwriting-evidence-link-master의 ⑦ 시각화 sub. 완성 그래프 (노드·엣지·권위·루프·고립)를 markdown table + ASCII diagram으로 결정론 출력한다. pure Python str 조립 — 외부 라이브러리 의존 없음. 저자 spot-check 검토 용이성 우선.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Isolation Detector 통과 후 → Step 9 최종 산출 직전 자동
- 옵션 `--visualize` 시 본 sub 강제 실행

## Detailed Methodology

### 1. 결정론 chain — markdown table + ASCII diagram

```python
from dataclasses import dataclass

@dataclass
class VisualizationOutput:
    node_table_md: str           # markdown table
    edge_table_md: str
    ascii_diagram: str           # 간단 ASCII (루프 그룹화)
    summary_md: str

def visualize_graph(
    nodes: list,
    edges: list,
    authority_results: list,
    loop_integrations: list,
    isolated_results: list,
) -> VisualizationOutput:
    """그래프 → markdown + ASCII 결정론 시각화."""
    # 1. 노드 markdown table
    node_lines = ["| Node | Grade | Author | Loops | Degree |", "|---|---|---|---|---|"]
    by_node_loop = {it.node_id: it.mapped_loops for it in loop_integrations}
    by_node_grade = {r.node_id: r.grade for r in authority_results}
    degree = {n.node_id: 0 for n in nodes}
    for e in edges:
        degree[e.source_node] = degree.get(e.source_node, 0) + 1
        degree[e.target_node] = degree.get(e.target_node, 0) + 1
    for n in nodes:
        loops = ",".join(by_node_loop.get(n.node_id, [])) or "-"
        node_lines.append(
            f"| {n.node_id} | {by_node_grade.get(n.node_id, '?')} | {n.author or '-'} | {loops} | {degree.get(n.node_id, 0)} |"
        )
    node_table_md = "\n".join(node_lines)

    # 2. 엣지 markdown table
    edge_lines = ["| Edge | Source | Target | Type | Label | Weight |", "|---|---|---|---|---|---|"]
    for e in edges:
        edge_lines.append(
            f"| {e.edge_id} | {e.source_node} | {e.target_node} | {e.edge_type.value} | {e.label} | {e.weight:.2f} |"
        )
    edge_table_md = "\n".join(edge_lines)

    # 3. ASCII diagram — 루프 그룹화 (L1 → 노드 목록)
    ascii_lines = ["```", "evidence graph (loop grouping):"]
    loops_to_nodes: dict[str, list[str]] = {}
    for it in loop_integrations:
        for lid in it.mapped_loops:
            loops_to_nodes.setdefault(lid, []).append(it.node_id)
    for lid in sorted(loops_to_nodes.keys()):
        ascii_lines.append(f"  {lid}: {', '.join(loops_to_nodes[lid])}")
    if isolated_results:
        ascii_lines.append("  (isolated):")
        for it in isolated_results:
            if it.is_isolated:
                ascii_lines.append(f"    - {it.node_id} (degree 0)")
    ascii_lines.append("```")
    ascii_diagram = "\n".join(ascii_lines)

    # 4. summary
    summary_md = (
        f"- 노드 {len(nodes)}개\n"
        f"- 엣지 {len(edges)}개 "
        f"(논리 {sum(1 for e in edges if e.edge_type.value == 'logical')}"
        f" · 시간 {sum(1 for e in edges if e.edge_type.value == 'temporal')}"
        f" · 인과 {sum(1 for e in edges if e.edge_type.value == 'causal')})\n"
        f"- 고립 노드 {sum(1 for it in isolated_results if it.is_isolated)}개\n"
    )

    return VisualizationOutput(
        node_table_md=node_table_md,
        edge_table_md=edge_table_md,
        ascii_diagram=ascii_diagram,
        summary_md=summary_md,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-link-subs.md SUB 7)

| 명세 항목 | 본 sub 구현 |
|---|---|
| 그래프를 markdown table 시각화 | `node_table_md` + `edge_table_md` |
| 간단한 ASCII 시각화 | `ascii_diagram` (루프 그룹화) |
| 저자 검토 용이한 형식 | summary_md + 한국어 헤더 + 정렬 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | nodes + edges + authority_results + loop_integrations + isolated_results |
| Output | VisualizationOutput — 4 markdown 필드 |
| 후속 단계 | 부모 마스터가 저자 화면에 출력 |
| Dependencies | Isolation Detector 통과 (모든 sub 결합) |
| 결정론 모듈 | 자체 str 조립 (pure Python — 외부 의존 없음) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | str 조립 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 3 항목 1:1 환원 |
| #7 결정론 환원 | 100% 결정론 (외부 라이브러리 의존 없음 — pure Python) |

### 5. Verification (명세 §5)

- 저자 spot-check 가독성 (markdown table 양식)
- 노드·엣지 정합 (counts·grade·loops 누락 0)
- ASCII diagram 루프 그룹화 정확

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-link-subs.md` §SUB 7
부모 마스터 SPEC: `specs/bookwriting-evidence-link-master.md` §7 Step 8 (저자 화면) + §13 페르소나 7 ⭐ (visualize option) + §17 검증 4 (그래프 시각화 markdown table)
결정론 양식: pure Python str — 외부 라이브러리 의존 영구 금지
