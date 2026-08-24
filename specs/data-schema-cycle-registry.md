# SPEC: data-schema-cycle-registry.yaml

> bookwriting의 *사이클 단일 진실 공급원*. 저자가 호출한 모든 사이클(모드 1·2)의 *상태·진행·트레이스·결정*을 *영속 추적*.
>
> 작성일: 2026-05-24
> 양식: 데이터 schema 전용 10 항목

---

## 1. Identity

| 항목 | 값 |
|---|---|
| Schema 이름 | `cycle-registry.yaml` |
| 카테고리 | Data Schema (사이클 마스터) |
| 파일 위치 | `$BOOK_ROOT/master/cycle-registry.yaml` |
| 작성·갱신 주체 | bookwriting-master (자동) — 저자 직접 편집 거의 없음 |

---

## 2. Purpose

bookwriting이 진행한 *모든 사이클*을 *영속적으로 기록*한다. 저자가 *언제든* 사이클을 *중단·재개·검토·아카이브*할 수 있는 *단일 진실 공급원*.

**6대 책임:**
1. **사이클 ID 유일성** — C-NNN (모드 1) / SIM-NNN (모드 2)
2. **상태 추적** — RUNNING·PENDING_DECISION·COMPLETED·DEFERRED·ABORTED·INTERRUPTED·PROMOTED
3. **진행 위치** — current_phase·completed_phases·next_phase
4. **저자 결정 추적** — pending_decisions·deferred_decisions·resolved_decisions
5. **트레이스 누적** — invoked_sub_skills·outputs·매크로 카운터
6. **resume 지원** — 중단된 사이클의 정확한 재진입점

---

## 3. Scope

### In scope
- ✅ 모든 사이클 (모드 1 정밀·모드 2 시뮬레이션) 메타데이터
- ✅ 사이클의 *진행 위치·상태·결정·트레이스*
- ✅ 동시 다중 사이클 추적 (소프트 제한 5개)
- ✅ 매크로 트리거 카운터

