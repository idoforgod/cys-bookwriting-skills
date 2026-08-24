---
name: bookwriting-insight-synthesis-master
description: 저자 책 ⑥ 단계 마스터 — 제2저자 최정상. 저자 진북 14단계 *의미·영향력·놀라움 단면 선택*. 저자 진북 *"가장 의미있고 영향력 크고 깜짝놀랄만한 미래의 단면을 매력적인 글로 쓰는 방식이 핵심"* 직접 구현. 7 AI Agents 페르소나 + 8 sub-skill + 6 Cycle + 7 Gate (Q18 최정밀).
when_to_use: "`/bookwriting cycle` 진행 Step 6 자동 발동 — ④ evidence-collect·⑤ evidence-link 통과 후. 저자 명시 `/bookwriting-insight-synthesis cycle <target>` 호출도 가능."
---

# bookwriting-insight-synthesis-master (⑥ 제2저자 최정상)

## TLDR

저자 책의 *통찰 가치 보장* 핵심. ④·⑤ 통과한 evidence·그래프에서 *3 기준 (의미·영향력·놀라움)*으로 *책에 담을 단면* 5-7개 후보 생성·저자 묶음 채택. M3·M4·M1·M8 결정론 + 저자 사상적 척추 4개 매핑.

## Triggers

- `/bookwriting cycle <target>` Step 6 자동 (④·⑤ 통과 후)
- `/bookwriting-insight-synthesis cycle <target>` — 저자 직접
- `/bookwriting-insight-synthesis candidates <target>` — 후보만
- `/bookwriting-insight-synthesis evaluate <insight-id>` — 특정 통찰 재평가

## Detailed Methodology

### 1. 3 기준 (Insight Triad — 저자 진북 직접 인용)

> *"가장 의미있고, 영향력이 크고, 깜짝놀랄만한 미래의 단면을 선택하여 매력적인 글로 쓰는 방식이 핵심이다."*

| 기준 | 가중치 | 결정론 측정 |
|---|---|---|
| 의미 (Meaning) | 0.35 | M1.compute_meaning_score (저자 사상적 척추 4개 매핑) |
| 영향력 (Impact) | 0.35 | M4.extract_all (정량 앵커·스케일·시점) |
| 놀라움 (Surprise) | 0.30 | M8.detect_opportunities (시그니처 패턴 *X가 아니라 Y* 등) |

### 2. 결정론 chain (LLM 추론 영구 금지)

```python
import paths
from voice_scoring import VoiceScorer
from quantitative_extraction import QuantitativeAnchorExtractor
from authority_grader import AuthorityGrader, Grade
from signature_pattern_applier import SignaturePatternApplier
from pathlib import Path
import yaml

with open(paths.book_config_path()) as f:
    config = yaml.safe_load(f.read())

scorer = VoiceScorer(config["voice_guidelines"])
extractor = QuantitativeAnchorExtractor()
grader = AuthorityGrader(Path("../../expert_pool/citation-authority-db.yaml"))
sig_applier = SignaturePatternApplier()

# 각 통찰 후보별 3 점수
for candidate in insight_candidates:
    meaning = scorer.compute_meaning_score(candidate.text)
    impact_anchors = extractor.extract_all(candidate.text)
    impact = min(1.0, len(impact_anchors) / 3.0)
    surprise_ops = sig_applier.detect_opportunities(candidate.text)
    surprise = min(1.0, len(surprise_ops) / 2.0)
    weighted = 0.35 * meaning + 0.35 * impact + 0.30 * surprise
    
    # ★ 추천: weighted >= 0.7
    candidate.starred = weighted >= 0.7
    
    # R4 다층 권위 매핑 강제
    r4 = grader.verify_r4_multi_layer(candidate.citation_grades)
    if not r4["r4_pass"]:
        # 통찰 풀에서 제외 (단일 권위)
        continue
```

### 3. 7 AI Agents 페르소나 (SPEC §13)

| # | 페르소나 | 역할 |
|---|---|---|
| 1 | Meta-tool Identifier | 메타도구 명제 연결 통찰 |
| 2 | System Loop Detector | L1-L7 시스템 루프 변수 |
| 3 | Authority Cross-checker | 권위 5층 다층 검증 (R4) |
| 4 | Surprise Hunter ⭐ | 통념 깨기·프레임 전복 |
| 5 | Impact Assessor | 정량 앵커·스케일 |
| 6 | Meaning Synthesizer | 저자 사상적 척추 매핑 |
| 7 | Voice Aligner ⭐ | 저자 voice + 시그니처 패턴 |

### 4. 저자 묶음 출력 양식 (Mode 1)

```markdown
# 사이클 C-NNN — ⑥ insight-synthesis 묶음

## 통찰 후보 5개

### (a) ★ INS-001 [의미 0.88·영향 0.85·놀라움 0.82·종합 0.85]
"AGI는 도구가 아니라 도구를 만드는 도구 — 메타도구는 인간 인지를 무한 확장"
- 권위: Layer 1 (Amodei) + Layer 4 (Harari) — R4 다층 ✅
- 정량 앵커: 1-3년 / 90% 확신 / 100배 스케일
- 시그니처: "X가 아니라 Y" 적용
- 시스템 루프: L1 지능대체나선 변수 1

### (b) ★ INS-003 [...] 
...

저자: "1=a,b,c" 응답
```

