# SPEC: bookwriting-insight-synthesis sub-skills (4개 핵심)

> ⑥ insight-synthesis-master의 핵심 4 sub-skill 명세.
> 마스터 SPEC: `../bookwriting-insight-synthesis-master.md` 참조.
> Q18 매트릭스: 마스터 1 + 8 sub. 본 SPEC은 4개 핵심만. 나머지 4 sub는 구축 시점 결정.
>
> 작성일: 2026-05-24
> 양식: sub-skill 간략 8 항목

---

## SUB 1: bookwriting-insight-synthesis-candidate-generation

### 1. Identity
| 항목 | 값 |
|---|---|
| 부모 마스터 | `bookwriting-insight-synthesis-master` |
| 카테고리 | INTERNAL sub-skill (disable-model-invocation: true) |
| Q18 매트릭스 | 마스터의 1번째 sub |

### 2. Purpose
3 AI Agents 페르소나 (Meta-tool Identifier·System Loop Detector·Surprise Hunter)를 동시 발동해 *통찰 후보 9-15개* 생성. 후속 sub들의 *평가 대상 풀* 제공.

### 3. Scope
- **In**: 3 페르소나 발동·후보 INS-NNN 임시 ID 발급·각 페르소나당 3-5개 후보
- **Out**: 후보 평가 (다른 sub) / 후보 본문 작성 (⑦)

### 4. Behavior
```
Step 1: 시드·evidence·skeleton 로드
Step 2: Meta-tool Identifier 발동 (3-5 후보 생성)
Step 3: System Loop Detector 발동 (2-4 후보)
Step 4: Surprise Hunter 발동 (3-5 후보)
Step 5: 임시 ID 발급 + 풀 정돈
Step 6: 다음 sub (meaning·impact·surprise-evaluation)에 전달
```

### 5. Input·Output
- **Input**: ch-NNN·S-NNN | evidence-track | skeleton.md
- **Output**: 후보 풀 (INS-NNN × 9-15) + 페르소나 raw output

### 6. Dependencies
- ④ evidence-collect 통과
- 마스터의 Cycle C2 (다중 시드)에 호출됨

### 7. Verification
1. ch01 호출 → 통찰 후보 11개 생성 (Meta-tool 4 / Loop 3 / Surprise 4)
2. 모든 후보에 INS-NNN 임시 ID 발급
3. 페르소나별 raw output 보존

---

## SUB 2: bookwriting-insight-synthesis-triad-evaluation

### 1. Identity
| 항목 | 값 |
|---|---|
| 부모 마스터 | `bookwriting-insight-synthesis-master` |
| 카테고리 | INTERNAL sub-skill |
| 통합 sub | meaning + impact + surprise 평가 통합 (3 sub을 1 SPEC으로 집약 — 저자 진북 *3 기준* 동시 평가) |

### 2. Purpose
저자 진북 *3 기준* (의미·영향력·놀라움) 점수 0-1 평가. 종합 점수 = 0.35·meaning + 0.35·impact + 0.30·surprise.

### 3. Scope
- **In**: 후보별 *3 점수* 계산·종합 점수
- **Out**: 권위 매핑 (다른 sub) / 본문 작성 (⑦)

### 4. Behavior
```
Step 1: 후보 풀 로드
Step 2: meaning-evaluation 페르소나 (Meaning Synthesizer)
  - 저자 사상적 척추 (메타도구·시스템사고·UBI지능·인문학적 창조자) 연결 깊이
Step 3: impact-evaluation 페르소나 (Impact Assessor)
  - 정량 앵커·스케일·시점 도달
Step 4: surprise-evaluation 페르소나 (Surprise Hunter)
  - 통념 깨기·프레임 전복·수렴의 놀라움
Step 5: 종합 점수 계산 + 종합 점수 ≥ 2.7 → ★ 추천 자동 부여
```

### 5. Input·Output
- **Input**: candidate-generation 후보 풀
- **Output**: 후보별 (meaning_score, impact_score, surprise_score, weighted_score, ★ 여부)

### 6. Dependencies
- candidate-generation 통과
- book-config의 surprise_weight (기본 0.30)

### 7. Verification
1. 11 후보 평가 → meaning 평균 0.72 / impact 평균 0.61 / surprise 평균 0.55
2. ★ 추천 자동 부여 (종합 ≥ 2.7) 3개
3. 점수 0-1 범위 100%

---

## SUB 3: bookwriting-insight-synthesis-voice-craft

