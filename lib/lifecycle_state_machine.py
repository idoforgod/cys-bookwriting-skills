"""M11: lifecycle_state_machine.py — 시드 lifecycle 6 외골격 결정론 전환
SPEC: expert_pool/deterministic-modules.md §M11
저자 진북 #7 (결정론 환원) — LLM이 임의로 상태 변경 영구 금지.

SEED → LINKED → EXPANDED → EVIDENCED → INSIGHTED → POLISHED (단방향)
잘못된 전환 시 ValueError raise.
"""
from __future__ import annotations

from enum import Enum


class LifecycleState(str, Enum):
    SEED = "SEED"
    LINKED = "LINKED"
    EXPANDED = "EXPANDED"
    EVIDENCED = "EVIDENCED"
    INSIGHTED = "INSIGHTED"
    POLISHED = "POLISHED"


class LifecycleStateMachine:
    """시드 lifecycle 6 외골격 단방향 전환 강제."""

    VALID_TRANSITIONS: dict[LifecycleState, list[LifecycleState]] = {
        LifecycleState.SEED: [LifecycleState.LINKED],
        LifecycleState.LINKED: [LifecycleState.EXPANDED],
        LifecycleState.EXPANDED: [LifecycleState.EVIDENCED],
        LifecycleState.EVIDENCED: [LifecycleState.INSIGHTED],
        LifecycleState.INSIGHTED: [LifecycleState.POLISHED],
        LifecycleState.POLISHED: [],
    }

    # 단계 마스터 → lifecycle 전환 매핑
    STAGE_TO_TRANSITION = {
        "absorb": (LifecycleState.SEED, LifecycleState.SEED),  # 시드 등록·상태 유지
        "fact_anchor": (LifecycleState.SEED, LifecycleState.LINKED),
        "systemlink": (LifecycleState.LINKED, LifecycleState.LINKED),  # 자산 연결만
        "evidence_collect": (LifecycleState.LINKED, LifecycleState.EXPANDED),
        "evidence_link": (LifecycleState.EXPANDED, LifecycleState.EVIDENCED),
        "insight_synthesis": (LifecycleState.EVIDENCED, LifecycleState.INSIGHTED),
        "content_expand": (LifecycleState.INSIGHTED, LifecycleState.INSIGHTED),  # 본문 확장
        "narrative_craft": (LifecycleState.INSIGHTED, LifecycleState.INSIGHTED),
        "structure_review": (LifecycleState.INSIGHTED, LifecycleState.INSIGHTED),
        "line_edit": (LifecycleState.INSIGHTED, LifecycleState.POLISHED),
        "cross_chapter_relink": (LifecycleState.POLISHED, LifecycleState.POLISHED),
    }

    def can_transition(self, current: LifecycleState, target: LifecycleState) -> bool:
        if current == target:
            return True  # 같은 상태 유지 허용
        return target in self.VALID_TRANSITIONS[current]

    def transition(self, current: LifecycleState, target: LifecycleState) -> LifecycleState:
        if not self.can_transition(current, target):
            raise ValueError(f"Invalid transition: {current.value} → {target.value}")
        return target

    def next_state(self, current: LifecycleState) -> LifecycleState | None:
        """다음 정상 진행 상태 — POLISHED는 None."""
        valid = self.VALID_TRANSITIONS[current]
        return valid[0] if valid else None

    def is_terminal(self, state: LifecycleState) -> bool:
        return state == LifecycleState.POLISHED
