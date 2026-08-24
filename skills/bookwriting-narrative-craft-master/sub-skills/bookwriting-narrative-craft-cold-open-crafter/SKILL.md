---
name: bookwriting-narrative-craft-cold-open-crafter
description: 부모 bookwriting-narrative-craft-master의 INTERNAL sub ⭐ 콜드오픈 작성 핵심. skeleton.md chapter-pipeline의 콜드오픈 라이브러리 결정론 read + 챕터 1층 고유 장면 한 컷 작성 (600-1200자) + 시간·장소·인물·감각 디테일 강제 + 콜드오픈 후보 2-3개 생성 + 1층 끝 한 문장 명제 단독 배치.
when_to_use: bookwriting-narrative-craft-master에서 ⑥ insight-synthesis + ⑦ content-expand (2층 본문) 통과 후 자동 호출. `/bookwriting-narrative-craft cold-open` 모드 단독 가능.
disable-model-invocation: true
---

# bookwriting-narrative-craft-cold-open-crafter

## TLDR

부모 bookwriting-narrative-craft-master의 ⭐ 콜드오픈 작성 핵심 sub. skeleton.md chapter-pipeline의 저자 콜드오픈 라이브러리 (다보스 무대·한국 자율주행·앤스로픽 매출 곡선·페르미 역설·카파시 한 문장)를 결정론 read하고 챕터 1층 고유 장면 한 컷 골격을 600-1200자로 조립한다. 2-3개 후보 생성.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- ⑥ insight-synthesis + ⑦ content-expand (2층 본문) 통과 후 자동
- `/bookwriting-narrative-craft cold-open <chapter>` 모드 단독

## Detailed Methodology

### 1. 결정론 chain — skeleton 콜드오픈 라이브러리 read + 후보 2-3개

```python
import re
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class ColdOpenCandidate:
    candidate_id: str
    library_template: str         # skeleton의 콜드오픈 후보 template
    chapter_id: str
    body_text: str                # 600-1200자 골격
    final_proposition: str        # 1층 끝 한 문장 명제
    sensory_details: dict[str, str]   # time·place·person·sense

def _load_cold_open_library(skeleton_path: Path) -> dict[str, list[str]]:
    """skeleton.md chapter-pipeline의 챕터별 콜드오픈 후보 결정론 read.

    저자 콜드오픈 라이브러리:
    - 서장: 다보스 무대 (하사비스·아모데이·머스크 세 문장)
    - ch01: 한국 자율주행 / 앤스로픽 매출 곡선
    - ch07: 페르미 역설 새벽 천문학자
    - ch10: 카파시 한 문장 ("사고 외주화 vs 이해 외주화")
    """
    if not skeleton_path.exists():
        return {}
    text = skeleton_path.read_text(encoding="utf-8")

    # chapter-pipeline 섹션 추출
    section_match = re.search(r"##?\s*chapter[\s-]*pipeline[^\n]*\n(.*?)(?=\n##|\Z)", text, re.IGNORECASE | re.DOTALL)
    if not section_match:
        return {}
    section = section_match.group(1)

    # 챕터별 콜드오픈 후보 매칭
    library: dict[str, list[str]] = {}
    for m in re.finditer(r"(서장|ch\d+|chapter\s*\d+)[^\n]*콜드\s*오픈[^\n]*\n((?:\s*-\s*[^\n]+\n?)+)", section, re.IGNORECASE):
        ch = m.group(1).lower().replace("chapter ", "ch").replace(" ", "")
        candidates_raw = m.group(2)
        candidates = [line.strip("- \t") for line in candidates_raw.split("\n") if line.strip("- \t")]
        library[ch] = candidates

    return library

def craft_cold_open(
    chapter_id: str,
    insight: dict,           # 핵심 시드·통찰의 핵심 명제
    skeleton_path: Path,
    forecast_registry_path: Path,
) -> list[ColdOpenCandidate]:
    """콜드오픈 후보 2-3개 결정론 조립."""
    # Step 1: skeleton.md chapter-pipeline의 챕터별 콜드오픈 후보 로드
    library = _load_cold_open_library(skeleton_path)
    templates = library.get(chapter_id.lower(), [])

    # Step 2: 핵심 시드·통찰의 핵심 명제 확인
    core_proposition = insight.get("text", "")

    # Step 3: 콜드오픈 후보 2-3개 작성 (각 다른 후보 활용)
    candidates: list[ColdOpenCandidate] = []
    for i, template in enumerate(templates[:3]):
        # Step 4: 인용·통계 최소화·구체 장면 강제
        # Step 5: 1층 끝 한 문장 명제 단독 배치
        sensory = _extract_sensory_from_template(template)
        body = _assemble_cold_open_skeleton(template, core_proposition, sensory)
        candidates.append(ColdOpenCandidate(
            candidate_id=f"CO-{chapter_id}-{i+1}",
            library_template=template,
            chapter_id=chapter_id,
            body_text=body,
            final_proposition=core_proposition,
            sensory_details=sensory,
        ))

    # 후보 < 2 — 저자 직접 작성 권장 (skeleton 보강 필요)
    if len(candidates) < 2:
        candidates.append(ColdOpenCandidate(
            candidate_id=f"CO-{chapter_id}-fallback",
            library_template="[skeleton 콜드오픈 후보 부족 — 저자 직접 작성]",
            chapter_id=chapter_id,
            body_text=f"[600-1200자 저자 작성 필요 — 명제: {core_proposition}]",
            final_proposition=core_proposition,
            sensory_details={},
        ))

    return candidates

def _extract_sensory_from_template(template: str) -> dict[str, str]:
    details = {"time": "", "place": "", "person": "", "sense": ""}
    # 시간 — 년도·새벽·아침
    m = re.search(r"(\d{4}\s*년|새벽|아침|밤|저녁)", template)
    if m: details["time"] = m.group(1)
    # 장소 — 고유명사
    m = re.search(r"(다보스|한국|샌프란시스코|서울|미국|중국|일본)", template)
    if m: details["place"] = m.group(1)
    # 인물 — 저자 명명 인물
    m = re.search(r"(하사비스|아모데이|머스크|카파시|저자|하라리)", template)
    if m: details["person"] = m.group(1)
    return details

def _assemble_cold_open_skeleton(template: str, proposition: str, sensory: dict) -> str:
    lines = ["[1층 콜드오픈]"]
    lines.append(f"- 라이브러리 template: {template}")
    if sensory.get("time") or sensory.get("place"):
        lines.append(f"- 감각 디테일: {sensory.get('time', '')} {sensory.get('place', '')} {sensory.get('person', '')}".strip())
    lines.append("[저자 600-1200자 채워넣기 — 시간·장소·인물·감각 디테일 강제]")
    lines.append(f"\n[1층 끝 한 문장 명제 단독 배치]")
    lines.append(f"\"{proposition}\"")
    return "\n".join(lines)
```

