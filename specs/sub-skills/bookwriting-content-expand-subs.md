# SPEC: bookwriting-content-expand sub-skills (4개 핵심)

> ⑦ content-expand-master의 핵심 4 sub-skill.
> 마스터 SPEC: `../bookwriting-content-expand-master.md` 참조.
> 저자 *2층 표준 골격 7요소* 중 핵심 4 페르소나 sub.

---

## SUB 1: bookwriting-content-expand-weak-signal-synthesizer

### 1. Identity
부모: `bookwriting-content-expand-master`. INTERNAL. 저자 2층 골격 *요소 2 (약신호)* 담당.

### 2. Purpose
저자 *약신호 (Weak Signal)*를 본문에 *가시적 증거*로 풀어 작성. 한국 자율주행 택시·앤스로픽 매출 곡선·코슬라 80%·전신마비 환자 뉴럴링크 등 *구체 사례*로 변환.

### 3. Scope
- **In**: 채택된 통찰의 *약신호 차원* 본문 작성 (200-600자)
- **Out**: 추동력·시스템 루프 (다른 sub)

### 4. Behavior
```
Step 1: 통찰 + evidence-track 로드
Step 2: 가장 *가시적*인 evidence 선별 (영상·뉴스·저자 직접 관찰)
Step 3: 저자 *콜드오픈 라이브러리* (skeleton.md chapter-pipeline에 명시)와 정합
Step 4: 약신호 본문 작성 (시간·장소·감각 디테일 동반)
Step 5: voice·citation gate 자동 발동
```

### 5. Input·Output
- **In**: INSIGHTED 시드 / evidence-track / book-config
- **Out**: analysis.md의 약신호 부분 (200-600자)

### 6. Dependencies
- ⑥ insight-synthesis 통과 / ④ evidence-collect 풍부 evidence

### 7. Verification
1. 약신호 본문에 구체적 시간·장소·인물 명시
2. evidence 인용 1-3개 (Grade A·B 우선)
3. voice_score 0.7+

---

## SUB 2: bookwriting-content-expand-driving-force-synthesizer

### 1. Identity
부모: master. INTERNAL. 저자 2층 골격 *요소 3 (추동력)* 담당.

### 2. Purpose
약신호를 만든 *시스템적 힘*을 본문에 풀어 작성. 한계비용 제로·자본 동원·패러다임 전환 등.

### 3. Scope
- **In**: 추동력 본문 작성 (200-500자)
- **Out**: 시스템 루프 호명 (다음 sub)

### 4. Behavior
```
Step 1: 약신호 본문 로드 (앞 sub 출력)
Step 2: 저자 *추동력 패턴* 매칭 (한계비용·자본·기술 곡선·정치 변수)
Step 3: 추동력 본문 작성 (시스템 사고 흐름)
Step 4: 시그니처 패턴 *변수 X 따라 결과 갈리는* 적용 시도
Step 5: voice·citation gate
```

### 5. Input·Output
- **In**: 약신호 본문 / 통찰 / system_loops 매핑
- **Out**: analysis.md 추동력 부분 (200-500자)

### 6. Dependencies
- weak-signal-synthesizer 통과

### 7. Verification
1. 추동력이 약신호와 *논리적 연결*
2. 저자 시스템 사고 어휘 (한계비용·피드백·임계) 사용
3. 시그니처 패턴 활용 시도

---

## SUB 3: bookwriting-content-expand-system-loop-narrator

### 1. Identity
부모: master. INTERNAL. 저자 2층 골격 *요소 4 (시스템 루프 호명)* 담당.

### 2. Purpose
저자 v1 *L1-L7 시스템 루프*를 본문에 *명시적으로 호명*. 어느 루프의 어떤 변수에 해당하는지, 어떤 피드백이 작동하는지.

### 3. Scope
- **In**: 시스템 루프 본문 작성 (300-600자)
- **Out**: 시나리오 분기·시점 좌표·횡단 연결 (다른 sub 또는 통합)

### 4. Behavior
```
Step 1: 통찰·시드의 system_loops 매핑 로드
Step 2: 저자 L1-L7 정의 (forecast-registry) 참조
Step 3: "L1 지능대체나선의 변수 1 — 인지 외주화" 형식으로 호명
Step 4: 변수 간 피드백 명시 (예: "변수 1 → 변수 2 → 변수 1 강화")
Step 5: 본문 작성 + 저자 시스템 사고 어휘 풍부 사용
```

### 5. Input·Output
- **In**: 시드·통찰의 system_loops 매핑 / forecast-registry / skeleton.md §2
- **Out**: analysis.md 시스템 루프 부분 (300-600자)

### 6. Dependencies
- ③ systemlink의 system_loops 매핑 / driving-force-synthesizer 통과

### 7. Verification
1. L1-L7 중 1개 이상 명시적 호명
2. 변수·피드백 명시
3. 저자 v1 chapter-pipeline.md의 2층 요소 4 양식 정합

---

## SUB 4: bookwriting-content-expand-voice-aligner

### 1. Identity
부모: master. INTERNAL. ⭐ Voice Aligner 페르소나 (⑩ line-edit도 유사 sub 보유).

### 2. Purpose
⑦ content-expand가 작성한 본문 전체에 *저자 voice + 시그니처 패턴* 적용. ⑩ line-edit의 *strict 임계 0.85+*보다 *gentle 임계 0.7+*. ⑩에서 추가 정밀화.