### 5. Mode 2 자동 채택 (시뮬레이션)

★ 추천 (weighted ≥ 0.7) 자동 채택 → `chapters/<ch>/_simulations/sim-NNN-insights.md` 저장. 정식 chapter·seed-registry 미갱신.

### 6. 진북 #6 Safe Messaging Gate 자동 발동

skeleton.md 8장 "의미 위기" 통찰 → 자동 감지 → surprise_weight 0.30 → 0.10 자동 하향 (Round 7 #C10.3) + WHO safe messaging guidelines 적용.

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ M2 cross-cutting + R4 단일 권위 풀 제외 |
| #2 grill-me 일치 | ✅ 저자 진북 *3 기준 (의미·영향력·놀라움)* 직접 인용 |
| #3 출처 명시 | ✅ M3 권위 등급화 + R4 다층 강제 |
| #4 저자 작가성 ⭐⭐ | ✅ M1 meaning_score + 사상적 척추 4개 + 시그니처 적용 |
| #6 정신건강 | ✅ Safe Messaging Gate 8장 의미 위기 자동 |
| #7 결정론 환원 | ✅ M1·M3·M4·M8 모두 결정론 |

## 출처

SPEC: `specs/bookwriting-insight-synthesis-master.md` (17 항목 풀)
실행 모듈: `lib/voice_scoring.py` + `lib/quantitative_extraction.py` + `lib/authority_grader.py` + `lib/signature_pattern_applier.py`
저자 진북 인용: skeleton.md §사상적척추 + grill-me-decisions.md 저자 진북 직접 명시

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 9개 sub-skill을 자동 orchestration — 저자 제2저자 최정밀 단계.

| 순서 | Sub-skill | 호출 시점 | 페르소나 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-insight-synthesis-candidate-generation` | Step 2 | Meta-tool·System Loop·Surprise Hunter (3 페르소나) | M7 IdGenerator INS-NNN |
| 2 | `bookwriting-insight-synthesis-meaning-evaluation` | Step 2 (병렬) | Meaning Synthesizer | 4 사상적 척추 가중합 (0.30+0.25+0.25+0.20) |
| 3 | `bookwriting-insight-synthesis-impact-evaluation` | Step 2 (병렬) | Impact Assessor | M4 QuantitativeAnchorExtractor + 3 차원 |
| 4 | `bookwriting-insight-synthesis-surprise-evaluation` ⭐ | Step 2 (병렬) | Surprise Hunter | 4 놀라움 유형 정규식 |
| 5 | `bookwriting-insight-synthesis-triad-evaluation` | Step 5 | Master 통합 | 0.35·meaning + 0.35·impact + 0.30·surprise · ≥2.7 ★ |
| 6 | `bookwriting-insight-synthesis-authority-multi-layer` ⭐ | Step 5 | Authority Cross-checker | M3 + M13 + 단일 권위 풀 제외 |
| 7 | `bookwriting-insight-synthesis-voice-craft` ⭐ | Step 6 | Voice Aligner | M1 VoiceScorer + M8 SignaturePatternApplier + 1회 재시도 |
| 8 | `bookwriting-insight-synthesis-cross-chapter-check` | Step 7 | Master | M6 BM25 |
| 9 | `bookwriting-insight-synthesis-bundle-builder` | Step 8 | Master | M7 D-NNN + markdown 묶음 |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-insight-synthesis cycle <target>
↓ Step 2 후보 생성 + 3 기준 병렬 평가
bookwriting-insight-synthesis-candidate-generation (3 페르소나 9-15 후보)
├─ bookwriting-insight-synthesis-meaning-evaluation (0-1)
├─ bookwriting-insight-synthesis-impact-evaluation (0-1)
└─ bookwriting-insight-synthesis-surprise-evaluation ⭐ (0-1)
↓ Step 5 통합 평가 + R4
bookwriting-insight-synthesis-triad-evaluation (가중합 + ≥2.7 ★ 자동)
+ bookwriting-insight-synthesis-authority-multi-layer ⭐ (R4 단일 권위 풀 제외)
↓ Step 6 voice 정밀화 (★ 추천만)
bookwriting-insight-synthesis-voice-craft ⭐ (0.7+ 도달까지 1회 재시도)
↓ Step 7 cross-chapter
bookwriting-insight-synthesis-cross-chapter-check (M6 BM25 ≥0.7)
↓ Step 8 저자 묶음 markdown
bookwriting-insight-synthesis-bundle-builder (★ 표시 + D-NNN + 저자 즉답 형식)
↓
Master Synthesis: seed lifecycle EVIDENCED → INSIGHTED + analysis.md·implications.md 통찰 본문
```

### 저자 결정 묶음 강제
- Authority Multi-Layer 단일 권위 통찰 풀 *제외* (자동)
- Voice Craft 1회 재시도 후 0.7+ 미달 시 저자 묶음 (재작성 옵션)
- Bundle Builder 저자 즉답 형식 `1=a,b,c / 2=skip`

### OrchestratorTracer (M18) 자동 기록
deterministic_modules_used 누적: M1·M3·M4·M6·M7·M8·M13 7종.
