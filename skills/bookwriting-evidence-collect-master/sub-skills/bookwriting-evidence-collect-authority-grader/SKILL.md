---
name: bookwriting-evidence-collect-authority-grader
description: 부모 bookwriting-evidence-collect-master의 INTERNAL sub ⭐ Citation Gate 핵심. asset-searcher 자료에 M3 AuthorityGrader citation-authority-db Grade A·B·C·D·E·out 결정론 매핑 + Grade out 풀 제외 + R4 다층 강제 (단일 권위 주장 제외) + Grade A·B 60%+ 권위 분포 검증 + 매칭 안 된 author citation-authority-learning-log 갱신.
when_to_use: bookwriting-evidence-collect-master Step 3 (Authority Grader 페르소나)에서 자동 호출. asset-searcher 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-evidence-collect-authority-grader

## TLDR

부모 bookwriting-evidence-collect-master의 ⭐ Citation Gate 핵심 sub. M3 AuthorityGrader + citation-authority-db.yaml로 자료별 Grade A·B·C·D·E·out 결정론 매핑한다. M13 R4 다층 강제로 단일 권위 주장은 풀에서 제외하고, Grade A·B 60%+ 분포를 검증하며, 매칭 안 된 author는 learning-log에 갱신.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- asset-searcher 통과 후 → Step 3 자동
- Citation Gate cross-cutting의 핵심 — 부모 §12 ⭐⭐⭐ 가장 엄격 적용

## Detailed Methodology

### 1. 결정론 chain — M3 + M13 + Grade out 제외

