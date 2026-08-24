"""M13: r4_multi_layer_verifier.py — R4 다층 인용 결정론 검증
SPEC: expert_pool/deterministic-modules.md §M13
저자 v1 R4 규칙 — 단일 권위만 인용 영구 금지. 최소 2층 권위.

저자 진북 #3 (출처 명시) + #7 (결정론 환원) 핵심.
M3 AuthorityGrader.verify_r4_multi_layer와 독립·재사용 가능.
"""
from __future__ import annotations

from typing import Any


class R4MultiLayerVerifier:
    """주장별 권위층 수 카운트 → 단일 권위 검출."""

    MIN_LAYERS = 2

    def verify_claim(self, claim_id: str, citations: list[dict[str, Any]]) -> dict:
        """단일 주장 R4 검증.

        citations 예: [{"author": "Amodei", "grade": "A"}, {"author": "Harari", "grade": "D"}]
        """
        unique_grades = {
            c["grade"]
            for c in citations
            if isinstance(c, dict) and c.get("grade") not in (None, "out")
        }
        is_pass = len(unique_grades) >= self.MIN_LAYERS
        return {
            "claim_id": claim_id,
            "layer_count": len(unique_grades),
            "layers": sorted(unique_grades),
            "r4_pass": is_pass,
            "action": "approve" if is_pass else "exclude_or_escalate",
        }

    def verify_all_claims(
        self, claims_with_citations: dict[str, list[dict[str, Any]]]
    ) -> list[dict]:
        return [
            self.verify_claim(cid, cites) for cid, cites in claims_with_citations.items()
        ]

    def count_pass_rate(self, results: list[dict]) -> float:
        """통과율 0-1."""
        if not results:
            return 0.0
        pass_count = sum(1 for r in results if r["r4_pass"])
        return round(pass_count / len(results), 3)
