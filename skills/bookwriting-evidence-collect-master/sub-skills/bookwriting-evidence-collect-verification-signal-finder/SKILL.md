---
name: bookwriting-evidence-collect-verification-signal-finder
description: 부모 bookwriting-evidence-collect-master의 INTERNAL sub. 저자 v1 R5 verification_signal·falsifies_if 결정론 정규식 패턴 발견 (5년 후·10년 후·N% 도달·반증 시 등) + chapter-pipeline.md R5 양식 정합 + forecast-registry P-NNN에 추가 + 저자 검증 가능성 점수 (재인용·재추적).
when_to_use: bookwriting-evidence-collect-master Step 5 (Verification Signal Finder 페르소나)에서 자동 호출. authority-grader 통과 후. `/bookwriting-evidence-collect verification-signal` 모드도 본 sub 단독.
disable-model-invocation: true
---

# bookwriting-evidence-collect-verification-signal-finder

## TLDR

부모 bookwriting-evidence-collect-master의 R5 검증 신호 sub. 저자 v1 chapter-pipeline.md R5의 *verification_signal·falsifies_if* 양식을 결정론 정규식으로 evidence 텍스트에서 추출하고, 5년·10년 후 책 명제가 검증·반증되는 지표를 발견하여 forecast-registry P-NNN에 추가한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- authority-grader 통과 후 → Step 5 자동
- `/bookwriting-evidence-collect verification-signal <target>` 모드는 본 sub 단독

## Detailed Methodology

### 1. 결정론 chain — R5 정규식 + 검증 가능성 점수

