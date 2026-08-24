# SPEC: bookwriting-master

> 기준 모델 (Reference Model). 다른 모든 SPEC이 이 양식을 따른다.
> 
> 작성일: 2026-05-24
> 합의 기반: grill-me Phase 1 — 저자와 합의된 25 주요 결정 + 11 sub 결정

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-master` |
| 카테고리 | 메타 마스터 (Top-level orchestrator) |
| 저자 11 단계 매트릭스 위치 | 최상위 — 모든 11 단계 마스터를 위임·orchestration |
| 저자 진짜 워크플로우 매핑 | 14·15단계 + 전체 흡수·통합·정합성·매력 글쓰기·voice 영역 *오케스트레이션* |
| 스킬 디렉토리 | `~/.claude/skills/bookwriting-master/` |
| 슬래시 prefix | `/bookwriting` |

---

## 2. Purpose (목적)

bookwriting 워크플로우의 *진입점·orchestrator·trace 발신자*. 저자의 시드·명령을 받아 11 단계 마스터에 위임하고, 결과를 집약하여 저자 HITL을 진행한다.

**저자 진짜 워크플로우 15단계 중 책임:**
- 1-13단계 (foresight 사슬) = **책임 밖** (저자 외부 manual)
- 14단계 (의미·영향력·놀라움 단면 선택) = `bookwriting-insight-synthesis-master`에 위임
- 15단계 (매력적 글쓰기) = `bookwriting-content-expand-master` + `bookwriting-narrative-craft-master` + `bookwriting-line-edit-master`에 위임
- 통합·흡수·정합성·voice = `absorb`·`fact-anchor`·`systemlink`·`evidence-link`·`structure-review`·`cross-chapter-relink`에 위임

**bookwriting-master 본인의 책임:**
- 위임 결정 (어느 단계 마스터를 어느 순서로)
- Trace 누적·집약
- 저자 HITL 진행 (모드 1) 또는 자동 진행 (모드 2)
- Voice cross-cutting gate 발동
- 사이클 상태 관리 (cycle-registry·seed-registry·chapter 파일)

---

## 3. Philosophy (철학)

**저자 8 절대 protocol 중 적용:**
- **#4** (AgenticWorkflow master 패턴): master orchestrator는 inline protocol, 워커가 직접 실행. 2단 nested sub-agent 위임 금지. → bookwriting-master는 *Skill 도구로 단계 마스터 호출*, 그 안에서 sub-agent 재위임 안 함.
- **#5** (3-Layer Description Template): `## TLDR + ## Triggers + ## Detailed Methodology` 양식 강제.
- **#6** (Sub-skill naming): 모든 sub는 `bookwriting-` prefix.
- **#7** (Master Orchestration Trace 강제): 각 sub-skill 호출 시점·순서·산출물을 *명시적 trace*로 표시.

**저자 v1 원칙 준수:**
- *로컬 실행 보장* — Read·Write·Edit·Bash·Glob·Grep만 사용. API/SDK 호출 없음.

**bookwriting 옵션 A+ 완전 자기완결:**
- 설치된 다른 스킬을 자동 호출하지 않는다
- 저자가 외부에서 manual 호출 후 결과를 inbox·import로 전달
- bookwriting은 *그 결과를 매력적 글로 변환*에 집중

**Voice는 cross-cutting:**
- 모든 단계 마스터 출력에 voice gate 자동 발동
- 위반 시 자동 재작성 1회 → 실패 시 저자 묶음 제안

---

## 4. Scope (책임 영역)

### In scope (담당)
- ✅ 사이클 진입·계획·orchestration
- ✅ 11 단계 마스터 위임 + trace 누적
- ✅ 저자 HITL 진행 (모드 1) 또는 자동 진행 (모드 2)
- ✅ Voice cross-cutting gate 발동
- ✅ book-config·seed-registry·cycle-registry 읽기·쓰기
- ✅ 사이클 결과 집약 + 저자 보고
- ✅ inbox 관리·라우팅 결정
- ✅ 시뮬레이션 → 정식 사이클 promote

### Out of scope (담당 안 함)
- ❌ 실제 분석·검색·근거 수집·통찰 추출·글쓰기 작업 (각 단계 마스터 담당)
- ❌ 다른 스킬 자동 호출 (옵션 A+ 원칙)
- ❌ foresight 사슬 (envscan·delphi·scenarios 등) 직접 실행 (저자 외부 manual)
- ❌ NotebookLM 직접 query (`bookwriting-notebooklm-bridge`가 별도 담당)
- ❌ Obsidian vault 직접 검색 (단계 마스터가 grep/glob으로 자체 수행)
- ❌ 책 외부 영역 (다른 책·일반 작업) — bookwriting은 *책 한 권의 워크플로우*

---

## 5. Capabilities (기능)

