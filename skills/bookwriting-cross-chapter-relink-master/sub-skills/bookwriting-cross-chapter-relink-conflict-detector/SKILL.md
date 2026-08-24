---
name: bookwriting-cross-chapter-relink-conflict-detector
description: 부모 bookwriting-cross-chapter-relink-master의 INTERNAL sub ⭐ ②와 다른 차원 (챕터 간 모순). 챕터 간 수치 모순 (ch01 30% vs ch08 25%)·시점 모순 (ch03 2030 vs ch09 2035)·논리 모순 (ch02 X→Y vs ch07 X→Z) 결정론 검출 + severity 평가 + 저자 묶음 강제 (자동 결정 영구 금지).
when_to_use: bookwriting-cross-chapter-relink-master에서 cross-checker 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-cross-chapter-relink-conflict-detector

## TLDR

부모 bookwriting-cross-chapter-relink-master의 ⭐ 챕터 간 모순 검출 sub. ② fact-anchor가 *챕터 내부* 모순이라면, 본 sub는 *챕터 간* 모순 (수치·시점·논리)을 결정론 검출하고 severity별 저자 묶음 강제한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- cross-checker 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — 3 모순 분류

```python
import re
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

class CrossConflictType(str, Enum):
    NUMERIC = "numeric"       # 수치 (30% vs 25%)
    TEMPORAL = "temporal"     # 시점 (2030 vs 2035)
    LOGICAL = "logical"       # 논리 (X→Y vs X→Z)

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class CrossChapterConflict:
    conflict_id: str
    chapter_a: str
    chapter_b: str
    item_a_id: str
    item_b_id: str
    conflict_type: CrossConflictType
    severity: Severity
    description: str
    needs_bundle: bool = True    # 저자 묶음 강제

def detect_cross_chapter_conflicts(graph) -> list[CrossChapterConflict]:
    """3 모순 유형 결정론 검출."""
    conflicts: list[CrossChapterConflict] = []
    counter = 0
    nodes_by_id = {n.item_id: n for n in graph.nodes}

    # 관련성 ≥ 0.7 엣지 페어 검사 (cross-checker 산출)
    for edge in graph.edges:
        n1 = nodes_by_id.get(edge.node_a)
        n2 = nodes_by_id.get(edge.node_b)
        if not n1 or not n2:
            continue

        # 수치 모순 — 같은 주제 다른 %·N
        num_a = _extract_number(n1.text)
        num_b = _extract_number(n2.text)
        if num_a is not None and num_b is not None and num_a != num_b:
            counter += 1
            # 연도 분리
            year_a = _extract_year(n1.text)
            year_b = _extract_year(n2.text)
            if year_a and year_b and year_a != year_b:
                ctype = CrossConflictType.TEMPORAL
                delta = abs(year_a - year_b)
                sev = _severity_temporal(delta)
                desc = f"시점 모순: {n1.chapter_id} {year_a} vs {n2.chapter_id} {year_b}"
            else:
                ctype = CrossConflictType.NUMERIC
                delta = abs(num_a - num_b) / max(abs(num_a), abs(num_b), 1)
                sev = _severity_numeric(delta)
                desc = f"수치 모순: {n1.chapter_id} {num_a} vs {n2.chapter_id} {num_b}"
            conflicts.append(CrossChapterConflict(
                conflict_id=f"CC-{counter:03d}",
                chapter_a=n1.chapter_id,
                chapter_b=n2.chapter_id,
                item_a_id=n1.item_id,
                item_b_id=n2.item_id,
                conflict_type=ctype,
                severity=sev,
                description=desc,
            ))

        # 논리 모순 — X → Y vs X → Z (정규식)
        impl_a = _extract_implication(n1.text)
        impl_b = _extract_implication(n2.text)
        if impl_a and impl_b and impl_a[0] == impl_b[0] and impl_a[1] != impl_b[1]:
            counter += 1
            conflicts.append(CrossChapterConflict(
                conflict_id=f"CC-{counter:03d}",
                chapter_a=n1.chapter_id,
                chapter_b=n2.chapter_id,
                item_a_id=n1.item_id,
                item_b_id=n2.item_id,
                conflict_type=CrossConflictType.LOGICAL,
                severity=Severity.MEDIUM,
                description=f"논리 모순: {impl_a[0]}→{impl_a[1]} ({n1.chapter_id}) vs {impl_b[0]}→{impl_b[1]} ({n2.chapter_id})",
            ))

    return conflicts

def _extract_number(text: str) -> Optional[float]:
    m = re.search(r"(\d+(?:\.\d+)?)", text)
    return float(m.group(1)) if m else None

def _extract_year(text: str) -> Optional[int]:
    m = re.search(r"\b(20\d{2})\b", text)
    return int(m.group(1)) if m else None

def _extract_implication(text: str) -> Optional[tuple[str, str]]:
    m = re.search(r"([\w가-힣]+)\s*[→\-]+>\s*([\w가-힣]+)", text)
    return (m.group(1), m.group(2)) if m else None

def _severity_numeric(delta: float) -> Severity:
    if delta < 0.1: return Severity.LOW
    if delta < 0.3: return Severity.MEDIUM
    if delta < 0.6: return Severity.HIGH
    return Severity.CRITICAL

def _severity_temporal(delta: int) -> Severity:
    if delta < 2: return Severity.LOW
    if delta < 5: return Severity.MEDIUM
    if delta < 10: return Severity.HIGH
    return Severity.CRITICAL
```

### 2. 명세 §출처 (SPEC: bookwriting-cross-chapter-relink-subs.md SUB 2) ⭐

| 명세 항목 | 본 sub 구현 |
|---|---|
| 수치 모순: "ch01 30% vs ch08 25%" | `CrossConflictType.NUMERIC` + delta 정규식 |
| 시점 모순: "ch03 2030 vs ch09 2035" | `CrossConflictType.TEMPORAL` + year delta |
| 논리 모순: "ch02 X→Y vs ch07 X→Z" | `CrossConflictType.LOGICAL` + implication 추출 |
| severity 평가 + 저자 묶음 | `_severity_numeric`·`_severity_temporal` + `needs_bundle=True` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | graph (cross-checker 산출) |
| Output | List[CrossChapterConflict] — 3 type·severity·저자 묶음 |
| 후속 sub | reroute-recommender |
| Dependencies | cross-checker 통과 |
| 결정론 모듈 | 자체 정규식 + dict 분기 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 정규식 + 분기 결정론 |
| #2 grill-me 원문 일치 | 명세 3 모순 1:1 |
| #4 저자 작가성 | 저자 묶음 *강제* — 자동 결정 영구 금지 |
| #5 법적 위험 | 책 일관성 파탄 차단 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 모순 검출 정확도 80%+ (false positive 허용)
- 저자 결정 강제 (`needs_bundle = True` 영구)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-cross-chapter-relink-subs.md` §SUB 2 ⭐
부모 마스터 SPEC: `specs/bookwriting-cross-chapter-relink-master.md`
② fact-anchor-conflict-detector 정합: 챕터 *내부* vs ⑪ *간*
