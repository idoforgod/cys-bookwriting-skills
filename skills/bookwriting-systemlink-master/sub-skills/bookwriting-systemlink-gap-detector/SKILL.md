---
name: bookwriting-systemlink-gap-detector
description: 부모 bookwriting-systemlink-master의 INTERNAL sub ⭐. 시스템 그래프 분석 + 빈 고리 3 패턴 (변수-피드백 누락·시나리오 분기 정치 변수 누락·시스템 루프 evidence 누락) 결정론 검출 + 저자 묶음 4 옵션 (신 시드 추가·외부 foresight manual·재검색·defer) escalate + cycle-registry pending_decisions 등록.
when_to_use: bookwriting-systemlink-master Step 6 (Gap Detector 페르소나)에서 자동 호출. System Loop Mapper 통과 후. `/bookwriting-systemlink gap-detect` 모드도 본 sub 단독. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-systemlink-gap-detector

## TLDR

부모 bookwriting-systemlink-master의 ⭐ 빈 고리 검출 핵심 sub. 저자 진짜 워크플로우 4단계 *빈 고리 채우기*의 글쓰기 차원. System Loop Mapper 산출 그래프에서 3 빈 고리 패턴 (변수-피드백 누락·시나리오 정치 변수 누락·루프-evidence 누락)을 결정론 검출하고 저자 묶음 4 옵션을 escalate한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- System Loop Mapper 통과 후 → Step 6 자동
- `/bookwriting-systemlink gap-detect <target>` 모드는 본 sub 단독

## Detailed Methodology

### 1. 결정론 chain — 3 빈 고리 패턴 검출

```python
from enum import Enum
from dataclasses import dataclass, field

class GapType(str, Enum):
    VARIABLE_FEEDBACK_MISSING = "variable_feedback_missing"
    SCENARIO_POLITICS_MISSING = "scenario_politics_missing"
    LOOP_EVIDENCE_MISSING = "loop_evidence_missing"

class GapOption(str, Enum):
    NEW_SEED = "new_seed"
    EXTERNAL_FORESIGHT_MANUAL = "external_foresight_manual"
    RE_SEARCH = "re_search"
    DEFER = "defer"

@dataclass
class SystemGap:
    gap_id: str
    gap_type: GapType
    loop_id: str            # L1-L7
    description: str
    affected_seeds: list[str] = field(default_factory=list)
    bundle_options: list[GapOption] = field(default_factory=lambda: list(GapOption))

def detect_gaps(loop_mappings: list, seeds: list[dict], scenarios: list[dict] | None = None) -> list[SystemGap]:
    """시스템 그래프 빈 고리 결정론 검출."""
    gaps = []
    gap_counter = 0

    # 루프별 매핑 그룹화
    by_loop: dict[str, list] = {}
    for m in loop_mappings:
        by_loop.setdefault(m.loop_id, []).append(m)

    # Step 1: 시스템 루프 그래프 분석
    # Step 2: 빈 고리 패턴 검출

    # 패턴 A — 변수 호명됐는데 피드백 누락
    for loop_id, mappings in by_loop.items():
        variables_named = {m.variable_id for m in mappings if m.variable_id}
        feedbacks_named = {m.feedback_path for m in mappings if m.feedback_path}

        # 변수 N개 호명·피드백 0 → 빈 고리
        if len(variables_named) >= 2 and len(feedbacks_named) == 0:
            gap_counter += 1
            gaps.append(SystemGap(
                gap_id=f"GAP-{gap_counter:03d}",
                gap_type=GapType.VARIABLE_FEEDBACK_MISSING,
                loop_id=loop_id,
                description=f"{loop_id}: 변수 {len(variables_named)}개 호명, 피드백 화살표 누락",
                affected_seeds=[m.seed_id for m in mappings],
            ))

    # 패턴 B — 시나리오 분기 정의됐는데 정치 변수 미명시
    if scenarios:
        for scenario in scenarios:
            has_politics_var = any(
                "정치" in str(v) or "political" in str(v).lower()
                for v in scenario.get("variables", [])
            )
            if scenario.get("branches") and not has_politics_var:
                gap_counter += 1
                gaps.append(SystemGap(
                    gap_id=f"GAP-{gap_counter:03d}",
                    gap_type=GapType.SCENARIO_POLITICS_MISSING,
                    loop_id=scenario.get("loop_id", ""),
                    description=f"시나리오 '{scenario.get('id')}' 분기 정의됐으나 정치 변수 미명시",
                ))

    # 패턴 C — 시스템 루프 정의됐는데 evidence 없음
    for loop_id, mappings in by_loop.items():
        has_evidence = any(
            seed.get("connections", {}).get("linked_assets", [])
            for seed in seeds
            if seed["id"] in [m.seed_id for m in mappings]
        )
        if not has_evidence:
            gap_counter += 1
            gaps.append(SystemGap(
                gap_id=f"GAP-{gap_counter:03d}",
                gap_type=GapType.LOOP_EVIDENCE_MISSING,
                loop_id=loop_id,
                description=f"{loop_id}: 루프 정의됐으나 linked_assets 0건",
                affected_seeds=[m.seed_id for m in mappings],
            ))

    # Step 3: 저자 묶음 (4 옵션 자동 부착)
    # — 부모 마스터가 저자 묶음 화면 출력

    # Step 4: cycle-registry pending_decisions 등록 — 부모 마스터가 yaml write
    return gaps
```

