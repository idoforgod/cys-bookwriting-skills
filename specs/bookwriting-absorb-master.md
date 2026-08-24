# SPEC: bookwriting-absorb-master

> bookwriting 사이클의 *진입 단계*. 저자 외부 manual (foresight 결과)·저자 시드·자산 발굴 결과를 *4 type으로 분류·시드 등록·라우팅 제안*.
>
> 작성일: 2026-05-24
> 매트릭스: 4 sub + 4 AI Agents + 3 Cycle + 3 Gate (Q18)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-absorb-master` |
| 카테고리 | 단계 마스터 (①, MVP 수직 슬라이스 포함) |
| 저자 11 단계 매트릭스 위치 | ① (진입 정밀도 핵심) |
| 저자 진짜 워크플로우 매핑 | (흡수 영역 — 저자 1-13단계 결과를 받음) |
| 슬래시 | `/bookwriting-absorb <mode> [target]` |
| 매트릭스 수치 | 4 sub + 4 AI Agents + 3 Cycle + 3 Gate |

---

## 2. Purpose

저자가 외부에서 manual 호출한 *foresight 사슬 결과* + *저자 시드 입력* + *drop-folder 적재 자산*을 *4 type (seed·evidence·insight·cycle-input)*으로 분류하고 *seed-registry에 등록·라우팅 제안*한다. 후속 모든 단계 마스터의 *진입 정밀도*가 ① absorb의 품질로 결정된다.

**4 책임:**
1. **분류** — inbox·import 파일을 4 type으로 자동 분류
2. **시드 등록** — type=seed 자산을 seed-registry에 등록 (S-NNN ID 발급)
3. **라우팅 제안** — skeleton.md 매칭으로 챕터·layer·chapter_role 후보 제시
4. **frontmatter 검증** — 저자 Q13-D-3 (c) 정책 — frontmatter 우선

---

## 3. Philosophy

**저자 옵션 A+ 자기완결:**
- 외부 web 호출 안 함
- 저자 외부 manual 호출 결과만 흡수

**옵션 D 느슨한 결합 (Q13):**
- import (동기 즉시) + drop-folder (비동기 누적) 둘 다 처리
- frontmatter 우선 (Q13-D-3 c)

**Citation Gate cross-cutting 적용:**
- 흡수 시점에 *원본 자료의 출처 메타데이터* 검증
- 출처 누락 자산은 저자 묶음 escalate

---

## 4. Scope

### In scope
- ✅ inbox/*.md 파일 일괄 처리
- ✅ /bookwriting import 즉시 처리
- ✅ 4 type 자동 분류 (frontmatter `type` 우선, 없으면 자동 추측)
- ✅ seed 자산을 seed-registry에 등록
- ✅ evidence 자산을 chapters/<ch>/evidence-track.yaml *예비 등록*
- ✅ insight 자산을 (사이클 진행 중이면) ⑥ insight-synthesis 후보 풀에 추가
- ✅ cycle-input 자산을 (사이클 진행 중이면) bookwriting-master에 전달
- ✅ 라우팅 cascade (Q20-D-3 d): 키워드 → Claude 의미 평가 → Obsidian 풀

### Out of scope
- ❌ 자산 내용 *깊은 분석* (③ systemlink·④ evidence-collect 담당)
- ❌ 통찰 *평가* (⑥ insight-synthesis 담당)
- ❌ NotebookLM 직접 query (bookwriting-notebooklm-bridge 담당)
- ❌ Obsidian vault 검색 (③ systemlink 담당 — ① absorb는 *inbox·import만*)

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-absorb inbox` | inbox/ 일괄 흡수 |
| `/bookwriting-absorb import <path>` | 단일 파일 즉시 흡수 |
| `/bookwriting-absorb classify <path>` | 자산 type 분류만 (등록 X) |
| `/bookwriting-absorb route <S-NNN>` | 시드 라우팅 제안만 |

---

## 6. Invocation

```bash
/bookwriting-absorb inbox                                    # inbox 일괄
/bookwriting-absorb import /path/to/foresight-result.md      # 즉시
/bookwriting-absorb import /path/to/output.md --as seed --to ch01    # type·라우팅 명시
/bookwriting-absorb classify /path/to/file.md                # 분류만
```

