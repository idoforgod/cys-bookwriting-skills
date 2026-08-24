---
name: bookwriting-evidence-collect-quantitative-anchor-extractor
description: 부모 bookwriting-evidence-collect-master의 INTERNAL sub ⭐ 저자 정량 표현 패턴. M4 QuantitativeAnchorExtractor 결정론 추출 + 저자 시그니처 정량 표현 (100배·90% 확신·2027 임계점·5억 명) 정합 + source_file·author·grade 명시 + 출처 미명시 정량 표현 Citation Gate Critical 즉시 차단 (M2 HallucinationDetector).
when_to_use: bookwriting-evidence-collect-master Step 4 (Quantitative Anchor Extractor 페르소나)에서 자동 호출. authority-grader 통과 후. `/bookwriting-evidence-collect quantitative` 모드도 본 sub 단독.
disable-model-invocation: true
---

# bookwriting-evidence-collect-quantitative-anchor-extractor

## TLDR

부모 bookwriting-evidence-collect-master의 ⭐ 저자 정량 표현 추출 sub. M4 QuantitativeAnchorExtractor로 수치 결정론 추출 + 저자 시그니처 패턴 (100배 스케일·90% 확신·2027 임계점·5억 명) 정합 + source_file·author·grade 명시. 출처 미명시 정량 → M2 Citation Gate Critical 즉시 차단.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- authority-grader 통과 후 → Step 4 자동
- `/bookwriting-evidence-collect quantitative <target>` 모드는 본 sub 단독

## Detailed Methodology

### 1. 결정론 chain — M4 + 저자 시그니처 + M2 Critical

```python
import re
from dataclasses import dataclass
from quantitative_extraction import QuantitativeAnchorExtractor   # M4
from citation_detection import HallucinationDetector              # M2

@dataclass
class QuantAnchor:
    anchor_id: str          # QA-NNN
    text: str               # "100배 스케일"
    value: float
    unit: str               # "배"|"%"|"년"|"명"|"$"
    source_file: str
    author: str | None
    grade: str              # "A"|"B"|"C"|"D"|"E"
    is_park_signature: bool # 저자 시그니처 패턴 일치
    citation_gate_critical: bool = False
    critical_reason: str | None = None

# 저자 시그니처 정량 표현 패턴 (부모 §3 Philosophy + §17 검증 3)
PARK_SIGNATURES = [
    re.compile(r"100\s*배"),                  # 산업혁명 × 10 × 10
    re.compile(r"9\d\s*%\s*확신"),            # 90% 확신 (Amodei 1-3년)
    re.compile(r"2027\s*년?\s*임계"),         # 2027 임계점
    re.compile(r"[1-9]\s*억\s*명"),           # 5억 명 영향 범위
    re.compile(r"1-3\s*년"),                  # Amodei 시간 추정
]

def extract_quantitative_anchors(graded_evidence: list) -> list[QuantAnchor]:
    """M4 + 저자 시그니처 + Citation Gate Critical 결정론."""
    extractor = QuantitativeAnchorExtractor()
    detector = HallucinationDetector()
    results = []
    anchor_counter = 0

    for ev in graded_evidence:
        if ev.is_excluded:
            continue
        text = _safe_read(ev.source_file)
        if not text:
            continue

        # Step 1: M4 결정론 추출 (Round 9 정합 — quantitative_extraction PATTERNS)
        anchors_raw = extractor.extract_all(text)

        for raw in anchors_raw:
            anchor_counter += 1
            anchor_id = f"QA-{anchor_counter:03d}"

            # Step 2: 저자 시그니처 정량 표현 정합
            is_signature = any(p.search(raw.text) for p in PARK_SIGNATURES)

            # Step 3: source_file·author·grade 명시
            qa = QuantAnchor(
                anchor_id=anchor_id,
                text=raw.text,
                value=raw.value,
                unit=raw.unit,
                source_file=ev.source_file,
                author=ev.author,
                grade=ev.grade,
                is_park_signature=is_signature,
            )

            # Step 5: 출처 미명시 정량 표현 → Citation Gate Critical 차단
            if not ev.author and not _has_source_marker(raw.text, text):
                # M2 HallucinationDetector 검증
                signals = detector.detect_all(text, citation_metadata=None)
                if signals.is_critical():
                    qa.citation_gate_critical = True
                    qa.critical_reason = "출처 미명시 정량 표현 (할루시네이션 의심)"

            results.append(qa)

    # Step 4: forecast-registry.quantitative_anchor 갱신은 별도 sub (Registry Syncer, 20주차)
    return results

def _safe_read(path: str) -> str:
    from pathlib import Path
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""

def _has_source_marker(anchor_text: str, full_text: str) -> bool:
    """anchor 주변에 (저자 연도) 출처 표시 존재 확인."""
    idx = full_text.find(anchor_text)
    if idx == -1:
        return False
    nearby = full_text[max(0, idx-50):idx+len(anchor_text)+50]
    # (Author 2024)·[저자] 양식 매칭
    return bool(re.search(r"\([\w가-힣\s,]+\s*\d{4}\)|\[[\w가-힣]+\]", nearby))
```

