"""M4: quantitative_extraction.py — 저자 정량 표현 패턴 결정론 추출
SPEC: expert_pool/deterministic-modules.md §M4
저자 진북 #1 (할루시네이션 0) + #7 (결정론 환원).

LLM이 수치 텍스트 검색 영구 금지. 정규식 결정론.

Round 16 #I9.1 통합 — 탄소·에너지·데이터·FLOPS 단위 추가.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class QuantitativeAnchor:
    pattern_type: str
    value: str
    context: str
    source_position: int


class QuantitativeAnchorExtractor:
    """저자 정량 패턴 결정론 추출."""

    PATTERNS = {
        "scale": r"(\d+(?:\.\d+)?)\s*배",
        "percentage": r"(\d+(?:\.\d+)?)\s*%",
        "year_threshold": r"(\d{4})\s*(임계점|기점|시점)",
        "count": r"(\d+(?:\.\d+)?)\s*(억|만|명|개)",
        "currency": r"(\d+(?:\.\d+)?)\s*(달러|원|만원|억원)",
        "duration": r"(\d+(?:\.\d+)?)\s*(년|개월|일)\s*(내|안|뒤)",
        # Round 16 #I9.1 탄소·에너지 추가
        "carbon_emission": r"(\d+(?:\.\d+)?)\s*(tCO2e?|gCO2/kWh|kgCO2)",
        "energy_consumption": r"(\d+(?:\.\d+)?)\s*(Wh|kWh|MWh|GWh|TWh|MW|GW)",
        "data_volume": r"(\d+(?:\.\d+)?)\s*(KB|MB|GB|TB|PB|EB)",
        "compute_flops": r"(\d+(?:\.\d+)?)\s*(FLOPS|TFLOPS|PFLOPS|EFLOPS)",
    }

    # 저자 시그니처 정량 표현 (Round 7·Phase 3-B 2주차 fix — 스케일 옵션화)
    SIGNATURE_QUANTITATIVES = [
        ("100배 스케일 (산업혁명)", r"100\s*배(.{0,30}스케일|.{0,20}(산업혁명|말한다))?"),
        ("90% 확신 (Amodei)", r"90\s*%.{0,20}확신"),
        ("2027 임계점", r"2027\s*임계점"),
    ]

    def extract_all(self, text: str, context_chars: int = 50) -> list[QuantitativeAnchor]:
        anchors: list[QuantitativeAnchor] = []
        for ptype, pattern in self.PATTERNS.items():
            for m in re.finditer(pattern, text):
                start = max(0, m.start() - context_chars)
                end = min(len(text), m.end() + context_chars)
                anchors.append(
                    QuantitativeAnchor(
                        pattern_type=ptype,
                        value=m.group(0),
                        context=text[start:end],
                        source_position=m.start(),
                    )
                )
        return anchors

    def detect_signature_patterns(self, text: str) -> list[str]:
        return [name for name, p in self.SIGNATURE_QUANTITATIVES if re.search(p, text)]

    def has_unit(self, anchor: QuantitativeAnchor) -> bool:
        """Round 9 #C9.5 — 정량 앵커에 단위 명시 검증.

        "100배"만으론 부족 — "100배 GDP"·"100배 스케일" 같이 *맥락 단위* 필요.
        """
        # carbon·energy 등은 단위 자체 포함 → True
        if anchor.pattern_type in {
            "carbon_emission",
            "energy_consumption",
            "data_volume",
            "compute_flops",
            "currency",
        }:
            return True
        # scale·percentage·year_threshold·count·duration → context에 명사 키워드 필요
        context_keywords = [
            "GDP",
            "스케일",
            "생산성",
            "확신",
            "임계점",
            "도달",
            "범위",
            "영향",
        ]
        return any(kw in anchor.context for kw in context_keywords)
