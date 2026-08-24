# SPEC: bookwriting-evidence-link-master

> ④ evidence-collect가 수집한 *근거들 간 그래프 연결*. 저자 권위 5층 다층 매핑·논리 정합 검증.
>
> 작성일: 2026-05-24
> 매트릭스: 7 sub + 6 AI Agents + 5 Cycle + 4 Gate (Q18)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-evidence-link-master` |
| 카테고리 | 단계 마스터 (⑤a) — Phase 3-B (수직 슬라이스 외) |
| 저자 11 단계 매트릭스 위치 | ⑤ |
| 저자 진짜 워크플로우 매핑 | **5·6단계 — 신호 연관·미래 시스템 구축 (글쓰기 차원)** |
| 슬래시 | `/bookwriting-evidence-link <mode> [target]` |
| 매트릭스 수치 | 7 sub + 6 AI Agents + 5 Cycle + 4 Gate |

---

## 2. Purpose

④ evidence-collect가 발굴·등급화한 근거들 사이의 *논리 그래프*를 구축한다. 저자 v1 *권위 5층 다층 인용* (R4)과 *시스템 사고 피드백 루프*를 evidence 그래프에 매핑. 후속 ⑥ insight-synthesis의 *통찰 추출 기반 자료* 제공.

**4 책임:**
1. **근거 간 연결** — evidence 끼리 *논리·시간·인과* 연결 자동 발견
2. **권위 5층 매핑** — 모든 evidence 노드를 5층 중 1개에 속하게 매핑
3. **R4 다층 검증** — 같은 주장에 *최소 2층* 권위 매핑
4. **시스템 루프 그래프** — 저자 v1 L1-L7 루프와 evidence 그래프 정합

---

## 3. Philosophy

**저자 v1 호환:**
- forecast-registry.yaml의 `system_loops` + `authority_layer` 필드
- chapter-pipeline.md의 R4 규칙 (단일 권위 금지)

**Citation Gate cross-cutting 적용:**
- 그래프 노드별 출처 검증
- R4 다층 자동 강제

**옵션 A+ 자기완결:**
- 외부 호출 없음
- ④ evidence-collect 출력만 사용

---

## 4. Scope

### In scope
- ✅ evidence 노드 간 그래프 연결 자동 발견
- ✅ 권위 5층 매핑 검증
- ✅ R4 다층 인용 강제
- ✅ 시스템 루프 (L1-L7) 그래프 매핑
- ✅ chapters/<ch>/evidence-track.yaml 확장 (그래프 필드)

### Out of scope
- ❌ evidence 수집 (④ evidence-collect 담당)
- ❌ 통찰 추출 (⑥ insight-synthesis 담당)
- ❌ 본문 작성 (⑦ content-expand 담당)

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-evidence-link cycle <target>` | 풀 사이클 |
| `/bookwriting-evidence-link graph <target>` | 그래프 구축만 |
| `/bookwriting-evidence-link r4-verify <target>` | R4 검증만 |
| `/bookwriting-evidence-link loop-integrate <target>` | 시스템 루프 통합만 |

---

## 6. Invocation

```bash
/bookwriting-evidence-link cycle ch01-economy
/bookwriting-evidence-link graph ch01-economy
/bookwriting-evidence-link r4-verify ch01-economy
```

---

## 7. Behavior

**9단계 행동 시나리오 (요약):**

```
Step 1: ④ evidence-collect 출력 로드 (evidence-track.yaml)
Step 2: evidence 그래프 노드 구축 (Graph Builder 페르소나)
Step 3: 노드 간 연결 자동 발견 (Edge Detector 페르소나)
  - 논리: A 주장 → B 결론
  - 시간: 1990 사건 → 2024 결과
  - 인과: 원인 evidence → 결과 evidence
Step 4: 권위 5층 매핑 (Authority Mapper 페르소나)
Step 5: R4 다층 검증 (R4 Verifier 페르소나)
  - 주장별 권위층 수 카운트
  - 단일 권위 주장 → 풀에서 제외 또는 저자 묶음
Step 6: 시스템 루프 통합 (Loop Integrator 페르소나)
  - L1-L7 루프 그래프와 evidence 그래프 정합
Step 7: Citation Gate cross-cutting
Step 8: 저자 묶음 (모드 1) — R4 위반·고립 노드·loop 누락 처리
Step 9: evidence-track.yaml 그래프 필드 갱신
```

---

## 8. Input Schema

```typescript
{
  mode: "cycle" | "graph" | "r4-verify" | "loop-integrate"
  target: string
  options: {
    min_authority_layers?: number   // 기본 2 (R4)
    visualize?: boolean              // 그래프 시각화 출력
  }
}
```

---

## 9. Output Schema

