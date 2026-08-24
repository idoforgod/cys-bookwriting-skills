"""M16-A: risk_assessor.py — auto_yes 안전 가드 결정론 구현
SPEC: expert_pool/deterministic-modules.md §M16-A (Round 16 #I5.1 Critical)
저자 메모리 "선택 질문 자동 yes (위험·비가역 작업 제외)" 정책 결정론 실현.

LLM 추측으로 '위험·비가역' 판단 영구 금지. 정규식 기반 결정론만.
저자 진북 #5 (보안·법적 위험) + #7 (결정론 환원) 핵심.
"""
from __future__ import annotations

import re


class RiskAssessor:
    """auto_yes 적용 가능 여부 결정론 판정.

    감지 카테고리 6개:
    - 파일 시스템 비가역 (delete/rm/destroy)
    - 게시·공개 비가역 (publish/deploy/공개·배포·발행·출간·게시)
    - Git 비가역 (push --force·reset --hard·rebase·filter-branch·gc)
    - 저자 voice immutable_core 변경
    - Mode 2 simulation promote (SIM-NNN)
    - citation 변조·gate 우회
    """

    IRREVERSIBLE_KEYWORDS: list[str] = [
        # 파일 시스템 비가역
        r"\b(delete|remove|rm|destroy|drop|purge|wipe)\b",
        r"--force|--hard|--no-backup",
        # 게시·공개 비가역
        r"\b(publish|deploy|release|public_release)\b",
        r"push\s+to\s+main",
        r"공개|배포|발행|출간|게시",
        # Git 비가역
        r"git\s+push\s+--force",
        r"git\s+reset\s+--hard",
        r"git\s+rebase",
        r"git\s+filter-branch",
        r"git\s+gc",
        # 저자 voice immutable_core·sacred_spine·voice_seal 변경
        r"immutable_core|sacred_spine|voice_seal",
        # Mode 2 simulation promote (SIM-NNN → S-NNN 비가역 승격)
        r"\bpromote\s+SIM-\d+",
        # citation·gate 우회
        r"override.*citation",
        r"skip.*citation_gate",
        r"bypass.*voice_gate",
    ]

    def is_irreversible(self, action_description: str) -> bool:
        """위험·비가역 키워드 검출 시 True → auto_yes 영구 차단."""
        if not action_description:
            return False
        return any(
            re.search(p, action_description, re.IGNORECASE)
            for p in self.IRREVERSIBLE_KEYWORDS
        )

    def matched_patterns(self, action_description: str) -> list[str]:
        """매칭된 패턴 목록 반환 (디버깅·escalate 메시지용)."""
        if not action_description:
            return []
        matched = []
        for p in self.IRREVERSIBLE_KEYWORDS:
            if re.search(p, action_description, re.IGNORECASE):
                matched.append(p)
        return matched

    def assess(self, prompt: str, action: str) -> dict:
        """auto_yes 적용 가능 여부 결정론 판정.

        prompt + action 둘 다 검사 — 어느 한쪽이라도 비가역이면 차단.
        """
        prompt_matches = self.matched_patterns(prompt)
        action_matches = self.matched_patterns(action)
        irreversible = bool(prompt_matches) or bool(action_matches)
        return {
            "auto_yes_eligible": not irreversible,
            "reason": "irreversible_keyword_detected" if irreversible else "safe_to_auto_yes",
            "requires_explicit_user": irreversible,
            "matched_patterns_in_prompt": prompt_matches,
            "matched_patterns_in_action": action_matches,
        }
