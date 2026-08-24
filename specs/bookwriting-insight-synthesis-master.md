# SPEC: bookwriting-insight-synthesis-master

> 저자 *제2저자 성능 최정상*. 저자 진짜 워크플로우 *14단계 — 의미·영향력·놀라움 단면 선택*의 정밀 구현.
>
> 저자 강조: *"가장 의미있고, 영향력이 크고, 깜짝놀랄만한 미래의 단면을 선택하여 매력적인 글로 쓰는 방식이 핵심이다."*
>
> 작성일: 2026-05-24
> 양식: 17 항목 풀 SPEC + 단계 마스터 정밀화
> 매트릭스: 8 sub + 7 AI Agents + 6 Cycle + 7 Gate (Q18 — 최정밀)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-insight-synthesis-master` |
| 카테고리 | 단계 마스터 (⑥, MVP 수직 슬라이스 포함) |
| 저자 11 단계 매트릭스 위치 | ⑥ (제2저자 성능 핵심 4개 중 1개) |
| 저자 진짜 워크플로우 매핑 | **14단계 — 의미·영향력·놀라움 단면 선택** |
| 스킬 디렉토리 | `~/.claude/skills/bookwriting-insight-synthesis-master/` (또는 cys-bookwriting-skills/skills/) |
| 슬래시 | `/bookwriting-insight-synthesis <mode> [target]` |
| 마스터에서 호출 | `bookwriting-master`의 ⑥번 위임 |
| 매트릭스 수치 | 8 sub + 7 AI Agents + 6 Cycle + 7 Gate ⭐ 최정밀 |

---

## 2. Purpose

저자 진짜 워크플로우 *14단계 — 의미·영향력·놀라움 단면 선택*을 정밀 구현한다. 저자가 *foresight 사슬로 추출한 결과들* 또는 *④·⑤를 거친 evidence·연결*에서 *책에 담을 *최고의 단면들*을 *3 기준으로 평가·선택*한다.

**저자 인용 (진북):**
> *"가장 의미있고, 영향력이 크고, 깜짝놀랄만한 미래의 단면을 선택하여 매력적인 글로 쓰는 방식이 핵심이다."*

**3 기준 (Insight Triad):**
1. **의미 (Meaning)** — 저자 책 사상적 척추(메타도구·시스템 사고·UBI지능·인문학적 창조자)와의 *연결 깊이*. 의미는 *책 전체에 어떻게 짜여들어가는가*.
2. **영향력 (Impact)** — 통찰의 *스케일·범위·시점 도달*. 100배 스케일·5억 명 영향·2027 임계점 같은 *정량 앵커*.
3. **놀라움 (Surprise)** — 통념을 *깨는* 명제. 저자 "두 창업자가 정확히 같은 100배" 같은 *수렴의 놀라움* 또는 "셋 중 하나를 선택하는 것이 아니다" 같은 *프레임 전복*.

**저자 진짜 워크플로우와 다른 점:**
- 저자 14단계는 *foresight 결과* 위에서 일어남 — bookwriting-insight-synthesis-master는 *그 결과를 받아* 14단계 수행
- 옵션 A+ 원칙: 다른 스킬 자동 호출 안 함. *흡수된 결과만으로* 통찰 추출

---

## 3. Philosophy

**저자 8 절대 protocol 적용:**
- **#1 Absolute Anchor 4원칙**: 통찰 묶음에 *★ 추천 표시* (의미·영향력·놀라움 점수 종합)
- **#5 3-Layer Description Template**: TLDR + Triggers + Detailed Methodology
- **#6 Sub-skill naming**: `bookwriting-insight-synthesis-*` prefix
- **#7 Master Orchestration Trace**: 8 sub의 호출 trace 명시
- **#8 VRMP** = N/A (foresight 마스터가 아님 — 외부 web 호출 안 함)

**저자 v1 호환:**
- *권위 5층 다층 인용* (chapter-pipeline.md R4 규칙) — 모든 통찰에 *최소 2층 권위* 매핑
- *system_loops 호명* 강제 — 통찰이 *어느 시스템 루프*에 속하는가
- *quantitative_anchor* — 통찰에 *최소 1개 정량 앵커* 권장

**Voice 보존 (cross-cutting gate 적용):**
- 통찰 표현 시 *저자 voice 80%+ 일치* 필수
- 통찰의 *명제 표현*은 저자 시그니처 패턴 (`X가 아니라 Y`·`셋 중 하나를 선택하는 것이 아니다` 등) 활용
- 외국어 무분별 사용·기성 AI 어투 절대 금지

**모드 1·2 분기:**
- **모드 1**: 통찰 5-7개 후보 → ★ 추천 2-3개 → 저자 묶음 응답 (`1=a,b,c`)
- **모드 2**: 통찰 5-7개 후보 → ★ 추천 자동 채택 → 정식 채택 없이 *_simulations/* 드래프트

---

## 4. Scope (책임 영역)

### In scope (담당)
- ✅ 흡수된 evidence·시드·연결에서 *통찰 후보 N개 생성*
- ✅ 통찰 각각을 *의미·영향력·놀라움 3 기준*으로 평가·점수화
- ✅ 통찰을 *권위 5층 다층*에 매핑
- ✅ 통찰을 *book skeleton의 챕터·층·section_role*에 라우팅
- ✅ 통찰을 *저자 voice로 표현* (시그니처 패턴 활용)
- ✅ cross-chapter 통찰 발견·매핑 (다른 챕터와의 연결)
- ✅ 저자 묶음 제안 생성 (모드 1) 또는 자동 채택 (모드 2)
- ✅ seed-registry.yaml의 시드 lifecycle을 *EVIDENCED → INSIGHTED*로 진행
- ✅ chapters/<ch>/analysis.md·implications.md에 통찰 본문 작성

### Out of scope (담당 안 함)
- ❌ 통찰 *후보 자체의 원본 생성* (foresight 사슬 — 저자 외부 manual)
- ❌ 통찰의 *근거 자료 수집* (④ evidence-collect 담당)
- ❌ 통찰들 간 *그래프 연결* (⑤ evidence-link 담당)
- ❌ 통찰의 *꼭지 분량 확장* (⑦ content-expand 담당)
- ❌ 통찰의 *콜드 오픈 서사 구현* (⑧ narrative-craft 담당)
- ❌ 다른 스킬 자동 호출 (옵션 A+ 원칙)
- ❌ 통찰의 *문장 미시 첨삭* (⑩ line-edit 담당)

---

## 5. Capabilities (기능)

| 슬래시 모드 | 기능 | 트리거 |
|---|---|---|
| `/bookwriting-insight-synthesis cycle <target>` | 통찰 추출 사이클 (모든 8 sub 실행) | `bookwriting-master` ⑥번 위임 또는 저자 명시 |
| `/bookwriting-insight-synthesis candidates <target>` | 후보 통찰만 생성 (1-2 sub 실행) | 저자가 *후보 보기*만 원할 때 |
| `/bookwriting-insight-synthesis evaluate <insight-id>` | 특정 통찰의 3 기준 점수 재계산 | 저자가 *통찰 평가만* 원할 때 |
| `/bookwriting-insight-synthesis cross-chapter <target>` | cross-chapter 통찰 발견만 | 저자가 *연결 발견만* 원할 때 |
| `/bookwriting-insight-synthesis voice-craft <insight-id>` | 통찰을 저자 voice로 재표현 | 저자가 *표현만 다듬기* 원할 때 |

---

## 6. Invocation (호출 방식)

**예시 5개:**

```bash
# 1. 풀 사이클 (bookwriting-master에서 위임)
/bookwriting-insight-synthesis cycle ch01-economy

