---
name: bookwriting-content-expand-weak-signal-synthesizer
description: 부모 bookwriting-content-expand-master의 INTERNAL sub. 저자 2층 골격 요소 2 (약신호) 담당. 채택된 통찰의 약신호 차원을 가시적 evidence (영상·뉴스·저자 직접 관찰)로 결정론 선별 + 200-600자 본문 작성 + 시간·장소·인물 감각 디테일 강제 + voice·citation gate 자동 발동.
when_to_use: bookwriting-content-expand-master에서 ⑥ insight-synthesis 통과 INSIGHTED 시드 대상 자동 호출. 저자 본문 작성 보조 (저자 진북 #4 — 본문 자체는 저자 작성, sub-skill은 골격·검증).
disable-model-invocation: true
---

# bookwriting-content-expand-weak-signal-synthesizer

## TLDR

부모 bookwriting-content-expand-master의 저자 2층 골격 *요소 2* 담당. 채택된 통찰의 약신호 차원을 가시적 evidence로 선별하여 200-600자 본문 골격을 결정론 조립한다. 저자 콜드오픈 라이브러리 (skeleton.md chapter-pipeline) 정합. voice·citation gate 자동 발동.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- INSIGHTED 시드 대상 cycle 진입 시 자동 첫 단계
- 2층 골격 요소 2 작성 시점

## Detailed Methodology

### 1. 결정론 chain — 가시 evidence 선별 + 본문 골격

```python
from pathlib import Path
from dataclasses import dataclass, field
from authority_grader import AuthorityGrader, Grade   # M3

@dataclass
class WeakSignalContent:
    insight_id: str
    selected_evidence: list[str]    # 가시 evidence source_file (1-3개)
    body_text: str                  # 200-600자
    voice_score: float
    citation_grades: list[str]      # 인용 evidence grade
    sensory_details: dict[str, str]  # time·place·person

VISIBLE_KEYWORDS = ["영상", "live", "직접 관찰", "video", "라이브", "현장", "news", "뉴스"]

def synthesize_weak_signal(
    insight: dict,
    evidence_track: list[dict],
    skeleton_path: Path,
    authority_db_path: Path,
) -> WeakSignalContent:
    """약신호 차원 본문 골격 결정론 조립."""
    grader = AuthorityGrader(authority_db_path)

    # Step 1: 통찰 + evidence-track 로드 (입력으로 받음)
    # Step 2: 가장 *가시적*인 evidence 선별 — Grade A·B 우선 + VISIBLE_KEYWORDS 매칭
    visible_evidence: list[dict] = []
    for ev in evidence_track:
        ev_grade = ev.get("grade", "C")
        ev_text_lower = (ev.get("excerpt") or "").lower()
        is_visible = any(kw in ev_text_lower for kw in VISIBLE_KEYWORDS)
        if ev_grade in ("A", "B") and is_visible:
            visible_evidence.append(ev)
    # Grade A·B 가시 evidence 우선, 1-3개 선별
    visible_evidence = visible_evidence[:3]

    # Step 3: 저자 콜드오픈 라이브러리 (skeleton.md chapter-pipeline) 정합
    skeleton_text = skeleton_path.read_text(encoding="utf-8") if skeleton_path.exists() else ""

    # Step 4: 약신호 본문 골격 작성 (시간·장소·감각 디테일 동반)
    # — 본 sub는 결정론 골격 조립만. 저자가 직접 200-600자 채움 (저자 진북 #4 작가성)
    sensory_details = _extract_sensory_details(visible_evidence)
    body_skeleton = _assemble_skeleton(insight, visible_evidence, sensory_details)

    # Step 5: voice·citation gate 자동 발동 (부모 마스터가 cross-cutting 호출)
    return WeakSignalContent(
        insight_id=insight.get("id", ""),
        selected_evidence=[ev["source_file"] for ev in visible_evidence],
        body_text=body_skeleton,
        voice_score=0.0,    # 부모가 M1 호출 후 채움
        citation_grades=[ev.get("grade", "C") for ev in visible_evidence],
        sensory_details=sensory_details,
    )

def _extract_sensory_details(evidence: list[dict]) -> dict[str, str]:
    """가시 evidence에서 시간·장소·인물 자동 추출."""
    import re
    details = {"time": "", "place": "", "person": ""}
    for ev in evidence:
        text = ev.get("excerpt", "") or ev.get("text", "")
        if not details["time"]:
            m = re.search(r"(\d{4})\s*년", text)
            if m: details["time"] = m.group(0)
        if not details["place"]:
            m = re.search(r"(한국|미국|중국|일본|다보스|샌프란시스코|서울)", text)
            if m: details["place"] = m.group(1)
        if not details["person"]:
            details["person"] = ev.get("author", "")
    return details

def _assemble_skeleton(insight, evidence, sensory) -> str:
    """본문 골격 — 저자가 채울 형식 마련."""
    lines = []
    if sensory["time"] or sensory["place"]:
        lines.append(f"[{sensory['time']} {sensory['place']} 약신호]")
    lines.append(f"- 통찰: {insight.get('text', '')}")
    for ev in evidence:
        lines.append(f"- evidence: {ev.get('source_file', '')} (Grade {ev.get('grade', '?')})")
    lines.append("[저자 본문 200-600자 채워넣기]")
    return "\n".join(lines)
```

### 2. 명세 §출처 (SPEC: bookwriting-content-expand-subs.md SUB 1)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 통찰 + evidence-track 로드 | 입력 |
| Step 2: 가장 *가시적*인 evidence 선별 | `VISIBLE_KEYWORDS` + Grade A·B 우선 |
| Step 3: 저자 콜드오픈 라이브러리 정합 | skeleton.md chapter-pipeline read |
| Step 4: 약신호 본문 작성 (시간·장소·감각 디테일) | `_extract_sensory_details()` + `_assemble_skeleton()` |
| Step 5: voice·citation gate 자동 발동 | 부모 마스터 cross-cutting 호출 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | insight (INSIGHTED) + evidence_track + skeleton.md + authority-db |
| Output | WeakSignalContent — selected_evidence·body_text·voice_score·citation_grades·sensory_details |
| 후속 sub | `bookwriting-content-expand-driving-force-synthesizer` |
| Dependencies | ⑥ insight-synthesis 통과 + ④ evidence-collect Grade A·B 풍부 |
| 결정론 모듈 | M3 AuthorityGrader (Grade A·B 필터) + 자체 정규식 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M3 + 정규식 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 |
| #3 출처 명시 | citation_grades 필수 |
| #4 저자 작가성 | 본 sub는 *골격만* 조립 — 200-600자는 저자 직접 채움 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- 약신호 본문 골격에 구체적 시간·장소·인물 명시 (`sensory_details` 3 필드)
- evidence 인용 1-3개 (Grade A·B 우선)
- voice_score 0.7+ (cross-cutting voice-gate)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-content-expand-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-content-expand-master.md` (2층 골격 요소 2 약신호)
저자 콜드오픈 라이브러리: skeleton.md chapter-pipeline (영구 변경 금지 — PHASE3B_HANDOFF §8)
결정론 모듈: `lib/authority_grader.py` (M3)
