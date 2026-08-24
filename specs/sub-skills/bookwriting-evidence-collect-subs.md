# SPEC: bookwriting-evidence-collect sub-skills (4개 핵심)

> ④ evidence-collect-master의 핵심 4 sub-skill.
> 마스터 SPEC: `../bookwriting-evidence-collect-master.md` 참조.
> ⭐ Citation Gate 가장 엄격 적용 단계.

---

## SUB 1: bookwriting-evidence-collect-asset-searcher

### 1. Identity
부모: `bookwriting-evidence-collect-master`. INTERNAL.

### 2. Purpose
저자 search_paths ($BOOK_ROOT·Obsidian vault·등록 자료 폴더) 자산 풀에서 *시드·통찰 관련 근거 자료*를 grep·glob으로 발굴. inbox/ 우선 처리.

### 3. Scope
- **In**: search_paths grep·glob + inbox 우선 + relevance 점수
- **Out**: 등급화 (다른 sub) / 정량 앵커 추출 (다른 sub)

### 4. Behavior
```
Step 1: 시드 keyword + 시그니처 어휘 추출
Step 2: inbox/ 미처리 파일 우선 검색
Step 3: search_paths 전체 grep·glob
Step 4: Obsidian vault (다수 파일) 정밀 검색
Step 5: 각 발견 자료에 relevance 0-1 점수
Step 6: relevance ≥ 0.7 자료만 풀에 채택
```

### 5. Input·Output
- **In**: 시드·통찰·book-config.search_paths
- **Out**: 자료 풀 + relevance + source_file 경로

### 6. Dependencies
- ③ systemlink (자산 연결 정보 활용 가능)

### 7. Verification
1. search_paths 외 검색 0건 (옵션 A+ 가드)
2. inbox 우선 처리 (mtime 기준)
3. Obsidian vault에서 평균 5-10 자료 발견
4. relevance ≥0.7 채택률 60%+

---

## SUB 2: bookwriting-evidence-collect-authority-grader

### 1. Identity
부모: master. INTERNAL. ⭐ Citation Gate 핵심 sub.

### 2. Purpose
asset-searcher가 발견한 자료에 *권위 5층 등급* 부여. citation-authority-db.yaml 매칭. Grade A·B·C·D·E + out (부적합) 분류.

### 3. Scope
- **In**: 자료별 grade 매핑·R4 다층 강제·Grade out 풀에서 제외
- **Out**: 정량 앵커 추출 (다른 sub)

### 4. Behavior
```
Step 1: 자료의 author·publication·source_type 분석
Step 2: citation-authority-db.yaml 매칭 (matching_policy 따라)
Step 3: Grade 부여 (A·B·C·D·E·out)
Step 4: Grade out 자료 풀에서 제외
Step 5: Grade A·B 비율 60%+ 확인 (정성 기준)
Step 6: R4 다층 강제 — 같은 주장에 단일 권위만 매핑 시 *해당 주장 풀에서 제외*
Step 7: 매칭 안 되는 author → 임시 Grade C + DB 보강 권장
```

### 5. Input·Output
- **In**: asset-searcher 자료 풀 / citation-authority-db.yaml
- **Out**: 등급화 자료 + 권위 분포 보고

### 6. Dependencies
- asset-searcher 통과
- citation-authority-db (expert_pool)
- Citation Gate cross-cutting

### 7. Verification
1. 모든 자료에 grade 부여 (out 포함)
2. Grade A·B 비율 60%+
3. Grade out 자료 풀 제외
4. R4 단일 권위 주장 제외
5. citation-authority-learning-log 갱신 (매칭 안 된 author)

---

## SUB 3: bookwriting-evidence-collect-quantitative-anchor-extractor

### 1. Identity
부모: master. INTERNAL. ⭐ 저자 정량 표현 패턴 추출.

### 2. Purpose
저자 책의 *quantitative_anchor* 자동 추출. 저자 정량 표현 패턴 (100배·90% 확신·2027 임계점·5억 명) 정합. forecast-registry.quantitative_anchor 갱신.

### 3. Scope
- **In**: 자료에서 정량 표현 자동 추출·검증 신호 발견
- **Out**: forecast-registry 갱신 (별도 sub)