# 2. 단일 시드 통찰만
/bookwriting-insight-synthesis cycle S-001

# 3. 후보만 보기
/bookwriting-insight-synthesis candidates ch01-economy

# 4. 특정 통찰 재평가
/bookwriting-insight-synthesis evaluate INS-012

# 5. cross-chapter 발견만
/bookwriting-insight-synthesis cross-chapter ch01-economy
```

**인자 파싱:**
- `<target>`: ch-NNN | ch-NNN-section-N | S-NNN | INS-NNN | --all
- `--mode 1|2`: 명시적 모드 (생략 시 bookwriting-master 컨텍스트 따름)
- `--max-candidates N`: 후보 통찰 최대 개수 (기본 7)
- `--min-authority-layers N`: 권위 5층 중 최소 N층 매핑 강제 (기본 2)

---

## 7. Behavior (작동 방식)

**9단계 행동 시나리오:**

```
호출: /bookwriting-insight-synthesis cycle ch01-economy (mode 1)

【Step 1: 입력 검증·자료 로드】
  - target 파싱: ch01-economy
  - book-config.yaml 로드 (voice·매크로·layer_ratios)
  - skeleton.md에서 ch01의 *외골격* 추출 (사상적 척추 §1·1장 흐름)
  - seed-registry에서 ch01 라우팅 시드 (EVIDENCED 상태) 추출
  - chapters/01-economy/evidence-track.yaml + analysis.md(부분 작성) 로드
  - forecast-registry에서 ch01 관련 P-NNN 예측 로드
  - cycle-registry.yaml에서 ⑥ 단계 진입 기록

【Step 2: candidate-generation sub-skill 호출】
  - AI Agent 1 (Meta-tool Identifier) 발동
  - AI Agent 2 (System Loop Detector) 발동
  - AI Agent 4 (Surprise Hunter) 발동
  - 위 3 페르소나가 각자 통찰 후보 3-5개씩 생성 (총 9-15 후보)
  - 후보 풀에 INS-NNN 임시 ID 발급
  → trace: "[bookwriting-insight-synthesis-master] Meta-tool 4개 / System Loop 3개 / Surprise 4개 — 총 11 후보"

【Step 3: 의미·영향력·놀라움 평가 (3 sub 병렬)】
  - meaning-evaluation 호출: 후보별 *책 사상적 척추 연결 깊이* 0-1 점수
  - impact-evaluation 호출: 후보별 *정량 스케일·시점 도달* 0-1 점수
  - surprise-evaluation 호출: 후보별 *통념 깨기·프레임 전복* 0-1 점수
  - 종합 점수 = 0.35 * meaning + 0.35 * impact + 0.30 * surprise
  → trace: "[3 sub] meaning 평균 0.72 / impact 평균 0.61 / surprise 평균 0.55"

【Step 4: 후보 풀 정돈 + 권위 5층 매핑】
  - 종합 점수 상위 5-7개 선별
  - authority-multi-layer sub-skill 호출
  - 각 통찰을 *권위 5층 중 최소 2층*에 매핑
  - 매핑 실패 (단일 권위만 매핑) 시 → *해당 통찰을 풀에서 제외*
  → trace: "[authority] 7 후보 → 5 후보 (2층 미달 2개 제외)"

