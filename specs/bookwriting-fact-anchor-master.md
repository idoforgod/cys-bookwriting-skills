# SPEC: bookwriting-fact-anchor-master

> 흡수된 fact·score의 *정합성·중복·충돌* 검증. 저자 v1 forecast-registry.yaml의 quantitative_anchor와 cross-check.
>
> 작성일: 2026-05-24
> 매트릭스: 5 sub + 5 AI Agents + 4 Cycle + 4 Gate (Q18)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-fact-anchor-master` |
| 카테고리 | 단계 마스터 (②, MVP 수직 슬라이스 포함) |
| 저자 11 단계 매트릭스 위치 | ② |
| 저자 진짜 워크플로우 매핑 | **2단계 — Fact + Score 정합 (글쓰기 차원)** |
| 슬래시 | `/bookwriting-fact-anchor <mode> [target]` |
| 매트릭스 수치 | 5 sub + 5 AI Agents + 4 Cycle + 4 Gate |

---

## 2. Purpose

흡수된 fact·통계·정량 표현이 *서로 모순되지 않는지* 검증한다. 저자 v1 forecast-registry.yaml의 *quantitative_anchor*와 *cross-check*하여 *책 전체 정량 일관성*을 보장한다.

**4 책임:**
1. **fact 추출** — 흡수 자료에서 fact·통계·정량 표현 자동 추출
2. **중복 검출** — 같은 fact가 여러 출처에서 등장 시 *권위 비교*
3. **충돌 검출** — 서로 모순되는 fact (예: "100배" vs "50배")
4. **forecast-registry sync** — v1 호환 정합성 보장

---

## 3. Philosophy

**v1 chapter-pipeline.md의 *fact 정합성 규칙* 직접 호환:**
- R1: quantitative_anchor 정합
- R5: verification_signal 명시

**Citation Gate가 *가장 엄격* 적용되는 두 번째 단계** (④ evidence-collect 다음):
- 모든 fact에 *출처 권위 등급* 강제
- 출처 누락 fact → Critical 차단

---

## 4. Scope

### In scope
- ✅ 흡수 자산의 fact·통계·정량 표현 자동 추출
- ✅ 같은 fact 중복 검출 + 권위 등급 비교
- ✅ 충돌 fact 검출 + 저자 묶음 escalate
- ✅ forecast-registry quantitative_anchor 갱신·정합 검증
- ✅ seed-registry connections.linked_predictions 갱신

### Out of scope
- ❌ fact의 *내용 진위 검증* (저자 책임 — 흡수 결정 시점에)
- ❌ fact의 *외부 web 재검색* (옵션 A+)
- ❌ 인용 표현 작성 (⑦ content-expand 담당)

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-fact-anchor cycle <target>` | 풀 사이클 |
| `/bookwriting-fact-anchor extract <target>` | fact 추출만 |
| `/bookwriting-fact-anchor conflict-detect <target>` | 충돌만 검출 |
| `/bookwriting-fact-anchor sync-registry` | forecast-registry 동기화만 |

---

## 6. Invocation

```bash
/bookwriting-fact-anchor cycle ch01-economy
/bookwriting-fact-anchor extract S-001
/bookwriting-fact-anchor conflict-detect ch01-economy
/bookwriting-fact-anchor sync-registry
```

---

## 7. Behavior

**9단계 행동 시나리오:**

