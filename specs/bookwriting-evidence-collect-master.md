# SPEC: bookwriting-evidence-collect-master

> 저자 책의 *근거 자료 수집* 단계. ⑥ insight-synthesis의 *통찰 후보 평가*에 필요한 *권위 5층 인용·정량 앵커·검증 신호*를 흡수 자료 풀에서 정밀 수집. **Citation Gate 가장 엄격 적용 단계** ⭐.
>
> 작성일: 2026-05-24
> 매트릭스: 6 sub + 5 AI Agents + 4 Cycle + 3 Gate (Q18)

---

## 1. Identity

| 항목 | 값 |
|---|---|
| 스킬 이름 | `bookwriting-evidence-collect-master` |
| 카테고리 | 단계 마스터 (④, MVP 수직 슬라이스 포함) |
| 저자 11 단계 매트릭스 위치 | ④ |
| 저자 진짜 워크플로우 매핑 | **2단계 — Fact + Score 수집 (글쓰기 차원)** |
| 슬래시 | `/bookwriting-evidence-collect <mode> [target]` |
| 매트릭스 수치 | 6 sub + 5 AI Agents + 4 Cycle + 3 Gate |
| 저자 강조 영역 | ⭐ Citation Gate 가장 엄격 적용 단계 |

---

## 2. Purpose

저자 흡수 자료 풀 (Obsidian vault·NotebookLM bridge·inbox·search_paths)에서 *책에 인용할 근거 자료*를 *권위 5층 등급화*하여 수집한다. 저자 v1 forecast-registry.yaml의 *예측 데이터*와 *정합 동기화*하여 *후속 ⑥ insight-synthesis의 입력*을 만든다.

**4 책임:**
1. **근거 자료 발굴** — search_paths·NotebookLM bridge·inbox에서 *해당 시드·통찰 후보 관련* 근거 자동 수집
2. **권위 5층 등급화** — citation-gate 적용해 Grade A·B·C·D·E 매핑
3. **정량 앵커 추출** — 저자 *quantitative_anchor* 자동 추출 (100배·90% 확신·2027 임계점 등)
4. **검증 신호 추출** — 저자 v1 R5 *verification_signal·falsifies_if* 자동 발견

---

## 3. Philosophy

**저자 v1 호환:**
- forecast-registry.yaml의 예측 데이터 *읽고 갱신*
- 6 파일 schema의 evidence-track.yaml 갱신
- *quantitative_anchor·authority_layer·verification_signal* 필드 호환

**Citation Gate 가장 엄격 적용:**
- ④ evidence-collect의 *모든 출력*에 citation-gate 자동 발동
- 할루시네이션 의심 → Critical 즉시 차단 (재시도 안 함)
- R4 다층 강제 — 단일 권위 evidence는 풀에서 제외

**옵션 A+ 자기완결:**
- 외부 web 호출 안 함 — 저자 흡수 자료에서만 발굴
- 저자가 외부 web 근거가 필요하면 *외부 manual* 호출 후 inbox로 전달

---

## 4. Scope

### In scope
- ✅ 흡수 자료 풀에서 시드·통찰 관련 근거 자동 수집
- ✅ 권위 5층 등급화 (citation-gate 활용)
- ✅ 정량 앵커 자동 추출
- ✅ 검증 신호 (verification_signal·falsifies_if) 발견
- ✅ chapters/<ch>/evidence-track.yaml 갱신
- ✅ forecast-registry.yaml 갱신 (신규 예측 등록)
- ✅ seed-registry의 progress.evidence_collected·linked_predictions 갱신

### Out of scope
- ❌ 외부 web 검색 (옵션 A+)
- ❌ 근거 간 그래프 연결 (⑤ evidence-link 담당)
- ❌ 근거 자체의 *진위 검증* (저자가 흡수한 자료의 내용은 저자 책임)
- ❌ 통찰 후보 평가 (⑥ insight-synthesis 담당)

---

## 5. Capabilities

| 슬래시 모드 | 기능 |
|---|---|
| `/bookwriting-evidence-collect cycle <target>` | 풀 사이클 |
| `/bookwriting-evidence-collect search <query> --layer A\|B\|C\|D\|E` | 특정 권위층 검색 |
| `/bookwriting-evidence-collect quantitative <target>` | 정량 앵커만 추출 |
| `/bookwriting-evidence-collect verification-signal <target>` | 검증 신호만 발견 |

