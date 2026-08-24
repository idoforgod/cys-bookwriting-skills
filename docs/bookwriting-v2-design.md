# bookwriting v2 — 워크플로우 아키텍처 설계

> 저자 *제2저자 연구원 + 시뮬레이션 도구*로서 bookwriting v2의 *전체 청사진*.
>
> 본 문서는 *bookwriting을 처음 접하는 사람도 이해할 수 있는* 시스템 개요다.
> 세부 명세는 `../specs/` 폴더의 각 SPEC 참조.

---

## 1. 핵심 명제

### 1.1 무엇인가
`bookwriting`은 저자의 *책 쓰기 워크플로우*를 *AI 제2저자*와 함께 진행하는 *11 단계 마스터 + sub-skill 70+*의 스킬 세트이다.

### 1.2 무엇이 아닌가
- ❌ 저자 미래학자 본업 *분석 도구* (foresight 사슬은 별도 542 스킬)
- ❌ 설치된 다른 스킬을 *자동 호출하는 통합 메타* (옵션 A+ 자기완결)
- ❌ 모든 책 쓰기 작업을 *대체*하는 도구 (저자 통제·voice·통찰이 본질)

### 1.3 무엇을 하는가
저자가 *외부에서 foresight 사슬을 manual 호출*해 얻은 결과를 + *저자가 매일 던지는 시드*를 + *저자 자산 풀(Obsidian·NotebookLM)*을 *흡수·통합·매력적 글로 변환*한다.

---

## 2. 두 가지 사용 모드

### 2.1 모드 1 — 저자 감독 하 제2저자 (정밀 작업)
```
/bookwriting cycle ch01
  → 11 단계 마스터 순차 위임
  → 각 단계 결과마다 저자 HITL
  → chapter 파일에 *실제 책 원고* 작성
  → 시간: 15-30분/사이클
```

**저자가 *책 원고를 직접 만드는* 모드.** voice·통찰·정확성이 *반드시* 보장됨.

### 2.2 모드 2 — 전자동 시뮬레이션 (탐색·드래프트)
```
/bookwriting simulate ch01 --variant insight-driven
  → 11 단계 마스터 자동 진행 (HITL 0회)
  → ★ 추천 옵션 자동 채택
  → 별도 _simulations/sim-NNN.md 파일 생성 (드래프트)
  → 정식 chapter 파일 미갱신
  → 시간: 5-10분/사이클
```

**저자가 *원고 방향·내용을 미리 탐색하는* 모드.** 정밀하지 않지만 *대략적 흐름* 빠르게.

### 2.3 모드 1·2의 상호작용
```
[일상 패턴]
  ① /bookwriting simulate ch01           ← 탐색 (5분)
  ② 저자가 결과 보고 방향 결정
  ③ /bookwriting cycle ch01              ← 정밀 작업 (30분)
  
[승격 패턴]
  ① /bookwriting simulate ch01 --variant A   ← 시뮬 A
  ② /bookwriting simulate ch01 --variant B   ← 시뮬 B 비교
  ③ /bookwriting promote SIM-007              ← A 채택 → 정식 사이클 진입
```

---

## 3. 저자 진짜 워크플로우 안에서의 위치

### 3.1 저자 미래학자 본업 워크플로우 (15단계)

```
[분석 단계 — foresight 사슬]
 1. 신호 발견                → /foresight-environmental-scanning
 2. Fact + Score 수집        → /foresight-statistical-modeling
 3. 시스템 사고 연결          → /foresight-systems-perspective
 4. 빈 고리 채우기            → /foresight-structural-analysis
 5. 추가 통찰 추출            → /foresight-causal-layered-analysis
 6. 미래 시스템 구축          → /foresight-systems-perspective
 7. 패턴 추출                 → /foresight-tech-mining

[시뮬레이션 단계]
 8. 패턴 시뮬레이션          → /foresight-simulation-games
 9. 사이클 도출              → /foresight-realtime-delphi
10. 미래 테스트              → /foresight-robust-decisionmaking

[시나리오 단계]
11. 가장 적합한 선택         → /foresight-decision-modeling
12. 시나리오 기법 적용       → /foresight-scenarios
13. 미래 가능성 추출         → /foresight-futures-polygon

[글쓰기 단계 — bookwriting]
14. 의미·영향력·놀라움 단면 선택  → /bookwriting (insight-synthesis)
15. 매력적 글쓰기                  → /bookwriting (content-expand + narrative-craft)
```

