# SPEC: bookwriting-content-expand-master

> 저자 *제2저자 성능 핵심 4개 중 1개*. 저자 진짜 워크플로우 *15단계 매력적 글쓰기*의 *분량 확장* 영역.
>
> 저자 강조: *"매력적인 글로 쓰는 방식이 핵심이다."*
>
> 작성일: 2026-05-24
> 매트릭스: 7 sub + 6 AI Agents + 5 Cycle + 3 Gate (Q18 — 제2저자 핵심)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-content-expand-master` |
| 카테고리 | 단계 마스터 (⑦, MVP 수직 슬라이스 포함) |
| 저자 11 단계 매트릭스 위치 | ⑦ (제2저자 성능 핵심 4개 중 1개) |
| 저자 진짜 워크플로우 매핑 | **15단계 — 매력적 글쓰기 (분량 확장 영역)** |
| 슬래시 | `/bookwriting-content-expand <mode> [target]` |
| 매트릭스 수치 | 7 sub + 6 AI Agents + 5 Cycle + 3 Gate |

---

## 2. Purpose

⑥ insight-synthesis가 *선택한 의미 단면 (통찰)*을 *꼭지 분량의 매력적 본문*으로 확장한다. 저자 책의 *3층 구조* (1층 narrative 10-15% · 2층 analysis 60-70% · 3층 implications 15-25%)에 정확히 배치한다.

**3 책임:**
1. **분량 확장** — 통찰 한 줄 → 꼭지 분량 (1500-4000자)
2. **3층 배치** — chapter_role에 따라 1층·2층·3층 본문 작성
3. **매력 유지** — 저자 voice + 시그니처 패턴 + 시스템 사고 흐름

---

## 3. Philosophy

**저자 8 절대 protocol:**
- #5 3-Layer Description + #6 prefix + #7 Trace

**v1 호환:**
- chapter-pipeline.md의 *2층 표준 골격* (1.핵심명제 재진술 → 2.약신호 → 3.추동력 → 4.시스템 루프 호명 → 5.시나리오 분기 → 6.시점 좌표 → 7.횡단 연결) 그대로 사용
- *layer_ratios* 강제 (10-15% / 60-70% / 15-25%)

**Voice·Citation gate cross-cutting 적용:**
- 모든 출력에 두 gate 자동 발동

---

## 4. Scope

### In scope
- ✅ 통찰을 꼭지 분량으로 확장
- ✅ chapter_role에 따른 1·2·3층 배치
- ✅ 저자 *2층 표준 골격* 준수
- ✅ 저자 voice + 시그니처 패턴 활용
- ✅ chapters/<ch>/narrative.md·analysis.md·implications.md에 본문 작성

### Out of scope
- ❌ 콜드 오픈·서사 매력 도구 (⑧ narrative-craft 담당)
- ❌ 문장 미시 첨삭 (⑩ line-edit 담당)
- ❌ 구조 리뷰·분량 비율 검증 (⑨ structure-review 담당)
- ❌ 다른 스킬 자동 호출 (옵션 A+)

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-content-expand cycle <target>` | 통찰 확장 풀 사이클 |
| `/bookwriting-content-expand layer <insight-id> --layer 2` | 특정 layer로 확장 |
| `/bookwriting-content-expand variant <insight-id> --tone formal\|narrative` | 톤 변경 확장 |
| `/bookwriting-content-expand resize <chapter> --target-chars 3000` | 분량 조정 |

---

## 6. Invocation

```bash
/bookwriting-content-expand cycle ch01-economy        # 풀 사이클
/bookwriting-content-expand cycle INS-001              # 단일 통찰
/bookwriting-content-expand layer INS-001 --layer 2    # 2층 분석으로 확장
```

**인자**: target (ch-NNN·INS-NNN·--all) + `--layer 1|2|3` + `--target-chars N` + `--mode 1|2`

---

## 7. Behavior

**9단계 행동 시나리오:**

