"""M7: id_generator.py — bookwriting v2 결정론 ID 발급
SPEC: expert_pool/deterministic-modules.md §M7
저자 진북 #7 (결정론 환원) 강제 — LLM이 ID 임의 생성 영구 금지.

ID 종류:
- S-NNN: seed (seed-registry)
- C-NNN: cycle (cycle-registry)
- SIM-NNN: simulation (cycle-registry 별도 분류)
- INS-NNN: insight (insight-synthesis 후보)
- F-NNN: fact (fact-anchor)
- D-NNN: decision (HITL 묶음)
- E-NNN: evidence (evidence-collect)
- CITE-NNN: citation (citation-gate)

atomic lock (fcntl) 강제 — 동시 사이클 race condition 방어.
"""
from __future__ import annotations

import fcntl
import re
from pathlib import Path
from typing import Optional


class IdGenerator:
    """결정론 ID 발급 (atomic file lock 강제). Round 8 #D4.3·Round 16 #I 패치 통합."""

    PREFIXES = {
        "seed": "S",
        "cycle": "C",
        "simulation": "SIM",
        "insight": "INS",
        "fact": "F",
        "decision": "D",
        "evidence": "E",
        "citation": "CITE",
        "prediction": "P",
    }

    ID_PATTERN = re.compile(r"^(?P<prefix>[A-Z]+)-(?P<num>\d{3,4})$")

    def __init__(self, registry_path: Path, lock_path: Optional[Path] = None):
        self.registry_path = Path(registry_path)
        self.lock_path = lock_path or self.registry_path.with_suffix(".lock")
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)

    @classmethod
    def parse_id(cls, id_str: str) -> tuple[str, int]:
        """ID 파싱 — 결정론 정규식. 잘못된 형식 → ValueError."""
        m = cls.ID_PATTERN.match(id_str)
        if not m:
            raise ValueError(f"잘못된 ID 형식: {id_str!r} (기대: PREFIX-NNN)")
        return m.group("prefix"), int(m.group("num"))

    def issue(self, id_type: str, current_max_num: int) -> str:
        """atomic file lock 보호 하에 max+1 발급.

        Args:
            id_type: PREFIXES 키 (seed·cycle·simulation 등)
            current_max_num: registry에서 읽은 현재 최대 번호

        Returns:
            "PREFIX-NNN" 형식 ID
        """
        if id_type not in self.PREFIXES:
            raise ValueError(f"알 수 없는 id_type: {id_type!r}")
        prefix = self.PREFIXES[id_type]

        with open(self.lock_path, "w") as lock_f:
            fcntl.flock(lock_f, fcntl.LOCK_EX)
            try:
                next_num = current_max_num + 1
                return f"{prefix}-{next_num:03d}"
            finally:
                fcntl.flock(lock_f, fcntl.LOCK_UN)

    @classmethod
    def compute_max_num(cls, ids: list[str], prefix: str) -> int:
        """기존 ID 목록에서 동일 prefix의 max 번호 계산. 빈 목록 → 0."""
        nums = []
        for id_str in ids:
            try:
                p, n = cls.parse_id(id_str)
                if p == prefix:
                    nums.append(n)
            except ValueError:
                continue
        return max(nums) if nums else 0
