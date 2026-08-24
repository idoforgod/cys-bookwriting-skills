"""M3: authority_grader.py — 저자 권위 7층 (A·A_preprint·B·C·D·E·F·G) 결정론 매핑
SPEC: expert_pool/deterministic-modules.md §M3
저자 진북 #3 (출처 명시) + #7 (결정론 환원) 강제.

LLM이 "이건 Grade A 같다" 추측 영구 금지. citation-authority-db.yaml 결정론 lookup.

Round 9 #E2.1 + Round 16 #I6.1 통합:
- Grade enum 7층 (A·A_preprint·B·C·D·E·F·G·OUT)
- publication_pattern 단일 정규식 (publications list 미파싱 결함 해소)
"""
from __future__ import annotations

import re
from enum import Enum
from pathlib import Path
from typing import Optional

import yaml


class Grade(str, Enum):
    A = "A"
    A_PREPRINT = "A_preprint"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    OUT = "out"


class AuthorityGrader:
    """citation-authority-db.yaml 결정론 lookup. yaml.safe_load 강제 (Round 8 #D3.1)."""

    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        with open(self.db_path, encoding="utf-8") as f:
            self.db = yaml.safe_load(f.read())
        self.policy = self.db.get("matching_policy", {})
        self.entries = self.db.get("authority_grades", [])

    def assign_grade(
        self,
        author: Optional[str] = None,
        publication: Optional[str] = None,
        source_type: Optional[str] = None,
    ) -> Grade:
        """우선순위: author > publication > source_type.

        매칭 안 되면 임시 Grade C 반환 + 미매칭 로그.
        """
        for entry in self.entries:
            # 1. author_pattern
            if "author_pattern" in entry and author:
                if re.search(entry["author_pattern"], author, re.IGNORECASE):
                    return Grade(entry["grade"])
            # 2. publication_pattern
            if "publication_pattern" in entry and publication:
                if re.search(entry["publication_pattern"], publication, re.IGNORECASE):
                    return Grade(entry["grade"])
            # 3. source_type
            if "source_type" in entry and source_type:
                if entry["source_type"] == source_type:
                    return Grade(entry["grade"])

        # 매칭 안 됨 → 임시 Grade C
        self._log_unmatched(author, publication, source_type)
        return Grade.C

    def _log_unmatched(
        self, author: Optional[str], publication: Optional[str], source_type: Optional[str]
    ) -> None:
        """미매칭 author·publication·source_type을 learning log에 append (Round 9 #E10.1)."""
        from datetime import datetime, timezone

        log_path = (
            Path(__file__).resolve().parent.parent
            / "_progress"
            / "citation-authority-learning-log.md"
        )
        log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = (
            f"\n- {datetime.now(timezone.utc).isoformat()} | "
            f"author={author!r} | publication={publication!r} | source_type={source_type!r}"
        )
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(entry)

    def count_by_grade(self) -> dict[Grade, int]:
        """현재 db의 grade 분포 — Diversity Gatekeeper용."""
        counts = {g: 0 for g in Grade}
        for entry in self.entries:
            try:
                g = Grade(entry.get("grade", "out"))
                counts[g] += 1
            except ValueError:
                continue
        return counts

    def verify_r4_multi_layer(self, citation_grades: list[Grade]) -> dict:
        """R4 다층 인용 강제 (Round 8 #D1.4) — 주장 1개당 최소 2 layer.

        citation_grades = 같은 주장을 뒷받침하는 citation들의 grade 목록.
        """
        unique_layers = {g for g in citation_grades if g != Grade.OUT}
        is_pass = len(unique_layers) >= 2
        return {
            "layer_count": len(unique_layers),
            "layers": sorted(g.value for g in unique_layers),
            "r4_pass": is_pass,
            "action": "approve" if is_pass else "exclude_or_escalate",
        }
