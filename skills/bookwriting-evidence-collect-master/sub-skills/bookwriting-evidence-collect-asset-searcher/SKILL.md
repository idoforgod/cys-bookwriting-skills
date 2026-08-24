---
name: bookwriting-evidence-collect-asset-searcher
description: 부모 bookwriting-evidence-collect-master의 INTERNAL sub. inbox/ 미처리 우선 + search_paths 전체 grep·glob + Obsidian vault 정밀 검색 + M6 BM25 relevance ≥ 0.7 채택. search_paths 외 검색 영구 금지 (옵션 A+). ③ systemlink와 연동 가능.
when_to_use: bookwriting-evidence-collect-master Step 2 (Asset Searcher 페르소나)에서 자동 호출. EXPANDED 시드 cycle 진입 시. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-evidence-collect-asset-searcher

## TLDR

부모 bookwriting-evidence-collect-master의 ① 진입 sub. inbox/ 미처리 자료를 mtime 기준 우선 처리하고 search_paths ($BOOK_ROOT·Obsidian vault·등록 자료 폴더)를 결정론 grep·glob 한다. M6 BM25 relevance ≥ 0.7만 채택. search_paths 외 영구 금지 (옵션 A+).

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- `/bookwriting-evidence-collect cycle <target>` Step 2 자동
- `/bookwriting-evidence-collect search <query>` 모드도 본 sub 진입

## Detailed Methodology

### 1. 결정론 chain — inbox 우선 + search_paths grep + M6

```python
from pathlib import Path
from dataclasses import dataclass
from relevance_scorer import RelevanceScorer   # M6 BM25

@dataclass
class EvidenceAsset:
    source_file: str
    relevance: float
    is_inbox_unprocessed: bool       # inbox/ 우선 처리 플래그
    matched_keywords: list[str]
    excerpt: str                     # ±100 chars

def search_evidence_assets(
    seed: dict,
    search_paths: list[Path],
    inbox_path: Path,
    min_relevance: float = 0.7,
) -> list[EvidenceAsset]:
    """inbox 우선 + search_paths 결정론 검색."""
    scorer = RelevanceScorer()
    keywords = _extract_keywords(seed)
    results = []

    # Step 1-2: 시드 keyword 추출 + inbox/ 미처리 파일 우선 검색
    inbox_unprocessed = []
    if inbox_path.exists():
        # mtime 기준 최신 우선
        inbox_files = sorted(
            (p for p in inbox_path.glob("*.md")),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        for md_file in inbox_files:
            score, matched, excerpt = _score_file(md_file, keywords, scorer)
            if score >= min_relevance:
                results.append(EvidenceAsset(
                    source_file=str(md_file),
                    relevance=score,
                    is_inbox_unprocessed=True,
                    matched_keywords=matched,
                    excerpt=excerpt,
                ))
                inbox_unprocessed.append(str(md_file))

    # Step 3-4: search_paths 전체 + Obsidian vault grep·glob
    for path in search_paths:
        if not path.exists():
            continue
        # search_paths 외 영구 금지 (옵션 A+ §12 가드 — 부모 마스터 강제)
        for md_file in path.rglob("*.md"):
            if str(md_file) in inbox_unprocessed:
                continue   # 중복 방지
            score, matched, excerpt = _score_file(md_file, keywords, scorer)
            # Step 5: relevance 점수
            # Step 6: relevance ≥ 0.7 채택
            if score >= min_relevance:
                results.append(EvidenceAsset(
                    source_file=str(md_file),
                    relevance=score,
                    is_inbox_unprocessed=False,
                    matched_keywords=matched,
                    excerpt=excerpt,
                ))

    # inbox 우선 정렬 + relevance 내림차순
    results.sort(key=lambda a: (a.is_inbox_unprocessed, a.relevance), reverse=True)
    return results

def _score_file(md_file: Path, keywords: list[str], scorer) -> tuple:
    try:
        text = md_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return (0.0, [], "")
    matched = [kw for kw in keywords if kw in text]
    if not matched:
        return (0.0, [], "")
    score = scorer.score(text, keywords)
    idx = text.find(matched[0])
    excerpt = text[max(0, idx-100):idx+100]
    return (score, matched, excerpt)

def _extract_keywords(seed: dict) -> list[str]:
    keywords = [t for t in seed.get("text", "").split() if len(t) >= 2]
    keywords.extend(seed.get("signature_vocab", []))
    return list(set(keywords))
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-collect-subs.md SUB 1)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 시드 keyword + 시그니처 어휘 추출 | `_extract_keywords(seed)` |
| Step 2: inbox/ 미처리 파일 우선 검색 | `inbox_files` mtime 정렬 + `is_inbox_unprocessed=True` 플래그 |
| Step 3: search_paths 전체 grep·glob | `for path in search_paths: ... .rglob("*.md")` |
| Step 4: Obsidian vault (다수 파일) 정밀 검색 | search_paths에 등록된 vault 자동 포함 |
| Step 5: relevance 0-1 점수 | M6 BM25 `scorer.score()` |
| Step 6: relevance ≥ 0.7 자료만 풀에 채택 | `if score >= min_relevance` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | seed (dict) + search_paths (list[Path]) + inbox_path (Path) + min_relevance |
| Output | List[EvidenceAsset] — source_file·relevance·is_inbox_unprocessed·matched·excerpt |
| 후속 sub | `bookwriting-evidence-collect-authority-grader` |
| Dependencies | ③ systemlink 협업 가능 (자산 연결 정보 활용) + book-config search_paths |
| 결정론 모듈 | M6 RelevanceScorer (BM25) + 자체 pathlib·subprocess |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M6 BM25 결정론 + mtime 정렬 |
| #2 grill-me 원문 일치 | 명세 6 Step 1:1 환원 |
| #5 법적 위험 | search_paths 외 영구 금지 (옵션 A+ §12 가드 — 부모 마스터 강제) |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- search_paths 외 검색 0건 (옵션 A+ 가드)
- inbox 우선 처리 (mtime 기준)
- Obsidian vault에서 평균 5-10 자료 발견 (부모 §10 정량)
- relevance ≥ 0.7 채택률 60%+ (부모 §10)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-collect-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-evidence-collect-master.md` §7 Step 2 + §13 페르소나 1 + 부록 결정론 (subprocess + M6)
결정론 모듈: `lib/relevance_scorer.py` (M6 BM25)
옵션 A+ 가드: 부모 §3 + §12 (search_paths 외 *절대* 검색 안 함)
③ systemlink 협업: `bookwriting-systemlink-asset-searcher`와 데이터 공유 가능