【Step 5: cross-chapter 통찰 발견】
  - cross-chapter-check sub-skill 호출
  - 각 통찰이 *다른 챕터의 시드·예측과 연결*되는가 탐색
  - 발견 시 통찰에 cross_reference 필드 추가
  → trace: "[cross-chapter] INS-003 → ch08 / INS-005 → ch10"

【Step 6: Voice craft 적용】
  - voice-craft sub-skill 호출 (AI Agent 7 Voice Aligner)
  - 5 후보를 *저자 시그니처 패턴*으로 재표현
  - 시그니처 패턴 적용 시도: `X가 아니라 Y`·`셋 중 하나를 선택하는 것이 아니다`·`X와 Y 사이의 거리에서 시작한다`
  - voice_score < 0.7인 통찰은 *자동 재표현* (1회 시도)
  → trace: "[voice-craft] 5 후보 모두 voice_score 0.7+ 통과 (재표현 1회 발동)"

【Step 7: 저자 묶음 제안 생성 (모드 1)】
  - bundle-builder sub-skill 호출 (AI Agent — HITL Mediator)
  - 5 통찰 후보를 *마크다운 묶음*으로 정돈
  - ★ 추천 표시 (종합 점수 상위 2-3개)
  - cross-reference 별도 묶음
  - cycle-registry.yaml에 decision_id D-NNN 등록
  → trace: "[bundle] D-007 생성 — 5 통찰 + 2 cross-ref + ★ 추천 3"

【Step 8: 모드 1 = 저자 응답 대기 / 모드 2 = 자동 채택】
  - 모드 1: status = PENDING_DECISION. 저자 응답 대기.
    응답 예: "1=a,b,c / 2=skip"
    → bookwriting-master가 응답 파싱 → resolved_decisions로 이동
  - 모드 2: ★ 추천 자동 채택. cycle-registry.sim_specific에 기록.
  → trace: "[모드 1] 저자 응답 대기" 또는 "[모드 2] 3 통찰 자동 채택"

【Step 9: 채택된 통찰 본문 작성 + lifecycle 갱신】
  - 채택된 통찰 (예: INS-001, INS-003, INS-005)을 chapters/01-economy/analysis.md의 *적절한 layer 위치*에 *본문 작성*
  - 통찰별로 *권위 5층 인용·정량 앵커·시스템 루프 호명* 모두 본문에 포함
  - seed-registry: 해당 시드들 lifecycle EVIDENCED → INSIGHTED 진행
  - chapters/01-economy/evidence-track.yaml: insights_used 갱신
  - seed-registry의 progress.insights_derived 증가
  → trace: "[output] analysis.md +1200자 / 3 시드 INSIGHTED 진행"
```

---

## 8. Input Schema

### 슬래시 인자
```typescript
{
  mode: "cycle" | "candidates" | "evaluate" | "cross-chapter" | "voice-craft"
  target: string         // ch-NNN | S-NNN | INS-NNN | --all
  options: {
    mode_1_or_2?: 1 | 2                 // 명시적 모드
    max_candidates?: number             // 기본 7
    min_authority_layers?: number       // 기본 2
    surprise_weight?: number            // 기본 0.30
  }
}
```

### 파일 입력 (필수)
- `book-config.yaml` — voice·매크로·layer_ratios
- `seed-registry.yaml` — 대상 시드의 lifecycle·connections
- `cycle-registry.yaml` — 현재 사이클 컨텍스트
- `skeleton.md` — 챕터 외골격
- `chapters/<ch>/evidence-track.yaml` — 사용 가능한 evidence
- `chapters/<ch>/analysis.md` — 현재 분석 본문 (부분 작성)
- `forecast-registry.yaml` — 관련 예측

### 파일 입력 (옵션)
- `chapters/<ch>/narrative.md` — 1층 콜드오픈 컨텍스트 (참조용)
- `chapters/<ch>/implications.md` — 3층 함의 컨텍스트 (cross-reference 발견용)
- 저자 외부 흡수 자산 (foresight 결과 — inbox/import 처리됨)

---

## 9. Output Schema

### 저자 화면 (모드 1)
```markdown
# 사이클 C-007 — ⑥ insight-synthesis 묶음

## 저자 판단 묶음 1: 통찰 채택 (5개 중)

### (a) ★ 추천 — INS-001 [의미 0.88·영향 0.85·놀라움 0.82]
**"AGI는 도구가 아니라 도구를 만드는 도구다 — 메타도구는 인간 인지를 무한 확장한다"**

권위층: 창업자 증언 (아모데이 "1-3년 90% 확신") + 미래학자 시스템 사고 (한계비용 제로)
시스템 루프: L1 지능대체나선 — 변수 1 인지 외주화
정량 앵커: 1-3년 / 90% 확신 / 100배 스케일
시그니처: "X가 아니라 Y" 패턴 적용

### (b) ★ 추천 — INS-003 [의미 0.85·영향 0.78·놀라움 0.79]
...

### (c) ★ 추천 — INS-005 [의미 0.82·영향 0.76·놀라움 0.75]
...

### (d) INS-007 [의미 0.65·영향 0.70·놀라움 0.62]
...

### (e) INS-009 [의미 0.60·영향 0.55·놀라움 0.50]
...

