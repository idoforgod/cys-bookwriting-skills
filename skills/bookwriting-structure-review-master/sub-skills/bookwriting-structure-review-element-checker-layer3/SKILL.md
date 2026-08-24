---
name: bookwriting-structure-review-element-checker-layer3
description: 부모 bookwriting-structure-review-master의 INTERNAL sub. 저자 v1 3층 표준 골격 6요소 (본문 의미 한 문장·개인/조직/정책 차원 응답·한국 결정 윈도우 KW-1·KW-2·KW-3·검증 신호) 결정론 정규식 검출 + 각 요소 ✅/⚠️ 표시.
when_to_use: bookwriting-structure-review-master에서 element-checker-layer2 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-structure-review-element-checker-layer3

## TLDR

부모 bookwriting-structure-review-master의 3층 6요소 검출 sub. implications.md에서 저자 v1 3층 표준 골격 6요소 (의미 문장·개인/조직/정책 응답·한국 결정 윈도우·검증 신호)를 결정론 정규식으로 검출한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- element-checker-layer2 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — 3층 6요소 정규식

```python
import re
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class Layer3ElementCheck:
    chapter_id: str
    element_1_meaning_sentence: bool       # 본문 의미 한 문장
    element_2_individual_response: bool    # 개인 차원 응답
    element_3_organizational_response: bool   # 조직 차원 응답
    element_4_policy_response: bool        # 정책 차원 응답
    element_5_korea_decision_window: bool  # 한국 결정 윈도우 (KW-1·KW-2·KW-3, 해당 시)
    element_6_verification_signal: bool    # 검증 신호 (해당 시)
    missing_elements: list[str] = field(default_factory=list)

ELEMENT_PATTERNS = {
    "1_meaning": re.compile(r"(의미|핵심은|결국|요컨대)"),
    "2_individual": re.compile(r"(개인|독자|당신|나|자기)\s*(차원|관점|입장|수준)"),
    "3_organizational": re.compile(r"(조직|기업|회사|팀)\s*(차원|관점|입장|수준)"),
    "4_policy": re.compile(r"(정책|정부|국가|규제|법)\s*(차원|관점|입장|수준)"),
    "5_korea_window": re.compile(r"KW-[123]|한국\s*결정\s*윈도우|한국[\s가이은]+해야"),
    "6_verification": re.compile(r"verification_signal|falsifies_if|검증\s*신호|반증|\d+년\s*후"),
}

ELEMENT_NAMES = {
    "1_meaning": "본문 의미 한 문장",
    "2_individual": "개인 차원 응답",
    "3_organizational": "조직 차원 응답",
    "4_policy": "정책 차원 응답",
    "5_korea_window": "한국 결정 윈도우",
    "6_verification": "검증 신호",
}

def check_layer3_elements(chapter_id: str, implications_path: Path) -> Layer3ElementCheck:
    """3층 6요소 결정론 검출."""
    if not implications_path.exists():
        return Layer3ElementCheck(
            chapter_id=chapter_id,
            element_1_meaning_sentence=False,
            element_2_individual_response=False,
            element_3_organizational_response=False,
            element_4_policy_response=False,
            element_5_korea_decision_window=False,
            element_6_verification_signal=False,
            missing_elements=list(ELEMENT_NAMES.values()),
        )

    text = implications_path.read_text(encoding="utf-8")
    checks = {key: bool(pat.search(text)) for key, pat in ELEMENT_PATTERNS.items()}
    missing = [ELEMENT_NAMES[k] for k, present in checks.items() if not present]

    return Layer3ElementCheck(
        chapter_id=chapter_id,
        element_1_meaning_sentence=checks["1_meaning"],
        element_2_individual_response=checks["2_individual"],
        element_3_organizational_response=checks["3_organizational"],
        element_4_policy_response=checks["4_policy"],
        element_5_korea_decision_window=checks["5_korea_window"],
        element_6_verification_signal=checks["6_verification"],
        missing_elements=missing,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-structure-review-subs.md SUB 3)

| 명세 요소 | 본 sub 구현 |
|---|---|
| 1. 본문 의미 한 문장 | `ELEMENT_PATTERNS["1_meaning"]` |
| 2. 개인 차원 응답 | `ELEMENT_PATTERNS["2_individual"]` |
| 3. 조직 차원 응답 | `ELEMENT_PATTERNS["3_organizational"]` |
| 4. 정책 차원 응답 | `ELEMENT_PATTERNS["4_policy"]` |
| 5. 한국 결정 윈도우 (KW-1·KW-2·KW-3) | `ELEMENT_PATTERNS["5_korea_window"]` |
| 6. 검증 신호 (verification_signal) | `ELEMENT_PATTERNS["6_verification"]` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + implications_path |
| Output | Layer3ElementCheck — 6 bool + missing_elements |
| 후속 sub | flow-validator |
| Dependencies | element-checker-layer2 통과 |
| 결정론 모듈 | 자체 정규식 6 패턴 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 정규식 결정론 |
| #2 grill-me 원문 일치 | 명세 6요소 1:1 환원 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §5)

- 6요소 검출 정확도 95%+

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-structure-review-subs.md` §SUB 3
부모 마스터 SPEC: `specs/bookwriting-structure-review-master.md`
저자 v1 3층 6요소: chapter-pipeline.md
