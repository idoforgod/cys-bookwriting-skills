#!/usr/bin/env bash
#
# cys-bookwriting-skills 설치 스크립트
#
#   ./install.sh                          기본 설치 (심볼릭 링크)
#   ./install.sh --copy                   링크 대신 복사
#   ./install.sh --book-root ~/my-book    설치 후 책 프로젝트까지 만든다
#   ./install.sh --skills-dir <경로>       스킬 설치 위치 지정 (기본 ~/.claude/skills)
#   ./install.sh --uninstall              설치한 스킬 링크만 제거
#
# 이 스크립트는 당신의 책 원고를 건드리지 않는다. 스킬을 Claude Code 가 찾는
# 자리에 놓고, 필요하면 빈 책 프로젝트 뼈대를 만들어 줄 뿐이다.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
MODE="link"
BOOK_ROOT=""
FORCE=0
UNINSTALL=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --copy)        MODE="copy"; shift ;;
    --link)        MODE="link"; shift ;;
    --skills-dir)  SKILLS_DIR="$2"; shift 2 ;;
    --book-root)   BOOK_ROOT="$2"; shift 2 ;;
    --force)       FORCE=1; shift ;;
    --uninstall)   UNINSTALL=1; shift ;;
    -h|--help)     sed -n '2,14p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *)             echo "알 수 없는 옵션: $1" >&2; exit 64 ;;
  esac
done

say()  { printf '%s\n' "$*"; }
ok()   { printf '  ✓ %s\n' "$*"; }
warn() { printf '  ⚠ %s\n' "$*"; }
die()  { printf '✗ %s\n' "$*" >&2; exit 1; }

# ── 제거 ────────────────────────────────────────────────────
if [[ "$UNINSTALL" == "1" ]]; then
  say "스킬 제거 — $SKILLS_DIR"
  removed=0
  for src in "$REPO_DIR"/skills/*/; do
    name="$(basename "$src")"
    target="$SKILLS_DIR/$name"
    # 이 저장소가 설치한 것만 지운다. 남의 스킬은 건드리지 않는다.
    if [[ -L "$target" && "$(readlink "$target")" == "$REPO_DIR"* ]]; then
      rm "$target"; ok "링크 제거 $name"; removed=$((removed+1))
    elif [[ -d "$target" && -f "$target/.installed-by-cys-bookwriting-skills" ]]; then
      rm -rf "$target"; ok "복사본 제거 $name"; removed=$((removed+1))
    elif [[ -e "$target" ]]; then
      warn "$name — 이 저장소가 설치한 것이 아니라 건너뛴다"
    fi
  done
  say ""; say "제거 완료: ${removed}개. 책 원고와 설정은 그대로 두었다."
  exit 0
fi

# ── 1. 사전 점검 ────────────────────────────────────────────
say "1) 사전 점검"

command -v python3 >/dev/null 2>&1 || die "python3 가 없다. Python 3.9 이상을 먼저 설치하라."
PYV="$(python3 -c 'import sys;print("%d.%d"%sys.version_info[:2])')"
python3 - <<'PY' || die "Python 3.9 이상이 필요하다 (현재 $PYV)."
import sys
raise SystemExit(0 if sys.version_info[:2] >= (3, 9) else 1)
PY
ok "python3 $PYV"

if python3 -c 'import yaml' >/dev/null 2>&1; then
  ok "PyYAML 설치됨"
else
  warn "PyYAML 이 없다. 설치를 시도한다."
  python3 -m pip install --user pyyaml >/dev/null 2>&1 \
    && ok "PyYAML 설치 완료" \
    || die "PyYAML 설치 실패. 직접 설치하라:  python3 -m pip install --user pyyaml"
fi

# ── 2. 스킬 배치 ────────────────────────────────────────────
say ""
say "2) 스킬 배치 — $SKILLS_DIR"
mkdir -p "$SKILLS_DIR"

installed=0
skipped=0
for src in "$REPO_DIR"/skills/*/; do
  name="$(basename "$src")"
  target="$SKILLS_DIR/$name"

  if [[ -e "$target" || -L "$target" ]]; then
    if [[ "$FORCE" == "1" ]]; then
      rm -rf "$target"
    else
      warn "$name — 이미 있어 건너뛴다 (덮어쓰려면 --force)"
      skipped=$((skipped+1)); continue
    fi
  fi

  if [[ "$MODE" == "link" ]]; then
    ln -s "${src%/}" "$target"
  else
    cp -R "${src%/}" "$target"
    : > "$target/.installed-by-cys-bookwriting-skills"
  fi
  installed=$((installed+1))
done
ok "설치 ${installed}개 / 건너뜀 ${skipped}개 (${MODE} 방식)"

# ── 3. 책 프로젝트 ──────────────────────────────────────────
say ""
if [[ -n "$BOOK_ROOT" ]]; then
  say "3) 책 프로젝트 생성 — $BOOK_ROOT"
  python3 "$REPO_DIR/bin/bookwriting.py" init --root "$BOOK_ROOT"
  BOOK_ROOT="$(cd "$BOOK_ROOT" && pwd)"
else
  say "3) 책 프로젝트"
  say "   아직 만들지 않았다. 준비되면 다음을 실행하라."
  say "     python3 $REPO_DIR/bin/bookwriting.py init --root ~/my-book --title \"내 책\" --author \"내 이름\""
fi

# ── 4. 동작 확인 ────────────────────────────────────────────
say ""
say "4) 동작 확인"
if BOOKWRITING_BOOK_ROOT="${BOOK_ROOT:-$HOME/bookwriting}" \
   python3 "$REPO_DIR/bin/bookwriting.py" healthcheck >/dev/null 2>&1; then
  ok "healthcheck 통과"
elif [[ -z "$BOOK_ROOT" ]]; then
  warn "책 프로젝트가 아직 없어 일부 항목을 건너뛰었다. init 후 다시 확인하라."
else
  warn "healthcheck 미통과 — 다음으로 원인을 보라:"
  say  "     python3 $REPO_DIR/bin/bookwriting.py healthcheck"
fi

# ── 5. 마무리 안내 ──────────────────────────────────────────
say ""
say "── 설치 완료 ──────────────────────────────────────────"
say "셸 설정(~/.zshrc 또는 ~/.bashrc)에 다음을 추가해 두면 편하다."
say ""
say "  export BOOKWRITING_HOME=\"$REPO_DIR\""
if [[ -n "$BOOK_ROOT" ]]; then
  say "  export BOOKWRITING_BOOK_ROOT=\"$BOOK_ROOT\""
else
  say "  export BOOKWRITING_BOOK_ROOT=\"\$HOME/my-book\"   # 당신의 책 폴더"
fi
say "  alias bookwriting=\"python3 \$BOOKWRITING_HOME/bin/bookwriting.py\""
say ""
say "그다음 Claude Code 를 새로 열고 이렇게 물어보라."
say "  \"bookwriting-master 스킬로 내 책 작업을 시작하자\""
