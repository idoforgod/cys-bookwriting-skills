---
name: bookwriting-evidence-collect-forecast-registry-syncer
description: 부모 bookwriting-evidence-collect-master의 INTERNAL sub. authority-grader·quantitative-anchor-extractor 통과 evidence를 M12 ForecastRegistrySyncer로 forecast-registry.yaml에 sync — 신규 P-NNN 등록·기존 P-NNN evidence 추가·중복 P-NNN 검출 시 저자 묶음 (병합·신규·skip) 강제 + 저자 v1 R1 quantitative_anchor 정합 검증.
when_to_use: bookwriting-evidence-collect-master Step 6 (Forecast Registry Syncer 페르소나)에서 자동 호출. quantitative-anchor-extractor + verification-signal-finder 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-evidence-collect-forecast-registry-syncer

## TLDR

부모 bookwriting-evidence-collect-master의 forecast-registry sync sub. M12 ForecastRegistrySyncer로 evidence·quant anchor·verification signal을 P-NNN에 결정론 sync한다. 중복 P-NNN 검출 시 저자 묶음 (병합·신규·skip 3 옵션) 강제. 저자 v1 R1 quantitative_anchor 정합 검증.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- quantitative-anchor-extractor + verification-signal-finder 통과 후 → Step 6 자동

## Detailed Methodology

### 1. 결정론 chain — M12 + 중복 저자 묶음 강제

```python
from enum import Enum
from dataclasses import dataclass
from pathlib import Path
from forecast_registry_syncer import ForecastRegistrySyncer   # M12

class DuplicateOption(str, Enum):
    MERGE = "merge"
    NEW = "new"
    SKIP = "skip"

@dataclass
class SyncResult:
    new_predictions: list[str]       # 신규 P-NNN
    updated_predictions: list[str]   # evidence 추가된 기존 P-NNN
    duplicate_conflicts: list[dict]  # 중복 P-NNN 저자 묶음 필요 (자동 결정 금지)
    r1_violations: list[str]         # R1 quantitative_anchor 위반

def sync_forecast_registry(
    graded_evidence: list,
    quant_anchors: list,
    verification_signals: list,
    forecast_registry_path: Path,
) -> SyncResult:
    """evidence·anchor·signal → forecast-registry 결정론 sync."""
    syncer = ForecastRegistrySyncer(forecast_registry_path)
    new_pnnns = []
    updated_pnnns = []
    duplicate_conflicts = []

    # Step 1: authority-grader·quantitative-anchor-extractor 통과 evidence 로드
    # (graded_evidence·quant_anchors·verification_signals 입력으로 받음)

    # Step 2: forecast-registry의 기존 P-NNN과 매칭
    for anchor in quant_anchors:
        if anchor.citation_gate_critical:
            continue   # Critical 차단된 anchor는 sync 안 함

        existing_pnnn = syncer.match_to_existing(
            quantitative_anchor=anchor.text,
            fact_type=anchor.unit,
        )

        # Step 3: 매칭되면 evidence 추가
        if existing_pnnn:
            # 중복 P-NNN 검출 — 저자 묶음 강제 (자동 결정 영구 금지)
            if syncer.is_ambiguous_match(existing_pnnn, anchor):
                duplicate_conflicts.append({
                    "anchor_id": anchor.anchor_id,
                    "existing_pnnn": existing_pnnn,
                    "anchor_text": anchor.text,
                    "options": list(DuplicateOption),
                })
            else:
                syncer.add_evidence(
                    pnnn=existing_pnnn,
                    source_file=anchor.source_file,
                    grade=anchor.grade,
                )
                updated_pnnns.append(existing_pnnn)
        else:
            # 매칭 없으면 P-NNN 신규 등록
            pnnn = syncer.register_new(
                quantitative_anchor=anchor.text,
                source_file=anchor.source_file,
                grade=anchor.grade,
                is_park_signature=anchor.is_park_signature,
            )
            new_pnnns.append(pnnn)

    # verification_signal·falsifies_if 필드도 sync (M12 forecast_registry_syncer)
    for vs in verification_signals:
        if vs.p_nnn_link:
            syncer.add_verification_signal(
                pnnn=vs.p_nnn_link,
                signal_type=vs.signal_type.value,
                text=vs.text,
                target_year=vs.target_year,
            )

    # Step 5: 저자 v1 R1 quantitative_anchor 정합 검증
    r1_violations = syncer.verify_r1_quantitative_anchor()

    return SyncResult(
        new_predictions=new_pnnns,
        updated_predictions=updated_pnnns,
        duplicate_conflicts=duplicate_conflicts,
        r1_violations=r1_violations,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-collect-subs.md SUB 5)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: authority-grader·quantitative-anchor-extractor 통과 evidence 로드 | `quant_anchors` + `graded_evidence` 입력 |
| Step 2: forecast-registry의 기존 P-NNN과 매칭 | M12 `syncer.match_to_existing()` |
| Step 3: 매칭되면 evidence 추가·매칭 없으면 P-NNN 신규 등록 | `syncer.add_evidence()` + `syncer.register_new()` |
| Step 4: 중복 P-NNN 검출 → 저자 묶음 (병합·신규·skip) | `duplicate_conflicts` + `DuplicateOption` 3 enum |
| Step 5: v1 R1 quantitative_anchor 정합 검증 | M12 `verify_r1_quantitative_anchor()` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | graded_evidence + quant_anchors + verification_signals + forecast-registry path |
| Output | SyncResult — new_predictions + updated_predictions + duplicate_conflicts + r1_violations |
| 후속 sub | `bookwriting-evidence-collect-evidence-quality-filter` |
| Dependencies | quantitative-anchor-extractor + verification-signal-finder 통과 |
| 결정론 모듈 | M12 ForecastRegistrySyncer |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M12 결정론 + yaml.safe_load — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 + 저자 묶음 3 옵션 (병합·신규·skip) |
| #3 출처 명시 | add_evidence에 source_file·grade 강제 |
| #4 저자 작가성 | 중복 P-NNN 저자 묶음 *강제* — 자동 병합 영구 금지 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- forecast-registry 정합 (yaml.safe_load 회귀)
- 중복 0건 (모호 매칭은 저자 묶음)
- v1 R1 통과 (모든 P-NNN에 quantitative_anchor)
- 영속 자산 보호: forecast-registry write *부모 마스터 단일 진입* (PHASE3B_HANDOFF §8) — 본 sub는 SyncResult 산출만

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-collect-subs.md` §SUB 5
부모 마스터 SPEC: `specs/bookwriting-evidence-collect-master.md` §7 Step 6 + §12 Forecast Registry 동기화 가드 (중복 저자 묶음) + 부록 결정론 (M12)
저자 v1 R1: chapter-pipeline.md R1 quantitative_anchor 원문
결정론 모듈: `lib/forecast_registry_syncer.py` (M12)
영속 자산 보호: PHASE3B_HANDOFF §8 (forecast-registry write 부모 위임)
