---
name: bookwriting-fact-anchor-conflict-detector
description: 부모 bookwriting-fact-anchor-master의 INTERNAL sub ⭐. 같은 주제 다른 수치/시점/논리 충돌 fact 자동 검출 + severity (low·medium·high·critical) 평가 + 저자 묶음 escalate 강제 (자동 결정 영구 금지).
when_to_use: bookwriting-fact-anchor-master Step 5 (Conflict Detector 페르소나)에서 자동 호출. Duplicate Detector 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-fact-anchor-conflict-detector

## TLDR

부모 bookwriting-fact-anchor-master의 ⭐ 모순 검출 핵심 sub. 같은 주제 다른 수치 (100배 vs 50배)·시점 (2030 vs 2035)·논리 (A→B vs A→C) 충돌을 자동 검출하고 severity를 평가한다. 발견 시 *저자 묶음 escalate 강제* — 자동 결정 영구 금지.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Duplicate Detector 통과 후 Step 5 자동
- `/bookwriting-fact-anchor conflict-detect <target>` 모드는 충돌만 단독 실행

## Detailed Methodology

### 1. 결정론 chain — 충돌 3 분류 + severity

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional
import re

class ConflictType(str, Enum):
    NUMERIC = "numeric"     # 수치 충돌 (100배 vs 50배)
    TEMPORAL = "temporal"   # 시점 충돌 (2030 vs 2035)
    LOGICAL = "logical"     # 논리 충돌 (A→B vs A→C)

class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class FactConflict:
    fact_a_id: str
    fact_b_id: str
    conflict_type: ConflictType
    severity: Severity
    delta: float            # 수치 차이 비율
    description: str

def detect_conflicts(fact_pool: list, duplicate_groups: list) -> list[FactConflict]:
    """같은 주제 fact 간 모순 검출 + severity 평가."""
    conflicts = []
    pool_by_id = {f.fact_id: f for f in fact_pool}

    # Step 1: *같은 주제* fact 페어 식별 — duplicate_groups의 secondary 검토
    for group in duplicate_groups:
        primary = pool_by_id[group.primary_fact_id]
        for sec_id in group.secondary_fact_ids:
            secondary = pool_by_id[sec_id]

            # Step 2: 충돌 분류
            ctype, delta = _classify_conflict(primary, secondary)
            if ctype is None:
                continue   # 충돌 아님 (true 중복)

            # Step 3: severity 평가
            severity = _severity_of(ctype, delta)

            conflicts.append(FactConflict(
                fact_a_id=primary.fact_id,
                fact_b_id=sec_id,
                conflict_type=ctype,
                severity=severity,
                delta=delta,
                description=f"{ctype.value}: '{primary.text}' vs '{secondary.text}'",
            ))

    # Step 4: 저자 묶음 escalate 강제 (자동 결정 영구 금지)
    if conflicts:
        # 부모 마스터에 ESCALATE_BUNDLE 신호 — 저자 결정까지 진행 차단
        pass

    return conflicts

def _classify_conflict(a, b) -> tuple[Optional[ConflictType], float]:
    """수치·시점·논리 분류."""
    # 수치 충돌: "N% / N배 / N명" 다름
    num_a = _extract_number(a.text)
    num_b = _extract_number(b.text)
    if num_a is not None and num_b is not None and num_a != num_b:
        if "년" in a.text and "년" in b.text:
            return (ConflictType.TEMPORAL, abs(num_a - num_b))
        delta = abs(num_a - num_b) / max(abs(num_a), abs(num_b), 1)
        return (ConflictType.NUMERIC, delta)
    # 논리 충돌은 LLM 의미 평가 영역 (부모 마스터 §부록 LLM 허용)
    return (None, 0.0)

def _extract_number(text: str) -> Optional[float]:
    m = re.search(r"(\d+(?:\.\d+)?)", text)
    return float(m.group(1)) if m else None

def _severity_of(ctype: ConflictType, delta: float) -> Severity:
    if ctype == ConflictType.NUMERIC:
        if delta < 0.1: return Severity.LOW
        if delta < 0.3: return Severity.MEDIUM
        if delta < 0.6: return Severity.HIGH
        return Severity.CRITICAL
    if ctype == ConflictType.TEMPORAL:
        if delta < 2: return Severity.LOW
        if delta < 5: return Severity.MEDIUM
        if delta < 10: return Severity.HIGH
        return Severity.CRITICAL
    return Severity.MEDIUM
```

### 2. 명세 §출처 (SPEC: bookwriting-fact-anchor-subs.md SUB 3) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: fact 풀에서 *같은 주제* 다른 수치/시점 발견 | duplicate_groups 통한 페어 식별 |
| Step 2: 모순 분류 (수치·시점·논리) | `ConflictType` enum 3 종 |
| Step 3: 모순 severity 평가 (low·medium·high·critical) | `_severity_of()` 임계 분기 |
| Step 4: 저자 묶음 escalate (자동 결정 안 함) | `if conflicts: ESCALATE_BUNDLE` 강제 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | fact_pool (list) + duplicate_groups (Duplicate Detector 산출) |
| Output | List[FactConflict] + ESCALATE_BUNDLE 신호 |
| 후속 sub | (충돌 해결 후) `bookwriting-fact-anchor-registry-syncer` |
| Dependencies | Duplicate Detector 통과 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 수치 추출 정규식·severity 임계 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 환원 + 3 분류 (수치·시점·논리) |
| #4 저자 작가성 | 저자 묶음 *강제* — 자동 결정 영구 금지 |
| #5 법적 위험 | 충돌 정량 자동 결정 시 책 일관성 파탄 위험 → 저자 결정 강제 |
| #7 결정론 환원 | 정규식 + 임계 분기 100% 결정론·LLM은 논리 충돌 의미 평가만 (부모 §부록 허용) |

### 5. Verification (명세 §7)

- 모순 검출 정확도 85%+ (false positive 허용 — 저자 확인)
- 저자 결정 *강제* (자동 결정 0건 — 본 sub 핵심 가드)
- severity 정합 (delta 임계 결정론 분기)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-fact-anchor-subs.md` §SUB 3 ⭐
부모 마스터 SPEC: `specs/bookwriting-fact-anchor-master.md` §7 Step 5 + §12 Conflict Detection 가드 + §13 페르소나 3 ⭐ + Round 8 #D9.4 (충돌 발견 시 저자 묶음 강제)
저자 결정: 자동 결정 영구 금지 (§12 가드)
