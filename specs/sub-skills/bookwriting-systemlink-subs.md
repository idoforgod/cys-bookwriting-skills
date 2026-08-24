# SPEC: bookwriting-systemlink sub-skills (6개)

> ③ systemlink-master의 6 sub-skill. 마스터: `../bookwriting-systemlink-master.md`

---

## SUB 1: bookwriting-systemlink-asset-searcher

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: search_paths grep·glob으로 시드 관련 자산 발견.

**3. Scope**
- In: search_paths 검색·relevance 점수
- Out: 자산 연결 (Asset Linker)

**4. Behavior**:
```
Step 1: 시드 keyword·시그니처 어휘 추출
Step 2: search_paths 순회 ($BOOK_ROOT·등록 자료 폴더·Obsidian 제외)
Step 3: grep·glob으로 자료 발견
Step 4: relevance 점수 (키워드 빈도·맥락 일치)
Step 5: ≥ 0.7 자료만 채택
```

**5. Input·Output**: In = 시드 / Out = 자산 풀 + relevance + source_file

**6. Dependencies**: ① absorb 통과

**7. Verification**: search_paths 외 검색 0건·relevance ≥0.7 정확도 80%+

---

## SUB 2: bookwriting-systemlink-obsidian-vault-searcher

**1. Identity**: 부모=master. INTERNAL. ⭐ Obsidian 전용 정밀 검색.

**2. Purpose**: 저자 Obsidian vault (reference-vault) 정밀 검색. 저자 *기존 사고 풀*과 연결.

**3. Scope**
- In: Obsidian vault grep·glob·wikilinks 추적
- Out: 일반 Asset Searcher와 통합

**4. Behavior**:
```
Step 1: Obsidian vault 진입
Step 2: vault 구조 인식 (.md 파일·wikilinks·tags)
Step 3: 시드 keyword 검색
Step 4: wikilinks 그래프 추적 (관련 노트 발견)
Step 5: 저자 *기존 사고 패턴* 발견 시 강조
```

**5. Input·Output**: In = 시드 / Out = Obsidian 자산 풀 + wikilinks 그래프

**6. Dependencies**: book-config search_paths에 Obsidian 등록 + vault 접근 권한

**7. Verification**: vault 다수 파일 중 평균 5-15 발견·wikilinks 추적 정확

---

## SUB 3: bookwriting-systemlink-asset-linker

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: seed-registry connections.linked_assets 갱신·citation 필드 자동 채움.

**3. Scope**
- In: 발견 자산을 seed-registry에 연결·citation 메타 추출
- Out: cross-seed linker (다음 sub)

**4. Behavior**:
```
Step 1: 발견 자산별 seed 연결 결정
Step 2: seed-registry linked_assets에 추가
Step 3: 각 자산의 citation 메타데이터 자동 추출:
  - source_file·author·date·publication
Step 4: citation-authority-db로 권위 등급 매핑
Step 5: citation_gate_verified 표시
```

**5. Input·Output**: In = 자산 풀 / Out = seed-registry connections 갱신

**6. Dependencies**: Asset Searcher 또는 Obsidian Vault Searcher 통과

**7. Verification**: linked_assets 정합·citation 필드 100% 추출·권위 등급 매핑

---

## SUB 4: bookwriting-systemlink-cross-seed-linker

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 시드 간 cross-reference 발견·relation_type 매핑.

**3. Scope**
- In: 시드 간 의미·논리 연결 발견
- Out: 시스템 루프 매핑 (다음 sub)

**4. Behavior**:
```
Step 1: 모든 시드 N×N 비교
Step 2: 의미 유사도·논리 연결 평가
Step 3: relation_type 매핑:
  - extends (확장)
  - contrasts (대비)
  - examples (예시)
  - depends_on (의존)
  - pairs_with (짝)
Step 4: seed-registry linked_seeds 갱신
```

**5. Input·Output**: In = 시드 풀 / Out = linked_seeds 그래프

**6. Dependencies**: Asset Linker 통과

**7. Verification**: 시드 간 관계 정확도 80%+·relation_type 올바른 매핑

---

## SUB 5: bookwriting-systemlink-system-loop-mapper

**1. Identity**: 부모=master. INTERNAL. 저자 v1 시스템 사고 핵심.

**2. Purpose**: 저자 v1 L1-L7 시스템 루프와 시드·자산 매핑.

**3. Scope**
- In: 시드·자산을 L1-L7 중 1개 이상 매핑
- Out: 빈 고리 검출 (Gap Detector)

**4. Behavior**:
```
Step 1: forecast-registry의 system_loops 정의 로드:
  - L1 지능대체나선·L2 정치내파·L3 봉건제 풍요·L4 인구 비용·L5 도덕 비용·L6 우주척도·L7 의미위기
Step 2: 시드별 시스템 루프 매핑 (변수·피드백 명시)
Step 3: 자산별 시스템 루프 매핑
Step 4: skeleton.md §2 시스템 사고 척추와 정합
Step 5: 매핑률 80%+ 확인
```

**5. Input·Output**: In = 시드·자산 풀 / Out = system_loops 매핑 그래프

**6. Dependencies**: Cross-Seed Linker 통과

**7. Verification**: L1-L7 매핑률 80%+·변수·피드백 명시·skeleton §2 정합

---

## SUB 6: bookwriting-systemlink-gap-detector

**1. Identity**: 부모=master. INTERNAL. ⭐ 빈 고리 검출 핵심.

**2. Purpose**: 시스템 그래프에서 *연결 누락 후보* 검출. 저자 진짜 워크플로우 4단계 *빈 고리 채우기*의 글쓰기 차원.

**3. Scope**
- In: 시스템 그래프 분석·빈 고리 후보 검출
- Out: 저자 묶음 escalate

**4. Behavior**:
```
Step 1: 시스템 루프 그래프 분석
Step 2: 빈 고리 패턴 검출:
  - 변수 호명됐는데 피드백 누락
  - 시나리오 분기 정의됐는데 정치 변수 미명시
  - 시스템 루프 정의됐는데 evidence 없음
Step 3: 저자 묶음:
  - (a) 새 시드 추가
  - (b) 외부 foresight manual 호출
  - (c) 현재 자산 재검색
  - (d) defer
Step 4: cycle-registry pending_decisions 등록
```

**5. Input·Output**: In = 시스템 그래프 / Out = 빈 고리 목록 + 저자 묶음

**6. Dependencies**: System Loop Mapper 통과

**7. Verification**: 빈 고리 검출 정확도 75%+ (false positive 허용)·저자 묶음 정합

---

**End: systemlink 6 sub**
