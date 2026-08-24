---
name: bookwriting-structure-review-r5-verifier
description: 부모 bookwriting-structure-review-master의 INTERNAL sub. 저자 v1 R5 — forecast-registry의 P-NNN 중 챕터 사용분 식별 + verification_signal·falsifies_if 필드 결정론 확인 + 누락 시 저자 알림 + ④ verification-signal-finder 재호출 권장.
when_to_use: bookwriting-structure-review-master에서 r4-distribution-analyzer 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-structure-review-r5-verifier

## TLDR

부모 bookwriting-structure-review-master의 저자 v1 R5 검증 sub. 챕터에서 사용된 P-NNN을 forecast-registry에서 식별하고 각 P-NNN의 verification_signal·falsifies_if 필드 누락을 결정론 검출한다. 누락 시 ④ verification-signal-finder 재호출 권장.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- r4-distribution-analyzer 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — P-NNN 식별 + R5 필드 확인

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class R5VerificationResult:
    chapter_id: str
    used_predictions: list[str]              # 챕터에서 사용된 P-NNN
    missing_verification_signal: list[str]   # verification_signal 누락 P-NNN
    missing_falsifies_if: list[str]          # falsifies_if 누락 P-NNN
    recommend_resignal_call: bool            # ④ verification-signal-finder 재호출 권장

def verify_r5(
    chapter_id: str,
    chapter_dir: Path,
    forecast_registry_path: Path,
) -> R5VerificationResult:
    """R5 verification_signal·falsifies_if 결정론 검증."""
    # Step 1: forecast-registry의 P-NNN 중 *챕터 사용분* 식별
    if not forecast_registry_path.exists():
        return R5VerificationResult(
            chapter_id=chapter_id, used_predictions=[],
            missing_verification_signal=[], missing_falsifies_if=[],
            recommend_resignal_call=False,
        )

    with forecast_registry_path.open(encoding="utf-8") as f:
        forecast = yaml.safe_load(f) or {}

    # evidence-track.yaml에서 챕터 P-NNN 사용분 추출
    evidence_track_path = chapter_dir / "evidence-track.yaml"
    used_pnnns: list[str] = []
    if evidence_track_path.exists():
        with evidence_track_path.open(encoding="utf-8") as f:
            track = yaml.safe_load(f) or {}
        for ev in track.get("evidence", []):
            pnnn = ev.get("p_nnn") or ev.get("prediction_id")
            if pnnn:
                used_pnnns.append(pnnn)

    # Step 2: 각 P-NNN의 verification_signal·falsifies_if 필드 확인
    missing_vs: list[str] = []
    missing_ff: list[str] = []
    predictions_dict = {p.get("id"): p for p in forecast.get("predictions", [])}
    for pnnn in set(used_pnnns):
        p = predictions_dict.get(pnnn)
        if not p:
            continue
        if not p.get("verification_signal"):
            missing_vs.append(pnnn)
        if not p.get("falsifies_if"):
            missing_ff.append(pnnn)

    # Step 3: 누락 시 저자 알림 + ④ verification-signal-finder 재호출 권장
    recommend_resignal = bool(missing_vs) or bool(missing_ff)

    return R5VerificationResult(
        chapter_id=chapter_id,
        used_predictions=list(set(used_pnnns)),
        missing_verification_signal=missing_vs,
        missing_falsifies_if=missing_ff,
        recommend_resignal_call=recommend_resignal,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-structure-review-subs.md SUB 6)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: forecast-registry의 P-NNN 중 *챕터 사용분* 식별 | evidence-track의 p_nnn 추출 |
| Step 2: 각 P-NNN의 verification_signal·falsifies_if 필드 확인 | `missing_vs`·`missing_ff` |
| Step 3: 누락 시 저자 알림 + ④ verification-signal-finder 재호출 권장 | `recommend_resignal_call` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + chapter_dir + forecast_registry_path |
| Output | R5VerificationResult — used_predictions·missing 2종·recommend_resignal |
| 후속 sub | resize-recommender |
| Dependencies | r4-distribution-analyzer 통과 |
| 결정론 모듈 | yaml.safe_load + dict lookup |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | yaml + dict 결정론 |
| #2 grill-me 원문 일치 | 명세 3 Step 1:1 |
| #7 결정론 환원 | 100% 결정론 |
| R5 강제 | 저자 v1 chapter-pipeline.md R5 양식 정합 |

### 5. Verification (명세 §5)

- 저자 v1 R5 정합 (forecast-registry verification_signal·falsifies_if)
- 누락 검출 (`missing_vs`·`missing_ff`)
- ④ verification-signal-finder 재호출 권장 시점 정확

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-structure-review-subs.md` §SUB 6
부모 마스터 SPEC: `specs/bookwriting-structure-review-master.md`
④ verification-signal-finder 정합: `bookwriting-evidence-collect-verification-signal-finder`
저자 v1 R5: chapter-pipeline.md
영속 자산 보호: PHASE3B_HANDOFF §8 (forecast-registry read-only)
