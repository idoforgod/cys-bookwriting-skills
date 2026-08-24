---
name: bookwriting-insight-synthesis-voice-craft
description: 부모 bookwriting-insight-synthesis-master의 INTERNAL sub ⭐ Voice Aligner 페르소나. 선별 통찰 후보를 저자 voice + 시그니처 5 패턴으로 재표현 + M1 VoiceScorer 0.7+ 보장 + M8 signature_pattern_applier 활용 + voice-gate cross-cutting 자동 + < 0.7 시 1회 재시도 후 저자 묶음 escalate.
when_to_use: bookwriting-insight-synthesis-master에서 triad-evaluation 통과 ★ 추천 통찰만 자동 호출. `/bookwriting-insight-synthesis voice-craft <insight-id>` 모드는 본 sub 단독.
disable-model-invocation: true
---

# bookwriting-insight-synthesis-voice-craft

## TLDR

부모 bookwriting-insight-synthesis-master의 ⭐ Voice Aligner sub. 저자 정체성 보호의 최후 페르소나. ★ 추천 통찰을 M1 VoiceScorer 0.7+ 도달까지 M8 signature_pattern_applier로 저자 시그니처 5 패턴 (X가 아니라 Y·셋 중 하나 아니다·X와 Y 사이 거리·두 창업자 N배·변수 X 따라 결과 갈리는) 적용한다. 1회 재시도 후에도 < 0.7이면 저자 묶음 escalate.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- triad-evaluation 통과 ★ 추천 통찰만 → 본 sub 자동
- `/bookwriting-insight-synthesis voice-craft <insight-id>` 모드는 본 sub 단독
- voice-gate cross-cutting 자동 발동

## Detailed Methodology

### 1. 결정론 chain — M1 + M8 + 1회 재시도

```python
from pathlib import Path
from dataclasses import dataclass, field
from voice_scoring import VoiceScorer                  # M1
from signature_pattern_applier import SignaturePatternApplier   # M8

@dataclass
class VoiceCraftResult:
    insight_id: str
    original_text: str
    crafted_text: str
    voice_score_before: float
    voice_score_after: float
    signatures_applied: list[str] = field(default_factory=list)
    retry_attempted: bool = False
    needs_bundle_escalation: bool = False
    bundle_reason: str | None = None

def craft_voice(
    insights: list,                  # ★ 추천 통찰만
    voice_guidelines_path: Path,
) -> list[VoiceCraftResult]:
    """Voice 0.7+ 도달까지 시그니처 적용 + 1회 재시도."""
    scorer = VoiceScorer(voice_guidelines_path)
    applier = SignaturePatternApplier()
    results: list[VoiceCraftResult] = []

    for ins in insights:
        original = ins.text

        # Step 1-2: Voice Aligner 페르소나 발동
        # 저자 preferred 어휘 치환 + 5 시그니처 패턴 적용 시도
        before_score = scorer.score(original)

        crafted, applied = applier.apply_all(original)

        # Step 3: voice_score 재계산
        after_score = scorer.score(crafted)

        retry = False
        needs_bundle = False
        reason = None

        # Step 4: < 0.7 → 1회 재시도
        if after_score < 0.7:
            retry = True
            # 재시도 — 다른 시그니처 우선순위
            crafted, applied = applier.apply_with_emphasis(original, emphasis=["X_NOT_Y", "TWO_FOUNDERS"])
            after_score = scorer.score(crafted)

            # Step 5: 여전히 < 0.7 → 저자 묶음 escalate
            if after_score < 0.7:
                needs_bundle = True
                reason = f"voice_score {after_score:.2f} < 0.7 (1회 재시도 후) — 저자 재표현 옵션 필요"

        results.append(VoiceCraftResult(
            insight_id=ins.insight_id,
            original_text=original,
            crafted_text=crafted,
            voice_score_before=before_score,
            voice_score_after=after_score,
            signatures_applied=applied,
            retry_attempted=retry,
            needs_bundle_escalation=needs_bundle,
            bundle_reason=reason,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-insight-synthesis-subs.md SUB 3) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 통찰 후보 텍스트 로드 | `original = ins.text` |
| Step 2: Voice Aligner 페르소나 발동 (preferred 어휘 + 5 시그니처) | M1 score + M8 `applier.apply_all()` |
| Step 3: voice_score 재계산 | `scorer.score(crafted)` |
| Step 4: < 0.7 → 1회 재시도 | `if after_score < 0.7: retry` + `apply_with_emphasis` |
| Step 5: 여전히 < 0.7 → 저자 묶음 escalate | `needs_bundle_escalation=True` + reason |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | insights (★ 추천 통찰) + voice_guidelines path (book-config) |
| Output | List[VoiceCraftResult] — voice_score_before/after·signatures_applied·retry·escalation |
| 후속 sub | `bookwriting-insight-synthesis-bundle-builder` |
| Dependencies | triad-evaluation 통과 (★ 추천 통찰만) + voice-gate cross-cutting |
| 결정론 모듈 | M1 VoiceScorer + M8 SignaturePatternApplier |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M1 + M8 결정론 점수 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 + 5 시그니처 패턴 원문 |
| #4 저자 작가성 ⭐ | 저자 정체성 보호 최후 페르소나 — Voice Aligner |
| #7 결정론 환원 | 100% 결정론 (1회 재시도도 결정론 패턴 우선순위) |

### 5. Verification (명세 §7)

- ★ 추천 통찰 모두 voice_score 0.7+ 도달 (또는 저자 묶음 escalate)
- 시그니처 패턴 활용률 30%+ (부모 §10 정성)
- 재작성 1회 시도 후 실패 시 저자 묶음 (자동 결정 영구 금지)
- 부모 §15 G5 — 모든 통찰 voice_score ≥ 0.7

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-insight-synthesis-subs.md` §SUB 3 ⭐
부모 마스터 SPEC: `specs/bookwriting-insight-synthesis-master.md` §13 페르소나 7 Voice Aligner ⭐ + §15 G5 + 부록 E (M1·M8)
저자 시그니처 5 패턴: 부모 §3 Voice 보존 (X가 아니라 Y·셋 중 하나 아니다·X와 Y 사이 거리·두 창업자 N배·변수 X 따라 결과 갈리는)
결정론 모듈: `lib/voice_scoring.py` (M1) + `lib/signature_pattern_applier.py` (M8)