```
호출: /bookwriting-fact-anchor cycle ch01-economy

【Step 1: 입력 검증·자료 로드】
  - ch01 라우팅 시드 (LINKED·EXPANDED) 추출
  - seed-registry.connections.linked_assets 자산 경로
  - forecast-registry.yaml 기존 P-NNN
  - inbox 미처리 자산도 포함

【Step 2: Fact 추출 (Fact Extractor 페르소나)】
  - 정규식·NLP로 fact·통계·정량 표현 추출
  - 저자 fact 패턴: "X% / Y배 / Z명 / N년"
  - 각 fact에 임시 ID F-NNN 발급
  - source_file 명시

【Step 3: Citation Gate (Critical 적용)】
  - 각 fact의 source_file 실재 검증
  - 메타데이터 완전성
  - 형식 모호 ("한 보고서에 따르면") → Critical 차단

【Step 4: 중복 검출 (Duplicate Detector 페르소나)】
  - 같은 fact가 여러 출처에서 등장
  - 권위 등급 비교 → 가장 권위 높은 출처 *primary*
  - 다른 출처는 *secondary cross-reference*

【Step 5: 충돌 검출 (Conflict Detector 페르소나)】
  - 서로 모순되는 fact 자동 검출
  - 예: "산업혁명 100배 (Musk)" vs "산업혁명 50배 (다른 출처)"
  - 충돌 발견 시 저자 묶음 escalate

【Step 6: forecast-registry sync (Registry Syncer 페르소나)】
  - 신규 fact 발견 시 forecast-registry에 P-NNN 신규 등록
  - 기존 P-NNN과 매칭 시 evidence 추가
  - quantitative_anchor 필드 갱신

【Step 7: seed-registry 갱신 (Seed Linker 페르소나)】
  - 시드의 connections.linked_predictions에 P-NNN 추가
  - citation_authority_grade 매핑

【Step 8: 저자 묶음 (모드 1)】
  - 충돌 fact 처리 묶음
  - 중복 fact의 primary 선택
  - 저자가 결정

【Step 9: 결과 출력 + 정합 보고】
  - cycle-registry.outputs 갱신
  - 정합성 보고: "fact 23개 / 충돌 1건 / 중복 4건 / forecast-registry +3 P-NNN"
```

---

## 8. Input Schema

```typescript
{
  mode: "cycle" | "extract" | "conflict-detect" | "sync-registry"
  target?: string
  options: {
    strict?: boolean        // strict 모드 시 Medium도 차단
  }
}
```

---

## 9. Output Schema

### 저자 화면
```markdown
# ② fact-anchor — ch01-economy

## Fact 추출 (23개)
- F-001 "100배 스케일" (Musk 2024, Amodei 2024 — Grade A 다층)
- F-002 "90% 확신 (1-3년)" (Amodei 2024 — Grade A)
- F-003 "한국 자율주행 점유율 30% (2030)" (충돌 의심)
- ...

## 중복 (4건) — primary 자동 선택
- "100배 스케일" → primary: Musk · Amodei 공동
- ...

## 충돌 (1건) ⚠️
**F-003**: "한국 자율주행 점유율 30%"
- 출처 A: 저자 칼럼 2024 "30%" (Grade B)
- 출처 B: inbox 자료 "25%" (Grade C)
- 저자 옵션:
  - (a) ★ Grade B 출처 채택 (30%)
  - (b) 저자 직접 검증
  - (c) 양쪽 모두 명시
  - (d) defer

저자: "1=a"

## forecast-registry sync
- 신규 P-NNN: 3건
- 기존 P-NNN evidence 추가: 8건
- quantitative_anchor 갱신: 5건
```

### 파일 갱신
- `forecast-registry.yaml`
- `seed-registry.yaml` (linked_predictions)
- `chapters/<ch>/evidence-track.yaml` (예비)

---

## 10. Deliverable Quality

### 정량 기준
- fact 추출 정확도: 90%+
- 중복 검출 정확도: 95%+
- 충돌 검출 정확도: 85%+ (false positive 허용 — 저자 확인)
- citation-gate Critical 0건 (위반 시 차단)
- forecast-registry sync 정합: 100%

### 정성 기준
- 저자 책 *정량 일관성* 보장 (어느 챕터든 같은 fact는 같은 수치)
- 권위 5층 매핑 *정확한 등급화*
- 충돌 발견 시 *저자 판단 명확 제시*

---

## 11. Dependencies

### 필수
- ① absorb 통과 (흡수 자산 등록)
- seed-registry / forecast-registry / chapter evidence-track
- citation-authority-db

### 후속
- ③ systemlink (시스템 연결 시 fact 활용)
- ④ evidence-collect (정밀 근거 수집)

---

## 12. Guards

### Citation Gate Critical 적용
- 모든 fact의 source_file 실재 강제
- 형식 모호 자동 차단

### Conflict Detection 가드
- 충돌 발견 시 *반드시* 저자 묶음 escalate (자동 결정 안 함)

### Registry Sync 가드
- forecast-registry 갱신 시 *기존 P-NNN과 일관성 검증*
- 충돌 시 저자 묶음

---

## 13. AI Agents Personas (5명)

| # | 페르소나 | 역할 |
|---|---|---|
| 1 | **Fact Extractor** | 정규식·NLP로 fact 추출 |
| 2 | **Duplicate Detector** | 중복 fact 검출·권위 비교 |
| 3 | **Conflict Detector ⭐** | 모순 fact 검출 |
| 4 | **Registry Syncer** | forecast-registry 갱신·정합 |
| 5 | **Seed Linker** | seed-registry linked_predictions 갱신 |

