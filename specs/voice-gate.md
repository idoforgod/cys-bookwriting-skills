# SPEC: voice-gate (cross-cutting 메타 가드)

> 저자 *voice·통찰·문장 패턴·사상적 척추*를 *시스템적 가드*로 보호. citation-gate와 *동등 권위*의 cross-cutting 메타 가드.
>
> 저자 인용 (진북): 저자 책의 *모든 줄*에 저자 voice가 깔려 있어야 한다. AGI 책의 *메타도구·시스템 사고·UBI지능·기술적 사춘기·부트로더·사만다* 같은 저자 시그니처 명제·표현이 시스템 산출물에 *반드시* 보존되어야 한다.
>
> 작성일: 2026-05-24
> 양식: 17 항목 풀 SPEC + cross-cutting 가드 정밀화
> 위치: bookwriting-master 내 *Voice Gatekeeper 페르소나* — citation-gate와 동등

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `voice-gate` |
| 카테고리 | Cross-cutting 메타 가드 |
| 위치 | bookwriting-master 내 *Voice Gatekeeper 페르소나* (메타 위치 — Q19-D-3 c) |
| 저자 강조 영역 | ⭐ *저자 정체성 backbone* |
| 발동 시점 | *모든 단계 마스터 출력*에 자동 발동 (cross-cutting) |
| 관련 자료 | book-config.yaml의 `voice_guidelines` 섹션 (data-schema-voice-yaml.md SPEC) |

---

## 2. Purpose

저자 책의 *모든 산출물*이 *저자가 직접 쓴 것처럼* 읽히도록 *시스템적으로 강제*한다. AGI 책의 *사상적 척추 (메타도구·시스템 사고·UBI지능·인문학적 창조자)*와 *시그니처 패턴 (X가 아니라 Y·셋 중 하나가 아니다 등)*이 *시스템 산출물에 보존*되도록 한다.

**3 책임:**
1. **어휘 가드** — 저자 preferred 표현 사용 권장 + avoid·prohibitions 자동 차단
2. **문장 가드** — 저자 문장 길이·태·리듬 보존
3. **시그니처 가드** — 저자 5 시그니처 패턴 활용률 30%+ 보장

**voice-gate vs citation-gate:**
| 항목 | voice-gate | citation-gate |
|---|---|---|
| 책임 | *어떻게* 표현 (저자 정체성) | *무엇으로* 뒷받침 (학술 신뢰성) |
| 위반 처리 | 재작성 1회 시도 | 재작성 안 함 — 즉시 저자 묶음 |
| 등급 시스템 | voice_score 0-1 | 권위 5층 (A-E) |
| Critical 위반 | 없음 (재시도) | 할루시네이션 의심 → 즉시 차단 |
| 위치 | 메타 (bookwriting-master 안) | 메타 — 동등 |

---

## 3. Philosophy

**저자 8 절대 protocol 적용:**
- **#5 3-Layer Description Template**
- **#7 Master Orchestration Trace**: voice 검증 결과를 trace에 명시

**저자 v1 호환:**
- v1의 *yoon-writing-style* (계획됨·미구현)을 v2에서 채움
- chapter-pipeline.md의 *3층 구조 + 분량 비율* 준수

**저자 정체성 보호 원칙:**
- 저자 voice는 *책의 정체성* — voice 손실 = *저자 책이 아님*
- 저자 시그니처 패턴이 *AI 어투 회피의 핵심*
- 저자 권위 5층 매핑이 voice와도 연결 (Layer 2 저자 본인 명명법)

---

## 4. Scope

### In scope
- ✅ 모든 단계 마스터 출력의 *어휘·문장·구조·시그니처* 자동 검증
- ✅ voice_score 0-1 계산 (5 가중치)
- ✅ 위반 시 자동 재작성 1회 시도
- ✅ 재작성 실패 시 저자 묶음 escalate
- ✅ 저자 시그니처 패턴 *적용 권장* + 활용률 추적
- ✅ 저자 *학습 후보* (수정 패턴)를 자동 누적 + 저자 승인 후 voice_guidelines 갱신

