"""M10: fact_extractor.py — fact·통계 결정론 추출 + Wagner-Fischer Levenshtein duplicate
SPEC: expert_pool/deterministic-modules.md §M10
저자 진북 #1 (할루시네이션 0) + #3 (출처 명시) + #7 (결정론 환원).

Round 9 #E10.1 — duplicate 검출 body 완성 (pure Python Levenshtein).
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class FactCandidate:
    fact_id: str
    text: str
    source_position: int
    fact_type: str


class FactExtractor:
    """fact·통계 결정론 추출 + duplicate 검출."""

    PATTERNS = {
        "percentage": r"\d+(?:\.\d+)?\s*%",
        "scale": r"\d+(?:\.\d+)?\s*배",
        "year": r"\d{4}\s*년",
        "count": r"\d+(?:\.\d+)?\s*(?:억|만|명|개)",
        "currency": r"\d+(?:\.\d+)?\s*(?:달러|원|만원|억원)",
    }

    LEVENSHTEIN_THRESHOLD = 3  # 거리 < 3 → 유사 fact

    def extract(self, text: str, start_id: int = 1) -> list[FactCandidate]:
        facts: list[FactCandidate] = []
        next_id = start_id
        for ftype, pattern in self.PATTERNS.items():
            for m in re.finditer(pattern, text):
                facts.append(
                    FactCandidate(
                        fact_id=f"F-{next_id:03d}",
                        text=m.group(0).strip(),
                        source_position=m.start(),
                        fact_type=ftype,
                    )
                )
                next_id += 1
        return facts

    @staticmethod
    def levenshtein(s1: str, s2: str) -> int:
        """Wagner-Fischer O(m·n) DP. pure Python (Round 9 #E10.1)."""
        if len(s1) < len(s2):
            return FactExtractor.levenshtein(s2, s1)
        if len(s2) == 0:
            return len(s1)
        previous = list(range(len(s2) + 1))
        for i, c1 in enumerate(s1):
            current = [i + 1]
            for j, c2 in enumerate(s2):
                ins = previous[j + 1] + 1
                delete = current[j] + 1
                sub = previous[j] + (c1 != c2)
                current.append(min(ins, delete, sub))
            previous = current
        return previous[-1]

    def detect_duplicates(self, facts: list[FactCandidate]) -> list[list[str]]:
        """유사 fact 그룹화 (Levenshtein < 3). 단일 fact는 그룹 제외."""
        groups: list[list[str]] = []
        used: set[str] = set()
        for i, a in enumerate(facts):
            if a.fact_id in used:
                continue
            group = [a.fact_id]
            used.add(a.fact_id)
            for b in facts[i + 1 :]:
                if b.fact_id in used:
                    continue
                if a.fact_type != b.fact_type:
                    continue
                if self.levenshtein(a.text, b.text) < self.LEVENSHTEIN_THRESHOLD:
                    group.append(b.fact_id)
                    used.add(b.fact_id)
            if len(group) > 1:
                groups.append(group)
        return groups
