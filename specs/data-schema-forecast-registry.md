# SPEC: data-schema-forecast-registry.yaml

> ⚠ Round 5 #B4.1·#A4.1 High 결함 수정 — *forecast-registry 전용 schema* 신규.
> 저자 v1 인프라의 핵심 자산 (130 예측·7 시스템 루프·6층 권위·3대 한국 윈도우)을 *bookwriting v2 데이터 모델*에 통합.
>
> 작성일: 2026-05-24

---

## 1. Identity

| 항목 | 값 |
|---|---|
| Schema 이름 | `forecast-registry.yaml` |
| 카테고리 | Data Schema (예측 마스터 — v1 인프라 흡수) |
| 파일 위치 | `$BOOK_ROOT/master/forecast-registry.yaml` (v1 기존) |
| 작성·갱신 주체 | bookwriting-master + ② fact-anchor·④ evidence-collect·⑪ cross-chapter-relink·M12 forecast_registry_syncer |
| 저자 v1 호환 | chapter-pipeline.md R1-R5 규칙 직접 호환 |

---

## 2. Purpose

저자 미래학 단행본의 *모든 예측*을 *단일 진실 공급원*으로 추적. R1-R5 정합성·권위 5층·시스템 루프·정량 앵커·검증 신호 모두 yaml 단일 파일에서 관리.

---

## 3. Structure (필수 필드)

```yaml
version: "2.0"
schema: forecast-registry
created: 2026-05-05      # v1 저자 작성 일자
last_updated: 2026-05-24
prediction_count: 130
next_id: P-131

predictions:
  - id: P-001
    statement: "..."                           # 예측 본문
    chapter: ch00-prologue                      # R2 chapter_role 정합
    chapter_role: 1층_콜드오픈                  # v1 chapter-pipeline R2
    
    # R1 정량 앵커
    quantitative_anchor:
      - value: "1-3년"
        source_file: $BOOK_ROOT/inbox/2024-amodei-machines.md
      - value: "90% 확신"
        source_file: $BOOK_ROOT/inbox/2024-amodei-machines.md
    
    # R3 시스템 루프
    system_loops:
      - loop_id: L1
        variable: "변수 1 — 인지 외주화"
    
    # R4 권위 5층 (다층 강제)
    authority_layers:
      - grade: A
        author: "Dario Amodei"
        publication: "Machines of Loving Grace"
        date: "2024-10-11"
        citation_text: "..."
        page_or_section: "Section 2"
      - grade: D
        author: "Yuval Noah Harari"
        publication: "21 Lessons"
        date: "2018"
    
    # R5 검증 신호
    verification_signal: "2027년 AI 연구원 수준 도달 여부"
    falsifies_if: "2030년까지 AGI 미도래 시 본 예측 반증"
    
    # bookwriting v2 확장
    linked_seeds: [S-001, S-007]          # seed-registry 참조
    used_in_chapters: [ch00, ch01, ch08]   # 다중 챕터 cross-reference
    
    citation_authority_distribution:
      A: 2
      B: 1
      C: 0
      D: 1
      E: 0
    
    # 변경 이력
    history:
      - timestamp: 2026-05-05T...
        action: CREATED
        cycle_id: null
      - timestamp: 2026-05-24T...
        action: AUTHORITY_LAYER_ADDED
        cycle_id: C-007
        layer_added: D
```

---

## 4. Validation Rules (R1-R5 결정론 검증)

| 규칙 | 검증 | M12 함수 |
|---|---|---|
| R1 quantitative_anchor | 모든 P-NNN에 ≥1 anchor + source_file | `verify_r1_quantitative_anchor()` |
| R2 chapter_role | enum [1층_콜드오픈·2층_분석·3층_함의] | `verify_r2_chapter_role()` |
| R3 system_loops | enum [L1-L7] + variable 명시 | `verify_r3_system_loops()` |
| R4 권위 5층 | authority_layers의 *unique grade* ≥ 2 | M13 `R4MultiLayerVerifier` |
| R5 verification_signal | verification_signal·falsifies_if 모두 명시 | `verify_r5_verification_signal()` |

---

## 5. Lifecycle

- **생성**: v1 저자 chapter-pipeline 작업 시 (2026-05-05)
- **갱신**: ②·④·⑤·⑪ 단계 자동 갱신 (M12 syncer)
- **삭제 없음**: 영속 자산 (5년·10년 후 검증)
- **아카이브**: 100 예측 초과 시 별도 정책 (book-config.yaml과 동일)

---

## 6. Dependencies
- v1 chapter-pipeline.md (호환 표준)
- seed-registry.yaml (linked_seeds 양방향)
- 모든 ②·④·⑤·⑪ 단계 마스터

---

## 7. Verification

```bash
# R1-R5 결정론 검증
$ python lib/forecast_registry_syncer.py verify_all
✅ R1 통과: 130/130 (100%)
✅ R2 통과: 130/130
✅ R3 통과: 128/130 (2 P-NNN 시스템 루프 미명시)
✅ R4 다층 통과: 125/130 (5 P-NNN 단일 권위 — 저자 보강 권장)
✅ R5 통과: 130/130
```

**End of SPEC: data-schema-forecast-registry**