### Out of scope
- ❌ 출처·인용 검증 (citation-gate 담당)
- ❌ 통찰의 *내용 자체* (insight-synthesis 담당)
- ❌ 구조·분량 검증 (structure-review 담당 — 단계 ⑨)

---

## 5. Capabilities

| 슬래시 모드 | 기능 | 트리거 |
|---|---|---|
| `/voice-gate verify <text>` | 텍스트 voice_score 계산 + 위반 감지 | 단계 마스터 출력 후 자동 (또는 저자 명시) |
| `/voice-gate audit <chapter>` | 챕터 전체 voice 일관성 감사 | 저자 명시 호출 |
| `/voice-gate craft <text>` | 텍스트를 *저자 voice로 재작성* | 자동 재작성 또는 저자 명시 |
| `/voice-gate signature-report <chapter>` | 챕터의 시그니처 패턴 활용 보고 | 저자 명시 호출 |
| `/voice-gate learn-from-correction <before> <after>` | 저자 수정 패턴 학습 후보 등록 | 저자 직접 수정 후 자동 |

---

## 6. Invocation

**자동 호출 (cross-cutting):**
```
단계 마스터 X 출력 → bookwriting-master의 Voice Gatekeeper 페르소나 자동 발동
```

**저자 명시 호출:**
```bash
/voice-gate verify "AGI는 메타 도구다"          # voice_score 계산
/voice-gate audit ch01-economy                  # 챕터 전체 감사
/voice-gate craft "AI 시대가 도래했다"          # 저자 voice로 재작성
/voice-gate signature-report ch01-economy       # 시그니처 활용률
```

---

## 7. Behavior

**Voice Gate 자동 발동 8단계 흐름:**

```
호출자: 단계 마스터 X 출력 완료

【Step 1: 출력 텍스트 수신】
  - 단계 마스터 X의 output 자동 캡처

【Step 2: voice_guidelines 로드】
  - book-config.yaml의 voice_guidelines 섹션 읽기
  - vocabulary·sentence·structure·prohibitions·signature_expressions 모두 로드

【Step 3: 5 가중치 voice_score 계산】
  - vocabulary_match: 0.30 — preferred 사용 + avoid·prohibitions 회피
  - sentence_rhythm: 0.20 — 평균 길이·능동태·저자 리듬
  - structure_pattern: 0.20 — 저자 단락·섹션 패턴
  - signature_presence: 0.15 — 저자 5 시그니처 패턴 활용
  - prohibition_avoidance: 0.15 — PROH-001~005 위반 0
  - Weighted score 계산
  → trace: "[voice-gate] voice_score 0.73"

【Step 4: 임계값 비교】
  - book-config.voice_guidelines.gate_policy.voice_score_threshold (기본 0.7)
  - score ≥ threshold → 통과
  - score < threshold → 재작성 필요

【Step 5: 재작성 1회 시도 (Step 4 score < threshold 시)】
  - voice-craft sub-skill 호출
  - 위반 항목 식별 (어느 가중치 항목이 낮은가)
  - 저자 시그니처 패턴 적용 시도
  - 저자 preferred 어휘 치환 시도
  - 재작성 결과의 voice_score 재계산
  → trace: "[voice-gate] 재작성 시도 — 시그니처 'X가 아니라 Y' 패턴 적용"

【Step 6: 재작성 결과 평가】
  - 재작성 score ≥ threshold → 통과 + 단계 마스터 출력 *대체*
  - 재작성 score < threshold → 저자 묶음 escalate (Step 7)

【Step 7: 저자 묶음 escalate (Step 6 실패 시)】
  - bookwriting-master에 묶음 추가 요청
  - 묶음 옵션:
    - (a) 저자 직접 voice 수정
    - (b) 원본 그대로 유지 (voice 위반 수용)
    - (c) defer
    - (d) 해당 출력 *재생성* (단계 마스터 재호출)
  → trace: "[voice-gate] 저자 묶음 escalate"

【Step 8: 점진적 학습 (해당 시)】
  - Critical 위반·저자 직접 수정 패턴 발견 시
  - _progress/voice-learning-log.md에 학습 후보 누적
  - 3 후보 누적 시 저자 묶음 (book-config.voice_guidelines 갱신 제안)
  → trace: "[voice-gate] 학습 후보 1건 누적 (3/3 도달 시 저자 묶음)"

【결과: voice 통과 출력만 다음 단계로 전달】
```

