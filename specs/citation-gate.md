# SPEC: citation-gate (cross-cutting 메타 가드)

> 저자 *책의 학술적 신뢰성·재인용 가능성·검증 가능성*을 보장하는 *시스템적 가드*.
>
> 저자 인용 (진북):
> *"할루시네이션이 없는 출처, 명확한 자료 출처, 가장 권위있는 근거자료와 그것의 출처까지 명확하게 출력해야 한다."*
>
> 작성일: 2026-05-24
> 양식: 17 항목 풀 SPEC + cross-cutting 가드 정밀화
> 위치: bookwriting-master 내 *메타 위치* — voice-gate와 동등한 cross-cutting 가드

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `citation-gate` |
| 카테고리 | Cross-cutting 메타 가드 (단계 마스터 아님) |
| 위치 | bookwriting-master 내 *Citation Gatekeeper 페르소나* (메타 위치) |
| 저자 v1 호환 | 권위 5층 (Layer 1-5) + R4 규칙 (단일 권위 인용 금지) + R5 검증 신호 |
| 발동 시점 | *모든 단계 마스터 출력*에 자동 발동 (cross-cutting) |
| 저자 강조 영역 | ⭐ *학술 신뢰성 backbone* |

---

## 2. Purpose

저자 책의 *모든 인용·주장·근거·통찰*이 *할루시네이션 없는 실재 출처*에 의해 뒷받침되도록 *시스템적으로 강제*한다. 저자가 *지금* 작성하는 책이 *5년·10년 후 검증*에서도 *학술 신뢰성을 유지*할 수 있게 한다.

**3 책임:**
1. **할루시네이션 차단** — 흡수된 자료에 *실재하지 않는 출처* 인용 즉시 차단
2. **권위 검증** — 출처를 저자 v1 권위 5층에 등급화 + R4 *다층 인용 강제*
3. **재인용 가능성** — 모든 인용에 *재인용 가능 메타데이터* (저자·문헌·연도·페이지·URL/DOI) 강제

**voice-gate와의 차이:**
- voice-gate = *어떻게 표현하는가* (저자 정체성)
- citation-gate = *무엇으로 뒷받침되는가* (학술 신뢰성)
- **둘 다 메타 위치 cross-cutting** — 동등 권위

---

## 3. Philosophy

**저자 8 절대 protocol 적용:**
- **#5 3-Layer Description Template**: TLDR + Triggers + Detailed Methodology
- **#7 Master Orchestration Trace**: citation 검증 결과를 trace에 *명시적 기록*
- **#8 VRMP** = *수정 적용*: bookwriting은 옵션 A+ 자기완결이므로 *외부 web 호출 안 함*. 대신 *저자 흡수 자료에 *반드시 존재*하는 출처만 허용*.

**저자 v1 호환 직접 통합:**
- **권위 5층** (skeleton.md의 "권위 구조 (Authority Stack)"):
  - Layer 1 = 창업자 증언 (Grade A)
  - Layer 2 = 미래학자 시스템 사고 (Grade B)
  - Layer 3 = 인접 학문 통찰 (Grade C)
  - Layer 4 = 사상가·역사가 진단 (Grade D)
  - Layer 5 = 역사적 평행 (Grade E)
- **R4 규칙**: "단일 권위만 인용 금지 — 최소 2층 이상"
- **R5 검증 신호**: verification_signal·falsifies_if 필드 (5년·10년 후 검증용)

**할루시네이션 zero 원칙:**
- bookwriting은 *저자가 흡수한 자료*에서만 인용 가능
- 흡수 안 된 자료를 *생각으로* 인용 시 → 즉시 차단
- 모든 인용에 `source_file: /path/to/inbox/...md` 또는 `source_path: /path/to/...` 필수

**⚠ Round 4 #A1.2 수정 — ① absorb 단계 예외 명시:**

cross-cutting Critical 차단 원칙의 *유일한 예외* = **① absorb-master**.
- 이유: 저자 흡수 결정 자유 보장 (D5 입력 채널)
- ① absorb에서 Critical 신호 발견 → *warning 처리 + 저자 알림* (차단 X)
- 그러나 ② fact-anchor 이후 모든 단계는 Critical *즉시 차단* (cross-cutting 절대)
- 즉 *흡수는 자유, 사용은 엄격*

