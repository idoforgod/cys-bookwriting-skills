---
name: bookwriting-insight-synthesis-bundle-builder
description: 부모 bookwriting-insight-synthesis-master의 INTERNAL sub. 저자 묶음을 markdown 결정론 정돈 + ★ 추천 표시 (종합 점수 상위 2-3개) + 묶음 1 통찰 채택·묶음 2 cross-chapter 매핑·묶음 3 위반 escalation + cycle-registry D-NNN 발급·등록 + 저자 즉답 형식 `1=a,b,c / 2=skip` 지원.
when_to_use: bookwriting-insight-synthesis-master에서 voice-craft + cross-chapter-check + authority-multi-layer 통과 후 자동 호출. 저자 화면 출력 직전. 사용자 직접 호출 금지.
disable-model-invocation: true
---

# bookwriting-insight-synthesis-bundle-builder

## TLDR

부모 bookwriting-insight-synthesis-master의 저자 묶음 정돈 sub. voice-craft·cross-chapter·authority-multi-layer 통과 통찰들을 markdown 묶음 (★ 추천 + 통찰 채택 + cross-chapter + 위반 escalation)으로 결정론 조립한다. M7 D-NNN 발급 + cycle-registry pending_decisions 등록 + 저자 즉답 형식.

## Triggers

사용자 직접 trigger 차단 (disable-model-invocation: true).
부모 마스터 호출 경로:
- voice-craft + cross-chapter-check + authority-multi-layer 3 sub 통과 후 자동 (마지막 단계)
- bookwriting-master HITL Mediator 페르소나와 협업

## Detailed Methodology

### 1. 결정론 chain — markdown 조립 + D-NNN 발급

```python
from dataclasses import dataclass
from id_generator import IdGenerator   # M7

@dataclass
class BundleOutput:
    decision_id: str             # D-NNN
    markdown_text: str
    bundle_count: int            # 묶음 1·2·3 합계
    starred_insights: list[str]
    pending_decisions_entry: dict   # cycle-registry append 양식

def build_bundle(
    voice_crafted: list,
    triad_scores: list,
    cross_chapter_results: list,
    authority_results: list,
    id_gen: IdGenerator,
    chapter_id: str,
) -> BundleOutput:
    """저자 묶음 markdown 결정론 조립."""
    # Step 1: 통과 통찰들 수집 (voice·R4 통과만)
    passed_insights = []
    crafted_by_id = {vc.insight_id: vc for vc in voice_crafted}
    triad_by_id = {ts.insight_id: ts for ts in triad_scores}
    authority_by_id = {ar["insight_id"]: ar for ar in authority_results} if authority_results else {}

    for vc in voice_crafted:
        if vc.needs_bundle_escalation:
            continue
        if not authority_by_id.get(vc.insight_id, {}).get("r4_compliant", True):
            continue
        passed_insights.append(vc)

    # Step 2: ★ 추천 표시 (종합 점수 상위 2-3개)
    starred = sorted(
        passed_insights,
        key=lambda vc: triad_by_id.get(vc.insight_id).total_score if vc.insight_id in triad_by_id else 0,
        reverse=True,
    )[:3]
    starred_ids = [s.insight_id for s in starred]

    # Step 3-5: 3 묶음 markdown 조립
    lines = [f"# ⑥ insight-synthesis — {chapter_id}", ""]

    # 묶음 1: 통찰 채택 (5-7개 후보)
    lines.append("## 저자 묶음 1: 통찰 채택 (★ 추천)")
    for i, ins in enumerate(passed_insights[:7]):
        ts = triad_by_id.get(ins.insight_id)
        star = "★" if ins.insight_id in starred_ids else " "
        score_str = f"({ts.total_score:.2f}/3.0)" if ts else ""
        lines.append(f"- ({chr(ord('a')+i)}) {star} {ins.insight_id} {score_str} {ins.crafted_text}")
    lines.append("")

    # 묶음 2: cross-chapter 매핑 (해당 시)
    if cross_chapter_results:
        lines.append("## 저자 묶음 2: cross-chapter 매핑")
        for i, cc in enumerate(cross_chapter_results[:5]):
            lines.append(f"- ({chr(ord('a')+i)}) {cc['source_insight']} → {cc['target_chapter']} (관련성 {cc.get('relevance', 0):.2f})")
        lines.append("")

    # 묶음 3: 위반 escalation (voice·R4·citation 위반 발견 시)
    violations = [vc for vc in voice_crafted if vc.needs_bundle_escalation]
    r4_violations = [ar for ar in (authority_results or []) if not ar.get("r4_compliant", True)]
    if violations or r4_violations:
        lines.append("## 저자 묶음 3: 위반 escalation")
        for vc in violations:
            lines.append(f"- voice 위반: {vc.insight_id} (voice_score {vc.voice_score_after:.2f}) — {vc.bundle_reason}")
        for ar in r4_violations:
            lines.append(f"- R4 위반: {ar.get('insight_id')} — {ar.get('reason', 'single-layer authority')}")
        lines.append("")

    # 저자 즉답 형식 안내
    lines.append("---")
    lines.append("저자 응답 형식: `1=a,b,c / 2=a / 3=skip`")

    markdown_text = "\n".join(lines)

    # Step 6: cycle-registry D-NNN 등록 (부모 마스터가 yaml write)
    decision_id = id_gen.next_decision_id()   # M7 D-NNN
    pending_entry = {
        "decision_id": decision_id,
        "chapter_id": chapter_id,
        "starred_insights": starred_ids,
        "bundle_count": len(passed_insights) + len(cross_chapter_results or []) + len(violations) + len(r4_violations),
        "status": "pending",
    }

    bundle_count = len(passed_insights) + len(cross_chapter_results or []) + len(violations) + len(r4_violations)

    return BundleOutput(
        decision_id=decision_id,
        markdown_text=markdown_text,
        bundle_count=bundle_count,
        starred_insights=starred_ids,
        pending_decisions_entry=pending_entry,
    )
```

