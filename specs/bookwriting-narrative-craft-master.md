# SPEC: bookwriting-narrative-craft-master

> 저자 *제2저자 성능 핵심 4개 중 1개*. 저자 진짜 워크플로우 *15단계 매력적 글쓰기*의 *매력 도구 영역*. 콜드 오픈·1층 서사·시나리오 묘사.
>
> 저자 인용 (진북): *"매력적인 글로 쓰는 방식이 핵심이다."*
>
> 작성일: 2026-05-24
> 매트릭스: 7 sub + 6 AI Agents + 5 Cycle + 4 Gate (Q18)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-narrative-craft-master` |
| 카테고리 | 단계 마스터 (⑧) — Phase 3-B (수직 슬라이스 외, 매력 핵심) |
| 저자 11 단계 매트릭스 위치 | ⑧ (제2저자 성능 핵심 4개 중 1개) |
| 저자 진짜 워크플로우 매핑 | **15단계 매력 글쓰기 — 매력 도구 영역** |
| 슬래시 | `/bookwriting-narrative-craft <mode> [target]` |
| 매트릭스 수치 | 7 sub + 6 AI Agents + 5 Cycle + 4 Gate |
| 저자 강조 영역 | ⭐ |

---

## 2. Purpose

저자 책 *15단계 매력적 글쓰기*의 *콜드 오픈·1층 서사·시나리오 묘사·등장인물 입체화·역사 평행 narrate* 등 *매력 도구*를 정밀 구현. ⑦ content-expand가 *2층 논증*에 집중한다면, ⑧ narrative-craft는 *독자 끌어당기는 매력*에 집중.

**4 책임:**
1. **콜드 오픈** — 챕터 1층 *고유 장면 한 컷* (날짜·장소·인물·감각 디테일)
2. **1층 서사** — 추상 명제 회피·구체 장면으로 시작
3. **시나리오 묘사** — 시나리오 분기·역사 평행을 *서사적 묘사*로
4. **등장인물 입체화** — 저자 *권위 5층* 등장인물 (Amodei·Hassabis·저자·바루파키스·하라리 등)을 *입체적 인물*로

---

## 3. Philosophy

**저자 v1 호환:**
- chapter-pipeline.md의 *1층 표준 골격* (콜드 오픈 라이브러리 + 5 검사항)
- skeleton.md의 1층 콜드 오픈 후보 (도입부·1-10장·종장)

**저자 시그니처 패턴 적극 활용:**
- "X와 Y 사이의 거리에서 시작한다" — 도입부
- "셋 중 하나를 선택하는 것이 아니다" — 결론
- "두 창업자가 정확히 같은 N배" — 수렴 강조

**Voice·Citation gate cross-cutting 적용:**
- 콜드오픈도 *역사적 사실은 출처 명시*
- AI 어투 절대 금지

---

## 4. Scope

### In scope
- ✅ chapters/<ch>/narrative.md 콜드 오픈 작성
- ✅ 1층 추상 명제 회피·구체 장면 강제
- ✅ 시나리오·역사 평행 narrate
- ✅ 등장인물 입체화 (Amodei·Hassabis·저자 등)
- ✅ 저자 콜드 오픈 라이브러리 활용 (skeleton.md chapter-pipeline)
- ✅ 종장의 결론적 서사 작성

### Out of scope
- ❌ 2층 논증 (⑦ content-expand 담당)
- ❌ 3층 함의 (⑦ content-expand 담당)
- ❌ 문장 미시 (⑩ line-edit)
- ❌ 외부 web 검색

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-narrative-craft cycle <target>` | 풀 사이클 |
| `/bookwriting-narrative-craft cold-open <chapter>` | 콜드 오픈만 |
| `/bookwriting-narrative-craft scenario-narrate <chapter>` | 시나리오 묘사만 |
| `/bookwriting-narrative-craft character <chapter>` | 등장인물 입체화 |
| `/bookwriting-narrative-craft historical-parallel <chapter>` | 역사 평행 서사 |

---

## 6. Invocation

```bash
/bookwriting-narrative-craft cycle ch01-economy
/bookwriting-narrative-craft cold-open ch07-cosmic   # 7장 페르미 역설 새벽 천문학자
/bookwriting-narrative-craft scenario-narrate ch03-feudal
/bookwriting-narrative-craft character ch00-prologue  # 다보스 무대 인물
```

---

## 7. Behavior

**9단계 행동 시나리오:**

