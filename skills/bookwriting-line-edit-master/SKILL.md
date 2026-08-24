---
name: bookwriting-line-edit-master
description: 저자 책 ⑩ 단계 마스터 — 문장 단위 결정론 첨삭. M9 AITonePurger + M1 VoiceScorer ≥0.85 (POLISHED 임계) + M8 시그니처 균형 + M2 HallucinationDetector 0건 + M15 TraumaWitnessDetector. INSIGHTED → POLISHED 최종 게이트.
when_to_use: "`/bookwriting cycle` Step 10 자동. `/bookwriting-line-edit <chapter_id>` 단독 호출."
---

# bookwriting-line-edit-master (⑩ 단계 마스터)

## TLDR

문장 단위 결정론 첨삭. AI 어조 0건 + voice ≥0.85 + 시그니처 균형 + Hallucination 0건 + trauma 보호 → POLISHED 진입.

## Triggers

- `/bookwriting cycle <target>` Step 10 자동
- `/bookwriting-line-edit <chapter_id>` — 저자 직접
- `/bookwriting-line-edit ai-purge <draft>` — M9만
- `/bookwriting-line-edit trauma-check <draft>` — M15만

## Detailed Methodology

### 1. 결정론 chain

```python
from ai_tone_purger import AITonePurger
from voice_scoring import VoiceScorer
from signature_pattern_applier import SignaturePatternApplier
from citation_detection import HallucinationDetector
from trauma_witness_detector import TraumaWitnessDetector
from lifecycle_state_machine import LifecycleStateMachine, LifecycleState

# Step 1: M9 AI 어조 청소 (Korean + English 패턴)
purger = AITonePurger()
violations_ko = purger.detect(draft, language="ko")
violations_en = purger.detect(draft, language="en")
if violations_ko or violations_en:
    cleaned = purger.purge(draft)
else:
    cleaned = draft

# Step 2: M1 voice score ≥0.85 (POLISHED 임계 — ⑦ content-expand의 0.70보다 엄격)
scorer = VoiceScorer(profile_path=".../voice_profile.yaml")
voice_score = scorer.score(cleaned)
if voice_score["weighted_total"] < 0.85:
    return {"action": "fail_voice_polished", "score": voice_score, "required": 0.85}

# Step 3: M8 시그니처 균형 — [2, 7] 범위
applier = SignaturePatternApplier()
sig_count = applier.count_in_draft(cleaned)
if not (2 <= sig_count <= 7):
    return {"action": "fail_signature_distribution", "count": sig_count}

# Step 4: M2 HallucinationDetector — 5 signals 모두 0
detector = HallucinationDetector()
signals = detector.detect_signals(text=cleaned)
if signals["any_critical"]:
    return {"action": "fail_hallucination", "signals": signals}

# Step 5: M15 TraumaWitnessDetector — 6 카테고리 보호 정책 강제
trauma_detector = TraumaWitnessDetector()
trauma_result = trauma_detector.assess(cleaned)
if trauma_result["trauma_detected"]:
    # Safe Messaging Gatekeeper 자동 발동
    if not trauma_result["actions_required"]["consent_verification"]:
        return {"action": "fail_trauma_consent", "details": trauma_result}

# Step 6: lifecycle INSIGHTED → POLISHED 결정론 전환 (M11 STAGE_TO_TRANSITION line_edit)
fsm = LifecycleStateMachine()
new_state = fsm.transition(LifecycleState.INSIGHTED, LifecycleState.POLISHED)
```

### 2. POLISHED 진입 임계 매트릭스

| 검사 | 임계 |
|---|---|
| voice_score weighted_total | ≥ 0.85 |
| AI 어조 violations (ko + en) | == 0 |
| 시그니처 분포 | [2, 7] |
| HallucinationDetector | any_critical == False |
| trauma 검출 시 consent_verification | == True |

### 3. 문장 단위 세부 첨삭 규칙

| 규칙 | 결정론 모듈 |
|---|---|
| 저자 단정형 강제 ("입니다" → "다") | M9 정규식 |
| "매우·다소·꽤" 과다 부사 제거 | M9 |
| 저자 5 시그니처 분포 균형 | M8 |
| 정량 앵커 누락 시 저자 escalate | M4 |
| 외래어 한자어 균형 (저자 voice profile) | M1 |

### 4. trauma 본문 처리 우선순위

trauma 검출 시 line-edit *건너뛰지 않고* M15 보호 정책을 line-edit 전에 강제 발동. 저자 6 보호 정책 적용 후에만 line-edit 진입 허용.

### 5. lifecycle 전환

