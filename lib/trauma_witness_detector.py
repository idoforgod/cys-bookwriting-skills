"""M15: trauma_witness_detector.py — 저자 진북 #6 trauma 증언 결정론 검출
SPEC: expert_pool/citation-authority-db.yaml §trauma_bearing_witness_category

6 카테고리 자동 검출 + 저자 6 보호 정책 트리거:
- war_survivor (참전·생존자)
- mass_disaster_bereaved (세월호·이태원·9·11 유가족)
- state_violence_victim (5·18·4·3·정치박해)
- sexual_violence_survivor (성폭력·성착취)
- pandemic_loss_bereaved (COVID-19 유가족)
- deceased_digital_remnant (사망자 SNS·voice clone)

LLM 추론 영구 금지 — citation-authority-db 결정론 키워드 매칭만.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class TraumaDetection:
    detected: bool
    category_ids: list[str]
    matched_keywords: list[str]
    protocol_required: dict


class TraumaWitnessDetector:
    """trauma_bearing_witness 6 카테고리 결정론 검출."""

    DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "expert_pool" / "citation-authority-db.yaml"

    def __init__(self, db_path: Path | None = None):
        path = Path(db_path) if db_path else self.DEFAULT_DB_PATH
        with open(path, encoding="utf-8") as f:
            db = yaml.safe_load(f.read())
        category_block = db.get("trauma_bearing_witness_category", {})
        self.enabled: bool = category_block.get("enabled", True)
        self.categories: list[dict] = category_block.get("categories", [])
        self.protocol: dict = category_block.get("protocol", {})
        self.trigger_keywords: list[str] = category_block.get("detection_trigger_keywords", [])
        self.fix_action: str = category_block.get("fix_action", "")

    def detect(self, text: str) -> TraumaDetection:
        """본문 trauma 키워드 결정론 매칭."""
        if not self.enabled or not text:
            return TraumaDetection(False, [], [], {})

        matched_keywords = [
            kw for kw in self.trigger_keywords
            if re.search(re.escape(kw), text)
        ]

        # 매칭된 키워드 → 카테고리 매핑
        matched_categories: list[str] = []
        for kw in matched_keywords:
            for cat in self.categories:
                examples = cat.get("examples", [])
                if any(kw in ex for ex in examples):
                    cat_id = cat.get("id")
                    if cat_id and cat_id not in matched_categories:
                        matched_categories.append(cat_id)
            # 키워드만 매칭되고 example 매핑 실패 → 일반 trauma 플래그
        # 키워드 매칭은 있는데 카테고리 매핑 실패 시 → fall-back generic
        if matched_keywords and not matched_categories:
            matched_categories.append("generic_trauma")

        return TraumaDetection(
            detected=bool(matched_keywords),
            category_ids=matched_categories,
            matched_keywords=matched_keywords,
            protocol_required=self.protocol if matched_keywords else {},
        )

    def requires_safe_messaging(self, text: str) -> bool:
        """Safe Messaging Gatekeeper 발동 필요 여부 결정론."""
        result = self.detect(text)
        return result.detected and bool(result.protocol_required.get("safe_messaging_invoke"))

    def requires_consent_verification(self, text: str) -> bool:
        """저자 동의 검증 필요 여부."""
        result = self.detect(text)
        return result.detected and result.protocol_required.get("consent_status") == "required_before_quote"

    def assess(self, text: str) -> dict:
        """결정론 보호 정책 발동 여부 반환."""
        result = self.detect(text)
        return {
            "trauma_detected": result.detected,
            "categories": result.category_ids,
            "matched_keywords": result.matched_keywords,
            "actions_required": {
                "safe_messaging_invoke": result.protocol_required.get("safe_messaging_invoke", False),
                "consent_verification": result.protocol_required.get("consent_status") == "required_before_quote",
                "anonymity_default": result.protocol_required.get("anonymity_default", False),
                "hotline_required": result.protocol_required.get("hotline_required", False),
                "re_traumatization_warning": result.protocol_required.get("re_traumatization_warning", False),
            },
            "citation_gate_priority": result.protocol_required.get("citation_gate_priority"),
            "fix_action": self.fix_action if result.detected else None,
        }
