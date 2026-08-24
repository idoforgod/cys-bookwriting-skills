# SPEC: bookwriting-line-edit-master

> 저자 *제2저자 성능 핵심 4개 중 1개*. 저자 *voice·문장·표현* 정밀 첨삭의 최종 단계. 저자 책의 *문장 미시 품질 보장*.
>
> 작성일: 2026-05-24
> 매트릭스: 6 sub + 5 AI Agents + 4 Cycle + 3 Gate (Q18)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-line-edit-master` |
| 카테고리 | 단계 마스터 (⑩, MVP 수직 슬라이스 포함) |
| 저자 11 단계 매트릭스 위치 | ⑩ (제2저자 성능 핵심 4개 중 1개) |
| 저자 진짜 워크플로우 매핑 | **15단계 매력 글쓰기 — 문장 미시 첨삭** |
| 슬래시 | `/bookwriting-line-edit <mode> [target]` |
| 매트릭스 수치 | 6 sub + 5 AI Agents + 4 Cycle + 3 Gate |
| 시점 | 저자 lifecycle: 통찰 INSIGHTED → POLISHED 진입의 *최종 관문* |

---

## 2. Purpose

⑦ content-expand가 작성한 본문의 *문장 미시 차원*을 정밀 첨삭한다. 저자 voice·문장 길이·태·리듬·시그니처 패턴이 *모든 문장*에 정확히 적용되도록 한다. 시드 lifecycle을 *INSIGHTED → POLISHED*로 진행시키는 *최종 관문*.

**3 책임:**
1. **문장 미시 첨삭** — 어색·중복·수동태·외국어 무분별 자동 수정
2. **저자 voice 정밀 보존** — voice_score 0.85+ 도달 (일반 단계는 0.7+)
3. **시그니처 패턴 정밀 적용** — 활용 가능한 곳에 저자 5 시그니처 패턴 적용

---

## 3. Philosophy

**저자 v1 *yoon-writing-style* (계획됨·미구현)을 v2에서 완성.**

**voice-gate와의 협업:**
- voice-gate는 *cross-cutting 자동 발동* (모든 단계 출력)
- ⑩ line-edit은 *전용 단계* — 단계 마스터 출력 통과 후에도 *추가 정밀 첨삭*
- 두 가드의 *임계값 차이*: cross-cutting voice gate는 0.7, ⑩ line-edit은 0.85+ 도달

---

## 4. Scope

### In scope
- ✅ 모든 layer 본문 (narrative·analysis·implications)의 문장 첨삭
- ✅ 저자 voice 정밀 (preferred·avoid·prohibitions 엄격)
- ✅ 시그니처 패턴 정밀 적용 (5 패턴 활용 기회 발견·치환)
- ✅ 저자 문장 리듬·길이·태 보존
- ✅ 외국어 무분별 자동 한국어 치환
- ✅ AI 어투 자동 감지·제거
- ✅ 시드 lifecycle INSIGHTED → POLISHED 진행

### Out of scope
- ❌ 통찰 *내용 변경* (⑥ insight-synthesis 담당)
- ❌ 분량 확장·축소 (⑦ content-expand 담당)
- ❌ 구조 변경 (⑨ structure-review 담당)
- ❌ 출처·인용 검증 (citation-gate 담당)

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-line-edit cycle <target>` | 풀 첨삭 사이클 |
| `/bookwriting-line-edit voice <text>` | 단일 텍스트 voice 첨삭 |
| `/bookwriting-line-edit signature-apply <chapter>` | 시그니처 패턴 적용 기회 발견·치환 |
| `/bookwriting-line-edit ai-tone-purge <chapter>` | AI 어투 일괄 제거 |

---

## 6. Invocation

```bash
/bookwriting-line-edit cycle ch01-economy           # 풀 첨삭
/bookwriting-line-edit cycle ch01-economy/analysis.md   # 단일 파일
/bookwriting-line-edit signature-apply ch01-economy     # 시그니처만
```

---

## 7. Behavior

**9단계 행동 시나리오:**

