---
name: bookwriting-insight-synthesis-cross-chapter-check
description: "부모 bookwriting-insight-synthesis-master의 INTERNAL sub. 통찰의 다른 챕터 연결 결정론 발견 — 사상적 척추·시스템 루프 매핑 추출 + 다른 챕터 시드·통찰과 N×N 비교 + cross-reference 후보 (예: ch01 INS-001 → ch08 추가 매핑) 제시 + 저자 묶음 (cross-chapter 채택). M6 relevance_scorer BM25."
when_to_use: bookwriting-insight-synthesis-master에서 voice-craft 통과 후 자동 호출. bundle-builder 직전 단계. `/bookwriting-insight-synthesis cross-chapter` 모드 단독 가능.
disable-model-invocation: true
---

# bookwriting-insight-synthesis-cross-chapter-check

## TLDR

부모 bookwriting-insight-synthesis-master의 cross-chapter 연결 sub. 통찰의 사상적 척추·시스템 루프 매핑을 다른 챕터 시드·통찰과 N×N으로 비교하고 M6 BM25 relevance ≥ 0.7 시 cross-reference 후보를 제시한다. 저자 묶음 2 (cross-chapter 매핑) 입력 제공.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- voice-craft 통과 후 → 본 sub 자동
- `/bookwriting-insight-synthesis cross-chapter <target>` 모드는 본 sub 단독

## Detailed Methodology

### 1. 결정론 chain — N×N + M6 BM25 + 저자 묶음

```python
import yaml
from pathlib import Path
from dataclasses import dataclass
from relevance_scorer import RelevanceScorer   # M6 BM25

@dataclass
class CrossChapterCandidate:
    source_insight_id: str
    source_chapter: str
    target_chapter: str
    relevance: float            # M6 BM25
    matched_spine: list[str]    # 사상적 척추 매칭 (meaning-evaluation과 cross-ref)
    matched_loops: list[str]    # 시스템 루프 매핑 (③ systemlink와 cross-ref)

def check_cross_chapter(
    insights: list,              # voice-craft 통과 통찰
    source_chapter: str,
    all_chapters_seeds: dict,    # ch_id → list of seed dicts
    min_relevance: float = 0.7,
) -> list[CrossChapterCandidate]:
    """N×N + M6 BM25 결정론 cross-chapter 발견."""
    scorer = RelevanceScorer()
    results: list[CrossChapterCandidate] = []

    for ins in insights:
        # Step 1: 통찰의 사상적 척추·시스템 루프 매핑 추출
        # (meaning-evaluation·③ systemlink-system-loop-mapper와 cross-reference)
        ins_keywords = ins.crafted_text.split() if hasattr(ins, "crafted_text") else ins.text.split()

        # Step 2: 다른 챕터의 시드·통찰과 비교
        for ch_id, seeds in all_chapters_seeds.items():
            if ch_id == source_chapter:
                continue   # 자기 챕터 skip

            # 각 챕터의 시드·통찰을 통합 텍스트로 풀
            chapter_corpus = " ".join(s.get("text", "") for s in seeds)

            # Step 3: M6 BM25 relevance 점수
            score = scorer.score(chapter_corpus, ins_keywords)

            if score >= min_relevance:
                # 사상적 척추·루프 매핑 추출 (간소화 — 부모가 결합)
                matched_spine = []
                matched_loops = []

                results.append(CrossChapterCandidate(
                    source_insight_id=ins.insight_id,
                    source_chapter=source_chapter,
                    target_chapter=ch_id,
                    relevance=score,
                    matched_spine=matched_spine,
                    matched_loops=matched_loops,
                ))

    # Step 4: 저자 묶음 (cross-chapter 채택 선택) — bundle-builder가 markdown 조립
    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-insight-synthesis-subs.md SUB 8)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 통찰의 사상적 척추·시스템 루프 매핑 추출 | `ins_keywords` + meaning·systemlink cross-ref |
| Step 2: 다른 챕터의 시드·통찰과 비교 | `for ch_id in all_chapters_seeds` |
| Step 3: cross-reference 후보 발견 | `if score >= min_relevance` |
| Step 4: 저자 묶음 (cross-chapter 채택 선택) | bundle-builder 위임 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | insights (voice-craft 통과) + source_chapter + all_chapters_seeds dict + min_relevance |
| Output | List[CrossChapterCandidate] — source·target·relevance·matched_spine·matched_loops |
| 후속 sub | `bookwriting-insight-synthesis-bundle-builder` (cross-chapter 묶음 입력) |
| Dependencies | voice-craft 통과 + 전체 챕터 시드 컨텍스트 |
| 결정론 모듈 | M6 RelevanceScorer (BM25) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M6 BM25 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 환원 |
| #4 저자 작가성 | cross-chapter 저자 묶음 *강제* — 자동 결정 영구 금지 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- cross-reference 정확도 75%+ (부모 §10)
- 저자 spot-check 통과
- bookwriting-master HITL Mediator와 협업 (저자 묶음 2 형식)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-insight-synthesis-subs.md` §SUB 8
부모 마스터 SPEC: `specs/bookwriting-insight-synthesis-master.md` §7 Step 7 + §14 C3 Cross-Chapter Insight
결정론 모듈: `lib/relevance_scorer.py` (M6 BM25)
cross-reference: `meaning-evaluation` (matched_spines) + ③ `bookwriting-systemlink-system-loop-mapper` (L1-L7 매핑)
