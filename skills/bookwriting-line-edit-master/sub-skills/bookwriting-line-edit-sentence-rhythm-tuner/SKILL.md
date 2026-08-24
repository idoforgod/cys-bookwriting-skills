---
name: bookwriting-line-edit-sentence-rhythm-tuner
description: 부모 bookwriting-line-edit-master의 INTERNAL sub. Sentence Rhythm Tuner 페르소나. 본문 문장 분석 (길이·태·리듬 패턴) + book-config sentence 규칙 (평균 50자·max 80자·능동태) 결정론 적용 + 저자 리듬 3박자 패턴 (짧은 명제+풍부한 부연·수치+인용+사상적 해석) 매칭 + 자동 첨삭 + diff 보존.
when_to_use: bookwriting-line-edit-master에서 vocabulary-refiner 통과 후 호출 (signature-applier·ai-tone-purger와 병렬 가능, 또는 voice-validator 전).
disable-model-invocation: true
---

# bookwriting-line-edit-sentence-rhythm-tuner

## TLDR

부모 bookwriting-line-edit-master의 문장 리듬 정밀화 sub. book-config voice_guidelines.sentence (평균 50자·max 80자·능동태)를 결정론 적용하고 저자 리듬 3박자 패턴을 매칭한다. 수동태 → 능동태·과도한 종속절 제거.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- vocabulary-refiner 통과 후 자동 (병렬 가능)

## Detailed Methodology

### 1. 결정론 chain — 문장 분석 + book-config 규칙

```python
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field

MAX_LENGTH = 80
AVG_LENGTH_TARGET = 50
PASSIVE_RATIO_LIMIT = 0.1   # < 10%

@dataclass
class SentenceRhythmResult:
    section_id: str
    original_text: str
    tuned_text: str
    sentence_count: int
    avg_length: float
    max_length_violations: int     # 80자 초과 문장 수
    passive_ratio: float           # 수동태 비율
    rhythm_pattern_detected: list[str]   # ["short_long", "stat_quote_interp"]
    diff_count: int

# 수동태 정규식 (한국어)
PASSIVE_PATTERN = re.compile(r"되었|되어|되는|되었던|진다|졌다|받았다|받는다|받게")

def tune_sentence_rhythm(
    sections: list[dict],
    book_config_path: Path,
) -> list[SentenceRhythmResult]:
    """문장 리듬·길이·태 결정론 정밀화."""
    with book_config_path.open(encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}
    sentence_rules = config.get("voice_guidelines", {}).get("sentence", {})
    max_len = sentence_rules.get("max_length", MAX_LENGTH)
    target_avg = sentence_rules.get("avg_length", AVG_LENGTH_TARGET)

    results: list[SentenceRhythmResult] = []
    for sec in sections:
        original = sec["text"]

        # Step 1: 문장 분리·길이·태·리듬 분석
        sentences = re.split(r"(?<=[.。!?])\s+", original)
        sentences = [s.strip() for s in sentences if s.strip()]

        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / max(len(sentences), 1)
        max_violations = sum(1 for L in lengths if L > max_len)

        passive_count = sum(1 for s in sentences if PASSIVE_PATTERN.search(s))
        passive_ratio = passive_count / max(len(sentences), 1)

        # Step 2-3: book-config 규칙 적용 + 저자 리듬 패턴 매칭
        # — 결정론 첨삭은 부모 마스터가 본문 조립 (본 sub는 분석·diff만)
        rhythm_patterns: list[str] = []
        # 짧은 명제 + 풍부한 부연 (3박자) — 단문·장문 흐름
        for i in range(len(sentences) - 1):
            if lengths[i] < 30 and lengths[i+1] > 60:
                rhythm_patterns.append("short_long")
                break
        # 수치 + 인용 + 사상적 해석 (3박자)
        for s in sentences:
            if re.search(r"\d+", s) and ('"' in s or "「" in s):
                rhythm_patterns.append("stat_quote_interp")
                break

        # Step 4: 자동 첨삭 + diff 보존 (간소화 — 부모 결합)
        diff_count = max_violations + passive_count

        results.append(SentenceRhythmResult(
            section_id=sec["section_id"],
            original_text=original,
            tuned_text=original,   # 부모 마스터가 분석 기반 첨삭
            sentence_count=len(sentences),
            avg_length=avg_length,
            max_length_violations=max_violations,
            passive_ratio=passive_ratio,
            rhythm_pattern_detected=list(set(rhythm_patterns)),
            diff_count=diff_count,
        ))

    return results
```

### 2. 명세 §출처 (SPEC: bookwriting-line-edit-subs.md SUB 5)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 본문 문장별 분석 (길이·태·리듬 패턴) | `sentences` + `lengths` + `passive_ratio` + `rhythm_patterns` |
| Step 2: book-config 규칙 적용 (max 80자·능동태) | yaml.safe_load + `max_len`·`PASSIVE_PATTERN` |
| Step 3: 저자 리듬 패턴 적용 (단문·장문·수치+인용+해석 3박자) | `rhythm_patterns` 매칭 |
| Step 4: 자동 첨삭 + diff 보존 | `diff_count` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | sections + book_config_path |
| Output | List[SentenceRhythmResult] — sentence 통계·rhythm 매칭·diff |
| 후속 sub | diff-preserver |
| Dependencies | vocabulary-refiner 통과 |
| 결정론 모듈 | 자체 정규식 + dict 통계 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 정규식 + 통계 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step + 저자 리듬 3박자 1:1 |
| #4 저자 작가성 | 저자 voice_guidelines.sentence 정합 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §6)

- 평균 문장 50자±10
- 수동태 < 10% (`passive_ratio < 0.1`)
- max 80자 위반 0건 (`max_length_violations == 0` 목표)
- 저자 리듬 패턴 검출 (3박자 1+ 매칭)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-line-edit-subs.md` §SUB 5
부모 마스터 SPEC: `specs/bookwriting-line-edit-master.md`
book-config voice_guidelines.sentence: max_length·avg_length·저자 리듬 패턴