---

## 7. Behavior

**9단계 행동 시나리오:**

```
호출: /bookwriting-absorb inbox

【Step 1: inbox 스캔】
  - $BOOK_ROOT/inbox/*.md 모든 파일 발견
  - 파일별 mtime·크기 확인
  → trace: "inbox 5 파일 발견"

【Step 2: frontmatter 추출 (Frontmatter Parser 페르소나)】
  - 각 파일 yaml frontmatter 파싱
  - type 필드 우선 추출 (seed·evidence·insight·cycle-input)
  - link·to·source·created 등 메타 필드
  - frontmatter 없으면 → Step 3 type 추측

【Step 3: Type 자동 추측 (해당 시 — Type Classifier 페르소나)】
  - 저자 Q13-D-2 (c) 자동 추측 옵션
  - 추측 규칙:
    - 짧은 명제·통찰 → seed
    - 출처·인용·통계 풍부 → evidence
    - "통찰·결론·해석" 단어 → insight
    - 외골격·구조·flow 단어 → cycle-input
  - 모호 시 저자 묶음 escalate

【Step 4: Citation Gate (자동 발동 — 원본 메타데이터)】
  - 흡수 자산의 *원본 출처*가 명시되었는가
  - source·author·date 누락 → Citation Gate Medium 위반
  - 저자 알림 + 진행 (절대 차단은 아님 — 저자가 흡수 결정 자유)

【Step 5: Type별 처리 분기】
  
  [Type = seed]
    - seed-registry에 S-NNN 등록
    - 라우팅 cascade 발동 (Step 6)
  
  [Type = evidence]
    - 라우팅 챕터 결정 → chapters/<ch>/evidence-track.yaml 예비 등록
    - ④ evidence-collect의 다음 사이클에서 *우선 검토 대상*
  
  [Type = insight]
    - 라우팅 챕터 결정
    - 사이클 진행 중이면 ⑥ insight-synthesis 후보 풀에 추가
    - 사이클 없으면 pending_insights에 보관
  
  [Type = cycle-input]
    - bookwriting-master에 *흐름 조정 입력*으로 전달
    - 예: skeleton.md 부분 수정·새 챕터 흐름 제안

【Step 6: 라우팅 cascade (Q20-D-3 d) — Route Cascade 페르소나】
  
  [L1: 키워드 매칭]
    - skeleton.md의 각 챕터·section 키워드와 자산 텍스트 매칭
    - 매칭 점수 0-1
  
  [L2: Claude 의미 평가 (모호 시)]
    - L1 매칭 점수 ≥ 0.8 → 명확 → Step 7
    - L1 매칭 점수 < 0.8 → Claude 의미 평가
  
  [L3: Obsidian 풀 참조 (더 모호 시)]
    - L2 결과 confidence < 0.7 → Obsidian vault에서 *비슷한 주제 다룬 곳* 참조
    - 저자 기존 글 패턴으로 *라우팅 추론*

【Step 7: 라우팅 묶음 제안 (모드 1)】
  - 저자가 명시 (--to·--link) 안 한 경우만 묶음
  - 후보 챕터·layer·chapter_role 3-5개 제시
  - ★ 추천 (cascade 최고 점수)
  - 저자 응답: "1=a / 2=b"

【Step 8: seed-registry·evidence-track·관련 파일 갱신】
  - type=seed: seed-registry seed[] append
  - type=evidence: chapters/<ch>/evidence-track.yaml *예비 등록*
  - type=insight: chapters/<ch>/pending-insights.yaml 등록
  - type=cycle-input: bookwriting-master에 즉시 전달

【Step 9: inbox 파일 정리】
  - 처리 완료된 inbox 파일을 inbox/_processed/ 로 이동
  - 처리 실패·저자 묶음 대기 파일은 inbox/에 잔류
  - 통계 출력: "5 흡수 / 4 등록 / 1 저자 묶음 대기"
```

---

## 8. Input Schema

```typescript
{
  mode: "inbox" | "import" | "classify" | "route"
  target?: string         // import의 경로 | route의 S-NNN
  options: {
    as?: "seed" | "evidence" | "insight" | "cycle-input"
    to?: string         // ch-NNN
    link?: string       // S-NNN
    auto_route?: boolean    // 라우팅 cascade 발동 (기본 true)
  }
}
```