---

## 14. Cycle

| Cycle | 트리거 | 작동 |
|---|---|---|
| **C1: Chapter Fact** | `cycle ch-NNN` | 챕터 전체 fact 정합 |
| **C2: Seed Fact** | `cycle S-NNN` | 단일 시드 |
| **C3: Conflict Only** | `conflict-detect` | 충돌만 |
| **C4: Registry Sync** | `sync-registry` | forecast-registry만 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| **G1: Input** | LINKED 이상 시드 ≥1개 |
| **G2: Citation Gate** | source_file 실재 100% |
| **G3: Conflict Handling** | 충돌 발견 시 저자 결정 완료 |
| **G4: Registry Sync** | forecast-registry 정합 |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| fact 0개 추출 | warning + ① absorb 재확인 권장 |
| Citation Critical 다수 | 저자 묶음 escalate |
| 충돌 다수 (5건+) | 저자 일괄 묶음 |
| forecast-registry 손상 | 백업 복원 + 저자 알림 |

---

## 17. Verification Examples

### 검증 1: 챕터 fact 정합
```bash
/bookwriting-fact-anchor cycle ch01-economy
✅ 23 fact 추출
✅ 중복 4건 — primary 자동 선택
✅ 충돌 1건 → 저자 묶음
✅ forecast-registry +3 P-NNN
✅ seed linked_predictions 갱신
```

### 검증 2: 충돌 검출·저자 결정
```bash
# 충돌: "30% vs 25%"
✅ 저자 묶음 escalate
✅ 저자 응답: "1=a" (Grade B 출처 채택)
✅ Grade C 출처는 *cross-reference 보관*
```

### 검증 3: forecast-registry sync
```bash
/bookwriting-fact-anchor sync-registry
✅ 신규 P-NNN 3건 등록
✅ 기존 P-NNN evidence 8건 추가
✅ quantitative_anchor 5건 갱신
✅ v1 R1 정합 통과
```

### 검증 4: Citation Critical 차단
```bash
# fact "한 보고서에 따르면 80%"
❌ 형식 모호 신호 2 + 메타데이터 누락 신호 3
✅ Citation Gate Critical 차단
✅ 저자 묶음 escalate
```

### 검증 5: 중복 fact primary 선택
```bash
# fact "100배 스케일" → Musk·Amodei·Hassabis 3 출처
✅ 모두 Grade A
✅ primary 자동 선택: 가장 먼저 발언한 Musk
✅ Amodei·Hassabis는 cross-reference (수렴의 놀라움 — 시그니처 패턴 활용 가능)
```

---

---

## 부록: 결정론·grill-me·9 항목·Mode 2·R1-R5

### 결정론 모듈
- M10 fact_extractor (정규식 추출·중복 검출)
- M3 AuthorityGrader (권위 등급)
- M12 forecast_registry_syncer (R1-R5 검증)
- M13 r4_multi_layer_verifier
- M2 HallucinationDetector (Critical 차단)

**LLM 허용 영역**: 모순 *원인 해석* (왜 모순인지) — 결정론 환원 불가, 단 출처 인용 강제

### grill-me D# 매핑
| D# | §위치 |
|---|---|
| D8 (seed-registry linked_predictions) | §7 Step 7 + 부록 결정론 |
| D9 (forecast-registry sync) | §7 Step 6 |
| R1 quantitative_anchor v1 규칙 | §3 + §7 + 부록 결정론 |
| Q33 (citation Critical 적용) | §12 ⭐ |

### 9 항목
(a) §1+§2 / (b) §2 / (c) §13 5 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록

### Mode 2 자동
- 충돌 자동 *처리* (★ 추천 = 높은 권위 자동 채택) — 저자 묶음 0회
- 결과 → `_simulations/`

### R1-R5
- R1 quantitative_anchor ⭐ 핵심 — 모든 정량 표현 정합 검증
- R2-R5: 후속 단계 (③·④·⑤)와 협업

**End of SPEC: bookwriting-fact-anchor-master**

> ② fact-anchor는 저자 책의 *정량 일관성·정합성* backbone. forecast-registry v1과 동기화하여 *책 전체 단위 일관성* 보장.
