---
name: bookwriting-notebooklm-bridge
description: 옵션 A+ 자기완결의 *유일한 예외* — 저자 명시 호출로만 NotebookLM 자산을 책 쓰기 워크플로우에 import. bookwriting-master 가 발동 (이 워커는 직접 호출 영구 금지). M16-A RiskAssessor + M15 TraumaWitnessDetector 통과 후 search_paths에 등재.
when_to_use: 저자가 명시적으로 `/bookwriting notebooklm import <notebook_id>` 호출 시. 다른 단계 마스터의 자동 호출 영구 금지.
---

# bookwriting-notebooklm-bridge (외부 자산 옵션 A+ 예외)

## TLDR

저자 NotebookLM 자산 → bookwriting search_paths tier_2_explicit 등재. **저자 명시 호출만 허용**. 다른 단계 마스터·sub-skill 자동 호출 영구 금지.

## Triggers

- `/bookwriting notebooklm import <notebook_id>` — 저자 직접 (유일한 호출 경로)
- `/bookwriting notebooklm list` — 등재된 외부 자산 목록 조회
- *그 외 모든 자동 호출 영구 차단*

## Detailed Methodology

### 1. 옵션 A+ 자기완결 — 예외 협약

저자 명시: "옵션 A+ 자기완결 — bookwriting은 self-contained, Dr. Choi's 542 스킬은 외부 manual 호출만 (옵션 D NotebookLM 예외 동의)".

따라서 이 bridge는 다음 4 조건 모두 만족 시에만 발동:

| 조건 | 검증 |
|---|---|
| 저자 명시 호출 | argparse 명령 라인 호출 *외* 호출 영구 차단 |
| RiskAssessor 통과 | M16-A `assess(prompt, action)` 비가역 키워드 0건 |
| TraumaWitnessDetector 통과 | M15 trauma 6 카테고리 검출 시 저자 동의 명시 |
| search_paths tier_2 등재 | book-config.yaml `search_paths.tier_2_explicit`에만 |

### 2. 결정론 chain (LLM 추론 영구 금지)

```python
from risk_assessor import RiskAssessor
from trauma_witness_detector import TraumaWitnessDetector
from id_generator import IdGenerator

def import_notebook(notebook_id: str, content: str) -> dict:
    # Step 1: M16-A 비가역 키워드 결정론 차단
    ra = RiskAssessor()
    risk = ra.assess(prompt=notebook_id, action=content)
    if not risk["auto_yes_eligible"]:
        return {"action": "blocked", "reason": "irreversible_keyword", "details": risk}

    # Step 2: M15 trauma 6 카테고리 결정론 검출
    td = TraumaWitnessDetector()
    trauma = td.assess(content)
    if trauma["trauma_detected"]:
        # 저자 동의 명시 후에만 import
        return {
            "action": "require_explicit_consent",
            "trauma_categories": trauma["categories"],
            "protocol_required": trauma["actions_required"],
        }

    # Step 3: tier_2 search_paths 결정론 등재
    config = load_book_config()
    notebook_dir = Path("...") / notebook_id
    if str(notebook_dir) not in config["search_paths"]["tier_2_explicit"]:
        config["search_paths"]["tier_2_explicit"].append(str(notebook_dir))

    # Step 4: import 결정론 trace 기록 (단계 마스터 자동 호출 검출용)
    return {
        "action": "imported",
        "notebook_id": notebook_id,
        "added_to_tier": "tier_2_explicit",
        "invoked_by": "user_explicit_only",  # 자동 호출 영구 차단
    }
```

### 3. 자동 호출 영구 차단 protocol

다른 단계 마스터 (① absorb ~ ⑪ cross-chapter-relink)는 이 bridge를 *간접적으로도 호출 영구 금지*. 저자 명시 명령 라인 호출 외에는 어떠한 trigger도 인정 안 함.

```python
def assert_explicit_invocation(invoker: str) -> None:
    """단계 마스터·sub-skill 호출 시 즉시 raise."""
    ALLOWED_INVOKERS = {"cli_explicit", "저자_명시"}
    if invoker not in ALLOWED_INVOKERS:
        raise PermissionError(
            f"bookwriting-notebooklm-bridge는 저자 명시 호출만 허용. "
            f"호출 주체: {invoker}는 영구 차단."
        )
```

### 4. import 후 자산 사용 규칙

- import된 NotebookLM 자산은 search_paths tier_2_explicit로 등재됨
- ③ systemlink 마스터의 M6 RelevanceScorer가 BM25 결정론 매칭 시 *tier_1 자산과 동등하게 검색*
- 단, ④ evidence-collect의 권위 등급은 *최소 D (사상가) 등급 default* — 저자 명시 grade 갱신 후 상향 가능

### 5. trauma 검출 시 처리

```python
if trauma["trauma_detected"]:
    print(f"⚠ trauma 검출: {trauma['categories']}")
    print(f"  필수 조치: {trauma['actions_required']}")
    print(f"  citation_gate_priority: {trauma['citation_gate_priority']}")
    return {"action": "require_explicit_consent"}
```

저자 동의 명시 후에만 import 진행. 자동 import 영구 차단.

## 저자 진북 정합

| 진북 | 검증 |
|---|---|
| #1 할루시네이션 0 | ✅ tier_2 등재 후 M6 BM25 결정론 매칭 — LLM 추론 0 |
| #3 출처 명시 | ✅ notebook_id metadata 명시 |
| #4 저자 작가성 | ✅ 저자 명시 호출만 — 자동 호출 영구 금지 |
| #5 보안·법적 위험 | ✅ M16-A RiskAssessor 비가역 키워드 차단 |
| #6 정신건강·취약 독자 | ✅ M15 TraumaWitnessDetector 6 카테고리 결정론 검출 |
| #7 결정론 환원 | ✅ Risk + Trauma + ID 발급 모두 pure Python 결정론 |

## CLI 통합 (Phase 3-B 12주차)

```bash
# 저자 명시 호출 (유일한 경로)
bookwriting notebooklm import nb-agi-foundations-2026

# 등재 자산 조회
bookwriting notebooklm list
```

*다른 단계 마스터에서 자동 발동 영구 금지 — OrchestratorTracer가 invocation_type="auto"로 검출 시 PermissionError raise.*

## 출처

- 저자 grill-me 합의: 옵션 A+ 자기완결 + 옵션 D NotebookLM 예외 동의
- 결정론 모듈: `lib/risk_assessor.py` + `lib/trauma_witness_detector.py` + `lib/id_generator.py`
- search_paths 정합: `book-config.yaml::search_paths.tier_2_explicit`
- Orchestrator trace: `lib/orchestrator_tracer.py` (자동 호출 검출 강제)
