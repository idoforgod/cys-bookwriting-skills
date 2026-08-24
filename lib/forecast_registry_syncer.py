"""M12: forecast_registry_syncer.py — forecast-registry.yaml R/W + R1-R5 결정론 검증
SPEC: expert_pool/deterministic-modules.md §M12
저자 v1 chapter-pipeline.md R1-R5 규칙 직접 구현.

R1 quantitative_anchor — 모든 P-NNN에 정량 앵커 필수
R2 chapter_role — 1층_콜드오픈|2층_분석|3층_함의
R3 system_loops — L1-L7 명시
R4 권위 다층 — 최소 2층
R5 verification_signal·falsifies_if — 5년·10년 검증
"""
from __future__ import annotations

from pathlib import Path

import yaml


class ForecastRegistrySyncer:
    """forecast-registry R1-R5 결정론 검증·sync. yaml.safe_load 강제."""

    VALID_CHAPTER_ROLES = {"1층_콜드오픈", "2층_분석", "3층_함의"}
    VALID_SYSTEM_LOOPS = {"L1", "L2", "L3", "L4", "L5", "L6", "L7"}

    def __init__(self, registry_path: Path):
        self.registry_path = Path(registry_path)
        if self.registry_path.exists():
            with open(self.registry_path, encoding="utf-8") as f:
                self.registry = yaml.safe_load(f.read()) or {}
        else:
            self.registry = {"predictions": []}
        if "predictions" not in self.registry:
            self.registry["predictions"] = []

    def verify_r1_quantitative_anchor(self) -> list[str]:
        """R1 위반 — quantitative_anchor 누락 P-NNN 목록."""
        violations = []
        for p in self.registry["predictions"]:
            anchors = p.get("quantitative_anchor", [])
            if not anchors:
                violations.append(p.get("id", "UNKNOWN"))
        return violations

    def verify_r2_chapter_role(self) -> list[str]:
        violations = []
        for p in self.registry["predictions"]:
            role = p.get("chapter_role")
            if role and role not in self.VALID_CHAPTER_ROLES:
                violations.append(p.get("id"))
        return violations

    def verify_r3_system_loops(self) -> list[str]:
        """R3 — system_loops 명시 (L1-L7 enum)."""
        violations = []
        for p in self.registry["predictions"]:
            loops = p.get("system_loops") or []
            for loop in loops:
                loop_id = loop.get("loop_id") if isinstance(loop, dict) else loop
                if loop_id not in self.VALID_SYSTEM_LOOPS:
                    violations.append(p.get("id"))
                    break
        return violations

    def verify_r4_multi_layer(self) -> list[str]:
        """R4 — authority_layers의 unique grade >= 2."""
        violations = []
        for p in self.registry["predictions"]:
            layers = p.get("authority_layers") or []
            grades = {layer.get("grade") for layer in layers if isinstance(layer, dict)}
            grades.discard(None)
            grades.discard("out")
            if len(grades) < 2:
                violations.append(p.get("id"))
        return violations

    def verify_r5_verification_signal(self) -> list[str]:
        violations = []
        for p in self.registry["predictions"]:
            if not p.get("verification_signal"):
                violations.append(p.get("id"))
        return violations

    def verify_all(self) -> dict[str, list[str]]:
        return {
            "R1_quantitative_anchor": self.verify_r1_quantitative_anchor(),
            "R2_chapter_role": self.verify_r2_chapter_role(),
            "R3_system_loops": self.verify_r3_system_loops(),
            "R4_multi_layer": self.verify_r4_multi_layer(),
            "R5_verification_signal": self.verify_r5_verification_signal(),
        }

    def count_predictions(self) -> int:
        return len(self.registry["predictions"])

    def add_prediction(self, prediction: dict) -> None:
        """신규 P-NNN 등록 (atomic write는 호출자 책임)."""
        self.registry["predictions"].append(prediction)
