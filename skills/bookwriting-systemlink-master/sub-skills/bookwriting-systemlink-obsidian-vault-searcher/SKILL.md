---
name: bookwriting-systemlink-obsidian-vault-searcher
description: 부모 bookwriting-systemlink-master의 INTERNAL sub ⭐. 저자 Obsidian vault (reference-vault, N .md) 정밀 검색 + wikilinks 그래프 추적 + tags 기반 라우팅 + 저자 *기존 사고 패턴* 강조. Asset Searcher와 통합되어 저자 시그니처 사고 풀 발견.
when_to_use: bookwriting-systemlink-master Step 2 (Asset Searcher 페르소나) 일부로 자동 호출. obsidian_only 옵션 또는 Asset Searcher가 Obsidian 경로를 만났을 때. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-systemlink-obsidian-vault-searcher

## TLDR

부모 bookwriting-systemlink-master의 ⭐ Obsidian 전용 정밀 sub. 저자 vault (reference-vault, N .md 파일)에서 grep·glob·wikilinks 그래프 추적·tags 라우팅으로 저자 *기존 사고 풀*과 시드를 연결한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Asset Searcher가 Obsidian search_paths 만남 → 본 sub 위임 자동
- `--obsidian_only` 옵션 시 단독 실행

## Detailed Methodology

### 1. 결정론 chain — vault grep + wikilinks 그래프

```python
import re
from pathlib import Path
from dataclasses import dataclass, field
from relevance_scorer import RelevanceScorer    # M6 BM25

@dataclass
class VaultAsset:
    source_file: str
    relevance: float
    matched_keywords: list[str]
    wikilinks: list[str] = field(default_factory=list)   # [[note-name]] 그래프
    tags: list[str] = field(default_factory=list)
    is_park_thinking_pattern: bool = False    # 저자 기존 사고 패턴 강조

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
TAG_PATTERN = re.compile(r"(?:^|\s)#([\w가-힣-]+)")

def search_obsidian_vault(seed: dict, vault_path: Path) -> list[VaultAsset]:
    """Obsidian vault 정밀 검색 — wikilinks 그래프 추적."""
    if not vault_path.exists():
        return []   # graceful — 부모 §16 (vault 접근 실패 warning + 계속)

    keywords = _extract_seed_keywords(seed)
    scorer = RelevanceScorer()

    # Step 1: vault 진입
    # Step 2: vault 구조 인식 (.md·wikilinks·tags)
    assets = []
    for md_file in vault_path.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        # Step 3: 시드 keyword 검색
        matched = [kw for kw in keywords if kw in text]
        if not matched:
            continue

        score = scorer.score(text, keywords)

        # Step 4: wikilinks·tags 추출 (그래프 추적)
        wikilinks = WIKILINK_PATTERN.findall(text)
        tags = TAG_PATTERN.findall(text)

        # Step 5: 저자 *기존 사고 패턴* 발견 강조
        # 저자 본인 노트 식별 — wikilinks 다수·시그니처 어휘 포함 시
        is_park = (
            len(wikilinks) >= 5
            and any(kw in seed.get("signature_vocab", []) for kw in matched)
        )

        assets.append(VaultAsset(
            source_file=str(md_file),
            relevance=score,
            matched_keywords=matched,
            wikilinks=wikilinks,
            tags=tags,
            is_park_thinking_pattern=is_park,
        ))

    # 저자 사고 패턴 우선 정렬
    assets.sort(key=lambda a: (a.is_park_thinking_pattern, a.relevance), reverse=True)
    return assets

def _extract_seed_keywords(seed: dict) -> list[str]:
    keywords = [t for t in seed.get("text", "").split() if len(t) >= 2]
    keywords.extend(seed.get("signature_vocab", []))
    return list(set(keywords))
```

### 2. 명세 §출처 (SPEC: bookwriting-systemlink-subs.md SUB 2)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: Obsidian vault 진입 | `vault_path.exists()` |
| Step 2: vault 구조 인식 (.md·wikilinks·tags) | `WIKILINK_PATTERN`·`TAG_PATTERN` 정규식 |
| Step 3: 시드 keyword 검색 | `kw in text` + M6 BM25 |
| Step 4: wikilinks 그래프 추적 | `WIKILINK_PATTERN.findall(text)` |
| Step 5: 저자 *기존 사고 패턴* 발견 시 강조 | `is_park_thinking_pattern` 가산 정렬 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | seed (dict) + vault_path (Path — book-config 등록) |
| Output | List[VaultAsset] — source_file + relevance + wikilinks + tags + is_park_thinking_pattern |
| 후속 sub | `bookwriting-systemlink-asset-linker` (vault 자산도 통합 등록) |
| Dependencies | book-config search_paths에 Obsidian 등록 + vault 접근 권한 |
| 결정론 모듈 | M6 RelevanceScorer + 자체 정규식 (wikilinks·tags) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | wikilinks·tags 정규식 + M6 BM25 결정론 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 (vault 다수 파일 명시) |
| #4 저자 작가성 | is_park_thinking_pattern 강조 — 저자 기존 사고와 연결 보장 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- vault 다수 파일 중 평균 5-15 발견 (부모 §17 검증 2)
- wikilinks 추적 정확 (정규식 회귀)
- vault 접근 실패 graceful (부모 §16 Obsidian 접근 실패 → 다른 search_paths 계속)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-systemlink-subs.md` §SUB 2 ⭐
부모 마스터 SPEC: `specs/bookwriting-systemlink-master.md` §7 Step 2 + §17 검증 2 (Obsidian vault 활용)
저자 vault: reference-vault (N .md, book-config 등록 — 옵션 A+ 영역 내)
결정론 모듈: `lib/relevance_scorer.py` (M6 BM25) + 정규식
