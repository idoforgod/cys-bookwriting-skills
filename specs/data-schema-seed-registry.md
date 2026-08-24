# SPEC: data-schema-seed-registry.yaml

> bookwriting의 *글감 단일 진실 공급원*. 저자가 던지는 모든 시드를 *ID·lifecycle·라우팅·연결·히스토리*로 추적.
>
> 작성일: 2026-05-24
> 양식: 데이터 schema 전용 10 항목

---

## 1. Identity

| 항목 | 값 |
|---|---|
| Schema 이름 | `seed-registry.yaml` |
| 카테고리 | Data Schema (글감 마스터) |
| 파일 위치 | `$BOOK_ROOT/master/seed-registry.yaml` |
| 작성·갱신 주체 | bookwriting-master + 단계 마스터들 (자동) + 저자 spot 수정 (드물게) |

---

## 2. Purpose

저자가 던지는 *모든 글감*을 *데이터*로 다룬다. 각 시드의 *lifecycle 진행·라우팅·연결·히스토리*를 *영속적으로* 추적해 *사이클을 가로지르는 글감 그래프*를 구축한다.

**5대 책임:**
1. **단일 진실 공급원** — 모든 시드 ID는 seed-registry에 등록
2. **Lifecycle 추적** — SEED → POLISHED까지 6 외골격 상태 + 13 내부 cycle
3. **라우팅 추적** — chapter_role + primary + cross-reference
4. **연결 추적** — linked_predictions·linked_assets·linked_seeds
5. **히스토리 추적** — cycle_history (어떤 사이클 거쳤는가)

---

## 3. Scope

### In scope
- ✅ 모든 시드 메타데이터·본문·상태·라우팅·연결·히스토리
- ✅ 저자 시드 + foresight 결과 흡수된 시드 + 자산 발굴 시드 모두
- ✅ 시드의 *cross-chapter 그래프*