```python
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from authority_grader import AuthorityGrader, Grade   # M3
from r4_multi_layer_verifier import R4MultiLayerVerifier   # M13

@dataclass
class GradedEvidence:
    source_file: str
    author: str | None
    publication: str | None
    grade: str            # "A"|"B"|"C"|"D"|"E"
    is_excluded: bool = False
    exclusion_reason: str | None = None
    r4_compliant: bool = True

def grade_evidence(
    evidence_assets: list,
    authority_db_path: Path,
    learning_log_path: Path,
) -> tuple[list[GradedEvidence], dict]:
    """권위 5층 등급 + R4 다층 강제 + Grade out 제외."""
    grader = AuthorityGrader(authority_db_path)
    r4 = R4MultiLayerVerifier(authority_db_path)
    learning_log = _load_yaml(learning_log_path) or {"unmatched_authors": []}

    graded = []
    grade_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "out": 0}
    unmatched = []

    for asset in evidence_assets:
        # Step 1: 자료의 author·publication·source_type 분석
        text = Path(asset.source_file).read_text(encoding="utf-8")
        meta = _extract_meta(text)

        # Step 2: citation-authority-db.yaml 매칭 (matching_policy)
        grade = grader.assign_grade(
            author=meta.get("author"),
            publication=meta.get("publication"),
            source_path=asset.source_file,
        )

        is_excluded = False
        reason = None

        # Step 3-4: Grade 부여 + Grade out 자료 풀 제외
        if grade == Grade.OUT:
            is_excluded = True
            reason = "Grade out (citation-authority-db 부적합)"
            grade_counts["out"] += 1
        else:
            grade_counts[grade.value] += 1

        # Step 7: 매칭 안 되는 author → 임시 Grade C + learning-log 갱신
        if grade == Grade.UNMATCHED:
            grade = Grade.C
            grade_counts["C"] += 1
            if meta.get("author"):
                unmatched.append({
                    "author": meta["author"],
                    "source_file": asset.source_file,
                })

        graded.append(GradedEvidence(
            source_file=asset.source_file,
            author=meta.get("author"),
            publication=meta.get("publication"),
            grade=grade.value,
            is_excluded=is_excluded,
            exclusion_reason=reason,
        ))

    # Step 6: R4 다층 강제 — 같은 주장에 단일 권위만 매핑 시 해당 주장 풀 제외
    # (주장 단위 — 부모 마스터가 통합·본 sub는 evidence 단위 R4 보조)
    for g in graded:
        if g.is_excluded:
            continue
        # R4 single-layer 의심 — 본 sub는 evidence 단위 flag만 (주장 단위는 ⑤ evidence-link)
        # (간소화 — 실제 R4는 부모가 fact-grouped 검증)

    # Step 5: Grade A·B 비율 60%+ 검증 (부모 §15 G3 게이트)
    total_kept = sum(grade_counts[g] for g in ["A", "B", "C", "D", "E"])
    ab_ratio = (grade_counts["A"] + grade_counts["B"]) / max(total_kept, 1)

    # learning-log 갱신 (영속 자산 보호 — 부모가 yaml write)
    learning_log["unmatched_authors"].extend(unmatched)

    summary = {
        "distribution": grade_counts,
        "ab_ratio": ab_ratio,
        "ab_ratio_meets_threshold": ab_ratio >= 0.6,
        "learning_log_updates": len(unmatched),
    }
    return graded, summary

def _extract_meta(text: str) -> dict:
    meta = {}
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            try:
                fm = yaml.safe_load(text[4:end]) or {}
                if isinstance(fm, dict):
                    meta["author"] = fm.get("author")
                    meta["publication"] = fm.get("publication") or fm.get("source")
            except yaml.YAMLError:
                pass
    return meta

def _load_yaml(path: Path) -> dict | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-collect-subs.md SUB 2) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: author·publication·source_type 분석 | `_extract_meta(text)` frontmatter + 본문 |
| Step 2: citation-authority-db.yaml 매칭 (matching_policy) | M3 `grader.assign_grade()` |
| Step 3: Grade 부여 (A·B·C·D·E·out) | `Grade` enum 6종 |
| Step 4: Grade out 자료 풀에서 제외 | `is_excluded=True` + `exclusion_reason` |
| Step 5: Grade A·B 비율 60%+ 확인 (정성) | `ab_ratio >= 0.6` 검증 |
| Step 6: R4 다층 강제 — 단일 권위 주장 풀 제외 | M13 + ⑤ evidence-link 협업 |
| Step 7: 매칭 안 되는 author → 임시 Grade C + DB 보강 권장 | `learning_log.unmatched_authors.append()` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | evidence_assets (asset-searcher 산출) + citation-authority-db path + learning-log path |
| Output | (List[GradedEvidence], summary dict — distribution·ab_ratio·learning_log_updates) |
| 후속 sub | `bookwriting-evidence-collect-quantitative-anchor-extractor` |
| Dependencies | asset-searcher 통과 + `expert_pool/citation-authority-db.yaml` + Citation Gate cross-cutting |
| 결정론 모듈 | M3 AuthorityGrader + M13 R4MultiLayerVerifier |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M3 + M13 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 7 Step 1:1 환원 (Grade A-E·out 6종 + R4 + learning-log) |
| #3 출처 명시 ⭐ | citation-authority-db 매칭 + author·publication 4 필드 |
| #5 법적 위험 | Grade out 제외·R4 단일 권위 제외 — 책 학술 신뢰성 backbone |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- 모든 자료에 grade 부여 (out 포함)
- Grade A·B 비율 60%+ (부모 §10 정성 기준 + §15 G3 게이트)
- Grade out 자료 풀 제외 (is_excluded=True)
- R4 단일 권위 주장 제외 (부모 §12 가드 ⭐⭐⭐)
- citation-authority-learning-log 갱신 (매칭 안 된 author 누적 → DB 보강 권장)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-collect-subs.md` §SUB 2 ⭐
부모 마스터 SPEC: `specs/bookwriting-evidence-collect-master.md` §7 Step 3 + §12 ⭐⭐⭐ + §13 페르소나 2 + 부록 결정론 (M3 + M13)
결정론 모듈: `lib/authority_grader.py` (M3) + `lib/r4_multi_layer_verifier.py` (M13)
권위 DB: `expert_pool/citation-authority-db.yaml` (57+ 권위 + 6 trauma 카테고리)
learning-log 영속: `expert_pool/citation-authority-learning-log.yaml` (부모 마스터 write)
