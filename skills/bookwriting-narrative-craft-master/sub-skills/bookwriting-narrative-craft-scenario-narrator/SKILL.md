---
name: bookwriting-narrative-craft-scenario-narrator
description: 부모 bookwriting-narrative-craft-master의 INTERNAL sub. 시나리오 분기 (봉건제 vs 풍요·평화의 역설 등)를 서사적 풍경 *대비되는 두 장면*으로 결정론 변환. 저자 시나리오 풍경 라이브러리 (키오스크 식당 vs 미슐랭·빛의 속도 AI 이민자·베네수엘라 팔란티어+클로드 작전 등) skeleton.md 결정론 read + 300-800자 본문 골격.
when_to_use: bookwriting-narrative-craft-master에서 character-animator 통과 후 자동 호출. ⑦ content-expand-scenario-brancher 산출을 입력.
disable-model-invocation: true
---

# bookwriting-narrative-craft-scenario-narrator

## TLDR

부모 bookwriting-narrative-craft-master의 시나리오 풍경 sub. ⑦ content-expand-scenario-brancher의 정치 변수 분기를 *대비되는 두 장면*으로 서사적 변환한다. skeleton.md의 시나리오 풍경 라이브러리 (키오스크 식당 vs 미슐랭 셰프·빛의 속도 AI 이민자·베네수엘라 팔란티어+클로드 작전)를 결정론 read하여 300-800자 본문 골격 조립.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- character-animator 통과 후 자동
- ⑦ content-expand-scenario-brancher 산출 입력 시

## Detailed Methodology

### 1. 결정론 chain — 대비 풍경 + skeleton read

```python
import re
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class ScenarioScene:
    branch_id: str
    scene_template: str          # skeleton 풍경 template
    visual_details: list[str]    # 시각 디테일
    contrast_partner: str        # 대비되는 분기 id

@dataclass
class ScenarioNarratorResult:
    chapter_id: str
    scenes: list[ScenarioScene]   # 분기당 1 scene (대비 쌍)
    body_text: str                # 300-800자 골격

def _load_scenario_library(skeleton_path: Path) -> list[str]:
    """skeleton.md 시나리오 풍경 라이브러리 결정론 read.

    저자 풍경 라이브러리 (명세 SUB 3 §3 — 변경 영구 금지):
    - 키오스크 식당 vs 미슐랭 셰프 풍경
    - 빛의 속도로 이동하는 AI 이민자
    - 베네수엘라 작전 (팔란티어+클로드 실시간)
    """
    if not skeleton_path.exists():
        return []
    text = skeleton_path.read_text(encoding="utf-8")
    section_match = re.search(r"##?\s*시나리오\s*풍경[^\n]*\n(.*?)(?=\n##|\Z)", text, re.DOTALL)
    if not section_match:
        # skeleton 미명시 시 기본 라이브러리
        return ["키오스크 식당 vs 미슐랭 셰프", "빛의 속도 AI 이민자", "베네수엘라 팔란티어+클로드"]
    section = section_match.group(1)
    return [line.strip("- \t") for line in section.split("\n") if line.strip("- \t")]

def narrate_scenarios(
    chapter_id: str,
    branches: list,              # ⑦ content-expand-scenario-brancher 산출
    skeleton_path: Path,
) -> ScenarioNarratorResult:
    """시나리오 분기 → 대비 풍경 결정론 narration."""
    library = _load_scenario_library(skeleton_path)
    scenes: list[ScenarioScene] = []

    # Step 1-3: 분기를 *대비되는 두 장면*으로
    for i, branch in enumerate(branches[:2]):  # 첫 2 분기만 대비 쌍
        # 저자 풍경 라이브러리에서 매칭 template 선별
        outcome = branch.outcome if hasattr(branch, "outcome") else branch.get("outcome", "")
        matched_template = ""
        for tmpl in library:
            kws = branch.keywords if hasattr(branch, "keywords") else branch.get("keywords", [])
            if any(kw in tmpl for kw in kws):
                matched_template = tmpl
                break

        scenes.append(ScenarioScene(
            branch_id=branch.branch_id if hasattr(branch, "branch_id") else f"B{i+1}",
            scene_template=matched_template or "[skeleton 풍경 라이브러리 매칭 실패 — 저자 작성]",
            visual_details=_extract_visual_details(outcome),
            contrast_partner=branches[1-i].branch_id if i < len(branches) and len(branches) >= 2 else "",
        ))

    # Step 4: 본문 골격 조립 (300-800자 — 저자 직접 채움)
    body = _assemble_scenario_skeleton(scenes)

    return ScenarioNarratorResult(
        chapter_id=chapter_id,
        scenes=scenes,
        body_text=body,
    )

def _extract_visual_details(outcome: str) -> list[str]:
    """결과 텍스트에서 시각 디테일 추출."""
    visuals = []
    for kw in ["빛", "공장", "식당", "사무실", "거리", "장면"]:
        if kw in outcome:
            visuals.append(kw)
    return visuals

def _assemble_scenario_skeleton(scenes: list[ScenarioScene]) -> str:
    lines = ["[2층 시나리오 풍경 narrative]"]
    for s in scenes:
        lines.append(f"- 분기 {s.branch_id} 풍경: {s.scene_template}")
        if s.contrast_partner:
            lines.append(f"  대비: {s.contrast_partner}")
    lines.append("[저자 300-800자 채워넣기 — 대비되는 두 장면 풍경 서사]")
    return "\n".join(lines)
```

### 2. 명세 §출처 (SPEC: bookwriting-narrative-craft-subs.md SUB 3)

| 명세 항목 | 본 sub 구현 |
|---|---|
| 키오스크 식당 vs 미슐랭 셰프 풍경 | `library` 라이브러리 0번 |
| 빛의 속도로 이동하는 AI 이민자 | library 1번 |
| 베네수엘라 작전 (팔란티어+클로드 실시간) | library 2번 |
| 시나리오 분기를 *대비되는 두 장면*으로 | `scenes` 2개 분기 쌍 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + branches (⑦ scenario-brancher 산출) + skeleton path |
| Output | ScenarioNarratorResult — scenes·body_text |
| 후속 sub | `historical-parallelist` |
| Dependencies | character-animator 통과 + ⑦ content-expand-scenario-brancher |
| 결정론 모듈 | skeleton 결정론 read + 정규식 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | skeleton + 정규식 결정론 |
| #2 grill-me 원문 일치 | 명세 4 항목 + 저자 풍경 라이브러리 원문 1:1 |
| #4 저자 작가성 | 300-800자는 저자 직접 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 시나리오 분기 명확 (`scenes` 2 쌍)
- 대비 풍경 효과적 (`contrast_partner` 명시)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-narrative-craft-subs.md` §SUB 3
부모 마스터 SPEC: `specs/bookwriting-narrative-craft-master.md`
저자 풍경 라이브러리: skeleton.md §시나리오 풍경 (변경 영구 금지 — PHASE3B_HANDOFF §8)
⑦ scenario-brancher 정합: `bookwriting-content-expand-scenario-brancher`