```
호출: /bookwriting-line-edit cycle ch01-economy

【Step 1: 입력 검증·자료 로드】
  - ch01의 narrative/analysis/implications.md 모두 읽기
  - book-config의 voice_guidelines 전체 로드
  - voice-gate가 *이미 통과*시킨 본문이지만 *추가 정밀 첨삭* 진행

【Step 2: 어휘 정밀 검토 (Vocabulary Refiner 페르소나)】
  - 모든 문장에서 *avoid·prohibitions* 위반 재검토 (cross-cutting gate보다 엄격)
  - preferred 어휘 *치환 기회* 발견
  - 외국어 → 한국어 치환

【Step 3: 문장 리듬 정밀화 (Sentence Rhythm Tuner 페르소나)】
  - 저자 평균 문장 길이 50자·max 80자 준수
  - 중복 수식·과도한 종속절 자동 분해
  - 수동태 → 능동태 전환

【Step 4: 시그니처 패턴 적용 (Signature Applier 페르소나)】
  - 5 시그니처 패턴 적용 가능한 곳 모두 발견
  - 활용률 30%+ 목표 (이미 활용된 곳 + 추가 활용)
  - 시그니처 패턴 자연스러운 곳에만 적용 (강제 X)

【Step 5: AI 어투 제거 (AI Tone Purger 페르소나)】
  - "물론, 이는 매우 중요한 질문입니다" 등 AI 패턴 자동 감지
  - 저자 voice로 자연 치환
  - PROH-005 (AI 어투) 위반 0건 목표

【Step 6: 저자 voice 정밀 확인 (Voice Validator 페르소나)】
  - voice_score 재계산
  - 목표: 0.85+ (cross-cutting 0.7보다 엄격)
  - 미달 시 추가 첨삭

【Step 7: Voice·Citation gate 재발동】
  - cross-cutting gate 다시 확인
  - 첨삭 결과가 위반 없음 확인

【Step 8: 저자 묶음 (모드 1) — 첨삭 결과 채택】
  - before·after diff 제시
  - 저자가 *수용·거부·일부 수정* 결정

【Step 9: 본문 저장 + lifecycle POLISHED】
  - chapter 파일 갱신
  - 시드 lifecycle INSIGHTED → POLISHED
  - 시드 progress.voice_violations_resolved 갱신
```

---

## 8. Input Schema

```typescript
{
  mode: "cycle" | "voice" | "signature-apply" | "ai-tone-purge"
  target: string         // ch-NNN | path/to/file.md | text
  options: {
    strict_threshold?: number  // 0.85 기본 (cross-cutting 0.7보다 엄격)
    preserve_diff?: boolean    // before·after 보존
  }
}
```

---

## 9. Output Schema

### 저자 화면 (모드 1)
```markdown
# ⑩ line-edit — ch01-economy

## 첨삭 묶음 1: 어휘 치환 (12 변경)

### (a) ★ 외국어 한국어 치환 (8건)
- "framework" → "프레임워크" (5건)
- "agent" → "에이전트" (3건)

### (b) ★ AI 어투 제거 (3건)
- "물론, 이는 매우 중요한 질문입니다" → "이 질문이 책의 핵심을 가른다"
- ...

### (c) preferred 어휘 추가 (1건)
- "확장한다" → "메타도구로 확장한다" (메타도구 시그니처 강화)

저자: "1=a,b / 2=c" 또는 자연어

## 첨삭 묶음 2: 문장 리듬 (5 변경)
...

## 첨삭 묶음 3: 시그니처 패턴 (3 적용)
- (a) 새 문장에 "X가 아니라 Y" 적용 가능
- (b) "셋 중 하나가 아니다" 결론 부분에
- (c) ...
```

### 파일 갱신
- chapter `*.md` 갱신 (first-version backup with `.before` suffix optional)
- seed-registry lifecycle POLISHED
- cycle-registry outputs 갱신

---

## 10. Deliverable Quality

