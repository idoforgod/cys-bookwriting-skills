# SPEC: data-schema-voice-yaml (book-config.yaml의 voice_guidelines 섹션)

> 저자 voice의 *명시적 규칙*. cross-cutting voice gate의 *판단 기준*. 저자 *제2저자 성능 보장의 핵심*.
>
> 작성일: 2026-05-24
> 양식: 데이터 schema 전용 10 항목
> 위치: book-config.yaml의 `voice_guidelines:` 섹션 (별도 파일 아님 — book-config 내포)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| Schema 이름 | `voice-yaml` (book-config.yaml의 voice_guidelines 섹션) |
| 카테고리 | Data Schema (voice 규칙 정의) |
| 파일 위치 | `$BOOK_ROOT/master/book-config.yaml` 내 `voice_guidelines:` |
| 작성·갱신 주체 | 저자 (1차 명시 + 점진 보강) + bookwriting-master (자동 학습 + 저자 승인) |
| 저자 핵심 강조 영역 | ⭐ *제2저자 성능 보장의 backbone* |

---

## 2. Purpose

저자 *voice·통찰·문장 패턴·사상적 척추*를 *명시적 yaml 규칙*으로 정의한다. bookwriting의 *모든 단계 마스터 출력*이 *이 규칙에 통과*해야 저자 voice가 *80% 이상 일치*로 보장된다.

**저자 voice의 4겹 정의:**
1. **어휘 (vocabulary)** — 저자가 *자주 쓰는* 표현 + *회피하는* 표현
2. **문장 (sentence)** — 저자 문장의 *길이·태·구조 패턴*
3. **구조 (structure)** — 저자 단락·섹션의 *논리 골격*
4. **시그니처 (signature_expressions)** — 저자 *고유 패턴 문장*

**3겹 보호:**
- 저자 reference 풀 (NotebookLM 저자 저서 + Obsidian vault + skeleton.md) — *학습 자료*
- voice yaml — *명시 규칙*
- cross-cutting gate — *실시간 검증*

---

## 3. Scope

### In scope
- ✅ 저자 voice의 *명시 규칙 정의*
- ✅ voice 위반 *자동 감지 기준*
- ✅ voice 자동 학습된 규칙의 *yaml 누적*
- ✅ 저자 *시그니처 패턴* 보존

### Out of scope
- ❌ 저자 voice의 *학습 자료 텍스트* (reference 풀이 별도 — NotebookLM·Obsidian)
- ❌ voice 위반의 *처리 로직* (voice-gate.md의 책임)
- ❌ 저자 *통찰 자체* (insight-synthesis-master 담당)

---

## 4. Structure (필드 정의)

