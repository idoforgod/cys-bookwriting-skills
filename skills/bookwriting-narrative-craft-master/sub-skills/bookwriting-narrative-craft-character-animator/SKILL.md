---
name: bookwriting-narrative-craft-character-animator
description: 부모 bookwriting-narrative-craft-master의 INTERNAL sub. 등장인물 (Amodei·Hassabis·저자·하라리·바루파키스 등) 입체화 — 직책·소속·맥락·신체 디테일·말투 결정론 추출 (evidence 기반) + 단순 "그가 말했다" 인용 → 입체적 narrate 변환 + forecast-registry author + skeleton 명시 정합. 인물 입체화 ≥1명/콜드오픈.
when_to_use: bookwriting-narrative-craft-master에서 cold-open-crafter 통과 후 자동 호출. ④ evidence-collect의 author·source 정보 활용.
disable-model-invocation: true
---

# bookwriting-narrative-craft-character-animator

## TLDR

부모 bookwriting-narrative-craft-master의 등장인물 입체화 sub. forecast-registry author + skeleton 명시 인물 (Amodei·Hassabis·저자·하라리·바루파키스)을 evidence 기반으로 직책·소속·맥락·신체 디테일·말투를 결정론 추출하고 단순 인용을 입체적 narrate로 변환한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- cold-open-crafter 통과 후 자동
- 콜드오픈·시나리오 narrate 강화

## Detailed Methodology

### 1. 결정론 chain — 인물 evidence 기반 입체화

```python
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class CharacterProfile:
    name: str
    role: str                    # 직책
    affiliation: str             # 소속
    context: str                 # 맥락
    physical_details: list[str]  # 신체 디테일 (evidence 기반만)
    speaking_style: str          # 말투·발언 양식
    evidence_sources: list[str]  # 인물 정보 evidence

@dataclass
class CharacterAnimationResult:
    chapter_id: str
    characters: list[CharacterProfile]
    animated_passages: list[str]   # 입체적 narrate로 변환된 단락

# 저자 명명 인물 (skeleton + forecast-registry author)
KNOWN_CHARACTERS = {
    "Amodei": {"role": "Anthropic 창업자·CEO", "affiliation": "Anthropic"},
    "Hassabis": {"role": "DeepMind CEO", "affiliation": "Google DeepMind"},
    "Musk": {"role": "xAI 창업자", "affiliation": "xAI / Tesla"},
    "Karpathy": {"role": "AI 연구자", "affiliation": "독립 / 前 OpenAI·Tesla"},
    "Harari": {"role": "역사학자·미래학자", "affiliation": "Hebrew University"},
    "Varoufakis": {"role": "정치경제학자", "affiliation": "전 그리스 재무장관"},
    "저자": {"role": "{{저자 직함}}", "affiliation": "{{소속 기관명}}"},
}

def animate_characters(
    chapter_id: str,
    cold_open_candidates: list,
    evidence_track: list[dict],
    forecast_registry_path: Path,
) -> CharacterAnimationResult:
    """등장인물 결정론 입체화."""
    # Step 1: 챕터 등장인물 식별 (forecast-registry author + skeleton 명시)
    characters_in_chapter: list[str] = []

    # 콜드오픈 candidates에서 인물 추출
    for co in cold_open_candidates:
        person = co.sensory_details.get("person") if hasattr(co, "sensory_details") else None
        if person and person not in characters_in_chapter:
            characters_in_chapter.append(person)

    # forecast-registry author 추출
    with forecast_registry_path.open(encoding="utf-8") as f:
        forecast = yaml.safe_load(f) or {}
    for p in forecast.get("predictions", []):
        for ev in p.get("evidence", []):
            author = ev.get("author")
            if author and author in KNOWN_CHARACTERS and author not in characters_in_chapter:
                characters_in_chapter.append(author)

    # Step 2: 각 인물의 입체 정보 결정론 추출
    profiles: list[CharacterProfile] = []
    for name in characters_in_chapter:
        if name not in KNOWN_CHARACTERS:
            continue
        base = KNOWN_CHARACTERS[name]

        # evidence에서 맥락·말투·신체 디테일 추출
        ev_sources = [ev for ev in evidence_track if ev.get("author") == name]
        physical = _extract_physical_details(ev_sources)
        speaking = _extract_speaking_style(ev_sources)
        context = _extract_context(ev_sources)

        profiles.append(CharacterProfile(
            name=name,
            role=base["role"],
            affiliation=base["affiliation"],
            context=context,
            physical_details=physical,
            speaking_style=speaking,
            evidence_sources=[ev.get("source_file", "") for ev in ev_sources],
        ))

    # Step 3-4: 본문에 단순 "그가 말했다" 인용 → 입체적 narrate 변환
    animated_passages = _animate_passages(profiles, cold_open_candidates)

    return CharacterAnimationResult(
        chapter_id=chapter_id,
        characters=profiles,
        animated_passages=animated_passages,
    )

def _extract_physical_details(evidence: list[dict]) -> list[str]:
    """evidence에서 신체 디테일 추출 — 가능한 것만 (할루시네이션 금지)."""
    details = []
    for ev in evidence:
        text = ev.get("excerpt", "") or ev.get("text", "")
        # 안경·수염·머리 등 명시된 신체 디테일만
        for kw in ["안경", "수염", "머리", "키", "옷"]:
            if kw in text:
                m = re.search(rf"[\w\s]{{0,15}}{kw}[\w\s]{{0,15}}", text)
                if m:
                    details.append(m.group(0).strip())
                    break
    return details[:3]   # 최대 3개

def _extract_speaking_style(evidence: list[dict]) -> str:
    """말투·발언 양식 — 직접 인용된 표현 추출."""
    quotes = []
    for ev in evidence:
        text = ev.get("excerpt", "") or ev.get("text", "")
        for m in re.finditer(r'"([^"]{10,80})"', text):
            quotes.append(m.group(1))
    if quotes:
        return f"대표 발언: \"{quotes[0]}\""
    return ""

def _extract_context(evidence: list[dict]) -> str:
    """발언 맥락 추출."""
    for ev in evidence:
        date = ev.get("date") or ev.get("timestamp")
        if date:
            return f"{date} 시점"
    return ""

def _animate_passages(profiles: list[CharacterProfile], cold_opens: list) -> list[str]:
    """단순 인용 → 입체 narrate."""
    passages = []
    for p in profiles:
        if p.speaking_style:
            passages.append(
                f"[{p.name} ({p.role}, {p.affiliation})] {p.context} — {p.speaking_style}"
            )
    return passages
```

