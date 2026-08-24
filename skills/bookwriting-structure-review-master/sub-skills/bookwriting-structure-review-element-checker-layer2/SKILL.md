---
name: bookwriting-structure-review-element-checker-layer2
description: 부모 bookwriting-structure-review-master의 INTERNAL sub. 저자 v1 2층 표준 골격 7요소 (핵심명제 재진술·약신호·추동력·L1-L7 시스템 루프 호명·시나리오 분기·AGI 5단계 시점·횡단 연결) 결정론 정규식 검출 + 각 요소 ✅/⚠️ 표시 + 누락 시 저자 알림.
when_to_use: bookwriting-structure-review-master에서 layer-ratio-measurer 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-structure-review-element-checker-layer2

## TLDR

부모 bookwriting-structure-review-master의 2층 7요소 검출 sub. analysis.md에서 저자 v1 2층 표준 골격 7요소를 결정론 정규식으로 검출하고 누락 시 저자 알림한다. ⑦ content-expand 작성 본문이 7요소 모두 충족했는지 검증.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- layer-ratio-measurer 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — 7요소 정규식 검출

```python
import re
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class Layer2ElementCheck:
    chapter_id: str
    element_1_proposition_restated: bool   # 핵심명제 재진술
    element_2_weak_signal: bool             # 약신호 (구체 evidence)
    element_3_driving_force: bool           # 추동력 (시스템적 힘)
    element_4_system_loop_named: bool       # L1-L7 명시 호명
    element_5_scenario_branch: bool         # 시나리오 분기 (정치 변수)
    element_6_time_coordinate: bool         # AGI 5단계 시점
    element_7_cross_chapter: bool           # 횡단 연결
    missing_elements: list[str] = field(default_factory=list)

# 7요소 정규식 (⑦ content-expand sub들과 양식 정합)
ELEMENT_PATTERNS = {
    "1_proposition": re.compile(r"([\.。!?]\s*)[가-힣A-Za-z][^\.。!?\n]{10,80}[\.。]"),   # 본문 시작 명제
    "2_weak_signal": re.compile(r"(영상|live|뉴스|현장|직접 관찰|video|2024|2025|2026)"),
    "3_driving_force": re.compile(r"(한계비용|자본|패러다임|기술 곡선|피드백|임계)"),
    "4_system_loop": re.compile(r"L[1-7]\s*(지능대체나선|정치내파|봉건제|인구|도덕|우주|의미위기)"),
    "5_scenario_branch": re.compile(r"(분기|시나리오)\s*\d+|봉건제\s*vs\s*풍요|정치\s*변수"),
    "6_time_coordinate": re.compile(r"단계\s*[1-5]|챗봇|추론가|대행자|혁신가|조직"),
    "7_cross_chapter": re.compile(r"(ch\d+|챕터\s*\d+|→\s*다른 챕터|연결됨)"),
}

ELEMENT_NAMES = {
    "1_proposition": "핵심명제 재진술",
    "2_weak_signal": "약신호",
    "3_driving_force": "추동력",
    "4_system_loop": "L1-L7 시스템 루프 호명",
    "5_scenario_branch": "시나리오 분기",
    "6_time_coordinate": "AGI 5단계 시점 좌표",
    "7_cross_chapter": "횡단 연결",
}

def check_layer2_elements(chapter_id: str, analysis_path: Path) -> Layer2ElementCheck:
    """2층 7요소 결정론 검출."""
    if not analysis_path.exists():
        return Layer2ElementCheck(
            chapter_id=chapter_id,
            element_1_proposition_restated=False,
            element_2_weak_signal=False,
            element_3_driving_force=False,
            element_4_system_loop_named=False,
            element_5_scenario_branch=False,
            element_6_time_coordinate=False,
            element_7_cross_chapter=False,
            missing_elements=list(ELEMENT_NAMES.values()),
        )

    text = analysis_path.read_text(encoding="utf-8")

    # 7요소 매칭
    checks = {
        key: bool(pattern.search(text))
        for key, pattern in ELEMENT_PATTERNS.items()
    }

    # 누락 요소 식별
    missing = [ELEMENT_NAMES[key] for key, present in checks.items() if not present]

    return Layer2ElementCheck(
        chapter_id=chapter_id,
        element_1_proposition_restated=checks["1_proposition"],
        element_2_weak_signal=checks["2_weak_signal"],
        element_3_driving_force=checks["3_driving_force"],
        element_4_system_loop_named=checks["4_system_loop"],
        element_5_scenario_branch=checks["5_scenario_branch"],
        element_6_time_coordinate=checks["6_time_coordinate"],
        element_7_cross_chapter=checks["7_cross_chapter"],
        missing_elements=missing,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-structure-review-subs.md SUB 2)

| 명세 요소 | 본 sub 구현 |
|---|---|
| 1. 핵심명제 재진술 | `ELEMENT_PATTERNS["1_proposition"]` |
| 2. 약신호 (구체 evidence) | `ELEMENT_PATTERNS["2_weak_signal"]` |
| 3. 추동력 (시스템적 힘) | `ELEMENT_PATTERNS["3_driving_force"]` |
| 4. 시스템 루프 호명 (L1-L7 명시) | `ELEMENT_PATTERNS["4_system_loop"]` |
| 5. 시나리오 분기 (정치 변수) | `ELEMENT_PATTERNS["5_scenario_branch"]` |
| 6. 시점 좌표 (AGI 5단계) | `ELEMENT_PATTERNS["6_time_coordinate"]` |
| 7. 횡단 연결 (cross-chapter) | `ELEMENT_PATTERNS["7_cross_chapter"]` |
| 각 요소 발견 시 ✅, 누락 시 ⚠️ | bool 7 + `missing_elements` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + analysis_path (chapters/<ch>/analysis.md) |
| Output | Layer2ElementCheck — 7 bool + missing_elements list |
| 후속 sub | flow-validator |
| Dependencies | layer-ratio-measurer 통과 |
| 결정론 모듈 | 자체 정규식 7 패턴 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 정규식 결정론 |
| #2 grill-me 원문 일치 | 명세 7요소 1:1 환원 |
| #4 저자 작가성 | 누락 시 저자 알림 — 저자 결정권 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 7요소 검출 정확도 95%+
- 누락 시 저자 알림 (`missing_elements`)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-structure-review-subs.md` §SUB 2
부모 마스터 SPEC: `specs/bookwriting-structure-review-master.md`
저자 v1 2층 7요소: chapter-pipeline.md
⑦ content-expand 정합: 7 sub와 양식 일치 (proposition·weak-signal·driving-force·system-loop·scenario·time·cross-chapter)