```yaml
# book-config.yaml의 voice_guidelines 섹션
voice_guidelines:
  
  # ───────────────────────────────────────────────────────
  # 1. 어휘 (vocabulary)
  # ───────────────────────────────────────────────────────
  vocabulary:
    preferred:                          # 저자가 자주·강력하게 쓰는 표현
      # 저자 미래학 핵심 개념
      - term: "메타 도구"
        context: "AGI 정의"
        usage_pattern: "노출 빈도 높음, 책 사상적 척추"
        related: ["인지 확장", "도구를 만드는 도구"]
      - term: "시스템 사고"
        context: "분석 방법론"
        usage_pattern: "단선적 인과 대신 사용"
        related: ["피드백 루프", "추동력", "약신호"]
      - term: "약신호"
        usage_pattern: "envscan 결과 인용 시"
      - term: "추동력"
        usage_pattern: "시스템 사고 변수 호명"
      - term: "수직 척추·수평 척추"
        usage_pattern: "책 구조 메타포"
      
      # 저자 고유 명제
      - term: "UBI(지능)"
        expansion: "Universal Basic Intelligence"
        context: "저자 야심찬 명제"
        usage_pattern: "UBI(소득) vs UHI(고소득) vs UBI(지능) 3단 대비"
      - term: "기술적 사춘기"
        source: "다리오 아모데이"
        usage_pattern: "현재 좌표 명명"
      - term: "부트로더"
        source: "일론 머스크"
        usage_pattern: "위협 메타포"
      - term: "사만다"
        source: "영화 Her"
        usage_pattern: "풍요 메타포"
      
      # 저자 권위 5층
      - term: "창업자 증언"
        usage_pattern: "권위층 1 — 가장 강력"
      - term: "미래학자의 시스템 사고"
        usage_pattern: "권위층 2 — 저자 척추"
      - term: "인접 학문의 통찰"
      - term: "사상가·역사가의 진단"
      - term: "역사적 평행"
    
    avoid:                              # 저자가 회피하는 표현
      - term: "AI가 일자리를 뺏는다"
        reason: "단선적 인과 — 저자는 시스템 사고로 분석"
        prefer_instead: "지능 대체 나선 (L1 시스템 루프)"
      - term: "기술 결정론적 표현"
        reason: "저자는 *정치 변수에 따라 결과가 갈리는 동일 시스템*을 강조"
      - term: "추상적 일반론"
        reason: "저자는 *구체적 시나리오·정량 앵커*를 반드시 동반"
      - term: "단일 권위 인용"
        reason: "저자 권위 5층 중 다층 인용 패턴"
      - term: "AI 시대가 도래했다"
        reason: "진부한 표현. 저자는 *2027 임계점·100배 스케일·90% 확신* 같은 정밀한 수치"
        added_by: system_learning        # 자동 학습된 항목
        added_at: 2026-05-30T10:15:00Z
        confirmed_by_user: true
  
  # ───────────────────────────────────────────────────────
  # 2. 문장 (sentence)
  # ───────────────────────────────────────────────────────
  sentence:
    max_length_chars: 80                # 저자 문장 최대 길이 기준
    avg_length_target: 50               # 평균 목표
    preference: "단문 + 능동태"
    avoid:
      - "중복 수식"
      - "과도한 종속절"
      - "수동태 남용"
      - "외국어 무분별 차용"
    
    rhythm:                             # 저자 문장 리듬
      - pattern: "짧은 명제 + 그 다음 풍부한 부연"
      - pattern: "수치 + 인용 + 사상적 해석 3박자"
      - pattern: "역사 평행 + 현재 좌표 + 미래 시점"
  
  # ───────────────────────────────────────────────────────
  # 3. 구조 (structure)
  # ───────────────────────────────────────────────────────
  structure:
    paragraph_pattern: "명제→근거→사례→통찰"
    
    section_pattern: "1층 콜드오픈→2층 분석→3층 함의"     # v1 chapter-pipeline 호환
    
    # ⚠ Round 4 #A2.1·#A7.5 수정 — target_percent 합 100 정합 강제
    layer_ratios:                       # 분량 비율 (v1 호환)
      narrative:                        # 1층 — 콜드오픈·서사
        target_percent: 13              # 12 → 13 (합 100 보장)
        range: [10, 15]
      analysis:                          # 2층 — 분석 본문
        target_percent: 65
        range: [60, 70]
      implications:                      # 3층 — 적용 함의
        target_percent: 22              # 20 → 22 (합 100 보장)
        range: [15, 25]
      # 수학 검증: 13 + 65 + 22 = 100 ✓
      # range 합 검증: min 10+60+15=85 / max 15+70+25=110 — *위반 시 정규화*
      _validation_rule: "narrative.target + analysis.target + implications.target == 100 강제"
      _normalization: "범위 외 분량 발견 시 ⑨ structure-review resize 자동 발동 (5% 범위)"
    
    chapter_role_layers:                # chapter_role별 권장 layer
      1층_콜드오픈: 1
      2층_분석: 2
      3층_함의: 3
    
    authority_stack:                    # 저자 권위 5층 (skeleton.md 호환)
      layer_1: "창업자 증언"
      layer_2: "미래학자의 시스템 사고"
      layer_3: "인접 학문의 통찰"
      layer_4: "사상가·역사가의 진단"
      layer_5: "역사적 평행"
      rule_R4: "단일 권위만 인용 금지 — 최소 2층 이상"
  
  # ───────────────────────────────────────────────────────
  # 4. 금지 (prohibitions)
  # ───────────────────────────────────────────────────────
  prohibitions:
    - id: PROH-001
      rule: "외국어 단어 무분별 사용 (한국어 우선)"
      example_violation: "AI agent의 capability를 framework로 분석"
      example_correction: "AI 에이전트의 능력을 프레임워크로 분석"
      severity: medium
    
    - id: PROH-002
      rule: "추상적 일반론 (구체적 시나리오 필수)"
      example_violation: "기술이 사회를 변화시킨다"
      example_correction: "2027년 다보스에서 아모데이가 90% 확신을 말한 날, 사회는 다음과 같이 변한다: [구체 시나리오]"
      severity: high
    
    - id: PROH-003
      rule: "단일 권위만 인용"
      example_violation: "머스크가 말했다 (이상 끝)"
      example_correction: "머스크·아모데이·하사비스 세 창업자가 정확히 같은 100배 스케일을 말한다"
      severity: high
    
    - id: PROH-004
      rule: "허위 인용·검증되지 않은 통계"
      example_violation: "한 보고서에 따르면 80%가..."  
      example_correction: "코슬라 벤처스 2024 보고서: '5년 내 화이트칼라 80% 대체'"
      severity: critical                  # voice gate 통과 안 함
    
    - id: PROH-005
      rule: "저자 voice와 어긋나는 *기성 AI 어투*"
      example_violation: "물론, 이는 매우 중요한 질문입니다."
      example_correction: "[구체 명제로 즉시 시작]"
      severity: high
  
  # ───────────────────────────────────────────────────────
  # 5. 시그니처 표현 (signature_expressions)
  # ───────────────────────────────────────────────────────
  signature_expressions:
    - pattern: "이 책은 X가 아니라 Y를 다룬다"
      examples:
        - "이 책은 AGI를 다루는 책이 아니다. AGI 이후의 인간을 다루는 책이다."
        - "이 책은 위협만 다루는 책이 아니라 위협과 풍요 사이의 응답을 다룬다."
      usage_context: "도입부·종장·챕터 첫 단락"
      frequency_target: "책 전체에서 5-10회 등장"
    
    - pattern: "셋 중 하나를 선택하는 것이 아니다"
      examples:
        - "기술적 사춘기를 통과해 부트로더가 되지 않고 사만다와 공진화하는 길을 설계하는 것이다"
      usage_context: "결론·종장"
    
    - pattern: "X와 Y 사이의 거리에서 시작한다"
      examples:
        - "이 책은 이 세 문장 사이의 거리에서 시작한다."
        - "기술 차원의 수직 이륙과 경제 차원의 소프트 테이크오프 사이의 시간차"
      usage_context: "서장·각 챕터 도입"
    
    - pattern: "두 창업자가 정확히 같은 N배를 말한다"
      examples:
        - "두 창업자가 정확히 같은 100배를 말한다"
      usage_context: "권위 수렴 강조"
    
    - pattern: "변수 X에 따라 결과가 갈리는 동일 시스템"
      examples:
        - "봉건제와 풍요는 정치 변수에 따라 결과가 갈리는 동일 시스템"
      usage_context: "시스템 사고 핵심 패턴"
  
  # ───────────────────────────────────────────────────────
  # 6. Voice gate 적용 정책
  # ───────────────────────────────────────────────────────
  gate_policy:
    apply_to_all_sub_skill_outputs: true   # 모든 단계 마스터 출력에 적용
    auto_retry_count: 1                     # 위반 시 1회 자동 재작성
    escalate_on_retry_failure: pending_decisions   # 재작성 실패 시 저자 묶음
    critical_severity_blocks: true          # PROH-004 critical은 *자동 통과 안 됨* (저자 검토 강제)
    voice_score_threshold: 0.7              # voice 일치도 70% 미만 시 재작성 트리거
  
  # ───────────────────────────────────────────────────────
  # 7. Reference 풀 (학습 자료 인덱스)
  # ───────────────────────────────────────────────────────
  reference_pool:
    notebooklm_notebooks:
      - notebook_id: "저자-저서-전체"     # 저자가 등록할 ID
        purpose: voice_pattern
        priority: 1
    obsidian_paths:
      - $REFERENCE_ROOT/저자_칼럼/
      - $REFERENCE_ROOT/저자_강의록/
    local_paths:
      - $BOOK_ROOT/bookidea/skeleton.md
        weight: 1.0                        # 저자 voice anchor (최고 가중치)
    voice_score_calculation:
      method: "weighted_similarity"
      weights:
        vocabulary_match: 0.30
        sentence_rhythm: 0.20
        structure_pattern: 0.20
        signature_presence: 0.15
        prohibition_avoidance: 0.15
  
  # ───────────────────────────────────────────────────────
  # 8. 점진적 학습 정책
  # ───────────────────────────────────────────────────────
  learning_policy:
    auto_learn_from_user_corrections: true   # 저자가 수정한 표현 자동 학습
    require_user_confirmation: true          # 학습된 항목 yaml 추가 전 저자 승인 필수
    learning_log_path: _progress/voice-learning-log.md
    learning_batch_threshold: 3              # 3개 학습 후보 누적 시 저자에게 묶음 제안
```

