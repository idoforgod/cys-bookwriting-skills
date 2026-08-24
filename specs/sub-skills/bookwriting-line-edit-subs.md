# SPEC: bookwriting-line-edit sub-skills (4개 핵심)

> ⑩ line-edit-master의 핵심 4 sub-skill.
> 마스터 SPEC: `../bookwriting-line-edit-master.md` 참조.
> 저자 voice strict 임계 0.85+ 도달의 핵심 페르소나.

---

## SUB 1: bookwriting-line-edit-vocabulary-refiner

### 1. Identity
부모: `bookwriting-line-edit-master`. INTERNAL.

### 2. Purpose
저자 *preferred·avoid·prohibitions* 어휘 정밀 치환. 외국어 무분별 한국어 치환. PROH-001 위반 0건 목표.

### 3. Scope
- **In**: 어휘 치환 (preferred 추가·avoid 제거·외국어 한국어)
- **Out**: 문장 리듬 (다른 sub) / 시그니처 (다른 sub)

### 4. Behavior
```
Step 1: 본문 어휘 분석 (book-config voice_guidelines.vocabulary)
Step 2: avoid 표현 자동 감지·치환 후보 생성
Step 3: preferred 어휘 *치환 기회* 발견 (강제 X — 자연스러운 곳만)
Step 4: 외국어 → 한국어 자동 치환 (framework→프레임워크, agent→에이전트)
Step 5: 저자 묶음 (자동 치환 안 한 곳은 저자 결정)
```

### 5. Input·Output
- **In**: ⑦ 통과 본문 / book-config voice_guidelines
- **Out**: 어휘 치환된 본문 + 치환 diff

### 6. Dependencies
- ⑦ content-expand 통과
- voice-gate cross-cutting과 협업

### 7. Verification
1. avoid 어휘 0건 (자동 치환)
2. PROH-001 (외국어) 위반 0건
3. preferred 어휘 사용 빈도 증가
4. before·after diff 보존

---

## SUB 2: bookwriting-line-edit-signature-applier

### 1. Identity
부모: master. INTERNAL. ⭐ 저자 *시그니처 패턴 정밀 적용* 담당.

### 2. Purpose
저자 5 시그니처 패턴 *적용 기회 자동 발견*. 적용 가능한 모든 곳에 시그니처 치환 (자연스러운 곳만). 활용률 35%+ 목표 (cross-cutting 30%보다 엄격).

### 3. Scope
- **In**: 5 시그니처 패턴 적용
- **Out**: voice·rhythm 일반 보정

### 4. Behavior
```
Step 1: 본문 구조 분석 (단락·문장)
Step 2: 5 시그니처 패턴 적용 기회 발견:
  - "이 책은 X가 아니라 Y" — 도입·결론·전환점
  - "셋 중 하나가 아니다" — 분기 결론
  - "X와 Y 사이의 거리" — 시간 좌표·대비
  - "두 창업자가 정확히 같은 N배" — 수렴
  - "변수 X에 따라 결과 갈리는 동일 시스템" — 시스템 사고
Step 3: 적용 시도 (자연 흐름 보존 — 강제 X)
Step 4: 활용률 35%+ 도달 확인
```

### 5. Input·Output
- **In**: vocabulary-refiner 통과 본문 / signature_expressions
- **Out**: 시그니처 패턴 적용 본문 + 활용률 보고

### 6. Dependencies
- vocabulary-refiner 통과

### 7. Verification
1. 시그니처 패턴 활용률 35%+
2. 자연스러운 곳에만 적용 (억지 0건)
3. 저자 spot-check 통과
4. 저자 책 *고유 voice* 강화

---

## SUB 3: bookwriting-line-edit-ai-tone-purger

### 1. Identity
부모: master. INTERNAL. ⭐ AI 어투 자동 감지·제거 담당.

### 2. Purpose
*기성 AI 패턴* (PROH-005) 자동 감지·저자 voice로 치환. 저자 책의 *AI 어투 0건* 목표.

### 3. Scope
- **In**: AI 어투 자동 감지·치환
- **Out**: voice score 일반 계산 (다른 sub)

### 5. Behavior
```
Step 1: AI 어투 패턴 감지:
  - "물론, 이는 매우 중요한 질문입니다"
  - "다음과 같이 살펴볼 수 있습니다"
  - "이러한 점들을 고려할 때"
  - "결론적으로 말하자면"
  - "여러분도 동의하실 것입니다"
  - 기타 GPT·Claude 기본 어투 패턴 풀
Step 2: 감지 빈도 카운트
Step 3: 저자 voice로 자동 치환:
  - "물론, 이는 매우 중요" → 저자 시그니처 활용 또는 즉시 명제 진입
  - 결론 표현 → 저자 *셋 중 하나가 아니다* 패턴
Step 4: PROH-005 위반 0건 도달
```