## 저자 판단 묶음 2: cross-chapter 매핑 (2개)
### (a) ★ — INS-003 → ch08 (의미 위기) 추가 매핑
**근거**: 메타도구의 양면 — 인지 외주화가 의미 위기로 직결
### (b) INS-005 → ch10 (응답) 추가 매핑

저자: 응답하세요 (예: "1=a,b,c / 2=a")
```

### 저자 화면 (모드 2)
```markdown
# SIM-007 — ⑥ insight-synthesis 자동 채택

✅ INS-001 채택 (★ 추천)
✅ INS-003 채택 (★ 추천)
✅ INS-005 채택 (★ 추천)
⏭️ INS-007 자동 skip
⏭️ INS-009 자동 skip
✅ cross-chapter INS-003 → ch08 자동 채택

→ _simulations/sim-007.md에 통찰 본문 작성됨
```

### 파일 갱신

| 파일 | 모드 1 | 모드 2 |
|---|---|---|
| `chapters/<ch>/analysis.md` | 채택 통찰 본문 추가 (1200-2000자) | 미갱신 |
| `chapters/<ch>/_simulations/sim-NNN.md` | 미갱신 | 자동 채택 통찰 본문 |
| `chapters/<ch>/evidence-track.yaml` | insights_used 갱신 | 미갱신 |
| `seed-registry.yaml` | 시드 lifecycle EVIDENCED → INSIGHTED | 미갱신 |
| `cycle-registry.yaml` | D-NNN resolved + outputs 갱신 | sim_specific.auto_accepted_options 갱신 |

---

## 10. Deliverable Quality (결과물 형태·수준)

### 성공 시나리오
- ✅ **통찰 후보 5-7개 생성** (최소 5개, 최대 max_candidates)
- ✅ **각 통찰의 *3 기준 점수* 0-1 범위** 정확히 계산
- ✅ **권위 5층 중 최소 2층 매핑** (R4 호환)
- ✅ **각 통찰에 *최소 1개 정량 앵커*** 포함
- ✅ **각 통찰이 *최소 1개 시스템 루프*에 호명**
- ✅ **★ 추천 2-3개** 명확 표시
- ✅ **cross-chapter 매핑 0-3개** 발견·제시
- ✅ **저자 voice_score 0.7+** 통찰 표현
- ✅ **시그니처 패턴 적용** 1개 이상 (가능한 경우)
- ✅ **모드 1: 저자 묶음 응답 후 *채택된 통찰만 본문 작성***
- ✅ **모드 2: ★ 추천 자동 채택 + _simulations/ 드래프트**

### 실패 시나리오
- ❌ **통찰 후보 0개** — evidence·시드 부족 → 저자 알림 + ④ evidence-collect 재호출 권고
- ❌ **모든 통찰 권위 1층만** — R4 위반. 풀에서 제외 → 저자 알림
- ❌ **voice_score < 0.7 통찰 다수** — 재표현 실패. 저자 묶음에 *재표현 옵션 포함*
- ❌ **3 기준 점수 모두 < 0.5** — 통찰 약함. 풀에서 제외
- ❌ **저자 응답 형식 오류** — 재요청 + 형식 안내

### 정량 기준
- **소요 시간**: 모드 1 = 3-5분 / 모드 2 = 2-3분
- **통찰 후보 수**: 5-7개 (max_candidates 기본 7)
- **★ 추천 수**: 2-3개
- **권위 5층 매핑 수**: 평균 2.5층/통찰
- **정량 앵커 수**: 평균 1.5개/통찰
- **시스템 루프 호명 수**: 평균 1개/통찰
- **voice_score**: 모든 채택 통찰 0.7+
- **시그니처 패턴 활용률**: 30%+

### 정성 기준
- **저자 정체성 보존**: 통찰이 *저자가 직접 말한 것처럼* 읽힘
- **3 기준 균형**: 의미만 강하거나 놀라움만 강한 통찰은 *★ 추천* 안 함
- **사상적 척추 연결**: 모든 통찰이 *메타도구·시스템 사고·UBI지능·인문학적 창조자* 중 1개 이상과 연결
- **권위 다층 인용**: 저자 R4 규칙 *엄격 준수*
- **시그니처 패턴**: 저자 voice의 *고유 패턴* 활용으로 *AI 어투 회피*

---

## 11. Dependencies

### 필수 의존
- `bookwriting-master` (위임 호출자)
- 8 sub-skill 모두 (insight-synthesis-candidate-generation 외 7개)
- `book-config.yaml` (voice_guidelines + min_authority_layers)
- `seed-registry.yaml` (시드·연결)
- `cycle-registry.yaml` (사이클 컨텍스트)
- `skeleton.md` (외골격)
- `chapters/<ch>/evidence-track.yaml` (evidence)
- `chapters/<ch>/analysis.md` (본문 작성 대상)
- `forecast-registry.yaml` (예측)

### 선행 단계 의존
- ④ evidence-collect 통과 (evidence-track.yaml 채워짐)
- ⑤ evidence-link 통과 (그래프 연결 완료)

### 후속 단계
- ⑦ content-expand가 *채택된 통찰을 꼭지 분량으로 확장*
- ⑧ narrative-craft가 *통찰을 콜드 오픈 서사로 구현*

### 명시적 비의존
- ❌ 설치된 다른 스킬 (옵션 A+)
- ❌ Web API
- ❌ NotebookLM bridge 자동 호출 (별도 sub-skill, 저자 명시 시만)

---

## 12. Guards

### Voice Gate (cross-cutting)
- 모든 통찰 표현에 자동 발동
- voice_score < 0.7 → 자동 재표현 1회 → 실패 시 저자 묶음 escalate

### 권위 5층 가드 (R4 호환)
- 통찰이 *권위 1층만* 매핑 시 → 풀에서 제외
- *권위 1층 (창업자 증언) 누락* + *2-5층만* 매핑 시 → 저자 알림 (보강 권장)

### 시스템 루프 가드
- 통찰이 *시스템 루프 미호명* → warning + 저자 알림 (R3 호환 — system_loops 호명 강제)

### 정량 앵커 가드
- 통찰에 *정량 앵커 0개* → warning (강제 아님 — 일부 통찰은 정성적)

### 3 기준 점수 가드
- 모든 점수 < 0.5 → 통찰 풀에서 제외
- 점수 합 > 2.7 → ★ 추천 자동 부여

### 시그니처 패턴 가드
- 저자 voice 보존을 위해 시그니처 패턴 활용률 30%+ 권장
- 미달 시 voice-craft sub가 *시그니처 패턴 적용 재시도*

### Loop 방지
- 같은 시드의 ⑥ 단계 *3회 호출* → abort + 저자 알림 (시드 자체에 문제 가능)

### ⭐ Citation Gate (cross-cutting — 저자 Q33 후속 명령)
- 모든 통찰 후보의 *권위 인용 출처* 자동 검증 (citation-gate.md SPEC 참조)
- 통찰 후보가 *source_file 실재 안 함* → Critical 위반 → 즉시 차단 + 저자 묶음 escalate
- 통찰 후보가 *권위 1층만 매핑* → R4 위반 → 풀에서 제외 (Authority Cross-checker 페르소나가 §13에서 이미 담당)
- 통찰의 *정량 앵커*가 *출처 없음* → 신호 5 검출 → 저자 묶음
- 저자 진북: *"할루시네이션 없는 출처, 명확한 자료 출처, 가장 권위있는 근거자료"*

---

## 13. AI Agents Personas (페르소나 7명) ⭐

저자 envscan 6 페르소나 패턴 변형. ⑥ insight-synthesis의 *최정밀 7 페르소나*:

### 페르소나 1: Meta-tool Identifier
| 항목 | 내용 |
|---|---|
| 역할 | 저자 *메타도구 명제 + 시스템 사고 관점*에서 통찰 발견 |
| 관점 | "이 evidence가 *AGI를 메타도구로 정의*하는데 어떻게 기여하는가?" |
| 결정 권한 | 메타도구 통찰 후보 3-5개 생성 |
| Voice 인식 | 저자 "메타 도구" 시그니처 표현 활용 |
| 저자 사상적 척추 연결 | §1 메타도구 명제 직접 연결 |

### 페르소나 2: System Loop Detector
| 항목 | 내용 |
|---|---|
| 역할 | *시스템 루프·피드백 관점*에서 통찰 발견 |
| 관점 | "이 evidence가 *어느 시스템 루프*에 속하는가? 어떤 변수가 어떻게 작동하는가?" |
| 결정 권한 | 시스템 루프 통찰 후보 2-4개 생성 |
| Voice 인식 | "L1 지능대체나선"·"L2 정치내파루프" 등 저자 루프 명명법 |
| 저자 사상적 척추 연결 | §2 시스템 사고 명제 직접 연결 |

### 페르소나 3: Authority Cross-checker
| 항목 | 내용 |
|---|---|
| 역할 | *권위 5층 다층 인용 검증* (R4 호환) |
| 관점 | "이 통찰이 *몇 개 권위층*에 의해 뒷받침되는가? 최소 2층 충족?" |
| 결정 권한 | 권위 매핑 검증 + 단일 권위만 매핑된 통찰 *풀에서 제외* |
| Voice 인식 | 저자 권위 5층 (창업자·미래학자·인접학문·사상가·역사평행) 명명법 |

### 페르소나 4: Surprise Hunter ⭐
| 항목 | 내용 |
|---|---|
| 역할 | *통념 깨기·프레임 전복·수렴의 놀라움* 발견 |
| 관점 | "이 evidence가 *독자가 예상하지 못한 명제*를 만드는가?" |
| 결정 권한 | 놀라움 통찰 후보 3-5개 생성 + 저자 시그니처 *X가 아니라 Y*·*셋 중 하나가 아니다* 적용 |
| Voice 인식 | 저자 *수렴의 놀라움* 패턴 ("두 창업자가 정확히 같은 100배") |
| 저자 강조 영역 | 저자 진북 인용: *"깜짝놀랄만한 미래의 단면을 선택"* 핵심 |

### 페르소나 5: Impact Assessor
| 항목 | 내용 |
|---|---|
| 역할 | *영향력 평가 — 스케일·범위·시점 도달* |
| 관점 | "이 통찰의 *정량 앵커는? 누구에게 어떻게 영향?*" |
| 결정 권한 | impact_score 0-1 계산 + 정량 앵커 명시 |
| Voice 인식 | "100배 스케일"·"5억 명"·"2027 임계점" 같은 저자 정량 표현 |

### 페르소나 6: Meaning Synthesizer
| 항목 | 내용 |
|---|---|
| 역할 | *의미 평가 — 저자 책 사상적 척추 연결* |
| 관점 | "이 통찰이 *메타도구·시스템 사고·UBI지능·인문학적 창조자* 중 어디에 연결?" |
| 결정 권한 | meaning_score 0-1 계산 + 사상적 척추 매핑 |
| Voice 인식 | 저자 4 사상적 척추 명명법 정확히 |

### 페르소나 7: Voice Aligner ⭐
| 항목 | 내용 |
|---|---|
| 역할 | *통찰을 저자 voice로 재표현* |
| 관점 | "이 통찰이 *저자가 직접 말한 것처럼* 읽히는가? voice_score 0.7+?" |
| 결정 권한 | voice-craft 발동 + 시그니처 패턴 적용 + 재표현 1회 시도 |
| Voice 인식 | 저자 *시그니처 5 패턴* 적극 활용 |
| 저자 강조 영역 | 저자 정체성 보호의 최후 페르소나 |

---

## 14. Cycle (C1-C6)

| Cycle | 트리거 | 입력 조건 | 작동 패턴 |
|---|---|---|---|
| **C1: Single Seed Insight** | `cycle S-NNN` | 단일 시드 EVIDENCED | 1 시드 → 통찰 5개 (스케일 작음) |
| **C2: Multi-Seed Synthesis** | `cycle ch-NNN` (기본) | 챕터의 다중 시드 EVIDENCED | 다중 시드 통합 통찰 5-7개 |
| **C3: Cross-Chapter Insight** | `cross-chapter <target>` | 챕터·시드 컨텍스트 | 다른 챕터와의 연결 통찰만 |
| **C4: Authority Multi-Layer** | `--min-authority-layers 4` | 권위 강조 모드 | 4-5층 매핑 통찰만 |
| **C5: Surprise Priority** | `--surprise-weight 0.5` | 놀라움 우선 | Surprise Hunter 가중치 증가 |
| **C6: Simulation Auto-Accept** | `cycle <target> --mode 2` (모드 2) | 시뮬레이션 | ★ 추천 자동 채택 + _simulations/ |

---

## 15. Gates (검증 게이트)

| Gate | 검증 항목 | 통과 기준 |
|---|---|---|
| **G1: Input Validation** | 시드·evidence·라우팅 확보 | EVIDENCED 시드 ≥1개 + evidence-track.yaml 존재 |
| **G2: Candidate Pool** | 통찰 후보 생성 | 최소 3개 후보 (max_candidates 한도 내) |
| **G3: Triad Evaluation** | 의미·영향력·놀라움 3 점수 | 모든 후보의 3 점수 계산 완료 |
| **G4: Authority Multi-Layer** | 권위 5층 매핑 | 모든 통찰이 *최소 min_authority_layers (기본 2)* 매핑 |
| **G5: Voice Gate Pass** | voice_score 검증 | 모든 통찰 voice_score ≥0.7 (재표현 후) |
| **G6: Bundle Generation** (모드 1) | 저자 묶음 제안 생성 | decision_id 발급 + ★ 추천 ≥1개 + 최소 3 후보 |
| **G6': Auto-Accept** (모드 2) | ★ 추천 자동 채택 | sim_specific.auto_accepted_options 등록 |
| **G7: Output Persistence** | 본문 작성·registry 갱신 | analysis.md 작성 (모드 1) 또는 sim 파일 생성 (모드 2) + seed-registry lifecycle 갱신 |

---

## 16. Error Handling

| 실패 시나리오 | 대응 |
|---|---|
| 통찰 후보 0개 (G2 위반) | abort + 저자 알림 + ④ evidence-collect 재호출 권장 |
| 모든 통찰 권위 1층만 (G4 위반) | 후보 풀에서 모두 제외 + 저자 알림 + 외부 evidence 보강 권장 |
| Voice_score 재표현 실패 (G5 위반) | pending_decisions에 *재표현 옵션* 포함 묶음 escalate |
| 저자 응답 형식 오류 | 재요청 + 형식 안내 (`1=a,b,c / 2=skip` 형식) |
| 저자 모든 통찰 거부 (skip 응답) | 사이클 DEFERRED + ④ evidence-collect 재시도 권장 |
| Cross-chapter 자동 라우팅 실패 | warning + cross-reference 없이 진행 |
| Sub-skill timeout (5분 초과) | 사이클 INTERRUPTED + 저자 알림 + resume 가능 |
| 매크로 트리거 *과도 발동* (사이클 중 ⑥ 3회 호출) | abort + Loop 방지 가드 발동 + 저자 알림 |
| seed-registry lifecycle 갱신 실패 | 백업 자동 복원 + 저자 알림 |
| analysis.md 쓰기 권한 오류 | abort + 저자 알림 |

---

## 17. Verification Examples ⭐

저자가 후일 *명세-실제 대조*하는 기준 시나리오 7개:

### 검증 1: ch01 메타도구 통찰 추출 (C2 다중 시드)
```bash
# 입력
/bookwriting-insight-synthesis cycle ch01-economy

