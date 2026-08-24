---
name: bookwriting-content-expand-proposition-restater
description: 부모 bookwriting-content-expand-master의 INTERNAL sub. 저자 2층 골격 요소 1 (핵심 명제 재진술) 담당. 1층 끝 핵심 명제 + M4 정량 앵커 (Quantitative Anchor) 결정론 결합 + 저자 시그니처 *X와 Y 사이의 거리에서* 적용 시도 + 200-400자 2층 첫 단락 골격.
when_to_use: bookwriting-content-expand-master에서 ⑧ narrative-craft 1층 명제 + ④ evidence-collect 정량 앵커 모두 준비 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-content-expand-proposition-restater

## TLDR

부모 bookwriting-content-expand-master의 저자 2층 골격 *요소 1* 담당. ⑧ narrative-craft의 1층 끝 핵심 명제 + ④ evidence-collect의 정량 앵커 (M4 QuantitativeAnchorExtractor)를 결정론 결합하여 2층 첫 단락 골격을 조립한다. 저자 시그니처 *X와 Y 사이의 거리에서* 적용 시도.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- ⑧ narrative-craft 1층 명제 산출 + ④ evidence-collect 정량 앵커 준비 후 자동

## Detailed Methodology

### 1. 결정론 chain — 1층 명제 + 정량 앵커 결합

```python
import re
from pathlib import Path
from dataclasses import dataclass
from quantitative_extraction import QuantitativeAnchorExtractor   # M4

@dataclass
class PropositionRestated:
    chapter_id: str
    layer1_proposition: str          # 1층 끝 핵심 명제
    quant_anchors: list[str]         # 정량 앵커 1+
    restated_text: str               # 200-400자 골격
    signature_attempted: bool        # *X와 Y 사이의 거리* 적용 여부

def restate_proposition(
    narrative_path: Path,            # chapters/<ch>/narrative.md
    quant_anchors_data: list[dict],
    chapter_id: str,
) -> PropositionRestated:
    """1층 명제 + 정량 앵커 결정론 재진술."""
    extractor = QuantitativeAnchorExtractor()

    # Step 1: chapters/<ch>/narrative.md의 1층 끝 핵심 명제 추출
    if not narrative_path.exists():
        layer1_text = ""
    else:
        narrative_text = narrative_path.read_text(encoding="utf-8")
        layer1_text = _extract_last_proposition(narrative_text)

    # Step 2: 통찰에 연결된 정량 앵커 (Quantitative Anchor) 로드
    # — M4 extract_all로 narrative_text에서도 추가 추출 가능
    anchors_from_qa = [qa.get("text", "") for qa in quant_anchors_data if qa.get("source_chapter") == chapter_id]
    anchors_from_extractor = [a.text for a in extractor.extract_all(layer1_text)] if layer1_text else []
    all_anchors = list(set(anchors_from_qa + anchors_from_extractor))

    # Step 3: 명제를 정량 데이터와 함께 재진술
    # — 예: "AGI는 메타도구다" + "1-3년 90% 확신·100배 스케일"
    restated = _assemble_restatement(layer1_text, all_anchors[:3])

    # Step 4: 저자 시그니처 *X와 Y 사이의 거리에서* 적용 시도
    sig_attempted = False
    if len(all_anchors) >= 2:
        # 두 정량 앵커 사이의 거리 — 시그니처 패턴 기회
        restated += f"\n[시그니처: '{all_anchors[0]}와 {all_anchors[1]} 사이의 거리에서' 적용 가능]"
        sig_attempted = True

    # Step 5: 2층 첫 단락에 배치 — 부모 마스터가 analysis.md write
    return PropositionRestated(
        chapter_id=chapter_id,
        layer1_proposition=layer1_text,
        quant_anchors=all_anchors,
        restated_text=restated,
        signature_attempted=sig_attempted,
    )

def _extract_last_proposition(narrative_text: str) -> str:
    """1층 끝 핵심 명제 — 마지막 비어있지 않은 단락의 마지막 문장."""
    paragraphs = [p.strip() for p in narrative_text.split("\n\n") if p.strip()]
    if not paragraphs:
        return ""
    last_para = paragraphs[-1]
    sentences = re.split(r"(?<=[.。!?])\s+", last_para)
    return sentences[-1].strip() if sentences else last_para

def _assemble_restatement(proposition: str, anchors: list[str]) -> str:
    lines = ["[2층 요소 1 — 핵심 명제 재진술]"]
    lines.append(f"- 1층 끝 명제: {proposition}")
    if anchors:
        lines.append(f"- 정량 앵커: {' · '.join(anchors)}")
    lines.append("[저자 본문 200-400자 채워넣기 — 명제 + 정량]")
    return "\n".join(lines)
```

### 2. 명세 §출처 (SPEC: bookwriting-content-expand-subs.md SUB 5)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: chapters/<ch>/narrative.md의 1층 끝 핵심 명제 추출 | `_extract_last_proposition()` |
| Step 2: 통찰에 연결된 정량 앵커 (Quantitative Anchor) 로드 | M4 + quant_anchors_data 통합 |
| Step 3: 명제를 정량 데이터와 함께 재진술 | `_assemble_restatement()` |
| Step 4: 저자 시그니처 *X와 Y 사이의 거리에서* 적용 시도 | 2 앵커 조건 분기 |
| Step 5: 2층 첫 단락에 배치 | 부모 마스터 yaml write |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | narrative_path (chapters/<ch>/narrative.md) + quant_anchors_data (④ 산출) + chapter_id |
| Output | PropositionRestated — layer1_proposition·quant_anchors·restated_text·signature_attempted |
| 후속 sub | 다른 ⑦ sub와 통합 (부모 마스터 조립) |
| Dependencies | ⑧ narrative-craft 1층 명제 + ④ evidence-collect 정량 앵커 |
| 결정론 모듈 | M4 QuantitativeAnchorExtractor + 자체 정규식 (마지막 문장 추출) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M4 + 정규식 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step + *X와 Y 사이의 거리* 시그니처 1:1 |
| #4 저자 작가성 | 200-400자는 저자 직접 — sub는 골격만 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §6)

- 정량 앵커 1+ 포함 (`quant_anchors` ≥ 1)
- 시그니처 활용 시도 (`signature_attempted` 플래그)
- voice_score 0.7+ (voice-aligner 후속 발동)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-content-expand-subs.md` §SUB 5
부모 마스터 SPEC: `specs/bookwriting-content-expand-master.md` (2층 요소 1 핵심 명제 재진술)
저자 v1: 2층 표준 골격 1번 요소
결정론 모듈: `lib/quantitative_extraction.py` (M4)
시그니처 *X와 Y 사이의 거리에서*: voice-craft 5 패턴 중 1개