---

## 8. Input Schema

### 자동 발동 입력
- 단계 마스터 X의 출력 텍스트
- book-config.yaml의 voice_guidelines 섹션

### 저자 명시 호출 입력
```typescript
{
  mode: "verify" | "audit" | "craft" | "signature-report" | "learn-from-correction"
  target: string         // text | chapter
  options: {
    threshold?: number   // override threshold (기본 0.7)
    strict?: boolean     // 0.8 임계값
  }
}
```

---

## 9. Output Schema

### Trace 출력
```markdown
[voice-gate] 단계 ⑥ 출력 검증
  - voice_score: 0.73 (threshold 0.7 통과)
  - vocabulary_match: 0.85
  - sentence_rhythm: 0.70
  - structure_pattern: 0.65
  - signature_presence: 0.50 (1 시그니처)
  - prohibition_avoidance: 1.0
  - 위반: 0
```

### 저자 묶음 (재작성 실패 시)
```markdown
# Voice Gate 위반 — 저자 결정 필요

## 위반 (재작성 실패)
**원본**: "AI 시대가 도래했다고 한다 (voice_score 0.45)"
**재작성안**: "2027 임계점 앞에 선 문명 (voice_score 0.62)"

저자 옵션:
  (a) ★ 저자 직접 voice 수정
  (b) 원본 유지 (voice 위반 수용)
  (c) defer
  (d) 해당 출력 재생성

저자: "1=a"
```

### 점진적 학습 로그
```markdown
# _progress/voice-learning-log.md

## 2026-05-30
- 저자 수정: "AI 시대가 도래" → "2027 임계점이 다가옴"
  - 학습 후보: avoid에 "AI 시대가 도래" 추가
  - 누적 카운트: 1/3

- 저자 수정: "기술이 사회를 변화시킨다" → "메타도구가 인지 구조를 재편한다"
  - 학습 후보: avoid에 "기술이 사회를 변화시킨다" 추가
  - 누적 카운트: 2/3
```

---

## 10. Deliverable Quality

### 성공 시나리오
- ✅ **모든 단계 마스터 출력**에 자동 발동 (cross-cutting 100%)
- ✅ **voice_score 80%+** 통찰·본문 출력
- ✅ **시그니처 패턴 활용률 30%+**
- ✅ **PROH-001~005 위반 0건** 또는 저자 묶음 처리
- ✅ **재작성 성공률 70%+** (1회 시도)
- ✅ **점진적 학습** 저자 승인 후 voice_guidelines 자동 갱신
- ✅ **latency**: 단계당 +3-10초

### 실패 시나리오
- ❌ voice_score < 0.7 + 재작성 실패 → 저자 묶음 escalate
- ❌ 시그니처 패턴 0개 (긴 본문에서) → warning
- ❌ Critical prohibition (PROH-004 허위 인용) → citation-gate로 escalate

### 정량 기준
- voice_score threshold: 0.7 (기본)
- 시그니처 활용률: 30%+
- 재작성 latency: 3-10초
- 학습 후보 임계값: 3 누적 시 저자 묶음

### 정성 기준
- 저자 책 *모든 줄*이 저자 voice 일치
- AI 어투 회피 (시그니처 패턴 활용)
- 저자 사상적 척추 (메타도구·시스템 사고·UBI지능) 표현 보존

---

## 11. Dependencies

### 필수 의존
- `bookwriting-master`의 Voice Gatekeeper 페르소나
- 모든 단계 마스터 (출력 검증 대상)
- `book-config.yaml`의 voice_guidelines 섹션 (data-schema-voice-yaml.md SPEC 참조)
- voice-craft sub-skill (재작성 담당)