# 기대 결과
✅ ch01 라우팅 시드 5개 (EVIDENCED 상태) 추출
✅ 통찰 후보 7개 생성 (max_candidates 기본)
   - Meta-tool Identifier 3개
   - System Loop Detector 2개
   - Surprise Hunter 2개
✅ 3 기준 점수 모두 0-1 범위
✅ 권위 5층 매핑 평균 2.5층
✅ 정량 앵커 평균 1.5개
✅ ★ 추천 3개 (종합 점수 상위)
✅ cross-chapter 발견 2개 (ch08·ch10)
✅ voice_score 모두 0.7+
✅ 시그니처 패턴 적용률 40%+
✅ 저자 묶음 제안 출력 (마크다운 + ★)
✅ 저자 응답 후 채택 통찰만 analysis.md에 작성
✅ 5 시드 lifecycle EVIDENCED → INSIGHTED 진행
```

### 검증 2: 단일 시드 통찰 (C1)
```bash
/bookwriting-insight-synthesis cycle S-001

✅ S-001 한 시드만 다룸
✅ 통찰 후보 5개 (단일 시드라 max보다 적음 OK)
✅ 권위 5층 매핑 평균 2층 이상
✅ 저자 묶음 제안 + 응답 후 채택
✅ S-001 lifecycle 진행
```

### 검증 3: cross-chapter 발견만 (별도 모드)
```bash
/bookwriting-insight-synthesis cross-chapter ch01-economy