### 5. Input·Output
- **In**: signature-applier 통과 본문 / PROH-005 패턴 풀
- **Out**: AI 어투 제거 본문 + 제거 카운트

### 6. Dependencies
- signature-applier 통과

### 7. Verification
1. PROH-005 위반 0건
2. 저자 voice로 자연스러운 치환
3. 본문 *AI 어투 0건* 검증
4. 저자 spot-check 통과

---

## SUB 4: bookwriting-line-edit-voice-validator

### 1. Identity
부모: master. INTERNAL. Strict 임계 0.85+ 검증.

### 2. Purpose
앞 3 sub (vocabulary·signature·ai-tone) 통과 후 *voice_score 재계산*. strict 임계 0.85+ 미달 시 *추가 첨삭 시도* (최대 2회). 최종 실패 시 저자 묶음.

### 3. Scope
- **In**: voice_score 재계산·추가 첨삭 시도
- **Out**: lifecycle POLISHED 진입 (마스터 담당)

### 4. Behavior
```
Step 1: 본문 voice_score 재계산 (5 가중치)
Step 2: ≥ 0.85 → 통과 → 시드 lifecycle POLISHED 진입 권장
Step 3: < 0.85 → 추가 첨삭 시도 (최대 2회)
Step 4: 여전히 실패 → 저자 묶음 escalate
  - (a) 저자 직접 수정
  - (b) 원본 유지 (voice 위반 수용)
  - (c) defer
  - (d) ⑦ content-expand 재호출
```

### 5. Input·Output
- **In**: ai-tone-purger 통과 본문 / book-config voice_guidelines
- **Out**: voice 통과 본문 (0.85+) + lifecycle 갱신 신호

### 6. Dependencies
- ai-tone-purger 통과

### 7. Verification
1. voice_score 0.85+ 달성
2. 시드 lifecycle INSIGHTED → POLISHED 진입 권장
3. progress.voice_violations_resolved 갱신
4. 최종 저자 책 *문장 미시 품질 보장*

---

---

## SUB 5: bookwriting-line-edit-sentence-rhythm-tuner

**1. Identity**: 부모=master. INTERNAL. Sentence Rhythm Tuner 페르소나.

**2. Purpose**: 저자 문장 *리듬·길이·태* 정밀화. 평균 50자·max 80자·능동태·저자 리듬 패턴.

**3. Behavior**:
```
Step 1: 본문 문장별 분석:
  - 길이 (글자 수)
  - 태 (능동·수동)
  - 리듬 패턴 (단문·장문 흐름)
Step 2: 저자 voice_guidelines.sentence 규칙 적용:
  - max_length 80자 초과 시 분해 시도
  - 수동태 → 능동태 전환
  - 중복 수식·과도한 종속절 제거
Step 3: 저자 리듬 패턴 적용:
  - "짧은 명제 + 풍부한 부연" (3박자)
  - "수치 + 인용 + 사상적 해석" (3박자)
Step 4: 자동 첨삭 + diff 보존
```

**4. Input·Output**: In = vocabulary-refiner 통과 본문 / Out = 리듬 정밀화 본문 + diff

**5. Dependencies**: vocabulary-refiner 통과

**6. Verification**: 평균 문장 50자±10·수동태 < 10%·max 80자 위반 0건·저자 리듬 패턴 검출

---

## SUB 6: bookwriting-line-edit-diff-preserver

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 모든 line-edit 변경의 *before·after diff 자동 보존*. 저자 후일 *원복 가능* 보장.

**3. Behavior**:
```
Step 1: 모든 sub의 변경 사항 capture
Step 2: diff 형식:
  - .before 백업 파일 (chapter <file>.md.before)
  - cycle-registry.outputs.line_edit_diffs 필드
Step 3: 변경 통계:
  - 어휘 치환 N건
  - 시그니처 적용 N건
  - AI 어투 제거 N건
  - 문장 리듬 변경 N건
Step 4: 저자 spot-check·원복 가능 인터페이스 제공
```

**4. Input·Output**: In = 모든 sub 변경 / Out = diff 보존 + 통계

**5. Dependencies**: 모든 line-edit sub 통과 후 마지막 발동

**6. Verification**: diff 100% 보존·저자 원복 명령 (`/bookwriting-line-edit revert`) 지원·통계 정합

---

**End of SUB SPEC: line-edit 6 sub**