```
호출: /bookwriting-content-expand cycle ch01-economy

【Step 1: 입력 검증·자료 로드】
  - ch01의 채택된 통찰 (INSIGHTED lifecycle 시드) 추출
  - chapters/01-economy의 현재 narrative/analysis/implications.md 읽기
  - skeleton.md의 ch01 외골격 (콜드오픈·2층 흐름·3층 함의)
  - book-config의 layer_ratios 로드

【Step 2: 통찰별 layer 결정】
  - 각 통찰의 chapter_role 확인 (1층_콜드오픈/2층_분석/3층_함의)
  - layer 별 통찰 그룹화

【Step 3: 1층 확장 (해당 시 — 콜드오픈은 ⑧로 위임)】
  - narrative.md의 *콜드오픈 부분*은 ⑧ narrative-craft 담당
  - ⑦은 1층의 *맥락 다리* 부분만 확장 (콜드오픈 끝 후 챕터 본문 전환)

【Step 4: 2층 확장 (핵심)】
  - 저자 2층 표준 골격 7요소 따라 확장:
    1. 핵심 명제 재진술 (1층 한 문장을 정량 데이터와 함께)
    2. 약신호 (가시적 증거) — Weak Signal Synthesizer 페르소나
    3. 추동력 (시스템적 힘) — Driving Force Synthesizer 페르소나
    4. 시스템 루프 호명 (어느 변수 어떤 피드백) — System Loop Narrator 페르소나
    5. 시나리오 분기 (정치 변수에 따른 결과)
    6. 시점 좌표 (AGI 5단계와의 동기화)
    7. 횡단 연결 (다른 챕터와의 다리)
  → 분량: 1200-3000자

【Step 5: 3층 확장 (해당 시)】
  - 저자 3층 표준 골격:
    1. 본문이 독자에게 의미하는 것 (한 문장)
    2. 개인 차원 응답
    3. 조직 차원 응답
    4. 정책 차원 응답
    5. (해당 시) 한국 결정 윈도우 호명
    6. (해당 시) 검증 신호 (5년·10년)
  → 분량: 500-1200자

【Step 6: 저자 voice·시그니처 패턴 적용】
  - Voice Aligner 페르소나가 5 시그니처 패턴 활용 시도
  - 저자 preferred 어휘 치환

【Step 7: Voice gate + Citation gate cross-cutting】
  - 모든 layer 본문에 두 gate 자동 발동
  - 위반 시 처리 (재작성 또는 저자 묶음)

【Step 8: 저자 묶음 (모드 1) — 확장 방향 선택】
  - 저자가 확장 *방향* 결정 (예: 약신호 위주 vs 시스템 루프 위주 vs 시나리오 위주)
  - 묶음: 통찰별 확장안 2-3개 제시

【Step 9: 본문 저장 + lifecycle 갱신】
  - narrative/analysis/implications.md 갱신
  - 통찰 lifecycle INSIGHTED → POLISHED 진입 준비 (실제 POLISHED는 ⑩ line-edit 통과 후)
```

---

## 8. Input Schema

```typescript
{
  mode: "cycle" | "layer" | "variant" | "resize"
  target: string         // ch-NNN | INS-NNN
  options: {
    layer?: 1 | 2 | 3
    target_chars?: number       // 분량 조정 시
    tone?: "formal" | "narrative"
    mode_1_or_2?: 1 | 2
  }
}
```

