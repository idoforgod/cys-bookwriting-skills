---
name: bookwriting-fact-anchor-master
description: 저자 책 ② 단계 마스터 — fact·score 정합성·중복·충돌 검증. M4 QuantitativeAnchorExtractor + M3 AuthorityGrader + M2 HallucinationDetector 결정론 호출. forecast-registry sync. citation-gate Critical 가장 엄격 적용 단계. 저자 진북 #1 (할루시네이션 0) + #3 (출처 명시) backbone.
when_to_use: "`/bookwriting cycle` 진행 중 Step 2 (fact-anchor) 자동 발동. 저자 명시 `/bookwriting-fact-anchor cycle <target>` 호출도 가능."
---

# bookwriting-fact-anchor-master (② 단계 마스터)

## TLDR

저자 책 ② 단계 — 흡수된 자산의 fact·통계·정량 표현을 *결정론 추출* + *권위 등급 매핑* + *중복·충돌 검출* + *forecast-registry sync*. 저자 진북 #1·#3·#5 동시 강제.

## Triggers

- `/bookwriting cycle <target>` 진행 중 Step 2 자동
- `/bookwriting-fact-anchor cycle <target>` — 저자 직접 호출
- `/bookwriting-fact-anchor extract <target>` — fact 추출만
- `/bookwriting-fact-anchor conflict-detect <target>` — 충돌만

## Detailed Methodology

### 1. 결정론 호출 chain (LLM 추론 영구 금지)

```python
from quantitative_extraction import QuantitativeAnchorExtractor
from authority_grader import AuthorityGrader, Grade
from citation_detection import HallucinationDetector, CitationMetadata
from pathlib import Path

extractor = QuantitativeAnchorExtractor()
grader = AuthorityGrader(Path("../../expert_pool/citation-authority-db.yaml"))
det = HallucinationDetector()

# Step 1: 흡수 자산에서 fact 결정론 추출
anchors = extractor.extract_all(text)

# Step 2: 단위 강제 (Round 9 #C9.5)
for anchor in anchors:
    if not extractor.has_unit(anchor):
        # 저자 묶음 escalate — "100배" 단위 불명확
        ...

# Step 3: 권위 등급화
grade = grader.assign_grade(author=source_author)

# Step 4: 할루시네이션 검증
signals = det.detect_all(text, citation)
if signals.is_critical():
    # 즉시 차단 (① absorb 외 모든 단계 Critical 즉시 차단)
    ...
```

### 2. 5 sub-skill 책임 (SPEC §13)

| Sub | 책임 | 결정론 모듈 |
|---|---|---|
| 1 | fact-extractor | M4 + M10 (Levenshtein) |
| 2 | duplicate-detector | M10 detect_duplicates |
| 3 | conflict-detector | (Critical — 저자 묶음 강제) |
| 4 | registry-syncer | M12 forecast_registry_syncer |
| 5 | seed-linker | seed-registry connections.linked_predictions |

### 3. 저자 v1 R1 quantitative_anchor 강제

저자 v1 chapter-pipeline.md R1 규칙 — 모든 P-NNN에 quantitative_anchor 필수.

```python
# M12 forecast_registry_syncer 호출
syncer = ForecastRegistrySyncer(forecast_registry_path)
violations = syncer.verify_r1_quantitative_anchor()
if violations:
    # 저자 묶음 — R1 위반 P-NNN 보강 요청
    ...
```

### 4. 충돌 검출 정책 (Round 8 #D9.4)

수치 충돌 발견 시 *권위 등급 비교* + *방법론 차이* 자동 분석:
- 같은 수치 다른 방법론 (예: 점유율 30% — 승차 기준 vs 차량 기준)
- 같은 방법론 다른 수치 (예: 100배 vs 50배)

저자 묶음 escalate — 자동 결정 영구 금지.

### 5. citation-gate Critical 가장 엄격 적용 ⭐⭐⭐