**파일 입력**:
- `inbox/*.md` (mode=inbox)
- `--target 경로` (mode=import)
- skeleton.md, seed-registry, book-config

---

## 9. Output Schema

### 저자 화면
```markdown
# ① absorb — inbox 일괄 흡수

## 발견 자산 (5개)

### (a) 2026-05-20-amodei-machines.md
- type: evidence (frontmatter 명시)
- source: Amodei 2024
- 권위: Grade A
- 라우팅: ch01-economy (★ 추천 점수 0.92)

### (b) 2026-05-22-scenarios-output.md
- type: cycle-input (자동 추측 confidence 0.85)
- 출처: 저자 /foresight-scenarios manual 호출
- 라우팅: ch07-cosmic + ch08-meaning 후보

### (c) ...

## 저자 묶음

### 라우팅 묶음 1: (b) 자산의 챕터
- (a) ★ ch07-cosmic (cascade 0.78)
- (b) ★ ch08-meaning (cascade 0.74)
- (c) 다중 라우팅 (primary ch07 + cross-ref ch08)
- (d) defer

저자: "1=c" (다중 라우팅 채택)
```

### 파일 갱신
- `seed-registry.yaml` (type=seed)
- `chapters/<ch>/evidence-track.yaml` (type=evidence 예비)
- `chapters/<ch>/pending-insights.yaml` (type=insight)
- `inbox/_processed/` (처리 완료 이동)

---

## 10. Deliverable Quality

### 정량 기준
- frontmatter 인식률: 95%+
- type 자동 추측 정확도: 85%+
- 라우팅 cascade 정확도: 80%+ (저자 spot-check)
- citation Medium 위반: warning 후 진행
- 처리 latency: 5-20초/파일

### 정성 기준
- 저자 흡수 결정 자유 보장 (Critical 차단 안 함)
- 라우팅 묶음의 ★ 추천이 저자 의도와 일치
- inbox 정리로 *후일 추적* 가능

---

## 11. Dependencies

### 필수
- book-config / seed-registry / cycle-registry / skeleton.md
- inbox/ 디렉토리

### 후속
- ② fact-anchor (흡수된 evidence·시드 검증)
- ③ systemlink (자산 풀 검색)

### 비의존
- 다른 스킬·web

---

## 12. Guards

### Citation Gate (Medium만 적용)
- 흡수 시점은 *Critical 차단 안 함* — 저자 흡수 결정 자유
- Medium 위반은 warning + 진행

### Voice Gate (해당 없음)
- ① absorb는 *분류·등록만* — 저자 voice 표현 작업 없음

### Type 분류 가드
- 자동 추측 confidence < 0.7 → 저자 묶음 escalate

### 라우팅 가드
- cascade L3까지도 confidence < 0.5 → unrouted 상태로 보관 + 저자 묶음 권장

---

## 13. AI Agents Personas (4명)

| # | 페르소나 | 역할 |
|---|---|---|
| 1 | **Frontmatter Parser** | yaml frontmatter 파싱·필수 필드 추출 |
| 2 | **Type Classifier** | 4 type 자동 추측 (규칙 + Claude 평가) |
| 3 | **Route Cascade** | 3-Layer cascade 라우팅 (키워드 → Claude → Obsidian) |
| 4 | **Inbox Organizer** | _processed/ 이동·통계 출력 |

---

## 14. Cycle

| Cycle | 트리거 | 작동 |
|---|---|---|
| **C1: Inbox Batch** | `inbox` | inbox 일괄 처리 |
| **C2: Immediate Import** | `import <path>` | 단일 파일 즉시 |
| **C3: Classify Only** | `classify <path>` | 분류만 (등록 X) |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| **G1: Discovery** | inbox 파일 발견 또는 path 유효 |
| **G2: Type Determined** | 4 type 중 1개 결정 (frontmatter 또는 추측) |
| **G3: Routing or Defer** | 라우팅 cascade 또는 명시·저자 묶음 |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| inbox 빈 폴더 | 정상 — "0 파일 발견" 출력 |
| frontmatter 파싱 실패 | type 자동 추측 fallback + 저자 알림 |
| 라우팅 cascade 모두 confidence < 0.5 | unrouted + 저자 묶음 권장 |
| seed-registry next_id 동기화 실패 | max S-NNN + 1 재계산 |
| inbox 파일 _processed/ 이동 실패 | warning + 원본 보존 |