✅ ch01 통찰들이 *다른 챕터*와 어떻게 연결되는지만 분석
✅ 새 통찰 생성 안 함 (기존 INS 활용)
✅ cross_reference 매핑 결과만 출력
✅ 저자 묶음 = "어떤 cross-reference 채택?"
```

### 검증 4: 놀라움 우선 (C5)
```bash
/bookwriting-insight-synthesis cycle ch01-economy --surprise-weight 0.5

✅ Surprise Hunter 페르소나 가중치 증가
✅ surprise 점수 가중 50%로 종합 점수 재계산
✅ ★ 추천이 *놀라움 강한 통찰* 위주
✅ 시그니처 패턴 *X가 아니라 Y*·*셋 중 하나가 아니다* 활용 증가
```

### 검증 5: 모드 2 자동 채택 (C6)
```bash
/bookwriting-insight-synthesis cycle ch01-economy --mode 2

✅ HITL 0회 (저자 응답 안 받음)
✅ ★ 추천 3개 자동 채택
✅ chapters/01-economy/_simulations/sim-007.md에 통찰 본문 작성
✅ 정식 analysis.md 미갱신
✅ seed-registry lifecycle 미갱신 (시뮬레이션)
✅ cycle-registry.sim_specific.auto_accepted_options 등록
```

### 검증 6: 권위 5층 가드 작동
```bash
# 통찰 후보 중 일부가 권위 1층만 매핑
/bookwriting-insight-synthesis cycle ch01-economy

