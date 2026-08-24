---
name: bookwriting-evidence-link-master
description: 저자 책 ⑤ 단계 마스터 — EXPANDED 시드의 각 fact·claim에 수집된 근거를 결정론 연결. M3 AuthorityGrader + M13 R4MultiLayerVerifier + M2 HallucinationDetector 통합. CITE-NNN ID 발급 + forecast-registry P-NNN R1-R5 검증. LINKED→EXPANDED→EVIDENCED 게이트.
when_to_use: "`/bookwriting cycle` Step 5 자동 발동. `/bookwriting-evidence-link <claim_id>` 단독 호출 가능."
---

# bookwriting-evidence-link-master (⑤ 단계 마스터)

## TLDR

EXPANDED 시드의 모든 claim에 ④에서 수집한 근거를 1:1 매핑·검증. R4 통과 + R1-R5 정합 + HallucinationDetector 0건 → EVIDENCED 진입.

## Triggers

- `/bookwriting cycle <target>` Step 5 자동
- `/bookwriting-evidence-link <seed_id>` — 저자 직접
- `/bookwriting-evidence-link verify-r1-r5 <prediction_id>` — R1-R5만
- `/bookwriting-evidence-link cite-issue <claim_id>` — CITE-NNN 발급만

## Detailed Methodology

### 1. 결정론 chain (LLM 추론 영구 금지)

```python
import paths
from r4_multi_layer_verifier import R4MultiLayerVerifier
from forecast_registry_syncer import ForecastRegistrySyncer
from citation_detection import HallucinationDetector
from authority_grader import AuthorityGrader
from id_generator import IdGenerator
from lifecycle_state_machine import LifecycleStateMachine, LifecycleState
from pathlib import Path

# Step 1: ④ 수집 결과 로드 (claim_id → [citations])
collected = load_evidence_collection_output(seed_id)

# Step 2: HallucinationDetector — 권위 5 signals 검증
detector = HallucinationDetector()
for claim_id, citations in collected.items():
    signals = detector.detect_signals(text=claim_text, citations=citations)
    if signals["any_critical"]:
        return {"action": "fail_hallucination", "claim_id": claim_id, "signals": signals}

# Step 3: R4 다층 인용 강제 (≥2층)
r4 = R4MultiLayerVerifier()
results = r4.verify_all_claims(collected)
pass_rate = r4.count_pass_rate(results)
if pass_rate < 1.0:  # 100% 통과 강제
    failed = [r for r in results if not r["r4_pass"]]
    return {"action": "fail_r4", "failed_claims": failed}

# Step 4: forecast-registry P-NNN R1-R5 검증
syncer = ForecastRegistrySyncer(paths.forecast_registry_path())
violations = syncer.verify_all()
if any(violations.values()):
    return {"action": "fail_r1_r5", "violations": violations}

# Step 5: CITE-NNN ID 발급 (M7 atomic fcntl)
gen = IdGenerator(citation_registry_path)
for claim_id, citations in collected.items():
    for c in citations:
        c["cite_id"] = gen.issue("citation", current_max_num=...)

# Step 6: lifecycle EXPANDED → EVIDENCED 결정론 전환 (M11)
fsm = LifecycleStateMachine()
new_state = fsm.transition(LifecycleState.EXPANDED, LifecycleState.EVIDENCED)
```

### 2. R1-R5 R4 ⊇ 게이트 매트릭스

| Rule | 검증 모듈 | 통과 조건 |
|---|---|---|
| R1 quantitative_anchor | M12 | 모든 P-NNN에 정량 앵커 ≥1 |
| R2 chapter_role | M12 | 1층_콜드오픈·2층_분석·3층_함의 enum |
| R3 system_loops | M12 | L1-L7 enum |
| R4 multi_layer | M13 | unique grades ≥2 |
| R5 verification_signal | M12 | 5년·10년 falsifies_if 명시 |

### 3. R4 fail 시 저자 escalate

