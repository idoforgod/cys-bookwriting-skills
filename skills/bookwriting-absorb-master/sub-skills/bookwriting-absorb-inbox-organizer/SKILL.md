---
name: bookwriting-absorb-inbox-organizer
description: 부모 bookwriting-absorb-master의 INTERNAL sub. 처리 완료 자산을 inbox/_processed/·실패 자산을 inbox/_failed/로 결정론 이동 + 저자 묶음 대기는 inbox/ 잔류 + 통계 출력 + cycle-registry outputs 갱신. pathlib.shutil.move 결정론.
when_to_use: bookwriting-absorb-master Step 9 (Inbox Organizer 페르소나)에서 자동 호출. Route Cascade 또는 저자 묶음 응답 완료 후. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-absorb-inbox-organizer

## TLDR

부모 bookwriting-absorb-master의 마지막 sub. 처리 결과를 분기하여 등록 완료 자산은 `inbox/_processed/`로·실패 자산은 `inbox/_failed/`로·저자 묶음 대기 자산은 inbox/ 잔류시키고, 처리 통계와 cycle-registry.outputs를 결정론 갱신한다.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- Route Cascade 완료 + seed-registry/evidence-track/pending-insights 갱신 후 Step 9 자동
- 저자 묶음 응답 완료 후 Step 9 자동
- `/bookwriting-absorb inbox` 일괄 호출 종료 시점 자동

## Detailed Methodology

### 1. 결정론 chain — 분기 + 이동 + 통계

```python
import shutil
from dataclasses import dataclass
from pathlib import Path

@dataclass
class OrganizeResult:
    processed_count: int
    registered_count: int
    bundle_pending_count: int   # 저자 묶음 대기
    failed_count: int

def organize_inbox(inbox_dir: Path, results: list[dict]) -> OrganizeResult:
    """처리 결과 분기 + 파일 이동 + 통계 산출."""
    processed_dir = inbox_dir / "_processed"
    failed_dir = inbox_dir / "_failed"
    processed_dir.mkdir(exist_ok=True)
    failed_dir.mkdir(exist_ok=True)

    counts = {"processed": 0, "registered": 0, "bundle": 0, "failed": 0}

    # Step 1: 각 처리 결과 분기
    for r in results:
        src = Path(r["source_file"])
        status = r["status"]   # "registered" | "bundle_pending" | "failed"

        if status == "registered":
            # 등록 완료 → _processed/로 이동
            try:
                shutil.move(str(src), str(processed_dir / src.name))
                counts["registered"] += 1
                counts["processed"] += 1
            except OSError:
                # 이동 실패 시 warning + 원본 보존 (부모 마스터 §16)
                counts["failed"] += 1
        elif status == "bundle_pending":
            # 저자 묶음 대기 → inbox/ 잔류 (이동 X)
            counts["bundle"] += 1
        elif status == "failed":
            # 실패 → _failed/로 이동 + 저자 알림
            shutil.move(str(src), str(failed_dir / src.name))
            counts["failed"] += 1

    # Step 2: 통계 출력 (저자 화면 §9 양식)
    print(f"통계: {counts['processed']} 처리 / {counts['registered']} 등록 "
          f"/ {counts['bundle']} 묶음 대기 / {counts['failed']} 실패")

    # Step 3: cycle-registry outputs 갱신은 부모 마스터가 담당
    return OrganizeResult(**counts)
```

### 2. 명세 §출처 (SPEC: bookwriting-absorb-subs.md SUB 4)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 각 처리 결과 분기 (등록·묶음·실패) | `for r in results` + `status` 분기 |
| _processed/로 이동 | `shutil.move(...)` |
| inbox/ 잔류 (묶음 대기) | 이동 X |
| _failed/로 이동 + 저자 알림 | `shutil.move(..., failed_dir/...)` + counts["failed"] |
| Step 2: 통계 출력 (처리 N건 / 등록 N건 / 묶음 N건 / 실패 N건) | `print(f"통계: ...")` |
| Step 3: cycle-registry outputs 갱신 | 부모 마스터 위임 (`results`로 전달) |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | inbox_dir (Path) + results (list[dict] — source_file·status) |
| Output | OrganizeResult (counts) + cycle-registry.outputs 갱신 trigger |
| Dependencies | Route Cascade 또는 저자 묶음 응답 완료 |
| 후속 단계 | ② fact-anchor·③ systemlink (다음 단계 마스터) |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | pathlib.shutil 표준 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 3 Step 1:1 환원 |
| #4 저자 작가성 | 저자 묶음 대기는 inbox 잔류 — 저자 결정 보장 |
| #7 결정론 환원 | shutil.move + counts dict 100% 결정론 |

### 5. Verification (명세 §7 + 부모 §10)

- 파일 이동 정확 (등록/실패 100% 분기 정합)
- 통계 정합 (counts 합 = results 길이)
- 실패 격리 (_failed/ 디렉토리 자동 생성·이동)
- 저자 묶음 대기 파일은 *후일 추적* 가능 (inbox 잔류·trace)

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-absorb-subs.md` §SUB 4
부모 마스터 SPEC: `specs/bookwriting-absorb-master.md` §7 Step 9 + §13 페르소나 4 + §16 (이동 실패 → warning + 원본 보존)
결정론 양식: pathlib.Path + shutil.move (Python 표준)
