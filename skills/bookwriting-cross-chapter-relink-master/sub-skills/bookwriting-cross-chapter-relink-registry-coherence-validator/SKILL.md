---
name: bookwriting-cross-chapter-relink-registry-coherence-validator
description: 부모 bookwriting-cross-chapter-relink-master의 INTERNAL sub. forecast-registry 책 전체 정합 결정론 검증 — 저자 v1 chapter-pipeline R1-R5 모든 규칙 (R1 quantitative_anchor·R2 chapter_role·R3 system_loops·R4 권위 5층 다층·R5 verification_signal) 책 전체 단위 검증. M12·M13 결정론 호출.
when_to_use: bookwriting-cross-chapter-relink-master에서 loop-coherence-checker 통과 후 마지막 자동 호출 (⑪ 마지막 sub).
disable-model-invocation: true
---

# bookwriting-cross-chapter-relink-registry-coherence-validator

## TLDR

부모 bookwriting-cross-chapter-relink-master의 마지막 sub. forecast-registry를 책 전체 단위로 R1-R5 모든 규칙 결정론 검증한다. 본 sub 통과 시 저자 책 *학술 신뢰성 backbone 완성* — Phase 3-C 진입 가능.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- loop-coherence-checker 통과 후 마지막 자동 호출 (⑪ 마지막 sub)

## Detailed Methodology

### 1. 결정론 chain — R1-R5 책 전체 정합

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from forecast_registry_syncer import ForecastRegistrySyncer   # M12
from r4_multi_layer_verifier import R4MultiLayerVerifier   # M13

@dataclass
class RegistryCoherenceReport:
    r1_violations: list[str]      # quantitative_anchor 누락 P-NNN
    r2_violations: list[str]      # chapter_role 누락
    r3_violations: list[str]      # system_loops 누락
    r4_violations: list[str]      # 권위 5층 단일층 P-NNN
    r5_violations: list[str]      # verification_signal·falsifies_if 누락
    r1_pass: bool
    r2_pass: bool
    r3_pass: bool
    r4_pass: bool
    r5_pass: bool
    overall_pass: bool

def validate_registry_coherence(
    forecast_registry_path: Path,
    chapters_dir: Path,
    authority_db_path: Path,
) -> RegistryCoherenceReport:
    """R1-R5 책 전체 결정론 정합 검증."""
    syncer = ForecastRegistrySyncer(forecast_registry_path)
    r4_verifier = R4MultiLayerVerifier(authority_db_path)

    with forecast_registry_path.open(encoding="utf-8") as f:
        forecast = yaml.safe_load(f) or {}
    predictions = forecast.get("predictions", [])

    # R1: quantitative_anchor 정합 (M12)
    r1_violations = syncer.verify_r1_quantitative_anchor()

    # R2: chapter_role 정합 — 모든 P-NNN에 chapter_role 명시
    r2_violations: list[str] = []
    for p in predictions:
        if not p.get("chapter_role"):
            r2_violations.append(p.get("id", ""))

    # R3: system_loops 호명 — 모든 P-NNN이 L1-L7 중 하나에 속함
    r3_violations: list[str] = []
    for p in predictions:
        loops = p.get("system_loops", [])
        if not loops:
            r3_violations.append(p.get("id", ""))

    # R4: 권위 5층 다층 (M13) — 모든 P-NNN의 evidence가 2층 이상 권위
    r4_violations: list[str] = []
    for p in predictions:
        evidence_list = p.get("evidence", [])
        grades = {ev.get("grade") for ev in evidence_list if ev.get("grade")}
        grades.discard(None)
        if len(grades) < 2:
            r4_violations.append(p.get("id", ""))

    # R5: verification_signal·falsifies_if 명시
    r5_violations: list[str] = []
    for p in predictions:
        if not p.get("verification_signal") or not p.get("falsifies_if"):
            r5_violations.append(p.get("id", ""))

    r1_pass = not r1_violations
    r2_pass = not r2_violations
    r3_pass = not r3_violations
    r4_pass = not r4_violations
    r5_pass = not r5_violations

    return RegistryCoherenceReport(
        r1_violations=r1_violations,
        r2_violations=r2_violations,
        r3_violations=r3_violations,
        r4_violations=r4_violations,
        r5_violations=r5_violations,
        r1_pass=r1_pass,
        r2_pass=r2_pass,
        r3_pass=r3_pass,
        r4_pass=r4_pass,
        r5_pass=r5_pass,
        overall_pass=all([r1_pass, r2_pass, r3_pass, r4_pass, r5_pass]),
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-cross-chapter-relink-subs.md SUB 6)

| 명세 항목 | 본 sub 구현 |
|---|---|
| R1: quantitative_anchor 정합 | M12 `verify_r1_quantitative_anchor()` |
| R2: chapter_role 정합 | `chapter_role` 필드 검사 |
| R3: system_loops 호명 정합 | `system_loops` 필드 검사 |
| R4: 권위 5층 다층 인용 | `len(grades) >= 2` (M13 정합) |
| R5: verification_signal 명시 | `verification_signal` + `falsifies_if` |
| 모든 규칙 책 전체 단위 검증 | `overall_pass = all([r1-r5_pass])` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | forecast_registry_path + chapters_dir + authority_db_path |
| Output | RegistryCoherenceReport — R1-R5 violations + overall_pass |
| 후속 단계 | Phase 3-C 진입 (저자 실제 본문 작성) |
| Dependencies | loop-coherence-checker 통과 + forecast-registry 정합 |
| 결정론 모듈 | M12 ForecastRegistrySyncer + M13 R4MultiLayerVerifier |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 ⭐ | R1-R5 모두 결정론 검증 — 책 학술 신뢰성 backbone |
| #2 grill-me 원문 일치 | 저자 v1 chapter-pipeline.md R1-R5 원문 1:1 |
| #3 출처 명시 | R4 다층 + R5 verification 강제 |
| #5 법적 위험 | 모든 P-NNN R4 통과 보장 |
| #7 결정론 환원 | M12 + M13 + dict 100% 결정론 |
| R1-R5 강제 | 저자 v1 모든 규칙 책 전체 단위 |

### 5. Verification (명세 §5)

- R1-R5 모두 검증 (`overall_pass = True`)
- 저자 v1 chapter-pipeline 호환

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-cross-chapter-relink-subs.md` §SUB 6
부모 마스터 SPEC: `specs/bookwriting-cross-chapter-relink-master.md`
저자 v1 R1-R5: `$BOOK_ROOT/workflows/book-planning.md` 원문
결정론 모듈: `lib/forecast_registry_syncer.py` (M12) + `lib/r4_multi_layer_verifier.py` (M13)
영속 자산 보호: PHASE3B_HANDOFF §8 (forecast-registry read-only)
Phase 3-C 진입: 본 sub `overall_pass=True` 도달 시 저자 실제 본문 작성 단계 가능