```python
if not r4_result["r4_pass"]:
    return {
        "action": "escalate",
        "message": (
            f"R4 위반 — claim_id={claim_id} 단일 권위만 인용. "
            f"현재 layers={r4_result['layers']}. "
            "추가 권위 1층 이상 수집 후 재시도 필요."
        ),
    }
```

### 4. citation-authority-db 누락 권위 — 자동 등록 영구 금지

저자 명시 확인 없이 citation-authority-db.yaml에 신규 권위 등록 영구 금지. 누락 권위 발견 시 저자 escalate, 저자 명시 후에만 DB 갱신.

### 5. lifecycle 전환

```python
# EXPANDED → EVIDENCED (Round 18 STAGE_TO_TRANSITION 매핑)
fsm = LifecycleStateMachine()
new_state = fsm.transition(LifecycleState.EXPANDED, LifecycleState.EVIDENCED)
```

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ HallucinationDetector + R4 + R1-R5 결정론 통합 |
| #3 출처 명시 | ✅ R4 다층 강제 + CITE-NNN 1:1 매핑 |
| #5 보안 법적 위험 | ✅ 신규 권위 자동 등록 영구 금지 |
| #7 결정론 환원 | ✅ M3·M13·M2·M12·M7·M11 pure Python |

## 출처

SPEC: `specs/bookwriting-evidence-link-master.md`
실행 모듈: `lib/r4_multi_layer_verifier.py` + `lib/forecast_registry_syncer.py` + `lib/citation_detection.py` + `lib/authority_grader.py` + `lib/id_generator.py` + `lib/lifecycle_state_machine.py`

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 7개 sub-skill을 자동 orchestration.

| 순서 | Sub-skill | 호출 시점 | 페르소나 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-evidence-link-graph-builder` | Step 2 | Graph Builder | yaml.safe_load + dataclass |
| 2 | `bookwriting-evidence-link-edge-detector` | Step 3 | Edge Detector | 3 type 정규식 (logical·temporal·causal) |
| 3 | `bookwriting-evidence-link-authority-mapper` | Step 4 | Authority Mapper | M3 AuthorityGrader |
| 4 | `bookwriting-evidence-link-r4-verifier` ⭐ | Step 5 | R4 Verifier | M13 R4MultiLayerVerifier + 저자 묶음 4 옵션 |
| 5 | `bookwriting-evidence-link-loop-integrator` | Step 6 | Loop Integrator | yaml + L1-L7 dict |
| 6 | `bookwriting-evidence-link-isolation-detector` | Step 6 | Isolation Detector | degree dict + 저자 묶음 3 옵션 |
| 7 | `bookwriting-evidence-link-graph-visualizer` | Step 9 | Graph Visualizer | str 조립 markdown table + ASCII |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-evidence-link cycle <target>
↓
Step 2: bookwriting-evidence-link-graph-builder (evidence-track → 노드)
↓
Step 3: bookwriting-evidence-link-edge-detector (논리·시간·인과 엣지)
↓
Step 4: bookwriting-evidence-link-authority-mapper (Grade A-E 100% 매핑)
↓
Step 5: bookwriting-evidence-link-r4-verifier ⭐ (R4 다층 강제 + 저자 묶음 4 옵션)
↓
Step 6 병렬:
  ├─ bookwriting-evidence-link-loop-integrator (L1-L7 매핑 80%+)
  └─ bookwriting-evidence-link-isolation-detector (degree 0·1 + 저자 묶음)
↓
Step 9: bookwriting-evidence-link-graph-visualizer (markdown + ASCII)
↓
Master Synthesis: chapters/<ch>/evidence-track.yaml 그래프 필드 갱신
```

### 저자 결정 묶음 강제
- R4 Verifier 단일 권위 주장 발견 시 저자 묶음 4 옵션 (외부 manual·Layer 1 유지·풀 제외·defer)
- Isolation Detector degree 0 발견 시 저자 묶음 3 옵션 (풀 제외·연결 추가·미해결 보관)

### OrchestratorTracer (M18) 자동 기록
deterministic_modules_used: M3·M13 + pure Python dict 그래프 (networkx 의존 없음).