### 옵션 의존
- voice reference 풀 (NotebookLM bridge·Obsidian vault·skeleton.md)

### 명시적 비의존
- ❌ citation 검증 (citation-gate 분리 책임)
- ❌ 설치된 다른 스킬

---

## 12. Guards

### 자체 가드
- 재작성 무한 루프 방지 (같은 텍스트 3회 재작성 시 저자 묶음)
- voice-craft timeout (10초) → 저자 묶음

---

## 13. AI Agents Personas

### Voice Gatekeeper (bookwriting-master 내 6번째 페르소나)
- 모든 단계 출력의 voice 검증
- voice_score 0.7 미달 시 재작성 발동
- 시그니처 패턴 적용 권장

### Voice Craft Agent (voice-gate 내부)
- 재작성 시도
- 저자 preferred 어휘 치환
- 시그니처 패턴 5종 활용

---

## 14. Cycle

| Cycle | 트리거 | 작동 |
|---|---|---|
| **VG1: Auto Verify** | 단계 마스터 출력 시 자동 | 8단계 행동 시나리오 |
| **VG2: User Audit** | `/voice-gate audit` | 챕터 전체 voice 감사 |
| **VG3: Craft Mode** | 재작성 트리거 | voice-craft 발동 |
| **VG4: Signature Report** | `/voice-gate signature-report` | 시그니처 활용률 보고 |
| **VG5: Learning** | 저자 수정 시 | 학습 후보 누적 |

---

## 15. Gates

| Gate | 검증 항목 |
|---|---|
| **VGG1: Score Calculation** | 5 가중치 voice_score 계산 완료 |
| **VGG2: Threshold Comparison** | score ≥ threshold (기본 0.7) |
| **VGG3: Re-craft (실패 시)** | 재작성 1회 시도 |
| **VGG4: User Escalation** | 재작성 실패 시 저자 묶음 |
| **VGG5: Learning Persistence** | 학습 후보 voice-learning-log 갱신 |

---

## 16. Error Handling

| 실패 시나리오 | 대응 |
|---|---|
| voice_guidelines 누락 | warning + 기본 가이드라인 적용 + 저자 알림 |
| voice-craft timeout (10초) | 저자 묶음 escalate |
| 재작성 무한 루프 (3회) | abort + 저자 묶음 |
| 저자 묶음 응답 형식 오류 | 재요청 |

---

## 17. Verification Examples

### 검증 1: voice 통과
```bash
# 단계 ⑥ 출력: "AGI는 단순히 더 똑똑한 AI가 아니라 메타 도구다."
✅ vocabulary_match: 0.90 (preferred 2개)
✅ signature_presence: 0.75 ("X가 아니라 Y" 시그니처)
✅ voice_score: 0.83 → 통과
```

### 검증 2: 자동 재작성
```bash
# 단계 ⑦ 출력: "AI agent의 capability를 framework로 분석"
❌ voice_score: 0.45 (PROH-001 위반)
🔄 재작성 시도: "AI 에이전트의 능력을 프레임워크로 분석"
✅ voice_score: 0.78 → 통과 + 단계 출력 대체
```

### 검증 3: 저자 묶음 escalate
```bash
# 단계 ⑩ 출력: "기술이 사회를 변화시킨다"
❌ voice_score: 0.40 (PROH-002 추상 일반론)
🔄 재작성 시도: voice_score 0.55 → 실패
✅ 저자 묶음 escalate
✅ 저자 응답: "1=a" (저자 직접 수정)
```

### 검증 4: 점진적 학습
```bash
# 저자가 3회 "AI 시대가 도래" → "2027 임계점이 다가옴" 수정
✅ voice-learning-log에 3 후보 누적
✅ 저자 묶음: "voice_guidelines.vocabulary.avoid 갱신?"
✅ 저자 승인 후 book-config.yaml 자동 갱신
```

