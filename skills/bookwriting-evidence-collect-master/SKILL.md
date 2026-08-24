---
name: bookwriting-evidence-collect-master
description: 저자 책 ④ 단계 마스터 — 근거자료 결정론 수집. R4 다층 인용 강제 (최소 2층 권위). M3 AuthorityGrader 7층 + M13 R4MultiLayerVerifier + M2 HallucinationDetector. citation-authority-db.yaml 57+ 권위 등록자 풀에서 결정론 매칭. 외부 LLM 추론 영구 금지.
when_to_use: "`/bookwriting cycle` Step 4 자동. `/bookwriting-evidence-collect <claim_id>` 단독 호출도 가능."
---

# bookwriting-evidence-collect-master (④ 단계 마스터)

## TLDR

LINKED 시드의 각 claim에 결정론적 근거 수집·등급화. R4 (최소 2층 권위) 통과해야 EXPANDED 진입.

## Triggers

- `/bookwriting cycle <target>` Step 4 자동
- `/bookwriting-evidence-collect <claim_id>` — 저자 직접
- `/bookwriting-evidence-collect db-lookup <author>` — citation-authority-db 단순 조회
- `/bookwriting-evidence-collect r4-verify <prediction_id>` — R4만 검증

## Detailed Methodology

### 1. citation-authority-db 결정론 조회 (LLM 추론 영구 금지)

```python
import paths
from authority_grader import AuthorityGrader, Grade
from r4_multi_layer_verifier import R4MultiLayerVerifier
from citation_detection import HallucinationDetector

grader = AuthorityGrader(
    db_path=paths.authority_db_path()
)

# Step 1: claim별 후보 권위 자동 매칭
authors_for_claim = grader.find_authorities_for_topic(claim_topic)
# 예: AGI timeline claim → ["Dario Amodei (A)", "Sam Altman (A)", "Yuval Harari (D)", "{{저자명}} (B)"]

# Step 2: HallucinationDetector — 권위 5층 누락 검출
detector = HallucinationDetector()
signals = detector.detect_signals(text=draft_claim)
# 5 signals: no_author·no_year·vague_attribution·no_source_type·no_authority_grade

# Step 3: R4 다층 인용 강제 (최소 2층, 단일 권위만 인용 영구 금지)
r4 = R4MultiLayerVerifier()
result = r4.verify_claim(claim_id, citations=[
    {"author": "Amodei", "grade": "A"},  # 창업자
    {"author": "{{저자명}}", "grade": "B"},  # 미래학자
])
# {"r4_pass": True, "layer_count": 2, "action": "approve"}
```

### 2. 7층 권위 등급 (citation-authority-db.yaml 57+ 등록자)

| Grade | 의미 | 예시 |
|---|---|---|
| A | 창업자·실행자 | Amodei·Altman·Hassabis |
| A_preprint | 학술 preprint (Round 9 추가) | arXiv·SSRN |
| B | 저자 본인·미래학자 | {{저자명}}·Glenn·Gordon |
| C | 인접학문 (경제·정치·인구학) | Acemoglu·Stiglitz |
| D | 사상가 | Harari·Bostrom |
| E | 역사평행 | Polanyi·Braudel |
| F | 신학 | Niebuhr·Brueggemann |
| G | 토착지혜 | 저자 명시 트라우마 증언 카테고리 |
| out | 권위 불명확 — 자동 거부 |

### 3. 빈 권위층 — 저자 escalate

```python
if result["layer_count"] < 2:
    return {
        "action": "escalate",
        "message": f"R4 위반 — claim_id={claim_id}에 권위 1층뿐. 추가 권위 필요. 후보: {authors_for_claim}",
    }
```

### 4. 트라우마 증언 카테고리 보호 (citation-authority-db.yaml Round 18 fix)