---

## 5. Validation Rules

| 필드 | 규칙 | 위반 시 |
|---|---|---|
| `vocabulary.preferred` | 최소 5개 권장 | 적으면 voice gate 약함 → 저자 보강 권장 |
| `vocabulary.avoid` | 형식: term + reason | reason 누락 시 저자 알림 |
| `sentence.max_length_chars` | 정수, 50-200 | 범위 외 → 기본값 80 |
| `structure.layer_ratios.*.range` | [min, max], min < max | 위반 시 자동 보정 |
| `structure.layer_ratios.*.range` 합계 | narrative + analysis + implications = 100 | 정규화 |
| `prohibitions[].severity` | enum [low·medium·high·critical] | enum 외 → medium |
| `prohibitions[].id` | 형식 PROH-NNN | 중복 자동 재발급 |
| `signature_expressions[].pattern` | 비어있지 않은 문자열 | 빈 값 → 항목 skip |
| `gate_policy.voice_score_threshold` | 0.0-1.0 float | 범위 외 → 기본 0.7 |
| `reference_pool.local_paths[].weight` | 0.0-1.0 | 범위 외 → 1.0 |
| `learning_policy.learning_batch_threshold` | 정수, 1-10 | 범위 외 → 3 |

---

## 6. Usage Examples

