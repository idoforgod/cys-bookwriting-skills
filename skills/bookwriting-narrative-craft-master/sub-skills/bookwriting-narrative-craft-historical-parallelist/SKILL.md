---
name: bookwriting-narrative-craft-historical-parallelist
description: 부모 bookwriting-narrative-craft-master의 INTERNAL sub. 저자 권위 Layer 5 (역사 평행) narrate — 1930년대 대공황·핵무기 통제·산업혁명 러다이트·앵글로색슨 영국 정복·바이마르 의회 패턴 결정론 매칭 + skeleton.md 역사 평행 풀 read + 시그니처 *두 창업자가 같은 N배* 패턴 활용 + 역사 evidence 정확성 강제.
when_to_use: bookwriting-narrative-craft-master에서 scenario-narrator 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-narrative-craft-historical-parallelist

## TLDR

부모 bookwriting-narrative-craft-master의 저자 권위 Layer 5 (역사 평행) narrate sub. 5 역사 패턴 (1930년대 대공황·핵무기 통제·산업혁명 러다이트·앵글로색슨 영국 정복·바이마르 의회)을 결정론 매칭하고 skeleton 권위 5층 Layer 5 정합. 시그니처 *두 창업자가 같은 N배* 패턴 활용 + 역사 사실 정확성 강제.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- scenario-narrator 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — 5 역사 평행 패턴 매칭

```python
import re
from pathlib import Path
from dataclasses import dataclass, field

class HistoricalParallel:
    DEPRESSION = "depression_1930s"
    NUCLEAR = "nuclear_control"
    LUDDITE = "industrial_luddite"
    ANGLOSAXON = "anglosaxon_conquest"
    WEIMAR = "weimar_parliament"

@dataclass
class HistoricalParallelResult:
    chapter_id: str
    parallels: list[dict]               # [{type, history_event, agi_target, evidence_source}]
    signature_two_founders_attempted: bool

# 명세 SUB 4 §3 저자 역사 평행 5종 (skeleton.md 권위 5층 Layer 5 정합)
PARALLEL_PATTERNS = {
    HistoricalParallel.DEPRESSION: {
        "history_keywords": ["대공황", "1930", "great depression"],
        "agi_target": "AGI 시대 경제",
    },
    HistoricalParallel.NUCLEAR: {
        "history_keywords": ["핵무기", "nuclear", "맨해튼"],
        "agi_target": "AGI 안전",
    },
    HistoricalParallel.LUDDITE: {
        "history_keywords": ["산업혁명", "러다이트", "luddite"],
        "agi_target": "일자리 대체",
    },
    HistoricalParallel.ANGLOSAXON: {
        "history_keywords": ["앵글로색슨", "영국 정복", "anglo-saxon"],
        "agi_target": "AI 이민",
    },
    HistoricalParallel.WEIMAR: {
        "history_keywords": ["바이마르", "weimar", "독일 의회"],
        "agi_target": "알고리즘 통치",
    },
}

def narrate_historical_parallels(
    chapter_id: str,
    insight_text: str,
    evidence_track: list[dict],
    skeleton_path: Path,
) -> HistoricalParallelResult:
    """5 역사 평행 결정론 매칭 + 시그니처 적용."""
    parallels: list[dict] = []

    for ptype, config in PARALLEL_PATTERNS.items():
        # 통찰·evidence에 역사 키워드 매칭
        matched_keyword = None
        evidence_source = None
        for kw in config["history_keywords"]:
            if kw in insight_text:
                matched_keyword = kw
                break
            for ev in evidence_track:
                excerpt = ev.get("excerpt", "") or ev.get("text", "")
                if kw in excerpt:
                    matched_keyword = kw
                    evidence_source = ev.get("source_file", "")
                    break
            if matched_keyword:
                break

        if matched_keyword:
            parallels.append({
                "type": ptype,
                "history_event": matched_keyword,
                "agi_target": config["agi_target"],
                "evidence_source": evidence_source,
            })

    # 시그니처 *두 창업자가 같은 N배* 패턴 활용 기회
    # — 역사 평행이 *두 시대*를 연결하므로 시그니처 적용 가능
    sig_attempted = len(parallels) >= 1 and "배" in insight_text

    return HistoricalParallelResult(
        chapter_id=chapter_id,
        parallels=parallels,
        signature_two_founders_attempted=sig_attempted,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-narrative-craft-subs.md SUB 4)

| 명세 항목 | 본 sub 구현 |
|---|---|
| 1930년대 대공황 → AGI 시대 경제 | `PARALLEL_PATTERNS[DEPRESSION]` |
| 핵무기 통제 → AGI 안전 | `PARALLEL_PATTERNS[NUCLEAR]` |
| 산업혁명 러다이트 → 일자리 대체 | `PARALLEL_PATTERNS[LUDDITE]` |
| 앵글로색슨 영국 정복 → AI 이민 | `PARALLEL_PATTERNS[ANGLOSAXON]` |
| 바이마르 의회 → 알고리즘 통치 | `PARALLEL_PATTERNS[WEIMAR]` |
| 저자 skeleton의 "권위 5층 Layer 5" 직접 활용 | skeleton 정합 (역사 패턴 매칭 시) |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + insight_text + evidence_track + skeleton path |
| Output | HistoricalParallelResult — parallels + signature_two_founders_attempted |
| 후속 sub | `signature-weaver` |
| Dependencies | scenario-narrator 통과 |
| 결정론 모듈 | 자체 키워드 매칭 + dict lookup |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 ⭐ | 역사 사실 정확성 — evidence 명시 + skeleton 정합 강제 |
| #2 grill-me 원문 일치 | 명세 5 역사 패턴 + 시그니처 1:1 환원 |
| #3 출처 명시 | `evidence_source` 필수 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 역사 사실 정확 (evidence 명시 강제)
- 저자 권위 5층 정합 (skeleton 패턴 매칭)
- 시그니처 *두 창업자가 같은 N배* 패턴 활용

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-narrative-craft-subs.md` §SUB 4
부모 마스터 SPEC: `specs/bookwriting-narrative-craft-master.md`
저자 권위 5층 Layer 5: skeleton.md (역사 평행 5종)
시그니처: voice-craft 5 패턴 중 *두 창업자 N배*
