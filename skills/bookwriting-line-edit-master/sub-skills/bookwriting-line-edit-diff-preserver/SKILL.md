---
name: bookwriting-line-edit-diff-preserver
description: 부모 bookwriting-line-edit-master의 INTERNAL sub. 모든 line-edit 변경의 before·after diff 결정론 보존 + .before 백업 파일 (chapter <file>.md.before) + cycle-registry.outputs.line_edit_diffs 필드 + 변경 통계 (어휘·시그니처·AI 어투·문장 리듬) + 저자 후일 원복 가능 인터페이스 (`/bookwriting-line-edit revert`).
when_to_use: bookwriting-line-edit-master의 모든 sub 통과 후 마지막 자동 호출 (⑩ 마지막 sub).
disable-model-invocation: true
---

# bookwriting-line-edit-diff-preserver

## TLDR

부모 bookwriting-line-edit-master의 마지막 sub. 모든 line-edit 변경을 결정론 capture하고 .before 백업 파일 + cycle-registry.outputs.line_edit_diffs 영속 보존한다. 저자 원복 가능 (`/bookwriting-line-edit revert`).

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- 모든 line-edit sub 통과 후 마지막 발동

## Detailed Methodology

### 1. 결정론 chain — diff capture + 백업 + 통계

```python
import shutil
from pathlib import Path
from dataclasses import dataclass, field

@dataclass
class DiffPreservationResult:
    chapter_id: str
    backup_files: list[str]              # .before 백업 경로
    diff_entries: list[dict]             # cycle-registry 양식
    statistics: dict[str, int]           # 어휘·시그니처·AI 어투·문장 리듬

def preserve_diffs(
    chapter_id: str,
    chapter_dir: Path,
    vocabulary_results: list,
    signature_results: list,
    ai_tone_results: list,
    rhythm_results: list,
) -> DiffPreservationResult:
    """모든 변경 capture + 백업 + 통계."""
    # Step 1: 모든 sub의 변경 사항 capture (입력으로 받음)

    # Step 2: diff 형식 — .before 백업 파일 (chapter <file>.md.before)
    backup_files: list[str] = []
    for layer_file in ["narrative.md", "analysis.md", "implications.md"]:
        original_path = chapter_dir / layer_file
        backup_path = chapter_dir / f"{layer_file}.before"
        if original_path.exists() and not backup_path.exists():
            shutil.copy2(original_path, backup_path)
            backup_files.append(str(backup_path))

    # cycle-registry.outputs.line_edit_diffs 양식 조립
    diff_entries: list[dict] = []
    for r in vocabulary_results:
        diff_entries.append({
            "section_id": r.section_id,
            "type": "vocabulary",
            "changes": {
                "avoid_removed": r.avoid_removed,
                "foreign_replaced": r.foreign_replaced,
                "preferred_added": r.preferred_added,
            },
        })
    for r in signature_results:
        if r.patterns_used:
            diff_entries.append({
                "section_id": r.section_id,
                "type": "signature",
                "patterns": r.patterns_used,
            })
    for r in ai_tone_results:
        if r.detected_patterns:
            diff_entries.append({
                "section_id": r.section_id,
                "type": "ai_tone",
                "detected": r.detected_patterns,
                "purged_count": r.purged_count,
            })
    for r in rhythm_results:
        if r.diff_count:
            diff_entries.append({
                "section_id": r.section_id,
                "type": "rhythm",
                "max_violations": r.max_length_violations,
                "passive_ratio": r.passive_ratio,
            })

    # Step 3: 변경 통계
    stats = {
        "vocabulary_changes": sum(r.diff_count for r in vocabulary_results),
        "signature_applied": sum(1 for r in signature_results if r.patterns_used),
        "ai_tone_purged": sum(r.purged_count for r in ai_tone_results),
        "rhythm_changes": sum(r.diff_count for r in rhythm_results),
    }

    # Step 4: 저자 spot-check·원복 가능 인터페이스 — 부모 마스터가 revert 명령 지원
    return DiffPreservationResult(
        chapter_id=chapter_id,
        backup_files=backup_files,
        diff_entries=diff_entries,
        statistics=stats,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-line-edit-subs.md SUB 6)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 모든 sub의 변경 사항 capture | 4 결과 (vocab·signature·ai_tone·rhythm) 입력 |
| Step 2 .before 백업 파일 | `shutil.copy2(original, backup)` |
| Step 2 cycle-registry.outputs.line_edit_diffs 필드 | `diff_entries` 양식 |
| Step 3: 변경 통계 (어휘·시그니처·AI 어투·문장 리듬 N건) | `statistics` 4 카운트 |
| Step 4: 저자 spot-check·원복 가능 인터페이스 | 부모 마스터 revert 명령 협업 |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | chapter_id + chapter_dir + 4 sub 결과 |
| Output | DiffPreservationResult — backup_files·diff_entries·statistics |
| 후속 단계 | 저자 원복 명령 (부모 마스터) |
| Dependencies | 모든 line-edit sub 통과 후 마지막 |
| 결정론 모듈 | shutil + dict |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | shutil + dict 결정론 |
| #2 grill-me 원문 일치 | 명세 4 Step 1:1 |
| #4 저자 작가성 | 저자 원복 가능 — 저자 결정권 보장 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §6)

- diff 100% 보존 (`backup_files` + `diff_entries`)
- 저자 원복 명령 (`/bookwriting-line-edit revert`) 지원 (부모 마스터)
- 통계 정합 (statistics 4 카운트)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-line-edit-subs.md` §SUB 6
부모 마스터 SPEC: `specs/bookwriting-line-edit-master.md`
영속 자산 보호: PHASE3B_HANDOFF §8 (cycle-registry write 부모 위임)
저자 원복 명령: 부모 마스터의 `/bookwriting-line-edit revert` 지원