```
호출: /bookwriting-narrative-craft cycle ch01-economy

【Step 1: 입력 로드】
  - chapter의 INSIGHTED 시드 + ⑦ 작성 본문
  - skeleton.md의 챕터 1층 콜드오픈 후보 (chapter-pipeline)
  - book-config voice_guidelines (시그니처 패턴)
  - forecast-registry의 등장인물 evidence

【Step 2: 콜드 오픈 작성 (Cold Open Crafter 페르소나)】
  - skeleton.md 명시 콜드 오픈 후보 활용 (예: ch01 한국 자율주행 거리 풍경)
  - 시간·장소·인물·감각 디테일 동반
  - 인용·통계 최소화 (1층 끝 한 문장만 명제)
  - 저자 시그니처 "X와 Y 사이의 거리" 적용 시도

【Step 3: 등장인물 입체화 (Character Animator 페르소나)】
  - 단순 이름 인용 ("머스크가 말했다") → 입체적 인물
  - 직책·맥락·신체 디테일·말투
  - 예: "다보스의 어느 무대, 앤스로픽의 다리오 아모데이가 말한다"

【Step 4: 시나리오 묘사 (Scenario Narrator 페르소나)】
  - 통찰의 시나리오 분기를 *서사적 풍경*으로
  - 예: 봉건제 시나리오 → "키오스크 식당의 풍경 vs 미슐랭 셰프의 풍경"

【Step 5: 역사 평행 narrate (Historical Parallelist 페르소나)】
  - 저자 권위 5층 Layer 5 (역사 평행) 적극 활용
  - 1930년대 대공황·러다이트·핵무기 통제·앵글로색슨 정복
  - 저자 시그니처 "두 창업자가 정확히 같은 N배" 패턴 활용

【Step 6: 시그니처 패턴 정밀 적용 (Signature Weaver 페르소나)】
  - "X가 아니라 Y" (도입·결론)
  - "셋 중 하나가 아니다" (결론)
  - "X와 Y 사이의 거리" (도입)
  - "두 창업자가 정확히 같은 N배" (수렴)

【Step 7: voice·citation gate cross-cutting】

【Step 8: 저자 묶음 (모드 1) — 콜드 오픈 채택】
  - 콜드 오픈 후보 2-3개 제시 (★ 추천)
  - 저자 응답

【Step 9: narrative.md 저장 + lifecycle 갱신】
  - 1층 분량: 챕터 전체의 10-15% 비율
  - 저자 v1 1층 5 검사항 통과 확인
```

---

## 8. Input Schema

```typescript
{
  mode: "cycle" | "cold-open" | "scenario-narrate" | "character" | "historical-parallel"
  target: string
  options: {
    layer_target_percent?: number   // 기본 12 (10-15 중간)
    signature_priority?: boolean    // 시그니처 적용 우선
  }
}
```

---

## 9. Output Schema

### 저자 화면
```markdown
# ⑧ narrative-craft — ch01-economy

## 콜드 오픈 후보 2개

### (a) ★ 한국 자율주행 거리 풍경 (skeleton 명시)
"2026년 봄, 강남 테헤란로 한복판..."
[전문 800자 미리보기]

### (b) ★ 앤스로픽 매출 곡선 0 → 100억 달러
"2024년 1월, 샌프란시스코의 어느 사무실에서..."
[전문 750자 미리보기]

## 등장인물 입체화 (3명)
- Amodei: 다보스 무대 / 매출 곡선 / 1-3년 90% 확신
- Hassabis: 평행 진단 100배 / 알파폴드 50년 난제
- 저자: 한계비용 제로의 AGI 시대 완성 명제

저자: "1=a / 2=...".
```

### 파일 갱신
- chapters/<ch>/narrative.md (콜드 오픈 + 1층 서사)

---

## 10. Deliverable Quality

### 정량 기준
- 1층 분량: 챕터 전체의 10-15% (v1 layer_ratios)
- 저자 v1 1층 5 검사항 통과:
  1. 구체적 시간·장소 명시
  2. 독자 감각 자극
  3. 1층에서 인용·통계 최소화
  4. 1층 끝에 핵심 명제 한 문장
  5. 분량 10-15% 통과
- 시그니처 패턴 활용 1-3개/콜드 오픈
- 등장인물 입체화: 최소 1명 (창업자 + 사상가 + 저자 중)

### 정성 기준
- 독자가 *책을 손에서 놓을 수 없는* 첫 단락
- 단순 사실 나열 X — *영화 콜드 오픈처럼* 장면
- 저자 voice 자연스러움
- skeleton.md 콜드오픈 라이브러리와 정합

---

## 11. Dependencies

### 필수
- ⑥ insight-synthesis 통과 (채택 통찰)
- ⑦ content-expand 통과 (2층 본문 — 1층과 정합)
- skeleton.md (콜드 오픈 라이브러리)
- forecast-registry (등장인물 evidence)

### 후속
- ⑨ structure-review (1·2·3층 분량 비율 검증)
- ⑩ line-edit (문장 미시)

---

## 12. Guards

### Voice·Citation gate cross-cutting
### 1층 분량 가드 (10-15%)
- 초과 시 축약 시도
- 미달 시 확장 시도

### 추상 명제 가드
- 1층에 추상 명제 발견 시 → 구체 장면으로 치환 시도

### 저자 v1 1층 5 검사항 gate
- 5개 모두 통과 필수