### 2. 명세 §출처 (SPEC: bookwriting-evidence-collect-subs.md SUB 3) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 수치 정규식 매칭 (N% / N배 / N년·연도 / N명·N달러 / N% 확신) | M4 `extractor.extract_all()` |
| Step 2: 저자 정량 표현 시그니처 패턴 정합 (100배·90%·2027·5억 명) | `PARK_SIGNATURES` 5 정규식 |
| Step 3: 각 정량 앵커에 source_file·author·grade 명시 | QuantAnchor dataclass — 3 필드 |
| Step 4: forecast-registry 갱신 (sync 별도 sub) | 20주차 SUB 5 Registry Syncer 위임 |
| Step 5: 출처 미명시 정량 표현 → Citation Gate Critical 차단 | M2 `detector.detect_all()` + `is_critical()` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | graded_evidence (authority-grader 통과 — is_excluded=False) |
| Output | List[QuantAnchor] — anchor_id·text·value·unit·source·grade·is_park_signature·critical |
| 후속 sub | `bookwriting-evidence-collect-verification-signal-finder` (20주차) |
| Dependencies | authority-grader 통과 + forecast-registry.yaml quantitative_anchor 필드 |
| 결정론 모듈 | M4 QuantitativeAnchorExtractor + M2 HallucinationDetector |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 ⭐ | M2 Citation Gate Critical 즉시 차단 — 출처 미명시 정량 영구 제외 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 + 저자 시그니처 5 패턴 |
| #3 출처 명시 | source_file·author·grade 3 필드 강제 |
| #4 저자 작가성 | is_park_signature 플래그 — 저자 정량 표현 패턴 보존 |
| #7 결정론 환원 | M4 + M2 + 정규식 100% 결정론 |

### 5. Verification (명세 §7)

- 정량 앵커 평균 0.6/자료 (부모 §10 정량)
- 모든 정량 앵커에 source_file 명시 (필수 필드)
- 저자 시그니처 정량 표현 (100배·90% 등) 식별 (is_park_signature)
- Citation Gate Critical 0건 (정량 앵커에 한해 — 출처 미명시는 영구 제외)
- 영속 자산 보호: forecast-registry write 영구 금지 (20주차 Registry Syncer 위임)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-evidence-collect-subs.md` §SUB 3 ⭐
부모 마스터 SPEC: `specs/bookwriting-evidence-collect-master.md` §7 Step 4 + §13 페르소나 3 ⭐ + §12 Citation Gate ⭐⭐⭐ + 부록 결정론 (M4 + M2)
저자 시그니처: 부모 §3 + §17 검증 3 (100배·90% 확신·2027 임계점·5억 명)
결정론 모듈: `lib/quantitative_extraction.py` (M4) + `lib/citation_detection.py` (M2)
영속 자산 보호: PHASE3B_HANDOFF §8 (forecast-registry write 20주차 Registry Syncer 위임)
