# SPEC: bookwriting-fact-anchor sub-skills (5개)

> ② fact-anchor-master의 5 sub-skill. 마스터: `../bookwriting-fact-anchor-master.md`

---

## SUB 1: bookwriting-fact-anchor-fact-extractor

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 흡수 자산에서 fact·통계·정량 표현 자동 추출.

**3. Scope**
- In: 정규식·NLP fact 추출·임시 F-NNN ID 발급
- Out: 중복·충돌 검출

**4. Behavior**:
```
Step 1: 자산 텍스트 로드
Step 2: 정규식 매칭:
  - "N%" / "N배" / "N년·연도" / "N명·N달러"
Step 3: 저자 fact 패턴 식별 (100배·90% 확신·2027 임계 등)
Step 4: 각 fact에 source_file·context 명시
Step 5: 임시 F-NNN 발급
```

**5. Input·Output**: In = ① absorb 통과 자산 / Out = fact 풀 (F-NNN, text, source_file, context)

**6. Dependencies**: ① absorb 통과

**7. Verification**: fact 추출 정확도 90%+·정량 패턴 인식·source_file 명시

---

## SUB 2: bookwriting-fact-anchor-duplicate-detector

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 같은 fact가 여러 출처에서 등장 시 권위 비교·primary 선정.

**3. Scope**
- In: 중복 fact 검출·권위 등급 비교·primary 자동 선택
- Out: 충돌 검출 (다른 sub)

**4. Behavior**:
```
Step 1: fact 풀 N×N 비교 (의미 유사도)
Step 2: 중복 fact 그룹화
Step 3: 각 그룹의 권위 등급 비교 (citation-authority-db 활용)
Step 4: 가장 권위 높은 출처 → primary
Step 5: 다른 출처 → secondary cross-reference
```

**5. Input·Output**: In = fact 풀 / Out = 중복 그룹 + primary/secondary 매핑

**6. Dependencies**: Fact Extractor 통과

**7. Verification**: 중복 검출 정확도 95%+·권위 등급 비교 정합·primary 자동 선택

---

## SUB 3: bookwriting-fact-anchor-conflict-detector

**1. Identity**: 부모=master. INTERNAL. ⭐ 모순 검출 핵심.

**2. Purpose**: 서로 모순되는 fact 자동 검출 (수치·시점·논리 충돌).

**3. Scope**
- In: 모순 발견·저자 묶음 escalate
- Out: registry sync (다른 sub)

**4. Behavior**:
```
Step 1: fact 풀에서 *같은 주제* 다른 수치/시점 발견
Step 2: 모순 분류:
  - 수치 충돌: "100배 vs 50배"
  - 시점 충돌: "2030 vs 2035"
  - 논리 충돌: "A→B vs A→C"
Step 3: 모순 severity 평가 (low·medium·high·critical)
Step 4: 저자 묶음 escalate (자동 결정 안 함)
```

**5. Input·Output**: In = 중복 검출된 fact 풀 / Out = 모순 목록 + severity + 저자 묶음

**6. Dependencies**: Duplicate Detector 통과

**7. Verification**: 모순 검출 정확도 85%+ (false positive 허용)·저자 결정 강제

---

## SUB 4: bookwriting-fact-anchor-registry-syncer

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: forecast-registry.yaml의 quantitative_anchor·P-NNN 갱신·정합 검증.

**3. Scope**
- In: 신규 P-NNN 등록·기존 P-NNN evidence 추가·정합 검증
- Out: seed-registry 연결 (다른 sub)

**4. Behavior**:
```
Step 1: 신규 fact 중 *기존 P-NNN에 없는 것* 식별
Step 2: forecast-registry에 신규 P-NNN 등록
Step 3: 기존 P-NNN에 *새 evidence 출처* 추가
Step 4: quantitative_anchor 필드 정합 검증
Step 5: 저자 v1 R1 규칙 준수 확인
```

**5. Input·Output**: In = 모순 처리된 fact 풀 / Out = forecast-registry 갱신

**6. Dependencies**: Conflict Detector 통과 (충돌 해결 후)

**7. Verification**: forecast-registry 정합 100%·R1 규칙 준수·중복 P-NNN 0건

---

## SUB 5: bookwriting-fact-anchor-seed-linker

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: seed-registry의 connections.linked_predictions 갱신·citation_authority_grade 매핑.

**3. Scope**
- In: 시드 → P-NNN 연결·권위 등급 매핑
- Out: ③ systemlink 진입

**4. Behavior**:
```
Step 1: 각 시드의 관련 P-NNN 식별
Step 2: seed-registry.connections.linked_predictions 갱신
Step 3: 각 P-NNN에 권위 등급 매핑
Step 4: 시드 lifecycle SEED → LINKED 진행 권장
```

**5. Input·Output**: In = forecast-registry 갱신 결과 / Out = seed-registry 갱신

**6. Dependencies**: Registry Syncer 통과

**7. Verification**: 시드 linked_predictions 정합·citation_authority_grade 모두 매핑·lifecycle 진행

---

**End: fact-anchor 5 sub**
