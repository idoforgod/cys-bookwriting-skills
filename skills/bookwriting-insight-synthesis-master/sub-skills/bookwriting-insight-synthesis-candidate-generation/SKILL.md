---
name: bookwriting-insight-synthesis-candidate-generation
description: 부모 bookwriting-insight-synthesis-master의 INTERNAL sub. 3 AI Agents 페르소나 (Meta-tool Identifier·System Loop Detector·Surprise Hunter) 동시 발동 + 통찰 후보 9-15개 결정론 생성 + M7 id_generator INS-NNN 임시 ID 발급 + 페르소나별 raw output 보존. 후속 평가 sub들의 *평가 대상 풀* 제공.
when_to_use: bookwriting-insight-synthesis-master Cycle C2 (다중 시드) 또는 C1 (단일 시드) 첫 단계에서 자동 호출. ④ evidence-collect 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-insight-synthesis-candidate-generation

## TLDR

부모 bookwriting-insight-synthesis-master의 ① 진입 sub. 3 페르소나 (Meta-tool Identifier 3-5개·System Loop Detector 2-4개·Surprise Hunter 3-5개)로 통찰 후보 9-15개를 생성하고 M7 id_generator로 INS-NNN 임시 ID를 결정론 발급한다. 페르소나별 raw output 보존.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- `/bookwriting-insight-synthesis cycle <target>` 진입 시 → 본 sub 자동 첫 단계
- `/bookwriting-insight-synthesis candidates <target>` 모드는 본 sub 단독

## Detailed Methodology

### 1. 결정론 chain — 3 페르소나 + M7 ID 발급

```python
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from id_generator import IdGenerator   # M7

class PersonaType(str, Enum):
    META_TOOL = "meta_tool_identifier"
    SYSTEM_LOOP = "system_loop_detector"
    SURPRISE = "surprise_hunter"

@dataclass
class InsightCandidate:
    insight_id: str             # INS-NNN (임시 — final ID는 채택 후 발급)
    persona: PersonaType
    text: str                   # 통찰 명제
    source_evidence_ids: list[str] = field(default_factory=list)
    source_seed_ids: list[str] = field(default_factory=list)
    raw_persona_output: str = ""  # 페르소나 raw output 보존

def generate_candidates(
    seeds: list[dict],
    evidence_track: dict,
    skeleton_path: Path,
    id_gen: IdGenerator,
) -> list[InsightCandidate]:
    """3 페르소나 동시 발동 + 후보 9-15개 결정론 생성."""
    candidates: list[InsightCandidate] = []

    # Step 1: 시드·evidence·skeleton 로드 (입력으로 받음)
    skeleton_text = skeleton_path.read_text(encoding="utf-8") if skeleton_path.exists() else ""

    # Step 2: Meta-tool Identifier 발동 (3-5 후보)
    meta_candidates = _meta_tool_persona(seeds, evidence_track, skeleton_text)
    for raw in meta_candidates[:5]:
        candidates.append(InsightCandidate(
            insight_id=id_gen.next_insight_id(),   # M7 INS-NNN
            persona=PersonaType.META_TOOL,
            text=raw["text"],
            source_evidence_ids=raw.get("evidence_ids", []),
            source_seed_ids=raw.get("seed_ids", []),
            raw_persona_output=raw["raw"],
        ))

    # Step 3: System Loop Detector 발동 (2-4 후보)
    loop_candidates = _system_loop_persona(seeds, evidence_track, skeleton_text)
    for raw in loop_candidates[:4]:
        candidates.append(InsightCandidate(
            insight_id=id_gen.next_insight_id(),
            persona=PersonaType.SYSTEM_LOOP,
            text=raw["text"],
            source_evidence_ids=raw.get("evidence_ids", []),
            source_seed_ids=raw.get("seed_ids", []),
            raw_persona_output=raw["raw"],
        ))

    # Step 4: Surprise Hunter 발동 (3-5 후보)
    surprise_candidates = _surprise_persona(seeds, evidence_track, skeleton_text)
    for raw in surprise_candidates[:5]:
        candidates.append(InsightCandidate(
            insight_id=id_gen.next_insight_id(),
            persona=PersonaType.SURPRISE,
            text=raw["text"],
            source_evidence_ids=raw.get("evidence_ids", []),
            source_seed_ids=raw.get("seed_ids", []),
            raw_persona_output=raw["raw"],
        ))

    # Step 5: 임시 ID 발급 + 풀 정돈 (id_gen이 결정론 보장)
    # Step 6: 다음 sub (triad-evaluation·meaning·impact·surprise)에 전달

    # G2 게이트: 최소 3 후보 (부모 §15)
    if len(candidates) < 3:
        raise ValueError("G2 위반: 통찰 후보 3개 미만 — ④ evidence-collect 재호출 권장")

    return candidates

def _meta_tool_persona(seeds, evidence, skeleton: str) -> list[dict]:
    """Meta-tool Identifier — 메타도구 명제·시스템 사고 관점에서 통찰 발견."""
    # 결정론 패턴: 시드·evidence 중 *메타도구·시스템 사고* 키워드 매칭
    # 페르소나의 의미 평가는 부모 §부록 E LLM 허용 영역 (단 근거 인용 강제)
    return []   # 실제 구현은 부모 마스터가 LLM·결정론 모듈 결합

def _system_loop_persona(seeds, evidence, skeleton: str) -> list[dict]:
    """System Loop Detector — 시스템 루프·피드백 관점."""
    return []

def _surprise_persona(seeds, evidence, skeleton: str) -> list[dict]:
    """Surprise Hunter — 통념 깨기·프레임 전복·수렴 놀라움."""
    return []
```