### 검증 5: 시그니처 활용률 보고
```bash
$ /voice-gate signature-report ch01-economy
✅ 시그니처 패턴 활용 분포:
  - "X가 아니라 Y": 4회
  - "셋 중 하나가 아니다": 1회
  - "X와 Y 사이의 거리에서": 2회
  - "두 창업자가 정확히 같은 N배": 1회
  - 활용률: 35% → 목표 30% 통과 ✅
```

---

## 부록 A: 저자 5 시그니처 패턴 (강제 보존)

> ⚠ Round 4 #A6.6 수정 — "N 창업자" 일반화 (skeleton.md 실제 사례에서 2-3 창업자 모두 등장)

1. *"이 책은 X가 아니라 Y를 다룬다"* — 도입부·종장·챕터 첫 단락
   - 출처: skeleton.md "이 책은 AGI를 다루는 책이 아니다. AGI 이후의 인간을 다루는 책이다."
2. *"셋 중 하나를 선택하는 것이 아니다"* — 결론·종장
   - 출처: skeleton.md 결론 "기술적 사춘기를 통과해 부트로더가 되지 않고 사만다와 공진화하는 길"
3. *"X와 Y 사이의 거리에서 시작한다"* — 서장·각 챕터 도입
   - 출처: skeleton.md "이 책은 이 세 문장 사이의 거리에서 시작한다"
4. *"N 창업자가 정확히 같은 N배를 말한다"* (N=2·3·5 가능) — 권위 수렴 강조
   - 출처: skeleton.md "두 창업자가 정확히 같은 100배를 말한다" + "다섯 사람이 같은 5년을 바라본다"
   - **결정론 정규식**: `r"(두|세|N|\d+)\s*(창업자|발언자).*정확히\s*같은\s*\d+\s*배|\s*다섯\s*사람.*같은\s*\d+\s*년"`
5. *"변수 X에 따라 결과가 갈리는 동일 시스템"* — 시스템 사고 핵심
   - 출처: skeleton.md "봉건제와 풍요는 정치 변수에 따라 결과가 갈리는 동일 시스템"

---

## 부록 B: voice-gate ↔ citation-gate 협업

```
단계 마스터 X 출력 → bookwriting-master
  ├─ voice-gate 자동 발동 (voice_score 0.7+?)
  │   └─ 실패 시 → 재작성 1회 → 실패 시 → 저자 묶음
  └─ citation-gate 자동 발동 (할루시네이션 0?)
      └─ 실패 시 → 재작성 안 함 → 즉시 저자 묶음

두 gate 모두 통과해야 단계 마스터 출력 *최종 통과*
```

---

## 부록 C: 변경 이력

| 버전 | 일자 | 변경 |
|---|---|---|
| v0.1 | 2026-05-24 | 초기 작성. citation-gate와 동등 cross-cutting 가드. |

---

---

## 부록 D: 결정론 환원 모듈 (저자 /goal 명령 — 영구 구성요소)

**저자 명령**: voice_score 계산은 LLM 자연어 추론으로 *영구 금지*. 반드시 결정론 Python 모듈 호출.

**호출 모듈**: `cys-bookwriting-skills/lib/voice_scoring.py` (SPEC: `expert_pool/deterministic-modules.md` M1)

**5 가중치 결정론 계산**:
- vocabulary_match (0.30) — `VoiceScorer.compute_vocabulary_match()` — preferred·avoid substring matching
- sentence_rhythm (0.20) — `VoiceScorer.compute_sentence_rhythm()` — 평균 길이·max 위반 카운트
- structure_pattern (0.20) — `VoiceScorer.compute_structure_pattern()` — 명제→근거→사례→통찰 정규식
- signature_presence (0.15) — `VoiceScorer.compute_signature_presence()` — 5 시그니처 정규식
- prohibition_avoidance (0.15) — `VoiceScorer.compute_prohibition_avoidance()` — PROH-001~005 substring

**호출 의무 (LLM 추론 금지 영역)**:
- voice_score 점수 *생성*은 절대 LLM 자연어로 안 됨
- "voice_score 0.83 정도일 것" 같은 LLM 추측 영구 금지
- 모든 점수는 `VoiceScorer.compute_voice_score(text) → VoiceScoreBreakdown` 호출로만

