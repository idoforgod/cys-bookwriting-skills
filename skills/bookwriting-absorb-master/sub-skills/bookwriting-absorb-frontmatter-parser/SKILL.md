---
name: bookwriting-absorb-frontmatter-parser
description: 부모 bookwriting-absorb-master의 INTERNAL sub. inbox/import 자산의 yaml frontmatter 결정론 파싱 + 필수 메타(type·source·to·link·created) 추출 + 누락 필드 식별. yaml.safe_load 결정론.
when_to_use: bookwriting-absorb-master Step 2 (Frontmatter Parser 페르소나)에서 자동 호출. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-absorb-frontmatter-parser

## TLDR

부모 bookwriting-absorb-master의 ① 진입 sub. inbox/*.md·import path의 yaml frontmatter를 yaml.safe_load 결정론으로 파싱하고 type·source·to·link·created 필수 필드를 추출한다. 누락 필드는 다음 sub (Type Classifier)에 전달.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- `/bookwriting-absorb inbox` → Step 2 (frontmatter 추출) 자동
- `/bookwriting-absorb import <path>` → Step 2 자동
- `/bookwriting-absorb classify <path>` → Step 2 자동

## Detailed Methodology

### 1. 결정론 chain (LLM 추론 영구 금지)

```python
import yaml
from pathlib import Path

def parse_frontmatter(file_path: Path) -> tuple[dict, list[str]]:
    """파일 head의 --- 사이 yaml 결정론 파싱.

    Returns:
        (frontmatter_dict, missing_required_fields)
    """
    REQUIRED = ["type", "source", "to", "link", "created"]
    text = file_path.read_text(encoding="utf-8")

    # Step 1: --- 분리
    if not text.startswith("---\n"):
        return ({}, REQUIRED)  # frontmatter 없음 — 전부 누락
    end = text.find("\n---\n", 4)
    if end == -1:
        return ({}, REQUIRED)
    raw = text[4:end]

    # Step 2: yaml.safe_load (결정론·CVE 안전)
    try:
        meta = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        return ({}, REQUIRED)  # 형식 오류 — graceful

    if not isinstance(meta, dict):
        return ({}, REQUIRED)

    # Step 3: 필수 필드 추출 + 누락 식별
    missing = [f for f in REQUIRED if f not in meta or meta[f] in (None, "")]
    return (meta, missing)
```

### 2. 명세 §출처 (SPEC: bookwriting-absorb-subs.md SUB 1)

| 명세 항목 | 본 sub 구현 |
|---|---|
| Step 1: 파일 head 파싱 (--- 사이 yaml) | `text.startswith("---\n")` + `text.find("\n---\n", 4)` |
| Step 2: type·source·to·link·created 필드 추출 | `REQUIRED = [...]` |
| Step 3: 누락 필드 식별 → Type Classifier에게 전달 | `return (meta, missing)` |
| Step 4: 형식 오류 시 warning + skip | `try ... except yaml.YAMLError` → graceful |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | `inbox/*.md` 또는 `--target <path>` 단일 파일 |
| Output | frontmatter dict + 누락 필드 목록 (list[str]) |
| 후속 sub | `bookwriting-absorb-type-classifier` (누락 필드 시) |
| Dependencies | 없음 (① 진입 sub) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | yaml.safe_load 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 환원 |
| #7 결정론 환원 | LLM 추론 코드 없음 — 100% 결정론 |

### 5. Verification (명세 §7)

- frontmatter 인식률 95%+ (yaml.safe_load 표준 준수)
- 누락 필드 정확 식별 (REQUIRED 5개 명시)
- yaml 오류 graceful 처리 (예외 시 `(dict={}, missing=REQUIRED)` 반환)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-absorb-subs.md` §SUB 1
부모 마스터 SPEC: `specs/bookwriting-absorb-master.md` §7 Step 2 + §13 페르소나 1
결정론 양식: yaml.safe_load (Python 표준 yaml 모듈)
