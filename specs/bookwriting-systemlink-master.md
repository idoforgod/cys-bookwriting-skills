# SPEC: bookwriting-systemlink-master

> *글쓰기 차원*의 자산 검색·시드 연결·시스템 사고 빈 고리 발견. 저자 진짜 워크플로우 3·4·5단계 (시스템 사고·빈 고리·추가 통찰)의 *글쓰기 차원* 구현.
>
> 작성일: 2026-05-24
> 매트릭스: 6 sub + 5 AI Agents + 4 Cycle + 3 Gate (Q18)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-systemlink-master` |
| 카테고리 | 단계 마스터 (③, MVP 수직 슬라이스 포함) |
| 저자 11 단계 매트릭스 위치 | ③ |
| 저자 진짜 워크플로우 매핑 | **3·4·5단계 — 시스템 사고·빈 고리·추가 통찰 (글쓰기 차원)** |
| 슬래시 | `/bookwriting-systemlink <mode> [target]` |
| 매트릭스 수치 | 6 sub + 5 AI Agents + 4 Cycle + 3 Gate |

---

## 2. Purpose

저자 *전체 자산 풀* (book-config.search_paths)에서 시드와 *글쓰기 차원* 연결되는 자산을 발견하고, *저자 시스템 사고 그래프*에서 *빈 고리*를 자동 발견한다.

**저자 옵션 A+ 원칙 준수:**
- 다른 스킬 자동 호출 안 함
- bookwriting의 자체 grep·glob·Read만 사용
- 저자가 외부에서 foresight-systems-perspective·structural-analysis 등을 *manual 호출*하면 → 결과를 inbox로 → ① absorb → ③ systemlink에서 활용

**4 책임:**
1. **자산 발견** — search_paths grep·glob으로 시드 관련 자산 발견
2. **자산 연결** — seed-registry connections.linked_assets·linked_seeds 갱신
3. **시스템 루프 호명** — 저자 v1 system_loops (L1-L7) 매핑
4. **빈 고리 발견** — 시스템 그래프에서 *연결 누락 후보* 검출 + 저자 묶음

---

## 3. Philosophy

**저자 옵션 A+ 자기완결:**
- 외부 web·API 호출 안 함
- search_paths ($BOOK_ROOT + Obsidian vault + 등록 자료 폴더) 내에서만

**저자 v1 호환:**
- forecast-registry.yaml의 system_loops 필드 사용 (L1-L7)
- skeleton.md의 시스템 사고 척추 §2 호환

**Citation Gate cross-cutting 적용:**
- 자산 연결 시 *출처 메타데이터* 자동 추출
- linked_assets[].citation 필드 강제 (data-schema-seed-registry SPEC 참조)

---

## 4. Scope

### In scope
- ✅ search_paths grep·glob으로 시드 관련 자산 발견
- ✅ seed-registry connections.linked_assets 갱신 (citation 필드 포함)
- ✅ 자산 간 cross-reference 발견 → linked_seeds 갱신
- ✅ 저자 v1 system_loops (L1-L7) 매핑
- ✅ 시스템 그래프 빈 고리 발견 + 저자 묶음
- ✅ Obsidian vault 검색 (옵션 A+ 로컬 파일 시스템)

### Out of scope
- ❌ NotebookLM 직접 query (bookwriting-notebooklm-bridge 담당, 저자 명시)
- ❌ 다른 스킬 자동 호출 (옵션 A+)
- ❌ 자산 *내용 분석 깊이* (③은 *연결*만, ④ evidence-collect가 *깊이 분석*)
- ❌ 외부 web 검색

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-systemlink cycle <target>` | 풀 사이클 (모든 6 sub 실행) |
| `/bookwriting-systemlink search <query>` | 단순 자산 검색 |
| `/bookwriting-systemlink loop-map <target>` | 시스템 루프 매핑만 |
| `/bookwriting-systemlink gap-detect <target>` | 빈 고리 발견만 |

---

## 6. Invocation