### 2. 명세 §출처 (SPEC: bookwriting-systemlink-subs.md SUB 6) ⭐

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 시스템 루프 그래프 분석 | `by_loop` 그룹화 |
| Step 2 패턴 A: 변수 호명·피드백 누락 | `len(variables_named) >= 2 and len(feedbacks_named) == 0` |
| Step 2 패턴 B: 시나리오 분기·정치 변수 미명시 | `scenario.get("branches") and not has_politics_var` |
| Step 2 패턴 C: 시스템 루프·evidence 없음 | `not has_evidence` |
| Step 3: 저자 묶음 4 옵션 (신 시드·외부 manual·재검색·defer) | `GapOption` enum 4종 |
| Step 4: cycle-registry pending_decisions 등록 | 부모 마스터 yaml write 위임 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | loop_mappings (System Loop Mapper 산출) + seeds + scenarios (옵션) |
| Output | List[SystemGap] — gap_id·gap_type·loop_id·description·affected_seeds·bundle_options |
| 후속 단계 | 저자 묶음 응답 → 새 시드/외부 manual/재검색/defer |
| Dependencies | System Loop Mapper 통과 |
| 결정론 모듈 | 자체 그래프 알고리즘 (set 연산·dict 그룹화) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | set·dict 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 4 Step + 3 패턴 + 4 옵션 1:1 환원 |
| #4 저자 작가성 | 저자 묶음 *강제* — 자동 결정 영구 금지 (저자 진짜 워크플로우 4단계 빈 고리 채우기) |
| #5 법적 위험 | 빈 고리 3건 초과 시 저자 알림 + 일괄 처리 (부모 §12 가드) |
| #7 결정론 환원 | 그래프 알고리즘 100% 결정론 |

### 5. Verification (명세 §7)

- 빈 고리 검출 정확도 75%+ (false positive 허용 — 저자 확인)
- 저자 묶음 정합 (4 옵션 자동 부착)
- 빈 고리 3건 초과 시 저자 일괄 묶음 (부모 §12 + §16)
- cycle-registry pending_decisions 등록 (영속 자산 보호 — 부모 마스터 write 위임)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-systemlink-subs.md` §SUB 6 ⭐
부모 마스터 SPEC: `specs/bookwriting-systemlink-master.md` §7 Step 6 ⭐ + §13 페르소나 5 ⭐ + §12 가드 (3건 초과 일괄) + §17 검증 4
저자 진짜 워크플로우: 4단계 빈 고리 채우기 *글쓰기 차원* (부모 §2 책임 4)
영속 자산 보호: PHASE3B_HANDOFF §8 (cycle-registry write 부모 위임)
