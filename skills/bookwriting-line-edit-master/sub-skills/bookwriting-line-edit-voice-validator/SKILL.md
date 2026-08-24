---
name: bookwriting-line-edit-voice-validator
description: 부모 bookwriting-line-edit-master의 INTERNAL sub. 앞 3 sub (vocabulary·signature·ai-tone) 통과 후 M1 VoiceScorer 재계산 + strict 임계 0.85+ 검증 + 미달 시 추가 첨삭 최대 2회 시도 + 최종 실패 시 저자 묶음 4 옵션 (직접 수정·원본 유지·defer·⑦ 재호출) + 시드 lifecycle INSIGHTED → POLISHED 진입 권장.
when_to_use: bookwriting-line-edit-master에서 ai-tone-purger 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-line-edit-voice-validator

## TLDR

부모 bookwriting-line-edit-master의 strict 검증 sub. M1 VoiceScorer 재계산으로 0.85+ 도달 확인 + 미달 시 최대 2회 추가 첨삭 시도 + 최종 실패 시 저자 묶음 4 옵션 escalate. 시드 lifecycle POLISHED 진입 권장.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- ai-tone-purger 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — M1 strict + 2회 재시도

```python
from enum import Enum
from pathlib import Path
from dataclasses import dataclass, field
from voice_scoring import VoiceScorer            # M1
from lifecycle_state_machine import LifecycleState   # M11

STRICT_THRESHOLD = 0.85
MAX_RETRIES = 2

class VoiceFallbackOption(str, Enum):
    DIRECT_FIX = "direct_fix"            # 저자 직접 수정
    KEEP_ORIGINAL = "keep_original"      # 원본 유지 (위반 수용)
    DEFER = "defer"
    REINVOKE_CONTENT_EXPAND = "reinvoke_content_expand"   # ⑦ 재호출

@dataclass
class VoiceValidationResult:
    section_id: str
    voice_score: float
    meets_strict_threshold: bool
    retries_attempted: int
    needs_bundle_escalation: bool
    bundle_options: list[VoiceFallbackOption] = field(default_factory=lambda: list(VoiceFallbackOption))
    lifecycle_transition_recommended: str | None = None   # "INSIGHTED → POLISHED"

def validate_voice_strict(
    sections: list[dict],
    voice_guidelines_path: Path,
) -> list[VoiceValidationResult]:
    """strict 0.85+ 검증 + 2회 재시도 + 저자 묶음."""
    scorer = VoiceScorer(voice_guidelines_path)
    results: list[VoiceValidationResult] = []

    for sec in sections:
        text = sec["text"]

        # Step 1: 본문 voice_score 재계산 (5 가중치)
        score = scorer.score(text)

        retries = 0
        meets = score >= STRICT_THRESHOLD

        # Step 3: < 0.85 → 추가 첨삭 시도 (최대 2회)
        # — 본 sub는 시도 *권장*만, 실제 재첨삭은 부모 마스터가 vocabulary/signature/ai-tone 재호출
        if not meets:
            retries = MAX_RETRIES   # 부모가 2회 재시도 트리거
            # 부모 마스터가 재시도 후 본 sub 재호출 → score 재측정

        meets = score >= STRICT_THRESHOLD
        needs_bundle = not meets
        lifecycle_rec = "INSIGHTED → POLISHED" if meets else None

        results.append(VoiceValidationResult(
            section_id=sec["section_id"],
            voice_score=score,
            meets_strict_threshold=meets,
            retries_attempted=retries,
            needs_bundle_escalation=needs_bundle,
            lifecycle_transition_recommended=lifecycle_rec,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-line-edit-subs.md SUB 4)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 본문 voice_score 재계산 (5 가중치) | M1 `scorer.score()` |
| Step 2: ≥ 0.85 → 통과 → 시드 lifecycle POLISHED 진입 권장 | `meets_strict_threshold` + `lifecycle_transition_recommended` |
| Step 3: < 0.85 → 추가 첨삭 최대 2회 | `MAX_RETRIES = 2` |
| Step 4: 저자 묶음 escalate (직접 수정·원본 유지·defer·⑦ 재호출) | `VoiceFallbackOption` 4 enum |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | sections (ai-tone-purger 통과) + voice_guidelines path |
| Output | List[VoiceValidationResult] — voice_score·meets·retries·escalation |
| 후속 sub | sentence-rhythm-tuner 또는 diff-preserver |
| Dependencies | ai-tone-purger 통과 |
| 결정론 모듈 | M1 VoiceScorer + M11 LifecycleState |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M1 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step + 4 옵션 1:1 |
| #4 저자 작가성 | 저자 묶음 강제 — 자동 결정 영구 금지 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- voice_score 0.85+ 달성
- 시드 lifecycle INSIGHTED → POLISHED 진입 권장
- 저자 책 *문장 미시 품질 보장*

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-line-edit-subs.md` §SUB 4
부모 마스터 SPEC: `specs/bookwriting-line-edit-master.md`
결정론 모듈: `lib/voice_scoring.py` (M1) + `lib/lifecycle_state_machine.py` (M11)
⑦ content-expand-voice-aligner 0.7+ → 본 sub 0.85+ (strict 정밀화)
