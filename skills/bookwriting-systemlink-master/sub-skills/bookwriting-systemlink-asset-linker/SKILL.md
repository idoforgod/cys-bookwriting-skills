---
name: bookwriting-systemlink-asset-linker
description: 부모 bookwriting-systemlink-master의 INTERNAL sub. seed-registry connections.linked_assets 결정론 갱신 + citation 메타데이터 자동 추출 (source_file·author·date·publication) + M3 AuthorityGrader 권위 등급 매핑 + citation_gate_verified 표시. data-schema-seed-registry SPEC 정합.
when_to_use: bookwriting-systemlink-master Step 3 (Asset Linker 페르소나)에서 자동 호출. Asset Searcher 또는 Obsidian Vault Searcher 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-systemlink-asset-linker

## TLDR

부모 bookwriting-systemlink-master의 자산 연결 sub. 발견 자산을 seed-registry connections.linked_assets에 결정론 연결하고 citation 메타데이터 (source_file·author·date·publication)를 자동 추출한다. M3 AuthorityGrader로 권위 등급 매핑 + citation_gate_verified 플래그.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Asset Searcher 통과 + Obsidian Vault Searcher 통과 후 → Step 3 자동

## Detailed Methodology

### 1. 결정론 chain — citation 메타 추출 + M3 권위 등급

```python
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, asdict
from authority_grader import AuthorityGrader, Grade   # M3

@dataclass
class CitationMeta:
    source_file: str
    author: str | None
    date: str | None
    publication: str | None
    grade: str            # "A"|"B"|"C"|"D"|"E"
    citation_gate_verified: bool

def link_assets(seed_id: str, assets: list, authority_db_path: Path) -> list[CitationMeta]:
    """발견 자산을 seed-registry에 연결 + citation 메타 추출 + 권위 등급."""
    grader = AuthorityGrader(authority_db_path)
    results = []

    for asset in assets:
        # Step 1: 발견 자산별 seed 연결 결정 — relevance ≥ 0.7만 (부모 §12 가드)
        if asset.relevance < 0.7:
            continue

        # Step 2: seed-registry linked_assets에 추가 (실제 yaml write는 부모가 일괄)

        # Step 3: citation 메타데이터 자동 추출
        text = Path(asset.source_file).read_text(encoding="utf-8")
        meta = _extract_citation_meta(text, asset.source_file)

        # Step 4: M3 권위 등급화
        grade = grader.assign_grade(
            author=meta.get("author"),
            publication=meta.get("publication"),
            source_path=asset.source_file,
        )

        # Step 5: citation_gate_verified — source_file 실재 + 메타 완전성
        source_exists = Path(asset.source_file).exists()
        meta_complete = bool(meta.get("source_file") and meta.get("author"))
        verified = source_exists and meta_complete

        results.append(CitationMeta(
            source_file=asset.source_file,
            author=meta.get("author"),
            date=meta.get("date"),
            publication=meta.get("publication"),
            grade=grade.value,
            citation_gate_verified=verified,
        ))

    return results

def _extract_citation_meta(text: str, source_file: str) -> dict:
    """frontmatter + 본문 패턴 매칭으로 citation 메타 결정론 추출."""
    meta = {"source_file": source_file}

    # frontmatter 우선 (yaml.safe_load)
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            try:
                fm = yaml.safe_load(text[4:end]) or {}
                if isinstance(fm, dict):
                    meta["author"] = fm.get("author")
                    meta["date"] = fm.get("date") or fm.get("created")
                    meta["publication"] = fm.get("publication") or fm.get("source")
            except yaml.YAMLError:
                pass

    # 본문 패턴 fallback — 자주 등장하는 인용 양식
    if not meta.get("author"):
        m = re.search(r"(?:저자|Author|by)\s*[:：]\s*([^\n]+)", text)
        if m:
            meta["author"] = m.group(1).strip()
    if not meta.get("date"):
        m = re.search(r"(\d{4})[-\s년]", text)
        if m:
            meta["date"] = m.group(1)

    return meta
```

### 2. 명세 §출처 (SPEC: bookwriting-systemlink-subs.md SUB 3)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 발견 자산별 seed 연결 결정 | `if asset.relevance < 0.7: continue` (부모 §12 가드) |
| Step 2: seed-registry linked_assets에 추가 | 부모 마스터가 yaml write (영속 자산 보호) |
| Step 3: citation 메타 자동 추출 (source_file·author·date·publication) | `_extract_citation_meta()` — frontmatter + 본문 정규식 |
| Step 4: citation-authority-db로 권위 등급 매핑 | M3 `grader.assign_grade()` |
| Step 5: citation_gate_verified 표시 | `source_exists and meta_complete` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | seed_id + assets (Asset Searcher + Vault Searcher 통합) + authority-db path |
| Output | List[CitationMeta] — source_file + author + date + publication + grade + verified |
| 후속 sub | `bookwriting-systemlink-cross-seed-linker` |
| Dependencies | Asset Searcher / Obsidian Vault Searcher 통과 |
| 결정론 모듈 | M3 AuthorityGrader + yaml.safe_load + 정규식 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | yaml.safe_load + 정규식 + M3 결정론 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 |
| #3 출처 명시 | citation 4 필드 (source_file·author·date·publication) 강제 추출 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- linked_assets 정합 (data-schema-seed-registry SPEC)
- citation 필드 100% 추출 (4 필드 — source_file·author·date·publication)
- 권위 등급 매핑 (M3 citation-authority-db 57+ 권위)
- 영속 자산 보호: 본 sub는 *산출만*. seed-registry write는 부모 마스터 (PHASE3B_HANDOFF §8)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-systemlink-subs.md` §SUB 3
부모 마스터 SPEC: `specs/bookwriting-systemlink-master.md` §7 Step 3 + §13 페르소나 2 + 부록 결정론 (M3)
결정론 모듈: `lib/authority_grader.py` (M3) + yaml.safe_load + 정규식
영속 자산 보호: PHASE3B_HANDOFF §8
