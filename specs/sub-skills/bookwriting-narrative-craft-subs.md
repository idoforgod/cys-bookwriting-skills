# SPEC: bookwriting-narrative-craft sub-skills (7개)

> ⑧ narrative-craft-master의 7 sub-skill. 마스터: `../bookwriting-narrative-craft-master.md`
> ⭐ 저자 제2저자 핵심 — 매력 글쓰기 영역

---

## SUB 1: bookwriting-narrative-craft-cold-open-crafter

**1. Identity**: 부모=master. INTERNAL. ⭐ 콜드 오픈 작성 핵심.

**2. Purpose**: skeleton.md 콜드오픈 라이브러리 활용해 챕터 1층 *고유 장면 한 컷* 작성. 시간·장소·인물·감각 디테일.

**3. Scope**: In = 콜드오픈 작성 (600-1200자) / Out = 1층 흐름 (Sensory Detail Adder·Signature Weaver)

**4. Behavior**:
```
Step 1: skeleton.md chapter-pipeline의 챕터별 콜드오픈 후보 로드
  - 서장: 다보스 무대 (하사비스·아모데이·머스크 세 문장)
  - ch01: 한국 자율주행 / 앤스로픽 매출 곡선
  - ch07: 페르미 역설 새벽 천문학자
  - ch10: 카파시 한 문장 "사고 외주화 vs 이해 외주화"
Step 2: 핵심 시드·통찰의 핵심 명제 확인
Step 3: 콜드오픈 후보 2-3개 작성 (각 다른 후보 활용)
Step 4: 인용·통계 최소화·구체 장면 강제
Step 5: 1층 끝 한 문장 명제 단독 배치
```

**5. Input·Output**: In = INSIGHTED 시드·skeleton·forecast-registry / Out = 콜드오픈 후보 2-3개

**6. Dependencies**: ⑥ insight-synthesis·⑦ content-expand (2층 본문) 통과

**7. Verification**: 저자 v1 1층 5 검사항 통과·콜드오픈 후보 ≥2·구체 장면 명확

---

## SUB 2: bookwriting-narrative-craft-character-animator

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 등장인물 (Amodei·Hassabis·저자·하라리·바루파키스 등) 입체화.

**3. Scope**: In = 인물 입체화 (직책·맥락·신체 디테일·말투) / Out = 콜드오픈·시나리오 narrate

**4. Behavior**:
```
Step 1: 챕터 등장인물 식별 (forecast-registry author + skeleton 명시)
Step 2: 각 인물의 입체 정보:
  - 직책·소속·맥락
  - 신체 디테일 (가능한 evidence 기반)
  - 말투·발언 양식
Step 3: 본문에 "그가 말했다" 단순 인용 → 입체적 narrate로
Step 4: 단순 이름 → 풍부한 등장
```

**5. Input·Output**: In = 등장 인물 evidence / Out = 입체화 narrate 텍스트

**6. Dependencies**: ④ evidence-collect의 author·source 정보

**7. Verification**: 인물 입체화 ≥1명/콜드오픈·evidence 기반 정확

---

## SUB 3: bookwriting-narrative-craft-scenario-narrator

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 시나리오 분기 (봉건제 vs 풍요·평화의 역설 등)를 *서사적 풍경*으로.

**3. Behavior**:
```
- 키오스크 식당 풍경 vs 미슐랭 셰프 풍경
- 빛의 속도로 이동하는 AI 이민자
- 베네수엘라 작전 (팔란티어+클로드 실시간)
- 시나리오 분기를 *대비되는 두 장면*으로
```

**4. Input·Output**: In = 통찰 시나리오 분기 / Out = 서사적 묘사 (300-800자)

**5. Verification**: 시나리오 분기 명확·대비 풍경 효과적

---

## SUB 4: bookwriting-narrative-craft-historical-parallelist

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 저자 권위 Layer 5 (역사 평행) narrate.

**3. Behavior**:
```
- 1930년대 대공황 → AGI 시대 경제
- 핵무기 통제 → AGI 안전
- 산업혁명 러다이트 → 일자리 대체
- 앵글로색슨 영국 정복 → AI 이민
- 바이마르 의회 → 알고리즘 통치
저자 skeleton의 "권위 5층 Layer 5" 직접 활용
```

**4. Input·Output**: In = 역사 evidence / Out = 역사 평행 서사

**5. Verification**: 역사 사실 정확·저자 권위 5층 정합·시그니처 *두 창업자가 같은 N배* 패턴 활용

---

## SUB 5: bookwriting-narrative-craft-signature-weaver

**1. Identity**: 부모=master. INTERNAL. ⭐ 시그니처 패턴 정밀 적용.

**2. Purpose**: 저자 5 시그니처 패턴 *narrative 차원* 정밀 적용.

**3. Behavior**:
```
- "이 책은 X가 아니라 Y" — 도입·결론
- "셋 중 하나가 아니다" — 결론
- "X와 Y 사이의 거리" — 시간 좌표
- "두 창업자가 정확히 같은 N배" — 권위 수렴
- "변수 X 따라 결과 갈리는 동일 시스템" — 시스템 사고
적용 기회 자동 발견·자연스러운 곳에만 적용
```

**4. Input·Output**: In = 콜드오픈·서사 / Out = 시그니처 강화 narrate

**5. Verification**: 시그니처 패턴 활용률 30%+·자연스러움 평가

---

## SUB 6: bookwriting-narrative-craft-sensory-detail-adder

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 시각·청각·촉각 디테일 추가. 저자 v1 1층 검사항 *독자 감각 자극*.

**3. Behavior**: 콜드오픈·서사에 감각 디테일 자동 추가 — 시각 (장면)·청각 (말·소리)·촉각 (분위기).

**4. Input·Output**: In = 콜드오픈·서사 / Out = 감각 강화 narrate

**5. Verification**: 저자 v1 1층 *독자 감각 자극* 검사항 통과

---

## SUB 7: bookwriting-narrative-craft-voice-aligner

**1. Identity**: 부모=master. INTERNAL.

**2. Purpose**: 1층 narrative 본문에 저자 voice 정밀 적용. ⑩ line-edit과 협업.

**3. Behavior**: 1층 본문에 저자 voice·시그니처·preferred 어휘 적용·voice_score 0.7+ 도달.

**4. Input·Output**: In = 작성 본문 / Out = voice 통과 본문

**5. Verification**: voice_score 0.7+·시그니처 활용·voice gate cross-cutting 통과

---

**End: narrative-craft 7 sub**
