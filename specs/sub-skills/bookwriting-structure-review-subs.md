# SPEC: bookwriting-structure-review sub-skills (7개)

> ⑨ structure-review-master의 7 sub-skill. 마스터: `../bookwriting-structure-review-master.md`

---

## SUB 1: bookwriting-structure-review-layer-ratio-measurer

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 1·2·3층 분량 비율 측정. 저자 v1 layer_ratios (10-15% / 60-70% / 15-25%) 검증.

**3. Behavior**:
```
Step 1: wc -w narrative.md / analysis.md / implications.md
Step 2: 총 단어 수 + 각 layer 비율 계산
Step 3: book-config.layer_ratios range 비교
Step 4: 위반 시 severity (low·medium·high)
```

**4. Input·Output**: In = 챕터 3 파일 / Out = 분량 표 + 위반 목록

**5. Verification**: 분량 측정 정확도 99%+·range 검증 정합

---

## SUB 2: bookwriting-structure-review-element-checker-layer2

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 저자 v1 2층 표준 골격 7요소 검출.

**3. Behavior**:
```
요소 검색:
1. 핵심명제 재진술 (1층 명제가 2층 시작에 등장)
2. 약신호 (구체 evidence)
3. 추동력 (시스템적 힘)
4. 시스템 루프 호명 (L1-L7 명시)
5. 시나리오 분기 (정치 변수)
6. 시점 좌표 (AGI 5단계)
7. 횡단 연결 (cross-chapter)
각 요소 발견 시 ✅, 누락 시 ⚠️
```

**4. Input·Output**: In = analysis.md / Out = 7요소 통과·누락 표

**5. Verification**: 7요소 검출 정확도 95%+·누락 시 저자 알림

---

## SUB 3: bookwriting-structure-review-element-checker-layer3

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 저자 v1 3층 표준 골격 6요소 검출.

**3. Behavior**:
```
요소 검색:
1. 본문 의미 한 문장
2. 개인 차원 응답
3. 조직 차원 응답
4. 정책 차원 응답
5. 한국 결정 윈도우 (KW-1·KW-2·KW-3, 해당 시)
6. 검증 신호 (verification_signal, 해당 시)
```

**4. Input·Output**: In = implications.md / Out = 6요소 통과·누락 표

**5. Verification**: 6요소 검출 정확도 95%+

---

## SUB 4: bookwriting-structure-review-flow-validator

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 1·2·3층 흐름 일관성 검증.

**3. Behavior**:
```
Step 1: 1층 끝 핵심 명제 추출
Step 2: 2층 본문이 *그 명제를 입증*하는지 확인
Step 3: 3층 함의가 *2층 분석에서 자연 도출*되는지 확인
Step 4: 흐름 끊김 발견 시 저자 묶음
```

**4. Input·Output**: In = 3 파일 / Out = 흐름 일관성 평가 + 끊김 목록

**5. Verification**: 흐름 평가 80%+·끊김 검출 정확

---

## SUB 5: bookwriting-structure-review-r4-distribution-analyzer

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 챕터 내 권위 5층 분포 분석·균형 검증.

**3. Behavior**:
```
Step 1: chapters/<ch>/evidence-track.yaml 권위 등급 분포 분석
Step 2: Layer 1-5 카운트
Step 3: 어느 한 층 *과편중* 검출 (예: Layer 1만 80%)
Step 4: 저자 R4 권장 (다층 균형)
```

**4. Input·Output**: In = evidence-track / Out = 권위 분포 + 편중 알림

**5. Verification**: 분포 측정 정합·편중 알림 정확

---

## SUB 6: bookwriting-structure-review-r5-verifier

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 저자 v1 R5 — verification_signal·falsifies_if 누락 검출.

**3. Behavior**:
```
Step 1: forecast-registry의 P-NNN 중 *챕터 사용분* 식별
Step 2: 각 P-NNN의 verification_signal·falsifies_if 필드 확인
Step 3: 누락 시 저자 알림 + ④ verification-signal-finder 재호출 권장
```

**4. Input·Output**: In = chapter + forecast-registry / Out = R5 검증 결과

**5. Verification**: 저자 v1 R5 정합·누락 검출

---

## SUB 7: bookwriting-structure-review-resize-recommender

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 분량 미달·초과 시 *자동 조정 권장*.

**3. Behavior**:
```
Step 1: layer ratio 위반 분석
Step 2: 5% 범위 내 → 자동 resize 시도
Step 3: 큰 위반 → 저자 묶음 (확장·축약·재호출)
```

**4. Input·Output**: In = 분량 측정 결과 / Out = resize 시도 또는 저자 묶음

**5. Verification**: 자동 resize 정확도·저자 묶음 명확

---

**End: structure-review 7 sub**