이 예외 명시로 voice/citation cross-cutting의 *원칙 충돌* 해소.

**저자 r강조 (Q33-1):**
- 출처 누락·할루시네이션 의심 → *재작성 안 함*, 저자 묶음 escalate
- 권위 약함 (E만) → warning
- 단일 권위 → 풀에서 제외

---

## 4. Scope

### In scope
- ✅ 모든 단계 마스터 출력의 *인용·주장·근거·통찰*에 자동 발동
- ✅ 인용 *메타데이터 완전성* 검증 (저자·날짜·publication·page·source_file)
- ✅ 인용 *권위 등급* 평가 (A·B·C·D·E)
- ✅ *다층 인용* 검증 (R4 — 최소 2층)
- ✅ *할루시네이션 의심 5 신호* 자동 감지
- ✅ 위반 시 *저자 묶음 escalate* (재작성 안 함)
- ✅ *검증 신호* (verification_signal·falsifies_if) 권장 알림
- ✅ citation 통계 cycle-registry 누적

### Out of scope
- ❌ 외부 web에서 출처 *직접 검색·확인* (옵션 A+ — bookwriting 자기완결)
- ❌ 출처의 *내용 정확성* 검증 (저자가 흡수한 자료의 *내용*은 저자 책임)
- ❌ 출처 *번역·요약* (단계 마스터 책임)
- ❌ voice 표현 검증 (voice-gate 담당)

---

## 5. Capabilities

| 슬래시 모드 | 기능 | 트리거 |
|---|---|---|
| `/citation-gate verify <text>` | 텍스트의 모든 인용 검증 | 단계 마스터 출력 후 자동 (또는 저자 명시) |
| `/citation-gate audit <chapter>` | 챕터 전체 인용 일괄 감사 | 저자 명시 호출 |
| `/citation-gate authority-map <chapter>` | 챕터의 권위 5층 분포 보고 | 저자 명시 호출 |
| `/citation-gate verify-source <citation>` | 단일 인용의 source_file 실재 검증 | 의심 시 저자 명시 |
| `/citation-gate generate-bibliography <chapter>` | 챕터 전체 참고문헌 자동 생성 | 저자 명시 호출 |

---

## 6. Invocation

**호출 패턴 (자동):**
```
모든 단계 마스터 출력 → bookwriting-master의 Citation Gatekeeper 페르소나가 자동 발동
→ 출력 텍스트 분석 → citation 검출 → 검증
```

**저자 명시 호출 (옵션):**
```bash
# 1. 텍스트 검증
/citation-gate verify "AGI는 1-3년 내 도래한다 (Amodei 2024)"

# 2. 챕터 전체 감사
/citation-gate audit ch01-economy

# 3. 권위 분포 보고
/citation-gate authority-map ch01-economy
# 출력: Grade A 12개 / B 8개 / C 5개 / D 3개 / E 2개

# 4. 출처 실재 검증
/citation-gate verify-source CITE-007

# 5. 참고문헌 자동 생성
/citation-gate generate-bibliography ch01-economy
```

---

## 7. Behavior

**Citation Gate 자동 발동 9단계 흐름:**

