"""M14: author_wellness_gatekeeper.py — 저자 진북 #6 정신건강 보호 결정론
SPEC: book-config.yaml §author_wellness_policy + Round 17 #J2.1 Critical

저자 wellness 정책 결정론:
- 일일 사이클 3회 초과 차단 (daily_cycle_max)
- 심야 23:00-06:00 신규 사이클 차단 (late_night_block_after/early_morning_block_before)
- 연속 2시간 작업 경고 (consecutive_hour_warn)
- 주간 14회 사이클 한도 (weekly_max_cycles)
"""
from __future__ import annotations

from datetime import datetime, time, timedelta, timezone
from pathlib import Path

import yaml


class AuthorWellnessGatekeeper:
    """저자 wellness 정책 결정론 게이트. LLM 판단 영구 금지."""

    def __init__(self, config_path: Path | None = None):
        if config_path:
            with open(config_path, encoding="utf-8") as f:
                config = yaml.safe_load(f.read())
            policy = config.get("author_wellness_policy", {})
        else:
            policy = {}
        self.enabled: bool = policy.get("enabled", True)
        self.daily_cycle_max: int = policy.get("daily_cycle_max", 3)
        self.consecutive_hour_warn: int = policy.get("consecutive_hour_warn", 2)
        self.late_night_block_after: str = policy.get("late_night_block_after", "23:00")
        self.early_morning_block_before: str = policy.get("early_morning_block_before", "06:00")
        self.break_recommendation_minutes: int = policy.get("break_recommendation_minutes", 15)
        self.weekly_max_cycles: int = policy.get("weekly_max_cycles", 14)

    @staticmethod
    def _parse_hhmm(s: str) -> time:
        hh, mm = s.split(":")
        return time(int(hh), int(mm))

    def is_late_night(self, now: datetime) -> bool:
        """심야 (23:00-06:00) 여부."""
        late = self._parse_hhmm(self.late_night_block_after)
        early = self._parse_hhmm(self.early_morning_block_before)
        now_t = now.time()
        # late_night_block_after = 23:00, early_morning_block_before = 06:00
        # 23:00 ≤ now or now < 06:00 → 심야
        return now_t >= late or now_t < early

    def count_today_cycles(self, cycles: list[dict], now: datetime) -> int:
        """오늘 (UTC 기준 동일 date) 등록 사이클 수."""
        today = now.date()
        count = 0
        for c in cycles:
            created_str = c.get("created")
            if not created_str:
                continue
            try:
                created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                continue
            if created.date() == today:
                count += 1
        return count

    def count_week_cycles(self, cycles: list[dict], now: datetime) -> int:
        """주간 (최근 7일) 사이클 수."""
        threshold = now - timedelta(days=7)
        count = 0
        for c in cycles:
            created_str = c.get("created")
            if not created_str:
                continue
            try:
                created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
            except (ValueError, TypeError):
                continue
            if created >= threshold:
                count += 1
        return count

    GAP_THRESHOLD_MINUTES = 90  # 사이클당 30-60분 가정, 90분 이상 간격 시 블록 단절

    def consecutive_hours_active(self, cycles: list[dict], now: datetime) -> float:
        """연속 활동 시간 (시간 단위). 최근 사이클 timestamp 기반.

        gap > GAP_THRESHOLD_MINUTES 시 단절 간주.
        """
        if not cycles:
            return 0.0
        timestamps = []
        for c in cycles:
            created_str = c.get("created")
            if not created_str:
                continue
            try:
                timestamps.append(
                    datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                )
            except (ValueError, TypeError):
                continue
        if not timestamps:
            return 0.0
        timestamps.sort(reverse=True)
        last = timestamps[0]
        block_start = last
        gap = timedelta(minutes=self.GAP_THRESHOLD_MINUTES)
        for ts in timestamps[1:]:
            if (block_start - ts) > gap:
                break
            block_start = ts
        if (now - last) > gap:
            return 0.0
        return (now - block_start).total_seconds() / 3600.0

    def assess(self, cycles: list[dict], now: datetime | None = None) -> dict:
        """신규 사이클 허용 여부 결정론 판정."""
        if not self.enabled:
            return {"allow_new_cycle": True, "reason": "wellness_disabled"}

        now = now or datetime.now(timezone.utc)
        today_count = self.count_today_cycles(cycles, now)
        week_count = self.count_week_cycles(cycles, now)
        consecutive = self.consecutive_hours_active(cycles, now)
        late_night = self.is_late_night(now)

        violations: list[str] = []
        if today_count >= self.daily_cycle_max:
            violations.append("daily_cycle_max_reached")
        if week_count >= self.weekly_max_cycles:
            violations.append("weekly_max_cycles_reached")
        if late_night:
            violations.append("late_night_block")
        if consecutive >= self.consecutive_hour_warn:
            violations.append("consecutive_hour_warn")

        # late_night + daily_max + weekly_max → 차단
        # consecutive_hour_warn → 경고만 (allow=True, warn=True)
        blocking = [
            v for v in violations
            if v in {"daily_cycle_max_reached", "weekly_max_cycles_reached", "late_night_block"}
        ]
        warning = "consecutive_hour_warn" in violations

        return {
            "allow_new_cycle": len(blocking) == 0,
            "warning": warning,
            "violations": violations,
            "today_cycle_count": today_count,
            "week_cycle_count": week_count,
            "consecutive_hours_active": round(consecutive, 2),
            "late_night": late_night,
            "break_recommendation_minutes": self.break_recommendation_minutes if warning else 0,
        }
