# SPEC: bookwriting-notebooklm-bridge

> 저자 NotebookLM 외부 통합 *별도 sub-skill*. 저자 옵션 D (Q15) — bookwriting 메인은 자기완결 유지하고 NotebookLM은 *저자 명시 호출* 전용 bridge.
>
> 작성일: 2026-05-24

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-notebooklm-bridge` |
| 카테고리 | 단일 sub-skill (마스터 없음) — 외부 통합 bridge |
| 저자 11 단계 매트릭스 위치 | 외부 (cross-cutting 아님 / 마스터 위계 아님) |
| 슬래시 | `/bookwriting-notebooklm-bridge <mode>` |
| 저자 강조 | 저자 모든 저서가 NotebookLM에 적재 — 책 작업의 핵심 자산 접근 통로 |

---

## 2. Purpose

저자 NotebookLM의 *모든 저서·자료*를 bookwriting 작업으로 *명시적으로 가져오는 통로*. 옵션 A+ 자기완결 원칙을 유지하기 위해 *bookwriting 메인 사이클은 NotebookLM 자동 호출 안 함*. 저자가 *필요 판단 시* 본 bridge 명시 호출 → 결과를 inbox에 자동 적재 → ① absorb에서 처리.

**4 책임:**
1. **NotebookLM query** — 저자 명시 질의를 MCP로 NotebookLM에 전달
2. **결과 inbox 적재** — 응답을 *frontmatter 동반 markdown*으로 inbox/에 저장
3. **권위 메타데이터 추출** — NotebookLM의 *출처 인용*을 권위 5층 매핑
4. **재인용 가능 메타데이터** — 저자 후일 검증을 위한 *citation_path·notebook_id·source_doc* 명시

---

## 3. Philosophy

**옵션 A+ 준수:**
- bookwriting 메인 사이클은 NotebookLM 자동 호출 *영구 금지*
- bridge는 *저자 명시 호출 전용*
- 결과는 *inbox 통로*로만 bookwriting에 진입

**저자 v1 로컬 원칙 *부분 완화*:**
- bridge 자체는 MCP로 외부 API 호출 (예외)
- 그러나 *결과는 로컬 inbox 적재*로 마무리 — 후속은 로컬

**Citation Gate cross-cutting 적용:**
- NotebookLM 응답의 *출처·인용*을 자동 추출·검증
- 출처 누락 응답은 저자 알림

---

## 4. Scope

### In scope
- ✅ `mcp__notebooklm-mcp__notebook_query`·`cross_notebook_query` 호출
- ✅ 응답을 markdown + frontmatter로 변환
- ✅ inbox/<YYYY-MM-DD>-notebooklm-<query-slug>.md 저장
- ✅ NotebookLM 출처 인용 추출 + citation 메타데이터

### Out of scope
- ❌ bookwriting 메인 사이클 자동 호출 (절대)
- ❌ NotebookLM 노트북 자체 *수정·생성* (저자 nlm CLI로)
- ❌ 응답 *내용 분석* (① absorb·③ systemlink·④ evidence-collect 담당)

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-notebooklm-bridge query "<text>" --notebook <ID>` | 단일 notebook 질의 |
| `/bookwriting-notebooklm-bridge cross-query "<text>"` | 모든 notebook cross-query |
| `/bookwriting-notebooklm-bridge list-notebooks` | 노트북 목록 조회 |
| `/bookwriting-notebooklm-bridge research "<topic>"` | research_start 시작 |

---

## 6. Invocation

```bash
# 단일 노트북 질의
/bookwriting-notebooklm-bridge query "AGI 메타도구 정의에 관한 저자 견해" --notebook 저자-저서-전체

# Cross-query
/bookwriting-notebooklm-bridge cross-query "한계비용 제로의 AGI 시대 완성"

# 노트북 목록
/bookwriting-notebooklm-bridge list-notebooks

# 결과 자동 inbox 적재
ls $BOOK_ROOT/inbox/
# 2026-05-24-notebooklm-agi-meta-tool.md
```

---

## 7. Behavior (요약)

```
Step 1: 인자 파싱 + nlm 인증 상태 확인
Step 2: MCP 호출:
  - mode=query: mcp__notebooklm-mcp__notebook_query
  - mode=cross-query: mcp__notebooklm-mcp__cross_notebook_query
Step 3: 응답 처리:
  - 출처·인용 자동 추출
  - 권위 5층 매핑 (Grade B 저자 본인 + Grade A 창업자 인용 등)
  - frontmatter 자동 생성:
    ---
    type: evidence (또는 저자 명시)
    source: NotebookLM
    notebook_id: 저자-저서-전체
    query: "..."
    created: <timestamp>
    citation:
      authority_grade: B
      author: "{{저자명}}"
      ...
    ---
Step 4: inbox/ 적재
Step 5: bookwriting-master에 *흡수 권장* 알림
Step 6: 저자가 /bookwriting absorb로 후속 처리
```

---

## 8. Input Schema

```typescript
{
  mode: "query" | "cross-query" | "list-notebooks" | "research"
  query?: string         // query·cross-query 시 필수
  notebook_id?: string   // query 모드 필수
  topic?: string         // research 모드
}
```

---

## 9. Output Schema

