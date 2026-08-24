# SPEC: bookwriting-cross-chapter-relink-master

> 책 전체 *cross-reference·재라우팅·매크로 정합성* 검증. 저자 워크플로우 ⑦ "시스템 재연관화" 직접 구현. 매크로 사이클 자동 발동 시 호출.
>
> 작성일: 2026-05-24
> 매트릭스: 6 sub + 6 AI Agents + 4 Cycle + 4 Gate (Q18)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-cross-chapter-relink-master` |
| 카테고리 | 단계 마스터 (⑪) — Phase 3-B / 매크로 사이클 |
| 저자 11 단계 매트릭스 위치 | ⑪ |
| 저자 진짜 워크플로우 매핑 | (cross-chapter 정합성·매크로) |
| 슬래시 | `/bookwriting-cross-chapter-relink <mode> [target]` |
| 매트릭스 수치 | 6 sub + 6 AI Agents + 4 Cycle + 4 Gate |

---

## 2. Purpose

저자 진짜 워크플로우 *⑦ 시스템 재연관화*를 책 전체 차원으로 구현. 매 사이클은 *챕터 한 단위*에 집중하지만, ⑪은 *책 전체*가 *정합한 흐름·재라우팅·cross-reference*를 유지하도록 *주기적으로* 검증.

**5 책임:**
1. **Cross-chapter 정합** — 챕터 간 *모순·중복·약한 연결* 발견
2. **Cross-reference 추가** — 시드의 secondary 챕터 매핑 발견
3. **시드 재라우팅** — primary 챕터가 잘못된 시드 자동 재배치 권장
4. **시스템 루프 책 전체 정합** — L1-L7 루프가 챕터 간 일관성 유지
5. **forecast-registry 책 전체 정합** — 예측·근거의 챕터 간 일관성

---

## 3. Philosophy

**저자 v1 호환:**
- chapter-pipeline.md의 *매주 정기 점검* (weekly coherence check)을 *시스템화*
- book-forecast-coherence skill의 *책 전체 정합성* 그대로 흡수

**매크로 사이클 자동 발동:**
- book-config의 micro_count_for_relink (기본 5) 도달 시 자동 권장
- 저자 명시 `/bookwriting cross-chapter-relink` 호출도 가능

---

## 4. Scope

### In scope
- ✅ 모든 챕터 (또는 명시 챕터 집합) 검토
- ✅ 챕터 간 모순·중복 발견
- ✅ 시드 cross-reference 추가 제안
- ✅ 시드 재라우팅 권장 (primary 변경)
- ✅ 시스템 루프 L1-L7 책 전체 정합
- ✅ forecast-registry 정합 검증

### Out of scope
- ❌ 단일 챕터 작업 (다른 단계 마스터 담당)
- ❌ 본문 작성 (⑦ content-expand)
- ❌ 구조 분량 (⑨ structure-review)

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-cross-chapter-relink cycle` | 책 전체 풀 사이클 |
| `/bookwriting-cross-chapter-relink cycle ch01..ch03` | 일부 챕터만 |
| `/bookwriting-cross-chapter-relink conflict-detect` | 모순만 |
| `/bookwriting-cross-chapter-relink reroute-suggest` | 재라우팅만 |
| `/bookwriting-cross-chapter-relink loop-coherence` | 시스템 루프 정합 |

---

## 6. Invocation

```bash
/bookwriting-cross-chapter-relink cycle               # 책 전체
/bookwriting-cross-chapter-relink cycle ch01..ch03    # 일부
/bookwriting-cross-chapter-relink conflict-detect     # 모순만
```

---

## 7. Behavior (요약)

```
Step 1: 모든 챕터 evidence-track·seed-track 로드
Step 2: 챕터 간 시드·통찰·근거 cross-check (Cross-Checker 페르소나)
Step 3: 모순 발견 (Conflict Detector — ②와 다른 차원, 챕터 간)
Step 4: Cross-reference 추가 후보 (Cross-Ref Suggester)
Step 5: 재라우팅 권장 (Reroute Recommender)
  - 시드의 primary 챕터가 잘못 매핑된 경우
Step 6: 시스템 루프 책 전체 정합 (Loop Coherence Checker)
  - L1-L7 루프 변수가 챕터 간 일관성 유지
Step 7: forecast-registry 정합 (Registry Coherence Validator)
Step 8: 저자 묶음 (모드 1)
  - 모순 처리
  - cross-ref 채택
  - 재라우팅 채택
  - 루프 정합 보강
Step 9: 갱신
  - seed-registry routing 변경
  - chapter seed-track·evidence-track 갱신
  - forecast-registry 정합
```

---

## 8. Input Schema

```typescript
{
  mode: "cycle" | "conflict-detect" | "reroute-suggest" | "loop-coherence"
  target?: string         // ch-NNN..ch-NNN 또는 생략 = 전체
  options: {
    min_conflict_severity?: "low" | "medium" | "high"
  }
}
```

---

## 9. Output Schema