### 1. Identity
| 항목 | 값 |
|---|---|
| 부모 마스터 | `bookwriting-insight-synthesis-master` |
| 카테고리 | INTERNAL sub-skill |
| 저자 강조 영역 | ⭐ Voice Aligner 페르소나 발동 |

### 2. Purpose
선별된 통찰 후보를 *저자 voice + 시그니처 패턴*으로 재표현. voice_score 0.7+ 보장. voice-gate 자동 발동 적용.

### 3. Scope
- **In**: voice·시그니처 적용 + 재표현 1회 시도
- **Out**: voice 위반의 *재작성 무한 시도* (voice-gate가 cross-cutting 담당)

### 4. Behavior
```
Step 1: 통찰 후보 텍스트 로드
Step 2: Voice Aligner 페르소나 발동
  - 저자 preferred 어휘 치환
  - 5 시그니처 패턴 적용 시도 (X가 아니라 Y / 셋 중 하나 아니다 / X와 Y 사이 거리 / 두 창업자 N배 / 변수 X 따라 결과 갈리는)
Step 3: voice_score 재계산
Step 4: < 0.7 → 1회 재시도
Step 5: 여전히 < 0.7 → 저자 묶음 escalate (재작성 옵션)
```

### 5. Input·Output
- **Input**: 통찰 후보 텍스트·voice_guidelines
- **Output**: voice 통과 통찰 표현 + voice_score + 시그니처 활용 표시

### 6. Dependencies
- triad-evaluation 통과 (★ 추천 통찰만 voice-craft 발동)
- voice-gate cross-cutting (자동)
- book-config voice_guidelines

### 7. Verification
1. 5 ★ 추천 통찰 모두 voice_score 0.7+ 도달
2. 시그니처 패턴 활용률 30%+
3. 재작성 1회 시도 후에도 실패 시 저자 묶음

---

## SUB 4: bookwriting-insight-synthesis-bundle-builder

### 1. Identity
| 항목 | 값 |
|---|---|
| 부모 마스터 | `bookwriting-insight-synthesis-master` |
| 카테고리 | INTERNAL sub-skill |

### 2. Purpose
저자 묶음 제안을 *마크다운 형식*으로 정돈. ★ 추천 표시 + 종합 점수 + 권위 매핑 + cross-reference 별도 묶음. 저자 응답 형식 `1=a,b,c / 2=skip`로 즉답 가능.

### 3. Scope
- **In**: 5-7 통찰을 묶음으로 정돈·바이올레이션 묶음 통합
- **Out**: 저자 응답 파싱 (bookwriting-master HITL Mediator 담당)

### 4. Behavior
```
Step 1: 통과 통찰들 (voice·citation·R4) 수집
Step 2: ★ 추천 표시 (종합 점수 상위 2-3개)
Step 3: 묶음 1: 통찰 채택 (5-7개 후보)
Step 4: 묶음 2: cross-chapter 매핑 (해당 시)
Step 5: 묶음 3: 위반 escalation (voice·citation 위반 발견 시)
Step 6: cycle-registry에 D-NNN 등록
Step 7: 저자 화면 출력
```

### 5. Input·Output
- **Input**: voice-craft 통과 통찰·권위 매핑·cross-chapter 결과
- **Output**: 저자 화면 markdown + decision_id D-NNN + cycle-registry 갱신

### 6. Dependencies
- voice-craft + cross-chapter-check + authority-multi-layer 통과
- bookwriting-master의 HITL Mediator 페르소나와 협업

### 7. Verification
1. 묶음 마크다운 형식 정합 (헤더·★·구조화 응답 형식)
2. D-NNN decision_id 발급
3. cycle-registry.pending_decisions 등록
4. 저자 즉답 가능 형식

---

---

## SUB 5: bookwriting-insight-synthesis-meaning-evaluation

**1. Identity**: 부모=master. INTERNAL. Meaning Synthesizer 페르소나 *별도 명세* (triad-evaluation에서 분리).

**2. Purpose**: 통찰 후보의 *의미 점수* 0-1 계산. 저자 책 사상적 척추 (메타도구·시스템사고·UBI지능·인문학적 창조자) 연결 깊이.

**3. Behavior**:
```
Step 1: 통찰 후보 텍스트 로드
Step 2: 저자 4 사상적 척추와의 *연결 깊이* 평가:
  - 메타도구 명제 직접 연결: +0.30
  - 시스템 사고 변수 연결: +0.25
  - UBI(지능) 명제 연결: +0.25
  - 인문학적 창조자 명제 연결: +0.20
Step 3: 의미 점수 0-1 정규화
Step 4: skeleton.md §사상적척추와 정합 검증
```

