---
name: bookwriting-fact-anchor-registry-syncer
description: 부모 bookwriting-fact-anchor-master의 INTERNAL sub. forecast-registry.yaml의 quantitative_anchor·P-NNN 결정론 갱신 + 신규 P-NNN 등록 + 기존 P-NNN evidence 추가 + 저자 v1 R1 규칙 정합 검증. M12 forecast_registry_syncer 호출.
when_to_use: bookwriting-fact-anchor-master Step 6 (Registry Syncer 페르소나)에서 자동 호출. Conflict Detector 통과 후 (충돌 해결 후). 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-fact-anchor-registry-syncer

## TLDR

부모 bookwriting-fact-anchor-master의 forecast-registry sync sub. M12 forecast_registry_syncer로 신규 P-NNN 등록·기존 P-NNN evidence 추가·quantitative_anchor 정합 검증·저자 v1 R1 규칙 준수 확인을 결정론 수행한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Conflict Detector 통과 (충돌 해결 후) → Step 6 자동
- `/bookwriting-fact-anchor sync-registry` 모드는 forecast-registry sync만 단독 실행

## Detailed Methodology

### 1. 결정론 chain — M12 forecast_registry_syncer 호출

```python
from forecast_registry_syncer import ForecastRegistrySyncer   # M12
from pathlib import Path
from dataclasses import dataclass

@dataclass
class SyncResult:
    new_predictions: list[str]      # 신규 P-NNN
    updated_predictions: list[str]  # evidence 추가된 P-NNN
    r1_violations: list[str]        # R1 quantitative_anchor 위반 P-NNN
    quantitative_anchor_updates: int

def sync_registry(fact_pool: list, forecast_registry_path: Path) -> SyncResult:
    """fact 풀 → forecast-registry 갱신 + R1 정합."""
    syncer = ForecastRegistrySyncer(forecast_registry_path)

    # Step 1: 신규 fact 식별 (기존 P-NNN에 없는 것)
    new_facts = []
    matched_facts = []
    for f in fact_pool:
        existing_pnnn = syncer.match_to_existing(f.text, f.fact_type)
        if existing_pnnn:
            matched_facts.append((f, existing_pnnn))
        else:
            new_facts.append(f)

    # Step 2: 신규 P-NNN 등록 (M12 register_new)
    new_pnnns = []
    for f in new_facts:
        pnnn = syncer.register_new(
            text=f.text,
            quantitative_anchor=f.text,
            source_file=f.source_file,
            fact_type=f.fact_type,
        )
        new_pnnns.append(pnnn)

    # Step 3: 기존 P-NNN evidence 추가
    updated_pnnns = []
    for f, pnnn in matched_facts:
        syncer.add_evidence(pnnn, source_file=f.source_file, context=f.context)
        updated_pnnns.append(pnnn)

    # Step 4: quantitative_anchor 필드 정합 검증 (M12)
    qa_update_count = syncer.verify_quantitative_anchor_fields()

    # Step 5: 저자 v1 R1 규칙 준수 (모든 P-NNN에 quantitative_anchor 필수)
    r1_violations = syncer.verify_r1_quantitative_anchor()

    return SyncResult(
        new_predictions=new_pnnns,
        updated_predictions=updated_pnnns,
        r1_violations=r1_violations,
        quantitative_anchor_updates=qa_update_count,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-fact-anchor-subs.md SUB 4)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 신규 fact 중 *기존 P-NNN에 없는 것* 식별 | `syncer.match_to_existing()` |
| Step 2: forecast-registry에 신규 P-NNN 등록 | `syncer.register_new()` |
| Step 3: 기존 P-NNN에 *새 evidence 출처* 추가 | `syncer.add_evidence()` |
| Step 4: quantitative_anchor 필드 정합 검증 | `syncer.verify_quantitative_anchor_fields()` |
| Step 5: 저자 v1 R1 규칙 준수 확인 | `syncer.verify_r1_quantitative_anchor()` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | fact_pool (Conflict Detector 통과 후) + forecast-registry.yaml path |
| Output | SyncResult (new·updated·r1_violations·qa_updates) |
| 후속 sub | `bookwriting-fact-anchor-seed-linker` |
| Dependencies | Conflict Detector 통과 (충돌 해결 후) |
| 결정론 모듈 | M12 ForecastRegistrySyncer |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M12 결정론 + yaml.safe_load — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 5 Step 1:1 환원 + R1 규칙 명시 |
| #3 출처 명시 | evidence add — source_file·context 필수 |
| #7 결정론 환원 | M12 호출 100% 결정론 |

### 5. Verification (명세 §7)

- forecast-registry 정합 100% (yaml.safe_load 회귀)
- R1 규칙 준수 (모든 P-NNN에 quantitative_anchor 필수)
- 중복 P-NNN 0건 (match_to_existing 우선)
- 신규 등록 시 저자 v15 130 predictions 변경 *영구 금지* (PHASE3B_HANDOFF §8 영속 자산 보호)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-fact-anchor-subs.md` §SUB 4
부모 마스터 SPEC: `specs/bookwriting-fact-anchor-master.md` §7 Step 6 + §13 페르소나 4 + 부록 결정론 (M12)
저자 v1 R1: `$BOOK_ROOT/workflows/book-planning.md` R1 quantitative_anchor 원문
결정론 모듈: `lib/forecast_registry_syncer.py` (M12)
영속 자산 보호: PHASE3B_HANDOFF §8 (sub-skill 환원 작업 중 registry 변경 영구 금지)