### Out of scope
- ❌ 시드 lifecycle 자체 (seed-registry.yaml 담당)
- ❌ chapter 작업물 (chapters/<ch>/*.md 담당)
- ❌ 사이클의 *상세 행동 trace* (chapters/<ch>/pipeline-log.md 담당 — cycle-registry는 *요약 trace*만)

---

## 4. Structure (필드 정의)

```yaml
# $BOOK_ROOT/master/cycle-registry.yaml

version: "2.0"
schema: cycle-registry
created: 2026-05-24
last_updated: 2026-05-24
cycle_count: 0
sim_count: 0
active_count: 0                         # RUNNING + PENDING_DECISION + INTERRUPTED
next_cycle_id: C-001
next_sim_id: SIM-001

# 글로벌 카운터 (매크로 트리거용)
global_counters:
  total_micro_cycles: 0                 # 누적 마이크로 사이클 수
  micro_since_last_relink: 0            # ⑪ relink 이후 마이크로 카운트
  micro_since_last_structure: 0         # ⑨ structure-review 이후
  evidenced_seeds_pending: 0             # EVIDENCED 도달했으나 ⑥ insight-synthesis 미진행 시드 수

cycles:
  - id: C-007
    type: cycle                          # cycle (모드 1) | simulate (모드 2) | resume | promote
    started: 2026-05-24T15:30:00Z
    last_action: 2026-05-24T16:45:00Z
    completed: null                      # 완료 시 timestamp
    duration_seconds: 4500                # last_action - started
    
    # ───────────────────────────────────────────
    # 1. 상태
    # ───────────────────────────────────────────
    status: PENDING_DECISION             # RUNNING | PENDING_DECISION | COMPLETED | DEFERRED | ABORTED | INTERRUPTED | PROMOTED
    status_reason: "저자 묶음 결정 대기 — 통찰 5개 중 a·b 추천"
    
    # ───────────────────────────────────────────
    # 2. 사이클 단위·target
    # ───────────────────────────────────────────
    target_type: CHAPTER                 # SEED | SECTION | CHAPTER | MULTI_CHAPTER | FULL_BOOK | RESUME
    target_id: ch01-economy
    target_seeds: [S-007, S-012, S-018, S-024, S-031]    # 사이클이 다루는 시드 ID 목록
    mode: 1                              # 1 (정밀) | 2 (시뮬레이션)
    variant: null                         # mode 2일 때만 (예: "insight-driven")
    
    # ───────────────────────────────────────────
    # 3. 진행 위치
    # ───────────────────────────────────────────
    progress:
      current_phase: 5                   # 1-11 (단계 마스터 인덱스)
      current_phase_name: "evidence-link-master"
      completed_phases: [1, 2, 3, 4]
      completed_phase_names: ["absorb", "fact-anchor", "systemlink", "evidence-collect"]
      next_phase: 6                       # ⑤ 종료 후 다음
      next_phase_name: "insight-synthesis-master"
      total_phases: 11                    # CHAPTER 프리셋 전체 단계
      progress_percent: 45.5              # (completed + 0.5*current) / total * 100
    
    # ───────────────────────────────────────────
    # 4. 저자 결정 풀
    # ───────────────────────────────────────────
    pending_decisions:                    # 저자 응답 대기 묶음
      - decision_id: D-007
        type: insight_selection
        phase: 6                          # 어느 단계에서 생성된 묶음
        created: 2026-05-24T16:30:00Z
        options:
          - id: a
            text: "AGI = 메타도구 + 가축화 도구 동시성"
            recommended: true            # ★
          - id: b
            text: "UBI(지능) > UBI(소득) 명제 강화"
            recommended: true            # ★
          - id: c
            text: "기술적 사춘기 = 가소성 손실 임계점"
            recommended: false
          - id: d
            text: "..."
            recommended: false
          - id: e
            text: "..."
            recommended: false
        deferred: false                   # defer 명시 시 true
      
      - decision_id: D-008
        type: routing_addition
        phase: 11
        ...
    
    resolved_decisions:                   # 저자가 이미 결정한 묶음
      - decision_id: D-001
        phase: 3
        decided_at: 2026-05-24T15:50:00Z
        response: "1=a,b / 2=skip"
        accepted_options: ["a", "b"]
        skipped: false
      - ...
    
    deferred_decisions:                   # 저자가 defer로 보류
      - decision_id: D-004
        phase: 4
        deferred_at: 2026-05-24T16:10:00Z
        carry_to: next_cycle              # 다음 사이클 시작 시 우선 제시
    
    # ───────────────────────────────────────────
    # 5. 호출된 sub-skills 트레이스 (요약)
    # ───────────────────────────────────────────
    invoked_sub_skills:
      - timestamp: 2026-05-24T15:35:00Z
        skill: bookwriting-absorb-inbox-scan
        master: bookwriting-absorb-master
        duration_seconds: 12
        result_summary: "inbox 3 파일 발견, type 분류 완료"
      - timestamp: 2026-05-24T15:38:00Z
        skill: bookwriting-systemlink-asset-index
        master: bookwriting-systemlink-master
        duration_seconds: 45
        result_summary: "Obsidian vault 8개 자산 연결, foresight-skill 폴더 3개 자산 연결"
      # ... (모든 sub 호출)
    
    # ───────────────────────────────────────────
    # 6. 매크로 트리거 카운터 (사이클별)
    # ───────────────────────────────────────────
    macro_counters:
      micro_since_last_relink: 4         # 임계값 5에 미달
      evidenced_count: 3                  # 임계값 5에 미달
      polished_ratio: 0.0                 # 임계값 80%에 미달
      will_trigger_macro: false           # 다음 단계에 매크로 발동 예정 여부
    
    # ───────────────────────────────────────────
    # 7. 산출물 추적
    # ───────────────────────────────────────────
    outputs:
      modified_files:
        - path: chapters/01-economy/analysis.md
          chars_added: 1800
          chars_removed: 200
        - path: chapters/01-economy/evidence-track.yaml
          predictions_added: [P-019, P-020]
        - path: master/seed-registry.yaml
          seeds_modified: [S-007, S-012, S-018, S-024, S-031]
      
      created_files: []
      
      voice_gate_results:
        total_outputs_scanned: 15
        violations_detected: 2
        violations_auto_resolved: 2
        violations_escalated: 0           # 저자 묶음으로 escalate된 위반
      
      # ⭐ Citation Gate 결과 (저자 Q33 후속 명령)
      citation_gate_results:
        total_citations_scanned: 23
        critical_violations: 0            # 할루시네이션 의심 — 0 유지가 목표
        high_violations: 1                # 메타데이터 불완전·R4 단일 권위
        medium_warnings: 2                # 권위 약함 (Grade E만)
        low_warnings: 0
        escalated_to_user: 1
        authority_distribution:
          A: 8                            # Layer 1 창업자 증언
          B: 7                            # Layer 2 미래학자 시스템 사고
          C: 4                            # Layer 3 인접 학문
          D: 2                            # Layer 4 사상가
          E: 2                            # Layer 5 역사 평행
          suspicious: 0                   # 할루시네이션 의심
        r4_multilayer_pass_rate: 0.92     # 다층 인용 통과율
        hallucination_blocks: 0           # 자동 차단된 인용 수
    
    # ───────────────────────────────────────────
    # 8. 트레이스 로그 위치
    # ───────────────────────────────────────────
    trace_log_path: chapters/01-economy/pipeline-log.md     # 상세 trace는 챕터 pipeline-log 참조
    
    # ───────────────────────────────────────────
    # 9. 저자 메모
    # ───────────────────────────────────────────
    notes: "이 사이클에서 메타도구 명제의 cross-chapter 가능성 발견. 다음 사이클에서 확장 검토."
    
    # ───────────────────────────────────────────
    # 10. 모드 2 전용 필드
    # ───────────────────────────────────────────
    sim_specific:
      auto_accepted_options:              # 자동 채택한 ★ 추천 옵션
        - decision_id: D-001
          accepted: ["a", "b"]
      simulation_artifact_path: chapters/01-economy/_simulations/sim-007.md
      can_promote: true                   # promote 가능 여부
    
    # ───────────────────────────────────────────
    # 11. 모듈 버전·재현성 추적 ⭐ (Round 5 #B6.3 High 수정)
    # ───────────────────────────────────────────
    lib_versions:
      voice_scoring: "0.1.0"
      citation_detection: "0.1.0"
      authority_grader: "0.1.0"
      quantitative_extraction: "0.1.0"
      layer_ratio_measurer: "0.1.0"
      relevance_scorer: "0.1.0"
      id_generator: "0.1.0"
      signature_pattern_applier: "0.1.0"
      ai_tone_purger: "0.1.0"
      fact_extractor: "0.1.0"
      lifecycle_state_machine: "0.1.0"
      forecast_registry_syncer: "0.1.0"
      r4_multi_layer_verifier: "0.1.0"
    
    # 12. 작가성 추적 ⭐ (Round 5 #B10.1·#B10.5 Critical)
    # ───────────────────────────────────────────
    authorship_tracking:
      user_intervention_score: 0.85       # 저자 *실응답* (자동 yes 제외) 비율
      ai_generation_ratio: 0.45            # AI 자동 생성 비율
      hitl_response_count_real: 11        # 저자 실제 응답 (defer·자동 yes 제외)
      hitl_response_count_auto_yes: 0     # 저자 자동 yes 비율 (정체성 표류 추적)
      mode_2_promote_from: null            # SIM-NNN promoted 여부
    
    # 13. 메타데이터 vs 본문 분리 ⭐ (Round 5 #B2.7 Critical 수정)
    # ───────────────────────────────────────────
    # *cycle-registry는 메타데이터만 보관*. chapter 본문에 메타데이터 침범 금지.
    # 본문에 메타데이터 포함 시 자동 제거·yaml frontmatter로 이동 강제.
    
    # 14. ⭐ Round 8 #D1.1·#D1.2·#D1.4 Critical — Audit Trail 강제
    # ───────────────────────────────────────────
    entry_sha256: "ab12cd34..."             # 이 entry 내용 SHA-256 (변조 검출)
    previous_entry_hash: "0f9e8d..."         # 이전 entry hash (체인)
    decided_by:                              # who 추적
      master: "bookwriting-master"            # 마스터 식별
      worker_session: null                    # 워커 사용 시
      terminal_hash: "sha256(cmux_session)"
    provenance_chain:                        # 시드 origin 역추적
      parent_seed_id: null
      parent_cycle_id: null
      parent_skill_name: null
    mode_2_log_path: _progress/mode2-decisions-append-only.log    # Mode 2 false attestation 차단
  
  # ─── SIM (모드 2) 사이클들 ───
  - id: SIM-007
    type: simulate
    ...

  # ─── 이전 완료된 사이클들 ───
  - id: C-006
    status: COMPLETED
    completed: 2026-05-23T...
    ...
```

---

## 5. Validation Rules

| 필드 | 규칙 | 위반 시 |
|---|---|---|
| `id` | 형식 `C-NNN` 또는 `SIM-NNN`, 유일성 | 중복 → bookwriting-master abort |
| `type` | enum [cycle·simulate·resume·promote] | enum 외 → 저자 알림 |
| `status` | enum [RUNNING·PENDING_DECISION·COMPLETED·DEFERRED·ABORTED·INTERRUPTED·PROMOTED] | enum 외 → 저자 알림 |
| `target_type` | enum [SEED·SECTION·CHAPTER·MULTI_CHAPTER·FULL_BOOK·RESUME] | enum 외 → abort |
| `target_seeds[]` | seed-registry에 존재 | 누락 → warning + 진행 |
| `progress.current_phase` | 1-11 정수 (또는 0 = 미시작) | 범위 외 → 저자 알림 |
| `progress.completed_phases` | current_phase 미만 | 위반 → 자동 정리 |
| `pending_decisions[].decision_id` | 형식 `D-NNN`, 유일성 (cycle 내) | 중복 → 자동 재발급 |
| `pending_decisions[].options` | 최소 2개 | 1개 이하 → 사이클 ABORT |
| `pending_decisions[].options[].recommended` | 최소 1개 ★ | ★ 없음 → 저자 알림 + 진행 |
| `macro_counters.*` | 정수, ≥0 | 음수 → 0 reset |
| `outputs.modified_files[].path` | 파일 존재 | 누락 → warning |
| 동시 active_count | book-config.cycle_triggers.concurrent_cycle_soft_limit 이하 | 초과 → warning + 저자 확인 |

---

## 6. Usage Examples

### 예시 1: 새 사이클 시작
```yaml
# 저자: /bookwriting cycle ch01
# bookwriting-master가 cycle-registry에 신규 등록
cycles:
  - id: C-007                          # next_cycle_id에서 발급
    type: cycle
    started: 2026-05-24T15:30:00Z
    status: RUNNING
    target_type: CHAPTER
    target_id: ch01-economy
    target_seeds: [...]                 # seed-registry에서 ch01 라우팅 시드 자동 수집
    mode: 1
    progress:
      current_phase: 1
      completed_phases: []
      next_phase: 2
      progress_percent: 9.1
    pending_decisions: []
    ...
```

### 예시 2: 저자 HITL 묶음 생성
```yaml
# ⑥ insight-synthesis-master 완료 시
cycles:
  - id: C-007
    status: PENDING_DECISION
    pending_decisions:
      - decision_id: D-007
        type: insight_selection
        phase: 6
        options:
          - id: a
            text: "AGI = 메타도구 + 가축화 도구 동시성"
            recommended: true
          - id: b
            ...
```

### 예시 3: 저자 응답 처리
```bash
# 저자: "1=a,b"
# bookwriting-master가 D-007을 resolved로 이동
```
```yaml
cycles:
  - id: C-007
    status: RUNNING                     # 다음 단계로 진행
    pending_decisions: []               # D-007 제거
    resolved_decisions:
      - decision_id: D-007
        phase: 6
        decided_at: 2026-05-24T16:50:00Z
        response: "1=a,b"
        accepted_options: ["a", "b"]
        skipped: false
```

### 예시 4: 사이클 중단·재개
```bash
# 저자가 Ctrl+C로 중단
```
```yaml
cycles:
  - id: C-007
    status: INTERRUPTED
    progress:
      current_phase: 7                 # 현재 단계 보존
      ...
```
```bash
# 저자: /bookwriting cycle resume C-007
```
```yaml
cycles:
  - id: C-007
    status: RUNNING                    # INTERRUPTED → RUNNING
    last_action: 2026-05-25T09:00:00Z  # 갱신
```

### 예시 5: 시뮬레이션 → promote
```bash
# 저자: /bookwriting simulate ch01
# SIM-007 생성, 완료
```
```yaml
cycles:
  - id: SIM-007
    type: simulate
    status: COMPLETED
    sim_specific:
      can_promote: true
```
```bash
# 저자: /bookwriting promote SIM-007
```
```yaml
cycles:
  - id: SIM-007
    status: PROMOTED
    notes: "C-009로 promote됨"
  - id: C-009
    type: promote
    promoted_from: SIM-007
    status: RUNNING
    ...
```

---

## 7. Lifecycle

### 생성
- **시점**: 저자 `/bookwriting cycle|simulate|resume|promote` 호출 시
- **방법**: `next_cycle_id` 또는 `next_sim_id`에서 발급
- **첫 상태**: `status: RUNNING`, `progress.current_phase: 1`

### 갱신
- **bookwriting-master 자동 갱신**: 단계 전환·저자 응답 처리·매크로 트리거 평가·산출물 추가
- **단계 마스터들도 일부 갱신**: invoked_sub_skills에 추가·outputs.modified_files 추가
- **저자 직접 편집**: notes 추가 (드물게)

### 삭제·아카이브
- **삭제 없음**: 사이클 기록은 영속 (감사·검토용)
- **아카이브 트리거**: cycle-registry의 cycles[] 길이가 `book-config.cycle_triggers.registry_archive_threshold` (기본 100) 초과 시
- **아카이브 동작**: 가장 오래된 COMPLETED·PROMOTED·ABORTED 사이클 N개를 `master/cycles-archive-YYYY.yaml`로 이동
- **active 사이클은 절대 아카이브 안 됨**: RUNNING·PENDING_DECISION·INTERRUPTED·DEFERRED는 cycle-registry에 잔류

### 검증
- **시점**: bookwriting-master 모든 호출 시 G2 게이트
- **방법**: Validation Rules 검증

---

## 8. Dependencies

### 이 schema를 *읽는* 스킬
- **bookwriting-master** (모든 행동의 기반)
- **status·list·history 모드** (cycle-registry 직접 조회)
- **resume 모드** (INTERRUPTED·PENDING_DECISION 사이클 검색)

### 이 schema를 *쓰는* 스킬
- **bookwriting-master**: 사이클 생성·status 전환·저자 응답 처리·outputs 추가
- **모든 단계 마스터**: invoked_sub_skills에 자기 호출 기록·outputs 갱신

### 외부 참조
- **seed-registry.yaml**: target_seeds·cycle_history 양방향 일관성
- **book-config.yaml**: cycle_triggers·concurrent_cycle_soft_limit·registry_archive_threshold
- **chapters/<ch>/pipeline-log.md**: 상세 trace 본문 (cycle-registry는 요약 trace만)

---

## 9. Error Handling

| 실패 시나리오 | 대응 |
|---|---|
| next_cycle_id 동기화 실패 | cycles[] max ID + 1 재계산 + 저자 알림 |
| 동시 사이클 5개 초과 | warning + 저자 확인 → 진행 또는 거부 (옵션 저자 결정) |
| 사이클 ABORT (부분 진행 상태) | partial 상태 *보존* + status: ABORTED + 저자 알림. *resume 가능* |
| Ctrl+C 인터럽트 | status: INTERRUPTED 자동 저장 + 모든 partial 상태 보존 + resume 가능 |
| pending_decisions 누적 (10개 초과) | warning + 저자 일괄 검토 권장 |
| voice gate 위반 자동 해소 실패 | voice_gate_results.violations_escalated 증가 + pending_decisions에 추가 |
| target_seeds의 시드 누락 | warning + 해당 시드 skip + 다음 시드 진행 |
| 사이클 timeout (3시간 초과) | status: INTERRUPTED 자동 전환 + 저자 알림 |
| 단계 마스터 호출 실패 | invoked_sub_skills에 실패 기록 + status: PENDING_DECISION + 저자 결정 요청 |
| yaml 손상 | 백업 자동 복원 시도 + 저자 알림 + 실패 시 abort |

---

## 10. Verification Examples

### 검증 1: 사이클 생성·ID 발급
```bash
$ /bookwriting cycle ch01
$ grep "id: C-" cycle-registry.yaml | tail -1
✅ "  - id: C-007"
$ grep "next_cycle_id:" cycle-registry.yaml
✅ "next_cycle_id: C-008"
$ grep -A2 "id: C-007" cycle-registry.yaml | grep "status:"
✅ "status: RUNNING"
```

### 검증 2: 저자 HITL → 응답 처리
```bash
# 저자 응답: "1=a,b"
$ grep -A5 "decision_id: D-007" cycle-registry.yaml | grep "decided_at:"
✅ resolved_decisions에 이동
✅ "decided_at: 2026-05-24T16:50:00Z"
$ grep "status:" cycle-registry.yaml | head -1
✅ "status: RUNNING" (PENDING_DECISION → RUNNING 전환)
```

### 검증 3: 사이클 중단·재개
```bash
# Ctrl+C 인터럽트
$ grep "status: INTERRUPTED" cycle-registry.yaml
✅ 자동 저장됨
$ grep -A3 "id: C-007" cycle-registry.yaml | grep "current_phase:"
✅ current_phase 보존 (예: "current_phase: 7")

# 재개
$ /bookwriting cycle resume C-007
$ grep -A3 "id: C-007" cycle-registry.yaml | grep "status:"
✅ "status: RUNNING" (INTERRUPTED → RUNNING)
```

### 검증 4: 매크로 트리거 작동
```bash
# 마이크로 사이클 5회 누적 후
$ grep "micro_since_last_relink:" cycle-registry.yaml | head -1
✅ "  micro_since_last_relink: 5"
$ /bookwriting status
✅ "매크로 권장: ⑪ cross-chapter-relink 발동"
```

### 검증 5: 시뮬레이션 → promote
```bash
$ /bookwriting simulate ch01
$ grep "id: SIM-007" cycle-registry.yaml
✅ SIM-007 등록됨
$ grep -A2 "id: SIM-007" cycle-registry.yaml | grep "can_promote:"
✅ "can_promote: true"

$ /bookwriting promote SIM-007
$ grep -A2 "id: SIM-007" cycle-registry.yaml | grep "status:"
✅ "status: PROMOTED"
$ grep "promoted_from:" cycle-registry.yaml
✅ "promoted_from: SIM-007"
```

### 검증 6: 아카이브 작동
```bash
# 100개 초과 시
$ wc -l cycle-registry.yaml
✅ 큰 폭 감소 (오래된 COMPLETED 이동됨)
$ ls master/cycles-archive-*.yaml
✅ 아카이브 파일 존재
```

---

**End of SPEC: data-schema-cycle-registry**
