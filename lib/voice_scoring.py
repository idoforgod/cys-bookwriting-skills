"""M1: voice_scoring.py — 저자 voice_score 6 가중치 결정론 계산
SPEC: expert_pool/deterministic-modules.md §M1
저자 진북 #4 (작가성·정체성) + #7 (결정론 환원).

가중치 (합 = 1.00):
- vocabulary_match: 0.27 (preferred·avoid substring)
- sentence_rhythm: 0.18 (평균 길이·max 위반)
- structure_pattern: 0.18 (명제→근거→사례→통찰)
- signature_presence: 0.14 (5 시그니처 정규식)
- prohibition_avoidance: 0.13 (PROH-001~008)
- meaning_score: 0.10 (Round 9 #E9.1 — 저자 사상적 척추 4개 + contradicting_claims)

LLM이 자연어로 점수 *생성* 영구 금지.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class VoiceScoreBreakdown:
    vocabulary_match: float
    sentence_rhythm: float
    structure_pattern: float
    signature_presence: float
    prohibition_avoidance: float
    meaning_score: float
    weighted_total: float


class VoiceScorer:
    WEIGHTS = {
        "vocabulary_match": 0.27,
        "sentence_rhythm": 0.18,
        "structure_pattern": 0.18,
        "signature_presence": 0.14,
        "prohibition_avoidance": 0.13,
        "meaning_score": 0.10,
    }

    # 저자 5 시그니처 정규식 (Round 4 #A3.7·Round 6 #A6.6 수정)
    SIGNATURE_PATTERNS = [
        r"(.+?)가 아니라\s*(.+?)(다|이다|입니다)",
        r"이 책은\s*(.+?)\s*아니라\s*(.+?)\s*(다룬다|쓰는)",
        r"셋 중 하나(를|만)?\s*(선택|아니)",
        r"(.+?)와\s*(.+?)\s*사이의\s*거리",
        r"(두|세|N|\d+|다섯)\s*(창업자|발언자|사람).*정확히\s*같은\s*\d+\s*(배|년)",
        r"변수\s*(.+?)에\s*따라.*결과.*갈리",
    ]

    # 저자 4 사상적 척추 (Round 9 #E9.1)
    SPINE_KEYWORDS = {
        "meta_tool": ["메타도구", "메타 도구", "도구를 만드는 도구", "인지 확장"],
        "system_thinking": ["시스템 사고", "피드백 루프", "약신호", "추동력"],
        "ubi_intelligence": ["UBI(지능)", "보편적 기본 지능", "박사급 지능"],
        "human_creator": ["인문학적 창조자", "어떻게 설계할", "철학"],
    }

    def __init__(self, voice_guidelines: dict[str, Any]):
        self.guidelines = voice_guidelines
        self.preferred = set(voice_guidelines.get("vocabulary", {}).get("preferred", []))
        self.avoid = set(voice_guidelines.get("vocabulary", {}).get("avoid", []))
        self.prohibitions = voice_guidelines.get("prohibitions", [])
        self.signatures = voice_guidelines.get("signature_expressions", [])
        self.max_chars = voice_guidelines.get("sentence", {}).get("max_length_chars", 80)
        self.contradicting_claims = self._collect_contradicting_claims()

    def _collect_contradicting_claims(self) -> list[str]:
        """prohibitions에서 contradicting_claims 집합 — Round 9 #E9.1."""
        claims: list[str] = []
        for proh in self.prohibitions:
            if isinstance(proh, dict):
                claims.extend(proh.get("contradicting_claims", []) or [])
        return claims

    # --- 6 가중치 결정론 함수 ---

    def compute_vocabulary_match(self, text: str) -> float:
        preferred_count = sum(text.count(term) for term in self.preferred)
        avoid_count = sum(text.count(term) for term in self.avoid)
        total_words = max(len(text.split()), 1)
        score = (preferred_count - avoid_count) / max(total_words / 10, 1)
        return max(0.0, min(1.0, score))

    def compute_sentence_rhythm(self, text: str) -> float:
        sentences = [s.strip() for s in re.split(r"[.!?。\n]+", text) if s.strip()]
        if not sentences:
            return 0.0
        avg_length = sum(len(s) for s in sentences) / len(sentences)
        violations = sum(1 for s in sentences if len(s) > self.max_chars)
        rhythm_score = 1.0 - abs(avg_length - 50) / 50
        violation_penalty = violations / len(sentences)
        return max(0.0, min(1.0, rhythm_score - violation_penalty))

    def compute_structure_pattern(self, text: str) -> float:
        paragraphs = [p for p in text.split("\n\n") if p.strip()]
        if not paragraphs:
            return 0.0
        elements = ["명제", r"근거|증거|evidence", r"사례|예시|case", r"통찰|insight"]
        scores = []
        for p in paragraphs:
            hits = sum(1 for e in elements if re.search(e, p, re.IGNORECASE))
            scores.append(hits / len(elements))
        return sum(scores) / len(scores)

    def compute_signature_presence(self, text: str) -> float:
        matched = sum(1 for p in self.SIGNATURE_PATTERNS if re.search(p, text))
        # Round 9 patch #5: divisor = len(patterns) * 0.5 (50% 매칭 시 1.0)
        target = len(self.SIGNATURE_PATTERNS) * 0.5
        return min(1.0, matched / target) if target > 0 else 0.0

    def compute_prohibition_avoidance(self, text: str) -> float:
        violations = 0
        for proh in self.prohibitions:
            if not isinstance(proh, dict):
                continue
            example = proh.get("example_violation")
            if example and example in text:
                violations += 1
        return max(0.0, 1.0 - violations * 0.2)

    def compute_meaning_score(self, text: str) -> float:
        """저자 사상적 척추 4개 매칭 - contradicting_claims 페널티."""
        matched_spines = sum(
            1
            for keywords in self.SPINE_KEYWORDS.values()
            if any(kw in text for kw in keywords)
        )
        base_score = min(1.0, matched_spines / 2.0)
        contradict_count = sum(1 for cc in self.contradicting_claims if cc in text)
        return max(0.0, base_score - contradict_count * 0.5)

    def compute_voice_score(self, text: str) -> VoiceScoreBreakdown:
        vocab = self.compute_vocabulary_match(text)
        rhythm = self.compute_sentence_rhythm(text)
        structure = self.compute_structure_pattern(text)
        signature = self.compute_signature_presence(text)
        prohibition = self.compute_prohibition_avoidance(text)
        meaning = self.compute_meaning_score(text)

        weighted = (
            self.WEIGHTS["vocabulary_match"] * vocab
            + self.WEIGHTS["sentence_rhythm"] * rhythm
            + self.WEIGHTS["structure_pattern"] * structure
            + self.WEIGHTS["signature_presence"] * signature
            + self.WEIGHTS["prohibition_avoidance"] * prohibition
            + self.WEIGHTS["meaning_score"] * meaning
        )
        return VoiceScoreBreakdown(
            vocabulary_match=round(vocab, 3),
            sentence_rhythm=round(rhythm, 3),
            structure_pattern=round(structure, 3),
            signature_presence=round(signature, 3),
            prohibition_avoidance=round(prohibition, 3),
            meaning_score=round(meaning, 3),
            weighted_total=round(weighted, 3),
        )
