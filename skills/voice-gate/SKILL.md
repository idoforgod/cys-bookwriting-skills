---
name: voice-gate
description: 저자 voice·통찰·문장 패턴 cross-cutting 가드. 모든 단계 마스터 출력에 자동 발동. M1 VoiceScorer 결정론 호출 — LLM 추론 영구 금지. 임계 0.7+ 미달 시 1회 재작성·실패 시 저자 묶음. 저자 진북 #4 (작가성·정체성) backbone.
when_to_use: 모든 단계 마스터 (① absorb ~ ⑪ cross-chapter-relink) 출력 직후 자동. 저자 명시 `/voice-gate verify <text>` 호출도 가능.
---

# voice-gate (cross-cutting 메타 가드)

## TLDR

저자 voice 6 가중치 결정론 검증 — `lib/voice_scoring.VoiceScorer.compute_voice_score()` 호출. 임계 0.7+ 미달 시 1회 재작성 시도 → 실패 시 저자 묶음 escalate.

## Triggers

- 모든 단계 마스터 출력 직후 *자동 발동* (cross-cutting)
- `/voice-gate verify "<text>"` — 단일 텍스트 voice_score 즉시 계산
- `/voice-gate audit <chapter>` — 챕터 전체 voice 감사

## Detailed Methodology

### 1. 결정론 호출 (LLM 추론 영구 금지)

```python
import paths
from voice_scoring import VoiceScorer
import yaml

with open(paths.book_config_path()) as f:
    config = yaml.safe_load(f.read())

scorer = VoiceScorer(voice_guidelines=config["voice_guidelines"])
breakdown = scorer.compute_voice_score(output_text)

if breakdown.weighted_total < 0.7:
    # 재작성 1회 시도 (signature 적용·preferred 치환)
    ...
```

### 2. 6 가중치 (합 = 1.00, pytest 검증 완료)

| 가중치 | 값 | 측정 |
|---|---|---|
| vocabulary_match | 0.27 | preferred·avoid substring |
| sentence_rhythm | 0.18 | 평균 길이·max 위반 |
| structure_pattern | 0.18 | 명제→근거→사례→통찰 |
| signature_presence | 0.14 | 5 시그니처 정규식 |
| prohibition_avoidance | 0.13 | PROH-001~005 |
| meaning_score | 0.10 | 저자 사상적 척추 4개 |

### 3. 저자 5 시그니처 패턴 (Round 4·6 수정 정규식)

1. `(.+?)가 아니라\s*(.+?)(다|이다|입니다)` — "AGI는 도구가 아니라 메타도구다"
2. `이 책은\s*(.+?)\s*아니라\s*(.+?)\s*(다룬다|쓰는)` — 도입부
3. `셋 중 하나(를|만)?\s*(선택|아니)` — 결론
4. `(.+?)와\s*(.+?)\s*사이의\s*거리` — 시간·공간 좌표
5. `(두|세|N|\d+|다섯)\s*(창업자|발언자|사람).*정확히\s*같은\s*\d+\s*(배|년)` — 수렴

### 4. 위반 시 처리

- voice_score < 0.7 → 재작성 1회 → 실패 시 저자 묶음
- ⑩ line-edit-master 전용: strict 임계 0.85+

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #4 작가성·정체성 | ✅ M1 결정론 + 5 시그니처 정규식 |
| #7 결정론 환원 | ✅ pytest 통과 (signature·preferred·weights sum 1.0) |

## 출처

SPEC: `specs/voice-gate.md` (17 항목 풀 + 부록 G·H)
실행 모듈: `lib/voice_scoring.py`
설정: `book-config.yaml::voice_guidelines`
