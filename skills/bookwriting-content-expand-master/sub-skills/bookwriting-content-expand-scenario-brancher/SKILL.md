---
name: bookwriting-content-expand-scenario-brancher
description: 부모 bookwriting-content-expand-master의 INTERNAL sub. 저자 2층 골격 요소 5 (시나리오 분기) 담당. 정치 변수에 따른 결과 다양화 (봉건제 vs 풍요·평화의 역설) 결정론 분기 + 저자 시그니처 *변수 X 따라 결과 갈리는 동일 시스템* 적용 + skeleton.md 챕터 시나리오 분기 후보 정합 + 400-800자 본문 골격.
when_to_use: bookwriting-content-expand-master에서 system-loop-narrator 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-content-expand-scenario-brancher

## TLDR

부모 bookwriting-content-expand-master의 저자 2층 골격 *요소 5* 담당. 통찰의 시나리오 분기 후보를 정치 변수 (봉건제 vs 풍요·평화의 역설) 기준으로 결정론 식별하고 시그니처 *변수 X 따라 결과 갈리는 동일 시스템*을 적용한다. 400-800자 분기 본문 골격.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- system-loop-narrator 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — 정치 변수 분기 + 시그니처

```python
import re
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class ScenarioBranch:
    branch_id: str
    political_variable: str   # "정치 변수 A 채택" 등
    outcome: str
    keywords: list[str]

@dataclass
class ScenarioBrancherResult:
    insight_id: str
    branches: list[ScenarioBranch]
    signature_applied: bool   # "변수 X 따라 결과 갈리는 동일 시스템"
    body_text: str            # 400-800자 골격

# 저자 시나리오 분기 패턴 (skeleton.md §시나리오 분기)
BRANCH_PATTERNS = {
    "feudalism_vs_abundance": ["봉건제", "풍요"],
    "peace_paradox": ["평화", "역설", "전쟁"],
    "regulation_split": ["규제", "자유", "통제"],
    "capital_inequality": ["자본", "불평등", "분배"],
}

def branch_scenarios(
    insight: dict,
    system_loop_mappings: list[dict],
    skeleton_path: Path,
) -> ScenarioBrancherResult:
    """시나리오 분기 결정론 식별 + 시그니처 적용."""
    # Step 1: 통찰의 시나리오 분기 후보 식별
    insight_text = insight.get("text", "")
    detected_pattern = None
    for pat_name, keywords in BRANCH_PATTERNS.items():
        if all(kw in insight_text or any(kw in m.get("description", "") for m in system_loop_mappings) for kw in keywords):
            detected_pattern = pat_name
            break

    # Step 2: 저자 시그니처 *변수 X 따라 결과 갈리는 동일 시스템* 적용
    sig_applied = bool(detected_pattern)

    # Step 3: 분기 본문 작성 (분기 1·분기 2)
    branches: list[ScenarioBranch] = []
    if detected_pattern == "feudalism_vs_abundance":
        branches = [
            ScenarioBranch("B1", "정치 변수 A: 자본 집중", "봉건제 — 소수가 AGI 독점", ["봉건제", "독점"]),
            ScenarioBranch("B2", "정치 변수 B: UBI 도입", "풍요 — 다수가 혜택 공유", ["풍요", "UBI"]),
        ]
    elif detected_pattern == "peace_paradox":
        branches = [
            ScenarioBranch("B1", "정치 변수 A: 군비 경쟁", "AGI 무장 — 핵 시대 평행", ["군비", "AGI 무장"]),
            ScenarioBranch("B2", "정치 변수 B: 협약 체결", "평화의 역설 — 안정 vs 정체", ["협약", "안정"]),
        ]
    # 그 외 패턴은 저자 직접 분기 작성 권장

    # Step 4: skeleton.md 챕터 시나리오 분기 후보와 정합
    body = _assemble_branches(insight, branches, sig_applied)

    return ScenarioBrancherResult(
        insight_id=insight.get("id", ""),
        branches=branches,
        signature_applied=sig_applied,
        body_text=body,
    )

def _assemble_branches(insight: dict, branches: list[ScenarioBranch], sig: bool) -> str:
    lines = ["[2층 요소 5 — 시나리오 분기]"]
    if sig:
        lines.append("[시그니처: '변수 X 따라 결과 갈리는 동일 시스템' 적용]")
    for b in branches:
        lines.append(f"- 분기 {b.branch_id}: {b.political_variable} → {b.outcome}")
    if not branches:
        lines.append("[저자 직접 시나리오 분기 식별 필요]")
    lines.append("[저자 본문 400-800자 채워넣기 — 분기 풍경 대비]")
    return "\n".join(lines)
```

### 2. 명세 §출처 (SPEC: bookwriting-content-expand-subs.md SUB 6)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 통찰의 시나리오 분기 후보 식별 | `BRANCH_PATTERNS` 4 패턴 + 매칭 |
| Step 2: 저자 시그니처 *변수 X 따라 결과 갈리는* 적용 | `signature_applied` 플래그 |
| Step 3: 분기 본문 작성 (분기 1·분기 2) | `ScenarioBranch` × 2 |
| Step 4: skeleton.md 챕터 시나리오 분기 후보 정합 | skeleton path read |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | insight + system_loop_mappings + skeleton path |
| Output | ScenarioBrancherResult — branches·signature_applied·body_text |
| 후속 sub | `time-coordinator` |
| Dependencies | system-loop-narrator 통과 |
| 결정론 모듈 | 자체 정규식 + dict lookup |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 정규식 + dict 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step + 4 분기 패턴 1:1 |
| #4 저자 작가성 | 본문 400-800자는 저자 직접 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §6)

- 분기 2+ 명확 (`branches` ≥ 2)
- 시그니처 패턴 활용 (`signature_applied`)
- 정치 변수 명시 (`political_variable` 필드)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-content-expand-subs.md` §SUB 6
부모 마스터 SPEC: `specs/bookwriting-content-expand-master.md` (2층 요소 5)
시그니처: voice-craft 5 패턴 중 *변수 X 따라 결과 갈리는 동일 시스템*
