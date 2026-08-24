"""M5: layer_ratio_measurer.py — 1·2·3층 분량 비율 결정론 측정
SPEC: expert_pool/deterministic-modules.md §M5
저자 v1 layer_ratios 강제 (1층 10-15%·2층 60-70%·3층 15-25%).
저자 진북 #7 (결정론 환원).
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class LayerRatioReport:
    narrative_chars: int
    analysis_chars: int
    implications_chars: int
    total_chars: int
    narrative_pct: float
    analysis_pct: float
    implications_pct: float
    violations: list[tuple[str, float]]
    resize_needed: bool


class LayerRatioMeasurer:
    def __init__(self, layer_ratios: dict):
        self.ranges = {
            "narrative": tuple(layer_ratios["narrative"]["range"]),
            "analysis": tuple(layer_ratios["analysis"]["range"]),
            "implications": tuple(layer_ratios["implications"]["range"]),
        }

    def measure(
        self,
        narrative_path: Path,
        analysis_path: Path,
        implications_path: Path,
    ) -> LayerRatioReport:
        n = self._read_chars(narrative_path)
        a = self._read_chars(analysis_path)
        i = self._read_chars(implications_path)
        total = n + a + i
        if total == 0:
            return LayerRatioReport(0, 0, 0, 0, 0.0, 0.0, 0.0, [("empty", 0.0)], False)

        n_pct = n / total * 100
        a_pct = a / total * 100
        i_pct = i / total * 100

        violations: list[tuple[str, float]] = []
        if not (self.ranges["narrative"][0] <= n_pct <= self.ranges["narrative"][1]):
            violations.append(("narrative", round(n_pct, 1)))
        if not (self.ranges["analysis"][0] <= a_pct <= self.ranges["analysis"][1]):
            violations.append(("analysis", round(a_pct, 1)))
        if not (self.ranges["implications"][0] <= i_pct <= self.ranges["implications"][1]):
            violations.append(("implications", round(i_pct, 1)))

        # 5% 범위 내 위반은 resize 가능
        resize_needed = all(self._within_resize_range(v[0], v[1]) for v in violations)

        return LayerRatioReport(
            narrative_chars=n,
            analysis_chars=a,
            implications_chars=i,
            total_chars=total,
            narrative_pct=round(n_pct, 1),
            analysis_pct=round(a_pct, 1),
            implications_pct=round(i_pct, 1),
            violations=violations,
            resize_needed=resize_needed,
        )

    def _read_chars(self, path: Path) -> int:
        path = Path(path)
        if not path.exists():
            return 0
        return len(path.read_text(encoding="utf-8"))

    def _within_resize_range(self, layer: str, actual_pct: float) -> bool:
        lo, hi = self.ranges[layer]
        mid = (lo + hi) / 2
        return abs(actual_pct - mid) < 5