**4. Input·Output**: In = 통찰 후보 / Out = meaning_score 0-1 + 척추 매핑

**5. Dependencies**: candidate-generation 통과

**6. Verification**: 모든 후보 meaning_score 0-1 범위·저자 사상적 척추 정합

---

## SUB 6: bookwriting-insight-synthesis-impact-evaluation

**1. Identity**: 부모=master. INTERNAL. Impact Assessor 페르소나 *별도 명세*.

**2. Purpose**: 통찰의 *영향력 점수* — 스케일·범위·시점 도달.

**3. Behavior**:
```
Step 1: 통찰의 정량 앵커 추출 (100배·90% 확신·5억 명 등)
Step 2: 영향력 차원 평가:
  - 스케일 (산업혁명 N배·인구 N명·GDP 영향)
  - 범위 (한국·아시아·세계·우주)
  - 시점 도달 (1년·5년·10년)
Step 3: impact_score 0-1 정규화
Step 4: 저자 정량 표현 패턴 정합
```

**4. Input·Output**: In = 통찰 후보 / Out = impact_score + 정량 앵커 표시

**5. Verification**: impact_score 0-1 범위·정량 앵커 명시·저자 정량 패턴 정합

---

## SUB 7: bookwriting-insight-synthesis-surprise-evaluation ⭐

**1. Identity**: 부모=master. INTERNAL. Surprise Hunter 페르소나 *별도 명세*. ⭐ 저자 진북 *깜짝놀랄만한* 단면 선택 핵심.

**2. Purpose**: 통찰의 *놀라움 점수* — 통념 깨기·프레임 전복·수렴의 놀라움.

**3. Behavior**:
```
Step 1: 통찰 후보를 *독자 예상* vs *실제 명제* 차이 평가
Step 2: 놀라움 유형 분류:
  - 통념 깨기 ("AGI는 도구가 아니라 메타도구")
  - 프레임 전복 ("셋 중 하나가 아니라 공진화")
  - 수렴의 놀라움 ("두 창업자가 같은 100배")
  - 역사 평행 놀라움 ("1930년대 대공황 패턴 재현")
Step 3: surprise_score 0-1 정규화
Step 4: 저자 시그니처 패턴 활용 기회 표시
```

**4. Input·Output**: In = 통찰 후보 / Out = surprise_score + 놀라움 유형

**5. Verification**: surprise_score 0-1·놀라움 유형 명확·시그니처 활용 기회 식별

---

## SUB 8: bookwriting-insight-synthesis-cross-chapter-check

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 통찰의 *다른 챕터 연결* 발견 — primary 챕터 외 secondary 매핑 후보 제시.

**3. Behavior**:
```
Step 1: 통찰의 사상적 척추·시스템 루프 매핑 추출
Step 2: 다른 챕터의 시드·통찰과 비교
Step 3: cross-reference 후보 발견 (예: ch01 INS-001 → ch08 추가 매핑)
Step 4: 저자 묶음 (cross-chapter 채택 선택)
```

**4. Input·Output**: In = 통찰 + 다른 챕터 컨텍스트 / Out = cross-reference 후보 목록

**5. Verification**: cross-reference 정확도 75%+·저자 spot-check 통과

---

## SUB 9: bookwriting-insight-synthesis-authority-multi-layer

**1. Identity**: 부모=master. INTERNAL. ⭐ R4 다층 강제.

**2. Purpose**: 통찰을 저자 권위 5층 (A-E) 매핑·R4 다층 강제.

**3. Behavior**:
```
Step 1: 통찰을 뒷받침하는 evidence들의 권위 등급 식별
Step 2: 통찰의 *권위 매핑 분포* 계산
Step 3: 최소 2층 매핑 강제 (R4)
Step 4: 단일 권위만 매핑 → 통찰 풀에서 *제외*
Step 5: Layer 1만 매핑 → 저자 알림 (Layer 2 저자 보강 권장)
```

**4. Input·Output**: In = 통찰 + evidence / Out = 권위 매핑 + R4 검증 결과

**5. Dependencies**: ④ evidence-collect의 권위 등급화

**6. Verification**: R4 통과 100%·매핑 정확·풀 정리 후 통찰 수 감소

---

**End of SUB SPEC: insight-synthesis 9 sub (마스터 매트릭스 8 + triad wrapper)**