### 2. 명세 §출처 (SPEC: bookwriting-insight-synthesis-subs.md SUB 1)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 시드·evidence·skeleton 로드 | `seeds + evidence_track + skeleton_path` 입력 |
| Step 2: Meta-tool Identifier 발동 (3-5 후보) | `_meta_tool_persona()` |
| Step 3: System Loop Detector 발동 (2-4 후보) | `_system_loop_persona()` |
| Step 4: Surprise Hunter 발동 (3-5 후보) | `_surprise_persona()` |
| Step 5: 임시 ID 발급 + 풀 정돈 | M7 `id_gen.next_insight_id()` → INS-NNN |
| Step 6: 다음 sub에 전달 | candidates 리턴 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | seeds (EVIDENCED 이상) + evidence-track.yaml + skeleton.md path + IdGenerator |
| Output | List[InsightCandidate] — INS-NNN × 9-15 + 페르소나 raw output |
| 후속 sub | `triad-evaluation` + `meaning-evaluation` + `impact-evaluation` + `surprise-evaluation` |
| Dependencies | ④ evidence-collect 통과 (evidence-track 존재) |
| 결정론 모듈 | M7 IdGenerator (insight ID 확장 — INS-NNN) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 페르소나 의미 평가 LLM 허용 (부모 §부록 E) — 근거 인용 강제 |
| #2 grill-me 원문 일치 | 명세 6 Step + 페르소나 3종 1:1 환원 |
| #4 저자 작가성 | 저자 진북 *깜짝놀랄만한 단면 선택* (Surprise Hunter ⭐) |
| #7 결정론 환원 | M7 INS-NNN + ID 발급·풀 정돈 100% 결정론 |

### 5. Verification (명세 §7)

- 통찰 후보 9-15개 생성 (Meta-tool 3-5 / Loop 2-4 / Surprise 3-5)
- 모든 후보에 INS-NNN 임시 ID 발급 (M7 결정론)
- 페르소나별 raw output 보존
- 부모 §15 G2 게이트 — 최소 3 후보 강제

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-insight-synthesis-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-insight-synthesis-master.md` §7 + §13 페르소나 1·2·4 (Meta-tool·System Loop·Surprise Hunter) + §14 Cycle C1·C2 + 부록 E (M7 insight ID 확장)
결정론 모듈: `lib/id_generator.py` (M7)
LLM 허용: 부모 §부록 E — 페르소나 의미 평가만 (근거 인용 강제)
