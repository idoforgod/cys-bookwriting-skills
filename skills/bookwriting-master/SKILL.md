---
name: bookwriting-master
description: 저자 책 쓰기 메타 마스터. 11 단계 마스터를 오케스트레이션하는 진입점. /bookwriting <mode> 슬래시로 호출. 저자 진북 7개 (할루시네이션 0·grill-me 일치·출처·작가성·법적·정신건강·결정론 환원) 모두 cross-cutting 강제. Mode 1 (정밀 HITL·15-25분/사이클·HITL 3-5회) + Mode 2 (전자동 시뮬레이션·5-10분·HITL 0). 옵션 A+ 자기완결 — 외부 스킬은 명시 호출만.
when_to_use: 저자가 `/bookwriting seed|cycle|simulate|status|list|history|skeleton|inbox|absorb|import|reroute|resume|promote|init` 호출 시. *책 쓰기 작업 외에는 발동 영구 금지*.
---

# bookwriting-master

> Phase 3-B 1주차 sprint 첫 실파일 (Round 18 저자 명령 — 옵션 A 진입).
> 본 SKILL.md는 `specs/bookwriting-master.md` SPEC 17 항목 풀 명세를 *실제 작동 코드*로 환원.

## TLDR

저자 책 쓰기 워크플로우의 *진입점·orchestrator*. 11 단계 마스터에게 위임하고 결과를 저자 HITL로 진행. 모든 결정론 작업은 `lib/*.py` 모듈 강제 호출 — LLM 추론 영구 금지.

## Triggers

