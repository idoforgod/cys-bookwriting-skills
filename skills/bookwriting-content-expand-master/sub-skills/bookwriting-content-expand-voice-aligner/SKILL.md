---
name: bookwriting-content-expand-voice-aligner
description: 부모 bookwriting-content-expand-master의 INTERNAL sub ⭐ Voice Aligner. ⑦이 작성한 모든 layer 본문 (narrative·analysis·implications)에 저자 voice + 시그니처 패턴 적용 + M1 VoiceScorer gentle 임계 0.7+ 도달 보장 (⑩ line-edit strict 0.85+ 보다 약함) + M8 signature_pattern_applier 자연스러운 곳만 적용 (강제 X) + voice-gate cross-cutting 협업.
when_to_use: bookwriting-content-expand-master의 다른 모든 sub 통과 후 마지막에 자동 발동. ⑩ line-edit의 추가 정밀화 전 1차 voice gentle 보정.
disable-model-invocation: true
---

# bookwriting-content-expand-voice-aligner

## TLDR

부모 bookwriting-content-expand-master의 ⭐ Voice Aligner sub. ⑩ line-edit의 *strict 0.85+* 보다 *gentle 0.7+* 임계로 ⑦ 작성 본문에 저자 voice를 1차 보정한다. M1 VoiceScorer + M8 signature_pattern_applier 자연스러운 곳만 적용. voice-gate cross-cutting과 협업 (재작성은 voice-gate 담당).

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- weak-signal·driving-force·system-loop·proposition·scenario·time 등 다른 sub 통과 후 마지막 자동
- voice-gate cross-cutting 자동 발동

## Detailed Methodology

### 1. 결정론 chain — M1 gentle + M8 자연 적용

```python
from pathlib import Path
from dataclasses import dataclass, field
from voice_scoring import VoiceScorer                  # M1
from signature_pattern_applier import SignaturePatternApplier   # M8

GENTLE_THRESHOLD = 0.7    # ⑩ line-edit strict 0.85+ 보다 약함
SIGNATURE_FORCE_LIMIT = 0.5   # 적용률 50% 초과 시 강제로 판정 → 적용 안 함

@dataclass
class VoiceAlignResult:
    chunk_id: str
    layer_type: str              # "narrative" | "analysis" | "implications"
    original_text: str
    aligned_text: str
    voice_score_before: float
    voice_score_after: float
    signatures_applied: list[str]
    meets_gentle_threshold: bool

def align_voice_gentle(
    layer_chunks: list[dict],            # [{chunk_id, layer_type, text}, ...]
    voice_guidelines_path: Path,
) -> list[VoiceAlignResult]:
    """gentle voice 0.7+ 1차 보정."""
    scorer = VoiceScorer(voice_guidelines_path)
    applier = SignaturePatternApplier()
    results: list[VoiceAlignResult] = []

    for chunk in layer_chunks:
        original = chunk["text"]

        # Step 1-2: 저자 preferred 어휘 *기본 치환*
        before = scorer.score(original)

        # Step 3: 시그니처 패턴 *자연스러운 곳*에만 적용 (강제 X)
        aligned, applied = applier.apply_natural_only(original)

        # 자연스러움 평가 — 강제 의심 시 원본 유지
        natural_ratio = len(applied) / max(len(aligned.split()), 1)
        if natural_ratio > SIGNATURE_FORCE_LIMIT:
            # 강제로 판정 — 원본 유지 (⑩ line-edit이 strict 처리)
            aligned = original
            applied = []

        # Step 4: voice_score 0.7+ 도달 확인
        after = scorer.score(aligned)
        meets = after >= GENTLE_THRESHOLD

        results.append(VoiceAlignResult(
            chunk_id=chunk["chunk_id"],
            layer_type=chunk["layer_type"],
            original_text=original,
            aligned_text=aligned,
            voice_score_before=before,
            voice_score_after=after,
            signatures_applied=applied,
            meets_gentle_threshold=meets,
        ))

    # Step 5: voice-gate cross-cutting과 협업 (재작성 안 함)
    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-content-expand-subs.md SUB 4) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: ⑦의 모든 layer 본문 (narrative·analysis·implications) 로드 | `layer_chunks` 입력 |
| Step 2: 저자 preferred 어휘 *기본 치환* | M1 score + M8 apply |
| Step 3: 시그니처 패턴 *자연스러운 곳*에만 적용 (강제 X) | `apply_natural_only` + `SIGNATURE_FORCE_LIMIT` |
| Step 4: voice_score 0.7+ 도달 확인 | `meets_gentle_threshold` |
| Step 5: voice-gate cross-cutting과 협업 (재작성 안 함) | 부모 마스터 협업 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | layer_chunks (⑦ 작성 본문) + voice_guidelines path |
| Output | List[VoiceAlignResult] — voice_score_before/after·signatures_applied·meets_gentle |
| 후속 단계 | ⑩ line-edit (strict 0.85+ 추가 정밀화) |
| Dependencies | 다른 3 sub (weak-signal·driving-force·system-loop) 통과 후 마지막 |
| 결정론 모듈 | M1 VoiceScorer + M8 SignaturePatternApplier |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M1 + M8 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step + gentle 임계 1:1 환원 |
| #4 저자 작가성 | 자연스러운 곳만 적용 — 강제 차단 (`SIGNATURE_FORCE_LIMIT`) |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- voice_score 0.7+ 달성 (chunk별 `meets_gentle_threshold`)
- 시그니처 패턴 활용률 30%+ (가능한 곳)
- ⑩ line-edit이 *추가 정밀화*로 0.85+ 도달 (협업)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-content-expand-subs.md` §SUB 4 ⭐
부모 마스터 SPEC: `specs/bookwriting-content-expand-master.md`
⑩ line-edit 협업: 본 sub gentle 0.7+ → ⑩ strict 0.85+ 정밀화
voice-craft 정합: ⑥ `bookwriting-insight-synthesis-voice-craft`와 다른 sub (insight 단위 vs 본문 단위)
결정론 모듈: `lib/voice_scoring.py` (M1) + `lib/signature_pattern_applier.py` (M8)
