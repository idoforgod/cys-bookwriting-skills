---
name: bookwriting-content-expand-time-coordinator
description: 부모 bookwriting-content-expand-master의 INTERNAL sub. 저자 2층 골격 요소 6+7 (시점 좌표 + 횡단 연결) 담당. AGI 5단계 (챗봇·추론가·대행자·혁신가·조직) skeleton.md §시점 동기화에서 결정론 read (Round 9 #E4.1 — 하드코딩 금지) + 통찰의 시점 좌표 식별 + 횡단 연결 (다른 챕터 시드) + 300-500자 본문 골격.
when_to_use: bookwriting-content-expand-master에서 scenario-brancher 통과 후 자동 호출. 저자 v14 OpenAI 5단계 정합.
disable-model-invocation: true
---

# bookwriting-content-expand-time-coordinator

## TLDR

부모 bookwriting-content-expand-master의 저자 2층 골격 *요소 6+7* (시점 좌표 + 횡단 연결) 담당. AGI 5단계 (챗봇·추론가·대행자·혁신가·조직)를 skeleton.md §시점 동기화에서 결정론 read (하드코딩 금지). 통찰의 시점 + 횡단 챕터 연결 + 300-500자 골격.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- scenario-brancher 통과 후 자동
- voice-aligner 직전 마지막 골격 단계

## Detailed Methodology

### 1. 결정론 chain — skeleton read + AGI 5단계 매칭

```python
import re
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class TimeCoordinatorResult:
    insight_id: str
    agi_stage: str | None        # "단계 1: 챗봇" 등 (skeleton read)
    stage_id: str | None         # "1"~"5"
    cross_chapter_links: list[str]
    body_text: str               # 300-500자 골격

def _load_agi_5_stages_from_skeleton(skeleton_path: Path) -> list[dict]:
    """skeleton.md §시점 동기화에서 AGI 5단계 결정론 read.

    Round 9 #E4.1 Critical — 하드코딩 영구 금지.
    skeleton 변경 시 자동 반영.
    """
    if not skeleton_path.exists():
        return []
    text = skeleton_path.read_text(encoding="utf-8")

    # §시점 동기화 섹션 추출 (skeleton.md 1589-1592줄 영역)
    section_match = re.search(r"##?\s*시점\s*동기화[^\n]*\n(.*?)(?=\n##|\Z)", text, re.DOTALL)
    if not section_match:
        return []
    section = section_match.group(1)

    # 단계 1·2·3·4·5 패턴 매칭
    stages = []
    for m in re.finditer(r"-?\s*단계\s*(\d)[\s:：]+([^\n]+)", section):
        stages.append({"id": m.group(1), "name": m.group(2).strip()})

    return stages

def coordinate_time(
    insight: dict,
    cross_chapter_results: list[dict],
    skeleton_path: Path,
) -> TimeCoordinatorResult:
    """AGI 5단계 시점 + 횡단 연결 결정론 조립."""
    # Step 1: 통찰의 *시점 좌표* 식별
    # Step 2: AGI 5단계 — skeleton.md §시점 동기화 결정론 read (하드코딩 금지)
    agi_stages = _load_agi_5_stages_from_skeleton(skeleton_path)
    insight_text = insight.get("text", "")

    matched_stage = None
    matched_id = None
    for s in agi_stages:
        if s["name"] in insight_text or f"단계 {s['id']}" in insight_text:
            matched_stage = f"단계 {s['id']}: {s['name']}"
            matched_id = s["id"]
            break

    # Step 3: 횡단 연결 — 통찰이 *다른 챕터 어떤 시드와 맞물리는가*
    cross_links: list[str] = []
    for cc in cross_chapter_results:
        if cc.get("source_insight") == insight.get("id") or cc.get("source_insight_id") == insight.get("id"):
            cross_links.append(f"{cc.get('target_chapter', '?')} (관련성 {cc.get('relevance', 0):.2f})")

    # Step 4: 본문 골격 — 시점 + 횡단 연결 (300-500자)
    body = _assemble_time_skeleton(matched_stage, cross_links, agi_stages)

    return TimeCoordinatorResult(
        insight_id=insight.get("id", ""),
        agi_stage=matched_stage,
        stage_id=matched_id,
        cross_chapter_links=cross_links,
        body_text=body,
    )

def _assemble_time_skeleton(stage: str | None, cross: list[str], all_stages: list[dict]) -> str:
    lines = ["[2층 요소 6+7 — 시점 좌표 + 횡단 연결]"]
    if stage:
        lines.append(f"- AGI 시점: {stage}")
    else:
        lines.append(f"- AGI 시점: 저자 식별 필요 (가용 단계: {len(all_stages)}개)")
    if cross:
        lines.append(f"- 횡단 연결: {' / '.join(cross)}")
    lines.append("[저자 본문 300-500자 채워넣기 — 시점 + 횡단]")
    return "\n".join(lines)
```

### 2. 명세 §출처 (SPEC: bookwriting-content-expand-subs.md SUB 7)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 통찰의 *시점 좌표* 식별 | `matched_stage`·`matched_id` |
| Step 2: AGI 5단계 skeleton 결정론 read (Round 9 #E4.1 하드코딩 금지) | `_load_agi_5_stages_from_skeleton()` |
| Step 3: 횡단 연결 — 다른 챕터 시드 | `cross_chapter_results` (cross-chapter-check 산출) |
| Step 4: 본문 작성 — 시점 + 횡단 연결 (300-500자) | `_assemble_time_skeleton()` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | insight + cross_chapter_results (⑥ insight-synthesis-cross-chapter-check 산출) + skeleton path |
| Output | TimeCoordinatorResult — agi_stage·stage_id·cross_chapter_links·body_text |
| 후속 sub | `voice-aligner` (마지막 voice 보정) |
| Dependencies | scenario-brancher 통과 + ⑥ cross-chapter-check 산출 |
| 결정론 모듈 | skeleton 결정론 read + 자체 정규식 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | skeleton read + 정규식 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step + Round 9 #E4.1 하드코딩 금지 명시 1:1 |
| #4 저자 작가성 | 본문 300-500자는 저자 직접 |
| #7 결정론 환원 | skeleton 결정론 read — 변경 시 자동 반영 |

### 5. Verification (명세 §6)

- AGI 5단계 명시 (`matched_stage` — skeleton 결정론 read)
- 횡단 연결 1+ 명시 (`cross_chapter_links` ≥ 1)
- 저자 v1 시점 동기화 정합 (skeleton.md §시점 동기화 원문)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-content-expand-subs.md` §SUB 7
부모 마스터 SPEC: `specs/bookwriting-content-expand-master.md` (2층 요소 6+7)
저자 v14: skeleton.md 1589-1592줄 OpenAI 공식 5단계 채택
Round 9 #E4.1 Critical: AGI 5단계 하드코딩 영구 금지 — skeleton read 강제
영속 자산 보호: PHASE3B_HANDOFF §8 (skeleton read-only)
⑥ cross-chapter-check 정합: `bookwriting-insight-synthesis-cross-chapter-check`
