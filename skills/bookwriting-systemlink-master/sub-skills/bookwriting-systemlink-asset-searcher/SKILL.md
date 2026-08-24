---
name: bookwriting-systemlink-asset-searcher
description: 부모 bookwriting-systemlink-master의 INTERNAL sub. book-config.search_paths를 subprocess grep + pathlib glob으로 결정론 검색 + 시드 keyword·시그니처 어휘 매칭 + M6 relevance_scorer BM25 점수 산출. relevance ≥ 0.7 자료만 채택. search_paths 외 검색 영구 금지 (옵션 A+).
when_to_use: bookwriting-systemlink-master Step 2 (Asset Searcher 페르소나)에서 자동 호출. 시드·챕터 cycle 진입 시. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-systemlink-asset-searcher

## TLDR

부모 bookwriting-systemlink-master의 ① 진입 sub. search_paths ($BOOK_ROOT·등록 자료 폴더·Obsidian vault — book-config 등록 외 영구 금지)에서 시드 keyword를 grep·glob 결정론 검색하고 M6 BM25 relevance 점수를 산출한다. ≥ 0.7만 자산 풀에 채택.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- `/bookwriting-systemlink cycle <target>` Step 2 자동
- `/bookwriting-systemlink search <query>` 모드는 본 sub 단독 실행

## Detailed Methodology

### 1. 결정론 chain — subprocess grep + M6 relevance_scorer

```python
import subprocess
from pathlib import Path
from dataclasses import dataclass
from relevance_scorer import RelevanceScorer   # M6 BM25

@dataclass
class AssetCandidate:
    source_file: str
    relevance: float
    matched_keywords: list[str]
    excerpt: str            # ±100 chars context

def search_assets(seed: dict, search_paths: list[Path], min_relevance: float = 0.7) -> list[AssetCandidate]:
    """search_paths 결정론 검색 — 옵션 A+ 영구 가드."""
    # Step 1: 시드 keyword·시그니처 어휘 추출
    keywords = _extract_keywords(seed)

    # Step 2: search_paths 순회 (book-config 등록만 — 외부 영구 금지)
    candidates = []
    for path in search_paths:
        if not path.exists():
            continue   # warning만 (부모 §16 graceful)

        # Step 3: grep·glob 결정론 검색
        for md_file in path.rglob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            matched = [kw for kw in keywords if kw in text]
            if not matched:
                continue

            # Step 4: M6 relevance 점수 (BM25 — 키워드 빈도·맥락 일치)
            scorer = RelevanceScorer()
            score = scorer.score(text, keywords)

            # Step 5: ≥ 0.7 채택
            if score >= min_relevance:
                # excerpt 추출 (첫 매칭 ±100)
                idx = text.find(matched[0])
                excerpt = text[max(0, idx-100):idx+100]
                candidates.append(AssetCandidate(
                    source_file=str(md_file),
                    relevance=score,
                    matched_keywords=matched,
                    excerpt=excerpt,
                ))

    # 정렬: relevance 내림차순
    candidates.sort(key=lambda c: c.relevance, reverse=True)
    return candidates

def _extract_keywords(seed: dict) -> list[str]:
    """시드 text·signature_vocab에서 keyword 결정론 추출."""
    keywords = []
    text = seed.get("text", "")
    # 명사·고유명사 추출 (간소화 — 부모 마스터가 정규식 보강)
    keywords.extend([t for t in text.split() if len(t) >= 2])
    keywords.extend(seed.get("signature_vocab", []))
    return list(set(keywords))
```

### 2. 명세 §출처 (SPEC: bookwriting-systemlink-subs.md SUB 1)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 시드 keyword·시그니처 어휘 추출 | `_extract_keywords(seed)` |
| Step 2: search_paths 순회 ($BOOK_ROOT·등록 자료 폴더·Obsidian) | `for path in search_paths` — book-config 등록만 |
| Step 3: grep·glob 자료 발견 | `path.rglob("*.md")` + `kw in text` |
| Step 4: relevance 점수 (키워드 빈도·맥락 일치) | M6 `scorer.score(text, keywords)` BM25 |
| Step 5: ≥ 0.7 자료만 채택 | `if score >= min_relevance` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | seed (dict) + search_paths (list[Path], book-config) + min_relevance (기본 0.7) |
| Output | List[AssetCandidate] — source_file + relevance + matched_keywords + excerpt |
| 후속 sub | `bookwriting-systemlink-obsidian-vault-searcher` (Obsidian 정밀) + `bookwriting-systemlink-asset-linker` |
| Dependencies | ① absorb 통과 + book-config.search_paths |
| 결정론 모듈 | M6 RelevanceScorer (BM25) + 자체 subprocess+pathlib |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M6 BM25 결정론 + grep — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 |
| #5 법적 위험 | search_paths 외 영구 금지 (옵션 A+ §12 가드) |
| #7 결정론 환원 | BM25 + grep 100% 결정론 |

### 5. Verification (명세 §7)

- search_paths 외 검색 0건 (옵션 A+ 가드 — 부모 §12 + §3)
- relevance ≥ 0.7 채택 정확도 80%+ (부모 §10 정량)
- Obsidian vault 파일 평균 5-15 발견 (부모 §17 검증 2)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-systemlink-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-systemlink-master.md` §7 Step 2 + §13 페르소나 1 + 부록 결정론 (M6)
결정론 모듈: `lib/relevance_scorer.py` (M6 BM25)
옵션 A+ 가드: 부모 §3 + §12 (search_paths 외 검색 영구 금지)
