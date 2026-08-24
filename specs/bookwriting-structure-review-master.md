# SPEC: bookwriting-structure-review-master

> 챕터·꼭지 *구조·분량·층 균형* 리뷰. 저자 v1 layer_ratios (1층 10-15% / 2층 60-70% / 3층 15-25%) 강제 + v1 2층·3층 표준 골격 요소 누락 검출.
>
> 작성일: 2026-05-24
> 매트릭스: 7 sub + 6 AI Agents + 5 Cycle + 4 Gate (Q18)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-structure-review-master` |
| 카테고리 | 단계 마스터 (⑨) — Phase 3-B |
| 저자 11 단계 매트릭스 위치 | ⑨ |
| 저자 진짜 워크플로우 매핑 | (정합성 영역) |
| 슬래시 | `/bookwriting-structure-review <mode> [target]` |
| 매트릭스 수치 | 7 sub + 6 AI Agents + 5 Cycle + 4 Gate |

---

## 2. Purpose

⑦·⑧이 작성한 챕터 본문의 *구조·분량·층 균형*을 저자 v1 layer_ratios에 맞게 검증·조정. 저자 v1 2층·3층 표준 골격 요소 (7요소·6요소) 누락 자동 검출. ⑩ line-edit 진입 전 *구조 정합성 보장*.

**4 책임:**
1. **분량 비율 검증** — 1층 10-15% / 2층 60-70% / 3층 15-25%
2. **2층·3층 표준 골격 요소 검증** — 저자 v1 chapter-pipeline 양식
3. **챕터 흐름 일관성** — 1층 콜드오픈 → 2층 분석 → 3층 함의의 *자연스러운 흐름*
4. **R4·R5 정합성 (v1)** — 권위 5층 균형·검증 신호 명시

---

## 3. Philosophy

**저자 v1 chapter-pipeline.md *직접 호환*:**
- layer_ratios 그대로
- 2층 표준 골격 7요소 그대로
- 3층 표준 골격 6요소 그대로
- R1-R5 정합성 규칙

**Voice·Citation gate cross-cutting 적용**:
- 구조 변경 시 voice·citation 재검증

---

## 4. Scope

### In scope
- ✅ 챕터 1·2·3층 분량 비율 측정·조정 권장
- ✅ 저자 v1 2층 7요소·3층 6요소 누락 검출
- ✅ 챕터 내 *흐름 끊김* 자동 감지
- ✅ R4 권위 분포 균형 검증
- ✅ R5 검증 신호 누락 검출
- ✅ chapters/<ch>/*.md 구조 조정

### Out of scope
- ❌ 본문 내용 자체 수정 (⑦ content-expand·⑩ line-edit 담당)
- ❌ 통찰 추가 (⑥ insight-synthesis 담당)
- ❌ cross-chapter 정합 (⑪ cross-chapter-relink 담당)

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-structure-review cycle <chapter>` | 풀 사이클 |
| `/bookwriting-structure-review ratios <chapter>` | 분량 비율만 |
| `/bookwriting-structure-review elements <chapter>` | 2층·3층 요소 누락만 |
| `/bookwriting-structure-review flow <chapter>` | 흐름 일관성만 |
| `/bookwriting-structure-review verification-signals <chapter>` | R5 검증 신호만 |

---

## 6. Invocation

```bash
/bookwriting-structure-review cycle ch01-economy
/bookwriting-structure-review ratios ch01-economy
/bookwriting-structure-review elements ch01-economy   # 7요소·6요소
```

---

## 7. Behavior (요약)

```
Step 1: chapters/<ch>/narrative·analysis·implications.md 로드
Step 2: 분량 측정 (Layer Ratio Measurer 페르소나)
  - wc -w narrative.md / analysis.md / implications.md
  - 비율 계산 + range 비교
Step 3: 2층 7요소 검출 (Element Checker — 2층)
  - 핵심명제·약신호·추동력·시스템루프·시나리오·시점·횡단
Step 4: 3층 6요소 검출 (Element Checker — 3층)
  - 의미·개인·조직·정책·한국윈도우·검증신호
Step 5: 챕터 흐름 일관성 (Flow Validator 페르소나)
  - 1층 콜드오픈의 핵심 명제 → 2층 본문 입증 → 3층 함의 정합
Step 6: 권위 분포 검증 (R4 Distribution Analyzer)
Step 7: 검증 신호 누락 검출 (R5 Verifier)
Step 8: 저자 묶음 (모드 1) — 조정 권장
  - 분량 미달·초과 (resize 권장)
  - 요소 누락 (해당 sub 재호출 권장)
  - 흐름 끊김 (재작성 권장)
Step 9: chapter 파일 갱신 또는 저자 결정 후 단계 재호출
```

---

## 8·9. Input·Output