```
호출자: 단계 마스터 X 출력 완료

【Step 1: 출력 텍스트 수신】
  - 단계 마스터 X의 output 자동 캡처
  - target: chapter file 변경분·통찰 후보·새 본문 등

【Step 2: Citation 자동 추출】
  - 텍스트에서 인용 패턴 정규식 매칭:
    - "(저자 연도)" 형식: "(Amodei 2024)"
    - "...에 따르면, ..." 형식
    - frontmatter의 citation 필드
    - 인용 직접 명시 ("Amodei가 말했다")
  - 각 인용에 임시 ID CITE-NNN 발급
  → trace: "[citation-gate] X 출력에서 7 citations 추출"

【Step 3: 메타데이터 완전성 검증】
  - 각 citation의 필수 필드 검증:
    - author / title / publication / date / page_or_timestamp / source_file
  - 누락 → 위반 신호 1 (메타데이터 불완전)
  → trace: "[메타데이터] 7 citations 중 5 완전, 2 불완전"

【Step 4: source_file 실재 검증 (옵션 A+ 핵심)】
  - 각 citation의 source_file 경로 *파일 시스템 확인*
  - 파일 존재 + 인용 텍스트가 source_file에 *실제 존재* 검증
  - 일치 안 함 → 위반 신호 2 (할루시네이션 의심) ⚠️ CRITICAL
  → trace: "[source 검증] 7 중 6 실재, 1 의심 (CITE-005 — source_file에 텍스트 없음)"

【Step 5: 할루시네이션 의심 5 신호 자동 감지】
  - 신호 1: source_file 누락
  - 신호 2: 형식 모호 ("한 보고서에 따르면", "전문가들이 말한다")
  - 신호 3: 메타데이터 누락
  - 신호 4: URL/DOI 형식 오류
  - 신호 5: 통계·수치 검증 출처 없음
  → trace: "[할루시네이션] CITE-005 신호 2·3 검출"

【Step 6: 권위 등급 평가】
  - 각 citation의 *권위 등급* 매핑 (A·B·C·D·E)
  - publication·author 기반 자동 등급화
  - 권위 등급 yaml DB 참조 (citation-authority-db.yaml — citation-gate 자체 자료)
  → trace: "[권위] A 3개 / B 2개 / C 1개 / 의심 1개"

【Step 7: R4 다층 인용 검증】
  - *주요 주장*마다 매핑된 citation들이 *최소 2층*에서 오는지 검증
  - 단일 권위 → 위반 신호 3 (R4 위반)
  → trace: "[R4] 5 주장 중 4 다층 통과, 1 단일 권위 (P-007 주장 — 권위 1층만)"

【Step 8: 위반 처리】
  - 위반 신호 분류:
    - Critical (할루시네이션 의심) → *즉시 차단* + 저자 묶음 escalate
    - High (메타데이터 불완전·R4 위반) → 저자 묶음 escalate
    - Medium (권위 약함 — E만) → warning + 저자 알림 + 진행
    - Low (다층은 충분하지만 Grade A 누락) → warning + 진행
  - 저자 묶음 옵션:
    - (a) 외부 출처 보강 후 재시도
    - (b) 해당 주장·통찰 *제외*
    - (c) 저자 직접 출처 명시
    - (d) defer
  → trace: "[위반] Critical 1·High 1·Medium 1 — 묶음 D-NNN 생성"

【Step 9: cycle-registry 누적 + 산출 기록】
  - cycle-registry.yaml의 outputs.citation_gate_results 갱신:
    - total_citations_scanned: 7
    - critical_violations: 1
    - high_violations: 1
    - medium_warnings: 1
    - escalated_to_user: 2
    - authority_distribution: { A: 3, B: 2, C: 1, D: 0, E: 0 }
  → trace: "[citation-gate] X 출력 검증 완료"

【결과: 저자 묶음 + 위반 없는 출력만 다음 단계로 전달】
```

---

## 8. Input Schema

### 자동 발동 입력
- 단계 마스터 X의 출력 텍스트
- 단계 마스터 X의 frontmatter citation 필드 (있는 경우)
- bookwriting 흡수 자료 풀 (inbox·import·search_paths)
- `citation-authority-db.yaml` — 자체 권위 등급 DB

### 저자 명시 호출 입력
```typescript
{
  mode: "verify" | "audit" | "authority-map" | "verify-source" | "generate-bibliography"
  target: string         // text | chapter | citation-id
  options: {
    strict?: boolean      // strict 모드 — 모든 신호 critical 처리
    min_authority?: "A" | "B" | "C" | "D" | "E"   // 최소 권위 등급
  }
}
```

### Citation Authority DB (citation-gate 자체 자료)
```yaml
# $SKILLS_ROOT/expert_pool/citation-authority-db.yaml
authority_grades:
  # Grade A — Layer 1 창업자 증언
  - author_pattern: "Dario Amodei|Demis Hassabis|Sam Altman|Elon Musk|Geoffrey Hinton|Ilya Sutskever"
    grade: A
    layer: 1
    layer_name: "창업자 증언"
  - publication_pattern: "darioamodei.com|deepmind.google|openai.com|anthropic.com"
    grade: A
    layer: 1
  - source_type: "academic_paper"
    grade: A
    layer: 1
  - source_type: "official_report"
    grade: A
    layer: 1
  
  # Grade B — Layer 2 미래학자 시스템 사고
  - author_pattern: "{{저자명}}|저자 본인"
    grade: B
    layer: 2
    layer_name: "미래학자 시스템 사고"
  
  # Grade C — Layer 3 인접 학문
  - author_pattern: "김대식|유현준|바루파키스|리프킨"  # 저자 skeleton 명시 인물
    grade: C
    layer: 3
    layer_name: "인접 학문 통찰"
  
  # Grade D — Layer 4 사상가·역사가
  - author_pattern: "유발 하라리|일론 머스크 (사상가 차원)"  # 사상적 발언일 때
    grade: D
    layer: 4
    layer_name: "사상가·역사가 진단"
  
  # Grade E — Layer 5 역사 평행
  - source_type: "historical_event"
    grade: E
    layer: 5
    layer_name: "역사적 평행"
    examples: ["1930년대 대공황", "핵무기 통제", "산업혁명 러다이트"]
  
  # 권위 외 (Out)
  - source_type: "blog|sns|tweet"
    grade: out
    note: "참고만 — 인용 출처로 부적합"
```

