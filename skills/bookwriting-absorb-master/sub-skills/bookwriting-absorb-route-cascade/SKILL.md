---
name: bookwriting-absorb-route-cascade
description: 부모 bookwriting-absorb-master의 INTERNAL sub. 저자 Q20-D-3 (d) 3-Layer cascade 라우팅 (L1 키워드 매칭 skeleton.md → L2 Claude 의미 평가 → L3 Obsidian vault 풀 참조). M6 relevance_scorer 결정론 호출. 저자 명시 (--to·--link) 시 cascade skip.
when_to_use: bookwriting-absorb-master Step 6 (Route Cascade 페르소나)에서 자동 호출. Type Classifier가 type 결정 후 (PROCEED) + 저자가 라우팅 명시 안 한 경우. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-absorb-route-cascade

## TLDR

부모 bookwriting-absorb-master의 ⭐ 라우팅 핵심 sub. type 분류된 자산을 챕터·layer·section·chapter_role에 매핑하는 *3-Layer cascade* (L1 키워드 → L2 의미 → L3 Obsidian 풀). M6 relevance_scorer로 점수 산출. 저자 명시 시 cascade skip.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Type Classifier 통과 + `--to`·`--link` 명시 *없음* → Step 6 자동
- 저자 명시 시 (--to ch01·--link S-001) → cascade skip + 명시값 직접 사용
- `/bookwriting-absorb route <S-NNN>` 모드는 라우팅 cascade만 단독 실행

## Detailed Methodology

### 1. 결정론 chain — 3-Layer cascade (저자 Q20-D-3 (d))

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class RouteCandidate:
    chapter: str            # ch-NNN
    layer: int              # 1·2·3
    section: str
    chapter_role: str
    confidence: float       # 0.0-1.0
    cascade_layer: str      # "L1_keyword" | "L2_semantic" | "L3_obsidian"

def cascade_route(asset_text: str, skeleton_path: Path, obsidian_paths: list[Path]) -> RouteCandidate:
    """3-Layer cascade — 저자 옵션 D 결정론 환원."""
    # L1: skeleton.md 키워드 매칭 (결정론 M6 relevance_scorer)
    from relevance_scoring import RelevanceScorer   # M6
    scorer = RelevanceScorer()
    l1_score = scorer.score_against_skeleton(asset_text, skeleton_path)
    if l1_score.best.score >= 0.8:
        return RouteCandidate(
            chapter=l1_score.best.chapter,
            layer=l1_score.best.layer,
            section=l1_score.best.section,
            chapter_role=l1_score.best.role,
            confidence=l1_score.best.score,
            cascade_layer="L1_keyword",
        )

    # L2: Claude 의미 평가 (LLM 허용 — confidence 점수는 결정론)
    # skeleton 외골격 + 자산 텍스트 의미 비교 → confidence 산출
    l2_confidence = _semantic_eval(asset_text, l1_score)
    if l2_confidence >= 0.7:
        return RouteCandidate(
            chapter=l1_score.best.chapter,
            layer=l1_score.best.layer,
            section=l1_score.best.section,
            chapter_role=l1_score.best.role,
            confidence=l2_confidence,
            cascade_layer="L2_semantic",
        )

    # L3: Obsidian vault 참조 (M6 relevance_scorer + 저자 기존 글 패턴)
    l3_score = scorer.score_against_obsidian(asset_text, obsidian_paths)
    return RouteCandidate(
        chapter=l3_score.best.chapter,
        layer=l3_score.best.layer,
        section=l3_score.best.section,
        chapter_role=l3_score.best.role,
        confidence=l3_score.best.score,
        cascade_layer="L3_obsidian",
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-absorb-subs.md SUB 3)

| 명세 cascade | 본 sub 구현 |
|---|---|
| L1: skeleton.md 키워드 매칭 (≥ 0.8 명확) | `scorer.score_against_skeleton` + `score >= 0.8` 분기 |
| L2: Claude 의미 평가 (confidence < 0.7 → L3) | `_semantic_eval` + `l2_confidence >= 0.7` |
| L3: Obsidian vault 참조 — 저자 패턴 라우팅 추론 | `scorer.score_against_obsidian` |
| 저자 명시 (--to·--link) 시 cascade skip | 부모 마스터가 본 sub 호출 자체 skip |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | asset_text (str) + skeleton.md path + Obsidian vault paths |
| Output | RouteCandidate (chapter, layer, section, chapter_role, confidence, cascade_layer) |
| 후속 sub | `bookwriting-absorb-inbox-organizer` (등록 완료 후 정리) |
| Dependencies | Type Classifier 통과 + book-config search_paths (Obsidian vault) |
| 결정론 모듈 | M6 relevance_scorer |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M6 relevance_scorer 결정론 점수·LLM은 의미 평가만 |
| #2 grill-me 원문 일치 | Q20-D-3 (d) 옵션 그대로 + cascade 임계값 0.8·0.7 명시 |
| #4 저자 작가성 | 저자 명시 시 cascade skip — 저자 의도 우선 |
| #7 결정론 환원 | M6·confidence 점수 100% 결정론 |

### 5. Verification (명세 §7)

- cascade L1-L3 confidence 흐름 명확 (cascade_layer 필드 trace)
- 저자 spot-check 정확도 80%+ (명세 §10 정량 기준)
- L3까지도 confidence < 0.5 → unrouted + 저자 묶음 (부모 마스터 §12 가드)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-absorb-subs.md` §SUB 3 ⭐
부모 마스터 SPEC: `specs/bookwriting-absorb-master.md` §7 Step 6 + §13 페르소나 3 + 부록 결정론 (L3 Obsidian = M6)
저자 옵션: Q20-D-3 (d) cascade
결정론 모듈: `lib/relevance_scoring.py` (M6)
