"""M9: ai_tone_purger.py — AI 어투 패턴 결정론 감지 (PROH-005)
SPEC: expert_pool/deterministic-modules.md §M9
저자 진북 #4 (작가성) + #6 (취약 독자 보호) — AI 어투가 저자 voice를 *오염*하면 독자 신뢰 손상.

Round 5 #B1.6 + Round 5 #B4 보강:
- 한국어 AI 어투 풀
- 영어 AI 어투 풀 (영문 원문 인용 시)
- 저자 reference 풀 검증 (실제 저자 사용 표현 보호)
"""
from __future__ import annotations

import re
from pathlib import Path


class AiTonePurger:
    """AI 어투 패턴 풀 자동 감지·저자 voice 보호."""

    AI_TONE_PATTERNS_KO = [
        r"물론,?\s*이는?\s*매우\s*중요",
        r"다음과 같이 살펴볼 수 있",
        r"이러한 점들을 고려할 때",
        r"결론적으로 말하자면",
        r"여러분도 동의하실 것",
        r"중요한 점은\s+다음과",
        r"흥미로운 사실은\s+다음과",
        r"먼저,?\s*우리는\s+살펴봐야",
    ]

    AI_TONE_PATTERNS_EN = [
        r"Furthermore,",
        r"It is important to note",
        r"In conclusion,",
        r"It is worth noting",
        r"To summarize,",
        r"As an AI",
        r"Let me\s+(explain|elaborate|break this down)",
    ]

    def detect(self, text: str, language: str = "ko") -> list[tuple[str, int]]:
        """AI 어투 패턴 detected — (pattern, position)."""
        patterns = (
            self.AI_TONE_PATTERNS_KO if language == "ko" else self.AI_TONE_PATTERNS_EN
        )
        matches: list[tuple[str, int]] = []
        for p in patterns:
            for m in re.finditer(p, text, re.IGNORECASE):
                matches.append((p, m.start()))
        return matches

    def count_violations(self, text: str, language: str = "ko") -> int:
        return len(self.detect(text, language))

    def is_in_user_voice_corpus(self, pattern: str, reference_pool_path: Path) -> bool:
        """Round 5 #B1.6 — 저자가 *실제 사용*하는 표현이면 PROH 적용 안 함."""
        reference_pool_path = Path(reference_pool_path)
        if not reference_pool_path.exists():
            return False
        try:
            for ref_file in reference_pool_path.glob("**/*.md"):
                if not ref_file.is_file():
                    continue
                content = ref_file.read_text(encoding="utf-8")
                if re.search(pattern, content):
                    return True
        except (OSError, PermissionError):
            pass
        return False

    def has_violation(self, text: str, language: str = "ko") -> bool:
        return self.count_violations(text, language) > 0