| 모드 | 슬래시 | 목적 | 트리거 |
|---|---|---|---|
| **init** ⭐ | `/bookwriting init` | **부트스트랩 — book-config·seed-registry·cycle-registry 기본 템플릿 자동 생성** (Round 4 #A8.1·#A8.2 수정) | 저자 *최초 실행* + 필수 파일 누락 자동 감지 |
| seed | `/bookwriting seed "..."` | 새 시드 등록 | 저자 시드 입력 |
| cycle | `/bookwriting cycle <target>` | 모드 1 정밀 사이클 | 저자 실제 원고 작업 |
| simulate | `/bookwriting simulate <target> [--variant]` | 모드 2 전자동 시뮬레이션 | 저자 방향 탐색 |
| promote | `/bookwriting promote SIM-NNN` | 시뮬레이션 → 정식 사이클 | 저자 방향 결정 후 |
| dispatch | `/bookwriting dispatch S-NNN` | 글감 라우팅 결정 | 시드 라우팅 미결 시 |
| reroute | `/bookwriting reroute S-NNN --to ch07` | 시드 재라우팅 | 저자 명시 |
| import | `/bookwriting import <path> --as <type> [--to|--link]` | 외부 파일 즉시 흡수 | 저자 외부 결과 가져옴 |
| absorb | `/bookwriting absorb` 또는 `inbox process` | inbox 일괄 흡수 | inbox에 미처리 파일 누적 시 |
| status | `/bookwriting status` | 진행 상태 보고 | 저자 조회 |
| list | `/bookwriting list seeds|chapters|cycles` | 목록 조회 | 저자 조회 |
| history | `/bookwriting history` | 사이클 히스토리 | 저자 조회 |
| skeleton | `/bookwriting skeleton` | 외골격 v2 확인·업데이트 | 저자 조회·수정 |
| resume | `/bookwriting cycle resume [C-NNN|--pending]` | 중단 사이클 재개 | 저자 이어가기 |

---

## 6. Invocation (호출 방식)

**예시 호출 5개:**

```bash
# 1. 시드 등록
/bookwriting seed "AGI는 단순히 더 똑똑한 AI가 아니라 메타 도구다"

# 2. 챕터 단위 정밀 사이클 (모드 1)
/bookwriting cycle ch01

# 3. 챕터 단위 시뮬레이션 (모드 2)
/bookwriting simulate ch01 --variant insight-driven

# 4. 외부 foresight 결과 즉시 흡수
/bookwriting import $BOOK_ROOT/inbox/2026-05-24-scenarios-output.md --as seed --to ch07

# 5. 시뮬레이션 → 정식 사이클 승격
/bookwriting promote SIM-007
```

**인자 파싱 규약:**
- 첫 인자 = mode (필수)
- `<target>`: 시드 ID (S-NNN), 챕터 ID (ch-NNN), 꼭지 ID (ch-NNN-section-N), `--all` (책 전체), 또는 없음 (default = 직전 컨텍스트)
- `--variant <name>`: simulate 모드의 방향 분기
- `--from-sim <SIM-NNN>`: cycle 모드의 시뮬레이션 시작점
- `--as <type>`: import의 type (seed|evidence|insight|cycle-input)
- `--to <ch-NNN>` / `--link <S-NNN>`: import의 라우팅 명시
- `--pending`: pending 상태 일괄 처리

---

## 7. Behavior (작동 방식)

**9단계 행동 시나리오 (Q23-B에서 저자 확정):**

```
저자: /bookwriting cycle ch01

【Step 1: 입력 파싱·검증】
  - 호출 인자 파싱 (target_type, target_id, mode, options)
  - book-config.yaml 로드
  - skeleton.md에서 해당 챕터 외골격 로드
  - seed-registry.yaml에서 해당 챕터 라우팅 시드 추출
  - cycle-registry.yaml에 신규 사이클 ID 등록 (status: RUNNING)
  → trace: "[bookwriting-master] 사이클 C-NNN 시작 — ch01 챕터 단위"

【Step 2: 사이클 계획 수립】
  - target_type 프리셋 + 상태 미세 조정 (Q24 옵션 C)
  - 시드별 lifecycle 다음 단계 매트릭스 결정
  - 매크로 트리거 평가 (빈도·상태 둘 다)
  → trace: 단계 호출 순서 표시

【Step 3-9: 단계 마스터 위임 (target_type 프리셋 따라)】
  CHAPTER 프리셋: ① → ② → ③ → ④ → ⑤ → ⑥ → ⑦ → ⑧ → ⑨ → ⑩ → ⑪
  각 단계 마스터에 Skill 도구로 위임 (또는 명시 호출)
  - 모드 1: 각 단계 종료 후 저자 HITL (Q25 옵션 C 매트릭스 따라)
    - 결정적 단계 (①·④) → 빠른 confirm
    - 판단 단계 (⑥·⑦·⑧·⑩) → 정밀 묶음 제안
  - 모드 2: 각 단계 자동 채택 (★ 추천 옵션 선택) + 다음 단계 진행
  → trace: 각 단계 위임 + 결과 + HITL 응답 누적

【Step 4 (cross-cutting): Voice Gate】
  - 각 단계 출력에 자동 발동
  - voice_guidelines.vocabulary·sentence·prohibitions 검사
  - 위반 시 1회 재작성 시도 → 실패 시 저자 묶음 풀에 추가

【Step 10: 매크로 트리거 자동 발동 (해당 시)】
  - 사이클 끝에 매크로 임계값 재평가
  - 매크로 발동 시 ⑪·⑥·⑨ 추가 호출

【Step 11: 상태 갱신】
  - cycle-registry.yaml 사이클 status 갱신 (COMPLETED / PENDING_DECISION / DEFERRED)
  - seed-registry.yaml 시드 lifecycle·cycle_history 갱신
  - chapters/<ch>/*.md 파일 갱신 (모드 1만)
  - chapters/<ch>/_simulations/sim-NNN.md 생성 (모드 2만)

【Step 12: 저자 종합 보고】
  - 사이클 종합 trace 요약
  - 산출물 위치
  - 다음 권장 행동 (`/bookwriting cycle ch02` 또는 `/bookwriting cycle S-024` 등)
```

---

## 8. Input Schema (입력)

### 슬래시 인자 (필수)
```typescript
{
  mode: "seed" | "cycle" | "simulate" | "promote" | "dispatch" | "reroute" | "import" | "absorb" | "status" | "list" | "history" | "skeleton" | "resume"
  target?: string  // S-NNN | ch-NNN | ch-NNN-section-N | SIM-NNN | C-NNN | --all
  options: {
    variant?: string         // simulate 모드의 방향 분기
    from_sim?: string         // cycle 모드의 SIM 시작점
    as?: "seed" | "evidence" | "insight" | "cycle-input"
    to?: string              // 챕터 라우팅
    link?: string            // 시드 연결
    pending?: boolean        // pending 일괄 처리
  }
  free_text?: string         // seed 모드의 시드 텍스트
}
```

### 파일 입력 (필수)
- `$BOOK_ROOT/master/book-config.yaml` — 검색 경로·voice 가이드라인·매크로 트리거
- `$BOOK_ROOT/master/seed-registry.yaml` — 시드 마스터
- `$BOOK_ROOT/master/cycle-registry.yaml` — 사이클 히스토리
- `$BOOK_ROOT/bookidea/skeleton.md` — 외골격

### 파일 입력 (옵션·해당 시)
- `$BOOK_ROOT/inbox/*.md` — 미처리 글감
- `$BOOK_ROOT/master/forecast-registry.yaml` — v1 호환
- `$BOOK_ROOT/chapters/<ch>/seed-track.yaml` — 챕터별 시드 trace

---

## 9. Output Schema (출력)

### 저자 화면 (Markdown)
- Trace 누적 (단계별 행동·소요 시간·산출물 위치)
- 묶음 제안 (모드 1, 마크다운 헤더 + 리스트 + ★ 추천 — Q25-C-2 (b))
- 사이클 종합 보고
- 다음 권장 행동

### 파일 갱신·생성

| 파일 | 모드 1 (정밀) | 모드 2 (시뮬레이션) |
|---|---|---|
| `cycle-registry.yaml` | 갱신 (사이클 ID + status) | 갱신 (SIM-NNN ID 별도 분류) |
| `seed-registry.yaml` | 갱신 (lifecycle + cycle_history) | 미갱신 (시뮬레이션 임시 상태만) |
| `chapters/<ch>/*.md` | 갱신 (실제 원고) | 미갱신 |
| `chapters/<ch>/seed-track.yaml` | 갱신 | 미갱신 |
| `chapters/<ch>/pipeline-log.md` | 추가 (사이클 로그) | 미추가 |
| `chapters/<ch>/_simulations/sim-NNN.md` | 미생성 | 생성 (드래프트) |
| `forecast-registry.yaml` | 갱신 (신규 예측 발견 시) | 미갱신 |

---

## 10. Deliverable Quality (결과물 형태·수준)

### 성공 시나리오
- ✅ 저자 명시 호출에 *정확한 응답*
- ✅ 단계 마스터 위임 trace가 *완전·명확* (어떤 sub 호출됐는지 누락 없음)
- ✅ 저자 HITL 묶음이 *읽고 즉답 가능*한 형식 (마크다운 + ★ 추천 + 구조화 응답)
- ✅ Voice gate 위반 *자동 처리* 또는 *명확 알림*
- ✅ 사이클 끝에 *다음 권장 행동* 명확 제시
- ✅ 모든 registry·log 파일 *정합* 갱신
- ✅ 모드 1 산출물 = 저자 voice 80%+ 일치 + 저자 통찰 단면 명시 + 저자 통제 가능
- ✅ 모드 2 산출물 = 대략적 흐름 + 시뮬레이션임 명시 + 정식 파일과 분리

### 실패 시나리오
- ❌ 슬래시 인자 파싱 실패 → 저자에게 *명확한 오류 + 사용법* 출력
- ❌ 단계 마스터 호출 실패 → trace에 *실패 명시* + 사이클 PENDING_DECISION + 저자 결정 요청
- ❌ Voice gate 위반 재작성 실패 → 저자 *묶음 제안*에 추가
- ❌ Registry 파일 손상 → 백업에서 복원 시도 + 저자 알림
- ❌ 저자 응답 형식 오류 → 재요청 + 형식 안내

### 정량 기준
- **사이클 소요 시간**: 모드 1 = 15-30분 / 모드 2 = 5-10분
- **저자 HITL 회수**: 모드 1 = 약 11회 / 모드 2 = 0회 (사이클 끝에만 결과 검토)
- **Trace 분량**: 사이클당 50-150줄 markdown
- **Voice 일치도**: 저자 reference 풀과 80%+ 일치 (정량 측정 어렵지만 저자 spot-check)

---

## 11. Dependencies (의존)

### 필수 의존 (없으면 작동 불가)
- 11 단계 마스터 모두 (위임 대상)
  - `bookwriting-absorb-master`
  - `bookwriting-fact-anchor-master`
  - `bookwriting-systemlink-master`
  - `bookwriting-evidence-collect-master`
  - `bookwriting-evidence-link-master`
  - `bookwriting-insight-synthesis-master`
  - `bookwriting-content-expand-master`
  - `bookwriting-narrative-craft-master`
  - `bookwriting-structure-review-master`
  - `bookwriting-line-edit-master`
  - `bookwriting-cross-chapter-relink-master`
- `book-config.yaml`
- `seed-registry.yaml`
- `cycle-registry.yaml`
- `skeleton.md`

### 옵션 의존 (있으면 활용, 없어도 작동)
- `forecast-registry.yaml` (v1 호환)
- `chapters/<ch>/*.md` (기존 챕터 작업물)
- `inbox/*.md` (미처리 글감)
- `bookwriting-notebooklm-bridge` (외부 NotebookLM query)
- Obsidian vault (`$REFERENCE_ROOT/`)

### 명시적 비의존 (절대 호출 안 함)
- ❌ 설치된 다른 스킬 풀 (foresight·vision·sermon·churchadmin 모두)
- ❌ Web API (WebSearch·WebFetch도 모드 1·2 자동 사이클에서 안 부름. 저자 명시 호출 시만)
- ❌ MCP 외부 도구 (NotebookLM bridge는 별도 sub-skill로 분리)

---

## 12. Guards (가드)

### Voice cross-cutting gate
- 모든 단계 마스터 출력에 자동 발동
- `voice_guidelines.vocabulary·sentence·prohibitions` 검사
- 위반 시 1회 자동 재작성 → 실패 시 저자 묶음 제안 풀에 추가
- 메타 위치 (단계 마스터 안이 아님) — Q19-D-3 (c)

### Citation cross-cutting gate ⭐ (저자 Q33 후속 명령)
- 모든 단계 마스터 출력에 자동 발동 (voice gate와 동등 cross-cutting)
- `citation-gate.md` SPEC 참조 — 메타 위치 *Citation Gatekeeper 페르소나*
- 검증: source_file 실재 + 메타데이터 완전성 + 권위 5층 등급 (A·B·C·D·E) + R4 다층
- 위반 시 *재작성 안 함* — 즉시 저자 묶음 escalate
- Critical (할루시네이션 의심) → *즉시 차단*. High (메타·R4 위반) → 저자 묶음. Medium (권위 약함) → warning.
- 저자 진북: *"할루시네이션 없는 출처, 명확한 자료 출처, 가장 권위있는 근거자료와 그것의 출처까지 명확하게 출력"*

### 동시 사이클 가드
- 동시 진행 사이클 5개 *소프트 제한* (Q17-D-1)
- 6번째 사이클 시작 시 *경고 + 저자 확인* → 저자가 무시하고 진행 가능

### Registry 크기 가드
- cycle-registry 100개 초과 시 *오래된 COMPLETED 사이클부터 아카이브 권장* (Q17-D-2)
- 아카이브 파일: `master/cycles-archive-YYYY.yaml`

### 명시 모드 무시 가드
- 저자가 `/bookwriting cycle ch01 --only systemlink` 같은 명시 시 *프리셋 무시·저자 명시만 실행*

### Loop 방지 가드
- 동일 시드가 *재작성 무한 루프*에 빠지지 않도록 *한 사이클 내 동일 sub-skill 최대 3회* 호출 제한

---

## 13. AI Agents Personas (페르소나)

저자 envscan 6 AI Agents 패턴 변형. bookwriting-master 내부에서 *역할 분담*하는 6 페르소나:

| # | 페르소나 | 역할 | 권한 |
|---|---|---|---|
| 1 | **Orchestrator** | 사이클 흐름·계획 결정·target_type 프리셋 적용 | 단계 마스터 호출 순서 결정권 |
| 2 | **Router** | 시드 라우팅·재라우팅·dispatch 결정 | seed-registry 라우팅 필드 쓰기 권한 |
| 3 | **Trace Logger** | 행동 trace 실시간 출력·pipeline-log 누적 | 저자 화면 출력 + log 파일 쓰기 |
| 4 | **HITL Mediator** | 저자 묶음 제안 생성·응답 파싱·defer 처리 | 저자 묶음 형식·내용 결정권 (모드 1) |
| 5 | **Status Reporter** | 진행 상태·history·list 보고 | 모든 registry 읽기 권한 |
| 6 | **Voice Gatekeeper** | cross-cutting voice gate 발동·재작성·저자 알림 | 모든 단계 마스터 출력 가로채기 권한 |
| 7 | **Citation Gatekeeper** ⭐ | cross-cutting citation gate 발동·할루시네이션 차단·권위 5층 등급화·R4 검증 | 모든 단계 마스터 출력 *citation 검증* 권한 + 위반 시 즉시 저자 묶음 escalate (재작성 안 함) |
| 8 | **Legal Gatekeeper** ⭐⭐ (Round 7 #C3.7 Critical) | 법적 risk 검증 — 미국·한국 출판법·1st Amendment·defamation·right of publicity·fair use 4 factor·informed consent | 현존 인물 묘사·fair use·명예훼손·right of publicity 위반 검출 시 저자 묶음 escalate |
| 9 | **Safe Messaging Gatekeeper** ⭐⭐ (Round 7 #C10.1 Critical) | 정신건강·자살·우울·소외 주제 자동 감지 + WHO safe messaging guidelines 적용 | 정신건강 민감 주제에서 surprise_weight 자동 하향·hotline 명시 강제·자동 채택 영구 금지 |
| 10 | **Diversity Gatekeeper** (Round 7 #C6.6) | 권위 풀 성별·국적·분야 분포 추적 + 임계 미달 시 알림 | citation_distribution_audit 메트릭 발동 |
| 11 | **Author Wellness Gatekeeper** ⭐⭐ (Round 17 #J2.1 Critical) | 저자 본인 정신건강·수면·인지 부담 보호. 일일 사이클 상한·심야 차단·연속 작업 경고 | `daily_cycle_max: 3`·`late_night_block_after: "23:00"`·`consecutive_hour_warn: 2` 임계 위반 시 저자 작업 중단 권장 |

---

## 14. Cycle (C1-C7)

bookwriting-master의 *진입 모드 7개*:

| Cycle | 트리거 슬래시 | 작동 |
|---|---|---|
| **C1: SEED** | `/bookwriting seed "..."` | 시드 등록 + 라우팅 제안 + lifecycle SEED 시작 |
| **C2: CYCLE** | `/bookwriting cycle <target>` | 모드 1 정밀 사이클 (9단계 행동 시나리오) |
| **C3: SIMULATE** | `/bookwriting simulate <target>` | 모드 2 전자동 시뮬레이션 (HITL 0회) |
| **C4: PROMOTE** | `/bookwriting promote SIM-NNN` | 시뮬레이션 → 정식 사이클 승격 |
| **C5: RESUME** | `/bookwriting cycle resume` | 중단 사이클 재개 |
| **C6: STATUS** | `/bookwriting status|list|history|skeleton` | 진행 상태 조회 |
| **C7: ABSORB** | `/bookwriting absorb` 또는 `import` | inbox 일괄 흡수 + 시드 등록·라우팅 제안 |

---

## 15. Gates (검증 게이트)

저자 futures-wheel Gate 1-11 패턴과 일관:

| Gate | 검증 항목 | 통과 기준 |
|---|---|---|
| **G1: Input Parse** | 슬래시 인자 파싱 완료 | mode 식별 + target 식별 + options 파싱 |
| **G2: Config Load** | book-config·skeleton·registry 로드 | 필수 파일 모두 존재·읽기 가능 |
| **G3: Cycle Plan** | 사이클 계획 수립 완료 | target_type 프리셋 + 상태 미세 조정 적용 |
| **G4: Sub Delegation** | 모든 단계 마스터 위임 완료 | 프리셋 단계 모두 호출 + trace 누적 |
| **G5: Voice Gate Pass** | voice cross-cutting gate 통과 | 위반 0개 또는 저자 묶음 처리 완료 |
| **G6: Registry Update** | cycle-registry·seed-registry 갱신 완료 | 정합성 검증 통과 |
| **G7: Chapter Update** | chapter 파일 갱신 완료 (모드 1만) | 6 파일 schema 정합 |
| **G8: HITL Complete** | 저자 HITL 응답 처리 완료 (모드 1만) | 모든 묶음 결정됨 또는 defer 명시 |
| **G9: Macro Trigger** | 매크로 트리거 평가·발동 완료 | 임계값 검증 |
| **G10: Trace Output** | 저자 종합 trace 출력 | 사이클 ID + 위임 trace + 다음 권장 행동 |
| **G11: Cleanup** | 임시 상태·lock 해제 | 사이클 status FINAL 도달 |

Gate 위반 시 → 저자 묶음 제안 또는 사이클 PENDING_DECISION.

---

## 16. Error Handling (실패 처리)

| 실패 시나리오 | 대응 |
|---|---|
| 슬래시 파싱 실패 | 명확한 오류 + 사용법 출력 + 저자 재입력 요청 |
| 필수 파일 누락 (book-config 등) | ⚠ Round 4 #A8.1 수정 — *자동 init 부트스트랩 진입* (사이클 임시 중단·init 완료 후 사이클 자동 재개) + 저자 알림. 저자 명시 거부 시 ABORT |
| 단계 마스터 호출 실패 | trace에 실패 명시 + 사이클 PENDING_DECISION + 저자 결정 요청 |
| 단계 마스터 timeout (3분 초과) | 사이클 INTERRUPTED 상태 + 저자 알림 + resume 가능 |
| Voice gate 위반 재작성 실패 | 저자 묶음 제안에 추가 |
| 저자 응답 형식 오류 | 재요청 + 형식 안내 (`1=a,b / 2=skip` 형식) |
| 동시 사이클 5개 초과 | 경고 + 저자 확인 → 진행 또는 거부 |
| 사이클 중단 (Ctrl+C·재시작) | cycle-registry에 INTERRUPTED 상태 + 모든 partial 상태 보존 + resume 가능 |
| Registry 파일 손상 | 백업 자동 복원 시도 + 저자 알림 |
| Loop 감지 (동일 sub 3회 호출) | 사이클 ABORT + 저자 알림 |

---

## 17. Verification Examples (검증 예시)

저자가 후일 *명세-실제 대조*하는 기준 시나리오 5개:

### 검증 1: 시드 등록 + 라우팅 제안
```bash
# 입력
/bookwriting seed "AGI는 단순히 더 똑똑한 AI가 아니라 메타 도구다. 인지 자체를 확장하는 메타 도구."

# 기대 결과
✅ seed-registry.yaml에 S-NNN 신규 등록
✅ frontmatter 자동 생성 (id, created, seed_text, lifecycle=SEED)
✅ 저자에게 라우팅 제안 (skeleton.md의 사상적척추.§1 후보 + ch01·ch08·ch10 cross-reference 후보)
✅ 저자 응답 (`1=a / 2=b,c`) 파싱 → seed-registry 라우팅 필드 갱신
✅ Trace에 모든 행동 명시
```

### 검증 2: 챕터 단위 정밀 사이클 (모드 1)
```bash
# 입력
/bookwriting cycle ch01

# 기대 결과
✅ ch01 라우팅 시드 모두 추출 + 사이클 계획 수립
✅ ① absorb → ⑪ relink까지 프리셋 단계 모두 위임
✅ 각 단계 종료 후 저자 HITL (결정적 confirm 또는 정밀 묶음)
✅ Voice gate 위반 자동 처리·저자 알림
✅ chapters/01-economy/*.md 파일 갱신 (analysis·narrative·implications·evidence-track·pipeline-log·manuscript)
✅ cycle-registry·seed-registry 갱신
✅ 종합 보고 + 다음 권장 행동
✅ 저자 voice 80%+ 일치 (spot-check)
```

### 검증 3: 시뮬레이션 (모드 2)
```bash
# 입력
/bookwriting simulate ch01 --variant insight-driven

# 기대 결과
✅ ch01 사이클 전자동 진행 (HITL 0회)
✅ 저자 묶음 제안 자동 채택 (★ 추천 옵션)
✅ chapters/01-economy/_simulations/sim-NNN.md 생성 (드래프트 표시)
✅ 정식 chapter 파일 미갱신
✅ seed-registry 미갱신 (lifecycle 변경 없음)
✅ cycle-registry에 SIM-NNN 별도 분류 등록
✅ 5-10분 내 완료
```

### 검증 4: 시뮬레이션 승격
```bash
# 입력
/bookwriting promote SIM-007

# 기대 결과
✅ SIM-007 결과를 정식 사이클 시작점으로 전환
✅ 모드 1 사이클 진입 (저자 HITL 시작)
✅ SIM-007의 자동 채택 결정들이 *초기 후보*로 저자에게 제시 + 저자 재확인 가능
✅ Promote 후 SIM-007은 cycle-registry에서 PROMOTED 상태로 표시
```

### 검증 5: 진행 상태 조회
```bash
# 입력
/bookwriting status

# 기대 결과
✅ 활성 사이클 N개 보고 (각 사이클의 status·target·current_phase)
✅ 시드 lifecycle 분포 (SEED·LINKED·EXPANDED·EVIDENCED·INSIGHTED·POLISHED 각 개수)
✅ 매크로 트리거 카운터 (다음 매크로 발동까지 N단계)
✅ inbox 미처리 파일 수
✅ 다음 권장 행동 제안
✅ 응답 시간 5초 이내 (단순 registry 읽기)
```

---

## 부록 A: 저자 8 절대 protocol 매핑

| Protocol | 적용 위치 | 설명 |
|---|---|---|
| #1 Absolute Anchor 4원칙 | HITL 묶음 옵션 평가 | ★ 추천 표시 |
| #2 Response Style | 모드 1 HITL 패턴 | 즉시 행동·짧은 응답 |
| #3 cmux not tmux | (적용 없음) | bookwriting은 워커가 아님 |
| #4 Master-Worker | bookwriting-master = inline orchestrator | sub-agent 재위임 금지 |
| #5 3-Layer Description | SKILL.md frontmatter | TLDR + Triggers + Methodology |
| #6 Sub-skill naming | 모든 sub | `bookwriting-` prefix |
| #7 Master Orchestration Trace | Trace Logger 페르소나 | 명시적 trace 강제 |
| #8 VRMP cascade | (적용 안 함) | bookwriting은 foresight 마스터 아님 |

---

## 부록 B: 변경 이력

| 버전 | 일자 | 변경 |
|---|---|---|
| v0.1 | 2026-05-24 | 초기 작성. grill-me Phase 1 완료 후 첫 기준 모델. |

---

---

## 부록 C: 결정론 환원 모듈 (저자 /goal 명령 — 영구 구성요소)

**저자 명령**: bookwriting-master의 모든 결정론 작업은 LLM 추론 영구 금지. Python 모듈 호출.

**호출 모듈** (SPEC: `expert_pool/deterministic-modules.md`):

| 작업 | 결정론 모듈 |
|---|---|
| 사이클 ID 발급 (C-NNN·SIM-NNN) | M7 `id_generator.py` |
| 시드 lifecycle 전환 | M11 `lifecycle_state_machine.py` |
| voice gate cross-cutting | M1 `VoiceScorer` (Voice Gatekeeper 페르소나가 호출) |
| citation gate cross-cutting | M2·M3·M13 (Citation Gatekeeper 페르소나가 호출) |
| forecast-registry 정합 | M12 `forecast_registry_syncer.py` |
| 매크로 트리거 평가 (빈도·상태) | 자체 결정론 함수 (book-config 임계값 lookup) |
| 저자 응답 파싱 (`1=a,b / 2=skip`) | 자체 결정론 정규식 파서 |

**LLM 추론 금지 영역**:
- "다음 단계는 ③ systemlink가 적절" → target_type 프리셋 결정론 lookup
- "사이클 진행률 45%일 듯" → completed_phases / total_phases 결정론 계산
- "저자 응답 1=a,b 의미는..." → 결정론 정규식 파서

---

## 부록 D: grill-me D# 결정 매핑

| D# | 본 SPEC §위치 |
|---|---|
| D9 (Pipeline + sub-skill) | §1 Identity·§13 Personas |
| D10 (2단 nested) | §10 11 단계 마스터 위임 |
| D14 (명시 슬래시 + 모드) | §6 Invocation |
| D15 (메타 + 단계별 hybrid) | §6 슬래시 트리 |
| D16 (두 모드) | §6 cycle vs simulate · §7B Mode 2 추가 필요 (아래) |
| D17 (사이클 단위) | §6 모드 매트릭스 |
| D18 (상태 관리 계층) | §11 Dependencies (registry 3종) |
| D24 (사이클 계획·HITL 단계별) | §7 행동 시나리오 (변경된 자율도) |
| D25 (시뮬레이션 분리) | §9 Output Schema 모드 2 |
| Q33 (citation cross-cutting) | §12 Citation cross-cutting gate |
| 저자 강조 "큰 그림 안에서" | §4 Scope (out: 1-13 단계 외부 manual) |

---

## 부록 E: 9 항목 요구사항 매핑

| 9 항목 | §위치 |
|---|---|
| (a) description | §1 Identity + §2 Purpose 1줄 요약 |
| (b) 목적·의미 | §2 Purpose 저자 진짜 워크플로우 매핑 |
| (c) 역할 | §1·§13 (6 페르소나) |
| (d) 고유 영역 | §4 Scope (in/out 명확) |
| (e) 운영원칙 | §3 Philosophy (8 절대 protocol + v1 + 옵션 A+) |
| (f) 기능·원칙 | §5 Capabilities + §3 |
| (g) 출력 양식 | §9 Output Schema (모드 1·2 분기) |
| (h) 오류·예외처리 | §16 Error Handling |
| (i) 결정론 환원 모듈 | 부록 C ⭐ |

---

## 부록 F: 저자 진짜 워크플로우 15단계 매핑

| 저자 15단계 | bookwriting 책임 | 본 SPEC 위치 |
|---|---|---|
| 1. 신호 발견 | **외부 manual** (foresight-environmental-scanning) | §4 Out of scope |
| 2. Fact + Score | **외부 manual** (foresight-statistical-modeling) | §4 Out of scope |
| 3. 시스템 사고 연결 | **외부 manual** (foresight-systems-perspective) + 글쓰기 차원은 ③ systemlink | §11 Dependencies |
| 4. 빈 고리 채우기 | **외부 manual** (foresight-structural-analysis) + 글쓰기 차원은 ③ systemlink Gap Detector | §11 |
| 5. 추가 통찰 | **외부 manual** (foresight-causal-layered-analysis) + ⑥ insight-synthesis | §11 |
| 6. 미래 시스템 | **외부 manual** | §4 Out |
| 7. 패턴 추출 | **외부 manual** (foresight-tech-mining) | §4 Out |
| 8. 패턴 시뮬레이션 | **외부 manual** (foresight-simulation-games) | §4 Out |
| 9. 사이클 도출 | **외부 manual** (foresight-realtime-delphi) | §4 Out |
| 10. 미래 테스트 | **외부 manual** (foresight-robust-decisionmaking) | §4 Out |
| 11. 선택 | **외부 manual** (foresight-decision-modeling) | §4 Out |
| 12. 시나리오 기법 | **외부 manual** (foresight-scenarios) | §4 Out |
| 13. 가능성 추출 | **외부 manual** (foresight-futures-polygon) | §4 Out |
| **14. 의미 단면 선택** | **bookwriting 책임** ⭐ — ⑥ insight-synthesis | §2 Purpose |
| **15. 매력 글쓰기** | **bookwriting 책임** ⭐ — ⑦ content-expand + ⑧ narrative-craft + ⑩ line-edit | §2 Purpose |

bookwriting-master는 *14·15 + 흡수·통합·정합성* 영역의 *오케스트레이션* 담당.

---

## 부록 G: Mode 2 자동 진행 행동 시나리오 (D14·D16 미반영 보강)

저자 grill-me D16 명시 — 두 사용 모드. §7 본문은 모드 1 (정밀 HITL) 위주. Mode 2 (전자동 시뮬레이션) 변형:

```
호출: /bookwriting simulate ch01 [--variant insight-driven]

【Step 1-2: 입력 파싱 + 사이클 계획】 (모드 1과 동일)
  - cycle-registry에 SIM-NNN 등록 (별도 분류)

【Step 3-9: 결정론 단계 + 판단 단계 모두 자동 진행】
  - 모든 단계 마스터 위임
  - 저자 HITL 0회
  - 판단 묶음: ★ 추천 옵션 자동 채택
  - voice gate 위반: 자동 재작성 1회 + 실패 시 *trace 기록만* (escalate 안 함)
  - citation gate Critical: 자동 차단·해당 산출 *_simulations/* 파일에서 제외 (정식 chapter 미갱신)

【Step 10: 산출물 위치 분기】
  - 정식 chapter 파일 미갱신 (chapters/<ch>/*.md)
  - 별도 `chapters/<ch>/_simulations/sim-NNN.md` 생성
  - seed-registry lifecycle 미갱신 (시뮬레이션 임시 상태만)
  - forecast-registry 미갱신

【Step 11: 저자 종합 보고】
  - 사이클 전체 trace 요약
  - 자동 채택 결정 목록 (★ 추천 어떤 옵션 선택했는지)
  - 다음 권장:
    * `/bookwriting promote SIM-NNN` (정식 사이클로 승격)
    * `/bookwriting simulate ch01 --variant other` (다른 방향 시도)
    * `/bookwriting cycle ch01` (정밀 작업 진입)

【Mode 2 강제 조건】
  - Mode 2는 *모든 결정 자동* — 저자 묶음 영구 없음
  - Mode 2 산출물은 *드래프트 표시* (frontmatter `status: simulation`)
  - Mode 2 cycle-registry status: SIM 전용 enum 사용 (RUNNING_SIM·COMPLETED_SIM)
```

---

---

## 부록 H: 작가성 (Authorship) 정의 ⭐ (Round 5 #B10.1·#B10.4 Critical 수정)

저자 진북: "제2저자". *제1저자는 저자*. SPEC 모든 사이클·산출물에 *저자 작가성 우선* 강제.

**Authorship Policy:**
- **모든 챕터·꼭지에 저자 직접 작성 비율 메타데이터 추적**:
  ```yaml
  # chapter frontmatter
  authorship:
    user_intervention_score: 0.0-1.0   # 저자 *실질 응답* 비율 (자동 yes 제외)
    ai_generation_ratio: 0.0-1.0        # AI 자동 생성 비율
    hitl_response_count: N              # 저자 묶음 실응답 수
    mode_2_promote: false               # Mode 2 promote 여부
  ```
- **임계값**: `user_intervention_score < 0.7` 또는 `ai_generation_ratio > 0.5` 시 → 저자 알림 "공저 표기·AI 협업 명시 권장"
- **Mode 2 산출물은 promote 없이 정식 진입 영구 불가** (Round 5 #B10.4)
- **promote 시**: 저자 명시 호출만 + Mode 2 채택률 trace 필수 + 발문에 AI 협업 명시 강제

## 부록 I: HITL 시간 효율 (Round 5 #B5.4·#B8.1·#B8.3 수정)

저자 *실제 작업 시간 15-30분/사이클* + HITL 11회 = 인지 피로 + 시간 초과. 저자 자동 yes 응답 = 정체성 표류 위험.

**수정 정책:**
- **HITL 묶음 통합**: 11 단계 마스터 결정 → *3-5 통합 묶음*으로 압축
- **결정적 단계 (①·②·④)**: 묶음 confirm 1회로 통합
- **판단 단계 (⑥·⑦·⑧·⑩)**: 정밀 묶음 2-3개로 통합
- **응답 형식 표준화**: 각 묶음 1분 이내 즉답 가능 (`1=a,b / 2=skip / 3=c` 형식)
- **매크로 트리거**: 발동 시 *저자 confirm 강제* (자동 발동 X) — 저자 일일 계획 보호

**수정된 정량 기준** (§10 갱신):
- 모드 1 저자 HITL 회수: 약 *3-5회* (이전 11회에서 축소)
- 평균 사이클 시간: 모드 1 = *20-25분*

## 부록 J: 저자 voice 학습 정체성 표류 방지 ⭐ (Round 5 #B1.3·#B7.3 Critical)

저자 자동 yes 정책 + voice_guidelines 자동 학습 → *시간이 흐를수록 저자 voice 변형* 위험.

**Voice immutable_core 분리:**
- `voice_guidelines.immutable_core` 필드 신규 — *변경 절대 금지* 항목 (저자 핵심 시그니처 5 패턴·사상적 척추 4 어휘·signature_expressions 원본)
- `voice_guidelines.learned_addendum` — 자동 학습된 항목 (별도 누적)
- **immutable_core 변경**: 자동 yes 적용 영구 제외. 저자 *명시적 입력* (yes·confirm·승인 단어 *직접 타이핑*) 강제
- **change_log**: 모든 voice 변경 추적 (`_progress/voice-change-log.md`) — 사이클 ID + 변경 trace + 저자 응답 원문

## 부록 K: 저자 voice 악용 방지 ⭐ (Round 5 #B7.2 Critical)

저자 grill-me D1 "2단계 범용화"에서 저자 voice 모사 도구 악용 위험.

**Posthumous·범용화 정책:**
- 2단계 범용화 시 저자 voice anchor *반드시 제외* — *방법론*만 공개
- 저자 실제 가중치·signature 원문은 *저자 개인 자산*으로 봉인
- `book-config.yaml`에 `posthumous_policy` 섹션 신규:
  ```yaml
  posthumous_policy:
    voice_seal_trigger: "저자 명시 또는 사후"
    seal_action: "voice_guidelines 전체 read-only + 신규 책 생성 차단"
    inheritance_delegate: "[저자 명시 위임자]"
  ```

---

## 부록 L: Critical Gatekeeper 가드 추가 (Round 7 #C3·#C4·#C5·#C6·#C9·#C10)

### Legal Gatekeeper (#C3)
- *현존 인물 묘사* (Character Animator) → AI 추측 영구 금지, source-verified 강제
- *fair use 4 factor* — quote_length만이 아닌 *목적·성격·분량·시장 영향*. "heart of work" 인용 시 별도 묶음
- *post-mortem rights* per-jurisdiction (KR·US-CA·US-NY 등)
- *invasion of privacy* — vault 내 제3자 미공개 자료 source_consent 추적

### Safe Messaging Gatekeeper (#C10)
- *민감 주제 자동 감지*: 의미 위기·자살·우울·소외·실직·무기력
- 트리거 시:
  - surprise_weight 0.30 → 0.10 자동 하향
  - WHO 자살보도 가이드라인 + hotline 명시 강제 (한국: 1393·109)
  - Mode 2 자동 채택 *영구 금지*
  - 디스토피아 시나리오 묘사 후 *대안 path·agency 명시* 강제

### Medical Claim Gate (#C4)
- 의학적 주장 자동 감지 (신경 가소성·뇌 인터페이스·임상 효과) → `medical_claim_disclaimer` 강제
- Karpathy 비공식 발언은 의학 권위 *아님* 명시
- 임상시험·역학 인용 시 `data_provenance: peer_reviewed|preprint|corporate_claim|speculation` 자동 분류

### Quantitative Unit Gate (#C9.5 Critical)
- 정량 앵커 추출 시 *unit 강제* — "100배"만 추출 X, "100배 [생산성|GDP|...]" 필수
- 비상장 기업 재무 인용 시 `financial_data_type: audited|reported|estimated|leaked` 강제
- 충돌 검출 시 *methodology field* — 같은 수치 다른 방법론 / 같은 방법론 다른 수치 구분
- arxiv는 Grade B (preprint) 또는 별도 Grade A-preprint — peer-review 전 자료

### Environmental·Resource Gate (#C5)
- 시나리오 묘사 시 *환경·자원 제약* 차원 자동 점검 (Climate Hidden Cost gate)
- 2층 7요소 → 8요소 — `8. (선택) 자원·환경 제약`
- cycle-registry에 `estimated_energy_kwh` 필드 — Phase 3-B 인식 제고

### Theological Review Gate (#C2)
- 저자 명시 시 4 사상적 척추에 *imago Dei 정합성* 자동 알림 (선택 가드)
- 신학 평행 narrate (구속사·바벨탑·계몽주의) optional mode
- Grade F (Layer 6) 신학 권위 인용 가능 — Calvin·Augustine·Bavinck·MLJ·Luther 등 저자 sermon-* 스킬 풀과 정합

### Diversity Gatekeeper (#C6)
- citation_distribution_audit 메트릭 — 책 전체 권위 풀 성별·국적·분야 분포 보고
- 임계 미달 (단일 성별 80%+) 시 저자 알림
- 시그니처 4 "N 창업자가 같은 N배" — N 권위자 일반화 (창업자 한정 해제)

### Senior·Accessibility Gate (#C7)
- `accessibility_mode_senior` 옵션 — 시그니처 활용률 30%→20% 하향·max 문장 길이 60자
- 신조어·외국어 차용 어휘 첫 노출 시 *각주 강제*
- 3층 6요소 → *연령·세대 차원* 보강

**End of SPEC: bookwriting-master**