✅ Authority Cross-checker가 단일 권위 통찰 *풀에서 제외*
✅ trace에 "G4 위반 — 통찰 INS-007 권위 1층만 매핑, 제외" 명시
✅ 저자 알림 + 외부 evidence 보강 권장
```

### 검증 7-bis: Citation Gate 작동 ⭐ (저자 Q33 후속 명령)
```bash
# 통찰 후보 INS-007 (창업자 증언 매핑 시도)
/bookwriting-insight-synthesis cycle ch01-economy

# Citation Gate 자동 발동 (cross-cutting)
✅ INS-007 인용: "한 보고서에 따르면 1조 달러 시장"
✅ Critical 신호 검출 (신호 2 — 형식 모호 + 신호 3 — 메타데이터 누락)
✅ source_file: null
✅ 즉시 차단 + 저자 묶음 escalate
✅ 저자 옵션: "(a) 외부 출처 보강 / (b) INS-007 제외 / (c) 저자 직접 출처"

# 저자 응답: "1=b" (INS-007 제외)
✅ INS-007 풀에서 제외
✅ ★ 추천 재계산 (남은 통찰 6개)
✅ cycle-registry.citation_gate_results 갱신
   - critical_violations: 1
   - escalated_to_user: 1
   - hallucination_blocks: 1
```

### 검증 7: Voice 재표현 + 시그니처 패턴
```bash
# 후보 통찰: "AGI는 인지 능력을 갖춘 AI다 (voice_score 0.45)"
/bookwriting-insight-synthesis cycle ch01-economy

