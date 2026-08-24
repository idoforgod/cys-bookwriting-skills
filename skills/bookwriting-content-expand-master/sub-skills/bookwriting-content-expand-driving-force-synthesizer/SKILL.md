---
name: bookwriting-content-expand-driving-force-synthesizer
description: 부모 bookwriting-content-expand-master의 INTERNAL sub. 저자 2층 골격 요소 3 (추동력) 담당. 약신호를 만든 시스템적 힘 (한계비용 제로·자본 동원·패러다임 전환·기술 곡선·정치 변수)을 결정론 패턴 매칭 + 200-500자 본문 골격 + 시그니처 패턴 *변수 X 따라 결과 갈리는* 적용 시도 + voice·citation gate.
when_to_use: bookwriting-content-expand-master에서 weak-signal-synthesizer 통과 후 자동 호출.
disable-model-invocation: true
---

# bookwriting-content-expand-driving-force-synthesizer

## TLDR

부모 bookwriting-content-expand-master의 저자 2층 골격 *요소 3* 담당. 약신호를 만든 시스템적 힘을 저자 추동력 패턴 (한계비용·자본·기술 곡선·정치) 결정론 매칭으로 식별하고 200-500자 본문 골격을 조립한다. 시그니처 *변수 X 따라 결과 갈리는* 적용 시도.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- weak-signal-synthesizer 통과 후 자동

## Detailed Methodology

### 1. 결정론 chain — 추동력 패턴 매칭

```python
import re
from dataclasses import dataclass, field

@dataclass
class DrivingForceContent:
    insight_id: str
    detected_forces: list[str]      # ["한계비용", "자본", "패러다임", "기술 곡선", "정치"]
    body_text: str                   # 200-500자 골격
    signature_applied: bool          # 변수 X 따라 결과 갈리는 패턴 활용 여부

# 저자 추동력 패턴 (부모 §3·skeleton.md §추동력)
FORCE_PATTERNS = {
    "한계비용": re.compile(r"한계비용|marginal cost|cost->0|제로"),
    "자본": re.compile(r"자본|capital|투자|VC|funding"),
    "패러다임": re.compile(r"패러다임|paradigm|전환|shift"),
    "기술 곡선": re.compile(r"곡선|curve|exponential|S-curve|로지스틱"),
    "정치": re.compile(r"정치|규제|법|국가|geopolitics"),
    "피드백": re.compile(r"피드백|feedback|루프|loop|순환"),
    "임계": re.compile(r"임계|critical|tipping|threshold"),
}

def synthesize_driving_force(
    weak_signal_content,                # 앞 sub 산출
    insight: dict,
    system_loops_mapping: list[dict] | None = None,
) -> DrivingForceContent:
    """추동력 결정론 패턴 매칭 + 본문 골격 조립."""
    # Step 1: 약신호 본문 로드 (앞 sub 출력)
    weak_text = weak_signal_content.body_text + " " + insight.get("text", "")

    # Step 2: 저자 추동력 패턴 매칭
    detected = []
    for force_name, pattern in FORCE_PATTERNS.items():
        if pattern.search(weak_text):
            detected.append(force_name)

    # Step 3: 추동력 본문 작성 (시스템 사고 흐름)
    body = _assemble_driving_force_skeleton(insight, detected, system_loops_mapping)

    # Step 4: 시그니처 패턴 *변수 X 따라 결과 갈리는* 적용 시도
    sig_applied = False
    if "정치" in detected and len(detected) >= 2:
        # 정치 변수가 다른 추동력과 결합되어 분기 효과 — 시그니처 적용 기회
        body += "\n[시그니처: 변수 X(정치) 따라 결과 갈리는 동일 시스템 — 적용 가능]"
        sig_applied = True

    # Step 5: voice·citation gate (부모 cross-cutting)
    return DrivingForceContent(
        insight_id=insight.get("id", ""),
        detected_forces=detected,
        body_text=body,
        signature_applied=sig_applied,
    )

def _assemble_driving_force_skeleton(insight: dict, forces: list[str], loops) -> str:
    lines = ["[2층 요소 3 — 추동력]"]
    if forces:
        lines.append(f"- 식별 추동력: {' / '.join(forces)}")
    else:
        lines.append("- 추동력: 저자 직접 식별 필요")
    if loops:
        loop_ids = [m.get("loop_id", "") for m in loops]
        lines.append(f"- 관련 시스템 루프: {','.join(filter(None, loop_ids))}")
    lines.append("[저자 본문 200-500자 채워넣기 — 시스템 사고 흐름]")
    return "\n".join(lines)
```

### 2. 명세 §출처 (SPEC: bookwriting-content-expand-subs.md SUB 2)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 약신호 본문 로드 (앞 sub 출력) | `weak_signal_content` 입력 |
| Step 2: 저자 추동력 패턴 매칭 | `FORCE_PATTERNS` 7 정규식 |
| Step 3: 추동력 본문 작성 (시스템 사고 흐름) | `_assemble_driving_force_skeleton()` |
| Step 4: 시그니처 *변수 X 따라 결과 갈리는* 적용 시도 | 정치 + 추동력 ≥ 2 조건 분기 |
| Step 5: voice·citation gate | 부모 cross-cutting |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | weak_signal_content + insight + system_loops_mapping |
| Output | DrivingForceContent — detected_forces·body_text·signature_applied |
| 후속 sub | `bookwriting-content-expand-system-loop-narrator` |
| Dependencies | weak-signal-synthesizer 통과 |
| 결정론 모듈 | 자체 정규식 7 패턴 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 정규식 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step + 추동력 패턴 1:1 환원 |
| #4 저자 작가성 | 본문 200-500자는 저자 직접 작성 — sub는 골격 조립만 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- 추동력이 약신호와 *논리적 연결* (detected_forces 매칭)
- 저자 시스템 사고 어휘 사용 (한계비용·피드백·임계 — `FORCE_PATTERNS` 포함)
- 시그니처 패턴 활용 시도 (`signature_applied` 플래그)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-content-expand-subs.md` §SUB 2
부모 마스터 SPEC: `specs/bookwriting-content-expand-master.md` (2층 요소 3 추동력)
저자 추동력 어휘: skeleton.md §추동력
저자 시그니처: voice-craft sub와 양식 정합 (변수 X 따라 결과 갈리는 동일 시스템)