```markdown
# ⑪ cross-chapter-relink — 책 전체

## 챕터 간 모순 (2건)
- ch01·ch08: "자율주행 점유율" 수치 충돌 (30% vs 25%)
- ch03·ch09: "한계비용 제로" 시점 충돌 (2030 vs 2035)

## Cross-reference 추가 (5건)
- S-001 (메타도구) → ch08·ch10 추가 매핑 권장
- S-024 (UBI 지능) → ch07 추가 매핑 권장

## 재라우팅 권장 (1건)
- S-042 (기술적 사춘기): primary ch01 → ch00-prologue (서장) 변경 권장

## 시스템 루프 정합
- L1 변수 1 (인지 외주화): ch01·ch08에 매핑됨, 일관성 OK
- L7 변수 3 (가소성 손실): ch08만 매핑, ch10 보강 권장

저자: "1=a / 2=a,b,c,d,e / 3=skip" 형식
```

---

## 10. Deliverable Quality

### 정량 기준
- 모순 검출 정확도 80%+
- cross-ref 추가 정확도 75%+
- 재라우팅 권장 정확도 85%+
- 시스템 루프 정합률 90%+

### 정성 기준
- 저자 책 *책 전체 단위 일관성* 유지
- chapter 간 *상호 보강·횡단 연결* 풍부
- forecast-registry 정합 100%

---

## 11. Dependencies

### 필수
- 모든 챕터의 evidence-track·seed-track
- forecast-registry (book 전체)
- seed-registry
- system_loops 정의

### 후속
- 저자 검토 후 다음 사이클로 진행

---

## 12. Guards

### Voice·Citation gate cross-cutting
### Conflict Severity Gate
- High 모순 발견 시 *반드시* 저자 묶음
### Reroute Confidence Gate
- 재라우팅 권장 confidence < 0.7 → 저자 묶음

---

## 13. AI Agents Personas (6명)

1. Cross-Checker — 챕터 간 시드·근거·통찰 비교
2. Conflict Detector — 모순 검출 (수치·시점·논리)
3. Cross-Ref Suggester — cross-reference 추가 후보
4. Reroute Recommender — 시드 primary 챕터 재라우팅
5. Loop Coherence Checker — L1-L7 책 전체 일관성
6. Registry Coherence Validator — forecast-registry 정합

---

## 14. Cycle (C1-C4)

| Cycle | 트리거 | 작동 |
|---|---|---|
| C1: Full Book Relink | `cycle` (인자 없음) | 책 전체 |
| C2: Partial Chapters | `cycle ch01..ch03` | 일부 챕터 |
| C3: Conflict Only | `conflict-detect` | 모순만 |
| C4: Loop Coherence | `loop-coherence` | 시스템 루프 정합만 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| G1: Input | 최소 2 챕터의 evidence-track 존재 |
| G2: Conflict Detection | 모든 High 모순 저자 결정 완료 |
| G3: Reroute Coherence | 재라우팅 후 seed-registry 정합 |
| G4: Loop Coherence | 시스템 루프 매핑률 90%+ |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| 챕터 evidence-track 부족 | warning + 해당 챕터 ④ 재호출 권장 |
| 모순 다수 (10+) | 저자 일괄 묶음 |
| forecast-registry 정합 실패 | 저자 알림 + 수동 점검 권장 |

---

## 17. Verification Examples

1. 책 전체 사이클: 모순 2건·cross-ref 5건·재라우팅 1건·시스템 루프 정합 92%
2. 저자 응답 후 모든 갱신 정합 ✅
3. forecast-registry 정합 100%
4. seed-registry 재라우팅 적용
5. cycle-registry outputs.cross_chapter_relink_results 갱신

---

---

## 부록: 결정론·grill-me·9 항목·Mode 2·R1-R5

### 결정론 모듈
- M12 forecast_registry_syncer ⭐ (R1-R5 책 전체 정합)
- M3 AuthorityGrader (cross-chapter 권위 균형)
- M11 lifecycle_state_machine (시드 재라우팅 lifecycle 영향 검증)
- 자체 결정론: 챕터 간 fact·시드 N×N 비교 (정규식·키워드 빈도)
- 자체 결정론: 시스템 루프 L1-L7 cross-chapter 매핑 (graph 정합)
- 자체 결정론: 재라우팅 confidence 점수 (relevance·권위·매핑 종합)

**LLM 허용**: 모순 *의미 해석* (단, 저자 v1 chapter-pipeline R 규칙 정합 강제)

### grill-me D# 매핑
| D# | §위치 |
|---|---|
| 저자 ⑦ 시스템 재연관화 | §2·§3 ⭐ |
| 매크로 사이클 자동 발동 (DE-1) | §2 + book-config cycle_triggers |
| 저자 v1 매주 정기 점검 | §3 + book-forecast-coherence skill 흡수 |
| Q33 cross-cutting | §12 |

### 9 항목
(a) §1+§2 / (b) §2 (책 전체 정합성) / (c) §13 6 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록

### Mode 2
- 책 전체 사이클이 *모드 2 사용 안 함* — cross-chapter는 정합성 책임이라 정밀 검증 필수
- 단, *partial cross-check* (단순 모순 감지)는 모드 2 허용

### R1-R5 책 전체 검증 ⭐
- R1 quantitative_anchor cross-chapter 정합
- R2 chapter_role cross-chapter 정합
- R3 system_loops L1-L7 일관성
- R4 권위 분포 챕터 간 균형
- R5 verification_signal 챕터 간 중복·일관

**End of SPEC: bookwriting-cross-chapter-relink-master**
