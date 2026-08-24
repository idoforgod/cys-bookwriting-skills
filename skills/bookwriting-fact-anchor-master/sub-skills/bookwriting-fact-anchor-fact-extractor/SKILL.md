---
name: bookwriting-fact-anchor-fact-extractor
description: 부모 bookwriting-fact-anchor-master의 INTERNAL sub. 흡수 자산 텍스트에서 fact·통계·정량 표현 (%·배·년·억·만·명·달러) 결정론 추출 + 임시 F-NNN ID 발급 + source_file·context 명시. M10 fact_extractor 정규식 결정론.
when_to_use: bookwriting-fact-anchor-master Step 2 (Fact Extractor 페르소나)에서 자동 호출. ① absorb 통과 자산이 입력. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-fact-anchor-fact-extractor

## TLDR

부모 bookwriting-fact-anchor-master의 ① 진입 sub. M10 fact_extractor 정규식 (percentage·scale·year·count)으로 fact를 결정론 추출하고 임시 F-NNN ID를 발급한다. 각 fact에 source_file과 context를 명시하여 후속 중복·충돌 검출 sub에 전달.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- `/bookwriting-fact-anchor cycle <target>` Step 2 자동
- `/bookwriting-fact-anchor extract <target>` 모드는 fact 추출만 단독 실행

## Detailed Methodology

### 1. 결정론 chain — M10 fact_extractor 호출

```python
from fact_extractor import FactExtractor, FactCandidate   # M10
from pathlib import Path
from dataclasses import dataclass

@dataclass
class AnchoredFact:
    fact_id: str            # F-NNN
    text: str
    fact_type: str          # percentage|scale|year|count
    source_file: str
    context: str            # ±50 chars surrounding text
    source_position: int

def extract_facts_from_asset(asset_path: Path, start_id: int = 1) -> list[AnchoredFact]:
    """① absorb 통과 자산에서 fact·통계·정량 표현 결정론 추출."""
    text = asset_path.read_text(encoding="utf-8")
    extractor = FactExtractor()

    # Step 1: M10 결정론 추출 (정규식 패턴 4종 — Round 9 정합)
    candidates = extractor.extract(text, start_id=start_id)
    # candidates: List[FactCandidate(fact_id, text, source_position, fact_type)]

    # Step 2-3: 저자 fact 패턴 강조 (100배·90% 확신·2027 임계 등 — 명세 SUB 1 Step 3)
    # → M10 PATTERNS["percentage"]·["scale"]·["year"]가 자동 포착

    # Step 4: source_file·context 명시
    anchored = []
    for c in candidates:
        start = max(0, c.source_position - 50)
        end = min(len(text), c.source_position + len(c.text) + 50)
        anchored.append(AnchoredFact(
            fact_id=c.fact_id,
            text=c.text,
            fact_type=c.fact_type,
            source_file=str(asset_path),
            context=text[start:end],
            source_position=c.source_position,
        ))

    return anchored
```

### 2. 명세 §출처 (SPEC: bookwriting-fact-anchor-subs.md SUB 1)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 자산 텍스트 로드 | `asset_path.read_text(encoding="utf-8")` |
| Step 2: 정규식 매칭 (N% / N배 / N년·연도 / N명·N달러) | M10 `extractor.extract()` — PATTERNS 4종 |
| Step 3: 저자 fact 패턴 식별 | M10 patterns가 자동 포착 (scale·percentage·year) |
| Step 4: 각 fact에 source_file·context 명시 | AnchoredFact dataclass — source_file + context (±50) |
| Step 5: 임시 F-NNN 발급 | M10 `start_id=N` → fact_id=f"F-{N:03d}" |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | asset_path (Path) — ① absorb 통과 자산 |
| Output | List[AnchoredFact] — fact 풀 (F-NNN, text, source_file, context) |
| 후속 sub | `bookwriting-fact-anchor-duplicate-detector` |
| Dependencies | ① absorb 통과 |
| 결정론 모듈 | M10 fact_extractor.FactExtractor |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M10 정규식 4 패턴 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 |
| #3 출처 명시 | source_file·context 필수 필드 |
| #7 결정론 환원 | M10 호출 100% 결정론 |

### 5. Verification (명세 §7)

- fact 추출 정확도 90%+ (M10 PATTERNS — Round 9 회귀 검증 완료)
- 정량 패턴 인식 (percentage·scale·year·count 4종 자동)
- source_file 명시 100% (필수 필드)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-fact-anchor-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-fact-anchor-master.md` §7 Step 2 + §13 페르소나 1 + 부록 결정론 (M10)
결정론 모듈: `lib/fact_extractor.py` (M10) — `expert_pool/deterministic-modules.md` §M10
저자 v1 R1: forecast-registry quantitative_anchor 정합 backbone