---

## 17. Verification Examples

### 검증 1: inbox 일괄 흡수
```bash
/bookwriting-absorb inbox
✅ 5 파일 발견
✅ frontmatter 4개 / 자동 추측 1개
✅ type 분류: seed 2 / evidence 2 / cycle-input 1
✅ 라우팅 cascade 평균 confidence 0.85
✅ seed-registry +2 S-NNN
✅ evidence-track +2 예비 등록
✅ inbox/_processed/로 4 파일 이동
```

### 검증 2: 즉시 import
```bash
/bookwriting-absorb import /path/to/scenarios.md --as cycle-input --to ch07
✅ 명시 type·라우팅 그대로 적용
✅ frontmatter 검증 통과
✅ bookwriting-master에 cycle-input 즉시 전달
```

### 검증 3: Type 자동 추측
```bash
# inbox 파일: 출처·인용 풍부, 메타데이터 명시
/bookwriting-absorb classify /path/to/file.md
✅ 자동 추측: evidence (confidence 0.92)
✅ 분류만 진행, 등록 X
```

### 검증 4: 라우팅 cascade
```bash
# 자산: "한국 자율주행 택시 점유율 30%"
✅ L1 키워드 매칭: ch01-economy (0.85)
✅ confidence 0.85 ≥ 0.8 → L2 생략
✅ ch01-economy 라우팅 ★ 추천
```

### 검증 5: 저자 묶음 (모호 라우팅)
```bash
# 자산: 메타도구 + 봉건제 + 정치
✅ L1: ch01·ch03·ch10 후보 (모두 0.65-0.75)
✅ L2 Claude 의미 평가
✅ L3 Obsidian 풀 참조
✅ 저자 묶음: "1=ch01 / 2=ch03 / 3=ch10 / 4=다중"
✅ 저자 응답: "1=4 (다중)"
```

### 검증 6: inbox 정리
```bash
$ ls $BOOK_ROOT/inbox/_processed/
✅ 처리 완료 파일들 정리됨
$ ls $BOOK_ROOT/inbox/
✅ 미처리·저자 묶음 대기 파일만 잔류
```

---

---

## 부록: 결정론·grill-me·9 항목·Mode 2

### 결정론 모듈
- frontmatter 파싱: 자체 결정론 (yaml.safe_load)
- type 자동 추측: 결정론 규칙 + LLM 의미 평가 fallback (confidence < 0.7 시 저자 묶음 강제)
- 라우팅 cascade L1 키워드: 자체 결정론 (정규식·키워드 빈도)
- L2 Claude 의미 평가: LLM 허용 (단, confidence 점수 결정론)
- L3 Obsidian: M6 relevance_scorer
- ID 발급 (S-NNN): M7 id_generator
- inbox 파일 이동: 자체 결정론 (pathlib.shutil.move)

**LLM 추론 금지**: confidence 점수 자체 추측·라우팅 결정 *근거 없이*

### grill-me D# 매핑
- D5 (입력 채널·4 type): §1·§2·§7
- D13 (inbox·import·frontmatter 우선): §2 + §3
- D20 (라우팅 cascade): §7 Step 6
- D16 (모드 1·2): Mode 2 자동 모드 — 모든 자동 추측 진행·저자 묶음 0회

### 9 항목
(a) §1+§2 / (b) §2 / (c) §13 4 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록 ⭐

### Mode 2 자동
- type 자동 추측 confidence < 0.7도 진행 (auto Type 부여 + trace 명시)
- 라우팅 cascade L1·L2·L3 모두 자동
- 저자 묶음 0회

**End of SPEC: bookwriting-absorb-master**

> ① absorb는 모든 단계의 *진입 정밀도*를 결정. type 분류·라우팅 cascade가 정확해야 후속 ②~⑪ 모든 단계의 품질이 보장된다.