**파일 입력**: skeleton.md / seed-registry (INSIGHTED 시드) / chapters/<ch>/* / book-config

---

## 9. Output Schema

### 저자 화면 (모드 1)
```markdown
# ⑦ content-expand — ch01-economy

## 통찰 INS-001 → 2층 확장안

### (a) ★ 약신호 중심 (1800자)
"한국 자율주행 택시가 거리에 나선 2025년..."
[전문 1800자 미리보기]

### (b) ★ 시스템 루프 중심 (2200자)
"L1 지능대체나선의 변수 1은 인지 외주화다..."
[전문 2200자 미리보기]

### (c) 시나리오 분기 중심 (2400자)
[전문 2400자 미리보기]

저자: "1=a / 2=b" 또는 자연어
```

### 파일 갱신
- `chapters/<ch>/narrative.md` (1층 맥락 다리)
- `chapters/<ch>/analysis.md` (2층 분석 — 핵심)
- `chapters/<ch>/implications.md` (3층 함의)

---

## 10. Deliverable Quality

### 정량 기준
- 2층 분량: 1200-3000자/통찰
- 3층 분량: 500-1200자/통찰
- layer_ratios 챕터 전체 통과
- 시그니처 패턴 활용률: 30%+
- voice_score: 0.7+ (모든 본문)
- citation 권위 5층 매핑: 평균 2.5층+

### 정성 기준
- 저자 2층 표준 골격 7요소 모두 포함
- 저자 3층 표준 골격 6요소 모두 포함 (해당 시)
- 저자 시스템 사고 흐름 자연스러움
- 단순 자료 나열이 아닌 *해석·통찰 직조*

---

## 11. Dependencies

### 필수
- ⑥ insight-synthesis 통과 (INSIGHTED 시드)
- skeleton.md / book-config / seed-registry / chapters/<ch>/*

### 후속
- ⑧ narrative-craft (콜드오픈·서사 매력)
- ⑨ structure-review (분량 비율 검증)
- ⑩ line-edit (문장 미시)

### 비의존
- 설치된 다른 스킬

---

## 12. Guards

### Voice cross-cutting gate ⭐
- 모든 layer 본문에 자동 발동
- voice_score < 0.7 시 자동 재작성

### Citation cross-cutting gate ⭐
- 모든 layer 본문의 인용 검증
- Critical 위반 → 저자 묶음 escalate

### Layer Ratio gate
- 챕터 전체 분량 비율 1층 10-15% / 2층 60-70% / 3층 15-25% 검증
- 위반 시 ⑨ structure-review 자동 호출 권장

### 저자 2층 표준 골격 gate
- 7요소 누락 검출 시 저자 알림 + 재확장 시도

---

## 13. AI Agents Personas (6명)

| # | 페르소나 | 역할 |
|---|---|---|
| 1 | **Weak Signal Synthesizer** | 약신호 (가시적 증거) 본문 작성 — 한국 택시·앤스로픽 매출·코슬라 80% 등 |
| 2 | **Driving Force Synthesizer** | 추동력 (시스템적 힘) — 한계비용 제로·자본 동원 등 |
| 3 | **System Loop Narrator** | 시스템 루프·변수·피드백 본문 작성 |
| 4 | **Scenario Brancher** | 시나리오 분기 (봉건제 vs 풍요·평화의 역설) 본문 |
| 5 | **Time Coordinator** | 시점 좌표·AGI 5단계 동기화·횡단 연결 |
| 6 | **Voice Aligner ⭐** | 5 시그니처 패턴 적용 + 저자 preferred 어휘 치환 |

---

## 14. Cycle

| Cycle | 트리거 | 작동 |
|---|---|---|
| **C1: Full Chapter Expand** | `cycle ch-NNN` | 챕터 모든 통찰 1·2·3층 확장 |
| **C2: Single Insight Expand** | `cycle INS-NNN` | 단일 통찰 확장 |
| **C3: Layer Specific** | `layer INS-NNN --layer 2` | 특정 layer만 |
| **C4: Tone Variant** | `variant --tone formal` | 톤 변경 |
| **C5: Resize** | `resize --target-chars N` | 분량 조정 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| **G1: Input** | INSIGHTED 시드 ≥1개 |
| **G2: Layer Structure** | 저자 2층 7요소·3층 6요소 포함 |
| **G3: Layer Ratios** | 챕터 분량 비율 통과 |
| **G4: Voice·Citation** | 두 gate 통과 |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| INSIGHTED 시드 없음 | abort + ⑥ insight-synthesis 재호출 권장 |
| 2층 7요소 누락 | 재확장 시도 + 누락 페르소나 발동 |
| 분량 초과·미달 | resize 자동 시도 (5% 범위) + 저자 알림 |
| Voice·Citation gate 위반 | 각 gate 정책 따름 |

---

## 17. Verification Examples

### 검증 1: 챕터 풀 확장
```bash
/bookwriting-content-expand cycle ch01-economy
✅ 5 INSIGHTED 시드 확장
✅ 2층 7요소 모두 포함 (재진술·약신호·추동력·루프·시나리오·시점·횡단)
✅ 분량: 2400자/통찰 (range 1200-3000)
✅ 시그니처 패턴 활용률: 38%
✅ voice_score 모두 0.7+
✅ citation 권위 평균 2.7층
✅ chapters/01-economy/analysis.md +12000자
```

### 검증 2: 1·2·3층 분량 비율
```bash
$ wc -w narrative.md analysis.md implications.md
✅ 1층: 13% (range 10-15)
✅ 2층: 64% (range 60-70)
✅ 3층: 23% (range 15-25)
```

### 검증 3: 시그니처 패턴 적용
```bash
# 통찰 본문에 "X가 아니라 Y" 자동 적용
"AGI는 *더 똑똑한 AI가 아니라*, 인지 자체를 확장하는 *메타도구다*"
✅ 시그니처 1 활용
```

### 검증 4: voice·citation gate 통과
```bash
# 본문 작성 후 두 gate 자동 발동
✅ voice_score 0.82
✅ citation 7개 추출, 모두 source_file 검증 통과
✅ R4 다층 통과율 100%
```

### 검증 5: 분량 조정
```bash
/bookwriting-content-expand resize ch01-economy --target-chars 8000
✅ 현재 분량 9200자 → 8000자로 축약
✅ 저자 voice·시그니처 보존
✅ 핵심 요소 (7요소) 모두 유지
```

---

## 부록: 저자 v1 chapter-pipeline.md 2층·3층 표준 골격 그대로 사용

(chapter-pipeline.md 인용)

**2층 표준 골격:**
```
1. 핵심 명제 재진술 (1층 한 문장을 정량 데이터와 함께)
2. 약신호 (Weak Signal) — 가시적 증거
3. 추동력 (Driving Force) — 시스템적 힘
4. 시스템 루프 호명 — 변수·피드백
5. 시나리오 분기 — 정치 변수
6. 시점 좌표 — AGI 5단계
7. 횡단 연결 — 다른 챕터
```

**3층 표준 골격:**
```
1. 본문이 독자에게 의미하는 것 (한 문장)
2. 개인 차원 응답
3. 조직 차원 응답
4. 정책 차원 응답
5. (해당 시) 한국 결정 윈도우
6. (해당 시) 검증 신호
```

---

---

## 부록 A: 결정론 환원 모듈
| 작업 | 모듈 |
|---|---|
| 분량 측정·layer_ratios 검증 | M5 layer_ratio_measurer |
| 시그니처 패턴 적용 | M8 signature_pattern_applier |
| voice_score 재계산 | M1 VoiceScorer |
| citation 메타 검증 | M2 HallucinationDetector |
| 시드 lifecycle EXPANDED 진행 | M11 lifecycle_state_machine |

**LLM 허용 영역**: 2층 7요소 본문 작성 자체 (창의 영역). 단, 저자 v1 chapter-pipeline.md 양식 1:1 준수 강제.

## 부록 B: grill-me D# 매핑
| D# | §위치 |
|---|---|
| D11 시그니처 5 패턴 | §7 Step 6 + 부록 A M8 |
| 저자 v1 2층 7요소 골격 | §7 Step 4 + 부록 골격 인용 |
| D16 두 모드 | §7 모드 1·2 + 부록 D 아래 |
| Q33 cross-cutting | §12 Citation Gate |

## 부록 C: 9 항목
(a) §1+§2 / (b) §2 / (c) §13 6 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 모드 분기 / (h) §16 / (i) 부록 A

## 부록 D: Mode 2 자동
모드 2 (`--mode 2`):
- 저자 묶음 0회·★ 추천 자동 채택 (확장 방향)
- 결과 → `_simulations/sim-NNN-expanded.md`
- 정식 chapter 파일 미갱신

## 부록 E: R1-R5 적용
| R1 quantitative_anchor | §10 정량 앵커 평균 X/통찰 |
| R2 chapter_role | §7 Step 2 layer 결정 |
| R3 system_loops | §13 System Loop Narrator 호명 강제 |
| R4 다층 인용 | citation-gate cross-cutting |
| R5 verification_signal | §10 검증 신호 본문 명시 |

---

## 부록 F: 3층 7요소 확장 (Round 7 #C10.6·#C7.7·#C5.5 Critical)

저자 v1 chapter-pipeline 3층 6요소 → *3층 7요소*로 확장:
1. 본문 의미 한 문장
2. 개인 차원 응답
3. 조직 차원 응답
4. 정책 차원 응답
5. (해당 시) 한국 결정 윈도우 (KW-1·KW-2·KW-3)
6. (해당 시) 검증 신호 (verification_signal)
7. ⭐ **(해당 시) 정신건강·지원 안내** (Round 7 #C10.6) — 위기 hotline·전문가 상담·자조모임. 저자 책이 의미 위기·자살·우울·실직·소외 주제 다룰 때 *반드시* 포함.

추가 *선택* 차원:
- 8. *세대 차원* (#C7.7) — 청소년·중장년·고령 인구 응답 분리
- 9. *환경·자원 차원* (#C5.5) — 자원 제약 인식

## 부록 G: 2층 8요소 확장 (Round 7 #C5.5·#C2.3)

저자 v1 2층 7요소 → *2층 8요소*로 확장:
1-7 (기존 골격 그대로)
8. ⭐ **(선택) 영적·도덕적 차원** (#C2.3) — 저자 종교적 입장 명시 책에서 활성화
9. **(선택) 자원·환경 제약** (#C5.5) — Climate Hidden Cost 인식

**End of SPEC: bookwriting-content-expand-master**

> ⭐ ⑦ content-expand는 *저자 통찰을 책 본문으로 만드는* 핵심 단계. 저자 *2층·3층 표준 골격*과 *시그니처 패턴*이 정확히 적용되어야 *저자 책 본문이 된다*.