### 3.2 bookwriting의 진짜 책임

```
저자 외부 manual:
  /foresight-* (1-13단계) → 결과 → inbox/ 또는 import

저자:
  /bookwriting absorb → 결과 흡수
  /bookwriting cycle ch01 → 11 단계 마스터로 매력적 글로 변환
```

bookwriting은 *foresight 결과를 매력적 책 원고로 변환하는 다리*다.

---

## 4. 11 단계 마스터 책임 매트릭스

| # | 마스터 | 책임 | 저자 15단계 매핑 | 비고 |
|---|---|---|---|---|
| 1 | absorb-master | foresight 결과·시드·자산 흡수 | (흡수 영역) | 진입 정밀도 핵심 |
| 2 | fact-anchor-master | fact·score 정합·중복·충돌 검증 | 2 (fact·score) | v1 forecast-registry 연동 |
| 3 | systemlink-master | 글쓰기 차원 연결·빈 고리 채움 | 3·4·5 (시스템·고리·통찰) | 글쓰기 차원 |
| 4 | evidence-collect-master | 책 인용 근거 수집·registry 갱신 | 2 (fact 글쓰기 차원) | v1 호환 |
| 5 | evidence-link-master | 근거 그래프·권위 5층 매핑 | 5·6 (통찰·시스템) | Phase 3-B |
| 6 | **insight-synthesis-master** | **의미·영향력·놀라움 단면 선택** | **14 (핵심)** | **제2저자 핵심 가치** |
| 7 | **content-expand-master** | **시드 → 꼭지 매력 글쓰기** | **15 (핵심)** | **제2저자 핵심 가치** |
| 8 | **narrative-craft-master** | **콜드 오픈·1층 서사·매력 도구** | **15 (핵심)** | **제2저자 핵심 가치, Phase 3-B** |
| 9 | structure-review-master | 챕터·꼭지 구조·층 균형 리뷰 | (정합성) | Phase 3-B |
| 10 | **line-edit-master** | **저자 voice·문장·표현 정밀** | (voice 보존) | **제2저자 핵심 가치** |
| 11 | cross-chapter-relink-master | 책 전체 cross-reference·재라우팅 | (cross-chapter) | Phase 3-B |

**볼드체 (⑥·⑦·⑧·⑩) = 저자 제2저자 역할의 핵심.** 이 4개 마스터의 SPEC을 *가장 정밀·진중·세밀*하게 작성한다.

---

## 5. 데이터 흐름

### 5.1 사이클 진입 시 데이터 흐름
```
입력 자원:
  ├─ slash command + args            ← 저자 명시
  ├─ book-config.yaml                ← 검색 경로·voice 가이드라인·매크로 트리거
  ├─ seed-registry.yaml              ← 시드 마스터
  ├─ cycle-registry.yaml             ← 사이클 히스토리
  ├─ skeleton.md                  ← 외골격 (책 전체 구조)
  ├─ forecast-registry.yaml          ← v1 호환 (예측 마스터)
  ├─ inbox/*.md                       ← 미처리 글감 (foresight 결과·저자 외부 작업)
  ├─ chapters/<ch>/*.md              ← 챕터 작업물 (6 파일 schema)
  └─ Obsidian vault + 저자 skill 폴더들  ← 자산 풀

bookwriting-master:
  ├─ 파싱·검증 → cycle-registry에 C-NNN 등록
  ├─ 11 단계 마스터 위임 (target_type 프리셋 따라)
  └─ Voice gate cross-cutting 적용

산출물:
  ├─ chapters/<ch>/narrative.md      ← 1층 서사
  ├─ chapters/<ch>/analysis.md       ← 2층 분석
  ├─ chapters/<ch>/implications.md   ← 3층 함의
  ├─ chapters/<ch>/evidence-track.yaml ← 사용 예측·시드 trace
  ├─ chapters/<ch>/seed-track.yaml   ← 사용 시드 매핑
  ├─ chapters/<ch>/pipeline-log.md   ← 사이클 행동 로그
  ├─ seed-registry.yaml              ← lifecycle·cycle_history 갱신
  ├─ cycle-registry.yaml             ← C-NNN status 갱신
  └─ forecast-registry.yaml          ← 신규 예측 발견 시 갱신
```

