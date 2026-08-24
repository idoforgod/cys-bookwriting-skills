---
name: bookwriting-narrative-craft-master
description: 저자 책 ⑧ 단계 마스터 — INSIGHTED 절·소절을 저자 narrative 결정론 조립. 1층 콜드오픈 13%·2층 분석 65%·3층 함의 22% 비율 강제 (M5) + 저자 5 시그니처 분포 균형 (M8) + voice_score ≥0.70 + AI 어조 0건. trauma_bearing_witness 6 카테고리 원문 인용 보호.
when_to_use: "`/bookwriting cycle` Step 8 자동. `/bookwriting-narrative-craft <seed_id>` 단독 호출 가능."
---

# bookwriting-narrative-craft-master (⑧ 단계 마스터)

## TLDR

INSIGHTED 절들을 단행본 narrative로 조립. 1·2·3층 13/65/22 비율·시그니처 분포·voice 점수 결정론 게이트.

## Triggers

- `/bookwriting cycle <target>` Step 8 자동
- `/bookwriting-narrative-craft <seed_id>` — 저자 직접
- `/bookwriting-narrative-craft cold-open <chapter_id>` — 1층 콜드오픈만
- `/bookwriting-narrative-craft trauma-witness <claim_id>` — 트라우마 증언 원문 보호 처리만

## Detailed Methodology

### 1. 결정론 chain

```python
from layer_ratio_measurer import LayerRatioMeasurer
from signature_pattern_applier import SignaturePatternApplier
from ai_tone_purger import AITonePurger
from voice_scoring import VoiceScorer
from lifecycle_state_machine import LifecycleStateMachine, LifecycleState

# Step 1: 절·소절 INSIGHTED 본문 입력 (⑦ content-expand 산출물)
draft = load_insighted_sections(seed_id)

# Step 2: M5 1·2·3층 비율 강제 (13/65/22 ±5%)
measurer = LayerRatioMeasurer()
ratios = measurer.measure(draft)
if ratios["resize_needed"]:
    return {"action": "fail_layer_ratio", "details": ratios}

# Step 3: M8 시그니처 분포 — chapter당 [2, 7] 균등
applier = SignaturePatternApplier()
sig_count = applier.count_in_draft(draft)
if not (2 <= sig_count <= 7):
    return {"action": "fail_signature_distribution", "count": sig_count}

# Step 4: M9 AI 어조 청소
purger = AITonePurger()
if purger.has_violation(draft):
    cleaned = purger.purge(draft)
else:
    cleaned = draft

# Step 5: M1 voice score 최종 ≥0.70
scorer = VoiceScorer(profile_path=".../voice_profile.yaml")
voice_score = scorer.score(cleaned)
if voice_score["weighted_total"] < 0.70:
    return {"action": "fail_voice", "score": voice_score}

# Step 6: lifecycle INSIGHTED 유지 (narrative_craft는 최종 polish 전)
fsm = LifecycleStateMachine()
new_state = fsm.transition(LifecycleState.INSIGHTED, LifecycleState.INSIGHTED)
```

### 2. 1층 콜드오픈 구조 (저자 v15)

| 요소 | 비율 |
|---|---|
| 장면·인물·구체 묘사 | 60% |
| 저자 직접 명제 | 25% |
| 다음 단계 hook (질문·통계) | 15% |

### 3. 트라우마 증언 원문 보호 (Round 18 trauma_bearing_witness 6 카테고리)

```python
# trauma_bearing_witness_category 6 카테고리 (참전·생존자·유가족·정치박해·자연재해·가정폭력)
if claim["trauma_category"]:
    # 1) 원문 그대로 인용 강제 (paraphrase 영구 금지)
    # 2) 저자 동의 metadata 확인
    # 3) 저자 6 보호 정책 자동 적용
    return inject_trauma_witness_block(claim, verbatim=True, consent_verified=True)
```

### 4. lifecycle 유지

```python
# INSIGHTED → INSIGHTED (narrative_craft는 INSIGHTED 내부 조립)
# line-edit (⑩)에서만 POLISHED 진입
```

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ voice profile + AI tone purger 결정론 |
| #4 저자 작가성·정체성 | ✅ M5·M8·M1·M9 통합 게이트 |
| #6 정신건강·취약 독자 보호 | ✅ trauma_bearing_witness 6 카테고리 원문 보호 |
| #7 결정론 환원 | ✅ M5·M8·M9·M1·M11 pure Python |