### ⭐ Round 7 #C3.3 Critical — Right of Publicity Gate
- *현존 인물 묘사* (Character Animator)에서 AI 추측 영구 금지
- "다보스의 어느 무대, 다리오 아모데이가 [body language·말투·표정]"를 채울 때 *source-verified만* (영상·인터뷰 transcript)
- 모든 캐릭터 묘사 디테일에 `source_path` 강제

### ⭐ Round 7 #C10.4 — Catastrophic Thinking Gate
- 디스토피아 시나리오 묘사 후 *대안 path·agency 명시* 강제
- 부정 시나리오 비율 50% 초과 시 저자 알림 — catastrophic balance recovery

---

## 13. AI Agents Personas (6명)

| # | 페르소나 | 역할 |
|---|---|---|
| 1 | Cold Open Crafter ⭐ | skeleton 콜드오픈 후보 활용·구체 장면 작성 |
| 2 | Character Animator | 등장인물 입체화 (창업자·저자·사상가) |
| 3 | Scenario Narrator | 시나리오 분기를 서사적 풍경으로 |
| 4 | Historical Parallelist | 역사 평행 (Layer 5) narrate |
| 5 | Signature Weaver ⭐ | 5 시그니처 패턴 정밀 적용 |
| 6 | Sensory Detail Adder | 시각·청각·촉각 디테일 추가 |

---

## 14. Cycle (C1-C5)

| Cycle | 트리거 | 작동 |
|---|---|---|
| C1: Chapter Full Narrate | `cycle ch-NNN` | 1층 풀 작성 |
| C2: Cold Open Only | `cold-open` | 콜드 오픈만 (2-3 후보) |
| C3: Scenario Narrate | `scenario-narrate` | 시나리오 묘사만 |
| C4: Character Build | `character` | 등장인물 입체화만 |
| C5: Historical Parallel | `historical-parallel` | 역사 평행 narrate만 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| G1: Input | INSIGHTED·2층 본문 존재 |
| G2: 1층 5 검사항 | 저자 v1 5 검사항 모두 통과 |
| G3: 분량 비율 | 10-15% 도달 |
| G4: 시그니처 패턴 | 1+ 활용 |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| skeleton 콜드오픈 후보 없음 | 저자 시드 기반 신규 콜드 오픈 작성 시도 |
| 1층 5 검사항 위반 | 재작성 시도 + 실패 시 저자 묶음 |
| 분량 미달·초과 | 자동 조정 (resize) |
| 등장인물 evidence 부족 | 저자 알림 + ④ evidence-collect 권장 |

---

## 17. Verification Examples

1. ch01 콜드 오픈: skeleton 명시 후보 (한국 자율주행) 활용 ✅
2. 1층 분량 12% (range 10-15) ✅
3. 시그니처 "X와 Y 사이의 거리" 적용 ✅
4. Amodei·Hassabis 입체화 ✅
5. voice·citation gate 통과 ✅

---

**End of SPEC: bookwriting-narrative-craft-master**

> ⭐ ⑧ narrative-craft는 저자 책의 *독자 끌어당기는 매력*. ⑦ 논증 + ⑧ 매력 = *저자 책이 일반 지식인에게 *손에서 놓을 수 없는* 작품*이 된다.

---

## 부록: 결정론·grill-me·9 항목·Mode 2·R1-R5

### 결정론 모듈
- M5 layer_ratio_measurer (1층 10-15% 검증)
- M8 signature_pattern_applier (5 시그니처 정규식)
- M1 VoiceScorer (voice gate)
- M2 HallucinationDetector (citation gate — 역사 평행도 출처 강제)
- M3 AuthorityGrader (Layer 5 역사 평행 등급)
- 자체 결정론: 저자 v1 1층 5 검사항 정규식 검증

**LLM 허용 영역 (창의 글쓰기)**: 콜드 오픈·등장인물 narrate·서사 묘사 — 결정론 환원 어려움. **단 출처·저자 voice 1:1 준수 강제**.

### grill-me D# 매핑
| D# | §위치 |
|---|---|
| 저자 진북 "매력적인 글로 쓰는 방식이 핵심" | §1·§2 ⭐ |
| 저자 강조 "제2저자 핵심" | §2·§10 |
| D11 시그니처 패턴 | §13 Signature Weaver + 부록 M8 |
| 저자 v1 1층 5 검사항 + 콜드오픈 라이브러리 | §3·§7 |

### 9 항목
(a) §1+§2 / (b) §2 + 저자 진북 / (c) §13 6 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록

### Mode 2
- skeleton 콜드오픈 후보 중 relevance 최고 자동 선택
- 시그니처 패턴 자동 적용
- 저자 묶음 0회

### R1-R5
- R1 quantitative (콜드오픈도 시간·장소 명시)
- R4 다층 (Layer 5 역사 평행 + Layer 1 창업자 발언 등 다층)
- R5 verification_signal (1층 끝 명제도 검증 가능 지표 동반)

**End of SPEC: bookwriting-narrative-craft-master**
