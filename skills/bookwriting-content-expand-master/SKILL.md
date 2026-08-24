---
name: bookwriting-content-expand-master
description: 저자 책 ⑦ 단계 마스터 — INSIGHTED 시드 본문 확장. M5 LayerRatioMeasurer 1·2·3층 13/65/22 비율 강제 + M4 QuantitativeExtraction 정량 앵커 강제 (R1) + M8 SignaturePattern 저자 5 시그니처 적용 + M9 AITonePurger AI 어조 청소. 시드 → 절·소절 단위 확장.
when_to_use: "`/bookwriting cycle` Step 7 자동. `/bookwriting-content-expand <seed_id>` 단독 호출."
---

# bookwriting-content-expand-master (⑦ 단계 마스터)

## TLDR

INSIGHTED 시드를 절·소절 단위 본문으로 확장. 1·2·3층 13/65/22 비율 + 저자 5 시그니처 + AI 어조 청소 + R1 정량 앵커 강제.

## Triggers

- `/bookwriting cycle <target>` Step 7 자동
- `/bookwriting-content-expand <seed_id>` — 저자 직접
- `/bookwriting-content-expand layer-check <draft>` — M5 비율 측정만
- `/bookwriting-content-expand signature-apply <draft>` — M8 시그니처 적용만
- `/bookwriting-content-expand ai-purge <draft>` — M9 AI 어조 청소만

## Detailed Methodology

### 1. 결정론 chain

```python
from layer_ratio_measurer import LayerRatioMeasurer
from quantitative_extraction import QuantitativeExtractor
from signature_pattern_applier import SignaturePatternApplier
from ai_tone_purger import AITonePurger
from voice_scoring import VoiceScorer

# Step 1: 시드 → 초안 확장 (LLM 작성 — 저자 작가성 유지)
draft = expand_seed_to_section(seed)  # 절 단위, 1000-3000자

# Step 2: M5 1·2·3층 비율 측정 (R2 chapter_role 정합)
measurer = LayerRatioMeasurer()
ratios = measurer.measure(draft)
# {"layer_1": 0.12, "layer_2": 0.63, "layer_3": 0.25, "violations": [], "resize_needed": False}

# 13/65/22 ±5% 이탈 시 resize
if ratios["resize_needed"]:
    return {"action": "resize", "details": ratios}

# Step 3: R1 정량 앵커 강제
extractor = QuantitativeExtractor()
anchors = extractor.extract(draft)
if not anchors:
    return {"action": "fail_r1", "message": "정량 앵커 누락 — P-NNN 등록 거부"}

# Step 4: 저자 5 시그니처 적용 (MAX_PER_CHAPTER=7)
applier = SignaturePatternApplier()
signature_count = applier.count_in_draft(draft)
if signature_count < 2:
    return {"action": "fail_signature", "message": "시그니처 < 2 — 저자 작가성 부족"}
if signature_count > 7:
    return {"action": "fail_signature_excess", "message": "시그니처 > 7 — 과포화 (MAX_PER_CHAPTER)"}

# Step 5: M9 AI 어조 청소
purger = AITonePurger()
clean_draft = purger.purge(draft)
# Korean + English AI 어조 패턴 제거

# Step 6: M1 VoiceScorer 최종 점수 (>=0.70 통과)
scorer = VoiceScorer(profile_path=".../voice_profile.yaml")
voice_score = scorer.score(clean_draft)
if voice_score["weighted_total"] < 0.70:
    return {"action": "fail_voice", "score": voice_score}
```

### 2. 1·2·3층 비율 (Round 8 #D8.1 — 13/65/22 default)

| 층 | 비율 | 역할 |
|---|---|---|
| 1층 콜드오픈 | 13% (±5%) | 저자 narrative — 장면·인물·구체 |
| 2층 분석 | 65% (±5%) | 저자 분석·근거·논거 |
| 3층 함의 | 22% (±5%) | 미래학적 함의·정책 |

### 3. 저자 5 시그니처 (M8 정규식 결정론)

1. *X가 아니라 Y* — 저자 정의 차별화
2. *셋 중 하나가 아니다* — 저자 분기 거부
3. *X와 Y 사이의 거리* — 저자 측정 메타포
4. *N 창업자가 같은 N배* — 저자 스케일 마커
5. *변수 X에 따라 결과가 갈리는* — 저자 시나리오 마커

`MAX_PER_CHAPTER = 7` — 과포화 시 시그니처 패턴 자동 분산.

### 4. AI 어조 청소 (M9)