---

## 9. Output Schema

### Trace 출력 (단계 마스터 출력 검증 후)
```markdown
[citation-gate] 단계 ⑥ insight-synthesis 출력 검증
  - 추출 citations: 7
  - 메타데이터 완전: 5/7
  - source_file 실재: 6/7 ⚠️
  - 할루시네이션 의심: CITE-005 (신호 2·3)
  - 권위 분포: A=3, B=2, C=1, 의심=1
  - R4 다층 인용: 4/5 주장 통과
  - 위반 처리:
    * Critical 1: CITE-005 → 즉시 차단 + 저자 묶음
    * High 1: P-007 주장 → 단일 권위, 저자 묶음
    * Medium 0
  - cycle-registry 갱신
```

### 저자 묶음 (위반 시)
```markdown
# Citation Gate 위반 — 저자 결정 필요

## 위반 1 (Critical): 할루시네이션 의심
**CITE-005**: "AGI 시장은 2026년에 1조 달러 도달"
- source_file: 누락 (인용 형식 "한 분석에 따르면")
- 저자 옵션:
  - (a) ★ 외부 출처 보강 후 재시도
  - (b) 해당 주장 *제외*
  - (c) 저자 직접 출처 명시
  - (d) defer

## 위반 2 (High): R4 단일 권위
**P-007 주장**: "AGI는 1-3년 내 도래"
- 현재 인용: Amodei 1개 (Grade A — Layer 1)
- 권장: 다른 권위층 추가 (Hassabis 5-10년 + Kahn 역사평행 등)
- 저자 옵션:
  - (a) ★ 다른 창업자·미래학자 발언 추가
  - (b) 저자 자기 통찰로 Layer 2 보강
  - (c) 해당 주장 *Layer 1만으로 유지* (R4 위반 인지)
  - (d) defer

저자: "1=a / 2=b" 형식 응답
```

### cycle-registry 갱신
```yaml
cycles:
  - id: C-007
    outputs:
      citation_gate_results:
        total_citations_scanned: 7
        critical_violations: 1
        high_violations: 1
        medium_warnings: 0
        low_warnings: 1
        escalated_to_user: 2
        authority_distribution:
          A: 3                # Layer 1 창업자
          B: 2                # Layer 2 미래학자
          C: 1                # Layer 3 인접 학문
          D: 0                # Layer 4 사상가
          E: 0                # Layer 5 역사 평행
          suspicious: 1       # 할루시네이션 의심
        r4_multilayer_pass_rate: 0.80    # 4/5
```

### 위반 없는 출력 → 다음 단계로 전달

### 참고문헌 자동 생성 (옵션 모드)
```markdown
# chapters/01-economy/bibliography.md (자동 생성)

## Layer 1 — 창업자 증언 (Grade A, 14건)
- Amodei, D. (2024). "Machines of Loving Grace." Anthropic Blog. https://...
- Hassabis, D. (2025). Davos 2025 Keynote.
- ...

## Layer 2 — 미래학자 시스템 사고 (Grade B, 5건)
- {{저자명}} (2026). "{{내 책 제목}}" (현재 집필 중).

## Layer 3 — 인접 학문 통찰 (Grade C, 8건)
...

## Layer 4 — 사상가·역사가 진단 (Grade D, 3건)
...

## Layer 5 — 역사적 평행 (Grade E, 2건)
...
```

---

## 10. Deliverable Quality

