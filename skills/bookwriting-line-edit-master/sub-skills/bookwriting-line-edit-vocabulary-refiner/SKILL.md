---
name: bookwriting-line-edit-vocabulary-refiner
description: 부모 bookwriting-line-edit-master의 INTERNAL sub. 저자 preferred·avoid·prohibitions 어휘 정밀 치환 + 외국어 무분별 한국어 자동 치환 (framework→프레임워크·agent→에이전트) + book-config voice_guidelines.vocabulary 정합 + avoid 0건 + PROH-001 위반 0건 + before·after diff 보존.
when_to_use: bookwriting-line-edit-master cycle 진입 시 자동 첫 단계 (line-edit의 ① 진입 sub).
disable-model-invocation: true
---

# bookwriting-line-edit-vocabulary-refiner

## TLDR

부모 bookwriting-line-edit-master의 ① 진입 sub. ⑦ content-expand 통과 본문에 저자 voice_guidelines.vocabulary의 preferred·avoid·prohibitions를 결정론 치환한다. 외국어 한국어 자동 (PROH-001 위반 0건 목표). diff 자동 보존.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- ⑩ line-edit cycle 진입 시 자동 첫 단계
- voice-gate cross-cutting과 협업

## Detailed Methodology

### 1. 결정론 chain — preferred/avoid 치환 + 외국어 변환

```python
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class VocabularyRefinement:
    section_id: str
    original_text: str
    refined_text: str
    avoid_removed: list[tuple[str, str]]    # [(avoid, replacement)]
    foreign_replaced: list[tuple[str, str]]
    preferred_added: list[str]
    diff_count: int
    needs_bundle_decision: list[str]   # 자동 치환 안 한 곳 (저자 결정)

FOREIGN_TO_KOREAN = {
    "framework": "프레임워크",
    "agent": "에이전트",
    "tool": "도구",
    "system": "시스템",
    "context": "맥락",
    "loop": "루프",
    "feedback": "피드백",
}

def refine_vocabulary(
    sections: list[dict],         # ⑦ 통과 본문 chunks
    book_config_path: Path,
) -> list[VocabularyRefinement]:
    """preferred·avoid·외국어 결정론 치환."""
    # Step 1: book-config voice_guidelines.vocabulary 로드
    with book_config_path.open(encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    vocab = config.get("voice_guidelines", {}).get("vocabulary", {})
    preferred_words: list[str] = vocab.get("preferred", [])
    avoid_pairs: dict[str, str] = vocab.get("avoid", {}) or {}

    results: list[VocabularyRefinement] = []
    for sec in sections:
        original = sec["text"]
        refined = original
        avoid_removed: list[tuple[str, str]] = []
        foreign_replaced: list[tuple[str, str]] = []
        preferred_added: list[str] = []
        bundle_decision: list[str] = []

        # Step 2: avoid 표현 자동 감지·치환
        for avoid_word, replacement in avoid_pairs.items():
            if avoid_word in refined:
                refined = refined.replace(avoid_word, replacement)
                avoid_removed.append((avoid_word, replacement))

        # Step 3: preferred 어휘 *치환 기회* 발견 (강제 X — 자연스러운 곳만)
        for pref in preferred_words:
            if pref in refined and pref not in original:
                preferred_added.append(pref)

        # Step 4: 외국어 → 한국어 자동 치환 (PROH-001 위반 차단)
        for foreign, korean in FOREIGN_TO_KOREAN.items():
            # 단어 경계 정규식 — 한국어와 영어 혼재 시
            pattern = re.compile(rf"\b{foreign}\b", re.IGNORECASE)
            if pattern.search(refined):
                refined = pattern.sub(korean, refined)
                foreign_replaced.append((foreign, korean))

        # 자동 치환 안 한 외국어 — 저자 묶음
        remaining_foreign = re.findall(r"\b[a-zA-Z]{3,}\b", refined)
        if remaining_foreign:
            bundle_decision.extend(set(remaining_foreign))

        results.append(VocabularyRefinement(
            section_id=sec["section_id"],
            original_text=original,
            refined_text=refined,
            avoid_removed=avoid_removed,
            foreign_replaced=foreign_replaced,
            preferred_added=preferred_added,
            diff_count=len(avoid_removed) + len(foreign_replaced),
            needs_bundle_decision=bundle_decision,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-line-edit-subs.md SUB 1)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 본문 어휘 분석 (book-config voice_guidelines.vocabulary) | yaml.safe_load + vocab dict |
| Step 2: avoid 표현 자동 감지·치환 후보 생성 | `avoid_removed` + `replace()` |
| Step 3: preferred 어휘 *치환 기회* 발견 (강제 X) | `preferred_added` |
| Step 4: 외국어 → 한국어 자동 치환 (framework→프레임워크) | `FOREIGN_TO_KOREAN` |
| Step 5: 저자 묶음 (자동 치환 안 한 곳) | `needs_bundle_decision` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | sections (⑦ 통과 본문) + book_config_path |
| Output | List[VocabularyRefinement] — refined·diffs·bundle |
| 후속 sub | signature-applier (또는 sentence-rhythm-tuner) |
| Dependencies | ⑦ content-expand 통과 + voice-gate cross-cutting |
| 결정론 모듈 | yaml.safe_load + 정규식 + dict 치환 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | dict 치환 결정론 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 |
| #4 저자 작가성 | preferred 강제 X — 자연스러운 곳만 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- avoid 어휘 0건 (자동 치환)
- PROH-001 (외국어) 위반 0건
- preferred 어휘 사용 빈도 증가
- before·after diff 보존 (`diff_count`)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-line-edit-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-line-edit-master.md`
book-config voice_guidelines.vocabulary: preferred·avoid·prohibitions (변경 영구 금지)
PROH-001: 외국어 무분별 사용 prohibition