본 단계는 ① absorb 예외와 달리 Critical *즉시 차단*:
- 할루시네이션 의심 → 풀에서 영구 제외
- R4 단일 권위 → 풀에서 제외
- 단위 누락 정량 → 저자 묶음 (Round 9 #C9.5)

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ M2 + Critical 즉시 차단 |
| #3 출처 명시 | ✅ M3 권위 등급화 + R4 검증 |
| #5 법적 위험 | ✅ 충돌 정량 저자 묶음 강제 |
| #7 결정론 환원 | ✅ M4·M3·M2 모두 결정론 |

## 출처

SPEC: `specs/bookwriting-fact-anchor-master.md` (17 항목 풀)
실행 모듈: `lib/quantitative_extraction.py` + `lib/authority_grader.py` + `lib/citation_detection.py`
호출자: `bookwriting-master` Step 2

## Sub-skill Orchestration Trace ⭐ (저자 7번째 절대 protocol)

본 마스터 호출 시 5개 sub-skill을 자동 orchestration. M18 OrchestratorTracer 결정론 기록.

| 순서 | Sub-skill | 호출 시점 | AI Agent 페르소나 | 결정론 모듈 |
|---|---|---|---|---|
| 1 | `bookwriting-fact-anchor-fact-extractor` | Step 2 | Fact Extractor | M10 FactExtractor |
| 2 | `bookwriting-fact-anchor-duplicate-detector` | Step 4 | Duplicate Detector | M10 detect_duplicates + M3 AuthorityGrader |
| 3 | `bookwriting-fact-anchor-conflict-detector` ⭐ | Step 5 | Conflict Detector | 정규식 + 저자 묶음 강제 |
| 4 | `bookwriting-fact-anchor-registry-syncer` | Step 6 | Registry Syncer | M12 ForecastRegistrySyncer |
| 5 | `bookwriting-fact-anchor-seed-linker` | Step 7 | Seed Linker | M3 + M11 LifecycleStateMachine |

### 자동 호출 흐름

```
사용자 명령: /bookwriting-fact-anchor cycle <target>
↓
Step 2: bookwriting-fact-anchor-fact-extractor 자동 호출
  Input: ① absorb 통과 자산
  Output: List[AnchoredFact] (F-NNN + source_file + context)
↓
Step 4: bookwriting-fact-anchor-duplicate-detector 자동 호출
  Input: fact 풀 + citation-authority-db
  Output: List[DuplicateGroup] (primary + secondary)
↓
Step 5: bookwriting-fact-anchor-conflict-detector ⭐ 자동 호출
  Input: 중복 검출 fact 풀
  Output: List[FactConflict] (수치·시점·논리 + severity)
  ⚠ 충돌 발견 시 저자 묶음 *강제* — 자동 결정 영구 금지
↓ (충돌 해결 후)
Step 6: bookwriting-fact-anchor-registry-syncer 자동 호출
  Input: fact 풀 + forecast-registry path
  Output: SyncResult (new_predictions + updated + r1_violations)
↓
Step 7: bookwriting-fact-anchor-seed-linker 자동 호출
  Input: SyncResult + fact_pool + seed-registry
  Output: List[SeedLinkResult] (linked_predictions + grades + lifecycle SEED→LINKED)
↓
Master Synthesis: seed-registry·forecast-registry 갱신 + 저자 화면 출력
```

### 저자 결정 묶음 강제
- Conflict Detector 충돌 발견 시 *반드시* 저자 묶음 (자동 결정 영구 금지)
- Registry Syncer 중복 P-NNN 모호 매칭 시 저자 묶음 (병합·신규·skip)

### OrchestratorTracer (M18) 자동 기록
```python
tracer.record(skill_name="bookwriting-fact-anchor-fact-extractor", sequence=1, deterministic_modules_used=["M10"])
tracer.record(skill_name="bookwriting-fact-anchor-duplicate-detector", sequence=2, deterministic_modules_used=["M10", "M3"])
tracer.record(skill_name="bookwriting-fact-anchor-conflict-detector", sequence=3, deterministic_modules_used=[])
tracer.record(skill_name="bookwriting-fact-anchor-registry-syncer", sequence=4, deterministic_modules_used=["M12"])
tracer.record(skill_name="bookwriting-fact-anchor-seed-linker", sequence=5, deterministic_modules_used=["M3", "M11"])
```
