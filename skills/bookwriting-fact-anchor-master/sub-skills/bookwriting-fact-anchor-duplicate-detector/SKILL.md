---
name: bookwriting-fact-anchor-duplicate-detector
description: 부모 bookwriting-fact-anchor-master의 INTERNAL sub. fact 풀에서 의미 유사 fact (Levenshtein < 3) 그룹화 + M3 AuthorityGrader 권위 등급 비교 + primary/secondary 자동 선택. 동일 fact 다출처 시 가장 권위 높은 출처가 primary.
when_to_use: bookwriting-fact-anchor-master Step 4 (Duplicate Detector 페르소나)에서 자동 호출. Fact Extractor 산출 fact 풀이 입력. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-fact-anchor-duplicate-detector

## TLDR

부모 bookwriting-fact-anchor-master의 중복 검출 sub. M10 `detect_duplicates` (Wagner-Fischer Levenshtein < 3) + M3 AuthorityGrader로 같은 fact 다출처 그룹의 primary/secondary를 자동 결정한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Fact Extractor 통과 후 Step 4 자동
- `/bookwriting-fact-anchor cycle <target>` 진행 중

## Detailed Methodology

### 1. 결정론 chain — M10 + M3 호출

```python
from fact_extractor import FactExtractor, FactCandidate    # M10
from authority_grader import AuthorityGrader, Grade        # M3
from pathlib import Path
from dataclasses import dataclass

@dataclass
class DuplicateGroup:
    primary_fact_id: str
    secondary_fact_ids: list[str]
    primary_grade: Grade    # A·B·C·D·E
    primary_source: str

def detect_duplicates(fact_pool: list, authority_db_path: Path) -> list[DuplicateGroup]:
    """fact 풀 N×N 의미 유사도 비교 + 권위 등급 비교 + primary 선정."""
    extractor = FactExtractor()
    grader = AuthorityGrader(authority_db_path)

    # Step 1: 의미 유사도 그룹화 (M10 detect_duplicates — Levenshtein < 3)
    fact_candidates = [
        FactCandidate(f.fact_id, f.text, f.source_position, f.fact_type)
        for f in fact_pool
    ]
    groups: list[list[str]] = extractor.detect_duplicates(fact_candidates)

    # Step 2: 각 그룹 권위 등급 비교 → primary 선정
    result = []
    pool_by_id = {f.fact_id: f for f in fact_pool}
    for group_ids in groups:
        graded = []
        for fid in group_ids:
            f = pool_by_id[fid]
            # M3 권위 등급 (source_file의 저자/매체로 평가)
            grade = grader.assign_grade(source_path=f.source_file)
            graded.append((fid, grade, f.source_file))

        # Step 3: 가장 권위 높은 출처 → primary (Grade A > B > C > D > E)
        graded.sort(key=lambda g: g[1].rank)   # A=0 < B=1 < ...
        primary = graded[0]
        secondary_ids = [g[0] for g in graded[1:]]

        result.append(DuplicateGroup(
            primary_fact_id=primary[0],
            secondary_fact_ids=secondary_ids,
            primary_grade=primary[1],
            primary_source=primary[2],
        ))

    return result
```

### 2. 명세 §출처 (SPEC: bookwriting-fact-anchor-subs.md SUB 2)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: fact 풀 N×N 비교 (의미 유사도) | M10 `detect_duplicates()` — Wagner-Fischer Levenshtein < 3 |
| Step 2: 중복 fact 그룹화 | `groups: list[list[str]]` |
| Step 3: 각 그룹 권위 등급 비교 (citation-authority-db) | M3 `grader.assign_grade(source_path=...)` |
| Step 4: 가장 권위 높은 출처 → primary | `graded.sort(key=lambda g: g[1].rank)` |
| Step 5: 다른 출처 → secondary cross-reference | `secondary_fact_ids` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | fact_pool (list[AnchoredFact]) + citation-authority-db.yaml path |
| Output | List[DuplicateGroup] — primary_fact_id + secondary_fact_ids + primary_grade |
| 후속 sub | `bookwriting-fact-anchor-conflict-detector` |
| Dependencies | Fact Extractor 통과 + `expert_pool/citation-authority-db.yaml` |
| 결정론 모듈 | M10 detect_duplicates + M3 AuthorityGrader |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M10 + M3 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 |
| #3 출처 명시 | M3 권위 등급 + primary_source 필수 |
| #7 결정론 환원 | Wagner-Fischer + sort 100% 결정론 |

### 5. Verification (명세 §7)

- 중복 검출 정확도 95%+ (M10 Levenshtein 회귀 — Round 9 #E10.1 Critical 수정 완료)
- 권위 등급 비교 정합 (M3 citation-authority-db 57+ 권위)
- primary 자동 선택 — 동급 시 *수렴의 놀라움* 시그니처 (Musk·Amodei·Hassabis 사례 — 부모 §17 검증 5)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-fact-anchor-subs.md` §SUB 2
부모 마스터 SPEC: `specs/bookwriting-fact-anchor-master.md` §7 Step 4 + §13 페르소나 2 + 부록 결정론 (M10·M3)
결정론 모듈: `lib/fact_extractor.py` (M10) + `lib/authority_grader.py` (M3)
권위 DB: `expert_pool/citation-authority-db.yaml`