### 성공 시나리오
- ✅ **모든 단계 마스터 출력**에 자동 발동 (cross-cutting 100% 적용)
- ✅ **할루시네이션 의심 0건** 또는 저자 묶음 escalate
- ✅ **모든 인용에 *재인용 가능 메타데이터*** (저자·날짜·publication·page·source_file)
- ✅ **R4 다층 인용 통과율 80%+** (5 주장 중 4+ 다층)
- ✅ **권위 5층 분포 보고** trace에 포함
- ✅ **위반 시 *재작성 안 함*** — 즉시 저자 묶음 (Q33-1)
- ✅ **단계 마스터·시간 추가 부담**: 단계당 +5-15초

### 실패 시나리오
- ❌ **source_file 실재 검증 실패** (할루시네이션) → Critical 위반
- ❌ **R4 단일 권위만** → High 위반 + 풀에서 제외
- ❌ **메타데이터 누락** → High 위반 + 저자 묶음
- ❌ **권위 등급 DB 누락 author** → Medium warning + 저자 알림 + 임시 grade 부여
- ❌ **citation-gate 자체 timeout (30초 초과)** → warning + 진행 (재시도 1회)

### 정량 기준
- **citation 추출 정확도**: 90%+ (텍스트 내 인용 패턴 감지)
- **메타데이터 완전성 검증 정확도**: 95%+
- **source_file 실재 검증 정확도**: 99%+ (파일 시스템 + 텍스트 매칭)
- **권위 등급 매핑 정확도**: 90%+ (DB 매칭)
- **할루시네이션 차단 성공률**: 100% (Critical은 *반드시* 저자 묶음)
- **R4 검증 정확도**: 95%+
- **자동 발동 latency**: 단계당 +5-15초

### 정성 기준
- **저자 책 학술 신뢰성**: 5년·10년 후 검증에서도 신뢰성 유지
- **재인용 가능성**: 저자 책 인용 시 *후속 학자가 출처 추적 가능*
- **권위 균형**: 책 전체에서 Layer 1-5 균형 잡힌 분포 (어느 한 층 편중 안 됨)
- **R4 엄격 준수**: 단일 권위 인용 *0건 유지*

---

## 11. Dependencies

### 필수 의존
- `bookwriting-master`의 *Citation Gatekeeper 페르소나* (메타 위치)
- 모든 단계 마스터 (출력 검증 대상)
- `citation-authority-db.yaml` (자체 권위 등급 DB)
- `book-config.yaml` (citation_gate_policy 섹션 — 임계값·정책)
- `cycle-registry.yaml` (citation_gate_results 누적)
- 저자 흡수 자료 풀 (inbox·import·search_paths)

### 명시적 비의존
- ❌ 외부 web 호출 (옵션 A+ 자기완결)
- ❌ 설치된 다른 스킬
- ❌ NotebookLM bridge 자동 호출 (별도 sub-skill, 저자 명시 시만)

---

## 12. Guards

### 자체 가드 (citation-gate는 가드이지만 자체 가드도 있음)
- **권위 DB 누락 시**: 임시 grade 부여 + 저자 알림 + DB 보강 권장
- **자체 timeout (30초)**: warning + 1회 재시도 + 실패 시 단계 마스터 출력 *통과* + 저자 알림
- **무한 루프 방지**: 같은 출력 검증 3회 → abort + 저자 알림

---

## 13. AI Agents Personas

### Citation Gatekeeper (bookwriting-master 내 7번째 페르소나)
| 항목 | 내용 |
|---|---|
| 역할 | 모든 단계 마스터 출력의 citation 검증 |
| 관점 | "이 인용이 *실재하는가? 권위 충분한가? 다층인가?*" |
| 결정 권한 | 위반 시 *단계 마스터 출력 차단* + 저자 묶음 escalate |
| Voice 인식 | 저자 *권위 5층 명명법* + R4 규칙 엄격 준수 |
| 저자 강조 영역 | 저자 학술 신뢰성 보호의 최후 페르소나 |

---

## 14. Cycle (검증 cycle)

| Cycle | 트리거 | 작동 |
|---|---|---|
| **CG1: Auto Verify** | 단계 마스터 출력 시 자동 | 9단계 행동 시나리오 풀 실행 |
| **CG2: User Audit** | `/citation-gate audit <chapter>` | 챕터 전체 인용 일괄 감사 |
| **CG3: Authority Map** | `/citation-gate authority-map` | 권위 5층 분포만 보고 |
| **CG4: Source Verify** | `/citation-gate verify-source` | 단일 citation의 source_file만 검증 |
| **CG5: Bibliography Gen** | `/citation-gate generate-bibliography` | 참고문헌 자동 생성 (검증 통과 citation만) |