`trauma_bearing_witness_category` (참전·생존자·유가족·정치박해 등 6 카테고리)는 G등급 토착지혜와 별개로 *원문 그대로 인용 + 저자 동의 + 저자 6 보호 정책 적용*.

### 5. lifecycle 전환

```python
# LINKED → EXPANDED (Round 18 STAGE_TO_TRANSITION 매핑)
fsm = LifecycleStateMachine()
new_state = fsm.transition(LifecycleState.LINKED, LifecycleState.EXPANDED)
```

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ HallucinationDetector 5 signals + citation-authority-db 결정론 |
| #2 grill-me 원문 일치 | ✅ 원문 인용 강제 |
| #3 출처 명시 | ✅ R4 다층 강제 |
| #5 보안 법적 위험 | ✅ 출처 동의·인용 정책 |
| #7 결정론 환원 | ✅ M3·M13·M2 pure Python |

## 출처

SPEC: `specs/bookwriting-evidence-collect-master.md`
실행 모듈: `lib/authority_grader.py` + `lib/r4_multi_layer_verifier.py` + `lib/citation_detection.py`
DB: `expert_pool/citation-authority-db.yaml` (57+ 권위 + 6 트라우마 카테고리)

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 6개 sub-skill을 자동 orchestration.

| 순서 | Sub-skill | 호출 시점 | 페르소나 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-evidence-collect-asset-searcher` | Step 2 | Asset Searcher | M6 BM25 + inbox 우선 |
| 2 | `bookwriting-evidence-collect-authority-grader` ⭐ | Step 3 | Authority Grader | M3 + M13 + Grade out 제외 |
| 3 | `bookwriting-evidence-collect-quantitative-anchor-extractor` ⭐ | Step 4 | Quant Anchor Extractor | M4 + M2 Critical 즉시 차단 |
| 4 | `bookwriting-evidence-collect-verification-signal-finder` | Step 5 | Verification Signal Finder | R5 정규식 3 패턴 |
| 5 | `bookwriting-evidence-collect-forecast-registry-syncer` | Step 6 | Forecast Registry Syncer | M12 + 중복 저자 묶음 |
| 6 | `bookwriting-evidence-collect-evidence-quality-filter` | Step 9 | Evidence Quality Filter | 5차원 가중합 (relevance·grade·R4·anchor·signal) |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-evidence-collect cycle <target>
↓ Step 2
bookwriting-evidence-collect-asset-searcher (search_paths + inbox 우선)
↓ Step 3
bookwriting-evidence-collect-authority-grader ⭐ (Grade A-E·out + R4 + learning-log)
↓ Step 4
bookwriting-evidence-collect-quantitative-anchor-extractor ⭐ (저자 시그니처 100배·90%·5억 명·2027)
↓ Step 5
bookwriting-evidence-collect-verification-signal-finder (R5 verification_signal·falsifies_if)
↓ Step 6
bookwriting-evidence-collect-forecast-registry-syncer (P-NNN 등록·중복 저자 묶음 3 옵션)
↓ Step 9
bookwriting-evidence-collect-evidence-quality-filter (5차원 점수·임계 ADOPT·ESCALATE·REJECT)
↓
Master Synthesis: chapters/<ch>/evidence-track.yaml + forecast-registry 갱신 + lifecycle EXPANDED→EVIDENCED
```

### 저자 결정 묶음 강제
- Authority Grader Grade out 자료 풀 제외 (자동)
- Quantitative Anchor Extractor 출처 미명시 시 M2 Critical 즉시 차단
- Forecast Registry Syncer 중복 P-NNN 저자 묶음 강제 (병합·신규·skip)
- Evidence Quality Filter 임계 미달 시 저자 묶음 escalate (Grade A·B 보강 권장)

### OrchestratorTracer (M18) 자동 기록
deterministic_modules_used 6 sub 누적: M2·M3·M4·M6·M12·M13 — Citation Gate ⭐⭐⭐ 가장 엄격 적용 단계.