### 2. 명세 §출처 (SPEC: bookwriting-narrative-craft-subs.md SUB 2)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 챕터 등장인물 식별 (forecast-registry author + skeleton 명시) | `characters_in_chapter` + `KNOWN_CHARACTERS` lookup |
| Step 2: 각 인물의 입체 정보 (직책·소속·맥락·신체·말투) | `CharacterProfile` 5 필드 |
| Step 3: "그가 말했다" 단순 인용 → 입체적 narrate | `_animate_passages()` |
| Step 4: 단순 이름 → 풍부한 등장 | role·affiliation·context 결합 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + cold_open_candidates + evidence_track + forecast-registry path |
| Output | CharacterAnimationResult — characters·animated_passages |
| 후속 sub | 다른 narrative-craft sub (scenario-narrator 등 — 23주차) |
| Dependencies | cold-open-crafter 통과 + ④ evidence-collect의 author·source |
| 결정론 모듈 | 자체 정규식 (신체 디테일·인용) + dict lookup |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 ⭐ | evidence 명시된 것만 추출 (할루시네이션 신체 디테일 금지) |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 환원 |
| #3 출처 명시 | `evidence_sources` 필수 필드 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- 인물 입체화 ≥ 1명/콜드오픈
- evidence 기반 정확 (`evidence_sources` 필수, 미인용 신체 디테일 금지)
- KNOWN_CHARACTERS 매칭 정확 (skeleton + forecast-registry author 정합)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-narrative-craft-subs.md` §SUB 2
부모 마스터 SPEC: `specs/bookwriting-narrative-craft-master.md`
저자 명명 인물: skeleton.md (변경 영구 금지 — PHASE3B_HANDOFF §8)
④ evidence-collect 정합: `bookwriting-evidence-collect-asset-searcher` author 산출