### 예시 1: 저자 최초 voice 명시 (하이브리드 — 시스템 추출 + 저자 검토)
```bash
# 저자: /bookwriting voice init
# bookwriting-master가 skeleton.md + Obsidian vault에서 자동 추출
$ ls $BOOK_ROOT/master/book-config.yaml
# voice_guidelines 섹션 초안 생성됨

# 저자가 직접 yaml 편집하여 보강
# 예: signature_expressions 추가
```

### 예시 2: 위반 자동 감지·재작성
```yaml
# 출력 검증: "AI 에이전트의 capability를 framework로 분석"
# PROH-001 위반 (외국어 무분별)
# voice-gate가 자동 재작성:
# 결과: "AI 에이전트의 능력을 프레임워크로 분석"
# voice_score: 0.85 → gate 통과
```

### 예시 3: 저자 묶음 escalation
```yaml
# 출력: "기술이 사회를 변화시킨다 (PROH-002 violation)"
# 자동 재작성 시도 → voice_score 0.55 → 실패
# bookwriting-master가 pending_decisions에 추가:
pending_decisions:
  - decision_id: D-009
    type: voice_violation_escalation
    phase: 7
    options:
      - id: a
        text: "[재작성안 1]: 2027년 다보스에서 아모데이가..."
        recommended: true
      - id: b
        text: "[재작성안 2]: 머스크의 수직 이륙과..."
        recommended: false
      - id: c
        text: "저자가 직접 작성"
```