| 패턴 | 청소 |
|---|---|
| "*살펴보겠습니다*" | 저자 직설 |
| "*다음과 같습니다*" | 저자 단언 |
| "*매우*" 과다 | 저자 정량 |
| "*let me*", "*I'll*" | 저자 한국어 단정 |

### 5. lifecycle 유지

```python
# INSIGHTED → INSIGHTED (Round 18 STAGE_TO_TRANSITION: content_expand 유지)
fsm = LifecycleStateMachine()
new_state = fsm.transition(LifecycleState.INSIGHTED, LifecycleState.INSIGHTED)
```

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ R1 정량 앵커 + voice profile 결정론 |
| #4 저자 작가성·정체성 | ✅ M8 5 시그니처 + M9 AI 어조 청소 + M1 voice score >=0.70 |
| #7 결정론 환원 | ✅ M5·M4·M8·M9·M1 pure Python |

## 출처

SPEC: `specs/bookwriting-content-expand-master.md`
실행 모듈: `lib/layer_ratio_measurer.py` + `lib/quantitative_extraction.py` + `lib/signature_pattern_applier.py` + `lib/ai_tone_purger.py` + `lib/voice_scoring.py`

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 7개 sub-skill을 자동 orchestration — 저자 v1 2층 표준 골격 7요소.

| 순서 | Sub-skill | 호출 시점 | 저자 v1 2층 요소 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-content-expand-proposition-restater` | 요소 1 | 핵심 명제 재진술 | M4 + 정규식 |
| 2 | `bookwriting-content-expand-weak-signal-synthesizer` | 요소 2 | 약신호 | M3 Grade A·B 필터 |
| 3 | `bookwriting-content-expand-driving-force-synthesizer` | 요소 3 | 추동력 | 7 정규식 패턴 |
| 4 | `bookwriting-content-expand-system-loop-narrator` | 요소 4 | L1-L7 호명 | yaml + dict |
| 5 | `bookwriting-content-expand-scenario-brancher` | 요소 5 | 시나리오 분기 | 4 분기 패턴 |
| 6 | `bookwriting-content-expand-time-coordinator` | 요소 6+7 | AGI 5단계 + 횡단 | skeleton 결정론 read (Round 9 #E4.1) |
| 7 | `bookwriting-content-expand-voice-aligner` ⭐ | 마지막 | gentle voice | M1 + M8 (0.7+) |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-content-expand cycle <chapter>
(저자 진북 #4 게이트: 저자가 직접 본문 입력해야 진입)
↓ 요소 1
bookwriting-content-expand-proposition-restater (1층 명제 + 정량 앵커 재진술)
↓ 요소 2
bookwriting-content-expand-weak-signal-synthesizer (Grade A·B 가시 evidence)
↓ 요소 3
bookwriting-content-expand-driving-force-synthesizer (한계비용·자본·기술 곡선)
↓ 요소 4
bookwriting-content-expand-system-loop-narrator (L1 지능대체나선 변수·피드백)
↓ 요소 5
bookwriting-content-expand-scenario-brancher (분기 A vs B + 정치 변수)
↓ 요소 6+7
bookwriting-content-expand-time-coordinator (AGI 5단계 + cross-chapter)
↓ 마지막
bookwriting-content-expand-voice-aligner ⭐ (gentle 0.7+ — ⑩ strict 0.85+ 전 1차)
↓
Master Synthesis: chapters/<ch>/analysis.md 2층 본문 (4000-7000자)
```

### 저자 결정 묶음 강제
- 저자 진북 #4 (작가성) — 본문 200-1200자/요소는 저자 직접 채움
- sub-skill은 *골격 + 검증*만 수행
- voice-aligner gentle 0.7+ 미달 시 voice-gate cross-cutting 재작성

### OrchestratorTracer (M18) 자동 기록
deterministic_modules_used: M1·M3·M4·M8 + skeleton 결정론 read (AGI 5단계 하드코딩 영구 금지)

### PROH-006 마크다운 생성 단계 차단 (2026-05-25 신설)

본 마스터의 모든 sub-skill은 *생성 시점부터* 마크다운 기호 free 출력을 강제한다.

- LLM prompt에 명시: "마크다운 기호(#·*·**·`·>·-·---) 사용 금지. 강조는 줄바꿈+들여쓰기로."
- voice-aligner 통과 직전 markdown_violation_count 결정론 검증 (line-edit-master 정규식 7종 재사용)
- 위반 시 *재생성 1회* + 저자 묶음 (재생성 vs strip)

표(`| ... |`)와 ASCII diagram은 예외 — 단행본 시각 구조 보존.

book-config :: PROH-006 critical 일치.