### 3. Scope
- **In**: 본문의 voice 가벼운 보정 (preferred 치환·간단 시그니처 적용)
- **Out**: strict voice (⑩ line-edit) / 통찰 평가 (⑥)

### 4. Behavior
```
Step 1: ⑦의 모든 layer 본문 (narrative·analysis·implications) 로드
Step 2: 저자 preferred 어휘 *기본 치환*
Step 3: 시그니처 패턴 *자연스러운 곳*에만 적용 (강제 X)
Step 4: voice_score 0.7+ 도달 확인
Step 5: voice-gate cross-cutting과 협업 (재작성 안 함 — 그건 voice-gate 담당)
```

### 5. Input·Output
- **In**: ⑦ 작성 본문 / book-config voice_guidelines
- **Out**: voice 통과 본문

### 6. Dependencies
- 다른 3 sub (weak-signal·driving-force·system-loop) 통과 후 마지막에 발동
- voice-gate cross-cutting (자동)

### 7. Verification
1. voice_score 0.7+ 달성 (chunk별)
2. 시그니처 패턴 활용률 30%+ (가능한 곳)
3. ⑩ line-edit이 *추가 정밀화*로 0.85+ 도달

---

---

## SUB 5: bookwriting-content-expand-proposition-restater

**1. Identity**: 부모=master. INTERNAL. 저자 2층 골격 *요소 1 (핵심 명제 재진술)* 담당.

**2. Purpose**: 1층 끝의 핵심 명제를 2층 시작에 *정량 데이터와 함께* 재진술. 저자 v1 2층 표준 골격 1번 요소.

**3. Behavior**:
```
Step 1: chapters/<ch>/narrative.md의 1층 끝 핵심 명제 추출
Step 2: 통찰에 연결된 정량 앵커 (Quantitative Anchor) 로드
Step 3: 명제를 정량 데이터와 함께 재진술:
  - 예: "AGI는 메타도구다" + "1-3년 90% 확신·100배 스케일"
Step 4: 저자 시그니처 "X와 Y 사이의 거리에서" 적용 시도
Step 5: 2층 첫 단락에 배치
```

**4. Input·Output**: In = 1층 명제·정량 앵커 / Out = 2층 재진술 단락 (200-400자)

**5. Dependencies**: ⑧ narrative-craft (1층 명제) + ④ evidence-collect (정량 앵커)

**6. Verification**: 정량 앵커 1+ 포함·시그니처 활용 시도·voice_score 0.7+

---

## SUB 6: bookwriting-content-expand-scenario-brancher

**1. Identity**: 부모=master. INTERNAL. 저자 2층 골격 *요소 5 (시나리오 분기)* 담당.

**2. Purpose**: 시나리오 분기 본문 작성 — 정치 변수에 따른 결과 다양화 (봉건제 vs 풍요·평화의 역설 등).

**3. Behavior**:
```
Step 1: 통찰의 시나리오 분기 후보 식별
Step 2: 저자 시그니처 *변수 X 따라 결과 갈리는 동일 시스템* 적용
Step 3: 분기 본문 작성:
  - 분기 1: 정치 변수 A 채택 → 결과 X
  - 분기 2: 정치 변수 B 채택 → 결과 Y
Step 4: skeleton.md의 챕터 시나리오 분기 후보와 정합
```

**4. Input·Output**: In = 통찰 + 시스템 루프 매핑 / Out = 시나리오 분기 본문 (400-800자)

**5. Dependencies**: system-loop-narrator 통과

**6. Verification**: 분기 2+ 명확·시그니처 패턴 활용·정치 변수 명시

---

## SUB 7: bookwriting-content-expand-time-coordinator

**1. Identity**: 부모=master. INTERNAL. 저자 2층 골격 *요소 6+7 (시점 좌표 + 횡단 연결)* 담당.

**2. Purpose**: AGI 5단계 시점 좌표 + 다른 챕터와의 횡단 연결 작성.

**3. Behavior**:
```
Step 1: 통찰의 *시점 좌표* (AGI 5단계 어느 단계인가) 식별
Step 2: AGI 5단계 — skeleton.md §시점 동기화에서 결정론 lookup (Round 9 #E4.1 Critical 수정)
  저자 v14 결정적 변화 3번 (skeleton.md 1589-1592줄) — OpenAI 공식 5단계 채택:
  - 단계 1: 챗봇
  - 단계 2: 추론가
  - 단계 3: 대행자
  - 단계 4: 혁신가
  - 단계 5: 조직 (AGI)
  
  ⚠ 영구 강제: 본 5단계 풀은 *하드코딩 금지* — 반드시 skeleton.md §시점 동기화 라인을 *결정론 read*해서 적용 (skeleton 변경 시 자동 반영)
Step 3: 횡단 연결 — 통찰이 *다른 챕터 어떤 시드와 맞물리는가*
Step 4: 본문 작성 — 시점 + 횡단 연결 (300-500자)
```

**4. Input·Output**: In = 통찰 + cross-chapter 매핑 / Out = 시점·횡단 본문

**5. Dependencies**: scenario-brancher 통과

**6. Verification**: AGI 5단계 명시·횡단 연결 1+ 명시·저자 v1 시점 동기화 정합

---

**End of SUB SPEC: content-expand 7 sub**