## 출처

SPEC: `specs/bookwriting-narrative-craft-master.md`
실행 모듈: `lib/layer_ratio_measurer.py` + `lib/signature_pattern_applier.py` + `lib/ai_tone_purger.py` + `lib/voice_scoring.py` + `lib/lifecycle_state_machine.py`

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 7개 sub-skill을 자동 orchestration — 저자 1층 콜드오픈 backbone.

| 순서 | Sub-skill | 호출 시점 | 페르소나 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-narrative-craft-cold-open-crafter` ⭐ | Step 1 | Cold Open Crafter | skeleton 콜드오픈 라이브러리 결정론 read |
| 2 | `bookwriting-narrative-craft-character-animator` | Step 2 | Character Animator | KNOWN_CHARACTERS dict + evidence-only |
| 3 | `bookwriting-narrative-craft-scenario-narrator` | Step 3 | Scenario Narrator | skeleton 풍경 라이브러리 |
| 4 | `bookwriting-narrative-craft-historical-parallelist` | Step 4 | Historical Parallelist | 5 역사 패턴 정규식 |
| 5 | `bookwriting-narrative-craft-signature-weaver` ⭐ | Step 5 | Signature Weaver | M8 5 패턴 자연 적용 |
| 6 | `bookwriting-narrative-craft-sensory-detail-adder` | Step 6 | Sensory Detail Adder | 3 정규식 (시각·청각·촉각) |
| 7 | `bookwriting-narrative-craft-voice-aligner` | Step 7 | Voice Aligner | M1 + M8 |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-narrative-craft cycle <chapter>
↓ Step 1
bookwriting-narrative-craft-cold-open-crafter ⭐ (skeleton 라이브러리 2-3 후보)
↓ Step 2
bookwriting-narrative-craft-character-animator (Amodei·Hassabis·Khosla·저자 입체화)
↓ Step 3
bookwriting-narrative-craft-scenario-narrator (대비 두 장면 풍경)
↓ Step 4
bookwriting-narrative-craft-historical-parallelist (대공황·핵무기·러다이트·앵글로색슨·바이마르 5종)
↓ Step 5
bookwriting-narrative-craft-signature-weaver ⭐ (5 시그니처 35%+ 자연 적용)
↓ Step 6
bookwriting-narrative-craft-sensory-detail-adder (evidence 명시 감각만)
↓ Step 7
bookwriting-narrative-craft-voice-aligner (1층 voice 0.7+ → ⑩ strict 0.85+)
↓
Master Synthesis: chapters/<ch>/narrative.md 1층 콜드오픈 (600-1200자)
```

### 저자 결정 묶음 강제
- 저자 본문 600-1200자 직접 채움 — sub는 골격·sensory·signature 기회 식별
- Historical Parallelist evidence 명시 강제 (할루시네이션 신체 디테일 금지)

### OrchestratorTracer (M18) 자동 기록
deterministic_modules_used: M1·M8 + skeleton 결정론 read.

### PROH-006 bold 인용 → 들여쓰기 인용 변환 (2026-05-25 신설)

본 마스터는 1층 콜드오픈에서 *인용 강조*를 저자 voice S4(들여쓰기 인용)로만 처리한다. 마크다운 bold(`**X**`) 금지.

변환 규칙:
- 핵심 인용 (예: 다보스 무대 verbatim) → 빈 줄 + 들여쓰기 + 한국어 인용부호 「」 또는 큰따옴표 ""
- 강조 단어 → 줄바꿈으로 호명 (예: "Hard Takeoff. 수직 이륙.")
- 저자 voice S4가 *마크다운 bold 대체* 시그니처로 영구 부착

예: `**"AI는 도구가 아니라 행위자입니다."**` →

```
   "AI는 도구가 아니라 행위자입니다.
    샐러드를 자를지 살인을 저지를지 스스로 결정할 수 있는 칼입니다."
```

book-config :: PROH-006 critical 일치. line-edit-master가 잔여 bold 검출 시 본 마스터로 재호출.