### 예시 4: 점진적 학습
```yaml
# 저자가 사이클 중 "AI 시대가 도래했다"를 손수 "2027 임계점이 다가왔다"로 수정
# voice-gate가 학습 후보로 _progress/voice-learning-log.md에 기록
# 3개 후보 누적 시 저자에게 묶음 제안:
# "1=add_avoid:'AI 시대가 도래했다' / 2=add_preferred:'2027 임계점이 다가왔다'"
# 저자 승인 후 yaml 자동 갱신
```

### 예시 5: voice score 측정
```yaml
# 출력 텍스트의 voice_score 계산:
# - vocabulary_match: 0.85 (preferred 5개 사용, avoid 0개)
# - sentence_rhythm: 0.70 (평균 길이 60자, 능동태)
# - structure_pattern: 0.90 (명제→근거→사례 순)
# - signature_presence: 0.50 (시그니처 1개)
# - prohibition_avoidance: 1.0 (위반 0)
# Weighted: 0.30*0.85 + 0.20*0.70 + 0.20*0.90 + 0.15*0.50 + 0.15*1.0 = 0.81
# threshold 0.7 통과 ✅
```

---

## 7. Lifecycle

### 생성
- **시점**: book-config.yaml 최초 생성 시 voice_guidelines 섹션 *기본 템플릿* 포함
- **방법**: 저자가 직접 yaml 편집 + 시스템 자동 추출 보조 (하이브리드 Q19-D-1)
- **초기 자료**: skeleton.md의 저자 voice anchor + 저자 명시 보강

### 갱신
- **저자 수동 갱신**: vocabulary·signature_expressions·prohibitions 직접 추가
- **시스템 자동 학습**: 저자 사이클 수정 패턴에서 학습 → 저자 묶음 승인 후 yaml 자동 갱신
- **점진적 보강**: 사이클을 거치며 *위반 패턴*이 vocabulary.avoid에 누적

### 삭제
- **삭제 없음**: voice 규칙은 *영속 자산*
- **저자 수정 시**: 저자가 직접 yaml 편집

### 검증
- **시점**: bookwriting-master 모든 사이클의 G5 게이트 + voice-gate 발동 시
- **방법**: 모든 단계 출력의 voice_score 계산 → threshold 비교

---

## 8. Dependencies

### 이 schema를 *읽는* 스킬
- **voice-gate**: 모든 규칙 직접 사용 (vocabulary·sentence·structure·prohibitions·signature_expressions·gate_policy)
- **bookwriting-line-edit-master**: voice 일치 정밀 첨삭의 기준
- **bookwriting-narrative-craft-master**: signature_expressions 인용 패턴 채택
- **bookwriting-content-expand-master**: structure.paragraph_pattern·layer_ratios 기준

### 이 schema를 *쓰는* 스킬
- **bookwriting-master**: 학습 후보 자동 추가 (저자 승인 후)
- **voice-gate**: learning_log 누적 + 저자 승인 후 yaml 갱신

### 외부 참조
- **reference_pool**: NotebookLM bridge + Obsidian vault + skeleton.md
- **prohibitions**: 저자 v1 chapter-pipeline.md의 R4 규칙 호환

---

## 9. Error Handling