```python
# INSIGHTED → POLISHED (Round 18 STAGE_TO_TRANSITION line_edit)
# 단행본 최종 단계 — POLISHED는 terminal state
```

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ M2 5 signals 모두 0 강제 |
| #4 저자 작가성·정체성 | ✅ M1 ≥0.85 (3주차 0.70보다 엄격) |
| #6 정신건강·취약 독자 보호 | ✅ M15 6 카테고리 자동 검출 + 보호 정책 |
| #7 결정론 환원 | ✅ M9·M1·M8·M2·M15·M11 pure Python |

## 출처

SPEC: `specs/bookwriting-line-edit-master.md`
실행 모듈: `lib/ai_tone_purger.py` + `lib/voice_scoring.py` + `lib/signature_pattern_applier.py` + `lib/citation_detection.py` + `lib/trauma_witness_detector.py` + `lib/lifecycle_state_machine.py`

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 6개 sub-skill을 자동 orchestration — 저자 voice strict 0.85+ backbone.

| 순서 | Sub-skill | 호출 시점 | 페르소나 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-line-edit-vocabulary-refiner` | Step 1 | Vocabulary Refiner | yaml + 정규식 + 외국어 dict |
| 2 | `bookwriting-line-edit-signature-applier` ⭐ | Step 2 | Signature Applier | M8 SignaturePatternApplier (35%+) |
| 3 | `bookwriting-line-edit-ai-tone-purger` ⭐ | Step 3 | AI Tone Purger | M9 AiTonePurger + 7 PROH-005 정규식 |
| 4 | `bookwriting-line-edit-voice-validator` ⭐ | Step 4 | Voice Validator | M1 VoiceScorer strict 0.85+ + 2회 재시도 |
| 5 | `bookwriting-line-edit-sentence-rhythm-tuner` | Step 5 | Sentence Rhythm Tuner | 정규식 50자±10 + 능동태 |
| 6 | `bookwriting-line-edit-diff-preserver` | Step 6 | Diff Preserver | shutil + .before 백업 |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-line-edit cycle <chapter>
↓ Step 1
bookwriting-line-edit-vocabulary-refiner (preferred·avoid·외국어 PROH-001 0건)
↓ Step 2
bookwriting-line-edit-signature-applier ⭐ (5 시그니처 strict 35%+ 자연 적용)
↓ Step 3
bookwriting-line-edit-ai-tone-purger ⭐ (PROH-005 0건 — 물론·다음과 같이·이러한 점들·결론적으로 등)
↓ Step 4
bookwriting-line-edit-voice-validator ⭐ (M1 strict 0.85+ — 미달 시 2회 재시도)
↓ Step 5
bookwriting-line-edit-sentence-rhythm-tuner (50자±10·max 80자·능동태·저자 리듬 3박자)
↓ Step 6
bookwriting-line-edit-diff-preserver (.before 백업 + cycle-registry.outputs.line_edit_diffs)
↓
Master Synthesis: chapters/<ch>/{narrative,analysis,implications}.md voice 0.85+ + lifecycle INSIGHTED→POLISHED 권장
```

### 저자 결정 묶음 강제
- Voice Validator 2회 재시도 후 0.85+ 미달 시 저자 묶음 4 옵션 (직접 수정·원본 유지·defer·⑦ 재호출)
- Diff Preserver `/bookwriting-line-edit revert` 명령으로 저자 원복 가능

### OrchestratorTracer (M18) 자동 기록
deterministic_modules_used 누적: M1·M8·M9·M11 + 자체 정규식. 저자 voice backbone 완성 단계.

### PROH-006 마크다운 기호 집행 책임 (2026-05-25 신설 — 9번째 절대 protocol)

본 마스터가 PROH-006 마크다운 기호 금지 정책의 집행 책임을 맡는다 (book-config :: voice_guidelines.prohibitions[PROH-006] severity critical).

마크다운 검출 정규식 7종 (결정론):
- heading `^#{1,6}\s+`
- bold `\*\*.+?\*\*` (DOTALL)
- italic `(?<!\*)\*(?!\*).+?\*(?!\*)`
- blockquote `^>\s?`
- bullet `^\s*[-*]\s+`
- hr `^---+$`
- code fence ` ^``` `

변환 규칙 (voice 보존):
- 헤더 `## 1. X` → `1. X` (한글 번호만 유지)
- bold/italic → plain text (강조는 줄바꿈+들여쓰기 또는 한국어 인용부호)
- blockquote `>` → 제거 (들여쓰기로)
- bullet `-/*` → 제거 (들여쓰기 유지)
- hr `---` → 빈 줄
- code fence ` ``` ` → 제거 (ASCII diagram 내용 보존)

예외: 표 `| ... |`는 단행본 시각 구조 유지.

집행 시점:
- Step 6 (sentence-rhythm-tuner) 직후 자동 발동
- 위반 발견 시 즉시 strip + .before 백업
- voice 손상 0.05+ 시 저자 묶음 (변환 vs 원본)
- 통과 조건: markdown_violation_count == 0 (표 제외)
