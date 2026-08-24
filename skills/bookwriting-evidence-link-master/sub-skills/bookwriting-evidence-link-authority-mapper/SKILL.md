---
name: bookwriting-evidence-link-authority-mapper
description: 부모 bookwriting-evidence-link-master의 INTERNAL sub. 모든 그래프 노드를 M3 AuthorityGrader citation-authority-db 매칭 + Grade A-E 결정론 부여 + 매칭 안 되는 노드는 임시 Grade C + citation-authority-learning-log 갱신. 100% 등급 부여 강제.
when_to_use: bookwriting-evidence-link-master Step 4 (Authority Mapper 페르소나)에서 자동 호출. Edge Detector 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-evidence-link-authority-mapper

## TLDR

부모 bookwriting-evidence-link-master의 권위 매핑 sub. 모든 그래프 노드를 M3 AuthorityGrader로 citation-authority-db.yaml 결정론 매칭하고 Grade A-E를 부여한다. 매칭 안 되는 노드는 임시 Grade C + learning-log 갱신. 100% 등급 부여 강제.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Edge Detector 통과 후 → Step 4 자동

## Detailed Methodology

### 1. 결정론 chain — M3 AuthorityGrader 매핑

```python
from pathlib import Path
from dataclasses import dataclass
from authority_grader import AuthorityGrader, Grade   # M3

@dataclass
class AuthorityMappingResult:
    node_id: str
    grade: str               # "A"|"B"|"C"|"D"|"E"
    matched_db_entry: str | None
    is_temporary_c: bool = False
    log_recommendation: str | None = None

def map_authorities(nodes: list, authority_db_path: Path) -> tuple[list[AuthorityMappingResult], list[dict]]:
    """노드 100% 등급 부여 + 매칭 안 되는 노드 learning-log 갱신."""
    grader = AuthorityGrader(authority_db_path)
    results: list[AuthorityMappingResult] = []
    learning_log_updates: list[dict] = []

    for node in nodes:
        # Step 1: citation-authority-db 매칭
        grade = grader.assign_grade(
            author=node.author,
            source_path=node.source_file,
        )

        is_temporary = False
        log_rec = None

        # Step 2: 각 노드 grade 부여
        if grade == Grade.UNMATCHED:
            # Step 3: 매칭 안 되는 노드 → 임시 Grade C + DB 보강 권장
            grade = Grade.C
            is_temporary = True
            log_rec = f"매칭 안 됨: author={node.author or 'unknown'} — citation-authority-db 보강 권장"
            learning_log_updates.append({
                "node_id": node.node_id,
                "author": node.author,
                "source_file": node.source_file,
                "recommendation": log_rec,
            })

        results.append(AuthorityMappingResult(
            node_id=node.node_id,
            grade=grade.value,
            matched_db_entry=grader.last_matched_entry,
            is_temporary_c=is_temporary,
            log_recommendation=log_rec,
        ))

    return results, learning_log_updates
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-link-subs.md SUB 3)

| 명세 항목 | 본 sub 구현 |
|---|---|
| citation-authority-db 매칭 | M3 `grader.assign_grade()` |
| 각 노드 grade 부여 | AuthorityMappingResult.grade 필드 |
| 매칭 안 되는 노드는 임시 Grade C + DB 보강 권장 | `is_temporary_c=True` + `learning_log_updates.append()` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | nodes (Graph Builder 산출) + authority-db path |
| Output | (List[AuthorityMappingResult], learning_log_updates list) |
| 후속 sub | `bookwriting-evidence-link-r4-verifier` |
| Dependencies | Graph Builder 통과 + `expert_pool/citation-authority-db.yaml` |
| 결정론 모듈 | M3 AuthorityGrader |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M3 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 3 항목 1:1 환원 |
| #3 출처 명시 | grade·matched_db_entry 필수 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 100% 등급 부여 (UNMATCHED → 임시 Grade C로 강제 매핑)
- 매칭 안 되는 노드 learning-log 로그 (DB 보강 권장)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-link-subs.md` §SUB 3
부모 마스터 SPEC: `specs/bookwriting-evidence-link-master.md` §7 Step 4 + §13 페르소나 3 + 부록 결정론 (M3)
결정론 모듈: `lib/authority_grader.py` (M3)
권위 DB: `expert_pool/citation-authority-db.yaml`
learning-log 영속: `expert_pool/citation-authority-learning-log.yaml` (부모 마스터 단일 진입 write)