### 4. Behavior
```
Step 1: 자료 텍스트에서 수치 정규식 매칭:
  - N% / N배 / N년·연도 / N명·N달러 / N% 확신
Step 2: 저자 정량 표현 *시그니처 패턴*과 정합:
  - "100배 스케일" (산업혁명 × 10 × 10)
  - "90% 확신 1-3년" (Amodei)
  - "2027 임계점"
  - "5억 명" (영향 범위)
Step 3: 각 정량 앵커에 source_file·author·grade 명시
Step 4: forecast-registry.quantitative_anchor 갱신 (sync 별도 sub 담당)
Step 5: 출처 미명시 정량 표현 → Citation Gate Critical 차단
```

### 5. Input·Output
- **In**: authority-grader 통과 자료 풀
- **Out**: 정량 앵커 목록 + 출처 매핑

### 6. Dependencies
- authority-grader 통과
- forecast-registry.yaml의 quantitative_anchor 필드

### 7. Verification
1. 정량 앵커 평균 0.6/자료
2. 모든 정량 앵커에 source_file 명시
3. 저자 시그니처 정량 표현 (100배·90% 등) 식별
4. Citation Gate Critical 0건 (정량 앵커에 한해)

---

## SUB 4: bookwriting-evidence-collect-verification-signal-finder

### 1. Identity
부모: master. INTERNAL.

### 2. Purpose
저자 v1 R5 *verification_signal·falsifies_if* 자동 발견. 5년·10년 후 *책의 명제가 검증·반증되는 지표*를 evidence 풀에서 추출.

### 3. Scope
- **In**: evidence에서 검증 신호 자동 발견 + 저자 v1 R5 호환
- **Out**: forecast-registry.verification_signal·falsifies_if 갱신

### 4. Behavior
```
Step 1: evidence 텍스트에서 검증 가능 표현 패턴 매칭:
  - "5년 후 X가 Y에 도달하면" → verification_signal
  - "Z 미발생 시 본 명제 반증" → falsifies_if
  - "2030년까지 N% 도달 예상" → verification 후보
Step 2: 저자 v1 chapter-pipeline.md R5 양식 정합
Step 3: forecast-registry 해당 P-NNN에 추가
Step 4: 저자 검증 가능성 점수 (재인용·재추적 가능성)
```

### 5. Input·Output
- **In**: authority-grader 통과 자료 / forecast-registry
- **Out**: verification_signal·falsifies_if 목록 + 출처 매핑

### 6. Dependencies
- authority-grader 통과

### 7. Verification
1. 검증 신호 3-7건/챕터
2. 저자 v1 R5 양식 정합
3. forecast-registry verification_signal 필드 갱신
4. 저자 책 *5년·10년 후 검증 가능*한 학술 신뢰성 보장

---

---

## SUB 5: bookwriting-evidence-collect-forecast-registry-syncer

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 발굴 evidence를 forecast-registry.yaml에 sync. 신규 P-NNN 등록·기존 P-NNN evidence 추가·중복 검출.

**3. Behavior**:
```
Step 1: authority-grader·quantitative-anchor-extractor 통과 evidence 로드
Step 2: forecast-registry의 기존 P-NNN과 매칭
Step 3: 매칭되면 evidence 추가, 매칭 없으면 P-NNN 신규 등록
Step 4: 중복 P-NNN 검출 → 저자 묶음 (병합·신규·skip)
Step 5: v1 R1 quantitative_anchor 정합 검증
```

**4. Input·Output**: In = 등급화 evidence·정량 앵커 / Out = forecast-registry 갱신

**5. Verification**: forecast-registry 정합·중복 0건·v1 R1 통과

---

## SUB 6: bookwriting-evidence-collect-evidence-quality-filter

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 모든 발굴 evidence 종합 평가·최종 채택·제외 결정.

**3. Behavior**:
```
Step 1: 각 evidence 종합 점수:
  - relevance (시드 관련성)
  - authority_grade (Grade A·B 가산점)
  - R4 적합성 (다층 매핑 가능성)
  - 정량 앵커 수
  - 검증 신호 보유
Step 2: 임계값 통과 evidence → chapter evidence-track에 등록
Step 3: 임계 미달 → 풀에서 제외 + 저자 묶음 (Grade A·B 보강 권장)
```

**4. Input·Output**: In = 모든 발굴 evidence / Out = 채택·제외 분류

**5. Verification**: 채택률 60%+·Grade A·B 비율 60%+·저자 spot-check 정합

---

**End of SUB SPEC: evidence-collect 6 sub**
