---
name: bookwriting-evidence-collect-evidence-quality-filter
description: 부모 bookwriting-evidence-collect-master의 INTERNAL sub. 모든 발굴 evidence 5 차원 종합 점수 (relevance·authority_grade·R4 적합성·정량 앵커 수·검증 신호 보유) 결정론 산출 + 임계 통과 시 chapter evidence-track 등록 + 임계 미달 시 저자 묶음 (Grade A·B 보강 권장) escalate + 채택률 60%+ 검증.
when_to_use: bookwriting-evidence-collect-master Step 9 (Forecast Registry Syncer 다음, 최종 산출 직전)에서 자동 호출. 모든 sub 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-evidence-collect-evidence-quality-filter

## TLDR

부모 bookwriting-evidence-collect-master의 ⑥ 최종 필터 sub. 모든 발굴 evidence를 5 차원 (relevance·authority_grade·R4·정량 앵커·검증 신호) 결정론 가중합 점수로 평가하고, 임계 통과 시 chapter evidence-track에 등록·임계 미달 시 저자 묶음 escalate. 채택률 60%+, Grade A·B 60%+ 검증.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Forecast Registry Syncer 통과 후 → Step 9 자동 (최종 필터)

## Detailed Methodology

### 1. 결정론 chain — 5 차원 가중합 + 임계 분기

```python
from dataclasses import dataclass
from enum import Enum

class Decision(str, Enum):
    ADOPT = "adopt"           # evidence-track 등록
    ESCALATE = "escalate"     # 저자 묶음 — Grade A·B 보강 권장
    REJECT = "reject"         # 풀에서 제외

@dataclass
class QualityScore:
    evidence_id: str
    source_file: str
    relevance: float          # 0-1 (시드 관련성, asset-searcher 산출)
    authority_grade: str      # "A"|"B"|"C"|"D"|"E"
    r4_compliant: bool        # R4 다층 적합성 (authority-grader 산출)
    quant_anchor_count: int   # 정량 앵커 보유 수
    has_verification_signal: bool
    total_score: float
    decision: Decision

# 5 차원 가중치 (부모 §10 정량 기준 + Grade A·B 가산점)
GRADE_WEIGHT = {"A": 1.0, "B": 0.85, "C": 0.6, "D": 0.4, "E": 0.2}
ADOPT_THRESHOLD = 0.65    # 60% (부모 §10 채택률) + α 마진

def filter_evidence_quality(
    graded_evidence: list,
    quant_anchors: list,
    verification_signals: list,
    sync_result,
) -> tuple[list[QualityScore], dict]:
    """5 차원 종합 점수 + 채택 vs 저자 묶음."""
    # source_file별 anchor·signal 인덱스
    anchors_by_source = {}
    for a in quant_anchors:
        anchors_by_source.setdefault(a.source_file, []).append(a)
    signals_by_source = {}
    for s in verification_signals:
        signals_by_source.setdefault(s.source_file, []).append(s)

    results = []
    for ev in graded_evidence:
        if ev.is_excluded:
            results.append(QualityScore(
                evidence_id=ev.source_file,
                source_file=ev.source_file,
                relevance=0.0,
                authority_grade=ev.grade,
                r4_compliant=False,
                quant_anchor_count=0,
                has_verification_signal=False,
                total_score=0.0,
                decision=Decision.REJECT,
            ))
            continue

        # Step 1: 각 evidence 종합 점수 산출
        relevance = getattr(ev, "relevance", 0.7)   # asset-searcher 산출
        grade_w = GRADE_WEIGHT.get(ev.grade, 0.5)
        r4_compliant = getattr(ev, "r4_compliant", True)
        anchor_count = len(anchors_by_source.get(ev.source_file, []))
        has_vs = bool(signals_by_source.get(ev.source_file))

        # 가중합 결정론: relevance × grade × (R4 보너스) × (anchor 보너스) × (signal 보너스)
        score = (
            0.30 * relevance
            + 0.30 * grade_w
            + 0.15 * (1.0 if r4_compliant else 0.0)
            + 0.15 * min(1.0, anchor_count / 3)   # 3+ anchor = 만점
            + 0.10 * (1.0 if has_vs else 0.0)
        )

        # Step 2-3: 임계 분기
        if score >= ADOPT_THRESHOLD:
            decision = Decision.ADOPT
        elif score >= 0.4:
            decision = Decision.ESCALATE   # 저자 묶음 — Grade A·B 보강 권장
        else:
            decision = Decision.REJECT

        results.append(QualityScore(
            evidence_id=ev.source_file,
            source_file=ev.source_file,
            relevance=relevance,
            authority_grade=ev.grade,
            r4_compliant=r4_compliant,
            quant_anchor_count=anchor_count,
            has_verification_signal=has_vs,
            total_score=score,
            decision=decision,
        ))

    # 통계 summary
    total = len(results)
    adopted = sum(1 for r in results if r.decision == Decision.ADOPT)
    ab_count = sum(1 for r in results if r.decision == Decision.ADOPT and r.authority_grade in ("A", "B"))

    summary = {
        "total_evidence": total,
        "adopted": adopted,
        "adopt_ratio": adopted / max(total, 1),
        "ab_ratio_in_adopted": ab_count / max(adopted, 1),
        "meets_adopt_threshold": (adopted / max(total, 1)) >= 0.6,
        "meets_ab_threshold": (ab_count / max(adopted, 1)) >= 0.6,
    }
    return results, summary
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-collect-subs.md SUB 6)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 각 evidence 종합 점수 (5 차원: relevance·grade·R4·anchor·signal) | 가중합 결정론 0.30+0.30+0.15+0.15+0.10 |
| Step 2: 임계값 통과 evidence → chapter evidence-track 등록 | `decision=ADOPT` + 부모 yaml write |
| Step 3: 임계 미달 → 풀 제외 + 저자 묶음 (Grade A·B 보강 권장) | `ESCALATE` vs `REJECT` 분기 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | graded_evidence + quant_anchors + verification_signals + sync_result |
| Output | (List[QualityScore], summary dict — adopt_ratio·ab_ratio·threshold 정합) |
| 후속 단계 | ⑤ evidence-link (다음 단계 마스터) — adopted evidence만 입력 |
| Dependencies | Forecast Registry Syncer 통과 (모든 sub 결합) |
| 결정론 모듈 | 가중합 점수 + dict lookup |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 가중합 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 3 Step 1:1 환원 + 5 차원 그대로 |
| #3 출처 명시 | source_file 필수 |
| #5 법적 위험 | Grade A·B 60%+ 강제 — 책 학술 신뢰성 |
| #7 결정론 환원 | 100% 결정론 (가중치 hardcode·임계 분기) |

### 5. Verification (명세 §5 + 부모 §10)

- 채택률 60%+ (부모 §10 정량)
- Grade A·B 비율 60%+ (채택 evidence 중)
- 저자 spot-check 정합 (5 차원 가중합 — 저자 직관과 일치)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-collect-subs.md` §SUB 6
부모 마스터 SPEC: `specs/bookwriting-evidence-collect-master.md` §10 정량 기준 + §15 G3 게이트 (Grade A·B 60%+)
영속 자산 보호: PHASE3B_HANDOFF §8 (evidence-track yaml write 부모 마스터 단일 진입)
