---
name: bookwriting-line-edit-ai-tone-purger
description: 부모 bookwriting-line-edit-master의 INTERNAL sub ⭐ AI 어투 자동 감지·제거. M9 AiTonePurger로 기성 AI 패턴 (PROH-005 — "물론, 이는 매우 중요"·"다음과 같이 살펴볼"·"여러분도 동의" 등) 결정론 감지 + 저자 voice 자동 치환 + PROH-005 위반 0건 강제.
when_to_use: bookwriting-line-edit-master에서 signature-applier 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-line-edit-ai-tone-purger

## TLDR

부모 bookwriting-line-edit-master의 ⭐ AI 어투 제거 sub. M9 AiTonePurger로 기성 AI 패턴 (PROH-005)을 결정론 감지하고 저자 voice로 자동 치환한다. 책 *AI 어투 0건* 목표.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- signature-applier 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — M9 AiTonePurger

```python
import re
from dataclasses import dataclass, field
from ai_tone_purger import AiTonePurger   # M9

@dataclass
class AiTonePurgeResult:
    section_id: str
    original_text: str
    purged_text: str
    detected_patterns: list[str]    # 감지된 AI 어투 패턴
    purged_count: int               # 제거 횟수
    proh_005_count: int             # PROH-005 위반 (제거 후 잔여)

# 기성 AI 패턴 풀 (PROH-005)
AI_TONE_PATTERNS = [
    re.compile(r"물론[\s,，]\s*이는?\s*(?:매우|아주|상당히)?\s*중요한?\s*(?:질문|점|문제)"),
    re.compile(r"다음과\s*같이\s*살펴볼?\s*수\s*있"),
    re.compile(r"이러한\s*점들?을?\s*고려할?\s*때"),
    re.compile(r"결론적으로\s*말하자면"),
    re.compile(r"여러분도?\s*동의(?:하실|하시는)?\s*것"),
    re.compile(r"흥미롭게도"),
    re.compile(r"주목할\s*점은"),
]

def purge_ai_tone(sections: list[dict]) -> list[AiTonePurgeResult]:
    """M9 AI 어투 결정론 감지·제거."""
    purger = AiTonePurger()
    results: list[AiTonePurgeResult] = []

    for sec in sections:
        original = sec["text"]

        # Step 1: AI 어투 패턴 감지
        detected: list[str] = []
        for pat in AI_TONE_PATTERNS:
            for m in pat.finditer(original):
                detected.append(m.group(0))

        # Step 2: 감지 빈도 카운트 + Step 3: 저자 voice로 자동 치환
        purged_text, purged_count = purger.purge_all(original)

        # Step 4: PROH-005 위반 0건 도달 확인 (잔여 패턴)
        proh_005_remaining = sum(1 for pat in AI_TONE_PATTERNS for _ in pat.finditer(purged_text))

        results.append(AiTonePurgeResult(
            section_id=sec["section_id"],
            original_text=original,
            purged_text=purged_text,
            detected_patterns=detected,
            purged_count=purged_count,
            proh_005_count=proh_005_remaining,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-line-edit-subs.md SUB 3) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: AI 어투 패턴 감지 ("물론·다음과 같이·이러한 점들·결론적으로·여러분도") | `AI_TONE_PATTERNS` 7 정규식 |
| Step 2: 감지 빈도 카운트 | `detected` 리스트 |
| Step 3: 저자 voice로 자동 치환 | M9 `purger.purge_all()` |
| Step 4: PROH-005 위반 0건 도달 | `proh_005_count == 0` 검증 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | sections (signature-applier 통과) |
| Output | List[AiTonePurgeResult] — detected·purged·proh_005_count |
| 후속 sub | voice-validator |
| Dependencies | signature-applier 통과 |
| 결정론 모듈 | M9 AiTonePurger + 자체 정규식 7 패턴 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M9 + 정규식 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step + 7 패턴 1:1 |
| #4 저자 작가성 ⭐ | AI 어투 0건 — 저자 voice backbone |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- PROH-005 위반 0건 (`proh_005_count == 0`)
- 저자 voice로 자연스러운 치환
- 본문 *AI 어투 0건* 검증

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-line-edit-subs.md` §SUB 3 ⭐
부모 마스터 SPEC: `specs/bookwriting-line-edit-master.md`
결정론 모듈: `lib/ai_tone_purger.py` (M9)
PROH-005: 기성 AI 어투 prohibition