```bash
/bookwriting-systemlink cycle ch01-economy
/bookwriting-systemlink cycle S-001
/bookwriting-systemlink search "한계비용 제로"
/bookwriting-systemlink loop-map ch01-economy        # L1-L7 매핑
/bookwriting-systemlink gap-detect ch01-economy      # 빈 고리만
```

---

## 7. Behavior

**9단계 행동 시나리오:**

```
호출: /bookwriting-systemlink cycle ch01-economy

【Step 1: 입력 검증·자료 로드】
  - ch01 라우팅 시드 (SEED·LINKED) 추출
  - book-config.search_paths 로드
  - forecast-registry의 system_loops (L1-L7) 로드
  - skeleton.md 시스템 사고 척추 §2 로드

【Step 2: 자산 검색 (Asset Searcher 페르소나)】
  - search_paths 전체에서 시드 keyword·시그니처 어휘 grep
  - Obsidian vault (reference-vault) 우선
  - 저자 저자가 등록한 다른 자료 폴더도
  - 발견 자산별 relevance 0-1 점수

【Step 3: 자산 연결 (Asset Linker 페르소나)】
  - 발견 자산을 seed-registry connections.linked_assets에 추가
  - 각 자산의 source_file·citation 필드 자동 채움 (Citation Gate 적용)
  - relevance ≥0.7 자산만 채택 (낮은 점수는 풀에서 제외)

【Step 4: 시드 간 cross-reference 발견 (Cross-Seed Linker 페르소나)】
  - 발견 자산이 다른 시드와도 연결되는가
  - seed-registry connections.linked_seeds 갱신
  - relation_type 매핑: extends·contrasts·examples·depends_on·pairs_with

【Step 5: 시스템 루프 호명 (System Loop Mapper 페르소나)】
  - 저자 v1 L1-L7 루프 정의 (forecast-registry):
    - L1 지능대체나선
    - L2 정치내파루프
    - L3 봉건제 풍요 분기
    - L4 인구 비용 전환
    - L5 도덕 비용 증발
    - L6 우주척도 종결자
    - L7 의미 위기 신경학 루프
  - 시드가 어느 루프의 어떤 변수에 해당하는지 매핑
  - skeleton.md 시스템 사고 척추 §2와 정합

【Step 6: 빈 고리 발견 (Gap Detector 페르소나) ⭐】
  - 시스템 그래프에서 *연결 누락 후보* 검출
  - 예: "L1 변수 3은 정의됐는데 변수 4로 가는 피드백 누락"
  - 저자 묶음 escalate: "이 빈 고리를 채울 시드·근거가 필요"

【Step 7: Citation Gate (자동)】
  - 모든 linked_assets[].citation 필드 검증
  - source_file 실재·메타데이터 완전성

【Step 8: 저자 묶음 (모드 1)】
  - 발견 자산 묶음 (10-20개 자산 중 채택 선택)
  - 빈 고리 묶음 (1-3 빈 고리)
  - cross-reference 묶음

【Step 9: 산출 갱신】
  - seed-registry connections 갱신
  - 시드 lifecycle SEED → LINKED 또는 LINKED → EXPANDED 진행
  - cycle-registry outputs 갱신
```

---

## 8. Input Schema

```typescript
{
  mode: "cycle" | "search" | "loop-map" | "gap-detect"
  target: string         // ch-NNN | S-NNN | query
  options: {
    min_relevance?: number    // 기본 0.7
    max_assets?: number       // 기본 20
    obsidian_only?: boolean   // Obsidian vault만
  }
}
```

**파일 입력**: search_paths / seed-registry / forecast-registry / skeleton.md

---

## 9. Output Schema

