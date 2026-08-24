# SPEC: bookwriting-cross-chapter-relink sub-skills (6개)

> ⑪ cross-chapter-relink-master의 6 sub-skill. 마스터: `../bookwriting-cross-chapter-relink-master.md`

---

## SUB 1: bookwriting-cross-chapter-relink-cross-checker

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 챕터 간 시드·통찰·근거 비교.

**3. Behavior**: 모든 챕터의 seed-track·evidence-track 로드·N×N 비교·시드·근거 중복 검출·시드 cross-chapter 풀 구축.

**4. Input·Output**: In = 모든 챕터 / Out = cross-chapter 그래프

**5. Verification**: 중복·연결 정확도 80%+·그래프 정합

---

## SUB 2: bookwriting-cross-chapter-relink-conflict-detector

**1. Identity**: 부모=master. INTERNAL. ⭐ ②와 다른 차원 — 챕터 간 모순.

**2. Purpose**: 챕터 간 모순 (수치·시점·논리) 검출.

**3. Behavior**:
```
- 수치 모순: "ch01 30% vs ch08 25%"
- 시점 모순: "ch03 2030 vs ch09 2035"
- 논리 모순: "ch02 X→Y vs ch07 X→Z"
severity 평가 + 저자 묶음
```

**4. Input·Output**: In = cross-chapter 그래프 / Out = 모순 목록 + 저자 묶음

**5. Verification**: 모순 검출 정확도 80%+·저자 결정 강제

---

## SUB 3: bookwriting-cross-chapter-relink-cross-ref-suggester

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 시드의 secondary 챕터 매핑 후보 발견.

**3. Behavior**: 각 시드의 *다른 챕터 관련성* 평가·confidence 점수·cross_reference 추가 후보 제시.

**4. Input·Output**: In = 시드 cross-chapter 풀 / Out = cross-ref 후보 목록

**5. Verification**: cross-ref 후보 정확도 75%+

---

## SUB 4: bookwriting-cross-chapter-relink-reroute-recommender

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 시드의 primary 챕터 재라우팅 권장.

**3. Behavior**:
```
Step 1: 각 시드의 *원래 primary*와 *실제 cross-chapter 관련성* 비교
Step 2: primary 챕터보다 *다른 챕터 관련성*이 더 높으면 재라우팅 권장
Step 3: confidence < 0.7 → 저자 묶음 강제
Step 4: confidence ≥ 0.7 → 저자 묶음에 ★ 추천
```

**4. Input·Output**: In = 시드 + cross-chapter 관련성 / Out = 재라우팅 권장 목록

**5. Verification**: 재라우팅 정확도 85%+·confidence < 0.7 저자 묶음 강제

---

## SUB 5: bookwriting-cross-chapter-relink-loop-coherence-checker

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 저자 v1 L1-L7 시스템 루프 *책 전체 정합* 검증.

**3. Behavior**:
```
Step 1: 모든 챕터의 system_loops 매핑 로드
Step 2: 같은 루프 변수가 챕터 간 *일관성 유지*하는지 검증
Step 3: 변수 누락·정의 모순 발견 시 저자 묶음
Step 4: 매핑률 90%+ 목표
```

**4. Input·Output**: In = 모든 챕터 system_loops / Out = 루프 정합 결과

**5. Verification**: L1-L7 일관성 90%+·변수 모순 검출

---

## SUB 6: bookwriting-cross-chapter-relink-registry-coherence-validator

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: forecast-registry 책 전체 정합 검증 (R1-R5 모두).

**3. Behavior**:
```
저자 v1 chapter-pipeline R1-R5 규칙:
R1: quantitative_anchor 정합
R2: chapter_role 정합
R3: system_loops 호명 정합
R4: 권위 5층 다층 인용
R5: verification_signal 명시
모든 규칙 책 전체 단위 검증
```

**4. Input·Output**: In = forecast-registry + 모든 챕터 evidence-track / Out = 정합 보고

**5. Verification**: R1-R5 모두 검증·저자 v1 chapter-pipeline 호환

---

**End: cross-chapter-relink 6 sub**