### 2. 명세 §출처 (SPEC: bookwriting-insight-synthesis-subs.md SUB 4)

| 명세 Step | 본 sub 구현 |
|---|---|
| Step 1: 통과 통찰들 수집 (voice·citation·R4) | `passed_insights` 필터 |
| Step 2: ★ 추천 표시 (종합 점수 상위 2-3개) | `sorted(..., key=total_score)[:3]` |
| Step 3: 묶음 1 통찰 채택 (5-7개 후보) | markdown 묶음 1 |
| Step 4: 묶음 2 cross-chapter 매핑 | markdown 묶음 2 |
| Step 5: 묶음 3 위반 escalation | markdown 묶음 3 |
| Step 6: cycle-registry D-NNN 등록 | M7 `id_gen.next_decision_id()` |
| Step 7: 저자 화면 출력 | `markdown_text` |

### 3. Input · Output

| 항목 | 값 |
|---|---|
| Input | voice_crafted + triad_scores + cross_chapter_results + authority_results + IdGenerator + chapter_id |
| Output | BundleOutput — D-NNN + markdown + bundle_count + starred + pending_entry |
| 후속 단계 | bookwriting-master HITL Mediator 페르소나 (저자 응답 파싱) |
| Dependencies | voice-craft + cross-chapter-check + authority-multi-layer 통과 |
| 결정론 모듈 | M7 IdGenerator (D-NNN) + str 조립 |

### 4. 저자 진북 정합

| 진북 | 정합 |
|---|---|
| #1 할루시네이션 0 | M7 + str 조립 결정론 — LLM 추정 0 |
| #2 grill-me 원문 일치 | 명세 7 Step + 3 묶음 + 응답 형식 1:1 환원 |
| #4 저자 작가성 | 저자 *즉답 가능* 형식 — 저자 결정권 보장 |
| #7 결정론 환원 | 100% 결정론 |

### 5. Verification (명세 §7)

- 묶음 markdown 형식 정합 (헤더·★·구조화 응답 형식)
- D-NNN decision_id 발급 (M7)
- cycle-registry.pending_decisions 등록 (부모 마스터 yaml write)
- 저자 즉답 가능 형식 (`1=a,b,c / 2=skip`)
- 부모 §15 G6 게이트 — decision_id 발급 + ★ 추천 ≥1개 + 최소 3 후보

## 출처

명세 1차 진실: `specs/sub-skills/bookwriting-insight-synthesis-subs.md` §SUB 4
부모 마스터 SPEC: `specs/bookwriting-insight-synthesis-master.md` §7 + §15 G6 (Bundle Generation) + bookwriting-master HITL Mediator 협업
결정론 모듈: `lib/id_generator.py` (M7)
영속 자산 보호: PHASE3B_HANDOFF §8 (cycle-registry write 부모 위임)
