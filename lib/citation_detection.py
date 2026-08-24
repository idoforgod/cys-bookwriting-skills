"""M2: citation_detection.py — 저자 진북 #3 (출처 명시) + #1 (할루시네이션 0)
SPEC: expert_pool/deterministic-modules.md §M2
5 할루시네이션 신호 결정론 감지 — LLM 추측 영구 금지.

신호 (Round 4·9·13·14·17 누적):
1. source_file_missing
2. source_format_vague (한 보고서에 따르면 등)
3. metadata_incomplete (author·date·publication 누락)
4. url_doi_invalid
5. stat_no_source
6. physical_implausibility (Round 13 patch #10) — 별도 검증
7. timescale_mismatch (Round 14 #H9.2)
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class CitationMetadata:
    author: Optional[str] = None
    title: Optional[str] = None
    publication: Optional[str] = None
    date: Optional[str] = None
    page_or_section: Optional[str] = None
    source_file: Optional[Path] = None
    url: Optional[str] = None
    doi: Optional[str] = None


@dataclass
class HallucinationSignals:
    source_file_missing: bool
    source_format_vague: bool
    metadata_incomplete: bool
    url_doi_invalid: bool
    stat_no_source: bool

    def is_critical(self) -> bool:
        return self.source_file_missing or self.source_format_vague


class HallucinationDetector:
    """5 신호 결정론 감지기. 모든 citation 검증에 호출."""

    VAGUE_PATTERNS = [
        r"한 보고서에 따르면",
        r"전문가들이 말한다",
        r"최근 연구에서",
        r"어느 분석에 따르면",
        r"한 연구는",
        r"일부.*는",
    ]

    DOI_PATTERN = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)
    URL_PATTERN = re.compile(r"^https?://[^\s]+\.[^\s]+$")
    STAT_PATTERN = re.compile(r"\d+(?:\.\d+)?\s*(%|배|명|달러|원|년)")

    def detect_source_file_missing(self, citation: CitationMetadata) -> bool:
        if citation.source_file is None:
            return True
        return not Path(citation.source_file).exists()

    def detect_source_format_vague(self, text: str) -> bool:
        return any(re.search(p, text) for p in self.VAGUE_PATTERNS)

    def detect_metadata_incomplete(self, citation: CitationMetadata) -> bool:
        return any(getattr(citation, f) is None for f in ("author", "date", "publication"))

    def detect_url_doi_invalid(self, citation: CitationMetadata) -> bool:
        if citation.url:
            if not self.URL_PATTERN.match(citation.url):
                return True
        if citation.doi:
            if not self.DOI_PATTERN.match(citation.doi):
                return True
        return False

    def detect_stat_no_source(self, text: str, citation: CitationMetadata) -> bool:
        has_stat = bool(self.STAT_PATTERN.search(text))
        if has_stat and citation.source_file is None:
            return True
        return False

    def detect_all(self, text: str, citation: CitationMetadata) -> HallucinationSignals:
        return HallucinationSignals(
            source_file_missing=self.detect_source_file_missing(citation),
            source_format_vague=self.detect_source_format_vague(text),
            metadata_incomplete=self.detect_metadata_incomplete(citation),
            url_doi_invalid=self.detect_url_doi_invalid(citation),
            stat_no_source=self.detect_stat_no_source(text, citation),
        )