---

## 6. Invocation

```bash
/bookwriting-evidence-collect cycle ch01-economy       # 풀
/bookwriting-evidence-collect cycle S-001              # 단일 시드
/bookwriting-evidence-collect search "한계비용 제로" --layer A,B    # 권위 A·B만
```

---

## 7. Behavior

**9단계 행동 시나리오:**

```
호출: /bookwriting-evidence-collect cycle ch01-economy

【Step 1: 입력 검증·자료 로드】
  - ch01 시드 추출 (EXPANDED lifecycle 위주, EVIDENCED 미만)
  - book-config의 search_paths 로드
  - forecast-registry.yaml 로드 (기존 P-NNN 예측)

【Step 2: 흡수 자료 검색 (Asset Searcher 페르소나)】
  - search_paths ($BOOK_ROOT·Obsidian vault·등록 자료 폴더) grep·glob
  - 시드 keyword·시그니처 어휘 매칭
  - inbox/ 미처리 파일 우선 확인

【Step 3: 권위 5층 등급화 (Authority Grader 페르소나)】
  - 발견 자료의 source_type·author·publication 분석
  - citation-authority-db.yaml 매칭
  - Grade A·B·C·D·E 등급 부여
  - Grade out 발견 시 풀에서 제외

【Step 4: 정량 앵커 추출 (Quantitative Anchor Extractor 페르소나)】
  - 수치·날짜·% 등 정량 표현 자동 추출
  - 저자 정량 표현 패턴: "100배 스케일"·"90% 확신"·"2027 임계점"·"5억 명"
  - 정량 앵커별 source_file 명시

【Step 5: 검증 신호 발견 (Verification Signal Finder 페르소나)】
  - 저자 v1 R5 verification_signal·falsifies_if 필드 발견
  - "5년·10년 후 어떤 지표가 검증·반증할까?" 추출

【Step 6: forecast-registry 갱신】
  - 신규 예측 (P-NNN) 등록
  - 기존 예측에 새 evidence 연결

【Step 7: Citation Gate 자동 발동 ⭐】
  - 모든 evidence에 citation-gate 검증
  - source_file 실재 확인
  - 메타데이터 완전성 확인
  - 할루시네이션 의심 → Critical 즉시 차단
  - R4 다층 확인 (단일 권위 evidence는 풀에서 제외)

【Step 8: 저자 묶음 (모드 1) — 채택 evidence 선택】
  - 수집된 evidence (예: 25개) 중 저자 묶음에 정돈
  - Grade A·B 우선 ★ 추천
  - 저자가 *채택 evidence 선택*

【Step 9: 산출 갱신】
  - chapters/<ch>/evidence-track.yaml에 채택 evidence 등록
  - seed-registry의 progress.evidence_collected·linked_predictions 갱신
  - 시드 lifecycle EXPANDED → EVIDENCED 진행
```

---

## 8. Input Schema

```typescript
{
  mode: "cycle" | "search" | "quantitative" | "verification-signal"
  target: string         // ch-NNN | S-NNN | query
  options: {
    layer?: "A" | "B" | "C" | "D" | "E" | "A,B"
    max_evidence?: number       // 기본 20
    min_authority?: "A" | "B" | "C"
  }
}
```

**파일 입력**: book-config / seed-registry / forecast-registry / search_paths / inbox

---

## 9. Output Schema

### 저자 화면
```markdown
# ④ evidence-collect — ch01-economy

## 발굴 evidence (총 25개)

### Layer A (창업자 증언) — 8개
- (a) ★ Amodei 2024 "Machines of Loving Grace" — "1-3년 90% 확신"
  - source_file: $BOOK_ROOT/inbox/2026-05-20-amodei-machines.md
  - 정량: 1-3년·90%
- (b) ★ Hassabis Davos 2025 — "AlphaFold 50년 난제 해결"
- ...

### Layer B (미래학자) — 5개
- (a) ★ 저자 칼럼 2024 "AGI 메타도구"
- ...

### Layer C·D·E — 12개

## 정량 앵커 추출 (15건)
- 100배 스케일 (산업혁명) — Layer A·D 권위
- 2027 임계점 — Layer A
- 5억 명 영향 — Layer C
- ...

## 검증 신호 (5건)
- "5년 후 한국 자율주행 택시 점유율 30% 도달?" (verification_signal)
- "2027년 AGI 미도래 시 본 책 명제 1 반증" (falsifies_if)
- ...

저자: "1=a,b,c / 2=a / 3=skip"
```

