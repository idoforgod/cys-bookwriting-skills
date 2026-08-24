---
name: bookwriting-structure-review-flow-validator
description: 부모 bookwriting-structure-review-master의 INTERNAL sub. 1·2·3층 흐름 일관성 결정론 검증 — 1층 끝 핵심 명제 추출 → 2층이 *그 명제를 입증*하는지 → 3층 함의가 *2층 분석에서 자연 도출*되는지 + 흐름 끊김 발견 시 저자 묶음 escalate (자동 결정 영구 금지).
when_to_use: bookwriting-structure-review-master에서 element-checker-layer3 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-structure-review-flow-validator

## TLDR

부모 bookwriting-structure-review-master의 흐름 일관성 sub. 1층 끝 명제 → 2층 입증 → 3층 함의 도출의 3 단계 흐름을 결정론 keyword overlap + 의미 유사도로 검증하고 끊김 발견 시 저자 묶음 escalate한다. 자동 결정 영구 금지.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- element-checker-layer3 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — 흐름 일관성 + keyword overlap

```python
import re
from pathlib import Path
from dataclasses import dataclass, field
from relevance_scorer import RelevanceScorer   # M6 BM25

@dataclass
class FlowValidationResult:
    chapter_id: str
    layer1_proposition: str          # 1층 끝 핵심 명제
    layer1_to_2_score: float          # M6 BM25 — 명제 → 2층 입증 일관성
    layer2_to_3_score: float          # M6 BM25 — 2층 → 3층 자연 도출
    breaks_detected: list[str]        # 끊김 목록
    needs_bundle_escalation: bool

FLOW_THRESHOLD = 0.6   # M6 BM25 임계 — 미달 시 끊김

def validate_flow(
    chapter_id: str,
    chapter_dir: Path,
) -> FlowValidationResult:
    """3 layer 흐름 일관성 결정론 검증."""
    scorer = RelevanceScorer()

    narrative_path = chapter_dir / "narrative.md"
    analysis_path = chapter_dir / "analysis.md"
    implications_path = chapter_dir / "implications.md"

    # Step 1: 1층 끝 핵심 명제 추출
    layer1_text = narrative_path.read_text(encoding="utf-8") if narrative_path.exists() else ""
    proposition = _extract_last_proposition(layer1_text)

    layer2_text = analysis_path.read_text(encoding="utf-8") if analysis_path.exists() else ""
    layer3_text = implications_path.read_text(encoding="utf-8") if implications_path.exists() else ""

    # Step 2: 2층 본문이 *그 명제를 입증*하는지
    proposition_keywords = proposition.split() if proposition else []
    layer1_to_2 = scorer.score(layer2_text, proposition_keywords) if proposition_keywords else 0.0

    # Step 3: 3층 함의가 *2층 분석에서 자연 도출*되는지
    layer2_keywords = _extract_keywords(layer2_text)[:20]
    layer2_to_3 = scorer.score(layer3_text, layer2_keywords) if layer2_keywords else 0.0

    # Step 4: 흐름 끊김 발견 시 저자 묶음
    breaks = []
    if layer1_to_2 < FLOW_THRESHOLD:
        breaks.append(f"1층 → 2층 흐름 약함 (BM25 {layer1_to_2:.2f} < {FLOW_THRESHOLD})")
    if layer2_to_3 < FLOW_THRESHOLD:
        breaks.append(f"2층 → 3층 흐름 약함 (BM25 {layer2_to_3:.2f} < {FLOW_THRESHOLD})")

    return FlowValidationResult(
        chapter_id=chapter_id,
        layer1_proposition=proposition,
        layer1_to_2_score=layer1_to_2,
        layer2_to_3_score=layer2_to_3,
        breaks_detected=breaks,
        needs_bundle_escalation=bool(breaks),    # 자동 결정 금지
    )

def _extract_last_proposition(text: str) -> str:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return ""
    sentences = re.split(r"(?<=[.。!?])\s+", paragraphs[-1])
    return sentences[-1].strip() if sentences else paragraphs[-1]

def _extract_keywords(text: str) -> list[str]:
    return [w for w in text.split() if len(w) >= 2]
```

### 2. 명세 §출처 (SPEC: bookwriting-structure-review-subs.md SUB 4)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 1층 끝 핵심 명제 추출 | `_extract_last_proposition()` |
| Step 2: 2층 본문이 *그 명제를 입증*하는지 확인 | M6 BM25 `layer1_to_2_score` |
| Step 3: 3층 함의가 *2층 분석에서 자연 도출*되는지 확인 | M6 BM25 `layer2_to_3_score` |
| Step 4: 흐름 끊김 발견 시 저자 묶음 | `breaks_detected` + `needs_bundle_escalation` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + chapter_dir |
| Output | FlowValidationResult — proposition·BM25 scores·breaks·escalation |
| 후속 단계 | 저자 묶음 (자동 결정 금지) |
| Dependencies | element-checker-layer3 통과 |
| 결정론 모듈 | M6 RelevanceScorer (BM25) + 정규식 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M6 + 정규식 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 |
| #4 저자 작가성 | 흐름 끊김 저자 묶음 강제 — 자동 결정 영구 금지 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 흐름 평가 80%+ (M6 BM25 임계 0.6+)
- 끊김 검출 정확 (`breaks_detected`)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-structure-review-subs.md` §SUB 4
부모 마스터 SPEC: `specs/bookwriting-structure-review-master.md`
결정론 모듈: `lib/relevance_scorer.py` (M6 BM25)