- `/bookwriting seed "..."` — 새 시드 등록 (`lib/id_generator.py` 호출 → S-NNN 발급)
- `/bookwriting cycle <target>` — 모드 1 정밀 사이클 (target = S-NNN | ch-NN | --all)
- `/bookwriting simulate <target>` — 모드 2 전자동 시뮬레이션
- `/bookwriting status` — cycle-registry·seed-registry 현재 상태 보고
- `/bookwriting list seeds|chapters|cycles` — 목록 조회
- `/bookwriting init` — 부트스트랩 (Round 4 #A8.1)

## Detailed Methodology

### 1. 사이클 진입 (Mode 1 — 저자 감독)

```
저자: /bookwriting cycle ch01
  → Step 1: book-config.yaml 로드 (yaml.safe_load — Round 8 #D3.1 강제)
  → Step 2: seed-registry·cycle-registry 로드
  → Step 3: lib/id_generator.IdGenerator.issue("cycle", max_num) → C-NNN
  → Step 4: 11 단계 마스터 순차 호출 (① absorb → ⑪ cross-chapter-relink)
  → Step 5: 각 단계 출력에 voice-gate + citation-gate cross-cutting 자동 발동
       - lib/voice_scoring.VoiceScorer.compute_voice_score(output_text)
       - lib/citation_detection.HallucinationDetector.detect_all(text, citation)
  → Step 6: 저자 HITL (3-5회 통합 묶음)
  → Step 7: lib/atomic_writer.AtomicWriter.write(chapter_path, content)
  → Step 8: cycle-registry entry 추가 (entry_sha256·previous_entry_hash 체인)
```

### 2. 사이클 진입 (Mode 2 — 전자동 시뮬레이션)

Mode 1과 동일하나 저자 HITL 0회·산출물은 `chapters/<ch>/_simulations/sim-NNN.md`로만.
정식 chapter 파일·seed-registry 미갱신. `/bookwriting promote SIM-NNN`로 정식 진입.

### 3. 결정론 모듈 강제 호출 (저자 진북 #7)

| 작업 | 결정론 모듈 | LLM 추론 금지 |
|---|---|---|
| voice_score 계산 | `lib/voice_scoring.VoiceScorer` | "0.83 정도일 것" |
| 할루시네이션 감지 | `lib/citation_detection.HallucinationDetector` | "형식 모호한 듯" |
| ID 발급 | `lib/id_generator.IdGenerator.issue()` | "S-007 같다" |
| 파일 쓰기 | `lib/atomic_writer.AtomicWriter.write()` | 직접 open/write |

### 4. 자산 풀 제한 (옵션 A+)

`book-config.yaml::search_paths.tier_1_always` + `tier_2_explicit`만 허용. 외부 web·MCP 자동 호출 영구 금지 (단 `bookwriting-notebooklm-bridge` 저자 명시 호출 예외).

### 5. 가드 11종 (Cross-cutting)

1. Voice Gatekeeper — voice_score < 0.7 시 재작성 1회
2. Citation Gatekeeper — Critical 신호 시 즉시 차단
3. Legal Gatekeeper — defamation·right of publicity·fair use 4 factor
4. Safe Messaging Gatekeeper — 자살·정신건강 민감 주제 WHO 가이드라인
5. Medical Claim Gate — 의학적 주장 disclaimer 강제
6. Quantitative Unit Gate — 정량 앵커 단위 강제 (예: "100배 GDP")
7. Theological Review Gate — 저자 imago Dei 정합 (선택)
8. Senior Accessibility Gate — 60-70대 독자 인지 부하
9. Diversity Gatekeeper — 권위 풀 분포 추적
10. Ecological Gatekeeper — 5장·9장 생태 차원
11. Author Wellness Gatekeeper — 저자 본인 수면·일일 사이클 상한 (Round 17 #J2.1)

### 6. Orchestrator Trace 강제 (저자 메모리 7번째 절대 protocol)

마스터가 각 sub-skill 호출 시점·순서·산출물을 명시적 trace로 기록한다. **Inline 시뮬레이션 단독 영구 금지** — 모든 sub-skill 호출은 `lib/orchestrator_tracer.OrchestratorTracer`로 결정론 기록.

```python
from orchestrator_tracer import OrchestratorTracer
tracer = OrchestratorTracer()
tracer.add_step(
    skill_name="bookwriting-fact-anchor-master",  # ②
    invocation_type="auto",
    inputs_summary={"seed_id": "S-001"},
    outputs_summary={"facts_extracted": 4, "duplicates": 0},
    deterministic_modules_used=["M10", "M4"],
    lifecycle_before="SEED",
    lifecycle_after="LINKED",
    status="completed",
)
# ... 11 단계 + voice-gate + citation-gate 모두 trace 기록
compliance = tracer.assert_protocol_compliant()
assert compliance["compliant"], compliance["violations"]
```

### 7. 저자 진북 #4 작가성 게이트

⑦ content-expand·⑧ narrative-craft·⑩ line-edit는 저자 본문 입력 후에만 진입. 마스터 orchestrator는 ⑥ insight-synthesis 도달 후 *자동 진행 중단 + 저자 escalate*:

```
next_stage_blocked = {
    "stage": "content_expand",
    "blocked": True,
    "reason": "저자 진북 #4 — INSIGHTED 시드의 본문 확장은 저자 직접 작성 필요",
    "action_required": "저자 절·소절 본문 입력 후 ⑦ content-expand 호출",
}
```

### 8. Phase 3-B 8주차 sprint 현황

구현 완료 (16 결정론 모듈 + 14 SKILL.md):
- ✅ lib: M1-M13 + M14 AuthorWellnessGatekeeper + M15 TraumaWitnessDetector + M16-A RiskAssessor + M17 AtomicWriter + M18 OrchestratorTracer
- ✅ SKILL.md: master + voice-gate + citation-gate + **11 단계 마스터 ①~⑪ 전 완성**
- ✅ 영속 자산: seed-registry S-001 + cycle-registry C-001~C-004 (SEED → INSIGHTED) + forecast-registry P-001 + sim-registry SIM-001
- ✅ pytest: 100/100 통과

미구현 (Phase 3-C — 저자 사용자 진입):
- ⑦~⑪ 저자 본문 입력 후 실제 진행
- bookwriting-notebooklm-bridge SKILL.md (선택)
- Sub-skill (각 단계 마스터 sub) — 저자 사용 후 필요 시 확장

## 저자 진북 7개 매핑

1. **할루시네이션 0**: lib/citation_detection 결정론 + yaml.safe_load 강제
2. **grill-me 일치**: `_progress/grill-me-decisions.md` 25 결정 청사진
3. **출처 명시**: `expert_pool/citation-authority-db.yaml` 57 권위 entry + 7 grade (A·A_preprint·B·C·D·E·F·G)
4. **저자 작가성**: Phase 3-B 진입 — 실제 작동 시스템 (Round 18 #K10.1 수정)
5. **법적 위험**: trauma_bearing_witness_category protocol + Legal Gatekeeper
6. **정신건강·취약 독자**: Safe Messaging + Author Wellness Gatekeeper
7. **결정론 환원**: lib/ 4 핵심 모듈 + M5-M18 후속

## 사용 예시

```bash
# 1. 부트스트랩
/bookwriting init
✅ book-config.yaml 검증 통과
✅ seed-registry.yaml·cycle-registry.yaml 검증 통과

# 2. 첫 시드 등록
/bookwriting seed "AGI는 단순히 더 똑똑한 AI가 아니라 메타 도구다"
✅ S-001 발급
✅ 저자 라우팅 묶음 제안

# 3. 챕터 사이클
/bookwriting cycle ch00-prologue
✅ C-001 사이클 시작
✅ 11 단계 마스터 위임 (현재는 stub — Phase 3-B 후속 sprint에서 실구현)
```

## 출처

- SPEC: `cys-bookwriting-skills/specs/bookwriting-master.md` (17 항목 풀)
- 결정론 모듈: `cys-bookwriting-skills/expert_pool/deterministic-modules.md` (M1-M18)
- 권위 DB: `cys-bookwriting-skills/expert_pool/citation-authority-db.yaml` (57 권위)
- grill-me 청사진: `cys-bookwriting-skills/_progress/grill-me-decisions.md` (25 결정)
- 저자 v1: `$BOOK_ROOT/workflows/book-planning.md`
- 책 외골격: `$BOOK_ROOT/bookidea/skeleton.md` (95KB)