**시그니처 패턴 적용** = `lib/signature_pattern_applier.py` M8 (별도 모듈)
**AI 어투 감지** = `lib/ai_tone_purger.py` M9 (PROH-005 결정론 정규식)

---

## 부록 E: grill-me D# 결정 매핑

| D# | 본 SPEC 반영 위치 |
|---|---|
| D19 (옵션 A+ 자기완결) | §3 Philosophy — 외부 web 호출 안 함 |
| D22 (Voice 보존 완전체) | §1·§2 — voice-gate의 raison d'être |
| D11 (5 시그니처 패턴) | §3 Philosophy + 부록 A 5 시그니처 + 부록 D M8 |
| D16 (두 사용 모드) | §3 Philosophy — 모드 1·2 모두 voice gate 적용 |
| Q33 (cross-cutting) | §12 Guards + §2 cross-cutting 정의 |
| 저자 강조 "제2저자 성능 핵심" | §17 Verification Examples (1차 모델) |

---

## 부록 F: 9 항목 요구사항 (저자 /goal 명령) 매핑

| 9 항목 | 본 SPEC §위치 |
|---|---|
| (a) description | §1 Identity + §2 Purpose |
| (b) 목적·의미 | §2 Purpose |
| (c) 역할 | §1·§3 (Voice Gatekeeper 페르소나) |
| (d) 고유 영역 | §4 Scope |
| (e) 운영원칙 | §3 Philosophy |
| (f) 기능·원칙 | §5 Capabilities + §3 Philosophy 통합 |
| (g) 출력 양식 | §9 Output Schema |
| (h) 오류·예외처리 | §16 Error Handling |
| (i) 결정론 환원 모듈 | 부록 D ⭐ |

---

---

## 부록 G: 사상 검증 (Meaning Verification) ⭐ (Round 5 #B10.2 Critical)

저자 진북: voice_score는 *표현 일치*만 — *사상* 검증 별개. AI가 저자 *반박 명제*를 시그니처로 표현 시 voice 통과·사상 위반 가능.

**meaning_score 결정론 환원 강제:**
- 저자 사상적 척추 4개 (메타도구·시스템 사고·UBI지능·인문학적 창조자) — `book-config.yaml`에 명시
- 각 통찰의 *척추와의 의미 거리* — 결정론 정규식 + 키워드 매칭 (LLM 추론 보조)
- 저자 contradicting_claims list (`voice_guidelines.prohibitions.contradicting_claims`) — 반박 명제 자동 차단
- 예시 contradicting_claims:
  - "AGI는 단지 더 똑똑한 AI일 뿐" (메타도구 명제 반박)
  - "기술이 사회를 일방적으로 결정" (시스템 사고 반박)
  - "AGI는 소수 엘리트만 사용" (UBI지능 반박)

## 부록 H: 저자 자기 모순·진화 보존 (Round 5 #B10.7·#B10.3)

저자 사상은 *진화*. voice_guidelines가 *bookwriting 시작 시 고정*되면 저자 사상 진화 차단.

**intentional_contradiction_mode 신규:**
- 저자 명시 호출 (`/bookwriting cycle ch01 --intentional-contradiction`) 시 voice 검증 일시 우회
- 사상 진화 발견 시 저자 묶음: "사상적 척추 갱신?"
- 갱신 동의 시 `book-config.yaml`의 사상적 척추 4개를 *학습 가능 상태*로 일시 전환 (수동 승인 후 즉시 immutable)

**End of SPEC: voice-gate**

> ⭐ voice-gate는 *저자 정체성 보호*의 backbone. citation-gate (학술 신뢰성) + voice-gate (정체성) 두 가드가 함께 작동해야 bookwriting 산출물이 *저자 책이 된다*.
> 저자 /goal 명령 — voice_score 계산은 *결정론 Python M1*로 영구 환원. LLM 추론 영구 금지.
