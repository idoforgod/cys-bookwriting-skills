"""M17: atomic_writer.py — POSIX atomic write (yaml registry + chapter .md)
SPEC: expert_pool/deterministic-modules.md §M17
저자 진북 #4 (작가성) + #7 (결정론 환원) — 사이클 중단 시 partial 손상 방어.

Round 11 #F4.2 Critical: tmpfile → fsync → rename (POSIX atomic guarantee).
"""
from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path


class AtomicWriter:
    """모든 registry yaml + chapter .md 파일 atomic write 강제."""

    def write(self, target_path: Path, content: str, encoding: str = "utf-8") -> str:
        """tmpfile → fsync → rename. 실패 시 tmpfile 정리.

        Returns:
            content의 SHA-256 (hash chain용 — Round 8 #D1.1)
        """
        target_path = Path(target_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        fd, tmp_path = tempfile.mkstemp(
            dir=str(target_path.parent),
            prefix=f".{target_path.name}.",
            suffix=".tmp",
        )
        try:
            with os.fdopen(fd, "w", encoding=encoding) as f:
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, str(target_path))
            return hashlib.sha256(content.encode(encoding)).hexdigest()
        except Exception:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    def write_with_backup(
        self, target_path: Path, content: str, backup_dir: Path, rotation: int = 10
    ) -> dict:
        """atomic write + 백업 rotation. Round 5 #B9.4 정합."""
        target_path = Path(target_path)
        backup_dir = Path(backup_dir)
        backup_dir.mkdir(parents=True, exist_ok=True)

        # 기존 파일이 있으면 백업
        backup_path = None
        if target_path.exists():
            import datetime as _dt

            ts = _dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
            backup_path = backup_dir / f"{target_path.name}.{ts}.bak"
            backup_path.write_text(target_path.read_text(encoding="utf-8"), encoding="utf-8")
            self._rotate_backups(backup_dir, target_path.name, rotation)

        sha = self.write(target_path, content)
        return {"sha256": sha, "backup_path": str(backup_path) if backup_path else None}

    @staticmethod
    def _rotate_backups(backup_dir: Path, base_name: str, keep: int) -> None:
        """오래된 백업 N개 초과 제거."""
        backups = sorted(backup_dir.glob(f"{base_name}.*.bak"))
        if len(backups) > keep:
            for old in backups[: len(backups) - keep]:
                try:
                    old.unlink()
                except OSError:
                    pass