### 정량 기준
- **voice_score 0.85+** (모든 본문) — strict
- **시그니처 활용률 35%+** (cross-cutting 30%보다 엄격)
- **PROH-001~005 위반 0건** 목표 (cross-cutting은 자동 재작성 후 100% 보장)
- **외국어 무분별 0건**
- **AI 어투 0건** (PROH-005)
- **평균 문장 길이 50자**
- **수동태 비율 < 10%**

### 정성 기준
- 저자 본인 *육성으로 읽힘*
- 문장 *흐름이 저자 리듬*
- 시그니처 패턴이 *자연스럽게* 등장 (억지 X)
- AI 어투 *완전 제거*

---

## 11. Dependencies

### 필수
- ⑦ content-expand 통과 (확장 본문 있음)
- voice-gate (cross-cutting — 임계값 차이만)
- book-config voice_guidelines

### 후속
- 저자 *최종 감수* (인간)

### 비의존
- 설치된 다른 스킬

---

## 12. Guards

### Voice gate (cross-cutting) — 자동 발동
### Citation gate (cross-cutting) — 자동 발동
### Strict Voice Threshold (⑩ 전용)
- ⑩ line-edit 통과 임계값: 0.85+ (일반 0.7보다 엄격)
- 미달 시 추가 첨삭 시도 (최대 2회)
- 실패 시 저자 묶음

### 시그니처 활용률 가드
- 35%+ 목표 (cross-cutting 30%보다 엄격)
- 미달 시 시그니처 적용 기회 추가 발견

### Diff 보존 가드
- before·after diff 자동 보존 (`.before` 백업 또는 cycle-registry)
- 저자가 원복 가능

---

## 13. AI Agents Personas (5명)

| # | 페르소나 | 역할 |
|---|---|---|
| 1 | **Vocabulary Refiner** | preferred 치환·avoid 회피·외국어 한국어 치환 |
| 2 | **Sentence Rhythm Tuner** | 저자 문장 길이·태·리듬 정밀화 |
| 3 | **Signature Applier ⭐** | 5 시그니처 패턴 적용 기회 발견·치환 |
| 4 | **AI Tone Purger ⭐** | AI 어투 (PROH-005) 자동 감지·제거 |
| 5 | **Voice Validator** | voice_score 재계산·0.85+ 검증 |

---

## 14. Cycle

| Cycle | 트리거 | 작동 |
|---|---|---|
| **C1: Chapter Full Edit** | `cycle ch-NNN` | 챕터 전체 첨삭 |
| **C2: Single File Edit** | `cycle <path>` | 단일 파일 |
| **C3: Signature Apply Only** | `signature-apply` | 시그니처만 |
| **C4: AI Tone Purge Only** | `ai-tone-purge` | AI 어투만 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| **G1: Input** | content-expand 통과한 본문 존재 |
| **G2: Strict Voice** | voice_score 0.85+ |
| **G3: Signature·AI Tone** | 활용률 35%+ + AI 어투 0건 |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| voice_score 추가 첨삭 후에도 0.85 미달 | 저자 묶음 escalate + before·after diff 제시 |
| 시그니처 적용 자연스럽지 않음 | 해당 적용 skip + 다음 기회 발견 |
| AI 어투 패턴 누적 (10건+) | 저자 알림 — ⑦ content-expand 재호출 권장 |
| diff 백업 실패 | warning + 메모리 보존 + 저자 알림 |

---

## 17. Verification Examples

### 검증 1: 챕터 풀 첨삭
```bash
/bookwriting-line-edit cycle ch01-economy
✅ voice_score 0.74 → 0.88 (strict 임계 통과)
✅ 시그니처 활용률 32% → 38%
✅ AI 어투 8건 → 0건
✅ 외국어 14건 → 0건
✅ 5 INSIGHTED 시드 → POLISHED 진행
✅ chapters/01-economy/*.md 갱신
✅ diff `.before` 백업
```

### 검증 2: AI 어투 제거
```bash
# 전: "물론, 이 통찰은 매우 중요합니다. 다음과 같이 살펴볼 수 있습니다."
# 후: "이 통찰이 책의 핵심을 가른다."
✅ PROH-005 위반 1건 해소
✅ voice_score +0.12
```