### 파일 갱신
- `chapters/<ch>/evidence-track.yaml`
- `forecast-registry.yaml` (신규 P-NNN 등록)
- `seed-registry.yaml` (lifecycle EVIDENCED 진행)

---

## 10. Deliverable Quality

### 정량 기준
- 발굴 evidence: 15-30개/챕터
- Grade A·B 비율: 60%+ (권위 우위)
- 정량 앵커: 평균 0.6/evidence
- 검증 신호: 3-7건/챕터
- citation-gate 통과율: 95%+ (Critical 위반 < 5%)
- R4 다층 통과율: 100% (단일 권위 모두 제외)
- 할루시네이션 차단: 100%

### 정성 기준
- 저자 책 *권위 척추*에 부합
- 정량 앵커가 *저자 표현 패턴*에 정합 (100배·90% 확신 형식)
- 검증 신호가 *5년·10년 후 추적 가능*
- forecast-registry 일관성 유지

---

## 11. Dependencies

### 필수
- ③ systemlink 통과 (자산·시드 연결)
- search_paths (book-config)
- citation-authority-db.yaml
- forecast-registry.yaml

### 후속
- ⑤ evidence-link (근거 그래프)
- ⑥ insight-synthesis (통찰 후보 평가)

### 비의존
- 다른 스킬·web

---

## 12. Guards

### Citation Gate ⭐⭐⭐ (가장 엄격 적용)
- 모든 evidence 출력에 자동 발동
- Critical (할루시네이션) → 풀에서 *영구 제외* (재시도 안 함)
- R4 단일 권위 → 풀에서 제외
- 메타데이터 누락 → 저자 묶음 escalate

### Voice Gate
- 자동 발동 (출력 텍스트)

### Search 범위 가드
- search_paths 외 디렉토리 *절대* 검색 안 함 (옵션 A+ 원칙)

### Forecast Registry 동기화 가드
- 신규 예측 등록 시 *기존 P-NNN과 중복 검출*
- 중복 시 저자 알림 + 병합·신규 선택

---

## 13. AI Agents Personas (5명)

| # | 페르소나 | 역할 |
|---|---|---|
| 1 | **Asset Searcher** | search_paths grep·glob + inbox 우선 |
| 2 | **Authority Grader** | citation-authority-db 매칭 + 5층 등급 |
| 3 | **Quantitative Anchor Extractor ⭐** | 저자 정량 표현 패턴 추출 |
| 4 | **Verification Signal Finder** | R5 verification_signal·falsifies_if 발견 |
| 5 | **Forecast Registry Syncer** | forecast-registry 갱신·중복 검출 |

---

## 14. Cycle

| Cycle | 트리거 | 작동 |
|---|---|---|
| **C1: Chapter Evidence** | `cycle ch-NNN` | 챕터 풀 evidence 수집 |
| **C2: Seed Evidence** | `cycle S-NNN` | 단일 시드 evidence |
| **C3: Authority Layer Specific** | `search --layer A,B` | 특정 권위층만 |
| **C4: Quantitative Only** | `quantitative` | 정량 앵커만 |

---

## 15. Gates

| Gate | 검증 |
|---|---|
| **G1: Input** | EXPANDED 시드 ≥1개 |
| **G2: Citation Gate Pass** | Critical 0건·R4 100% |
| **G3: Authority Distribution** | Grade A·B 60%+ |

---

## 16. Error Handling

| 실패 | 대응 |
|---|---|
| 발굴 evidence 0개 | warning + 저자 알림 + ③ systemlink 재호출 권장 |
| Grade A·B 30% 미만 | warning + 저자 권위 외부 보강 권장 |
| citation-gate Critical 다수 | abort + 저자 알림 (수집 자료 자체에 문제) |
| forecast-registry 중복 | 저자 묶음 — 병합·신규·skip |

---

## 17. Verification Examples

