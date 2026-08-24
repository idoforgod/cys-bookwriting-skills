---
name: citation-gate
description: 저자 책 학술 신뢰성 cross-cutting 가드. M2 HallucinationDetector + M3 AuthorityGrader + M4 QuantitativeAnchorExtractor 결정론 호출. 5 신호 자동 감지 — Critical 시 즉시 차단·재작성 안 함. 저자 진북 #1 (할루시네이션 0) + #3 (출처 명시) + #5 (법적 위험) backbone.
when_to_use: 모든 단계 마스터 출력에 cross-cutting 자동 발동. 저자 명시 `/citation-gate verify <text> --citation <metadata>` 호출도 가능.
---

# citation-gate (cross-cutting 메타 가드)

## TLDR

저자 책의 모든 인용·주장·근거가 *할루시네이션 없는 실재 출처*에 의해 뒷받침되도록 시스템적 강제. `lib/citation_detection.HallucinationDetector` + `lib/authority_grader.AuthorityGrader` 결정론 호출.

## Triggers

- 모든 단계 마스터 출력 직후 *자동 발동* (cross-cutting)
- `/citation-gate verify <text>` — 5 신호 즉시 검사
- `/citation-gate audit <chapter>` — 챕터 전체 인용 일괄 감사
- `/citation-gate authority-map <chapter>` — 권위 7층 분포 보고

## Detailed Methodology

### 1. 결정론 호출 (LLM 추론 영구 금지)

```python
import paths
from citation_detection import HallucinationDetector, CitationMetadata
from authority_grader import AuthorityGrader, Grade
from pathlib import Path

det = HallucinationDetector()
grader = AuthorityGrader(paths.authority_db_path())

citation = CitationMetadata(
    author="Dario Amodei",
    date="2024-10-11",
    publication="Anthropic",
    source_file=paths.inbox_dir() / "2024-amodei.md",
)
signals = det.detect_all(text, citation)
grade = grader.assign_grade(author=citation.author)

if signals.is_critical():
    # 즉시 차단 — 재작성 영구 금지
    escalate_to_user(signals, citation)
```

### 2. 5 할루시네이션 신호 (Round 4·9 누적)

1. source_file_missing — `Path.exists()` 결정론
2. source_format_vague — "한 보고서에 따르면" 등 정규식
3. metadata_incomplete — author·date·publication 누락
4. url_doi_invalid — URL·DOI 정규식
5. stat_no_source — 통계 + source_file 부재

### 3. 권위 7층 (A·A_preprint·B·C·D·E·F·G)

| Grade | Layer | 예시 |
|---|---|---|
| A | 1 | 창업자 증언·peer-reviewed (Amodei·Hassabis·WHO·IPCC) |
| A_preprint | 1 | arxiv·biorxiv (peer-review 전) |
| B | 2 | 저자 본인 (미래학자) |
| C | 3 | 인접 학문 (김대식·유현준·Zuboff·Crawford) |
| D | 4 | 사상가·역사가 (Harari·Turkle·Haraway) |
| E | 5 | 역사 평행 (대공황·러다이트) |
| F | 6 | 신학 권위 (Calvin·Bavinck·Augustine) |
| G | 7 | 토착 지혜 (이부영·서대석) |

### 4. R4 다층 인용 강제

```python
result = grader.verify_r4_multi_layer([Grade.A, Grade.D])
# {"layer_count": 2, "r4_pass": True, "action": "approve"}
```

### 5. 위반 시 처리 (Round 4 #Q33)

- **Critical** (할루시네이션 의심) → 즉시 차단·재작성 안 함·저자 묶음
- **High** (메타 누락·R4 단일 권위) → 저자 묶음 escalate
- **Medium** (Grade C·D만) → warning + 진행

### 6. trauma_bearing_witness_category (Round 17·18)

생존자·유가족·정치 박해 피해자 인용 시 자동 발동:
- consent_status: required_before_quote
- safe_messaging_invoke: true
- hotline_required: 한국 1393·109 명시 강제

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ M2 5 신호 결정론 + pytest 통과 |
| #3 출처 명시 | ✅ citation-authority-db 57 권위 + 7 grade |
| #5 법적 위험 | ✅ trauma_bearing_witness_category protocol |

## 출처

SPEC: `specs/citation-gate.md` (17 항목 풀)
실행 모듈: `lib/citation_detection.py` + `lib/authority_grader.py`
권위 DB: `expert_pool/citation-authority-db.yaml` (57 권위 entry)