### Out of scope
- ❌ 시드 본문 *집필 결과* (chapters/<ch>/*.md 담당)
- ❌ 시드의 *근거 자료 텍스트* (evidence-track.yaml + chapter 파일)
- ❌ 사이클 자체 상태 (cycle-registry.yaml 담당)
- ❌ 예측 데이터 (forecast-registry.yaml — v1)

---

## 4. Structure (필드 정의)

```yaml
# $BOOK_ROOT/master/seed-registry.yaml

version: "2.0"
schema: seed-registry
created: 2026-05-24
last_updated: 2026-05-24
seed_count: 0                          # 누적 시드 수 (자동 카운트)
active_count: 0                        # 비-POLISHED 시드 수
next_id: S-001                          # 다음 발급할 ID

seeds:
  - id: S-001                          # 자동 발급 (S-NNN 형식)
    created: 2026-05-24T15:30:00Z
    last_updated: 2026-05-24T16:45:00Z
    source: claude_dialog              # claude_dialog | inbox_import | foresight_result | asset_discovery | drop_folder
    source_detail: "저자 /bookwriting seed 호출"
    
    # ───────────────────────────────────────────
    # 1. 시드 본문
    # ───────────────────────────────────────────
    seed_text: "AGI는 단순히 더 똑똑한 AI가 아니라 메타 도구다. 인지 자체를 확장하는 메타 도구."
    seed_length: 38                    # 글자 수 (가변형 감지)
    seed_type: short                   # short | section | chapter | full (옵션 A 가변 모드)
    
    # ───────────────────────────────────────────
    # 2. Lifecycle (6 외골격 + 13 내부 cycle)
    # ───────────────────────────────────────────
    lifecycle: SEED                    # SEED | LINKED | EXPANDED | EVIDENCED | INSIGHTED | POLISHED
    sub_state: 1                       # 13 내부 cycle 인덱스
    sub_state_name: "글감 추출 완료"
    
    # ───────────────────────────────────────────
    # 3. 라우팅 (Q20 — chapter_role + primary + cross-reference)
    # ───────────────────────────────────────────
    routing:
      primary:
        chapter_id: ch-skeleton-spine   # 1차 라우팅 챕터
        chapter_name: "사상적 척추 §1"
        layer: spine                    # 1 | 2 | 3 | spine | appendix
        section: "메타 도구 명제"
        chapter_role: 2층_분석          # v1 forecast-registry 호환
      
      cross_reference:                  # 보조 챕터 N개
        - chapter_id: ch01-economy
          chapter_name: "1장 경제"
          relevance: "한계비용 제로의 AGI 시대 완성"
        - chapter_id: ch08-meaning
          chapter_name: "8장 의미"
          relevance: "메타도구가 의미 위기에 미치는 영향"
        - chapter_id: ch10-response
          chapter_name: "10장 응답"
          relevance: "메타도구 사용자 자리 지키기"
      
      routing_method: manual_explicit   # manual_explicit | auto_cascade | inbox_routed | promoted_from_sim
      routing_confidence: 1.0           # 0.0-1.0 (auto_cascade일 때만 의미)
      routing_timestamp: 2026-05-24T15:35:00Z
    
    # ───────────────────────────────────────────
    # 4. 연결 (linked_predictions·linked_assets·linked_seeds)
    # ───────────────────────────────────────────
    connections:
      linked_predictions:               # forecast-registry.yaml의 P-NNN 참조
        - id: P-013
          relevance: "한계비용 제로 + AGI 시대"
          discovered_in_cycle: C-007
          # ⭐ Citation Gate 권위 등급
          citation_authority_grade: B   # Jeremy Rifkin 한계비용 제로는 학문 layer 3 (C) but 저자 시스템 사고로 layer 2 (B) 활용
        - id: P-018
          relevance: "메타도구 정의"
          discovered_in_cycle: C-007
          citation_authority_grade: A   # 창업자 증언 (Amodei·Hassabis 발언) — Layer 1
      
      linked_assets:                    # 자산 풀에서 발견된 자료
        - path: $REFERENCE_ROOT/저자_칼럼_2024_AGI.md
          relevance: 0.85
          discovered_in_cycle: C-007
          quote_used: false             # chapter에 인용되었는가
          # ⭐ Citation Gate 메타데이터 (저자 Q33 후속 명령)
          citation:
            authority_grade: B          # Layer 2 — 저자 미래학자 시스템 사고
            author: "{{저자명}}"
            title: "AGI 칼럼 2024"
            publication: "저자 Obsidian vault"
            date: "2024-XX-XX"          # 저자가 yaml에 명시할 항목
            page_or_section: "전체"
            source_file: $REFERENCE_ROOT/저자_칼럼_2024_AGI.md
            citation_gate_verified: true
            hallucination_check: passed
        - path: $BOOK_ROOT/bookidea/skeleton.md#사상적척추-1
          relevance: 1.0
          discovered_in_cycle: C-007
          quote_used: true
          citation:
            authority_grade: B          # 저자 본인 외골격
            author: "{{저자명}}"
            title: "{{내 책 제목}} (집필 중) — 사상적 척추 §1"
            publication: "본 책 외골격"
            date: "2026-05-24"
            page_or_section: "§사상적척추.1 메타도구"
            source_file: $BOOK_ROOT/bookidea/skeleton.md
            citation_gate_verified: true
            hallucination_check: passed
      
      linked_seeds:                     # 다른 시드와의 cross-reference
        - id: S-007
          relevance: "UBI(지능) 명제와 연결"
          relation_type: extends         # extends | contrasts | examples | depends_on
        - id: S-042
          relevance: "기술적 사춘기와 함께 책 사상적 척추 형성"
          relation_type: pairs_with
    
    # ───────────────────────────────────────────
    # 5. 진행 카운터
    # ───────────────────────────────────────────
    progress:
      evidence_collected: 0             # 근거 자료 수집 개수
      insights_derived: 0               # 새 통찰 추출 개수
      content_expanded_chars: 0         # 확장된 글 분량 (글자 수)
      voice_violations: 0               # voice gate 위반 누적
      voice_violations_resolved: 0      # 위반 자동 해소
      cross_chapter_links: 3            # cross-reference 챕터 수
    
    # ───────────────────────────────────────────
    # 6. 사이클 히스토리 (D17·D18)
    # ───────────────────────────────────────────
    cycle_history:
      - cycle_id: C-007
        action: SEED_CAPTURE
        timestamp: 2026-05-24T15:30:00Z
        result: "lifecycle SEED → LINKED 진행 예정"
      - cycle_id: C-012
        action: LINK_ESTABLISHED
        timestamp: 2026-05-25T10:00:00Z
        result: "lifecycle LINKED, 자산 12개 연결"
      # ... 사이클마다 추가
    
    # ───────────────────────────────────────────
    # 7. 저자 메모
    # ───────────────────────────────────────────
    notes:
      - timestamp: 2026-05-24T15:30:00Z
        author: 저자
        content: "이 시드가 책 사상적 척추의 1번 명제. 절대 약화시키지 말 것."
    
    # ───────────────────────────────────────────
    # 8. 시뮬레이션 마킹 (모드 2)
    # ───────────────────────────────────────────
    simulation_only: false              # true면 _simulations/ 폴더 작업물만 (정식 lifecycle 미진행)
    promoted_from: null                 # SIM-NNN ID (promote된 경우)
    
  # ─── 다음 시드들 ───
  - id: S-002
    ...
```

---

## 5. Validation Rules

| 필드 | 규칙 | 위반 시 |
|---|---|---|
| `id` | 형식 `S-NNN`, 유일성 | 중복·형식 오류 → bookwriting-master abort |
| `lifecycle` | enum [SEED·LINKED·EXPANDED·EVIDENCED·INSIGHTED·POLISHED] | enum 외 → 저자 알림 + 마지막 유효값 유지 |
| `sub_state` | 1-13 정수 | 범위 외 → 0 (미정) 처리 |
| `routing.primary` | 필수 (라우팅 안 됐으면 routing_method: unrouted) | 누락 → 사이클 진행 시 라우팅 묶음 제안 |
| `routing.primary.layer` | enum [1·2·3·spine·appendix] | enum 외 → 저자 알림 |
| `routing.routing_confidence` | 0.0-1.0 float | 범위 외 → clamp |
| `connections.linked_predictions[].id` | forecast-registry.yaml에 존재 | 누락 P-NNN 발견 시 → forecast-registry 갱신 권장 |
| `connections.linked_assets[].path` | 파일 존재 | 누락 시 warning + path_missing 표시 |
| `connections.linked_seeds[].id` | seed-registry에 존재 | 누락 시 → 저자 알림 |
| `cycle_history` | 시간순 정렬 | 정렬 위반 → 자동 재정렬 |
| `progress.voice_violations` | 정수, ≥0 | 음수 → 0 reset |

---

## 6. Usage Examples

### 예시 1: 새 시드 등록
```yaml
# 저자: /bookwriting seed "AGI는 메타 도구다"
# bookwriting-master가 seed-registry.yaml에 자동 추가
seeds:
  - id: S-001                          # next_id에서 자동 발급
    created: 2026-05-24T15:30:00Z
    source: claude_dialog
    seed_text: "AGI는 메타 도구다"
    lifecycle: SEED
    routing: 
      routing_method: pending          # 저자 묶음 제안 대기
    ...

# next_id 갱신:
next_id: S-002
seed_count: 1
active_count: 1
```

### 예시 2: lifecycle 진행
```yaml
# 사이클 C-007 진행 중
# ① absorb → ② fact-anchor 통과 후
seeds:
  - id: S-001
    lifecycle: LINKED                   # SEED → LINKED
    sub_state: 3                        # "시스템 연관화 진행 중"
    sub_state_name: "시스템 연관화 진행 중"
    progress:
      ...
    cycle_history:
      - cycle_id: C-007
        action: LIFECYCLE_PROGRESS
        timestamp: 2026-05-24T15:45:00Z
        result: "SEED → LINKED, 자산 8개 연결"
```

### 예시 3: cross-chapter 추가 라우팅
```yaml
# 사이클 진행 중 ⑪ cross-chapter-relink이 추가 라우팅 권장
# 저자 묶음 응답: "1=a,b"
seeds:
  - id: S-001
    routing:
      primary: ...                      # 변경 없음
      cross_reference:
        - ...                           # 기존
        - chapter_id: ch07-cosmic        # 신규 추가
          relevance: "메타도구가 우주적 좌표에 미치는 영향"
```

### 예시 4: 시뮬레이션 시드 promote
```yaml
# 저자: /bookwriting promote SIM-007
# SIM-007에서 사용된 시드들이 정식 등록됨
seeds:
  - id: S-099
    promoted_from: SIM-007
    simulation_only: false              # promote로 false 전환
    ...
```

### 예시 5: 저자 메모 추가
```yaml
# 저자가 직접 yaml 편집해서 메모 추가
seeds:
  - id: S-001
    notes:
      - ...
      - timestamp: 2026-05-30T09:00:00Z
        author: 저자
        content: "이 시드를 ch01의 2층 분석 핵심으로 격상"
```

---

## 7. Lifecycle

### 생성
- **시점**: 저자 `/bookwriting seed` 호출 + bookwriting-master `absorb` + foresight 결과 import 시
- **방법**: `next_id`에서 ID 발급 + 기본 frontmatter 자동 생성
- **첫 상태**: `lifecycle: SEED`, `sub_state: 1`, `routing.routing_method: pending`

### 갱신
- **단계 마스터가 자동 갱신**:
  - ① absorb → lifecycle SEED 등록·라우팅 제안
  - ② fact-anchor → connections.linked_predictions 확인·갱신
  - ③ systemlink → connections.linked_assets·linked_seeds 발견
  - ④ evidence-collect → progress.evidence_collected 증가·linked_predictions 추가
  - ⑤ evidence-link → graph 정합 갱신
  - ⑥ insight-synthesis → progress.insights_derived 증가·lifecycle EVIDENCED → INSIGHTED
  - ⑦ content-expand → progress.content_expanded_chars 갱신
  - ⑩ line-edit → progress.voice_violations·voice_violations_resolved 갱신·lifecycle POLISHED
  - ⑪ cross-chapter-relink → routing.cross_reference 추가
- **저자 직접 편집**: notes·routing 등 저자 spot 수정 (드물게)

### 삭제·아카이브
- **삭제 거의 없음**: 시드는 *영속적 자산*
- **simulation_only: true 시드**: 시뮬레이션 종료 후 *자동 정리* (단, promoted_from 기록은 유지)
- **POLISHED 1년 이상 지난 시드**: archive 권장 (옵션 — 저자 결정)

### 검증
- **시점**: 모든 사이클의 G2 게이트 + 매크로 트리거 시점
- **방법**: Validation Rules 모든 규칙 통과 확인

---

## 8. Dependencies

### 이 schema를 *읽는* 스킬
- **모든 단계 마스터** (대상 시드 정보 조회)
- **bookwriting-master** (사이클 계획·status·list)
- **voice-gate** (progress.voice_violations 카운트)

### 이 schema를 *쓰는* 스킬
- **bookwriting-master**: id 발급·기본 frontmatter·cycle_history 추가
- **bookwriting-absorb-master**: 시드 본문·source·initial lifecycle
- **bookwriting-systemlink-master**: connections.linked_assets·linked_seeds
- **bookwriting-evidence-collect-master**: connections.linked_predictions·progress.evidence_collected
- **bookwriting-insight-synthesis-master**: progress.insights_derived·lifecycle INSIGHTED
- **bookwriting-content-expand-master**: progress.content_expanded_chars
- **bookwriting-line-edit-master**: progress.voice_violations·lifecycle POLISHED
- **bookwriting-cross-chapter-relink-master**: routing.cross_reference

### 외부 참조
- **forecast-registry.yaml**: linked_predictions.id가 P-NNN을 가리킴
- **book-config.yaml**: search_paths가 linked_assets 발견의 범위 결정
- **chapters/<ch>/seed-track.yaml**: 챕터별 사용 시드 매핑 (양방향 일관성)

---

## 9. Error Handling

| 실패 시나리오 | 대응 |
|---|---|
| ID 발급 충돌 (next_id 동기화 실패) | bookwriting-master가 *seeds[]에서 max ID + 1* 재계산 + 저자 알림 |
| 시드 중복 (seed_text 거의 일치) | systemlink 단계에서 *유사도 검출* → 저자 묶음 제안 ("S-001과 유사. 병합·분리?") |
| 라우팅 누락 | 사이클 진행 시 *라우팅 묶음 우선 제시* + 저자 응답 받음 |
| linked_predictions.id 누락 | warning + forecast-registry 갱신 권장 + 사이클 진행 |
| linked_assets.path 누락 | warning + path_missing 표시 + 다음 사이클에서 *재검색* 시도 |
| linked_seeds.id 누락 | 저자 알림 + 연결 끊김 표시 |
| yaml 파싱 오류 | bookwriting-master abort + 백업 자동 복원 시도 |
| 동시 쓰기 충돌 (두 사이클 동시) | 파일 lock + 큐잉 (cycle-registry에서 순서 결정) |

---

## 10. Verification Examples

### 검증 1: 시드 등록·자동 ID 발급
```bash
$ /bookwriting seed "AGI는 메타 도구다"
$ grep "^  - id: S-" $BOOK_ROOT/master/seed-registry.yaml | tail -1
✅ "  - id: S-001"
$ grep "next_id:" seed-registry.yaml
✅ "next_id: S-002"
```

### 검증 2: lifecycle 진행 정확성
```bash
$ /bookwriting cycle ch01
# ... ① absorb 통과 ...
$ grep -A2 "id: S-001" seed-registry.yaml | grep "lifecycle:"
✅ "lifecycle: LINKED"

# ... ⑥ insight-synthesis 통과 ...
$ grep -A2 "id: S-001" seed-registry.yaml | grep "lifecycle:"
✅ "lifecycle: INSIGHTED"
```

### 검증 3: cross-chapter 라우팅 추가
```bash
# 저자 묶음 응답: "1=a,b" (cross-reference 채택)
$ grep -A20 "id: S-001" seed-registry.yaml | grep "cross_reference" -A10
✅ ch07-cosmic이 cross_reference에 추가됨
✅ relevance 필드 명시됨
```

### 검증 4: 시뮬레이션 시드 분리
```bash
$ /bookwriting simulate ch01 --variant insight-driven
# ... 모드 2 진행 ...
$ grep "simulation_only: true" seed-registry.yaml
❌ 정식 seed-registry에는 없음 (시뮬레이션 시드는 정식 등록 안 됨)
$ ls $BOOK_ROOT/chapters/01-economy/_simulations/
✅ sim-NNN.md 파일에 시뮬레이션 시드 정보 존재
```

### 검증 5: cycle_history 누적
```bash
# 시드 S-001이 C-007·C-012·C-018 사이클을 거침
$ grep -A30 "id: S-001" seed-registry.yaml | grep "cycle_id:"
✅ "cycle_id: C-007"
✅ "cycle_id: C-012"
✅ "cycle_id: C-018"
✅ 시간순 정렬됨
```

---

**End of SPEC: data-schema-seed-registry**