### 저자 화면
```markdown
# ⑤ evidence-link — ch01-economy

## evidence 그래프 구축
- 노드 23개 (evidence)
- 엣지 31개 (논리 18·시간 8·인과 5)
- 고립 노드 0개

## R4 다층 검증
- 주장 15개 평가
- R4 통과 13개 (87%) ✅
- R4 위반 2건 ⚠️
  - 저자 묶음 escalate (단일 권위 보강·해당 주장 제외)

## 시스템 루프 통합
- L1 지능대체나선: evidence 8개 매핑
- L3 봉건제 풍요 분기: evidence 5개
- ...

저자: "1=a,b / 2=..." 응답
```

---

## 10. Deliverable Quality

### 정량 기준
- evidence 노드 그래프화 100%
- R4 통과율 85%+
- 시스템 루프 매핑률 80%+
- Citation Gate 위반 0건 (그래프 추가 시점)

### 정성 기준
- 저자 v1 system_loops와 정합
- 권위 5층 균형 잡힌 분포
- 논리·시간·인과 엣지 *해석 가능*

---

## 11. Dependencies

### 필수
- ④ evidence-collect 통과 (evidence-track.yaml)
- forecast-registry.system_loops
- citation-authority-db

### 후속
- ⑥ insight-synthesis (그래프 기반 통찰)

---

## 12. Guards

### Citation Gate cross-cutting
### R4 Multi-Layer Gate (전용)
- 모든 주장이 *최소 2층 권위* 도달
- 위반 시 저자 묶음 escalate

### Isolated Node Gate
- 고립 노드 (다른 evidence와 연결 없음) 발견 시 저자 알림
- 저자 결정: 풀에서 제외·연결 추가·미해결로 보관

---

## 13. AI Agents Personas (6명)

| # | 페르소나 | 역할 |
|---|---|---|
| 1 | Graph Builder | evidence 그래프 노드 구축 |
| 2 | Edge Detector | 논리·시간·인과 엣지 자동 발견 |
| 3 | Authority Mapper | 권위 5층 매핑 |
| 4 | R4 Verifier ⭐ | R4 다층 인용 강제 |
| 5 | Loop Integrator | 시스템 루프 (L1-L7) 통합 |
| 6 | Isolation Detector | 고립 노드·약한 연결 발견 |

---

## 14. Cycle (C1-C5)

| Cycle | 트리거 | 작동 |
|---|---|---|
| C1: Chapter Graph | `cycle ch-NNN` | 챕터 전체 그래프 구축 |
| C2: Seed Graph | `cycle S-NNN` | 단일 시드 evidence 그래프 |
| C3: Graph Only | `graph` | 노드·엣지만 (R4·loop 생략) |
| C4: R4 Verify Only | `r4-verify` | R4 검증만 |
| C5: Loop Integration | `loop-integrate` | 시스템 루프 통합만 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| G1: Input | ④ 출력 evidence-track 존재 |
| G2: Graph Completeness | 고립 노드 0 또는 저자 결정 |
| G3: R4 Multi-Layer | 85%+ 통과 |
| G4: Loop Integration | L1-L7 매핑률 80%+ |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| evidence 0개 (④ 미통과) | abort + ④ 재호출 권장 |
| 고립 노드 다수 (5+) | 저자 일괄 묶음 |
| R4 위반 30%+ | warning + ④ 추가 evidence 수집 권장 |
| L1-L7 매핑률 30% 미만 | warning + ③ systemlink 재호출 권장 |

---

## 17. Verification Examples

1. 챕터 그래프: 23 노드 + 31 엣지 + 고립 0
2. R4 통과율 87% + 저자 묶음 위반 2건
3. 시스템 루프 매핑 8 evidence → L1
4. 그래프 시각화 출력 (markdown table)
5. Citation Gate 100% 통과

---

---

## 부록: 결정론·grill-me·9 항목·Mode 2·R1-R5

### 결정론 모듈
- 그래프 구축: 자체 결정론 (networkx 또는 pure Python dict)
- M3 AuthorityGrader (Authority Mapper)
- M13 r4_multi_layer_verifier ⭐ 핵심
- M2 HallucinationDetector (Citation cross-cutting)
- 자체 결정론: 엣지 검출 (정규식·시간 비교·인과 키워드)
- 자체 결정론: 고립 노드 검출 (degree 0 그래프 알고리즘)

**LLM 허용**: 엣지 *논리 검증* (단, 저자 v1 chapter-pipeline 양식 1:1 준수)

### grill-me D# 매핑
| D# | §위치 |
|---|---|
| R4 다층 강제 ⭐ | §12 + 부록 결정론 M13 |
| D3 시스템 사고 (글쓰기 차원) | §2 + §13 Loop Integrator |
| Q33 citation cross-cutting | §12 |

### 9 항목
(a) §1+§2 / (b) §2 / (c) §13 6 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록

### Mode 2
- R4 위반 *자동 풀 제외* (저자 묶음 skip)
- 고립 노드 *기록만*

### R1-R5
- R4 다층 인용 강제 ⭐ — 본 단계 핵심 책임
- R3 system_loops 통합 — Loop Integrator 페르소나

**End of SPEC: bookwriting-evidence-link-master**
