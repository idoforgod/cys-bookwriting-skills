# SPEC: data-schema-book-config.yaml

> bookwriting의 *최상위 단일 진실 공급원*. 검색 경로·voice 가이드라인·매크로 트리거·외부 도구 통합을 *한 yaml 파일*에 명시.
>
> 작성일: 2026-05-24
> 양식: 데이터 schema 전용 10 항목

---

## 1. Identity

| 항목 | 값 |
|---|---|
| Schema 이름 | `book-config.yaml` |
| 카테고리 | Data Schema (최상위 설정 파일) |
| 파일 위치 | `$BOOK_ROOT/master/book-config.yaml` |
| 작성 주체 | 저자 (초안 = 시스템 자동 생성 + 저자 검토) |
| 갱신 주체 | 저자 (수동) + bookwriting-master (일부 자동 — voice 가이드라인 점진 보강) |

---

## 2. Purpose

bookwriting의 *모든 행동을 결정하는 설정*을 *한 곳에 집약*한다. 저자가 *이 한 파일만 보면* 시스템 행동을 *완전히 파악·제어* 가능하다.

**5대 설정 영역:**
1. **search_paths** — bookwriting 자체 검색이 접근할 디렉토리 (옵션 A+ 자기완결 원칙)
2. **exclude_patterns** — 검색 차단 패턴 (민감 정보 보호)
3. **voice_guidelines** — 저자 voice 명시적 규칙 (cross-cutting gate의 기준)
4. **cycle_triggers** — 매크로 자동 발동 임계값
5. **bridges** — NotebookLM 등 외부 도구 통합 옵션

---

## 3. Scope

### In scope
- ✅ bookwriting의 *모든 사이클·단계 마스터*가 읽는 설정
- ✅ 저자가 *수동 편집*해서 시스템 행동 조정 가능
- ✅ voice 가이드라인의 *점진적 보강* (자동 추가 + 저자 승인)