```python
import re
from dataclasses import dataclass
from enum import Enum

class SignalType(str, Enum):
    VERIFICATION = "verification_signal"   # 5년 후 X 도달 시 검증
    FALSIFICATION = "falsifies_if"         # Z 미발생 시 반증
    VERIFICATION_CANDIDATE = "candidate"   # 2030년까지 N% 도달 예상

@dataclass
class VerificationSignal:
    signal_id: str             # VS-NNN
    signal_type: SignalType
    text: str
    target_year: int | None
    target_metric: str | None  # 추적 지표 (점유율·% 등)
    source_file: str
    p_nnn_link: str | None     # forecast-registry P-NNN 연결
    verifiability_score: float # 0.0-1.0 (재인용·재추적 가능성)

# 저자 v1 R5 양식 정규식 (chapter-pipeline.md R5 원문 정합)
PATTERN_VERIFICATION = re.compile(
    r"(\d+)\s*년\s*(?:후|뒤|이내)\s*([^,.\n]+?)(?:가|이|면|도달|달성)"
)
PATTERN_FALSIFICATION = re.compile(
    r"([^,.\n]+?)\s*(?:미발생|불발|실패|반증)\s*(?:시|면)\s*([^,.\n]+?)(?:반증|부정|기각)"
)
PATTERN_CANDIDATE = re.compile(
    r"(\d{4})\s*년\s*까지\s*([^,.\n]+?)(?:N|\d+)%"
)

def find_verification_signals(graded_evidence: list, forecast_registry: dict) -> list[VerificationSignal]:
    """R5 verification_signal·falsifies_if 결정론 발견."""
    from pathlib import Path
    results = []
    counter = 0

    for ev in graded_evidence:
        if ev.is_excluded:
            continue
        text = _safe_read(ev.source_file)
        if not text:
            continue

        # Step 1: evidence 텍스트에서 검증 가능 표현 패턴 매칭
        for m in PATTERN_VERIFICATION.finditer(text):
            counter += 1
            year_offset = int(m.group(1))
            target = m.group(2).strip()
            results.append(VerificationSignal(
                signal_id=f"VS-{counter:03d}",
                signal_type=SignalType.VERIFICATION,
                text=m.group(0),
                target_year=None,   # offset만 알려짐
                target_metric=target,
                source_file=ev.source_file,
                p_nnn_link=_match_to_pnnn(target, forecast_registry),
                verifiability_score=_score(year_offset, target),
            ))

        for m in PATTERN_FALSIFICATION.finditer(text):
            counter += 1
            results.append(VerificationSignal(
                signal_id=f"VS-{counter:03d}",
                signal_type=SignalType.FALSIFICATION,
                text=m.group(0),
                target_year=None,
                target_metric=m.group(1).strip(),
                source_file=ev.source_file,
                p_nnn_link=None,
                verifiability_score=_score(0, m.group(2)),
            ))

        for m in PATTERN_CANDIDATE.finditer(text):
            counter += 1
            results.append(VerificationSignal(
                signal_id=f"VS-{counter:03d}",
                signal_type=SignalType.VERIFICATION_CANDIDATE,
                text=m.group(0),
                target_year=int(m.group(1)),
                target_metric=m.group(2).strip(),
                source_file=ev.source_file,
                p_nnn_link=_match_to_pnnn(m.group(2), forecast_registry),
                verifiability_score=_score_year(int(m.group(1))),
            ))

    # Step 2: 저자 v1 chapter-pipeline.md R5 양식 정합 (P-NNN에 추가 — 부모가 yaml write)
    # Step 3: forecast-registry 해당 P-NNN에 추가
    # Step 4: 저자 검증 가능성 점수 (verifiability_score)
    return results

def _safe_read(path: str) -> str:
    from pathlib import Path
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""

def _match_to_pnnn(target_metric: str, forecast_registry: dict) -> str | None:
    """P-NNN의 quantitative_anchor와 매칭."""
    for p in forecast_registry.get("predictions", []):
        anchor = p.get("quantitative_anchor", "")
        if any(kw in anchor for kw in target_metric.split() if len(kw) >= 2):
            return p.get("id")
    return None

def _score(year_offset: int, target: str) -> float:
    """검증 가능성 점수 — 짧은 기간·명확 지표일수록 높음."""
    base = 1.0 if year_offset <= 5 else (0.7 if year_offset <= 10 else 0.4)
    has_metric = any(c.isdigit() for c in target) or "%" in target
    return min(1.0, base + (0.1 if has_metric else 0))

def _score_year(target_year: int) -> float:
    from datetime import datetime
    offset = target_year - datetime.now().year
    return _score(offset, "")
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-collect-subs.md SUB 4)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: evidence 텍스트 검증 가능 표현 패턴 매칭 (5년 후·반증·N% 도달) | `PATTERN_VERIFICATION` + `PATTERN_FALSIFICATION` + `PATTERN_CANDIDATE` |
| Step 2: 저자 v1 chapter-pipeline.md R5 양식 정합 | SignalType enum 3종 (R5 양식 원문 그대로) |
| Step 3: forecast-registry 해당 P-NNN에 추가 | `_match_to_pnnn()` + 부모 yaml write 위임 |
| Step 4: 저자 검증 가능성 점수 (재인용·재추적) | `verifiability_score` 점수 산출 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | graded_evidence (authority-grader 통과) + forecast-registry (dict) |
| Output | List[VerificationSignal] — signal_id·type·text·target·source·p_nnn_link·verifiability_score |
| 후속 sub | `bookwriting-evidence-collect-forecast-registry-syncer` |
| Dependencies | authority-grader 통과 |
| 결정론 모듈 | 자체 정규식 3종 (R5 패턴) + 매칭 dict lookup |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | 정규식 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 환원 + 저자 v1 R5 양식 원문 |
| #3 출처 명시 | source_file + p_nnn_link 필수 |
| #7 결정론 환원 | 100% 결정론 (정규식 + dict lookup + 점수 산출) |

### 5. Verification (명세 §7)

- 검증 신호 3-7건/챕터 (부모 §10 정량)
- 저자 v1 R5 양식 정합 (chapter-pipeline.md R5 원문)
- forecast-registry verification_signal 필드 갱신 (부모가 yaml write)
- 저자 책 *5년·10년 후 검증 가능*한 학술 신뢰성 보장

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-collect-subs.md` §SUB 4
부모 마스터 SPEC: `specs/bookwriting-evidence-collect-master.md` §7 Step 5 + §13 페르소나 4 + 부록 R5 강제
저자 v1 R5: `$BOOK_ROOT/workflows/book-planning.md` R5 원문 (verification_signal·falsifies_if)
영속 자산 보호: PHASE3B_HANDOFF §8 (forecast-registry write 부모 마스터 위임)
