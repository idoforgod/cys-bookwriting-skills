#!/usr/bin/env python3
"""경로 해석 단일 창구.

이 스킬 묶음은 어느 컴퓨터에서나 그대로 동작해야 한다. 따라서 특정 사용자의
절대 경로를 코드나 문서에 박지 않고, 아래 두 뿌리만으로 모든 경로를 유도한다.

SKILLS_ROOT
    이 스킬 패키지가 설치된 위치. ``__file__`` 로 자동 탐지하므로 설정이 필요 없다.

BOOK_ROOT
    사용자의 *책 프로젝트* 루트. 다음 순서로 해석한다.

    1. 환경변수 ``BOOKWRITING_BOOK_ROOT``
    2. 현재 디렉토리에서 위로 올라가며 ``master/book-config.yaml`` 을 가진 디렉토리
    3. ``~/bookwriting`` (기본값)

책 프로젝트의 표준 배치:

    $BOOK_ROOT/
      master/     book-config.yaml · seed-registry.yaml · cycle-registry.yaml
                  forecast-registry.yaml · sim-registry.yaml
      chapters/   장별 작업물
      inbox/      아직 분류되지 않은 흡수 자료
      bookidea/   skeleton.md (책 외골격)

``python3 lib/paths.py`` 로 직접 실행하면 현재 해석 결과를 출력한다.
"""
from __future__ import annotations

import os
from pathlib import Path

__all__ = [
    "ENV_BOOK_ROOT",
    "ENV_REFERENCE_PATHS",
    "skills_root",
    "book_root",
    "master_dir",
    "chapters_dir",
    "inbox_dir",
    "bookidea_dir",
    "book_config_path",
    "seed_registry_path",
    "cycle_registry_path",
    "forecast_registry_path",
    "sim_registry_path",
    "skeleton_path",
    "authority_db_path",
    "templates_dir",
    "reference_paths",
    "describe",
]

ENV_BOOK_ROOT = "BOOKWRITING_BOOK_ROOT"
ENV_REFERENCE_PATHS = "BOOKWRITING_REFERENCE_PATHS"

DEFAULT_BOOK_ROOT = Path.home() / "bookwriting"

# 책 프로젝트를 식별하는 표지 파일 — 위로 거슬러 올라갈 때의 기준.
MARKER = Path("master") / "book-config.yaml"


def skills_root() -> Path:
    """이 스킬 패키지가 설치된 루트 (lib/ 의 부모)."""
    return Path(__file__).resolve().parent.parent


def _search_upward(start: Path) -> Path | None:
    """start 부터 위로 올라가며 책 프로젝트 표지를 찾는다."""
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / MARKER).exists():
            return candidate
    return None


def book_root(start: Path | str | None = None) -> Path:
    """책 프로젝트 루트를 해석한다. 존재 여부는 검사하지 않는다."""
    env = os.environ.get(ENV_BOOK_ROOT, "").strip()
    if env:
        return Path(env).expanduser().resolve()

    found = _search_upward(Path(start) if start else Path.cwd())
    if found is not None:
        return found

    return DEFAULT_BOOK_ROOT


def master_dir(root: Path | None = None) -> Path:
    return (root or book_root()) / "master"


def chapters_dir(root: Path | None = None) -> Path:
    return (root or book_root()) / "chapters"


def inbox_dir(root: Path | None = None) -> Path:
    return (root or book_root()) / "inbox"


def bookidea_dir(root: Path | None = None) -> Path:
    return (root or book_root()) / "bookidea"


def book_config_path(root: Path | None = None) -> Path:
    return master_dir(root) / "book-config.yaml"


def seed_registry_path(root: Path | None = None) -> Path:
    return master_dir(root) / "seed-registry.yaml"


def cycle_registry_path(root: Path | None = None) -> Path:
    return master_dir(root) / "cycle-registry.yaml"


def forecast_registry_path(root: Path | None = None) -> Path:
    return master_dir(root) / "forecast-registry.yaml"


def sim_registry_path(root: Path | None = None) -> Path:
    return master_dir(root) / "sim-registry.yaml"


def skeleton_path(root: Path | None = None) -> Path:
    """책 외골격 문서 (목차·구조의 단일 진실)."""
    return bookidea_dir(root) / "skeleton.md"


def authority_db_path() -> Path:
    """인용 권위 등급 DB — 스킬 패키지에 동봉된 기본본."""
    return skills_root() / "expert_pool" / "citation-authority-db.yaml"


def templates_dir() -> Path:
    """`bookwriting init` 이 복사해 쓰는 템플릿 모음."""
    return skills_root() / "templates"


def reference_paths() -> list[Path]:
    """저자 개인 참고자료 경로 목록.

    환경변수 ``BOOKWRITING_REFERENCE_PATHS`` 에 OS 경로 구분자(`:` / `;`)로 나열한다.
    예) 이전 저서 원고 폴더, 강의록 폴더, Obsidian vault.
    설정하지 않으면 빈 목록이며, 그때는 book-config.yaml 의
    ``search_paths.tier_2_explicit`` 만 쓰인다.
    """
    raw = os.environ.get(ENV_REFERENCE_PATHS, "").strip()
    if not raw:
        return []
    return [Path(p).expanduser().resolve() for p in raw.split(os.pathsep) if p.strip()]


def describe() -> dict[str, object]:
    """현재 해석 결과 — 설치 점검·디버깅용."""
    root = book_root()
    return {
        "skills_root": str(skills_root()),
        "book_root": str(root),
        "book_root_exists": root.exists(),
        "book_config": str(book_config_path(root)),
        "book_config_exists": book_config_path(root).exists(),
        "resolved_by": (
            f"환경변수 {ENV_BOOK_ROOT}"
            if os.environ.get(ENV_BOOK_ROOT, "").strip()
            else ("상위 디렉토리 탐색" if _search_upward(Path.cwd()) else "기본값 ~/bookwriting")
        ),
        "reference_paths": [str(p) for p in reference_paths()],
    }


if __name__ == "__main__":
    import json

    print(json.dumps(describe(), ensure_ascii=False, indent=2))