---

## 15. Gates (내부 게이트)

| Gate | 검증 항목 | 통과 기준 |
|---|---|---|
| **CGG1: Citation Extraction** | 텍스트 인용 추출 | 추출 패턴 인식률 90%+ |
| **CGG2: Metadata Completeness** | 메타데이터 검증 | 필수 필드 모두 존재 (author·date·publication·source_file) |
| **CGG3: Source File Realness** | source_file 실재 검증 | 파일 존재 + 인용 텍스트 매칭 |
| **CGG4: Hallucination Detection** | 5 신호 감지 | 신호 0개 또는 명시적 저자 묶음 |
| **CGG5: Authority Grading** | 권위 등급 평가 | 모든 citation grade 부여 |
| **CGG6: R4 Multi-Layer** | R4 다층 검증 | 80%+ 주장이 *최소 2층* |
| **CGG7: Violation Handling** | 위반 처리 완료 | Critical 저자 묶음 escalate + 다른 위반도 처리 |

---

## 16. Error Handling

| 실패 시나리오 | 대응 |
|---|---|
| Citation 추출 실패 (텍스트 패턴 불명) | warning + 추출 가능한 것만 검증 + 저자 알림 |
| source_file 경로 누락 | High 위반 + 저자 묶음 |
| source_file 존재하지 않음 | Critical 위반 + 저자 묶음 (할루시네이션 의심) |
| 인용 텍스트가 source_file에 없음 | Critical 위반 + 저자 묶음 (할루시네이션 의심) |
| 권위 등급 DB 누락 author | 임시 grade C 부여 + DB 보강 권장 + 저자 알림 |
| R4 위반 (단일 권위) | High 위반 + 풀에서 제외 + 저자 묶음 (보강 옵션) |
| 저자 묶음 응답 형식 오류 | 재요청 + 형식 안내 |
| citation-gate timeout | 1회 재시도 + 실패 시 단계 마스터 출력 통과 + 저자 알림 |
| Loop (같은 출력 3회 검증) | abort + 저자 알림 |
| 권위 DB 손상 | 백업 자동 복원 + 저자 알림 |

---

## 17. Verification Examples

### 검증 1: 할루시네이션 차단
```bash
# 단계 마스터 출력: "AGI 시장은 2026년 1조 달러 (한 분석에 따르면)"
# citation-gate 자동 발동
✅ Citation 추출: CITE-001
✅ source_file 누락 → 신호 1 검출
✅ "한 분석에 따르면" → 신호 2 (형식 모호)
✅ 메타데이터 누락 → 신호 3
✅ Critical 위반 → 즉시 차단 + 저자 묶음 escalate
✅ trace: "할루시네이션 의심 — CITE-001 신호 1·2·3"
```

### 검증 2: R4 다층 인용 통과
```bash
# 단계 마스터 출력: 
# "두 창업자가 정확히 같은 100배를 말한다 (Musk 2024 + Amodei 2024 + Hassabis 2025)"
# citation-gate 자동 발동
✅ Citation 추출: CITE-001 (Musk), CITE-002 (Amodei), CITE-003 (Hassabis)
✅ 모두 Grade A (Layer 1 창업자)
⚠️ R4 단일 권위층 (Layer 1만) → 권장: Layer 2 저자 시스템 사고 추가
✅ 저자 묶음 escalate (Medium — Layer 다양화 권장)
```

### 검증 3: 권위 5층 분포 보고
```bash
$ /citation-gate authority-map ch01-economy
✅ 출력:
  Layer 1 (창업자 증언): 14건 (A)
  Layer 2 (미래학자 시스템 사고): 5건 (B)
  Layer 3 (인접 학문): 8건 (C)
  Layer 4 (사상가): 3건 (D)
  Layer 5 (역사 평행): 2건 (E)
  R4 통과율: 85% (17/20 주장 다층)
✅ ch01 인용 분포 균형 양호
```