### Out of scope
- ❌ 시드 데이터 (seed-registry.yaml 담당)
- ❌ 사이클 상태 (cycle-registry.yaml 담당)
- ❌ 예측 데이터 (forecast-registry.yaml — v1)
- ❌ 챕터 작업물 (chapters/<ch>/* 담당)

---

## 4. Structure (필드 정의)

```yaml
# $BOOK_ROOT/master/book-config.yaml

version: "2.0"                          # schema 버전
project_name: "{{내 책 제목}}"  # 책 제목 (1단계 = AGI 단행본)
created: "2026-05-24"
last_updated: "2026-05-24"

# ───────────────────────────────────────────────────────
# 1. 검색 경로 (옵션 B + Obsidian + NotebookLM bridge)
# ───────────────────────────────────────────────────────
search_paths:
  tier_1_always:                        # 항상 검색
    - $BOOK_ROOT/
  
  tier_2_explicit:                      # 저자 명시 등록
    - $REFERENCE_ROOT/    # Obsidian vault (다수 파일)
    - $REFERENCE_ROOT/foresight-notes/
    - $REFERENCE_ROOT/lecture-notes/
    - $REFERENCE_ROOT/coaching-notes/
    # 저자가 후일 추가:
    # - ~/[강의록 경로]/
    # - ~/[이전저서 경로]/

# ───────────────────────────────────────────────────────
# 2. 검색 차단 패턴 (민감 정보 보호)
# ───────────────────────────────────────────────────────
exclude_patterns:
  # ⚠ Round 4 #A5.1 Critical 수정 — 보안 가드 강화
  # 자격·토큰·키 (확장)
  - "*credentials*"
  - "*.env*"
  - "*secret*"
  - "*token*"
  - "*tokens.json"            # Round 4 #A5.3 — MCP 인증 토큰
  - "*auth_tokens*"
  - "*.token"
  - "*oauth*"
  - "*api_key*"
  - "*private*"
  # SSH·SSL·GPG 키
  - ".ssh/*"                  # Round 4 #A5.1
  - "id_rsa*"
  - "id_ed25519*"
  - "id_dsa*"
  - "id_ecdsa*"
  - "*.pem"
  - "*.key"
  - "*.crt"
  - "*.cer"
  - "*.pfx"
  - "*.p12"
  - ".gnupg/*"
  - "*.gpg"
  # 클라우드 자격
  - ".aws/*"
  - ".azure/*"
  - ".docker/*"
  - ".netrc"
  # 비밀번호 관리자
  - "*.kdbx"
  - "*.1password*"
  # 일반
  - "*.git/*"
  - "*.DS_Store"
  - "*__pycache__*"
  - "*node_modules*"
  - "*.pyc"
  # 저자 추가 민감 영역 (자유 추가):
  # - "*개인_재정*"
  # - "*가족*"
  # - "*상담_기록*"

# ───────────────────────────────────────────────────────
# 3. Voice 가이드라인 (cross-cutting gate 기준)
# ───────────────────────────────────────────────────────
voice_guidelines:
  vocabulary:
    preferred:                          # 저자가 자주 쓰는 표현
      - "메타 도구"
      - "시스템 사고"
      - "약신호"
      - "추동력"
      - "수직 척추·수평 척추"
      - "UBI(지능)"
      - "기술적 사춘기"
      - "부트로더·사만다"
      # 저자가 추가...
    avoid:                              # 저자가 회피하는 표현
      - "AI가 일자리를 뺏는다"          # 단선적 인과
      - "기술 결정론적 표현"
      - "추상적 일반론"
      # ...
  
  sentence:
    max_length_chars: 80                # 저자 문장 길이 기준
    preference: "단문 + 능동태"
    avoid: ["중복 수식", "과도한 종속절"]
  
  structure:
    paragraph_pattern: "명제→근거→사례→통찰"
    section_pattern: "1층 콜드오픈→2층 분석→3층 함의"   # v1 chapter-pipeline 호환
    layer_ratios:                        # v1 호환
      narrative: [10, 15]                # 10-15%
      analysis: [60, 70]
      implications: [15, 25]
  
  prohibitions:
    - "외국어 단어 무분별 사용 (한국어 우선)"
    - "추상적 일반론 (구체적 시나리오 필수)"
    - "단일 권위만 인용 (다층 권위 v15 패턴 강제)"
    - "허위 인용·검증되지 않은 통계"
  
  signature_expressions:                # 저자 시그니처 패턴
    - "이 책은 X가 아니라 Y를 다룬다"
    - "셋 중 하나를 선택하는 것이 아니다"
    - "X와 Y 사이의 거리에서 시작한다"
    - "두 창업자가 정확히 같은 N배를 말한다"

# ───────────────────────────────────────────────────────
# 4. Cycle 매크로 트리거 (Q16-DE-1 — 빈도 + 상태 둘 다)
# ───────────────────────────────────────────────────────
cycle_triggers:
  micro_count_for_relink:           5    # 마이크로 사이클 5회 → ⑪ relink 권장
  micro_count_for_structure_review: 10   # 마이크로 10회 → ⑨ structure 권장
  evidenced_count_for_insight:      5    # EVIDENCED 시드 5개 → ⑥ insight-synthesis 권장
  polished_ratio_for_structure:     0.8  # POLISHED 비율 80% → ⑨ structure 권장
  concurrent_cycle_soft_limit:      5    # 동시 사이클 5개 소프트 제한
  registry_archive_threshold:       100  # cycle-registry 100개 초과 시 archive

# ───────────────────────────────────────────────────────
# 4.5. Citation Gate 정책 ⭐ (저자 Q33 후속 명령)
# ───────────────────────────────────────────────────────
citation_gate_policy:
  enabled: true                          # 항상 true (저자 명시 강제)
  apply_to_all_sub_skill_outputs: true   # cross-cutting 모든 단계 마스터 출력
  
  # 권위 5층 등급 시스템 (Q33-2 d — 저자 v1 권위 5층 통합)
  # ⚠ Round 9 #E2.1 Critical — Python enum (deterministic-modules M3 Grade enum)과 3중 정합 강제
  authority_grades:
    A: "창업자 증언·peer-reviewed 논문 (Layer 1)"
    A_preprint: "preprint (arxiv 등 peer-review 전, Round 8 #D2.2 추가)"
    B: "미래학자 시스템 사고 (Layer 2 — 저자 본인)"
    C: "인접 학문 통찰 (Layer 3)"
    D: "사상가·역사가 진단 (Layer 4)"
    E: "역사적 평행 (Layer 5)"
    F: "신학 권위 (Layer 6, Round 7 #C2.4 추가)"
  
  # 위반 처리 정책 (Q33-1 — 모두 적용)
  violation_handling:
    hallucination_critical:              # 출처 누락·source_file 실재 안 함
      action: escalate_to_user_immediately
      retry: false                        # 재작성 안 함 (없는 출처 만들 수 없음)
    metadata_incomplete_high:             # 메타데이터 누락
      action: escalate_to_user
      retry: false
    r4_single_authority_high:             # 단일 권위만 매핑
      action: exclude_from_pool
      retry: false
    weak_authority_medium:                # Grade E만
      action: warning_and_continue
      retry: false
    
  # 할루시네이션 의심 5 신호 (citation-gate.md 참조)
  hallucination_signals:
    - source_file_missing
    - source_format_vague          # "한 보고서에 따르면" 등
    - metadata_missing             # 저자·날짜·publication 누락
    - url_doi_invalid              # URL/DOI 형식 오류
    - stat_no_source               # 통계·수치에 검증 출처 없음
  
  # R4 다층 인용 강제 (저자 v1 호환)
  r4_min_layers: 2                  # 최소 2층
  
  # Citation Authority DB 위치
  authority_db_path: $SKILLS_ROOT/expert_pool/citation-authority-db.yaml

# ───────────────────────────────────────────────────────
# 5. 외부 도구 통합 (옵션 D — 별도 sub-skill bridge)
# ───────────────────────────────────────────────────────
bridges:
  notebooklm:
    enabled: true
    sub_skill: bookwriting-notebooklm-bridge
    auth_status: "저자 nlm login 완료 확인 필요"
    notebooks:
      # 저자가 채워야 할 항목:
      # - notebook_id: "저자-저서-전체"
      #   purpose: voice_reference
      # - notebook_id: "AGI-책-자료"
      #   purpose: evidence_source

# ───────────────────────────────────────────────────────
# 6. v1 호환 (모듈 통합)
# ───────────────────────────────────────────────────────
v1_compatibility:
  forecast_registry_path: $BOOK_ROOT/master/forecast-registry.yaml
  chapter_pipeline_path: $BOOK_ROOT/workflows/book-planning.md
  skeleton_path: $BOOK_ROOT/bookidea/skeleton.md
  use_v1_six_file_schema: true
  use_v1_three_layer_structure: true

# ───────────────────────────────────────────────────────
# 7. 백업·장기 보존 정책 ⭐ (Round 5 #B9.4 High 수정)
# ───────────────────────────────────────────────────────
backup_policy:
  enabled: true
  frequency: "on_every_write"               # yaml 갱신 시마다
  location: "$BOOK_ROOT/master/.backups/"
  rotation_count: 10                         # 최근 10개 백업 유지
  atomic_write: true                          # tmpfile → rename (POSIX atomic)
  checksum_algorithm: "sha256"                # 백업 파일 무결성 검증
  encoding: "UTF-8"                           # ⚠ Round 5 #B9.2 — 강제 인코딩
  schema_version_tracking: true               # backward compat migration

# 8. 인쇄·출판 메타데이터 ⭐ (Round 5 #B2.5 + 저자 진북 *5년·10년 검증*)
# ───────────────────────────────────────────────────────
publication_metadata:
  isbn: null                                  # 출판 확정 시 입력
  copyright: "© {{저자명}} 2026-2030"
  publisher: null                             # 출판 확정 시
  edition: "초판"
  expected_total_chars: 250000                # ⚠ Round 5 #B2.2 — 종이책 350p 목표
  target_total_pages: 350
  language: "ko"
  available_translations: []                   # ⚠ Round 5 #B4.1 multilingual

# 9. AI 협업 명시·작가성 ⭐ (Round 5 #B10.1·#B7.4 Critical 통합)
# ───────────────────────────────────────────────────────
authorship_policy:
  user_intervention_threshold: 0.70           # 저자 실응답 비율 < 0.70 시 알림
  ai_generation_warning: 0.50                  # AI 생성 비율 > 0.50 시 *공저 표기·AI 협업 명시* 강제
  promote_requires_explicit_user: true        # Mode 2 → 정식 진입은 저자 명시 호출만
  paratext_disclosure_required: true          # 발문에 AI 협업 명시 강제

# 9.5. ⭐⭐ 작가 본인 wellness 정책 (Round 17 #J2.1 Critical — 저자 진북 #6 보호)
# ───────────────────────────────────────────────────────
author_wellness_policy:
  enabled: true
  daily_cycle_max: 3                    # 하루 사이클 상한
  consecutive_hour_warn: 2              # 연속 작업 2시간+ 시 경고
  late_night_block_after: "23:00"       # 심야 작업 차단 (저자 수면 보호)
  early_morning_block_before: "06:00"
  break_recommendation_minutes: 15      # 사이클 종료 후 권장 휴식
  weekly_max_cycles: 14                 # 주 14사이클 (일 2회 평균)
  user_intervention_score_threshold: 0.5   # < 0.5 시 저자 피로 의심·알림

# 10. 사후·범용화 정책 ⭐ (Round 5 #B7.5·#B7.2 Critical)
# ───────────────────────────────────────────────────────
posthumous_policy:
  voice_seal_trigger: "저자 명시 또는 사후"
  seal_action: "voice_guidelines 전체 read-only + 신규 책 생성 차단"
  inheritance_delegate: null                  # 저자 명시 위임자 (사후 권리)
  generic_extraction_excluded_fields:        # 2단계 범용화에서 *반드시 제외*
    - voice_guidelines.signature_expressions    # 저자 시그니처 원본
    - voice_guidelines.immutable_core
    - reference_pool                            # 저자 학습 자료
```

---

## 5. Validation Rules

| 필드 | 규칙 | 위반 시 |
|---|---|---|
| `version` | 필수, 문자열 ("2.0" 형식) | bookwriting-master abort + 저자 알림 |
| `search_paths.tier_1_always` | 최소 1개 경로, 존재 검증 | 누락 경로는 warning + 진행 |
| `voice_guidelines.vocabulary.preferred` | 최소 5개 권장 | 적으면 voice gate 약함 → 저자 보강 권장 |
| `voice_guidelines.sentence.max_length_chars` | 정수, 50-200 범위 | 범위 외 → 기본값 80 적용 |
| `voice_guidelines.structure.layer_ratios.*` | 합계 100, 각 범위 [min, max] | 합계 ≠ 100 → 정규화 + 저자 알림 |
| `cycle_triggers.concurrent_cycle_soft_limit` | 정수, 1-20 | 범위 외 → 기본값 5 |
| `bridges.notebooklm.enabled` | 불리언 | true 시 sub_skill 필드 필수 |
| `v1_compatibility.skeleton_path` | 파일 존재 검증 | 누락 시 bookwriting-master abort |

---

## 6. Usage Examples

### 예시 1: 첫 생성 (시스템 자동 + 저자 검토)
```bash
# bookwriting-master 최초 실행 시
# 시스템이 기본 book-config.yaml 생성 (위 Structure의 기본값)
# 저자가 vocabulary·avoid·prohibitions 등 저자 voice를 *수동 보강*
```

### 예시 2: 검색 경로 추가
```yaml
# 저자가 강의록 폴더를 추가하고 싶을 때
search_paths:
  tier_2_explicit:
    - ... (기존)
    - ~/Documents/2025_강의록/    # 추가
```

### 예시 3: voice 가이드라인 점진 보강
```yaml
# bookwriting cycle 중 voice 위반 발견 시
# 저자가 묶음 응답으로 "이 표현은 저자 voice 아님" 표시
# bookwriting-master가 자동으로 voice_guidelines.vocabulary.avoid에 추가 (저자 승인 후)
voice_guidelines:
  vocabulary:
    avoid:
      - ... (기존)
      - "AI 시대가 도래했다"              # 자동 추가 (저자 승인)
      - "디지털 변혁"                      # 자동 추가
```

### 예시 4: 매크로 트리거 조정
```yaml
# 저자가 ⑥ insight-synthesis를 더 자주 발동시키고 싶을 때
cycle_triggers:
  evidenced_count_for_insight: 3        # 5 → 3 (더 자주)
```

---

## 7. Lifecycle

### 생성
- **시점**: bookwriting-master *최초 실행* 시 또는 저자 `/bookwriting init` 호출
- **방법**: 시스템이 *기본 템플릿*으로 생성 → 저자 검토·보강
- **위치**: `$BOOK_ROOT/master/book-config.yaml`

### 갱신
- **수동 갱신**: 저자가 직접 yaml 편집 (검색 경로 추가·매크로 임계값 조정 등)
- **자동 갱신**: voice 가이드라인의 vocabulary.avoid·prohibitions에 *학습된 위반 표현* 자동 추가 (저자 묶음 응답 기반)
- **자동 갱신 시 저자 승인 필수**: bookwriting-master가 추가 후보를 *저자 묶음으로 제시* → 저자 승인 후 yaml 갱신

### 삭제·아카이브
- **삭제 없음**: book-config.yaml은 *항상 유지*되는 핵심 자산
- **버전 관리**: 큰 변경 시 `book-config.v1.yaml`·`book-config.v2.yaml`로 백업 (수동)

### 검증
- **시점**: bookwriting-master 모든 실행 시 *G2: Config Load* 게이트에서 검증
- **방법**: Validation Rules의 모든 규칙 통과 확인

---

## 8. Dependencies

### 이 schema를 *읽는* 스킬
- **bookwriting-master** (모든 사이클·모드에서 필수)
- **모든 단계 마스터** (search_paths·voice_guidelines 참조)
- **voice-gate** (voice_guidelines.* 직접 사용)
- **bookwriting-notebooklm-bridge** (bridges.notebooklm.* 직접 사용)

### 이 schema가 *참조하는* 파일
- skeleton.md (`v1_compatibility.skeleton_path`)
- forecast-registry.yaml (`v1_compatibility.forecast_registry_path`)
- chapter-pipeline.md (`v1_compatibility.chapter_pipeline_path`)

### 이 schema와 *함께 작동하는* 다른 schema
- seed-registry.yaml (시드 라우팅 시 search_paths 기준)
- cycle-registry.yaml (cycle_triggers 기준)

---

## 9. Error Handling

| 실패 시나리오 | 대응 |
|---|---|
| 파일 누락 | bookwriting-master가 *기본 템플릿으로 자동 생성* + 저자 알림 + 저자 보강 요청 |
| yaml 파싱 오류 | bookwriting-master abort + 오류 위치 명시 + 저자 수동 수정 요청 |
| 필수 필드 누락 | 해당 필드 *기본값 적용* + 저자 알림 |
| 검증 규칙 위반 | warning 출력 + 진행 (가능한 경우) 또는 abort (필수 위반) |
| 경로 존재 검증 실패 | tier_1: abort. tier_2: warning + 해당 경로 skip |
| 자동 갱신 충돌 (저자가 동시 편집 중) | 자동 갱신 일시 보류 + 저자 묶음 deferred 풀에 추가 |

---

## 10. Verification Examples

### 검증 1: 기본 생성
```bash
# 시나리오: bookwriting-master 최초 실행
# 기대: 기본 book-config.yaml 생성됨
$ ls $BOOK_ROOT/master/book-config.yaml
✅ 파일 존재
$ yamllint book-config.yaml
✅ 문법 통과
$ grep -c "voice_guidelines" book-config.yaml
✅ voice_guidelines 섹션 포함
```

### 검증 2: voice 가이드라인 적용
```bash
# 시나리오: bookwriting cycle 중 voice 위반 검출
# 기대: voice_guidelines.vocabulary.avoid에 새 표현 자동 추가 (저자 승인 후)
$ /bookwriting cycle ch01
# ... 사이클 진행 중 ...
# 저자 묶음 응답: "1=accept_voice_addition"
$ grep "AI 시대가 도래했다" book-config.yaml
✅ avoid 목록에 자동 추가됨
```

### 검증 3: 검색 경로 변경 즉시 반영
```bash
# 시나리오: 저자가 search_paths 수정
$ vim book-config.yaml
# tier_2_explicit에 새 경로 추가
$ /bookwriting cycle ch01
# 기대: 다음 사이클에서 새 경로도 검색됨
✅ 단계 마스터의 systemlink가 새 경로 자산을 발견
```

### 검증 4: 매크로 트리거 즉시 반영
```bash
# 시나리오: 저자가 evidenced_count_for_insight를 5→3으로 변경
$ /bookwriting cycle ch01
# 기대: EVIDENCED 시드 3개에 도달하면 ⑥ insight-synthesis 자동 권장
✅ 매크로 트리거 발동
```

### 검증 5: 파일 손상 복구
```bash
# 시나리오: book-config.yaml이 손상됨
$ /bookwriting cycle ch01
# 기대: 오류 메시지 + 저자 수동 수정 요청
❌ "book-config.yaml 파싱 실패: line 23 — invalid syntax"
✅ 저자 알림 출력
✅ 사이클 ABORT (bookwriting-master abort)
```

---

**End of SPEC: data-schema-book-config**