✅ Voice Aligner 페르소나가 재표현 시도
✅ 재표현 결과: "AGI는 *더 똑똑한 AI*가 아니라, *모든 도구를 만드는 도구* — 메타도구다"
✅ 시그니처 패턴 "X가 아니라 Y" 적용
✅ voice_score 0.45 → 0.82 → 통과
```

---

## 부록 A: 저자 인용 (진북)

> *"가장 의미있고, 영향력이 크고, 깜짝놀랄만한 미래의 단면을 선택하여 매력적인 글로 쓰는 방식이 핵심이다."*

이 인용이 ⑥ insight-synthesis의 *진북*이다.

3 기준 = 저자 직접 명시:
1. **의미** (가장 의미있고)
2. **영향력** (영향력이 크고)
3. **놀라움** (깜짝놀랄만한)

이 3 기준이 *시뮬레이션·정량화·자동 평가 가능한* 데이터 구조로 정밀화되었다 (3 sub × AI Agent 3 페르소나).

---

## 부록 B: 저자 8 절대 protocol 매핑

| Protocol | 적용 위치 |
|---|---|
| #1 Absolute Anchor 4원칙 | ★ 추천 표시 + 종합 점수 |
| #5 3-Layer Description | SKILL.md frontmatter |
| #6 Sub-skill naming | `bookwriting-insight-synthesis-*` prefix |
| #7 Master Orchestration Trace | 8 sub 호출 trace 강제 |

---

## 부록 C: 8 Sub-skill 목록

| # | Sub-skill | 책임 |
|---|---|---|
| 1 | `bookwriting-insight-synthesis-candidate-generation` | Meta-tool·System Loop·Surprise 페르소나 발동 + 통찰 후보 N개 생성 |
| 2 | `bookwriting-insight-synthesis-meaning-evaluation` | 의미 점수 0-1 계산 (Meaning Synthesizer) |
| 3 | `bookwriting-insight-synthesis-impact-evaluation` | 영향력 점수 0-1 계산 (Impact Assessor) |
| 4 | `bookwriting-insight-synthesis-surprise-evaluation` | 놀라움 점수 0-1 계산 (Surprise Hunter) |
| 5 | `bookwriting-insight-synthesis-cross-chapter-check` | 다른 챕터와의 연결 통찰 발견 |
| 6 | `bookwriting-insight-synthesis-authority-multi-layer` | 권위 5층 매핑 (R4 호환, Authority Cross-checker) |
| 7 | `bookwriting-insight-synthesis-voice-craft` | 저자 voice로 재표현 + 시그니처 패턴 적용 (Voice Aligner) |
| 8 | `bookwriting-insight-synthesis-bundle-builder` | 저자 묶음 제안 생성 (HITL Mediator) |

---

## 부록 D: 변경 이력

| 버전 | 일자 | 변경 |
|---|---|---|
| v0.1 | 2026-05-24 | 초기 작성. 저자 *제2저자 성능 최정상* SPEC. |

---

---

## 부록 E: 결정론 환원 모듈 (저자 /goal 명령)

| 작업 | 결정론 모듈 (SPEC: `expert_pool/deterministic-modules.md`) |
|---|---|
| Insight Triad 3 점수 계산 (meaning·impact·surprise) | **결정론 환원 불가** — 저자 사상적 척추 평가는 *주관적 미학*. 단, 출처 1:1 대조 필수 (skeleton.md §사상적척추·저자 grill-me 진북 인용) |
| 정량 앵커 추출 (impact 평가용) | M4 `QuantitativeAnchorExtractor` |
| 권위 5층 매핑 (Authority Multi-Layer) | M3 `AuthorityGrader` (M13 `R4MultiLayerVerifier` cross-cutting) |
| voice_score 재계산 (voice-craft sub) | M1 `VoiceScorer` |
| 시그니처 패턴 적용 (voice-craft) | M8 `signature_pattern_applier` |
| 시드 lifecycle EVIDENCED → INSIGHTED 전환 | M11 `lifecycle_state_machine` |
| 통찰 ID 발급 (INS-NNN 임시) | M7 `id_generator` (insight ID 확장) |

**LLM 추론 금지 영역**: 점수 *수치* 자체 생성 금지. 정량 추출·권위 매핑·시그니처 검출 모두 결정론.
**LLM 허용 영역**: Insight Triad의 *의미 평가 자체* (저자 척추와의 의미 연결 깊이) — 주관적 미학이라 결정론 환원 불가. 단, *근거 인용 강제* (skeleton.md §사상적척추).

## 부록 F: grill-me D# 결정 매핑
| D# | 본 SPEC §위치 |
|---|---|
| D6 (insight lifecycle 6 외골격) | §2·§7 Step 9 lifecycle 전환 |
| D7 (13 내부 cycle 매핑) | §14 Cycle C1-C6 |
| 저자 진북 (의미·영향·놀라움) | §2 Purpose + 부록 A 진북 인용 |
| Q33 (R4 다층 강제) | §13 Authority Cross-checker·부록 C SUB 9 authority-multi-layer |
| D11 (시그니처 패턴) | §3 + §13 Voice Aligner + 부록 E M8 |
| D16 (두 모드) | §7 모드 1·2 분기 |

## 부록 G: 9 항목 매핑
| (a) description | §1·§2 |
| (b) 목적·의미 | §2 + 저자 진북 |
| (c) 역할 | §13 7 페르소나 |
| (d) 고유 영역 | §4 (in: 14단계 의미 단면 / out: 본문 작성·근거 수집 분리) |
| (e) 운영원칙 | §3 Philosophy |
| (f) 기능·원칙 | §5·§3 |
| (g) 출력 양식 | §9 모드 1·2 분기 |
| (h) 오류·예외처리 | §16 |
| (i) 결정론 환원 | 부록 E |

## 부록 H: Mode 2 자동 진행 행동
모드 2 (`/bookwriting-insight-synthesis cycle ch01 --mode 2`):
- 모든 평가 자동 (HITL 0회)
- ★ 추천 (종합 점수 상위) 자동 채택
- cross-chapter·voice·citation gate 자동 처리
- 결과 → `chapters/<ch>/_simulations/sim-NNN-insights.md` (드래프트 표시)
- 정식 analysis.md·seed-registry 미갱신

**End of SPEC: bookwriting-insight-synthesis-master**

> ⭐ 이 SPEC은 저자 책의 *통찰 가치 보장*의 핵심이다. 통찰이 *3 기준 균형 + 권위 다층 + voice 일치*로 정밀화되어야 저자 책이 *foresight 결과 자료집*이 아닌 *저자 사상이 살아있는 책*이 된다.