### inbox 파일 (자동 적재)
```markdown
---
type: evidence
source: NotebookLM
notebook_id: 저자-저서-전체
query: "AGI 메타도구 정의에 관한 저자 견해"
created: 2026-05-24T17:00:00Z
citation:
  authority_grade: B
  author: "{{저자명}}"
  publication: "저자 저서 전체 (NotebookLM)"
  source_file: NotebookLM://저자-저서-전체
to: ch-skeleton-spine
---

# NotebookLM 응답

[응답 본문]

## 출처 인용
- 저자 2024 저서 "..." (Section 3)
- 저자 2025 칼럼 "..." (NYT 인용)
- ...
```

### 저자 화면
```markdown
# NotebookLM bridge — query 완료

✅ 응답 수신 (1240 자)
✅ 출처 5개 자동 추출 (Grade B 3 / Grade A 2)
✅ inbox/2026-05-24-notebooklm-agi-meta-tool.md 저장
✅ /bookwriting absorb 호출로 흡수 권장

다음: /bookwriting absorb
```

---

## 10. Deliverable Quality

### 정량 기준
- MCP 호출 성공률 95%+
- 출처 추출 정확도 90%+
- frontmatter 자동 생성 100%
- inbox 적재 latency 10-30초

### 정성 기준
- 저자가 inbox 파일을 *바로 ① absorb로 흡수* 가능
- 출처 인용 메타데이터 *완전* — 후일 재인용 가능
- 저자 nlm 인증 끊김 자동 감지

---

## 11. Dependencies

### 필수
- 저자 NotebookLM MCP 설치·인증 (`nlm login`)
- `mcp__notebooklm-mcp__*` 도구 풀
- `$BOOK_ROOT/inbox/` 디렉토리

### 비의존
- bookwriting 메인 사이클 (옵션 A+ 자기완결 절대 준수)
- 설치된 다른 스킬

---

## 12. Guards

### 명시 호출 전용 가드
- bookwriting 메인 sub-skill에서 *절대* 자동 호출 안 함

### Citation Gate
- NotebookLM 응답의 출처 검증
- 출처 누락 → 저자 알림 (Critical 차단은 아님 — 저자 흡수 결정)

### MCP 인증 가드
- nlm 인증 끊김 시 저자 알림 + `nlm login` 권장

### Rate Limit 가드
- 시간당 호출 수 제한 (NotebookLM 정책 따름)

---

## 13. AI Agents Personas (3명)

1. **Query Constructor** — 저자 질의를 NotebookLM 친화 형식으로
2. **Response Parser** — 응답에서 출처·인용·메타데이터 추출
3. **Inbox Adapter** — frontmatter 동반 markdown으로 변환·저장

---

## 14. Cycle (C1-C2)

| Cycle | 트리거 | 작동 |
|---|---|---|
| C1: Single Query | `query` | 단일 노트북 질의 |
| C2: Cross-Notebook | `cross-query` | 모든 노트북 검색 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| G1: Auth | nlm 인증 통과 |
| G2: MCP Response | 응답 수신 성공 |
| G3: Citation Extraction | 출처 1개+ 추출 |
| G4: Inbox Persistence | 파일 저장 완료 |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| nlm 인증 실패 | 저자 알림 + `nlm login` 권장 |
| MCP timeout | 1회 재시도 + 실패 시 저자 알림 |
| 응답 출처 0개 | warning + frontmatter에 *출처 미명시* 표시 + 저자 알림 |
| inbox 쓰기 실패 | 저자 알림 + 응답 메모리 보존 |

---

## 17. Verification Examples

1. 단일 노트북 query: 응답 + frontmatter + inbox 적재 ✅
2. Cross-query: 5 노트북 통합 응답 ✅
3. 출처 추출: Grade A 2 + Grade B 3 ✅
4. 저자 후속 `/bookwriting absorb` 정상 처리 ✅
5. nlm 인증 끊김 자동 감지 ✅

---

**End of SPEC: bookwriting-notebooklm-bridge**

> ⭐ bridge는 *옵션 A+ 원칙 보존*하면서 저자 NotebookLM 자산 *모든 저서*에 접근하는 *유일한 통로*. 저자 명시 호출 → inbox → ① absorb로 정합 진입.

---

## 부록: 결정론·grill-me·9 항목·옵션 A+ 명확화

### 결정론 모듈
- 자체 결정론: MCP 응답 파싱·frontmatter 생성 (yaml.safe_dump)
- M2 HallucinationDetector (응답 출처 검증)
- M3 AuthorityGrader (응답 출처 권위 등급)
- 자체 결정론: inbox 파일 명명·timestamp 생성

**LLM 허용**: NotebookLM query 자연어 (저자 입력 → 그대로 MCP에 전달, LLM 가공 안 함)

### grill-me D# 매핑
| D# | §위치 |
|---|---|
| Q15 옵션 D (bridge 분리) | §1·§2·§3 ⭐ |
| D19 옵션 A+ (옵션 A+ 부분 완화) | §3 Philosophy + 부록 옵션 A+ 명확화 |
| 저자 명시 호출 전용 | §12 가드 |

### 9 항목
(a) §1+§2 / (b) §2 / (c) §13 3 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록

### 옵션 A+ 명확화 ⭐ (Round 1 발견)
**옵션 A+ 원칙은 *bookwriting 메인 사이클*에 한해 절대.**
- bookwriting-master·11 단계 마스터·gate·sub: NotebookLM 자동 호출 *영구 금지*
- bookwriting-notebooklm-bridge: *유일한 예외*. 저자 명시 호출 시만.
- bridge 결과는 *inbox 통로*로만 진입. ① absorb가 정상 처리.

이 *명시적 분리*가 옵션 A+ 원칙과 외부 MCP 호출의 *공존*을 보장.

**End of SPEC: bookwriting-notebooklm-bridge**