### 5.2 모드 2 시뮬레이션 데이터 흐름
모드 1과 *동일한 입력*에서 *동일한 11 단계 작업*. 차이:
- HITL 0회 → ★ 추천 자동 채택
- 산출물 위치 = `chapters/<ch>/_simulations/sim-NNN.md` (드래프트)
- 정식 chapter 파일·registry 미갱신
- cycle-registry에 `SIM-NNN` 별도 분류 등록

---

## 6. Voice 보존 — 저자 정체성 보호

### 6.1 3겹 가드
1. **Reference 풀**: 저자 NotebookLM 저서 전체 + Obsidian vault + skeleton.md
2. **yaml 가이드라인**: book-config.yaml의 voice_guidelines 섹션 — 저자 자기 명시
3. **Cross-cutting 게이트**: bookwriting-master의 Voice Gatekeeper 페르소나가 *모든 단계 출력*에 자동 발동

### 6.2 voice yaml 가이드라인 항목
```yaml
voice_guidelines:
  vocabulary:
    preferred: ["메타 도구", "시스템 사고", "약신호", ...]
    avoid: ["AI가 일자리를 뺏는다", "단선적 인과 표현", ...]
  sentence:
    max_length_chars: 80
    preference: "단문 + 능동태"
  structure:
    paragraph_pattern: "명제→근거→사례→통찰"
    section_pattern: "1층 콜드오픈→2층 분석→3층 함의"
  prohibitions:
    - "외국어 무분별 사용"
    - "추상적 일반론 (구체적 시나리오 필수)"
  signature_expressions:
    - "이 책은 X가 아니라 Y를 다룬다"
    - "셋 중 하나를 선택하는 것이 아니다"
```

### 6.3 위반 시 처리
- 위반 감지 → 자동 재작성 1회 시도
- 재작성 실패 → 저자 묶음 제안 풀에 추가
- 저자 결정 → voice yaml 보강 (점진적 학습)

---

## 7. 저자 통제와 자율도

### 7.1 모드 1 자율도 (옵션 C — 단계별 HITL)
- 결정적 단계 (① absorb·② fact-anchor·④ evidence-collect): 빠른 confirm HITL
- 판단 단계 (⑥ insight-synthesis·⑦ content-expand·⑧ narrative-craft·⑩ line-edit): 정밀 묶음 HITL
- 저자 응답 형식: `1=a,b / 2=skip / 3=defer / 4=a`

### 7.2 모드 2 자율도 (전자동)
- HITL 0회 — 저자 검토는 *사이클 끝 종합 trace*에서
- 저자가 결과 보고 *모드 1 진입* 또는 *다른 variant 시뮬레이션*

### 7.3 저자 통제권
- 저자는 *언제든* 사이클 중단 가능 (Ctrl+C → INTERRUPTED 상태 저장 → resume 가능)
- 저자는 *언제든* 단계 마스터 직접 호출 가능 (`/bookwriting-* <mode>`)
- 저자는 *언제든* defer로 결정 보류 가능
- 저자는 *언제든* 설치된 다른 스킬 외부 호출 → inbox로 결과 가져옴

---

## 8. 폴더 구조 (cys-bookwriting-skills)