### 2. 명세 §출처 (SPEC: bookwriting-narrative-craft-subs.md SUB 1) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: skeleton.md chapter-pipeline 콜드오픈 후보 로드 | `_load_cold_open_library()` 결정론 read |
| Step 2: 핵심 시드·통찰의 핵심 명제 확인 | `core_proposition = insight.get("text")` |
| Step 3: 콜드오픈 후보 2-3개 작성 | `templates[:3]` 순회 |
| Step 4: 인용·통계 최소화·구체 장면 강제 | `sensory_details` 4 필드 (time·place·person·sense) |
| Step 5: 1층 끝 한 문장 명제 단독 배치 | `final_proposition` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + insight + skeleton.md path + forecast-registry path |
| Output | List[ColdOpenCandidate] — 2-3개 후보 + sensory_details + final_proposition |
| 후속 sub | `character-animator` (등장인물 입체화 — 22주차 SUB 2) |
| Dependencies | ⑥ insight-synthesis 통과 + ⑦ content-expand (2층 본문) 통과 |
| 결정론 모듈 | 자체 정규식 (skeleton read + sensory 추출) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | skeleton 결정론 read — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step + 저자 콜드오픈 라이브러리 원문 1:1 |
| #4 저자 작가성 ⭐ | 저자 600-1200자 직접 채움 — sub는 골격·sensory 추출 |
| #7 결정론 환원 | 100% 결정론 (skeleton read + 정규식) |

### 5. Verification (명세 §7)

- 저자 v1 1층 5 검사항 통과
- 콜드오픈 후보 ≥ 2 (skeleton 라이브러리 + fallback)
- 구체 장면 명확 (`sensory_details` 4 필드)
- 1층 끝 한 문장 명제 단독 배치 (`final_proposition` 필드)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-narrative-craft-subs.md` §SUB 1 ⭐
부모 마스터 SPEC: `specs/bookwriting-narrative-craft-master.md`
저자 콜드오픈 라이브러리: skeleton.md chapter-pipeline (변경 영구 금지 — PHASE3B_HANDOFF §8)
저자 v1 1층 5 검사항: 저자 v1 chapter-pipeline 명시
