"""M8: signature_pattern_applier.py — 저자 5 시그니처 패턴 결정론 적용
SPEC: expert_pool/deterministic-modules.md §M8
저자 진북 #4 (작가성·정체성) + #7 (결정론 환원).

LLM이 시그니처 매칭 직접 수행 영구 금지.

Round 5 #B5.1: 활용률 상한 7회/챕터 (과도 사용 방지).
Round 9 patch #5: 정규식 6 → 5 패턴 정합 (M1 voice_scoring과 bit-for-bit 동일).
"""
from __future__ import annotations

import re


class SignaturePatternApplier:
    """저자 5 시그니처 패턴 적용 기회 발견·활용률 추적."""

    PATTERNS = {
        "x_not_y": r"(.+?)가 아니라\s*(.+?)(다|이다|입니다)",
        "this_book_x_not_y": r"이 책은\s*(.+?)\s*아니라\s*(.+?)\s*(다룬다|쓰는)",
        "not_three_choice": r"셋 중 하나(를|만)?\s*(선택|아니)",
        "distance_between": r"(.+?)와\s*(.+?)\s*사이의\s*거리",
        "n_founders_same_x_times": (
            r"(두|세|N|\d+|다섯)\s*(창업자|발언자|사람).*정확히\s*같은\s*\d+\s*(배|년)"
        ),
        "variable_branches_system": r"변수\s*(.+?)에\s*따라.*결과.*갈리",
    }

    MAX_PER_CHAPTER = 7  # Round 5 #B5.1 상한
    MIN_PER_CHAPTER = 3  # 활용률 30%+ 목표

    def detect_opportunities(self, text: str) -> list[tuple[str, int]]:
        """시그니처 적용 가능 위치 발견 — (pattern_name, position)."""
        ops: list[tuple[str, int]] = []
        for name, pat in self.PATTERNS.items():
            for m in re.finditer(pat, text):
                ops.append((name, m.start()))
        return ops

    def count_existing(self, text: str) -> dict[str, int]:
        return {name: len(re.findall(p, text)) for name, p in self.PATTERNS.items()}

    def total_count(self, text: str) -> int:
        return sum(self.count_existing(text).values())

    def is_overused(self, text: str) -> bool:
        """챕터당 MAX_PER_CHAPTER 초과 여부."""
        return self.total_count(text) > self.MAX_PER_CHAPTER

    def is_underused(self, text: str) -> bool:
        return self.total_count(text) < self.MIN_PER_CHAPTER

    def utilization_rate(self, text: str) -> float:
        """활용률 0-1 — MAX 기준 정규화."""
        return min(1.0, self.total_count(text) / max(self.MIN_PER_CHAPTER, 1))