```
cys-bookwriting-skills/
├── _master_automation/              # 후일 자동화 보조
├── _progress/                        # 저자 진행 추적
│   ├── grill-me-decisions.md        # 25 결정 + sub 결정 (청사진)
│   └── build-checkpoint.md          # 구축 체크포인트
├── docs/                             # 거대 설계 문서
│   ├── bookwriting-v2-design.md     # 본 문서 (아키텍처)
│   ├── bookwriting-philosophy.md    # 저자 제2저자 철학
│   └── two-modes-design.md          # 모드 1·2 상세
├── specs/                            # 각 스킬 명세 (집약 검토용)
│   ├── bookwriting-master.md
│   ├── bookwriting-<single>-master.md ... (11개 + voice-gate + bridge)
│   ├── data-schema-*.md ... (4개)
│   └── sub-skills/
│       ├── bookwriting-absorb-*.md ... (4개)
│       ├── bookwriting-fact-anchor-*.md ... (4개)
│       └── ... (총 28개 sub)
├── expert_pool/                      # bookwriting cross-skill 공유 자원
│   └── voice-reference-pool.md      # 저자 voice 참조 자료 인덱스
└── skills/                           # 실제 SKILL.md (Phase 3-B)
    ├── bookwriting-master/
    │   ├── SKILL.md
    │   └── references/
    │       ├── ai_agent_personas.md
    │       ├── cycle_definitions.md
    │       ├── hitl_format.md
    │       └── gate_definitions.md
    └── ... (각 마스터별 동일 구조)
```

---

## 9. 저자 책임·도구 분리

### 9.1 저자 책임 (수동)
- 시드 입력 (`/bookwriting seed "..."`)
- foresight 사슬 외부 manual 호출
- HITL 묶음 결정 (모드 1)
- voice 가이드라인 최초 명시 + 점진 보강
- 사이클 검토·승인·중단

### 9.2 bookwriting 도구 책임 (자동)
- 사이클 orchestration·trace
- 결정적 단계 자동 수행
- 판단 단계 묶음 제안 생성
- voice gate cross-cutting
- registry·log 정합 갱신
- 매크로 트리거 자동 발동
- 시뮬레이션 자동 진행 (모드 2)

### 9.3 설치된 다른 스킬 (외부)
- foresight 사슬 (envscan·delphi·scenarios 등)
- vision·sermon·churchadmin 스킬들
- bookwriting이 자동 호출하지 *않음*
- 저자가 *명시 호출* 후 결과를 bookwriting에 전달

---

## 10. Phase 진행 상태

| Phase | 내용 | 상태 |
|---|---|---|
| Phase 1 | grill-me — 저자와 25 주요 결정 합의 | ✅ 완료 (2026-05-24) |
| Phase 2 | 명세 작성 — 40개 SPEC | 🔄 진행 중 (bookwriting-master 완료) |
| Phase 3-A | MVP 수직 슬라이스 구축 — 15 스킬 | ⏳ 대기 (명세 합의 후) |
| Phase 3-B | 저자 검증·작동 확인·미세 조정 | ⏳ 대기 |
| Phase 3-C | 나머지 마스터 (⑤·⑧·⑨·⑪) + 풀 sub 구축 | ⏳ 대기 |
| Phase 4 | 2단계 일반화 (옵션 C — 저자 외 저자 적용 가능) | ⏳ 미래 |

---

## 부록: 저자 의도 명확화 인용

> "스킬은 만들어진 순간, 그대로 작동하니.. 스킬이 내가 원하는데로 작동하지 않으면, 처음부터 다시 만들어야 한다."

> "중요한 것은 실제로 나를 도와서 제2저자 역할을 하는 나머지 스킬들의 성능이다."

> "스킬은 크게 2가지로 사용할 예정이다. 1)철저한 나의 감독 하에서 나의 제2저자 연구원으로 사용한다. 2)가끔은 몇 개의 스킬을 전자동으로 작동시켜, 원고의 방향이나 내용에 대한 대략적인 흐름을 시뮬레이션 해 본다."

> "지금 만드는 책쓰기 스킬 세트는 cys-bookwriting-skills라는 폴더를 만들고 그 안에 모두 담는 것은 어떤가? 그래야 일관성이 있고, 나중에 master claude가 운용하기에도 좋을 듯 하다."

이 인용들이 *bookwriting v2의 진북*이다. 모든 SPEC·SKILL은 이 진북을 향해 만들어진다.

---

**End of Architecture Document**
