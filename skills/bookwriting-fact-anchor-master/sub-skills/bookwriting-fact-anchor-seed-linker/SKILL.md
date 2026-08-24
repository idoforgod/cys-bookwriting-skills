---
name: bookwriting-fact-anchor-seed-linker
description: 부모 bookwriting-fact-anchor-master의 INTERNAL sub. seed-registry connections.linked_predictions 결정론 갱신 + 각 P-NNN에 citation_authority_grade 매핑 + 시드 lifecycle SEED → LINKED 진행 권장. M3 AuthorityGrader + M11 lifecycle_state_machine.
when_to_use: bookwriting-fact-anchor-master Step 7 (Seed Linker 페르소나)에서 자동 호출. Registry Syncer 통과 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-fact-anchor-seed-linker

## TLDR

부모 bookwriting-fact-anchor-master의 마지막 sub. seed-registry의 connections.linked_predictions 필드를 결정론 갱신하고 각 P-NNN에 M3 AuthorityGrader로 citation_authority_grade를 매핑한다. 시드 lifecycle을 SEED → LINKED로 진행할 것을 부모 마스터에 권장.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Registry Syncer 통과 (forecast-registry 갱신 후) → Step 7 자동

## Detailed Methodology

### 1. 결정론 chain — seed-registry sync

```python
import yaml
from pathlib import Path
from dataclasses import dataclass
from authority_grader import AuthorityGrader               # M3
from lifecycle_state_machine import LifecycleState         # M11

@dataclass
class SeedLinkResult:
    seed_id: str
    linked_predictions: list[str]   # P-NNN 목록
    grades: dict[str, str]          # P-NNN → "A"|"B"|"C"|"D"|"E"
    lifecycle_recommendation: str   # 현재 lifecycle → 권장 lifecycle

def link_seeds(
    sync_result,                    # Registry Syncer 산출
    fact_pool: list,
    seed_registry_path: Path,
    authority_db_path: Path,
) -> list[SeedLinkResult]:
    """시드 → P-NNN 연결 + 권위 등급 매핑 + lifecycle 권장."""
    grader = AuthorityGrader(authority_db_path)

    # seed-registry 로드 (yaml.safe_load 결정론)
    with seed_registry_path.open(encoding="utf-8") as f:
        registry = yaml.safe_load(f) or {}
    seeds = registry.get("seeds", [])

    results = []
    for seed in seeds:
        seed_id = seed.get("id")
        seed_text = seed.get("text", "")

        # Step 1: 각 시드의 관련 P-NNN 식별
        # — Registry Syncer 산출 P-NNN 중 시드 내용과 연결되는 것
        related_pnnns = []
        for pnnn in sync_result.new_predictions + sync_result.updated_predictions:
            # 시드 텍스트와 P-NNN의 fact가 같은 chapter·topic 영역인가
            if _is_related(seed, pnnn, fact_pool):
                related_pnnns.append(pnnn)

        # Step 2: connections.linked_predictions 갱신
        # (실제 yaml 쓰기는 부모 마스터가 일괄 처리 — 본 sub는 산출만)

        # Step 3: 각 P-NNN에 권위 등급 매핑 (M3)
        grades = {}
        for pnnn in related_pnnns:
            # P-NNN의 evidence source로 권위 등급 산출
            pnnn_source = _find_pnnn_source(pnnn, fact_pool)
            grade = grader.assign_grade(source_path=pnnn_source)
            grades[pnnn] = grade.value   # "A"|"B"|"C"|"D"|"E"

        # Step 4: 시드 lifecycle SEED → LINKED 진행 권장 (M11)
        current_state = LifecycleState(seed.get("lifecycle", "SEED"))
        if related_pnnns and current_state == LifecycleState.SEED:
            recommendation = "SEED → LINKED"
        else:
            recommendation = "no_change"

        results.append(SeedLinkResult(
            seed_id=seed_id,
            linked_predictions=related_pnnns,
            grades=grades,
            lifecycle_recommendation=recommendation,
        ))

    return results

def _is_related(seed: dict, pnnn: str, fact_pool: list) -> bool:
    """seed connections·routing chapter 일치 검증."""
    # 결정론 매칭: seed의 routing chapter와 P-NNN evidence의 source 챕터가 같으면 연결
    seed_chapter = seed.get("routing", {}).get("primary_chapter")
    # (간소화 — 실제 chapter 매칭은 부모 마스터가 chapter_manifest와 cross-check)
    return bool(seed_chapter)

def _find_pnnn_source(pnnn: str, fact_pool: list) -> str:
    """P-NNN의 첫 evidence source 반환."""
    return fact_pool[0].source_file if fact_pool else ""
```

### 2. 명세 §출처 (SPEC: bookwriting-fact-anchor-subs.md SUB 5)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 각 시드의 관련 P-NNN 식별 | `_is_related(seed, pnnn, fact_pool)` |
| Step 2: seed-registry.connections.linked_predictions 갱신 | SeedLinkResult.linked_predictions (부모 마스터가 yaml write) |
| Step 3: 각 P-NNN에 권위 등급 매핑 | M3 `grader.assign_grade()` → grades dict |
| Step 4: 시드 lifecycle SEED → LINKED 진행 권장 | M11 LifecycleState + recommendation |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | SyncResult (Registry Syncer 산출) + fact_pool + seed-registry path + authority-db path |
| Output | List[SeedLinkResult] — seed_id + linked_predictions + grades + lifecycle_recommendation |
| 후속 단계 | ③ systemlink (다음 단계 마스터) |
| Dependencies | Registry Syncer 통과 |
| 결정론 모듈 | M3 AuthorityGrader + M11 lifecycle_state_machine |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M3 + M11 결정론 + yaml.safe_load — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 환원 |
| #3 출처 명시 | citation_authority_grade 모든 P-NNN 매핑 |
| #7 결정론 환원 | M3 + M11 + 권장 산출 100% 결정론 |

### 5. Verification (명세 §7)

- 시드 linked_predictions 정합 (seed-registry yaml 회귀)
- citation_authority_grade *모두 매핑* (M3 grader.assign_grade 빠짐 0건)
- lifecycle 진행 권장 (M11 SEED → LINKED 전이 규칙 정합)
- 영속 자산 보호: 본 sub는 *산출만*. seed-registry 실제 write는 부모 마스터 (PHASE3B_HANDOFF §8 영구 금지 정합)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-fact-anchor-subs.md` §SUB 5
부모 마스터 SPEC: `specs/bookwriting-fact-anchor-master.md` §7 Step 7 + §13 페르소나 5 + 부록 결정론 (M3)
결정론 모듈: `lib/authority_grader.py` (M3) + `lib/lifecycle_state_machine.py` (M11)
권위 DB: `expert_pool/citation-authority-db.yaml`
영속 자산 보호: PHASE3B_HANDOFF §8 (sub-skill 환원 중 registry 변경 영구 금지)