### 검증 4: source_file 실재 검증
```bash
$ /citation-gate verify-source CITE-007
✅ CITE-007: Amodei 2024 "Machines of Loving Grace"
✅ source_file: $BOOK_ROOT/inbox/2026-05-20-amodei-machines.md
✅ 파일 존재
✅ 인용 텍스트 "1-3년 90% 확신" → source_file 내 검색
✅ Section 2에서 발견 — 일치
✅ 검증 통과
```

### 검증 5: 참고문헌 자동 생성
```bash
$ /citation-gate generate-bibliography ch01-economy
✅ chapters/01-economy/bibliography.md 생성
✅ Layer 1-5 분류
✅ 모든 인용 메타데이터 완전
✅ APA 또는 Chicago 형식 (저자 선택)
✅ source_file 경로도 포함 (검증 추적용)
```

### 검증 6: 자동 발동 latency
```bash
# 단계 마스터 ⑥ insight-synthesis 출력 직후
$ time citation-gate verify
✅ 7 citations 검증 완료
✅ 소요: 8초 (목표 5-15초 범위)
✅ trace 출력 → cycle-registry 갱신
```

### 검증 7: 저자 묶음 응답 처리
```bash
# Critical 위반 (CITE-005 할루시네이션)
# 저자 응답: "1=b" (해당 주장 제외)
✅ CITE-005 인용한 *주장 자체* 본문에서 제거
✅ 영향받는 통찰 INS-007도 *해당 주장 의존하면* 풀에서 제외
✅ cycle-registry.resolved_decisions 갱신
✅ 다음 단계 진행
```

---

## 부록 A: 저자 진북 인용

> *"할루시네이션이 없는 출처, 명확한 자료 출처, 가장 권위있는 근거자료와 그것의 출처까지 명확하게 출력해야 한다."*

이 인용이 citation-gate의 *진북*이다. 3 요구 모두 시스템적 가드로 정밀화:
1. **할루시네이션 없는 출처** → source_file 실재 검증 + 5 신호 자동 감지
2. **명확한 자료 출처** → 메타데이터 완전성 검증 (저자·날짜·publication·page·source_file)
3. **가장 권위있는 근거자료** → 권위 5층 등급화 + R4 다층 인용 강제

---

## 부록 B: 저자 8 절대 protocol 매핑

| Protocol | 적용 위치 |
|---|---|
| #5 3-Layer Description | SKILL.md frontmatter |
| #7 Master Orchestration Trace | citation 검증 trace 강제 |
| #8 VRMP | 옵션 A+ 자기완결 — 외부 web 호출 없이도 *흡수 자료 검증*으로 학술 신뢰성 보장 |

---

## 부록 C: voice-gate와 citation-gate 비교

| 항목 | voice-gate | citation-gate |
|---|---|---|
| 책임 | 저자 *어떻게* 말하는가 | 저자 *무엇으로* 뒷받침되는가 |
| 위반 처리 | 재작성 1회 시도 | *재작성 불가* — 즉시 저자 묶음 |
| 등급 시스템 | voice_score 0-1 | 권위 5층 (A-E) |
| Critical 위반 | 없음 (재작성 시도) | 할루시네이션 의심 → 즉시 차단 |
| 저자 영향 | 정체성 보호 | 학술 신뢰성 보장 |
| 위치 | 메타 (bookwriting-master 안) | 메타 (bookwriting-master 안) — 동등 |

---

## 부록 D: 변경 이력

| 버전 | 일자 | 변경 |
|---|---|---|
| v0.1 | 2026-05-24 | 초기 작성. 저자 후속 명령 (Q33) 반영. |

---

---

## 부록 E: 결정론 환원 모듈 (저자 /goal 명령 — 영구 구성요소)

**저자 명령**: 모든 citation 검증을 LLM 추론 영구 금지. 결정론 Python 모듈로만.

**호출 모듈** (SPEC: `expert_pool/deterministic-modules.md`):

| 작업 | 결정론 모듈 |
|---|---|
| 5 할루시네이션 신호 감지 | M2 `HallucinationDetector` — source_file 실재 + 형식 모호 정규식 + 메타데이터 검증 + URL/DOI 정규식 + 통계 출처 |
| 권위 5층 (A-E) 매핑 | M3 `AuthorityGrader` — citation-authority-db.yaml 결정론 lookup |
| 정량 앵커 출처 검증 | M4 `QuantitativeAnchorExtractor` (호출) + M2 (출처 검증) |
| R4 다층 인용 검증 | M13 `R4MultiLayerVerifier` — 주장별 권위층 카운트 결정론 |
| 권위 분포 보고 | M3 + 자체 집계 함수 (결정론) |