### 저자 화면
```markdown
# ③ systemlink — ch01-economy

## 자산 발견 (총 28개, 채택 후보 18개)

### Obsidian vault — 12개
- (a) ★ 저자_칼럼_2024_AGI.md (relevance 0.92)
- (b) ★ 저자_강의_2025_메타도구.md (relevance 0.88)
- (c) ...

### 등록 자료 폴더
- (a) $REFERENCE_ROOT/foresight-notes/environmental-scanning.md
- (b) ...

### $BOOK_ROOT 작업물 — 2개

## 시스템 루프 매핑
- INS-001 → L1 지능대체나선 변수 1 (인지 외주화)
- INS-003 → L7 의미위기 변수 3 (가소성 손실)
- ...

## 빈 고리 발견 (2건) ⚠️
### Gap 1: L1 변수 3 → 변수 4 피드백 누락
- 저자 옵션:
  - (a) ★ 새 시드 추가 (`/bookwriting seed`)
  - (b) 외부 foresight-systems-perspective manual 호출
  - (c) 현재 자산에서 발견 시도 재실행
  - (d) defer

### Gap 2: L3 봉건제·풍요 분기 정치 변수 미명시

## Cross-reference (3건)
- S-001 ↔ S-007 (extends)
- ...

저자: "1=a,b,c... / 2=a / 3=a,b"
```

### 파일 갱신
- `seed-registry.yaml` (connections.linked_assets·linked_seeds + system_loops 매핑)
- `cycle-registry.yaml` (outputs)

---

## 10. Deliverable Quality

### 정량 기준
- 자산 발견 수: 10-30개/챕터
- relevance ≥0.7 채택률: 60%+
- 시스템 루프 매핑률: 80%+ (시드의 80%가 L1-L7 중 1개 이상 매핑)
- 빈 고리 발견: 1-3건/챕터
- Citation Gate 통과율: 95%+

### 정성 기준
- 저자 *시스템 사고 그래프 풍부화*
- Obsidian vault·skill 폴더에서 *저자 기존 사고*와 연결
- 빈 고리 명시로 저자 *후속 작업 방향* 명확
- cross-reference로 책 *cross-chapter 직조* 자료

---

## 11. Dependencies

### 필수
- ① absorb 통과 (시드 등록)
- ② fact-anchor 통과 (fact 정합 — 옵션, 동시 진행 가능)
- search_paths (book-config)
- forecast-registry (system_loops 정의)
- skeleton.md

### 후속
- ④ evidence-collect (정밀 근거)
- ⑤ evidence-link (그래프 정밀화)

### 비의존
- 다른 스킬·web

---

## 12. Guards

### Citation Gate ⭐
- 모든 linked_assets[].citation 필드 강제
- source_file 실재 검증

### search_paths 가드
- search_paths 외 디렉토리 검색 *영구 금지* (옵션 A+)

### Relevance 가드
- relevance < 0.7 자산 풀에서 제외 (저자 옵션으로 조정 가능)

### Gap Detection 가드
- 빈 고리 *3건 초과* 발견 시 저자 알림 + 일괄 처리 권장

---

## 13. AI Agents Personas (5명)

| # | 페르소나 | 역할 |
|---|---|---|
| 1 | **Asset Searcher** | search_paths grep·glob 검색 |
| 2 | **Asset Linker** | seed-registry connections.linked_assets 갱신·citation 필드 추출 |
| 3 | **Cross-Seed Linker** | linked_seeds 갱신·relation_type 매핑 |
| 4 | **System Loop Mapper** | 저자 v1 L1-L7 매핑 |
| 5 | **Gap Detector ⭐** | 시스템 그래프 빈 고리 발견 |

---

## 14. Cycle

| Cycle | 트리거 | 작동 |
|---|---|---|
| **C1: Chapter Link** | `cycle ch-NNN` | 챕터 전체 자산 연결 + 시스템 루프 + 빈 고리 |
| **C2: Seed Link** | `cycle S-NNN` | 단일 시드 |
| **C3: Loop Map Only** | `loop-map` | 시스템 루프 매핑만 |
| **C4: Gap Detect Only** | `gap-detect` | 빈 고리만 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| **G1: Input** | SEED 이상 시드 ≥1개 |
| **G2: Citation Gate** | linked_assets citation 100% |
| **G3: System Loop Map** | 시드 80%+가 L1-L7 매핑 |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| 자산 발견 0개 | warning + 저자 알림 + search_paths 확인 권장 |
| Obsidian vault 접근 실패 | warning + 다른 search_paths만 검색 + 저자 알림 |
| 시스템 루프 매핑 30% 미만 | warning + 저자 알림 (시스템 사고 척추 보강 권장) |
| 빈 고리 다수 (5건+) | 저자 일괄 묶음 |
| Citation Gate 위반 | 해당 자산 풀 제외 + 저자 알림 |

