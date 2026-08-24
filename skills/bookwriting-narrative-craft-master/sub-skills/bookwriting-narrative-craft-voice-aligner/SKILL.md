---
name: bookwriting-narrative-craft-voice-aligner
description: 부모 bookwriting-narrative-craft-master의 INTERNAL sub. 1층 narrative 본문에 저자 voice 정밀 적용 + M1 VoiceScorer + M8 시그니처 + preferred 어휘 치환 + voice_score 0.7+ 도달 + voice-gate cross-cutting 자동. ⑩ line-edit과 협업 (strict 0.85+).
when_to_use: bookwriting-narrative-craft-master에서 sensory-detail-adder 통과 후 마지막 자동 호출 (narrative-craft의 마지막 sub).
disable-model-invocation: true
---

# bookwriting-narrative-craft-voice-aligner

## TLDR

부모 bookwriting-narrative-craft-master의 마지막 sub. 1층 narrative 본문에 저자 voice·시그니처·preferred 어휘를 M1 + M8 결정론 적용하고 voice_score 0.7+ 도달을 강제한다. voice-gate cross-cutting 자동 발동. ⑩ line-edit의 strict 0.85+ 정밀화 전 1차 보정.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- sensory-detail-adder 통과 후 자동 (narrative-craft 마지막 sub)
- ⑦ content-expand-voice-aligner와 다른 sub (narrative-craft 1층 vs content-expand 2층)

## Detailed Methodology

### 1. 결정론 chain — M1 + M8 1층 narrative

```python
from pathlib import Path
from dataclasses import dataclass, field
from voice_scoring import VoiceScorer                  # M1
from signature_pattern_applier import SignaturePatternApplier   # M8

NARRATIVE_THRESHOLD = 0.7   # ⑩ line-edit strict 0.85+ 보다 약함

@dataclass
class NarrativeVoiceResult:
    section_id: str
    original_text: str
    aligned_text: str
    voice_score_before: float
    voice_score_after: float
    signatures_used: list[str]
    meets_narrative_threshold: bool

def align_narrative_voice(
    sections: list[dict],          # 1층 narrative 본문 chunks
    voice_guidelines_path: Path,
) -> list[NarrativeVoiceResult]:
    """1층 narrative voice 정밀 적용."""
    scorer = VoiceScorer(voice_guidelines_path)
    applier = SignaturePatternApplier()
    results: list[NarrativeVoiceResult] = []

    for sec in sections:
        original = sec["text"]
        before = scorer.score(original)

        # 1층 narrative는 *서사적 voice* — 시그니처 자연 적용 우선
        aligned, applied = applier.apply_natural_only(original)
        after = scorer.score(aligned)

        results.append(NarrativeVoiceResult(
            section_id=sec["section_id"],
            original_text=original,
            aligned_text=aligned,
            voice_score_before=before,
            voice_score_after=after,
            signatures_used=applied,
            meets_narrative_threshold=after >= NARRATIVE_THRESHOLD,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-narrative-craft-subs.md SUB 7)

| 명세 항목 | 본 sub 구현 |
|---|---|
| 1층 본문에 저자 voice·시그니처·preferred 어휘 적용 | M1 + M8 결합 |
| voice_score 0.7+ 도달 | `NARRATIVE_THRESHOLD = 0.7` |
| voice gate cross-cutting 통과 | 부모 cross-cutting |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | sections + voice_guidelines path |
| Output | List[NarrativeVoiceResult] — voice_score_before/after·signatures·meets |
| 후속 단계 | ⑩ line-edit (strict 0.85+ 정밀화) |
| Dependencies | sensory-detail-adder 통과 |
| 결정론 모듈 | M1 VoiceScorer + M8 SignaturePatternApplier |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M1 + M8 결정론 |
| #2 grill-me 원문 일치 | 명세 3 항목 1:1 |
| #4 저자 작가성 | 1층 narrative는 저자 *서사적 voice* |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- voice_score 0.7+ (`meets_narrative_threshold`)
- 시그니처 활용 (`signatures_used`)
- voice gate cross-cutting 통과

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-narrative-craft-subs.md` §SUB 7
부모 마스터 SPEC: `specs/bookwriting-narrative-craft-master.md`
⑩ line-edit 협업: 본 sub 0.7+ → ⑩ strict 0.85+
⑦ content-expand-voice-aligner 정합: 2층 vs 1층 (다른 영역)
결정론 모듈: `lib/voice_scoring.py` (M1) + `lib/signature_pattern_applier.py` (M8)