### 검증 1: 챕터 evidence 수집
```bash
/bookwriting-evidence-collect cycle ch01-economy
✅ 25 evidence 발굴
✅ Grade A 8개 / B 5개 / C 7개 / D 3개 / E 2개
✅ 정량 앵커 15건
✅ 검증 신호 5건
✅ citation-gate 100% 통과 (Critical 0)
✅ R4 다층 100%
✅ forecast-registry 신규 P-NNN 4건 등록
✅ seed lifecycle EVIDENCED 진행
```

### 검증 2: 권위 A·B만 검색
```bash
/bookwriting-evidence-collect search "한계비용 제로" --layer A,B
✅ 발굴 7개 (Rifkin 1·Amodei 2·저자 칼럼 4)
✅ 모두 Grade A 또는 B
✅ source_file 실재 확인
```

### 검증 3: 정량 앵커 추출
```bash
/bookwriting-evidence-collect quantitative ch01-economy
✅ "100배 스케일" 자동 추출 (Layer A — Musk·Amodei)
✅ "90% 확신" 자동 추출 (Layer A — Amodei)
✅ "2027 임계점" 자동 추출 (Layer A·B)
```

### 검증 4: citation-gate 차단
```bash
# evidence 발굴 중 "한 보고서에 따르면..." 형식 발견
✅ citation-gate Critical 검출 (할루시네이션 의심)
✅ 해당 evidence 풀에서 영구 제외
✅ trace에 명시
```

### 검증 5: R4 단일 권위 제외
```bash
# evidence "AGI는 2026년 도래 (Musk만 인용)"
✅ R4 단일 권위 감지
✅ 풀에서 제외
✅ 저자 묶음: "다른 권위층 (Amodei·Hassabis) evidence 추가 필요"
```

### 검증 6: 검증 신호 발견
```bash
$ /bookwriting-evidence-collect verification-signal ch01-economy
✅ "5년 후 한국 자율주행 택시 점유율 30%?" (verification_signal)
✅ "2027 AGI 미도래 시 본 책 명제 1 반증" (falsifies_if)
✅ forecast-registry 해당 P-NNN에 추가
```

---

---

## 부록: 결정론·grill-me·9 항목·Mode 2·R1-R5

### 결정론 모듈
| 작업 | 모듈 |
|---|---|
| 자산 검색 (search_paths grep) | 자체 결정론 (`subprocess` + grep) |
| 권위 5층 매핑 | M3 AuthorityGrader |
| 정량 앵커 추출 | M4 QuantitativeAnchorExtractor |
| relevance 점수 | M6 relevance_scorer (BM25) |
| forecast-registry sync·R1-R5 검증 | M12 forecast_registry_syncer |
| 검증 신호 정규식 발견 | 자체 결정론 (R5 패턴 정규식) |
| citation gate Critical 강제 | M2 HallucinationDetector (Critical 차단) |

**LLM 추론 금지**: relevance 점수 추측·권위 등급 추측·검증 신호 누락 직관 판단.

### grill-me D# 매핑
| D# | §위치 |
|---|---|
| D9·D10 (evidence schema·권위) | §2 책임 |
| D16 (citation gate Critical) | §12 ⭐⭐⭐ |
| Q33-2 (권위 5층 통합) | §3 Philosophy |
| 저자 강조 "할루시네이션 없는 출처" | §2 + §10 +citation-gate |

### 9 항목
(a) §1+§2 / (b) §2 (저자 14단계 진북) / (c) §13 5 페르소나 / (d) §4 / (e) §3 / (f) §5+§3 / (g) §9 / (h) §16 / (i) 부록 ⭐

### Mode 2 자동
모드 2: Grade A·B만 자동 채택 (Grade C 이하 제외)·confidence > 0.75 threshold·저자 묶음 0회·결과 → `_simulations/`

### R1-R5 강제
| R1 quantitative_anchor: forecast-registry 갱신 시 모든 신규 P-NNN에 명시 |
| R2 chapter_role: evidence별 chapter_role 매핑 강제 |
| R3 system_loops: ③ systemlink와 연동·일관성 |
| R4 다층 강제: ⑤ evidence-link에서 통합 검증 |
| R5 verification_signal: §7 Step 5 발견 → forecast-registry 갱신 |

**End of SPEC: bookwriting-evidence-collect-master**

> ⭐ ④ evidence-collect는 *citation-gate가 가장 엄격 적용*되는 단계. 저자 책의 *학술 신뢰성 backbone*. 할루시네이션 차단·R4 다층·정량 앵커·검증 신호 모두 정밀 보장.