### 검증 3: 시그니처 적용
```bash
# 본문: "AGI는 도구다. 인지를 확장한다."
# 시그니처 적용: "AGI는 도구가 아니다. *모든 도구를 만드는 도구* — 메타도구다."
✅ "X가 아니라 Y" 시그니처 적용
✅ voice_score +0.18
```

### 검증 4: 외국어 치환
```bash
# 전: "AI agent의 capability를 framework로 분석"
# 후: "AI 에이전트의 능력을 프레임워크로 분석"
✅ PROH-001 위반 1건 해소
✅ 저자 voice 일치
```

### 검증 5: 저자 묶음 응답·일부 거부
```bash
# 첨삭 묶음 12건 제시
# 저자 응답: "1=a,b / 2=skip" (2번 묶음 거부)
✅ 1번 채택 → 본문 갱신
✅ 2번 미채택 → 원본 유지 + 학습 후보 등록
```

### 검증 6: lifecycle POLISHED 진행
```bash
$ grep -A2 "id: S-001" seed-registry.yaml | grep "lifecycle:"
✅ "lifecycle: POLISHED"   # INSIGHTED → POLISHED
✅ progress.voice_violations_resolved 갱신
```

---

## 부록: voice-gate cross-cutting과 ⑩ line-edit 분리 이유

**왜 둘 다 필요한가?**
- voice-gate (cross-cutting) = 모든 단계 마스터 출력에 자동, *임계값 0.7*
- ⑩ line-edit (전용 단계) = 사이클 끝에 추가 정밀 첨삭, *임계값 0.85+*

**비유**: voice-gate는 *교정자의 1차 검토*, ⑩ line-edit은 *편집자의 최종 첨삭*. 둘 다 필요.

---

---

## 부록: 결정론 모듈·grill-me·9 항목·Mode 2·R1-R5

### 결정론 모듈
| 작업 | 모듈 |
|---|---|
| 어휘 치환 (preferred·avoid·외국어) | M1 VoiceScorer.compute_vocabulary_match + 자체 substitute 함수 |
| 시그니처 패턴 적용 | M8 signature_pattern_applier (35%+ strict 임계) |
| AI 어투 감지·치환 | M9 ai_tone_purger (PROH-005 정규식) |
| voice_score strict 0.85+ | M1 VoiceScorer (strict 모드) |
| 시드 lifecycle INSIGHTED → POLISHED | M11 lifecycle_state_machine |
| diff 보존 (`.before` 백업) | 자체 결정론 파일 IO |

**LLM 추론 금지**: voice_score 자체 추측·시그니처 매칭 직접·AI 어투 "이건 AI 어투" 추측.

### grill-me D# 매핑
| D# | §위치 |
|---|---|
| D22 (Voice 보존 완전체) | §2 + cross-cutting |
| D11 (시그니처 strict 적용) | §7 Step 4 (signature-applier sub) + 부록 결정론 M8 |
| 저자 강조 "제2저자 핵심" | §1 카테고리 + §10 strict 임계 |
| Q33 (citation gate cross-cutting) | §12 |

### 9 항목
(a) §1+§2 / (b) §2 (15단계 매력 글쓰기 — 문장 미시) / (c) §13 5 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록 ⭐

### Mode 2 자동
모드 2: AI 어투 자동 제거·시그니처 자동 적용·voice_score 0.85+ 실패 시도 *trace 기록만* (escalate 안 함)·diff 보존 미발동.

### R1-R5 적용
| R1·R2·R3·R4·R5 모두 보존 — line-edit가 원본 R 적합성 변경 X. 출력 후 *재검증* 강제. |

**End of SPEC: bookwriting-line-edit-master**

> ⭐ ⑩ line-edit은 저자 책의 *문장 미시 품질 마지막 관문*. voice·시그니처·AI 어투 제거가 *완벽 수준*에 도달해야 시드 lifecycle POLISHED 진입.
