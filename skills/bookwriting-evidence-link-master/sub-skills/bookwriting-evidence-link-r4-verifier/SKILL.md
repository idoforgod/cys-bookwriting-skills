---
name: bookwriting-evidence-link-r4-verifier
description: 부모 bookwriting-evidence-link-master의 INTERNAL sub ⭐ R4 다층 강제 핵심. 저자 v1 R4 — 같은 주장에 최소 2층 권위 매핑 강제. M13 R4MultiLayerVerifier로 주장 단위 권위층 카운트 + 단일 권위 저자 묶음 4 옵션 (외부 manual·Layer 1 유지·풀 제외·defer) escalate. 통과율 85%+ 검증.
when_to_use: bookwriting-evidence-link-master Step 5 (R4 Verifier 페르소나)에서 자동 호출. Authority Mapper 통과 후. `/bookwriting-evidence-link r4-verify` 모드는 본 sub 단독.
disable-model-invocation: true
---

# bookwriting-evidence-link-r4-verifier

## TLDR

부모 bookwriting-evidence-link-master의 ⭐ R4 다층 핵심 sub. 저자 v1 R4 (단일 권위 금지) 강제. M13 R4MultiLayerVerifier로 그래프에서 *주장 단위*를 식별하고 각 주장의 권위층 수를 카운트한다. 단일 권위 주장 → 저자 묶음 4 옵션 escalate. 통과율 85%+.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Authority Mapper 통과 후 → Step 5 자동
- `/bookwriting-evidence-link r4-verify <target>` 모드는 본 sub 단독
- Mode 2 자동: R4 위반 *자동 풀 제외* (저자 묶음 skip, 부모 §부록)

## Detailed Methodology

### 1. 결정론 chain — M13 + 저자 묶음 4 옵션

```python
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from r4_multi_layer_verifier import R4MultiLayerVerifier   # M13

class R4Option(str, Enum):
    ADD_OTHER_LAYER = "add_other_layer"           # 외부 manual evidence 추가
    KEEP_LAYER1_ONLY = "keep_layer1_only"         # 주장을 Layer 1만으로 유지 (R4 위반 인지)
    EXCLUDE_CLAIM = "exclude_claim"               # 주장을 풀에서 제외
    DEFER = "defer"

@dataclass
class Claim:
    claim_id: str
    text: str
    related_node_ids: list[str]
    authority_layers: set[str] = field(default_factory=set)   # {"A","B"} 등

@dataclass
class R4Result:
    claim_id: str
    layer_count: int
    layers: list[str]
    is_compliant: bool                # 2층 이상
    bundle_options: list[R4Option] = field(default_factory=lambda: list(R4Option))

def verify_r4(
    claims: list[Claim],
    authority_results: list,           # Authority Mapper 산출
    authority_db_path: Path,
) -> list[R4Result]:
    """R4 다층 검증 + 저자 묶음 강제."""
    verifier = R4MultiLayerVerifier(authority_db_path)
    # node_id → grade index
    node_grade = {r.node_id: r.grade for r in authority_results}

    results: list[R4Result] = []

    # Step 1: 그래프에서 *주장 단위* 식별 (claims로 입력)
    for claim in claims:
        # Step 2: 각 주장의 권위층 수 카운트
        grades = {node_grade.get(nid) for nid in claim.related_node_ids if node_grade.get(nid)}
        grades.discard(None)
        layer_count = len(grades)

        # Step 3: 단일 권위만 → 저자 묶음 escalate
        # — 자동 결정 영구 금지 (Mode 2 예외만 부모 §부록)
        is_compliant = layer_count >= 2

        results.append(R4Result(
            claim_id=claim.claim_id,
            layer_count=layer_count,
            layers=sorted(grades),
            is_compliant=is_compliant,
            bundle_options=list(R4Option) if not is_compliant else [],
        ))

    return results

def calculate_pass_rate(results: list[R4Result]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r.is_compliant)
    rate = passed / max(total, 1)
    return {
        "total_claims": total,
        "passed": passed,
        "pass_rate": rate,
        "meets_threshold": rate >= 0.85,   # 부모 §15 G3 게이트
    }
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-link-subs.md SUB 4) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 그래프에서 *주장 단위* 식별 | `claims: list[Claim]` 입력 |
| Step 2: 각 주장의 권위층 수 카운트 | `grades = set()` + `layer_count` |
| Step 3: 단일 권위만 → 저자 묶음 escalate | `R4Option` 4 enum + `if not is_compliant` |
| (a) 다른 권위층 evidence 추가 (외부 manual 호출) | `R4Option.ADD_OTHER_LAYER` |
| (b) 주장을 Layer 1만으로 유지 (R4 위반 인지) | `R4Option.KEEP_LAYER1_ONLY` |
| (c) 주장을 풀에서 제외 | `R4Option.EXCLUDE_CLAIM` |
| (d) defer | `R4Option.DEFER` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | claims (list[Claim]) + authority_results (Authority Mapper 산출) + authority-db path |
| Output | List[R4Result] + pass_rate summary |
| 후속 sub | `bookwriting-evidence-link-loop-integrator` |
| Dependencies | Authority Mapper 통과 |
| 결정론 모듈 | M13 R4MultiLayerVerifier |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M13 결정론 + set 카운트 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 4 Step + 4 옵션 1:1 환원 |
| #3 출처 명시 ⭐ | R4 = 단일 권위 금지 — 책 학술 신뢰성 backbone |
| #4 저자 작가성 | 저자 묶음 *강제* — 자동 결정 영구 금지 (Mode 2 예외만) |
| #5 법적 위험 | R4 위반 주장 풀 제외 옵션 — 책 학술 위험 차단 |
| #7 결정론 환원 | M13 + set 100% 결정론 |

### 5. Verification (명세 §5)

- 모든 주장 R4 검증 (claims 100% 처리)
- 통과율 85%+ (부모 §15 G3 게이트)
- 저자 묶음 4 옵션 자동 부착 (위반 시 반드시)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-link-subs.md` §SUB 4 ⭐
부모 마스터 SPEC: `specs/bookwriting-evidence-link-master.md` §7 Step 5 ⭐ + §12 R4 Multi-Layer Gate 전용 + §13 페르소나 4 ⭐ + §15 G3 (85%+) + 부록 결정론 (M13 ⭐) + 부록 R1-R5 R4 ⭐
저자 v1 R4: chapter-pipeline.md R4 (단일 권위 금지) 원문
결정론 모듈: `lib/r4_multi_layer_verifier.py` (M13)