---

## 17. Verification Examples

### 검증 1: 챕터 systemlink
```bash
/bookwriting-systemlink cycle ch01-economy
✅ 28 자산 발견
✅ 18 채택 (relevance ≥0.7)
✅ Obsidian vault에서 12개 발견
✅ system_loops 매핑률 87% (시드 7개 중 6개)
✅ 빈 고리 2건 발견 → 저자 묶음
✅ cross-reference 3건
✅ Citation Gate 100% 통과
```

### 검증 2: Obsidian vault 활용
```bash
/bookwriting-systemlink search "메타 도구"
✅ 저자 칼럼 2024·강의록 2025·기존 책 인용 발견
✅ 모두 Grade B (저자 본인 — Layer 2)
✅ source_file 실재 확인
```

### 검증 3: 시스템 루프 매핑
```bash
/bookwriting-systemlink loop-map ch01-economy
✅ INS-001 → L1 변수 1
✅ INS-003 → L1 변수 4 + L7 변수 3 (cross-loop)
✅ INS-005 → L3 정치 변수
✅ forecast-registry system_loops 필드 갱신
```

### 검증 4: 빈 고리 발견
```bash
/bookwriting-systemlink gap-detect ch01-economy
✅ Gap 1: L1 변수 3 → 변수 4 피드백 누락
✅ Gap 2: L3 정치 변수 → 봉건제 분기 결정 메커니즘 미정의
✅ 저자 묶음: "(a) 시드 추가 / (b) 외부 manual 호출 / (c) 재시도 / (d) defer"
```

### 검증 5: cross-seed 연결
```bash
✅ S-001 (메타도구) ↔ S-007 (UBI 지능) — relation: extends
✅ S-003 ↔ S-018 — relation: contrasts
✅ seed-registry linked_seeds 갱신
```

### 검증 6: search_paths 가드
```bash
# search_paths 외 경로 시도
✅ 절대 검색 안 함 (옵션 A+ 원칙)
✅ 저자 알림: "search_paths에 추가 필요 — book-config.yaml 갱신 권장"
```

---

**End of SPEC: bookwriting-systemlink-master**

> ③ systemlink는 저자 *시스템 사고 그래프*를 *글쓰기 차원*으로 풍부화. Obsidian vault 파일이 *저자 기존 사고와의 연결*을 제공. 빈 고리 발견으로 *후속 작업 방향* 명확화.

---

## 부록: 결정론·grill-me·9 항목·Mode 2·R1-R5

### 결정론 모듈
- M6 relevance_scorer (BM25 키워드 빈도)
- M3 AuthorityGrader (Asset Linker citation 자동)
- M11 lifecycle_state_machine (SEED → LINKED 전환)
- 자체 결정론: grep·glob 검색 (subprocess + pathlib)
- 자체 결정론: system_loops L1-L7 매핑 (forecast-registry lookup)
- 자체 결정론: 시스템 그래프 빈 고리 검출 (그래프 알고리즘)

**LLM 허용 영역**: 의미 유사도 평가 (cross-seed) — 결정론 환원 어려움, 단 confidence 점수 결정론

### grill-me D# 매핑
| D3·D4·D5 (시스템 사고·빈 고리·통찰) 글쓰기 차원 | §2 책임 |
| D19 (옵션 A+ 자기완결) | §3 + §12 search_paths 외 영구 금지 |
| D20 (검색 디렉토리) | §4 + §11 Dependencies |

### 9 항목
(a) §1+§2 / (b) §2 / (c) §13 5 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록

### Mode 2 자동
- relevance ≥0.7 자산 자동 채택·빈 고리 발견 *기록만* (저자 묶음 0회)
- 결과 → `_simulations/`

### R1-R5
- R3 system_loops 호명 강제 ⭐ — 본 단계의 핵심 책임
- R1·R2·R4·R5: 후속 단계 협업

**End of SPEC: bookwriting-systemlink-master**
