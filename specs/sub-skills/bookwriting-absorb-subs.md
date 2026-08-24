# SPEC: bookwriting-absorb sub-skills (4개)

> ① absorb-master의 4 sub-skill. 마스터: `../bookwriting-absorb-master.md`
> 양식: sub-skill 간략 7 항목

---

## SUB 1: bookwriting-absorb-frontmatter-parser

**1. Identity**: 부모=master. INTERNAL. 4 페르소나 중 Frontmatter Parser.

**2. Purpose**: yaml frontmatter 파싱·필수 메타 추출 (type·source·to·link·created).

**3. Scope**
- In: frontmatter 정규 파싱·필수 필드 추출
- Out: 본문 분석 (다음 sub)

**4. Behavior**:
```
Step 1: 파일 head 파싱 (--- 사이 yaml)
Step 2: type·source·to·link·created 필드 추출
Step 3: 누락 필드 식별 → Type Classifier에게 전달
Step 4: 형식 오류 시 warning + skip
```

**5. Input·Output**: In = inbox/*.md / Out = frontmatter dict + 누락 필드 목록

**6. Dependencies**: 없음 (① 진입 sub)

**7. Verification**: frontmatter 정확 파싱·누락 필드 정확 식별·yaml 오류 graceful 처리

---

## SUB 2: bookwriting-absorb-type-classifier

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: frontmatter `type` 누락 시 4 type 자동 추측 (seed·evidence·insight·cycle-input). Q13-D-2 (c) 자동 추측 옵션.

**3. Scope**
- In: 자동 추측 (Claude 의미 평가 + 규칙)
- Out: 라우팅 (Route Cascade)

**4. Behavior**:
```
Step 1: 본문 텍스트 + frontmatter 부분 정보 로드
Step 2: 규칙 매칭:
  - 짧은 명제·통찰 → seed
  - 출처·인용·통계 풍부 → evidence
  - "통찰·결론·해석" 단어 → insight
  - 외골격·구조·flow → cycle-input
Step 3: 규칙 모호 시 Claude 의미 평가
Step 4: confidence 0-1 점수
Step 5: < 0.7 → 저자 묶음 escalate
```

**5. Input·Output**: In = 본문 + frontmatter 부분 / Out = type + confidence

**6. Dependencies**: Frontmatter Parser 통과

**7. Verification**: type 추측 정확도 85%+·confidence < 0.7 시 저자 묶음

---

## SUB 3: bookwriting-absorb-route-cascade

**1. Identity**: 부모=master. INTERNAL. ⭐ 3-Layer cascade 라우팅 핵심.

**2. Purpose**: 저자 Q20-D-3 (d) cascade 라우팅 — 키워드 → Claude 의미 평가 → Obsidian 풀.

**3. Scope**
- In: 자산을 chapter·layer·section·chapter_role에 매핑
- Out: 저장 (Inbox Organizer)

**4. Behavior**:
```
L1: skeleton.md 키워드 매칭
  - 매칭 점수 ≥ 0.8 → 명확 → 라우팅 결정
  - < 0.8 → L2
L2: Claude 의미 평가
  - skeleton 외골격 + 자산 텍스트 의미 비교
  - confidence < 0.7 → L3
L3: Obsidian vault 참조
  - 저자 기존 글에서 비슷한 주제 위치 발견
  - 저자 패턴으로 라우팅 추론
저자 명시 안 했을 때만 발동
명시 (--to·--link) 시 cascade skip
```

**5. Input·Output**: In = type 분류된 자산 / Out = primary·cross-reference 후보 + confidence

**6. Dependencies**: Type Classifier 통과 + book-config search_paths

**7. Verification**: cascade L1-L3 confidence 흐름 명확·저자 spot-check 정확도 80%+

---

## SUB 4: bookwriting-absorb-inbox-organizer

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 처리 완료 자산을 inbox/_processed/로 이동·통계 출력.

**3. Scope**
- In: 처리 완료 파일 정리
- Out: 후속 단계 진입 (② fact-anchor·③ systemlink 등)

**4. Behavior**:
```
Step 1: 각 처리 결과 분기:
  - 등록 완료 → _processed/로 이동
  - 저자 묶음 대기 → inbox/ 잔류
  - 실패 → inbox/_failed/로 이동 + 저자 알림
Step 2: 통계 출력 (처리 N건 / 등록 N건 / 묶음 N건 / 실패 N건)
Step 3: cycle-registry outputs 갱신
```

**5. Input·Output**: In = 처리 결과 / Out = 파일 이동·통계·cycle-registry 갱신

**6. Dependencies**: Route Cascade 또는 저자 묶음 응답

**7. Verification**: 파일 이동 정확·통계 정합·실패 격리

---

**End: absorb 4 sub**