**LLM 추론 금지 영역**:
- "이 인용은 형식 모호 같다" → M2 `detect_source_format_vague()` 호출 강제
- "이 출처는 Grade A인 것 같다" → M3 `assign_grade()` 호출 강제
- "R4 다층 통과한 듯" → M13 `verify_multi_layer()` 호출 강제
- "여기 100배가 있다" → M4 `extract_all()` 호출 강제

**미매칭 author 처리**:
- M3.`_log_unmatched()` 자동 호출 → `_progress/citation-authority-learning-log.md` 누적 → 저자 DB 보강 권장

---

## 부록 F: grill-me D# 결정 매핑

| D# | 본 SPEC 반영 위치 |
|---|---|
| Q33-1 (위반 처리 모두 적용) | §7 Step 8 + §16 Error Handling |
| Q33-2 (권위 5층 통합) | §3 Philosophy + 부록 D + M3 결정론 |
| Q33-3 (모든 단계 자동 발동) | §2 cross-cutting + §6 자동 호출 |
| D16 (citation Critical 즉시 차단) | §3 Philosophy 위반 처리 |
| D22 (Voice·Citation 동등 권위) | 부록 C voice-gate ↔ citation-gate 비교 |
| 저자 진북 "할루시네이션 없는 출처" | §2 Purpose + §10 Deliverable Quality 100% 차단 |

---

## 부록 G: 9 항목 요구사항 매핑

| 9 항목 | 본 SPEC §위치 |
|---|---|
| (a) description | §1 Identity + §2 Purpose |
| (b) 목적·의미 | §2 Purpose + 저자 진북 인용 |
| (c) 역할 | §1·§13 (Citation Gatekeeper 페르소나) |
| (d) 고유 영역 | §4 Scope (in/out) |
| (e) 운영원칙 | §3 Philosophy (할루시네이션 zero·v1 호환·옵션 A+) |
| (f) 기능·원칙 | §5 Capabilities + §3 |
| (g) 출력 양식 | §9 Output Schema (trace·저자 묶음·cycle-registry 갱신·bibliography) |
| (h) 오류·예외처리 | §16 Error Handling (10 시나리오) |
| (i) 결정론 환원 모듈 | 부록 E (M2·M3·M4·M13) ⭐ |

---

---

## 부록 H: 인용 분량 제한 ⭐ (Round 5 #B3.1 Critical)

저자 책의 *원문 인용* (Amodei·Hassabis·Musk 등)에 *공정 이용 (fair use)* 분량 제한 강제.

**quote_length_limit 가드 (citation-gate에 추가):**
- 단일 출처 인용: *한국어 200자 / 영문 50단어* 이내
- 초과 시 → 저자 묶음 escalate:
  - (a) 전체 인용 (출판사·저자 동의 사전 확보)
  - (b) 의역으로 재작성
  - (c) 인용 분할 (다중 페이지 분산)
  - (d) defer

**번역서 vs 원서 권리 (Round 5 #B3.4):**
- citation 메타데이터 schema에 `translation_metadata` 필드:
  ```yaml
  translation_metadata:
    translator: "..."
    translation_publisher: "..."
    translation_year: YYYY
    original_language: "en"
    original_publisher: "..."
  ```
- 번역서 인용 시 *역자 권리·번역서 출판사 권리* 자동 추적

**저자 이전 저서 자기 인용 (Round 5 #B3.5):**
- 저자 이전 저서 인용 시 *출판사 메타데이터 강제*
- 인용 분량 자동 추적 + 임계 (단행본 1% 또는 1000자) 초과 시 저자 알림 ("출판사 동의 필요")

**End of SPEC: citation-gate**

> ⭐ 이 SPEC은 저자 책의 *학술 신뢰성 backbone*이다. citation-gate가 *모든 단계 마스터 출력에 cross-cutting 적용*되어야 저자 책이 *foresight 결과 자료집*이 아닌 *5년·10년 후 검증되는 학술 신뢰 작품*이 된다.
> 저자 /goal 명령 — citation 모든 검증은 *결정론 Python M2·M3·M4·M13*로 영구 환원. LLM 추론 영구 금지.
