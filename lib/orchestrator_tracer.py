"""M18: orchestrator_tracer.py — 저자 메모리 7번째 절대 protocol 결정론 구현
SPEC: feedback_master_orchestration_trace.md (마스터-Sub-skill Orchestration Trace 강제)

저자 절대 protocol: 마스터가 각 sub-skill 호출 시점·순서·산출물을 명시적 trace로 표시.
Inline 시뮬레이션 단독 영구 금지 — 모든 sub-skill 호출은 결정론적으로 기록되어야 한다.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class TraceStep:
    """sub-skill 호출 단일 trace 항목."""
    sequence: int
    timestamp: str
    skill_name: str
    invocation_type: str  # "auto" | "manual" | "blocked" | "deferred"
    inputs_summary: dict[str, Any] = field(default_factory=dict)
    outputs_summary: dict[str, Any] = field(default_factory=dict)
    deterministic_modules_used: list[str] = field(default_factory=list)
    lifecycle_before: str | None = None
    lifecycle_after: str | None = None
    status: str = "pending"  # "completed" | "failed" | "blocked" | "deferred"
    escalation: str | None = None  # 저자 escalate 메시지

    def to_dict(self) -> dict:
        return {
            "sequence": self.sequence,
            "timestamp": self.timestamp,
            "skill_name": self.skill_name,
            "invocation_type": self.invocation_type,
            "inputs_summary": self.inputs_summary,
            "outputs_summary": self.outputs_summary,
            "deterministic_modules_used": self.deterministic_modules_used,
            "lifecycle_before": self.lifecycle_before,
            "lifecycle_after": self.lifecycle_after,
            "status": self.status,
            "escalation": self.escalation,
        }


class OrchestratorTracer:
    """마스터 호출 trace 결정론 기록. Inline 시뮬레이션 영구 금지."""

    VALID_SKILLS = {
        "bookwriting-absorb-master",            # ①
        "bookwriting-fact-anchor-master",       # ②
        "bookwriting-systemlink-master",        # ③
        "bookwriting-evidence-collect-master",  # ④
        "bookwriting-evidence-link-master",     # ⑤
        "bookwriting-insight-synthesis-master", # ⑥
        "bookwriting-content-expand-master",    # ⑦
        "bookwriting-narrative-craft-master",   # ⑧
        "bookwriting-structure-review-master",  # ⑨
        "bookwriting-line-edit-master",         # ⑩
        "bookwriting-cross-chapter-relink-master",  # ⑪
        # cross-cutting gate
        "voice-gate",
        "citation-gate",
    }

    VALID_INVOCATION_TYPES = {"auto", "manual", "blocked", "deferred"}
    VALID_STATUSES = {"completed", "failed", "blocked", "deferred", "pending"}

    def __init__(self):
        self.steps: list[TraceStep] = []
        self._next_seq = 1

    def add_step(
        self,
        skill_name: str,
        invocation_type: str,
        inputs_summary: dict | None = None,
        outputs_summary: dict | None = None,
        deterministic_modules_used: list[str] | None = None,
        lifecycle_before: str | None = None,
        lifecycle_after: str | None = None,
        status: str = "completed",
        escalation: str | None = None,
    ) -> TraceStep:
        """trace 항목 추가 + 검증.

        호출 즉시 sequence + timestamp 결정론 발급.
        """
        if skill_name not in self.VALID_SKILLS:
            raise ValueError(
                f"Unknown skill: {skill_name}. Allowed: {sorted(self.VALID_SKILLS)}"
            )
        if invocation_type not in self.VALID_INVOCATION_TYPES:
            raise ValueError(
                f"Invalid invocation_type: {invocation_type}. "
                f"Allowed: {sorted(self.VALID_INVOCATION_TYPES)}"
            )
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")

        step = TraceStep(
            sequence=self._next_seq,
            timestamp=datetime.now(timezone.utc).isoformat(),
            skill_name=skill_name,
            invocation_type=invocation_type,
            inputs_summary=inputs_summary or {},
            outputs_summary=outputs_summary or {},
            deterministic_modules_used=deterministic_modules_used or [],
            lifecycle_before=lifecycle_before,
            lifecycle_after=lifecycle_after,
            status=status,
            escalation=escalation,
        )
        self.steps.append(step)
        self._next_seq += 1
        return step

    def to_list(self) -> list[dict]:
        """trace 전체 dict 직렬화."""
        return [s.to_dict() for s in self.steps]

    def count(self) -> int:
        return len(self.steps)

    def has_inline_simulation_only(self) -> bool:
        """Inline 시뮬레이션 단독 패턴 검출 — 저자 7번째 protocol 위반.

        모든 step의 deterministic_modules_used가 비어있으면 inline 단독 의심.
        """
        if not self.steps:
            return False
        return all(not s.deterministic_modules_used for s in self.steps)

    def assert_protocol_compliant(self) -> dict:
        """7번째 protocol 정합성 결정론 검증."""
        violations: list[str] = []
        if self.has_inline_simulation_only():
            violations.append(
                "inline_simulation_only — 모든 step에 결정론 모듈이 명시되지 않음 (저자 7번째 protocol 위반)"
            )
        # 시퀀스 연속성 검증
        seqs = [s.sequence for s in self.steps]
        if seqs and seqs != list(range(1, len(seqs) + 1)):
            violations.append(f"sequence_discontinuous: {seqs}")
        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "step_count": len(self.steps),
        }

    def get_escalations(self) -> list[dict]:
        """저자 escalate 메시지 모음."""
        return [
            {"sequence": s.sequence, "skill": s.skill_name, "message": s.escalation}
            for s in self.steps
            if s.escalation
        ]