| 실패 시나리오 | 대응 |
|---|---|
| voice_guidelines 섹션 누락 | bookwriting-master abort + 저자에게 init 호출 권장 |
| vocabulary.preferred 빈 목록 | warning + voice gate 약함 표시 + 진행 |
| voice_score 계산 실패 (reference 풀 접근 불가) | warning + voice_score 0.5로 가정 + 진행 |
| 자동 재작성 실패 (1회 시도 후 score < threshold) | pending_decisions에 escalate |
| Critical 위반 (PROH-004 등) | *자동 통과 안 됨* + 저자 결정 필수 |
| 학습 후보 yaml 추가 실패 | learning_log에는 기록 + 다음 시도 |
| NotebookLM bridge 호출 실패 | voice_score 계산 시 *Obsidian + local 만으로 fallback* |
| signature_expressions 매칭 실패 | warning + signature_presence: 0.0 처리 |

---

## 10. Verification Examples

### 검증 1: 기본 생성·자동 추출
```bash
$ /bookwriting voice init
$ grep -c "preferred" book-config.yaml
✅ vocabulary.preferred 섹션 존재
$ grep -c "signature_expressions" book-config.yaml
✅ signature_expressions 존재 (최소 3개 patterns)
$ grep "skeleton.md" book-config.yaml
✅ reference_pool.local_paths에 skeleton 포함
```

### 검증 2: 위반 자동 감지
```bash
# 단계 마스터 출력: "AI agent의 capability를 framework로"
$ # voice-gate 호출 → PROH-001 검출
✅ voice_score < 0.7
✅ 1회 재작성 시도 발동
✅ 재작성 결과: "AI 에이전트의 능력을 프레임워크로"
✅ voice_score 0.7 이상 → 통과
```

### 검증 3: Critical 위반 차단
```bash
# 출력: "한 보고서에 따르면 80%가 변한다고 한다 (출처 미명시)"
$ # PROH-004 critical 검출
✅ 자동 통과 안 됨
✅ pending_decisions에 즉시 추가
✅ 저자 결정 필수 (재작성·저자 보강·skip 선택)
```

### 검증 4: 점진적 학습
```bash
# 저자가 3회 "AI 시대가 도래" → "2027 임계점이 다가옴" 수정
$ cat _progress/voice-learning-log.md
✅ 3 학습 후보 누적
$ # 저자에게 묶음 제안
✅ "1=add_avoid / 2=add_preferred"
# 저자 승인 후
$ grep "AI 시대가 도래" book-config.yaml
✅ vocabulary.avoid에 추가
$ grep "added_by: system_learning" book-config.yaml
✅ 자동 학습 표시 포함
```

### 검증 5: voice score 정량 측정
```bash
# 단계 마스터 출력 1:
# "AGI는 메타 도구다. 인지 자체를 확장하는 메타 도구. 머스크·아모데이·하사비스 세 창업자가 같은 100배를 말한다."
$ # voice_score 계산
✅ vocabulary_match: 0.95 (preferred 5+개 포함)
✅ sentence_rhythm: 0.85 (평균 35자 단문)
✅ structure_pattern: 0.80
✅ signature_presence: 0.70 ("세 창업자가 같은 N배" 시그니처)
✅ prohibition_avoidance: 1.0
✅ Weighted score: 0.85+ → 통과
```

### 검증 6: layer_ratios 준수
```bash
# 챕터 완성 후
$ wc -w chapters/01-economy/narrative.md analysis.md implications.md
✅ narrative: 14% (range 10-15 통과)
✅ analysis: 65% (range 60-70 통과)
✅ implications: 21% (range 15-25 통과)
```

---

**End of SPEC: data-schema-voice-yaml**

---

> ⭐ **이 SPEC의 가치**: 저자 voice는 *책의 정체성*이다. voice yaml이 정밀할수록 bookwriting의 제2저자 역할이 *저자 voice 유지*에 충실하다. 이 SPEC은 *후일 voice 누락·왜곡 발견 시* 저자가 *원본 의도를 확인하는 기준*이다.
