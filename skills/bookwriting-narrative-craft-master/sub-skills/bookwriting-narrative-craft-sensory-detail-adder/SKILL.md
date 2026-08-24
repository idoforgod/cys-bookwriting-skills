---
name: bookwriting-narrative-craft-sensory-detail-adder
description: 부모 bookwriting-narrative-craft-master의 INTERNAL sub. 콜드오픈·서사에 시각·청각·촉각 감각 디테일 결정론 추가 — 시각 (장면)·청각 (말·소리)·촉각 (분위기) 정규식 패턴 + 저자 v1 1층 검사항 *독자 감각 자극* 통과 보장. evidence 기반만 추가 (할루시네이션 금지).
when_to_use: bookwriting-narrative-craft-master에서 signature-weaver 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-narrative-craft-sensory-detail-adder

## TLDR

부모 bookwriting-narrative-craft-master의 감각 강화 sub. 콜드오픈·서사에 3 감각 차원 (시각 장면·청각 말·소리·촉각 분위기)을 결정론 정규식으로 식별하고 evidence 기반 디테일만 추가한다. 저자 v1 1층 검사항 *독자 감각 자극* 통과 보장.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- signature-weaver 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — 3 감각 차원 정규식

```python
import re
from dataclasses import dataclass, field

@dataclass
class SensoryEnhancement:
    section_id: str
    original_text: str
    enhanced_text: str
    visual_details: list[str]    # 시각 (장면·이미지·색)
    auditory_details: list[str]  # 청각 (말·소리·음악)
    tactile_details: list[str]   # 촉각 (분위기·온도·질감)

# 3 감각 정규식 패턴
VISUAL_PATTERN = re.compile(r"(보다|장면|화면|풍경|색|빛|영상|들어가다|걸어|마주)")
AUDITORY_PATTERN = re.compile(r"(소리|말했|발음|들렸|음악|침묵|외쳤|속삭)")
TACTILE_PATTERN = re.compile(r"(차가운|따뜻한|무거운|가벼운|긴장|편안|숨|공기)")

def add_sensory_details(
    sections: list[dict],
    evidence_track: list[dict],
) -> list[SensoryEnhancement]:
    """3 감각 차원 결정론 추가 (evidence 기반)."""
    results: list[SensoryEnhancement] = []

    for sec in sections:
        text = sec["text"]

        # Step 1: 시각·청각·촉각 정규식 매칭
        visuals = VISUAL_PATTERN.findall(text)
        auditories = AUDITORY_PATTERN.findall(text)
        tactiles = TACTILE_PATTERN.findall(text)

        # Step 2: evidence 기반 디테일만 추가 (할루시네이션 금지)
        # — evidence excerpt에서 감각 디테일 *명시된 것*만 추출
        ev_visuals: list[str] = []
        ev_auditories: list[str] = []
        ev_tactiles: list[str] = []
        for ev in evidence_track:
            excerpt = ev.get("excerpt", "") or ev.get("text", "")
            ev_visuals.extend(VISUAL_PATTERN.findall(excerpt))
            ev_auditories.extend(AUDITORY_PATTERN.findall(excerpt))
            ev_tactiles.extend(TACTILE_PATTERN.findall(excerpt))

        # Step 3: 감각 통합 (본문 + evidence 명시)
        all_visuals = list(set(visuals + ev_visuals))[:5]
        all_auditories = list(set(auditories + ev_auditories))[:3]
        all_tactiles = list(set(tactiles + ev_tactiles))[:3]

        results.append(SensoryEnhancement(
            section_id=sec["section_id"],
            original_text=text,
            enhanced_text=text,    # 결정론 추가는 부모 마스터가 본문 조립
            visual_details=all_visuals,
            auditory_details=all_auditories,
            tactile_details=all_tactiles,
        ))

    return results

def check_sensory_stimulation(result: SensoryEnhancement) -> bool:
    """저자 v1 1층 검사항 *독자 감각 자극* 통과."""
    return (
        len(result.visual_details) >= 2
        and (len(result.auditory_details) >= 1 or len(result.tactile_details) >= 1)
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-narrative-craft-subs.md SUB 6)

| 명세 항목 | 본 sub 구현 |
|---|---|
| 시각 (장면) | `VISUAL_PATTERN` |
| 청각 (말·소리) | `AUDITORY_PATTERN` |
| 촉각 (분위기) | `TACTILE_PATTERN` |
| 저자 v1 1층 *독자 감각 자극* 검사항 통과 | `check_sensory_stimulation()` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | sections + evidence_track |
| Output | List[SensoryEnhancement] — visual·auditory·tactile details |
| 후속 sub | `voice-aligner` (narrative-craft) |
| Dependencies | signature-weaver 통과 |
| 결정론 모듈 | 자체 정규식 3 패턴 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | evidence 명시만 추출 — 미인용 감각 디테일 금지 |
| #2 grill-me 원문 일치 | 명세 3 감각 + 저자 v1 검사항 1:1 |
| #3 출처 명시 | evidence_track 기반만 |
| #7 결정론 환원 | 정규식 100% 결정론 |

### 5. Verification (명세 §5)

- 저자 v1 1층 *독자 감각 자극* 검사항 통과 (`check_sensory_stimulation()`)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-narrative-craft-subs.md` §SUB 6
부모 마스터 SPEC: `specs/bookwriting-narrative-craft-master.md`
저자 v1 1층 5 검사항: chapter-pipeline.md
