# SPEC: bookwriting-evidence-link sub-skills (7개)

> ⑤ evidence-link-master의 7 sub-skill. 마스터: `../bookwriting-evidence-link-master.md`

---

## SUB 1: bookwriting-evidence-link-graph-builder

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: evidence 그래프 노드 구축. 각 evidence를 노드로 변환·meta 부여.

**3. Behavior**: ④ evidence-track의 evidence를 노드로 변환·source·grade·timestamp meta 부여·노드 ID 발급.

**4. Input·Output**: In = evidence-track / Out = 노드 풀 + meta

**5. Verification**: 모든 evidence 노드 변환·meta 완전성

---

## SUB 2: bookwriting-evidence-link-edge-detector

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: evidence 노드 간 엣지 발견 (논리·시간·인과).

**3. Behavior**:
```
- 논리: A 주장 → B 결론 (causal·implication)
- 시간: 1990 사건 → 2024 결과 (temporal)
- 인과: 원인 evidence → 결과 evidence (causation)
- 엣지에 weight·confidence 부여
```

**4. Input·Output**: In = 노드 풀 / Out = 엣지 풀 (label·weight)

**5. Verification**: 엣지 검출 정확도 75%+·각 엣지 label 명확

---

## SUB 3: bookwriting-evidence-link-authority-mapper

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 모든 노드를 권위 5층 (Grade A-E) 매핑.

**3. Behavior**: citation-authority-db 매칭·각 노드 grade 부여·매칭 안 되는 노드는 임시 Grade C + DB 보강 권장.

**4. Input·Output**: In = 노드 풀 / Out = 등급화 노드

**5. Verification**: 100% 등급 부여·매칭 안 되는 노드 로그

---

## SUB 4: bookwriting-evidence-link-r4-verifier

**1. Identity**: 부모=master. INTERNAL. ⭐ R4 다층 강제 핵심.

**2. Purpose**: 저자 v1 R4 — 같은 주장에 최소 2층 권위 매핑 강제.

**3. Behavior**:
```
Step 1: 그래프에서 *주장 단위* 식별 (관련 evidence들의 합)
Step 2: 각 주장의 권위층 수 카운트
Step 3: 단일 권위만 → 저자 묶음 escalate
  - (a) 다른 권위층 evidence 추가 (외부 manual 호출)
  - (b) 주장을 *Layer 1만으로 유지* (R4 위반 인지)
  - (c) 주장을 풀에서 제외
  - (d) defer
```

**4. Input·Output**: In = 등급화 그래프 / Out = R4 검증 결과 + 저자 묶음

**5. Verification**: 모든 주장 R4 검증·통과율 85%+

---

## SUB 5: bookwriting-evidence-link-loop-integrator

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 저자 시스템 루프 L1-L7과 evidence 그래프 통합.

**3. Behavior**: 각 노드/엣지를 L1-L7 중 1개 이상에 매핑·forecast-registry system_loops와 정합.

**4. Input·Output**: In = R4 검증된 그래프 / Out = 루프 통합 그래프

**5. Verification**: L1-L7 매핑률 80%+·forecast-registry 정합

---

## SUB 6: bookwriting-evidence-link-isolation-detector

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 고립 노드·약한 연결 발견.

**3. Behavior**:
```
Step 1: degree 0 노드 (고립) 발견
Step 2: degree 1 노드 (약한 연결) 발견
Step 3: 저자 묶음:
  - (a) evidence 풀에서 제외
  - (b) 연결 추가 시도
  - (c) 미해결로 보관
```

**4. Input·Output**: In = 그래프 / Out = 고립·약한 노드 목록

**5. Verification**: 고립 노드 100% 검출·약한 연결 검출

---

## SUB 7: bookwriting-evidence-link-graph-visualizer

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 그래프를 markdown 시각화 (table + ascii diagram).

**3. Behavior**: 그래프를 markdown table·간단한 ASCII 시각화·저자 검토 용이한 형식.

**4. Input·Output**: In = 완성 그래프 / Out = markdown 시각화

**5. Verification**: 저자 spot-check 가독성·노드·엣지 정합

---

**End: evidence-link 7 sub**
