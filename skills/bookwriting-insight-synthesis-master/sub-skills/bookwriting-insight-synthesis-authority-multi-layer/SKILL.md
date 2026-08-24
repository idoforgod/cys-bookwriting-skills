---
name: bookwriting-insight-synthesis-authority-multi-layer
description: 부모 bookwriting-insight-synthesis-master의 INTERNAL sub ⭐ R4 다층 강제. 통찰을 저자 권위 5층 (A-E) 결정론 매핑 + M13 R4MultiLayerVerifier로 최소 2층 강제 + 단일 권위 통찰 풀 제외 + Layer 1만 매핑 시 저자 알림 (Layer 2 보강 권장) + R4 통과 100% 검증. M3 AuthorityGrader.
when_to_use: bookwriting-insight-synthesis-master에서 voice-craft 통과 후 자동 호출. cross-chapter-check와 병렬 진행 + bundle-builder 입력. C4 Authority Multi-Layer 모드 (`--min-authority-layers 4`) 가중치 증가.
disable-model-invocation: true
---

# bookwriting-insight-synthesis-authority-multi-layer

## TLDR

부모 bookwriting-insight-synthesis-master의 ⭐ R4 다층 강제 sub. 저자 v1 R4 (단일 권위 금지)를 통찰 단위로 적용. M3 AuthorityGrader + M13 R4MultiLayerVerifier로 통찰 뒷받침 evidence들의 권위 매핑 분포를 결정론 계산하고, 최소 2층 충족 못한 통찰은 풀에서 제외한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- voice-craft 통과 후 자동 (cross-chapter-check와 병렬)
- C4 Authority Multi-Layer 모드 `--min-authority-layers 4` 시 임계 상향

## Detailed Methodology

### 1. 결정론 chain — M3 + M13 + 풀 제외

```python
from dataclasses import dataclass, field
from pathlib import Path
from authority_grader import AuthorityGrader, Grade   # M3
from r4_multi_layer_verifier import R4MultiLayerVerifier   # M13

@dataclass
class InsightAuthorityResult:
    insight_id: str
    layer_distribution: dict[str, int]   # {"A": 2, "B": 1, ...}
    layer_count: int
    r4_compliant: bool                   # 최소 2층 충족
    is_excluded: bool = False
    needs_layer2_bundle: bool = False    # Layer 1만 매핑 시 저자 알림
    reason: str | None = None

def verify_insight_authority(
    insights: list,                       # voice-craft 통과
    insight_evidence_map: dict,           # insight_id → list of evidence (grade 포함)
    authority_db_path: Path,
    min_layers: int = 2,                  # C4 모드 시 4로 상향
) -> list[InsightAuthorityResult]:
    """R4 다층 강제 + 풀 제외."""
    grader = AuthorityGrader(authority_db_path)
    r4 = R4MultiLayerVerifier(authority_db_path)
    results: list[InsightAuthorityResult] = []

    for ins in insights:
        # Step 1: 통찰을 뒷받침하는 evidence들의 권위 등급 식별
        evidence_list = insight_evidence_map.get(ins.insight_id, [])
        distribution: dict[str, int] = {}
        for ev in evidence_list:
            grade = ev.get("grade") or grader.assign_grade(source_path=ev.get("source_file", "")).value
            distribution[grade] = distribution.get(grade, 0) + 1

        # Step 2: 통찰의 *권위 매핑 분포* 계산
        layer_count = len(distribution)

        # Step 3: 최소 2층 매핑 강제 (R4)
        r4_compliant = layer_count >= min_layers

        # Step 4-5: 단일 권위만 → 통찰 풀에서 *제외* / Layer 1만 → 저자 알림
        is_excluded = False
        needs_layer2 = False
        reason = None

        if not r4_compliant:
            is_excluded = True
            reason = f"R4 위반: 권위 {layer_count}층 < 최소 {min_layers}층"

        # Layer 1만 매핑된 경우 별도 알림 (R4 통과해도 저자 알림)
        if list(distribution.keys()) == ["A"]:
            needs_layer2 = True
            reason = "Layer 1 (Grade A) 단독 매핑 — Layer 2 (Grade B) 보강 권장"

        results.append(InsightAuthorityResult(
            insight_id=ins.insight_id,
            layer_distribution=distribution,
            layer_count=layer_count,
            r4_compliant=r4_compliant,
            is_excluded=is_excluded,
            needs_layer2_bundle=needs_layer2,
            reason=reason,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-insight-synthesis-subs.md SUB 9) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 통찰을 뒷받침하는 evidence들의 권위 등급 식별 | M3 + `insight_evidence_map` |
| Step 2: 통찰의 *권위 매핑 분포* 계산 | `distribution: dict[str, int]` |
| Step 3: 최소 2층 매핑 강제 (R4) | `r4_compliant = layer_count >= min_layers` |
| Step 4: 단일 권위만 매핑 → 통찰 풀에서 *제외* | `is_excluded=True` |
| Step 5: Layer 1만 매핑 → 저자 알림 (Layer 2 보강 권장) | `needs_layer2_bundle=True` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | insights (voice-craft 통과) + insight_evidence_map + authority-db path + min_layers (기본 2, C4 모드 시 4) |
| Output | List[InsightAuthorityResult] — insight_id·distribution·layer_count·r4_compliant·excluded·needs_layer2 |
| 후속 sub | `bookwriting-insight-synthesis-bundle-builder` (R4 위반 묶음 3 입력) |
| Dependencies | voice-craft 통과 + ④ evidence-collect의 권위 등급화 (insight_evidence_map) |
| 결정론 모듈 | M3 AuthorityGrader + M13 R4MultiLayerVerifier |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M3 + M13 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 |
| #3 출처 명시 ⭐ | R4 = 단일 권위 금지 — 책 학술 신뢰성 backbone |
| #4 저자 작가성 | Layer 2 보강 저자 알림 — 저자 결정권 보장 |
| #5 법적 위험 | 단일 권위 풀 제외 — 책 학술 위험 차단 |
| #7 결정론 환원 | M3 + M13 + dict 카운트 100% 결정론 |

### 5. Verification (명세 §6)

- R4 통과 100% (자동 제외 + 알림 후 잔여 100%)
- 매핑 정확 (insight_evidence_map 정합 — ④ evidence-collect 산출)
- 풀 정리 후 통찰 수 감소 (단일 권위 제외)
- 부모 §15 G4 게이트 — 모든 통찰 최소 min_authority_layers 매핑

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-insight-synthesis-subs.md` §SUB 9 ⭐
부모 마스터 SPEC: `specs/bookwriting-insight-synthesis-master.md` §13 페르소나 3 Authority Cross-checker + §14 C4 Authority Multi-Layer + §15 G4 + 부록 E (M3·M13)
저자 v1 R4: chapter-pipeline.md R4 (단일 권위 금지) 원문
결정론 모듈: `lib/authority_grader.py` (M3) + `lib/r4_multi_layer_verifier.py` (M13)
⑤ evidence-link R4와 cross-reference: `bookwriting-evidence-link-r4-verifier` (evidence 단위 R4) vs 본 sub (insight 단위 R4)