**Input**: chapters/<ch>/*.md / book-config.layer_ratios / forecast-registry

**Output (저자 화면)**:
```markdown
# ⑨ structure-review — ch01-economy

## 분량 비율 측정
| Layer | 분량 | 비율 | 목표 | 상태 |
|---|---|---|---|---|
| 1층 narrative | 850자 | 9% | 10-15% | ⚠️ 미달 |
| 2층 analysis | 7200자 | 78% | 60-70% | ⚠️ 초과 |
| 3층 implications | 1200자 | 13% | 15-25% | ⚠️ 미달 |

## 2층 7요소 검출
- ✅ 핵심명제 재진술
- ✅ 약신호
- ⚠️ 추동력 누락 (driving-force-synthesizer 재호출 권장)
- ✅ 시스템루프 호명
- ✅ 시나리오 분기
- ✅ 시점 좌표
- ✅ 횡단 연결

## 3층 6요소 검출
- ✅ 의미 한 문장
- ✅ 개인 차원
- ✅ 조직 차원
- ⚠️ 정책 차원 약함
- ✅ 한국 윈도우 KW-1
- ⚠️ 검증 신호 누락

저자 묶음:
1. 분량 조정: (a) 1층 확장 (b) 2층 축약 (c) 3층 확장 (d) 종합 조정
2. 누락 요소: (a) 추동력 sub 재호출 (b) ...
3. 흐름: (a) 1층 명제 → 2층 입증 정합 OK (b) ...
```

---

## 10. Deliverable Quality

### 정량 기준
- 분량 비율 측정 정확도 99%+
- 7요소·6요소 검출 정확도 95%+
- 흐름 일관성 평가 80%+
- 권위 5층 균형 검증 100%

### 정성 기준
- 저자 v1 layer_ratios 엄격 준수
- 저자 v1 골격 7+6 요소 누락 0건 목표
- 챕터 흐름 *독자 끌어당김*

---

## 11. Dependencies

### 필수
- ⑦ content-expand 통과 (2층·3층 본문)
- ⑧ narrative-craft 통과 (1층 콜드오픈)
- book-config.layer_ratios
- forecast-registry (R4·R5 검증)

### 후속
- ⑩ line-edit (구조 통과 후)

---

## 12. Guards

### Voice·Citation gate cross-cutting
### Layer Ratio Gate (전용)
- 위반 시 자동 조정 시도 (5% 범위)·실패 시 저자 묶음
### 7요소·6요소 Gate
- 누락 시 해당 sub 재호출 권장
### R4·R5 Gate
- 위반 시 저자 묶음

---

## 13. AI Agents Personas (6명)

1. Layer Ratio Measurer
2. Element Checker (2층 7요소 + 3층 6요소)
3. Flow Validator
4. R4 Distribution Analyzer
5. R5 Verifier
6. Resize Recommender

---

## 14. Cycle (C1-C5)

| Cycle | 트리거 | 작동 |
|---|---|---|
| C1: Chapter Full Review | `cycle ch-NNN` | 전체 검증 |
| C2: Ratios Only | `ratios` | 분량만 |
| C3: Elements Only | `elements` | 요소만 |
| C4: Flow Only | `flow` | 흐름만 |
| C5: Verification Signals | `verification-signals` | R5 신호만 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| G1: Input | chapter 파일 3개 존재 |
| G2: Layer Ratios | 모든 layer range 통과 |
| G3: Elements Coverage | 7+6 요소 통과율 90%+ |
| G4: R4·R5 | 위반 0건 또는 저자 결정 |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| chapter 파일 누락 | abort + 저자 알림 |
| layer 분량 30%+ 초과·미달 | resize 시도 → 실패 시 저자 묶음 |
| 요소 누락 다수 (3+) | 저자 일괄 묶음 + 해당 sub 재호출 권장 |

---

## 17. Verification Examples

1. ch01 분량 측정: 1층 13% / 2층 65% / 3층 22% ✅
2. 7요소 누락 0건 ✅
3. 6요소 누락 1건 (검증 신호) → ④ verification-signal-finder 재호출
4. 흐름 일관성: 1층 명제 → 2층 입증 → 3층 함의 정합 ✅
5. R4 통과율 88%·R5 검증신호 5건 ✅

---

---

## 부록: 결정론·grill-me·9 항목·Mode 2·R1-R5

### 결정론 모듈
- M5 layer_ratio_measurer ⭐ (wc -w 측정·range 검증·resize 권장)
- M3 AuthorityGrader (R4 권위 분포 분석)
- M13 r4_multi_layer_verifier
- 자체 결정론: 저자 v1 2층 7요소·3층 6요소 검출 (정규식·키워드 매칭)
- 자체 결정론: 1·2·3층 흐름 일관성 (1층 명제와 2층 입증 키워드 매칭)

**LLM 허용**: 흐름 *질적 평가* (단, 저자 v1 chapter-pipeline 양식 정합 강제)

### grill-me D# 매핑
| D# | §위치 |
|---|---|
| 저자 v1 layer_ratios (R3·R4·R5) | §2·§3 + 부록 ⭐ |
| 저자 v1 2층·3층 표준 골격 | §7 Step 3·4 |
| Q33 citation·voice gate cross-cutting | §12 + §7 Step 7 (재검증 명시) |

### 9 항목
(a) §1+§2 / (b) §2 / (c) §13 6 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록 ⭐

### Mode 2
- 분량 비율 위반 자동 resize (5% 범위)
- 요소 누락도 *해당 sub 자동 재호출* (저자 묶음 0회)
- 결과 → `_simulations/`

### R1-R5 ⭐ 본 단계 핵심
- R1 quantitative_anchor: 각 layer 본문에 정량 앵커 측정
- R2 chapter_role: chapter 파일 frontmatter chapter_role 정합
- R3 system_loops: 2층 4번 요소 호명 강제
- R4 권위 5층 다층: 권위 분포 분석
- R5 verification_signal: 3층 6번 요소 검증 신호 명시 강제

**End of SPEC: bookwriting-structure-review-master**
