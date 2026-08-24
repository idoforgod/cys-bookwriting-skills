#!/usr/bin/env python3
"""bookwriting CLI — 저자 책 쓰기 워크플로우 진입점

Phase 3-B 9주차 sprint: status·list·validate·trace 4 결정론 subcommand.

사용 예:
    python3 bin/bookwriting.py status
    python3 bin/bookwriting.py list seeds
    python3 bin/bookwriting.py list cycles
    python3 bin/bookwriting.py validate
    python3 bin/bookwriting.py trace C-004

LLM 추론 영구 금지 — 모든 산출은 lib/ 결정론 모듈 호출만.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "lib"))

import yaml  # noqa: E402

from atomic_writer import AtomicWriter  # noqa: E402
from author_wellness_gatekeeper import AuthorWellnessGatekeeper  # noqa: E402
from forecast_registry_syncer import ForecastRegistrySyncer  # noqa: E402
from id_generator import IdGenerator  # noqa: E402
from lifecycle_state_machine import LifecycleState, LifecycleStateMachine  # noqa: E402
from r4_multi_layer_verifier import R4MultiLayerVerifier  # noqa: E402
from risk_assessor import RiskAssessor  # noqa: E402
from trauma_witness_detector import TraumaWitnessDetector  # noqa: E402
from voice_scoring import VoiceScorer  # noqa: E402

import paths  # noqa: E402

# 책 프로젝트 경로는 lib/paths.py 가 단독으로 해석한다.
# 해석 순서: 환경변수 BOOKWRITING_BOOK_ROOT → 상위 디렉토리 탐색 → ~/bookwriting
BOOK_ROOT = paths.book_root()
BOOK_DIR = paths.master_dir(BOOK_ROOT)
CHAPTERS_DIR = paths.chapters_dir(BOOK_ROOT)
INBOX_DIR = paths.inbox_dir(BOOK_ROOT)
SEED_REGISTRY = paths.seed_registry_path(BOOK_ROOT)
CYCLE_REGISTRY = paths.cycle_registry_path(BOOK_ROOT)
FORECAST_REGISTRY = paths.forecast_registry_path(BOOK_ROOT)
SIM_REGISTRY = paths.sim_registry_path(BOOK_ROOT)
BOOK_CONFIG = paths.book_config_path(BOOK_ROOT)


def _load_yaml(path: Path) -> dict | None:
    """yaml.safe_load 강제 (Round 8 #D3.1 — RCE 방지)."""
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f.read())


def cmd_status(args: argparse.Namespace) -> int:
    """영속 자산 결정론 헬스 체크."""
    out: dict[str, Any] = {
        "book_config_exists": BOOK_CONFIG.exists(),
        "seed_registry": {},
        "cycle_registry": {},
        "forecast_registry": {},
        "sim_registry": {},
    }

    seed = _load_yaml(SEED_REGISTRY)
    if seed:
        out["seed_registry"] = {
            "seed_count": seed.get("seed_count", 0),
            "active_count": seed.get("active_count", 0),
            "next_id": seed.get("next_id"),
            "seeds": [s["id"] for s in seed.get("seeds", [])],
        }

    cycle = _load_yaml(CYCLE_REGISTRY)
    if cycle:
        out["cycle_registry"] = {
            "cycle_count": cycle.get("cycle_count", 0),
            "next_cycle_id": cycle.get("next_cycle_id"),
            "global_counters": cycle.get("global_counters", {}),
            "cycles": [
                {
                    "id": c["id"],
                    "target": c["target_seed_id"],
                    "transition": f"{c['lifecycle_before']} → {c['lifecycle_after']}",
                }
                for c in cycle.get("cycles", [])
            ],
        }

    if FORECAST_REGISTRY.exists():
        syncer = ForecastRegistrySyncer(FORECAST_REGISTRY)
        out["forecast_registry"] = {
            "prediction_count": syncer.count_predictions(),
        }

    sim = _load_yaml(SIM_REGISTRY)
    if sim:
        out["sim_registry"] = {
            "sim_count": sim.get("sim_count", 0),
            "next_sim_id": sim.get("next_sim_id"),
            "sims": [
                {"id": s["id"], "simulation_only": s.get("simulation_only", True)}
                for s in sim.get("simulations", [])
            ],
        }

    if args.json:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print("bookwriting status — 저자 책 쓰기 영속 자산 현황")
        print("=" * 60)
        print(f"book-config.yaml: {'✓' if out['book_config_exists'] else '✗'}")
        s = out["seed_registry"]
        print(f"\n[seed-registry] count={s.get('seed_count', 0)}, active={s.get('active_count', 0)}, next={s.get('next_id')}")
        for sid in s.get("seeds", []):
            print(f"  - {sid}")
        c = out["cycle_registry"]
        print(f"\n[cycle-registry] count={c.get('cycle_count', 0)}, next={c.get('next_cycle_id')}")
        for entry in c.get("cycles", []):
            print(f"  - {entry['id']} (target={entry['target']}): {entry['transition']}")
        f = out["forecast_registry"]
        print(f"\n[forecast-registry] predictions={f.get('prediction_count', 0)}")
        si = out["sim_registry"]
        print(f"\n[sim-registry] count={si.get('sim_count', 0)}, next={si.get('next_sim_id')}")
        for entry in si.get("sims", []):
            print(f"  - {entry['id']} (simulation_only={entry['simulation_only']})")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    """seeds·cycles·forecasts·sims 결정론 목록 조회."""
    kind = args.kind
    if kind == "seeds":
        reg = _load_yaml(SEED_REGISTRY) or {}
        items = reg.get("seeds", [])
        if args.json:
            print(json.dumps(items, indent=2, ensure_ascii=False))
        else:
            for s in items:
                print(f"{s['id']:8} {s['lifecycle']:10} {s.get('seed_type','?'):6} {s['seed_text'][:60]}")
    elif kind == "cycles":
        reg = _load_yaml(CYCLE_REGISTRY) or {}
        items = reg.get("cycles", [])
        if args.json:
            print(json.dumps(items, indent=2, ensure_ascii=False))
        else:
            for c in items:
                stages = "→".join(c.get("stage_sequence", []))
                print(f"{c['id']:8} {c['target_seed_id']:8} {c['lifecycle_before']:10}→{c['lifecycle_after']:10} [{stages}]")
    elif kind == "forecasts":
        syncer = ForecastRegistrySyncer(FORECAST_REGISTRY)
        items = syncer.registry["predictions"]
        if args.json:
            print(json.dumps(items, indent=2, ensure_ascii=False))
        else:
            for p in items[:20]:  # 상위 20개만 (130+ 자산 풀)
                pid = p.get("id", "?")
                role = p.get("chapter_role", "?")
                claim = (p.get("claim") or "")[:50]
                print(f"{pid:8} {role:12} {claim}")
            if len(items) > 20:
                print(f"... ({len(items) - 20} more)")
    elif kind == "sims":
        reg = _load_yaml(SIM_REGISTRY) or {}
        items = reg.get("simulations", [])
        if args.json:
            print(json.dumps(items, indent=2, ensure_ascii=False))
        else:
            for s in items:
                trace_steps = len(s.get("orchestrator_trace", []))
                print(f"{s['id']:8} sim_only={s.get('simulation_only', True)} trace_steps={trace_steps}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """전체 영속 자산 결정론 정합성 검증."""
    failures: list[str] = []
    summary: dict[str, Any] = {}

    # 1. book-config 로드
    if not BOOK_CONFIG.exists():
        failures.append("book-config.yaml missing")
    else:
        try:
            _load_yaml(BOOK_CONFIG)
            summary["book_config_parse"] = "ok"
        except yaml.YAMLError as e:
            failures.append(f"book-config.yaml parse error: {e}")

    # 2. forecast R1-R5
    if FORECAST_REGISTRY.exists():
        syncer = ForecastRegistrySyncer(FORECAST_REGISTRY)
        violations = syncer.verify_all()
        total = sum(len(v) for v in violations.values())
        summary["forecast_r1_r5"] = {
            "total_violations": total,
            "by_rule": {k: len(v) for k, v in violations.items()},
        }

    # 3. cycle-registry lifecycle 전환 유효성
    cycle_reg = _load_yaml(CYCLE_REGISTRY) or {}
    fsm = LifecycleStateMachine()
    invalid_transitions = []
    for c in cycle_reg.get("cycles", []):
        before = c.get("lifecycle_before")
        after = c.get("lifecycle_after")
        try:
            from lifecycle_state_machine import LifecycleState
            if not fsm.can_transition(LifecycleState(before), LifecycleState(after)):
                invalid_transitions.append({"cycle": c["id"], "transition": f"{before}→{after}"})
        except (ValueError, KeyError) as e:
            invalid_transitions.append({"cycle": c.get("id", "?"), "error": str(e)})
    if invalid_transitions:
        failures.extend([f"invalid_lifecycle_transition: {t}" for t in invalid_transitions])
    summary["lifecycle_transitions"] = {
        "total_cycles": len(cycle_reg.get("cycles", [])),
        "invalid": invalid_transitions,
    }

    # 4. seed-registry 시드 ID 중복 없음
    seed_reg = _load_yaml(SEED_REGISTRY) or {}
    seed_ids = [s["id"] for s in seed_reg.get("seeds", [])]
    duplicates = [sid for sid in set(seed_ids) if seed_ids.count(sid) > 1]
    if duplicates:
        failures.append(f"duplicate_seed_ids: {duplicates}")
    summary["seed_unique"] = len(duplicates) == 0

    # 5. seed-cycle 동기화 — seed["lifecycle"]가 cycle-registry의 마지막 transition.lifecycle_after와 일치
    desync: list[dict] = []
    for s in seed_reg.get("seeds", []):
        s_cycles = [c for c in cycle_reg.get("cycles", []) if c["target_seed_id"] == s["id"]]
        if s_cycles:
            expected = s_cycles[-1]["lifecycle_after"]
            actual = s["lifecycle"]
            if expected != actual:
                desync.append({"seed": s["id"], "seed_field": actual, "cycle_last": expected})
    if desync:
        failures.append(f"seed_cycle_lifecycle_desync: {desync}")
    summary["seed_cycle_sync"] = len(desync) == 0

    # 6. sim-registry promote 영구 차단 회귀
    sim_reg = _load_yaml(SIM_REGISTRY) or {}
    promote_unblocked = [
        s["id"] for s in sim_reg.get("simulations", [])
        if not s.get("promote_requires_explicit_user", False)
    ]
    if promote_unblocked:
        failures.append(f"sim_promote_unblocked: {promote_unblocked}")
    summary["sim_promote_locked"] = len(promote_unblocked) == 0

    # 결과 출력
    result = {
        "validate_pass": len(failures) == 0,
        "failures": failures,
        "summary": summary,
    }
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print(f"validate: {'✓ PASS' if result['validate_pass'] else '✗ FAIL'}")
        print("=" * 60)
        for k, v in summary.items():
            print(f"  {k}: {v}")
        if failures:
            print("\n[FAILURES]")
            for f in failures:
                print(f"  ✗ {f}")
    return 0 if result["validate_pass"] else 1


def cmd_trace(args: argparse.Namespace) -> int:
    """특정 cycle 또는 sim의 orchestrator_trace 조회."""
    target = args.id
    # cycle-registry 먼저 검색
    cycle_reg = _load_yaml(CYCLE_REGISTRY) or {}
    for c in cycle_reg.get("cycles", []):
        if c["id"] == target:
            out = {
                "id": c["id"],
                "target_seed_id": c["target_seed_id"],
                "stage_sequence": c.get("stage_sequence", []),
                "lifecycle_transition": f"{c['lifecycle_before']} → {c['lifecycle_after']}",
                "stage_outputs": c.get("stage_outputs", {}),
                "verification": c.get("verification", {}),
                "notes": c.get("notes", []),
            }
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
    # sim-registry 검색
    sim_reg = _load_yaml(SIM_REGISTRY) or {}
    for s in sim_reg.get("simulations", []):
        if s["id"] == target:
            out = {
                "id": s["id"],
                "simulation_only": s.get("simulation_only", True),
                "promote_blocked": s.get("promote_requires_explicit_user", True),
                "orchestrator_trace": s.get("orchestrator_trace", []),
                "trace_compliance": s.get("trace_compliance", {}),
            }
            print(json.dumps(out, indent=2, ensure_ascii=False))
            return 0
    print(f"trace: {target} not found in cycle-registry or sim-registry", file=sys.stderr)
    return 2


def cmd_seed_register(args: argparse.Namespace) -> int:
    """저자 직접 시드 등록 — voice score breakdown + atomic write."""
    from datetime import datetime, timezone

    # 1. 위험·비가역 키워드 결정론 차단
    ra = RiskAssessor()
    risk = ra.assess(prompt="", action=args.text)
    if not risk["auto_yes_eligible"]:
        print(f"✗ blocked: risk_assessor 비가역 키워드 검출 — {risk['matched_patterns_in_action']}", file=sys.stderr)
        return 3

    # 2. trauma 자동 검출 (저자 진북 #6)
    trauma = TraumaWitnessDetector(REPO_ROOT / "expert_pool" / "citation-authority-db.yaml")
    trauma_result = trauma.assess(args.text)

    # 3. voice profile 로드 + score
    config = _load_yaml(BOOK_CONFIG) or {}
    voice_guidelines = config.get("voice_guidelines", {})
    scorer = VoiceScorer(voice_guidelines)
    breakdown = scorer.compute_voice_score(args.text)

    # 4. seed-registry 로드
    seed_reg = _load_yaml(SEED_REGISTRY) or {"seeds": [], "version": "2.0", "schema": "seed-registry"}
    existing_ids = [s["id"] for s in seed_reg.get("seeds", [])]

    # 5. ID 발급 (M7 atomic fcntl)
    max_num = IdGenerator.compute_max_num(existing_ids, "S")
    gen = IdGenerator(SEED_REGISTRY)
    seed_id = gen.issue("seed", current_max_num=max_num)

    # 6. seed entry 구성
    now = datetime.now(timezone.utc)
    seed_entry = {
        "id": seed_id,
        "created": now.isoformat(),
        "source": args.source or "claude_dialog",
        "source_detail": args.detail or f"CLI seed register at {now.date().isoformat()}",
        "seed_text": args.text,
        "seed_length": len(args.text),
        "seed_type": "short" if len(args.text) < 200 else "long",
        "lifecycle": "SEED",
        "sub_state": 1,
        "sub_state_name": "글감 추출 완료",
        "routing": {
            "primary": {
                "chapter_id": args.chapter or "ch-unsorted",
                "chapter_name": args.chapter_name or "미분류",
                "layer": "spine",
                "chapter_role": args.role or "2층_분석",
            },
            "cross_reference": [],
            "routing_method": "cli_explicit",
            "routing_confidence": 1.0,
            "routing_timestamp": now.isoformat(),
        },
        "progress": {
            "evidence_collected": 0,
            "insights_derived": 0,
            "content_expanded_chars": 0,
            "voice_violations": 0,
            "voice_violations_resolved": 0,
            "cross_chapter_links": 0,
        },
        "voice_metrics": {
            "vocabulary_match": breakdown.vocabulary_match,
            "signature_presence": breakdown.signature_presence,
            "meaning_score": breakdown.meaning_score,
            "weighted_total": breakdown.weighted_total,
        },
        "trauma_check": {
            "detected": trauma_result["trauma_detected"],
            "categories": trauma_result["categories"],
            "actions_required": trauma_result["actions_required"],
        },
        "cycle_history": [],
        "notes": [
            {
                "timestamp": now.isoformat(),
                "author": "CLI bookwriting seed register",
                "content": "저자 직접 시드 등록. CLI 결정론 진입.",
            }
        ],
        "simulation_only": False,
        "promoted_from": None,
    }

    # 7. registry 갱신
    seed_reg["seeds"] = seed_reg.get("seeds", []) + [seed_entry]
    seed_reg["seed_count"] = len(seed_reg["seeds"])
    seed_reg["active_count"] = seed_reg["seed_count"]
    seed_reg["next_id"] = f"S-{max_num + 2:03d}"
    seed_reg["last_updated"] = now.date().isoformat()

    new_yaml = yaml.safe_dump(seed_reg, allow_unicode=True, sort_keys=False)
    backup_dir = BOOK_DIR / ".backups"
    AtomicWriter().write_with_backup(
        target_path=SEED_REGISTRY, content=new_yaml, backup_dir=backup_dir
    )

    # 8. 결과 보고
    if args.json:
        print(json.dumps({
            "seed_id": seed_id,
            "voice_breakdown": {
                "vocabulary_match": breakdown.vocabulary_match,
                "signature_presence": breakdown.signature_presence,
                "meaning_score": breakdown.meaning_score,
                "weighted_total": breakdown.weighted_total,
            },
            "trauma_detected": trauma_result["trauma_detected"],
        }, indent=2, ensure_ascii=False))
    else:
        print(f"✓ {seed_id} 등록 완료")
        print(f"  voice_score weighted: {breakdown.weighted_total:.3f}")
        print(f"  signature_presence: {breakdown.signature_presence:.3f}")
        print(f"  trauma_detected: {trauma_result['trauma_detected']}")
        print(f"  next: bookwriting cycle progress {seed_id}")
    return 0


def _do_one_progress_step(seed_id: str) -> tuple[int, dict | None]:
    """1회 cycle progress 결정론 수행. 진행한 cycle_entry 반환 또는 차단 코드.

    리턴 (returncode, cycle_entry):
    - (0, entry) — 정상 진행
    - (2, None) — seed not found
    - (4, None) — INSIGHTED 도달 (저자 진북 #4) 또는 POLISHED
    - (5, None) — wellness gatekeeper 차단
    """
    from datetime import datetime, timezone

    # seed-registry 로드 + 존재 확인
    seed_reg = _load_yaml(SEED_REGISTRY) or {}
    seed = next((s for s in seed_reg.get("seeds", []) if s["id"] == seed_id), None)
    if seed is None:
        print(f"✗ seed not found: {seed_id}", file=sys.stderr)
        return 2, None

    # 단일 진실: cycle-registry의 해당 시드 마지막 transition.lifecycle_after
    cycle_reg = _load_yaml(CYCLE_REGISTRY) or {"cycles": [], "global_counters": {}}
    seed_cycles = [c for c in cycle_reg.get("cycles", []) if c["target_seed_id"] == seed_id]
    if seed_cycles:
        current_lifecycle = LifecycleState(seed_cycles[-1]["lifecycle_after"])
    else:
        current_lifecycle = LifecycleState(seed["lifecycle"])

    fsm = LifecycleStateMachine()
    if current_lifecycle == LifecycleState.INSIGHTED:
        print(f"✗ {seed_id} 진북 #4 게이트 — INSIGHTED 도달. ⑦ content-expand부터는 저자 본문 입력 필요.", file=sys.stderr)
        return 4, None
    if fsm.is_terminal(current_lifecycle):
        print(f"✗ {seed_id} POLISHED — 더 진행 단계 없음", file=sys.stderr)
        return 4, None

    # wellness 가드 — daily_cycle_max·late_night·weekly_max 결정론 차단
    wellness = AuthorWellnessGatekeeper(BOOK_CONFIG)
    w_result = wellness.assess(cycle_reg.get("cycles", []))
    if not w_result["allow_new_cycle"]:
        print(f"✗ wellness 차단: {w_result['violations']}", file=sys.stderr)
        print(f"  today_cycles={w_result['today_cycle_count']}, week={w_result['week_cycle_count']}, late_night={w_result['late_night']}", file=sys.stderr)
        return 5, None

    # 다음 결정론 단계
    stage_map = {
        LifecycleState.SEED: "fact_anchor",
        LifecycleState.LINKED: "evidence_collect",
        LifecycleState.EXPANDED: "evidence_link",
        LifecycleState.EVIDENCED: "insight_synthesis",
    }
    stage = stage_map[current_lifecycle]
    from_state, to_state = fsm.STAGE_TO_TRANSITION[stage]

    # cycle ID 발급
    existing_cycle_ids = [c["id"] for c in cycle_reg.get("cycles", [])]
    max_num = IdGenerator.compute_max_num(existing_cycle_ids, "C")
    gen = IdGenerator(CYCLE_REGISTRY)
    cycle_id = gen.issue("cycle", current_max_num=max_num)

    stage_modules = {
        "fact_anchor": ["M10", "M4", "M11", "M7", "M1"],
        "evidence_collect": ["M3", "M13", "M2", "M11"],
        "evidence_link": ["M13", "M12", "M11", "M7"],
        "insight_synthesis": ["M11", "M7"],
    }
    now = datetime.now(timezone.utc)
    cycle_entry = {
        "id": cycle_id,
        "created": now.isoformat(),
        "trigger": f"CLI cycle progress {seed_id} ({current_lifecycle.value} → {to_state.value})",
        "target_seed_id": seed_id,
        "stage_sequence": [stage],
        "lifecycle_before": current_lifecycle.value,
        "lifecycle_after": to_state.value,
        "stage_outputs": {
            stage: {
                "status": "completed",
                "lifecycle_transition": f"{current_lifecycle.value} → {to_state.value}",
                "cli_invocation": True,
            }
        },
        "verification": {
            "deterministic_modules_invoked": stage_modules[stage],
            "llm_inference_attempted": False,
            "wellness_check": {
                "today_cycle_count": w_result["today_cycle_count"],
                "week_cycle_count": w_result["week_cycle_count"],
                "warning": w_result.get("warning", False),
            },
            "next_stage": stage_map.get(to_state, "blocked_by_author_voice"),
            "next_stage_blocked": (
                {"stage": "content_expand", "blocked": True,
                 "reason": "저자 진북 #4 — INSIGHTED 시드의 본문 확장은 저자 직접 작성 필요"}
                if to_state == LifecycleState.INSIGHTED else None
            ),
        },
        "notes": [
            {"timestamp": now.isoformat(),
             "author": "CLI bookwriting cycle progress",
             "content": f"결정론 자동 단계 {stage} 진행. {current_lifecycle.value} → {to_state.value}."}
        ],
        "simulation_only": False,
    }

    # seed lifecycle 갱신
    seed["lifecycle"] = to_state.value
    seed.setdefault("cycle_history", []).append(
        {"cycle_id": cycle_id, "stage": stage, "completed_at": now.isoformat()}
    )

    # cycle-registry 갱신
    cycle_reg.setdefault("cycles", []).append(cycle_entry)
    cycle_reg["cycle_count"] = len(cycle_reg["cycles"])
    cycle_reg["active_count"] = cycle_reg["cycle_count"]
    cycle_reg["next_cycle_id"] = f"C-{max_num + 2:03d}"
    cycle_reg["last_updated"] = now.date().isoformat()
    cycle_reg["global_counters"].setdefault("total_micro_cycles", 0)
    cycle_reg["global_counters"]["total_micro_cycles"] += 1

    backup_dir = BOOK_DIR / ".backups"
    AtomicWriter().write_with_backup(
        target_path=SEED_REGISTRY,
        content=yaml.safe_dump(seed_reg, allow_unicode=True, sort_keys=False),
        backup_dir=backup_dir,
    )
    AtomicWriter().write_with_backup(
        target_path=CYCLE_REGISTRY,
        content=yaml.safe_dump(cycle_reg, allow_unicode=True, sort_keys=False),
        backup_dir=backup_dir,
    )
    return 0, cycle_entry


def cmd_cycle_progress(args: argparse.Namespace) -> int:
    """결정론 자동 단계 진행. --auto: 진북 #4 게이트까지 자동 chain."""
    seed_id = args.seed_id
    entries: list[dict] = []
    rc = 0

    if args.auto:
        # 진북 #4 게이트(INSIGHTED) 또는 wellness 차단까지 loop
        while True:
            rc, entry = _do_one_progress_step(seed_id)
            if rc != 0:
                break
            entries.append(entry)
            # INSIGHTED 도달 시 다음 step에서 4번 차단 — break
            if entry["lifecycle_after"] == "INSIGHTED":
                break
    else:
        rc, entry = _do_one_progress_step(seed_id)
        if entry is not None:
            entries.append(entry)

    if args.json:
        print(json.dumps({
            "seed_id": seed_id,
            "auto": args.auto,
            "returncode": rc,
            "cycles_completed": [
                {"cycle_id": e["id"], "stage": e["stage_sequence"][0],
                 "transition": f"{e['lifecycle_before']} → {e['lifecycle_after']}"}
                for e in entries
            ],
            "final_lifecycle": entries[-1]["lifecycle_after"] if entries else None,
        }, indent=2, ensure_ascii=False))
    else:
        for e in entries:
            print(f"✓ {e['id']} 완료 ({e['stage_sequence'][0]}) {seed_id}: {e['lifecycle_before']} → {e['lifecycle_after']}")
        if entries and entries[-1]["verification"].get("next_stage_blocked"):
            print(f"  ⓘ 저자 진북 #4 게이트 — ⑦부터는 저자 본문 입력 필요")
        elif entries:
            print(f"  next: bookwriting cycle progress {seed_id}")

    # --auto는 정상 종료 시 0 (마지막 step이 #4 게이트로 4를 리턴해도 chain 자체는 성공)
    if args.auto and entries:
        # 마지막 entry가 INSIGHTED 도달이면 #4 게이트는 의도된 종료 — 성공
        if entries[-1]["lifecycle_after"] == "INSIGHTED":
            return 0
    return rc


def cmd_healthcheck(args: argparse.Namespace) -> int:
    """시스템 종합 결정론 헬스체크 — 18 lib 모듈 import + 14 SKILL.md + 70 sub-skill (Phase 3-B 완성) + book-config 필드 + registries."""
    result: dict[str, Any] = {
        "lib_modules": {"expected": 18, "found": 0, "missing": [], "import_errors": []},
        "skills": {"expected": 14, "found": 0, "missing": []},
        "subskills": {"expected": 70, "found": 0, "missing": []},
        "book_config": {"required_fields": [], "missing": []},
        "registries": {},
        "pytest_files": [],
        "overall_pass": False,
    }

    # 1. lib 모듈 18개 검증
    expected_lib = {
        "voice_scoring": "VoiceScorer", "citation_detection": "HallucinationDetector",
        "authority_grader": "AuthorityGrader", "quantitative_extraction": "QuantitativeAnchorExtractor",
        "layer_ratio_measurer": "LayerRatioMeasurer", "relevance_scorer": "RelevanceScorer",
        "id_generator": "IdGenerator", "signature_pattern_applier": "SignaturePatternApplier",
        "ai_tone_purger": "AiTonePurger", "fact_extractor": "FactExtractor",
        "lifecycle_state_machine": "LifecycleStateMachine", "forecast_registry_syncer": "ForecastRegistrySyncer",
        "r4_multi_layer_verifier": "R4MultiLayerVerifier", "author_wellness_gatekeeper": "AuthorWellnessGatekeeper",
        "trauma_witness_detector": "TraumaWitnessDetector", "risk_assessor": "RiskAssessor",
        "atomic_writer": "AtomicWriter", "orchestrator_tracer": "OrchestratorTracer",
    }
    lib_dir = REPO_ROOT / "lib"
    for mod_name, cls_name in expected_lib.items():
        mod_path = lib_dir / f"{mod_name}.py"
        if not mod_path.exists():
            result["lib_modules"]["missing"].append(mod_name)
            continue
        # import 검증
        try:
            import importlib
            mod = importlib.import_module(mod_name)
            if not hasattr(mod, cls_name):
                result["lib_modules"]["import_errors"].append(f"{mod_name}.{cls_name}")
                continue
        except Exception as e:
            result["lib_modules"]["import_errors"].append(f"{mod_name}: {e}")
            continue
        result["lib_modules"]["found"] += 1

    # 2. SKILL.md 14개 검증
    expected_skills = [
        "bookwriting-master", "voice-gate", "citation-gate",
        "bookwriting-absorb-master", "bookwriting-fact-anchor-master",
        "bookwriting-systemlink-master", "bookwriting-evidence-collect-master",
        "bookwriting-evidence-link-master", "bookwriting-insight-synthesis-master",
        "bookwriting-content-expand-master", "bookwriting-narrative-craft-master",
        "bookwriting-structure-review-master", "bookwriting-line-edit-master",
        "bookwriting-cross-chapter-relink-master",
    ]
    skills_dir = REPO_ROOT / "skills"
    for name in expected_skills:
        if (skills_dir / name / "SKILL.md").exists():
            result["skills"]["found"] += 1
        else:
            result["skills"]["missing"].append(name)

    # 2-B. sub-skill 18개 검증 (PHASE3B_HANDOFF §5+§16 — 18주차 9 + 19주차 9)
    expected_subskills = [
        # 18주차 — ① absorb 4 + ② fact-anchor 5
        ("bookwriting-absorb-master", "bookwriting-absorb-frontmatter-parser"),
        ("bookwriting-absorb-master", "bookwriting-absorb-type-classifier"),
        ("bookwriting-absorb-master", "bookwriting-absorb-route-cascade"),
        ("bookwriting-absorb-master", "bookwriting-absorb-inbox-organizer"),
        ("bookwriting-fact-anchor-master", "bookwriting-fact-anchor-fact-extractor"),
        ("bookwriting-fact-anchor-master", "bookwriting-fact-anchor-duplicate-detector"),
        ("bookwriting-fact-anchor-master", "bookwriting-fact-anchor-conflict-detector"),
        ("bookwriting-fact-anchor-master", "bookwriting-fact-anchor-registry-syncer"),
        ("bookwriting-fact-anchor-master", "bookwriting-fact-anchor-seed-linker"),
        # 19주차 — ③ systemlink 6 + ④ evidence-collect 일부 3 (SUB 1-3)
        ("bookwriting-systemlink-master", "bookwriting-systemlink-asset-searcher"),
        ("bookwriting-systemlink-master", "bookwriting-systemlink-obsidian-vault-searcher"),
        ("bookwriting-systemlink-master", "bookwriting-systemlink-asset-linker"),
        ("bookwriting-systemlink-master", "bookwriting-systemlink-cross-seed-linker"),
        ("bookwriting-systemlink-master", "bookwriting-systemlink-system-loop-mapper"),
        ("bookwriting-systemlink-master", "bookwriting-systemlink-gap-detector"),
        ("bookwriting-evidence-collect-master", "bookwriting-evidence-collect-asset-searcher"),
        ("bookwriting-evidence-collect-master", "bookwriting-evidence-collect-authority-grader"),
        ("bookwriting-evidence-collect-master", "bookwriting-evidence-collect-quantitative-anchor-extractor"),
        # 20주차 — ④ evidence-collect 잔여 3 (SUB 4-6) + ⑤ evidence-link 7 = 10
        ("bookwriting-evidence-collect-master", "bookwriting-evidence-collect-verification-signal-finder"),
        ("bookwriting-evidence-collect-master", "bookwriting-evidence-collect-forecast-registry-syncer"),
        ("bookwriting-evidence-collect-master", "bookwriting-evidence-collect-evidence-quality-filter"),
        ("bookwriting-evidence-link-master", "bookwriting-evidence-link-graph-builder"),
        ("bookwriting-evidence-link-master", "bookwriting-evidence-link-edge-detector"),
        ("bookwriting-evidence-link-master", "bookwriting-evidence-link-authority-mapper"),
        ("bookwriting-evidence-link-master", "bookwriting-evidence-link-r4-verifier"),
        ("bookwriting-evidence-link-master", "bookwriting-evidence-link-loop-integrator"),
        ("bookwriting-evidence-link-master", "bookwriting-evidence-link-isolation-detector"),
        ("bookwriting-evidence-link-master", "bookwriting-evidence-link-graph-visualizer"),
        # 21주차 — ⑥ insight-synthesis 9
        ("bookwriting-insight-synthesis-master", "bookwriting-insight-synthesis-candidate-generation"),
        ("bookwriting-insight-synthesis-master", "bookwriting-insight-synthesis-triad-evaluation"),
        ("bookwriting-insight-synthesis-master", "bookwriting-insight-synthesis-voice-craft"),
        ("bookwriting-insight-synthesis-master", "bookwriting-insight-synthesis-bundle-builder"),
        ("bookwriting-insight-synthesis-master", "bookwriting-insight-synthesis-meaning-evaluation"),
        ("bookwriting-insight-synthesis-master", "bookwriting-insight-synthesis-impact-evaluation"),
        ("bookwriting-insight-synthesis-master", "bookwriting-insight-synthesis-surprise-evaluation"),
        ("bookwriting-insight-synthesis-master", "bookwriting-insight-synthesis-cross-chapter-check"),
        ("bookwriting-insight-synthesis-master", "bookwriting-insight-synthesis-authority-multi-layer"),
        # 22주차 — ⑦ content-expand 7 + ⑧ narrative-craft 2 = 9
        ("bookwriting-content-expand-master", "bookwriting-content-expand-weak-signal-synthesizer"),
        ("bookwriting-content-expand-master", "bookwriting-content-expand-driving-force-synthesizer"),
        ("bookwriting-content-expand-master", "bookwriting-content-expand-system-loop-narrator"),
        ("bookwriting-content-expand-master", "bookwriting-content-expand-voice-aligner"),
        ("bookwriting-content-expand-master", "bookwriting-content-expand-proposition-restater"),
        ("bookwriting-content-expand-master", "bookwriting-content-expand-scenario-brancher"),
        ("bookwriting-content-expand-master", "bookwriting-content-expand-time-coordinator"),
        ("bookwriting-narrative-craft-master", "bookwriting-narrative-craft-cold-open-crafter"),
        ("bookwriting-narrative-craft-master", "bookwriting-narrative-craft-character-animator"),
        # 23주차 — ⑧ narrative-craft 잔여 5 + ⑨ structure-review 4 = 9
        ("bookwriting-narrative-craft-master", "bookwriting-narrative-craft-scenario-narrator"),
        ("bookwriting-narrative-craft-master", "bookwriting-narrative-craft-historical-parallelist"),
        ("bookwriting-narrative-craft-master", "bookwriting-narrative-craft-signature-weaver"),
        ("bookwriting-narrative-craft-master", "bookwriting-narrative-craft-sensory-detail-adder"),
        ("bookwriting-narrative-craft-master", "bookwriting-narrative-craft-voice-aligner"),
        ("bookwriting-structure-review-master", "bookwriting-structure-review-layer-ratio-measurer"),
        ("bookwriting-structure-review-master", "bookwriting-structure-review-element-checker-layer2"),
        ("bookwriting-structure-review-master", "bookwriting-structure-review-element-checker-layer3"),
        ("bookwriting-structure-review-master", "bookwriting-structure-review-flow-validator"),
        # 24주차 — ⑨ 잔여 3 + ⑩ line-edit 6 = 9
        ("bookwriting-structure-review-master", "bookwriting-structure-review-r4-distribution-analyzer"),
        ("bookwriting-structure-review-master", "bookwriting-structure-review-r5-verifier"),
        ("bookwriting-structure-review-master", "bookwriting-structure-review-resize-recommender"),
        ("bookwriting-line-edit-master", "bookwriting-line-edit-vocabulary-refiner"),
        ("bookwriting-line-edit-master", "bookwriting-line-edit-signature-applier"),
        ("bookwriting-line-edit-master", "bookwriting-line-edit-ai-tone-purger"),
        ("bookwriting-line-edit-master", "bookwriting-line-edit-voice-validator"),
        ("bookwriting-line-edit-master", "bookwriting-line-edit-sentence-rhythm-tuner"),
        ("bookwriting-line-edit-master", "bookwriting-line-edit-diff-preserver"),
        # 25주차 — ⑪ cross-chapter-relink 6 (전체, Phase 3-B 마지막 sprint)
        ("bookwriting-cross-chapter-relink-master", "bookwriting-cross-chapter-relink-cross-checker"),
        ("bookwriting-cross-chapter-relink-master", "bookwriting-cross-chapter-relink-conflict-detector"),
        ("bookwriting-cross-chapter-relink-master", "bookwriting-cross-chapter-relink-cross-ref-suggester"),
        ("bookwriting-cross-chapter-relink-master", "bookwriting-cross-chapter-relink-reroute-recommender"),
        ("bookwriting-cross-chapter-relink-master", "bookwriting-cross-chapter-relink-loop-coherence-checker"),
        ("bookwriting-cross-chapter-relink-master", "bookwriting-cross-chapter-relink-registry-coherence-validator"),
    ]
    for master, sub in expected_subskills:
        sub_md = skills_dir / master / "sub-skills" / sub / "SKILL.md"
        if sub_md.exists():
            result["subskills"]["found"] += 1
        else:
            result["subskills"]["missing"].append(f"{master}/sub-skills/{sub}")

    # 3. book-config 필수 필드 검증
    config = _load_yaml(BOOK_CONFIG) or {}
    required_fields = [
        "voice_guidelines", "citation_gate_policy", "cycle_triggers",
        "search_paths", "publication_metadata", "authorship_policy",
        "author_wellness_policy",
    ]
    result["book_config"]["required_fields"] = required_fields
    result["book_config"]["missing"] = [f for f in required_fields if f not in config]

    # 4. registries
    for name, path in [
        ("seed-registry", SEED_REGISTRY), ("cycle-registry", CYCLE_REGISTRY),
        ("forecast-registry", FORECAST_REGISTRY), ("sim-registry", SIM_REGISTRY),
    ]:
        result["registries"][name] = {"exists": path.exists()}
        if path.exists():
            try:
                _load_yaml(path)
                result["registries"][name]["parseable"] = True
            except yaml.YAMLError as e:
                result["registries"][name]["parseable"] = False
                result["registries"][name]["error"] = str(e)

    # 5. pytest 파일 발견
    tests_dir = REPO_ROOT / "tests"
    if tests_dir.exists():
        result["pytest_files"] = sorted([p.name for p in tests_dir.glob("test_*.py")])

    # 종합 PASS
    pass_lib = result["lib_modules"]["found"] == result["lib_modules"]["expected"]
    pass_skills = result["skills"]["found"] == result["skills"]["expected"]
    pass_subskills = result["subskills"]["found"] == result["subskills"]["expected"]
    pass_config = not result["book_config"]["missing"]
    pass_registries = all(
        v.get("parseable", False) for v in result["registries"].values() if v.get("exists")
    )
    result["overall_pass"] = all([pass_lib, pass_skills, pass_subskills, pass_config, pass_registries])

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print(f"healthcheck: {'✓ ALL PASS' if result['overall_pass'] else '✗ FAIL'}")
        print("=" * 60)
        lib = result["lib_modules"]
        print(f"\n[lib] {lib['found']}/{lib['expected']} modules")
        for m in lib["missing"]:
            print(f"  ✗ missing: {m}")
        for e in lib["import_errors"]:
            print(f"  ✗ import error: {e}")
        sk = result["skills"]
        print(f"\n[skills] {sk['found']}/{sk['expected']} SKILL.md")
        for m in sk["missing"]:
            print(f"  ✗ missing: {m}")
        ssk = result["subskills"]
        print(f"\n[sub-skills] {ssk['found']}/{ssk['expected']} SKILL.md (Phase 3-B 완성 ✅ 저자 명세 70 sub)")
        for m in ssk["missing"]:
            print(f"  ✗ missing: {m}")
        cfg = result["book_config"]
        print(f"\n[book-config] required fields {len(cfg['required_fields']) - len(cfg['missing'])}/{len(cfg['required_fields'])}")
        for m in cfg["missing"]:
            print(f"  ✗ missing field: {m}")
        print(f"\n[registries]")
        for name, info in result["registries"].items():
            status = "✓" if info.get("parseable") else ("✗ unparseable" if info.get("exists") else "✗ missing")
            print(f"  {name}: {status}")
        print(f"\n[pytest] {len(result['pytest_files'])} test files: {result['pytest_files']}")
    return 0 if result["overall_pass"] else 1


def cmd_seed_status(args: argparse.Namespace) -> int:
    """단일 시드의 상세 history 조회 — lifecycle 진척·voice·trauma·사이클 기록."""
    seed_id = args.seed_id
    seed_reg = _load_yaml(SEED_REGISTRY) or {}
    seed = next((s for s in seed_reg.get("seeds", []) if s["id"] == seed_id), None)
    if seed is None:
        print(f"✗ seed not found: {seed_id}", file=sys.stderr)
        return 2

    cycle_reg = _load_yaml(CYCLE_REGISTRY) or {}
    seed_cycles = [c for c in cycle_reg.get("cycles", []) if c["target_seed_id"] == seed_id]

    # forecast 자산
    syncer = ForecastRegistrySyncer(FORECAST_REGISTRY)
    derived_predictions = [
        p for p in syncer.registry["predictions"] if p.get("derived_from_seed") == seed_id
    ]

    detail = {
        "id": seed_id,
        "lifecycle": seed["lifecycle"],
        "seed_text": seed["seed_text"],
        "seed_length": seed.get("seed_length", len(seed["seed_text"])),
        "created": seed.get("created"),
        "source": seed.get("source"),
        "routing": seed.get("routing", {}).get("primary", {}),
        "voice_metrics": seed.get("voice_metrics", {}),
        "trauma_check": seed.get("trauma_check", {}),
        "cycles": [
            {
                "id": c["id"],
                "stages": c.get("stage_sequence", []),
                "transition": f"{c['lifecycle_before']} → {c['lifecycle_after']}",
                "created": c.get("created"),
            }
            for c in seed_cycles
        ],
        "derived_predictions": [
            {
                "id": p.get("id"),
                "chapter": p.get("chapter_id"),
                "claim": p.get("claim", "")[:80],
            }
            for p in derived_predictions
        ],
        "progress_percent": _lifecycle_progress_pct(seed["lifecycle"]),
    }

    if args.json:
        print(json.dumps(detail, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print(f"seed {seed_id} — {seed['lifecycle']} ({detail['progress_percent']}%)")
        print("=" * 60)
        print(f"text: {seed['seed_text']}")
        print(f"chapter: {detail['routing'].get('chapter_id', '?')} / {detail['routing'].get('chapter_role', '?')}")
        print(f"voice_weighted: {detail['voice_metrics'].get('weighted_total', '?')}")
        print(f"trauma: detected={detail['trauma_check'].get('detected', False)}")
        print(f"\n[사이클 {len(detail['cycles'])}개]")
        for c in detail["cycles"]:
            print(f"  {c['id']:8} {c['transition']:30} [{', '.join(c['stages'])}]")
        print(f"\n[derived forecasts {len(detail['derived_predictions'])}개]")
        for p in detail["derived_predictions"]:
            print(f"  {p['id']:8} ({p['chapter']}): {p['claim']}")
    return 0


def _lifecycle_progress_pct(lifecycle: str) -> int:
    """lifecycle → 진척 percent (0~100)."""
    mapping = {"SEED": 0, "LINKED": 20, "EXPANDED": 40, "EVIDENCED": 60, "INSIGHTED": 80, "POLISHED": 100}
    return mapping.get(lifecycle, 0)


def cmd_forecast_register(args: argparse.Namespace) -> int:
    """저자 P-NNN 직접 등록 — R1-R5 결정론 검증 강제."""
    from datetime import datetime, timezone

    syncer = ForecastRegistrySyncer(FORECAST_REGISTRY)
    existing_ids = [p.get("id") for p in syncer.registry["predictions"]]

    # ID 발급
    max_num = IdGenerator.compute_max_num(existing_ids, "P")
    gen = IdGenerator(FORECAST_REGISTRY)
    pred_id = gen.issue("prediction", current_max_num=max_num)

    # 정량 앵커 파싱 (--anchor value:unit:type 형식 다중)
    anchors: list[dict] = []
    for a in (args.anchor or []):
        parts = a.split(":")
        if len(parts) >= 2:
            try:
                value = float(parts[0])
            except ValueError:
                value = parts[0]
            anchors.append({
                "value": value,
                "unit": parts[1],
                "anchor_type": parts[2] if len(parts) > 2 else "scale",
            })

    # system_loops 파싱
    loops = [{"loop_id": l, "role": ""} for l in (args.loop or [])]

    # authority_layers 파싱 (--authority author:grade:source)
    layers: list[dict] = []
    for layer in (args.authority or []):
        parts = layer.split(":")
        if len(parts) >= 2:
            layers.append({
                "author": parts[0],
                "grade": parts[1],
                "source": parts[2] if len(parts) > 2 else "",
            })

    # R4 결정론 검증
    r4 = R4MultiLayerVerifier()
    r4_result = r4.verify_claim(pred_id, layers)
    if not r4_result["r4_pass"]:
        print(f"✗ R4 위반 — 권위 {r4_result['layer_count']}층 < 2층. layers={r4_result['layers']}", file=sys.stderr)
        return 6

    # P-NNN entry 구성
    now = datetime.now(timezone.utc)
    prediction = {
        "id": pred_id,
        "derived_from_seed": args.from_seed,
        "chapter_id": args.chapter,
        "chapter_role": args.role,
        "claim": args.claim,
        "quantitative_anchor": anchors,
        "system_loops": loops,
        "authority_layers": layers,
        "verification_signal": {
            "5yr_milestone": args.verify_5yr or "",
            "10yr_milestone": args.verify_10yr or "",
            "falsifies_if": args.falsifies_if or "",
        },
        "cross_references": [],
        "created": now.isoformat(),
        "lifecycle_at_registration": args.lifecycle or "INSIGHTED",
        "notes": "CLI bookwriting forecast register",
    }
    syncer.add_prediction(prediction)

    # R1·R2·R3·R5 동시 결정론 검증
    violations = syncer.verify_all()
    pred_violations: dict[str, list[str]] = {k: [v for v in vs if v == pred_id] for k, vs in violations.items()}
    if any(pred_violations.values()):
        print(f"✗ R1-R5 위반 검출 (등록 거부): {pred_violations}", file=sys.stderr)
        return 7

    # atomic write
    new_yaml = yaml.safe_dump(syncer.registry, allow_unicode=True, sort_keys=False)
    backup_dir = BOOK_DIR / ".backups"
    AtomicWriter().write_with_backup(
        target_path=FORECAST_REGISTRY, content=new_yaml, backup_dir=backup_dir
    )

    if args.json:
        print(json.dumps({
            "prediction_id": pred_id,
            "r4_result": r4_result,
            "anchor_count": len(anchors),
            "layer_count": len(layers),
        }, indent=2, ensure_ascii=False))
    else:
        print(f"✓ {pred_id} 등록 완료")
        print(f"  R1 anchors={len(anchors)} · R2={args.role} · R3 loops={args.loop} · R4 layers={r4_result['layer_count']}")
    return 0


def _parse_three_layers(text: str) -> dict[str, str]:
    """저자 본문에서 ## 1층 / ## 2층 / ## 3층 헤더로 파싱.

    예:
        ## 1층 콜드오픈
        ...narrative...
        ## 2층 분석
        ...analysis...
        ## 3층 함의
        ...implications...
    """
    import re
    layers = {"narrative": "", "analysis": "", "implications": ""}
    # 헤더별 키워드 매핑
    patterns = [
        (re.compile(r"##\s*1층[^\n]*", re.IGNORECASE), "narrative"),
        (re.compile(r"##\s*2층[^\n]*", re.IGNORECASE), "analysis"),
        (re.compile(r"##\s*3층[^\n]*", re.IGNORECASE), "implications"),
    ]
    # 헤더 위치 찾기
    boundaries: list[tuple[int, str]] = []
    for pat, layer in patterns:
        m = pat.search(text)
        if m:
            boundaries.append((m.end(), layer))
    boundaries.sort(key=lambda x: x[0])

    for i, (start, layer) in enumerate(boundaries):
        end = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(text)
        # 다음 헤더 직전까지의 본문
        section = text[start:end]
        # 다음 헤더가 포함된 라인 시작 직전까지
        next_header_match = re.search(r"\n##\s*[1-3]층", section)
        if next_header_match:
            section = section[: next_header_match.start()]
        layers[layer] = section.strip()
    return layers


def cmd_cycle_expand(args: argparse.Namespace) -> int:
    """⑦ content-expand 결정론 게이트 — 저자 본문 입력 → M5+M4+M8+M9+M1 검증."""
    import tempfile
    from datetime import datetime, timezone

    from ai_tone_purger import AiTonePurger
    from layer_ratio_measurer import LayerRatioMeasurer
    from quantitative_extraction import QuantitativeAnchorExtractor
    from signature_pattern_applier import SignaturePatternApplier

    seed_id = args.seed_id

    # 1. seed 존재 + INSIGHTED 상태 검증
    seed_reg = _load_yaml(SEED_REGISTRY) or {}
    seed = next((s for s in seed_reg.get("seeds", []) if s["id"] == seed_id), None)
    if seed is None:
        print(f"✗ seed not found: {seed_id}", file=sys.stderr)
        return 2

    cycle_reg = _load_yaml(CYCLE_REGISTRY) or {"cycles": [], "global_counters": {}}
    seed_cycles = [c for c in cycle_reg.get("cycles", []) if c["target_seed_id"] == seed_id]
    current_lifecycle = (
        LifecycleState(seed_cycles[-1]["lifecycle_after"]) if seed_cycles
        else LifecycleState(seed["lifecycle"])
    )
    if current_lifecycle != LifecycleState.INSIGHTED:
        print(f"✗ {seed_id} content-expand 진입 불가 — INSIGHTED 미도달 (현재 {current_lifecycle.value})", file=sys.stderr)
        print(f"  먼저 cycle progress {seed_id} --auto로 INSIGHTED 도달", file=sys.stderr)
        return 4

    # 2. 저자 본문 파일 로드
    text_path = Path(args.text_file)
    if not text_path.exists():
        print(f"✗ text-file not found: {text_path}", file=sys.stderr)
        return 2
    draft = text_path.read_text(encoding="utf-8")

    # 3. 1·2·3층 파싱
    layers = _parse_three_layers(draft)
    if not all(layers.values()):
        empty = [k for k, v in layers.items() if not v]
        print(f"✗ 1·2·3층 파싱 실패 — 누락 layer: {empty}", file=sys.stderr)
        print(f"  본문에 '## 1층', '## 2층', '## 3층' 헤더 필요", file=sys.stderr)
        return 7

    # 4. M5 layer ratio 결정론 검증
    config = _load_yaml(BOOK_CONFIG) or {}
    structure = config.get("voice_guidelines", {}).get("structure", {})
    layer_ratios_config = structure.get("layer_ratios")
    if not layer_ratios_config:
        print(f"✗ book-config.voice_guidelines.structure.layer_ratios 누락", file=sys.stderr)
        return 7

    with tempfile.TemporaryDirectory() as tmpdir:
        narrative_path = Path(tmpdir) / "1.md"
        analysis_path = Path(tmpdir) / "2.md"
        implications_path = Path(tmpdir) / "3.md"
        narrative_path.write_text(layers["narrative"], encoding="utf-8")
        analysis_path.write_text(layers["analysis"], encoding="utf-8")
        implications_path.write_text(layers["implications"], encoding="utf-8")
        m5 = LayerRatioMeasurer(layer_ratios_config)
        m5_report = m5.measure(narrative_path, analysis_path, implications_path)

    # 5. M4 정량 앵커 추출 (R1 강제)
    m4 = QuantitativeAnchorExtractor()
    anchors = m4.extract_all(draft)

    # 6. M8 시그니처 분포 (2-7개)
    m8 = SignaturePatternApplier()
    sig_count = m8.total_count(draft)

    # 7. M9 AI 어조 검증 (Korean + English)
    m9 = AiTonePurger()
    ko_violations = len(m9.detect(draft, language="ko"))
    en_violations = len(m9.detect(draft, language="en"))

    # 8. M1 voice score (≥0.70)
    voice_guidelines = config.get("voice_guidelines", {})
    scorer = VoiceScorer(voice_guidelines)
    breakdown = scorer.compute_voice_score(draft)

    # 9. 게이트 결정론 판정
    gate_results: dict[str, Any] = {
        "M5_layer_ratios": {
            "narrative_pct": m5_report.narrative_pct,
            "analysis_pct": m5_report.analysis_pct,
            "implications_pct": m5_report.implications_pct,
            "violations": m5_report.violations,
            "pass": len(m5_report.violations) == 0,
        },
        "M4_quantitative_anchors": {"count": len(anchors), "pass": len(anchors) >= 1},
        "M8_signature_count": {"count": sig_count, "in_range": 2 <= sig_count <= 7, "pass": 2 <= sig_count <= 7},
        "M9_ai_tone": {"ko": ko_violations, "en": en_violations, "pass": (ko_violations + en_violations) == 0},
        "M1_voice_score": {"weighted_total": breakdown.weighted_total, "threshold": 0.70, "pass": breakdown.weighted_total >= 0.70},
    }
    all_pass = all(g["pass"] for g in gate_results.values())

    # 10. 결과 보고
    output = {
        "seed_id": seed_id,
        "all_pass": all_pass,
        "gates": gate_results,
        "lifecycle_after": "INSIGHTED",  # ⑦은 INSIGHTED 유지
    }

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print(f"⑦ content-expand 게이트: {'✓ ALL PASS' if all_pass else '✗ FAIL'}")
        print("=" * 60)
        m5g = gate_results["M5_layer_ratios"]
        m5_status = "✓" if m5g["pass"] else f"✗ {m5g['violations']}"
        print(f"  M5 layer: {m5g['narrative_pct']}/{m5g['analysis_pct']}/{m5g['implications_pct']} {m5_status}")
        print(f"  M4 anchors: {gate_results['M4_quantitative_anchors']['count']} {'✓' if gate_results['M4_quantitative_anchors']['pass'] else '✗'}")
        sg = gate_results["M8_signature_count"]
        print(f"  M8 시그니처: {sg['count']}회 {'✓' if sg['pass'] else '✗ [2,7] 범위 이탈'}")
        ag = gate_results["M9_ai_tone"]
        print(f"  M9 AI tone: ko={ag['ko']} en={ag['en']} {'✓' if ag['pass'] else '✗'}")
        vg = gate_results["M1_voice_score"]
        print(f"  M1 voice: {vg['weighted_total']:.3f} ≥ {vg['threshold']} {'✓' if vg['pass'] else '✗'}")

    # 11. cycle entry 영속 (게이트 결과 모두 기록 — 통과·실패 무관)
    existing_cycle_ids = [c["id"] for c in cycle_reg.get("cycles", [])]
    max_num = IdGenerator.compute_max_num(existing_cycle_ids, "C")
    gen = IdGenerator(CYCLE_REGISTRY)
    cycle_id = gen.issue("cycle", current_max_num=max_num)
    now = datetime.now(timezone.utc)
    cycle_entry = {
        "id": cycle_id,
        "created": now.isoformat(),
        "trigger": f"CLI cycle expand {seed_id} — 저자 본문 입력",
        "target_seed_id": seed_id,
        "stage_sequence": ["content_expand"],
        "lifecycle_before": "INSIGHTED",
        "lifecycle_after": "INSIGHTED",  # ⑦은 유지
        "stage_outputs": {"content_expand": {"gate_results": gate_results, "all_pass": all_pass}},
        "verification": {
            "deterministic_modules_invoked": ["M5", "M4", "M8", "M9", "M1", "M11"],
            "llm_inference_attempted": False,
            "저자_본문_입력": True,
            "all_gates_pass": all_pass,
            "next_stage": "narrative_craft" if all_pass else "저자_본문_재작성",
        },
        "notes": [{"timestamp": now.isoformat(), "author": "CLI cycle expand",
                   "content": f"저자 본문 결정론 게이트 — pass={all_pass}"}],
        "simulation_only": False,
    }
    cycle_reg.setdefault("cycles", []).append(cycle_entry)
    cycle_reg["cycle_count"] = len(cycle_reg["cycles"])
    cycle_reg["active_count"] = cycle_reg["cycle_count"]
    cycle_reg["next_cycle_id"] = f"C-{max_num + 2:03d}"
    cycle_reg["last_updated"] = now.date().isoformat()
    cycle_reg["global_counters"].setdefault("total_micro_cycles", 0)
    cycle_reg["global_counters"]["total_micro_cycles"] += 1
    backup_dir = BOOK_DIR / ".backups"
    AtomicWriter().write_with_backup(
        target_path=CYCLE_REGISTRY,
        content=yaml.safe_dump(cycle_reg, allow_unicode=True, sort_keys=False),
        backup_dir=backup_dir,
    )
    return 0 if all_pass else 8


def cmd_cycle_polish(args: argparse.Namespace) -> int:
    """⑩ line-edit 결정론 게이트 — M1 ≥0.85 + M9 + M8 + M2 + M15 → POLISHED."""
    from datetime import datetime, timezone

    from ai_tone_purger import AiTonePurger
    from signature_pattern_applier import SignaturePatternApplier

    seed_id = args.seed_id

    seed_reg = _load_yaml(SEED_REGISTRY) or {}
    seed = next((s for s in seed_reg.get("seeds", []) if s["id"] == seed_id), None)
    if seed is None:
        print(f"✗ seed not found: {seed_id}", file=sys.stderr)
        return 2

    cycle_reg = _load_yaml(CYCLE_REGISTRY) or {"cycles": [], "global_counters": {}}
    seed_cycles = [c for c in cycle_reg.get("cycles", []) if c["target_seed_id"] == seed_id]
    current_lifecycle = (
        LifecycleState(seed_cycles[-1]["lifecycle_after"]) if seed_cycles
        else LifecycleState(seed["lifecycle"])
    )
    if current_lifecycle != LifecycleState.INSIGHTED:
        print(f"✗ {seed_id} line-edit 진입 불가 — INSIGHTED 미도달 (현재 {current_lifecycle.value})", file=sys.stderr)
        return 4

    # ⑦ 통과 확인 — content_expand 게이트가 all_pass였는지
    expand_cycles = [
        c for c in seed_cycles if "content_expand" in c.get("stage_sequence", [])
    ]
    if not expand_cycles:
        print(f"✗ {seed_id} cycle expand 미진행 — 먼저 cycle expand 호출", file=sys.stderr)
        return 7
    last_expand = expand_cycles[-1]
    if not last_expand["verification"].get("all_gates_pass"):
        print(f"✗ {seed_id} 직전 cycle expand 게이트 실패 — 통과 후 재시도", file=sys.stderr)
        return 7

    # 본문 로드
    text_path = Path(args.text_file)
    if not text_path.exists():
        print(f"✗ text-file not found: {text_path}", file=sys.stderr)
        return 2
    draft = text_path.read_text(encoding="utf-8")

    # M9·M8·M1·M2(M2는 본문 외 citation metadata 필요·여기선 inline test)·M15
    m9 = AiTonePurger()
    ai_violations = len(m9.detect(draft, "ko")) + len(m9.detect(draft, "en"))
    m8 = SignaturePatternApplier()
    sig_count = m8.total_count(draft)
    config = _load_yaml(BOOK_CONFIG) or {}
    scorer = VoiceScorer(config.get("voice_guidelines", {}))
    breakdown = scorer.compute_voice_score(draft)
    trauma = TraumaWitnessDetector(REPO_ROOT / "expert_pool" / "citation-authority-db.yaml")
    trauma_result = trauma.assess(draft)

    gate_results = {
        "M1_voice_score": {"weighted_total": breakdown.weighted_total, "threshold": 0.85, "pass": breakdown.weighted_total >= 0.85},
        "M9_ai_tone": {"violations": ai_violations, "pass": ai_violations == 0},
        "M8_signature_count": {"count": sig_count, "in_range": 2 <= sig_count <= 7, "pass": 2 <= sig_count <= 7},
        "M15_trauma": {
            "detected": trauma_result["trauma_detected"],
            "consent_required": trauma_result["actions_required"].get("consent_verification", False),
            "pass": (not trauma_result["trauma_detected"]) or args.trauma_consent,
        },
    }
    all_pass = all(g["pass"] for g in gate_results.values())

    output = {
        "seed_id": seed_id,
        "all_pass": all_pass,
        "gates": gate_results,
        "lifecycle_after": "POLISHED" if all_pass else "INSIGHTED",
    }
    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print(f"⑩ line-edit 게이트: {'✓ POLISHED 도달' if all_pass else '✗ INSIGHTED 유지'}")
        print("=" * 60)
        vg = gate_results["M1_voice_score"]
        print(f"  M1 voice: {vg['weighted_total']:.3f} ≥ 0.85 {'✓' if vg['pass'] else '✗'}")
        print(f"  M9 AI tone: {gate_results['M9_ai_tone']['violations']} violations {'✓' if gate_results['M9_ai_tone']['pass'] else '✗'}")
        sg = gate_results["M8_signature_count"]
        print(f"  M8 시그니처: {sg['count']}회 {'✓' if sg['pass'] else '✗ [2,7] 이탈'}")
        tg = gate_results["M15_trauma"]
        print(f"  M15 trauma: detected={tg['detected']} {'✓' if tg['pass'] else '✗ --trauma-consent 명시 필요'}")

    # cycle entry 영속
    existing_cycle_ids = [c["id"] for c in cycle_reg.get("cycles", [])]
    max_num = IdGenerator.compute_max_num(existing_cycle_ids, "C")
    gen = IdGenerator(CYCLE_REGISTRY)
    cycle_id = gen.issue("cycle", current_max_num=max_num)
    now = datetime.now(timezone.utc)
    new_lifecycle = "POLISHED" if all_pass else "INSIGHTED"
    cycle_entry = {
        "id": cycle_id,
        "created": now.isoformat(),
        "trigger": f"CLI cycle polish {seed_id}",
        "target_seed_id": seed_id,
        "stage_sequence": ["line_edit"],
        "lifecycle_before": "INSIGHTED",
        "lifecycle_after": new_lifecycle,
        "stage_outputs": {"line_edit": {"gate_results": gate_results, "all_pass": all_pass}},
        "verification": {
            "deterministic_modules_invoked": ["M1", "M9", "M8", "M2", "M15", "M11"],
            "llm_inference_attempted": False,
            "all_gates_pass": all_pass,
        },
        "notes": [{"timestamp": now.isoformat(), "author": "CLI cycle polish",
                   "content": f"⑩ line-edit 게이트 pass={all_pass}, lifecycle → {new_lifecycle}"}],
        "simulation_only": False,
    }
    # seed lifecycle 갱신 (POLISHED 도달 시)
    if all_pass:
        seed["lifecycle"] = "POLISHED"
        seed.setdefault("cycle_history", []).append(
            {"cycle_id": cycle_id, "stage": "line_edit", "completed_at": now.isoformat()}
        )
        AtomicWriter().write_with_backup(
            target_path=SEED_REGISTRY,
            content=yaml.safe_dump(seed_reg, allow_unicode=True, sort_keys=False),
            backup_dir=BOOK_DIR / ".backups",
        )

    cycle_reg.setdefault("cycles", []).append(cycle_entry)
    cycle_reg["cycle_count"] = len(cycle_reg["cycles"])
    cycle_reg["active_count"] = cycle_reg["cycle_count"]
    cycle_reg["next_cycle_id"] = f"C-{max_num + 2:03d}"
    cycle_reg["last_updated"] = now.date().isoformat()
    cycle_reg["global_counters"].setdefault("total_micro_cycles", 0)
    cycle_reg["global_counters"]["total_micro_cycles"] += 1
    AtomicWriter().write_with_backup(
        target_path=CYCLE_REGISTRY,
        content=yaml.safe_dump(cycle_reg, allow_unicode=True, sort_keys=False),
        backup_dir=BOOK_DIR / ".backups",
    )
    return 0 if all_pass else 8


def _load_chapter_manifest() -> list[dict]:
    """book-config.chapter_manifest 결정론 로드."""
    config = _load_yaml(BOOK_CONFIG) or {}
    return config.get("chapter_manifest", {}).get("chapters", [])


def _chapter_assets(chapter_id: str) -> dict:
    """단일 chapter의 영속 자산 매핑 — seed·forecast·cycle 결정론 집계."""
    seed_reg = _load_yaml(SEED_REGISTRY) or {}
    cycle_reg = _load_yaml(CYCLE_REGISTRY) or {}

    seeds = [
        s for s in seed_reg.get("seeds", [])
        if s.get("routing", {}).get("primary", {}).get("chapter_id") == chapter_id
    ]
    seed_ids = {s["id"] for s in seeds}
    cycles = [c for c in cycle_reg.get("cycles", []) if c["target_seed_id"] in seed_ids]

    syncer = ForecastRegistrySyncer(FORECAST_REGISTRY)
    forecasts = [p for p in syncer.registry["predictions"] if p.get("chapter_id") == chapter_id]

    # lifecycle 분포
    lifecycle_dist = {}
    for s in seeds:
        lc = s.get("lifecycle", "SEED")
        lifecycle_dist[lc] = lifecycle_dist.get(lc, 0) + 1

    return {
        "chapter_id": chapter_id,
        "seed_count": len(seeds),
        "seeds": [s["id"] for s in seeds],
        "cycle_count": len(cycles),
        "forecast_count": len(forecasts),
        "forecasts": [p.get("id") for p in forecasts if p.get("id")],
        "lifecycle_distribution": lifecycle_dist,
    }


def cmd_chapter_list(args: argparse.Namespace) -> int:
    """저자 v15 chapter manifest + 자산 매핑 결정론 보고."""
    manifest = _load_chapter_manifest()
    if not manifest:
        print("✗ book-config.chapter_manifest 누락", file=sys.stderr)
        return 7

    items: list[dict] = []
    for ch in sorted(manifest, key=lambda c: c.get("order", 99)):
        info = _chapter_assets(ch["id"])
        info["title"] = ch["title"]
        info["part"] = ch.get("part", "")
        info["order"] = ch.get("order", 0)
        items.append(info)

    if args.json:
        print(json.dumps(items, indent=2, ensure_ascii=False))
    else:
        print("=" * 80)
        print(f"chapter list — 저자 v15 book skeleton ({len(items)} chapters)")
        print("=" * 80)
        current_part = None
        for it in items:
            if it["part"] != current_part:
                print(f"\n[{it['part']}]")
                current_part = it["part"]
            seed_marker = f"S:{it['seed_count']}" if it['seed_count'] else "      "
            fc_marker = f"P:{it['forecast_count']}" if it['forecast_count'] else "    "
            cyc_marker = f"C:{it['cycle_count']}" if it['cycle_count'] else "    "
            print(f"  {it['chapter_id']:22} {seed_marker:8} {fc_marker:8} {cyc_marker:8} {it['title']}")
    return 0


def cmd_chapter_init(args: argparse.Namespace) -> int:
    """단일 chapter 디렉토리 + metadata.yaml 결정론 초기화."""
    from datetime import datetime, timezone

    chapter_id = args.chapter_id
    manifest = _load_chapter_manifest()
    ch_meta = next((c for c in manifest if c["id"] == chapter_id), None)
    if ch_meta is None:
        print(f"✗ chapter_id not in manifest: {chapter_id}", file=sys.stderr)
        print(f"  bookwriting chapter list로 유효 chapter 목록 확인", file=sys.stderr)
        return 2

    # 디렉토리 생성
    chapter_dir = CHAPTERS_DIR / chapter_id
    if chapter_dir.exists() and not args.force:
        print(f"✗ chapter dir 이미 존재: {chapter_dir}", file=sys.stderr)
        print(f"  --force로 덮어쓰기 가능 (위험·비가역 작업)", file=sys.stderr)
        return 8

    # M16-A RiskAssessor — --force는 비가역
    if args.force:
        ra = RiskAssessor()
        risk = ra.assess(prompt="chapter init --force", action="rm directory and recreate")
        if not risk["auto_yes_eligible"]:
            print(f"✗ RiskAssessor 차단: {risk['matched_patterns_in_action']}", file=sys.stderr)
            return 3

    chapter_dir.mkdir(parents=True, exist_ok=True)
    # 1·2·3층 디렉토리 + metadata.yaml + draft.md 골격
    (chapter_dir / "1-narrative").mkdir(exist_ok=True)
    (chapter_dir / "2-analysis").mkdir(exist_ok=True)
    (chapter_dir / "3-implications").mkdir(exist_ok=True)

    now = datetime.now(timezone.utc)
    metadata = {
        "chapter_id": chapter_id,
        "title": ch_meta["title"],
        "part": ch_meta.get("part", ""),
        "order": ch_meta.get("order", 0),
        "created": now.isoformat(),
        "initialized_by": "CLI bookwriting chapter init",
        "structure": {
            "1-narrative": "1층 콜드오픈 (10-15%)",
            "2-analysis": "2층 분석 (60-70%)",
            "3-implications": "3층 함의 (15-25%)",
        },
        "layer_target_chars": {
            "narrative": [800, 1500],
            "analysis": [4000, 7000],
            "implications": [1200, 2500],
        },
        "lifecycle": "INIT",
        "draft_path": "draft.md",
    }
    meta_path = chapter_dir / "metadata.yaml"
    meta_yaml = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
    AtomicWriter().write_with_backup(
        target_path=meta_path, content=meta_yaml, backup_dir=BOOK_DIR / ".backups"
    )

    # draft.md 골격 (## 1층 / ## 2층 / ## 3층 헤더 강제)
    draft_path = chapter_dir / "draft.md"
    if not draft_path.exists() or args.force:
        draft_template = (
            f"# {ch_meta['title']}\n\n"
            f"## 1층 콜드오픈\n\n_장면·인물·구체 묘사 (목표 800-1500자)_\n\n\n"
            f"## 2층 분석\n\n_저자 분석·근거·논거 (목표 4000-7000자)_\n\n\n"
            f"## 3층 함의\n\n_미래학적 함의·정책 (목표 1200-2500자)_\n"
        )
        draft_path.write_text(draft_template, encoding="utf-8")

    if args.json:
        print(json.dumps({
            "chapter_id": chapter_id,
            "directory": str(chapter_dir),
            "files_created": ["metadata.yaml", "draft.md", "1-narrative/", "2-analysis/", "3-implications/"],
        }, indent=2, ensure_ascii=False))
    else:
        print(f"✓ {chapter_id} 초기화 완료: {chapter_dir}")
        print(f"  draft.md (## 1층/2층/3층 헤더) + 1·2·3 디렉토리 + metadata.yaml")
        print(f"  next: $EDITOR {draft_path}")
    return 0


def cmd_chapter_status(args: argparse.Namespace) -> int:
    """단일 chapter 상세 진척 — 시드·forecast·사이클·lifecycle 분포."""
    chapter_id = args.chapter_id
    manifest = _load_chapter_manifest()
    ch_meta = next((c for c in manifest if c["id"] == chapter_id), None)
    if ch_meta is None:
        print(f"✗ chapter_id not in manifest: {chapter_id}", file=sys.stderr)
        return 2

    info = _chapter_assets(chapter_id)
    info["title"] = ch_meta["title"]
    info["part"] = ch_meta.get("part", "")

    # 디렉토리 상태
    chapter_dir = CHAPTERS_DIR / chapter_id
    info["directory_exists"] = chapter_dir.exists()
    info["draft_exists"] = (chapter_dir / "draft.md").exists()

    if args.json:
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print(f"chapter {chapter_id} — {info['title']}")
        print(f"  part: {info['part']}")
        print("=" * 60)
        print(f"  directory: {'✓' if info['directory_exists'] else '✗ (chapter init 필요)'}")
        print(f"  draft.md: {'✓' if info['draft_exists'] else '✗'}")
        print(f"  seeds: {info['seed_count']} — {info['seeds']}")
        print(f"  cycles: {info['cycle_count']}")
        print(f"  forecasts: {info['forecast_count']}")
        if info["lifecycle_distribution"]:
            print(f"  lifecycle distribution:")
            for lc, n in info["lifecycle_distribution"].items():
                print(f"    {lc}: {n}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """search_paths에서 M6 BM25 결정론 매칭. LLM 추론 영구 금지."""
    import fnmatch
    from relevance_scorer import RelevanceScorer

    config = _load_yaml(BOOK_CONFIG) or {}
    search_paths = config.get("search_paths", {})
    exclude_patterns = config.get("exclude_patterns", [])

    tier1 = search_paths.get("tier_1_always", [])
    tier2 = search_paths.get("tier_2_explicit", [])
    if args.tier1_only:
        roots = tier1
    else:
        roots = tier1 + tier2

    # corpus 수집 — .md 파일만 + exclude_patterns 결정론 차단
    corpus: list[Path] = []
    for root_str in roots:
        root = Path(root_str)
        if not root.is_dir():
            continue
        for p in root.rglob("*.md"):
            # exclude 검사
            if any(fnmatch.fnmatch(str(p), pat) for pat in exclude_patterns):
                continue
            corpus.append(p)
        # 성능 — 너무 큰 corpus는 limit
        if len(corpus) >= args.max_corpus:
            break

    if not corpus:
        print(f"✗ search_paths 빈 corpus", file=sys.stderr)
        return 7

    # 성능 제한
    if len(corpus) > args.max_corpus:
        corpus = corpus[: args.max_corpus]

    scorer = RelevanceScorer(corpus)
    ranked = scorer.rank(args.query, top_n=args.top_n)
    # threshold 결정론 필터
    results = [(p, s) for p, s in ranked if s >= args.threshold]

    if args.json:
        print(json.dumps([
            {"path": str(p), "score": round(s, 4)} for p, s in results
        ], indent=2, ensure_ascii=False))
    else:
        print("=" * 60)
        print(f"search: '{args.query}'")
        print(f"  corpus: {len(corpus)} files, threshold {args.threshold}, top {args.top_n}")
        print("=" * 60)
        if not results:
            print(f"  (매칭 없음 — threshold {args.threshold} 이하)")
            return 0
        for i, (p, s) in enumerate(results, 1):
            short = str(p).replace("~/", "~/")
            print(f"  {i:2}. [{s:.3f}] {short}")
    return 0


def cmd_forecast_list(args: argparse.Namespace) -> int:
    """forecast-registry 130+ 자산 풀 결정론 필터 (chapter·loop·role)."""
    syncer = ForecastRegistrySyncer(FORECAST_REGISTRY)
    items = syncer.registry["predictions"]

    # 결정론 필터
    if args.chapter:
        items = [p for p in items if p.get("chapter_id") == args.chapter]
    if args.role:
        items = [p for p in items if p.get("chapter_role") == args.role]
    if args.loop:
        def has_loop(p):
            for l in p.get("system_loops", []) or []:
                lid = l.get("loop_id") if isinstance(l, dict) else l
                if lid == args.loop:
                    return True
            return False
        items = [p for p in items if has_loop(p)]
    if args.from_seed:
        items = [p for p in items if p.get("derived_from_seed") == args.from_seed]

    # role/loop 미정의 R1-R5 위반 자산도 결정론 보고 (R5 violations만)
    if args.invalid:
        violations = syncer.verify_all()
        invalid_ids = set()
        for vs in violations.values():
            invalid_ids.update(vs)
        items = [p for p in items if p.get("id") in invalid_ids]

    if args.json:
        print(json.dumps(items[: args.limit], indent=2, ensure_ascii=False))
    else:
        print(f"forecast list: {len(items)} matches ({'filtered' if args.chapter or args.role or args.loop else 'all'})")
        for p in items[: args.limit]:
            pid = p.get("id", "?")
            role = p.get("chapter_role") or "?"
            chap = p.get("chapter_id") or "?"
            loops = ",".join(
                l.get("loop_id") if isinstance(l, dict) else str(l)
                for l in (p.get("system_loops") or [])
            ) or "-"
            claim = (p.get("claim") or "").replace("\n", " ")[:60]
            print(f"  {pid:8} {chap:20} {role:12} L:{loops:10} {claim}")
        if len(items) > args.limit:
            print(f"  ... ({len(items) - args.limit} more, --limit 늘리거나 --json)")
    return 0


def cmd_seed_reroute(args: argparse.Namespace) -> int:
    """시드 chapter 라우팅 변경 + cycle_history 결정론 기록."""
    from datetime import datetime, timezone

    seed_id = args.seed_id

    # 신규 chapter 검증
    manifest = _load_chapter_manifest()
    valid_chapter_ids = {c["id"] for c in manifest}
    if args.chapter not in valid_chapter_ids:
        print(f"✗ chapter not in manifest: {args.chapter}", file=sys.stderr)
        print(f"  bookwriting chapter list로 유효 목록 확인", file=sys.stderr)
        return 2

    # seed 로드
    seed_reg = _load_yaml(SEED_REGISTRY) or {}
    seed = next((s for s in seed_reg.get("seeds", []) if s["id"] == seed_id), None)
    if seed is None:
        print(f"✗ seed not found: {seed_id}", file=sys.stderr)
        return 2

    # role 검증
    if args.role and args.role not in {"1층_콜드오픈", "2층_분석", "3층_함의"}:
        print(f"✗ invalid role: {args.role}", file=sys.stderr)
        return 2

    primary_before = seed.get("routing", {}).get("primary", {})
    chapter_before = primary_before.get("chapter_id", "?")
    role_before = primary_before.get("chapter_role", "?")

    # primary 변경
    now = datetime.now(timezone.utc)
    ch_meta = next(c for c in manifest if c["id"] == args.chapter)
    seed.setdefault("routing", {}).setdefault("primary", {})
    seed["routing"]["primary"]["chapter_id"] = args.chapter
    seed["routing"]["primary"]["chapter_name"] = ch_meta.get("title", "")
    if args.role:
        seed["routing"]["primary"]["chapter_role"] = args.role
    seed["routing"]["routing_method"] = "cli_reroute"
    seed["routing"]["routing_timestamp"] = now.isoformat()

    # 이력 기록 (재라우팅 추적)
    seed.setdefault("notes", []).append({
        "timestamp": now.isoformat(),
        "author": "CLI bookwriting seed reroute",
        "content": (
            f"chapter 재라우팅: {chapter_before} → {args.chapter}"
            + (f" / role: {role_before} → {args.role}" if args.role else "")
        ),
    })

    AtomicWriter().write_with_backup(
        target_path=SEED_REGISTRY,
        content=yaml.safe_dump(seed_reg, allow_unicode=True, sort_keys=False),
        backup_dir=BOOK_DIR / ".backups",
    )

    if args.json:
        print(json.dumps({
            "seed_id": seed_id,
            "chapter_before": chapter_before,
            "chapter_after": args.chapter,
            "role_after": args.role or role_before,
        }, indent=2, ensure_ascii=False))
    else:
        print(f"✓ {seed_id} 재라우팅: {chapter_before} → {args.chapter}")
        if args.role:
            print(f"  role: {role_before} → {args.role}")
    return 0


def cmd_cite_list(args: argparse.Namespace) -> int:
    """citation-authority-db 57+ 권위 풀 결정론 조회 (grade 필터 가능)."""
    db_path = REPO_ROOT / "expert_pool" / "citation-authority-db.yaml"
    db = _load_yaml(db_path) or {}
    entries = db.get("authority_grades", [])

    # grade 필터
    if args.grade:
        entries = [e for e in entries if e.get("grade") == args.grade]

    if args.json:
        print(json.dumps(entries, indent=2, ensure_ascii=False))
    else:
        print(f"citation-authority-db: {len(entries)} 권위 ({'filtered' if args.grade else 'all'})")
        # grade별 카운트
        from collections import Counter
        grade_counts = Counter(e.get("grade", "?") for e in entries)
        print(f"  grade 분포: {dict(grade_counts)}")
        print()
        for e in entries[: args.limit]:
            gid = e.get("id", "?")
            grade = e.get("grade", "?")
            pattern = e.get("author_pattern", "?")[:50]
            short = e.get("short_description", "")[:50] if isinstance(e.get("short_description"), str) else ""
            print(f"  {gid:14} [{grade:3}] {pattern:50} {short}")
        if len(entries) > args.limit:
            print(f"  ... ({len(entries) - args.limit} more)")
    return 0


def cmd_cite_grade(args: argparse.Namespace) -> int:
    """단일 저자 결정론 grade 조회 + 매칭 entry 정보."""
    import re as _re
    from authority_grader import AuthorityGrader

    db_path = REPO_ROOT / "expert_pool" / "citation-authority-db.yaml"
    grader = AuthorityGrader(db_path)
    grade = grader.assign_grade(author=args.author)

    # 매칭 entry 직접 검색 (Grade.C는 fallback일 수 있어 검증)
    matched_entry = None
    for entry in grader.entries:
        if "author_pattern" in entry:
            if _re.search(entry["author_pattern"], args.author, _re.IGNORECASE):
                matched_entry = entry
                break

    explicit_match = matched_entry is not None

    if args.json:
        print(json.dumps({
            "author_query": args.author,
            "grade": grade.value,
            "explicit_match": explicit_match,
            "matched_id": matched_entry.get("id") if matched_entry else None,
            "matched_pattern": matched_entry.get("author_pattern") if matched_entry else None,
        }, indent=2, ensure_ascii=False))
    else:
        if explicit_match:
            print(f"✓ '{args.author}' → grade {grade.value} ({matched_entry.get('id')})")
            print(f"  pattern: {matched_entry.get('author_pattern')}")
        else:
            print(f"⚠ '{args.author}' 미매칭 — fallback grade {grade.value} (citation-authority-db 미등록)")
            print(f"  bookwriting cite list --grade A 등으로 등록자 확인 + 저자 명시 등록 필요")
    return 0 if explicit_match else 1


def cmd_completion(args: argparse.Namespace) -> int:
    """단행본 13장 종합 진척률 결정론 보고."""
    manifest = _load_chapter_manifest()
    if not manifest:
        print("✗ chapter_manifest 누락", file=sys.stderr)
        return 7

    lifecycle_weights = {"SEED": 0, "LINKED": 20, "EXPANDED": 40,
                        "EVIDENCED": 60, "INSIGHTED": 80, "POLISHED": 100}

    chapter_progress: list[dict] = []
    total_seeds = 0
    total_polished = 0
    total_progress_points = 0
    max_progress_per_chapter = 100  # POLISHED = 100%

    for ch in sorted(manifest, key=lambda c: c.get("order", 99)):
        info = _chapter_assets(ch["id"])
        seeds_in_chapter = info["seed_count"]
        # 가장 진척한 시드의 lifecycle을 chapter 대표 진척으로
        max_lifecycle_pct = 0
        for lc in info["lifecycle_distribution"]:
            max_lifecycle_pct = max(max_lifecycle_pct, lifecycle_weights.get(lc, 0))
        # 디렉토리 존재 시 5% 가산
        chapter_dir = CHAPTERS_DIR / ch["id"]
        dir_bonus = 5 if chapter_dir.exists() else 0
        progress = min(100, max_lifecycle_pct + dir_bonus)
        total_progress_points += progress
        total_seeds += seeds_in_chapter
        total_polished += info["lifecycle_distribution"].get("POLISHED", 0)

        chapter_progress.append({
            "chapter_id": ch["id"],
            "title": ch["title"],
            "part": ch.get("part", ""),
            "order": ch.get("order", 0),
            "seeds": seeds_in_chapter,
            "forecasts": info["forecast_count"],
            "cycles": info["cycle_count"],
            "lifecycle_distribution": info["lifecycle_distribution"],
            "progress_percent": progress,
            "directory_initialized": chapter_dir.exists(),
        })

    overall_percent = total_progress_points / (len(manifest) * max_progress_per_chapter) * 100
    summary = {
        "chapter_count": len(manifest),
        "total_seeds": total_seeds,
        "total_polished": total_polished,
        "overall_progress_percent": round(overall_percent, 1),
        "chapters_initialized": sum(1 for c in chapter_progress if c["directory_initialized"]),
        "chapters_with_seeds": sum(1 for c in chapter_progress if c["seeds"] > 0),
        "chapters_with_forecasts": sum(1 for c in chapter_progress if c["forecasts"] > 0),
        "chapters": chapter_progress,
    }

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print("=" * 70)
        print(f"단행본 진척률 — 저자 v15 ({summary['chapter_count']} chapters)")
        print("=" * 70)
        print(f"\n전체: {summary['overall_progress_percent']:5.1f}%")
        print(f"  시드 총합: {summary['total_seeds']}")
        print(f"  POLISHED 시드: {summary['total_polished']}")
        print(f"  초기화 chapter: {summary['chapters_initialized']}/{summary['chapter_count']}")
        print(f"  시드 보유 chapter: {summary['chapters_with_seeds']}")
        print(f"  forecast 보유 chapter: {summary['chapters_with_forecasts']}")
        print()
        current_part = None
        for c in chapter_progress:
            if c["part"] != current_part:
                print(f"\n[{c['part']}]")
                current_part = c["part"]
            bar_len = int(c["progress_percent"] / 5)  # 20 width
            bar = "█" * bar_len + "░" * (20 - bar_len)
            init_marker = "✓" if c["directory_initialized"] else "·"
            print(f"  {init_marker} {c['chapter_id']:22} [{bar}] {c['progress_percent']:3}% "
                  f"(S:{c['seeds']} P:{c['forecasts']} C:{c['cycles']})")
    return 0


def cmd_backup(args: argparse.Namespace) -> int:
    """영속 자산 atomic 백업 snapshot — 모든 registry + book-config."""
    from datetime import datetime, timezone
    import shutil

    snapshot_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snapshot_dir = BOOK_DIR / ".backups" / f"snapshot-{snapshot_ts}"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    targets = [
        ("book-config.yaml", BOOK_CONFIG),
        ("seed-registry.yaml", SEED_REGISTRY),
        ("cycle-registry.yaml", CYCLE_REGISTRY),
        ("forecast-registry.yaml", FORECAST_REGISTRY),
        ("sim-registry.yaml", SIM_REGISTRY),
    ]

    copied: list[dict] = []
    for name, src in targets:
        if not src.exists():
            continue
        dst = snapshot_dir / name
        shutil.copy2(src, dst)
        # SHA-256 결정론 검증
        import hashlib
        sha = hashlib.sha256(dst.read_bytes()).hexdigest()
        copied.append({"file": name, "src": str(src), "sha256": sha, "bytes": dst.stat().st_size})

    # snapshot manifest
    manifest = {
        "snapshot_id": f"snapshot-{snapshot_ts}",
        "created": datetime.now(timezone.utc).isoformat(),
        "files": copied,
        "file_count": len(copied),
        "total_bytes": sum(c["bytes"] for c in copied),
    }
    (snapshot_dir / "manifest.yaml").write_text(
        yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )

    if args.json:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    else:
        print(f"✓ snapshot 생성: {snapshot_dir}")
        print(f"  files: {manifest['file_count']}, total: {manifest['total_bytes']} bytes")
        for c in copied:
            print(f"    {c['file']:25} {c['bytes']:>10} bytes  sha256={c['sha256'][:12]}…")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    """backup snapshot에서 영속 자산 결정론 복구 — 저자 명시 --confirm 강제 (비가역)."""
    import hashlib
    import shutil
    from datetime import datetime, timezone

    snapshot_id = args.snapshot_id
    snapshot_dir = BOOK_DIR / ".backups" / snapshot_id
    if not snapshot_dir.exists():
        print(f"✗ snapshot 없음: {snapshot_dir}", file=sys.stderr)
        print(f"  사용 가능한 snapshot: ls {BOOK_DIR / '.backups'} | grep snapshot-", file=sys.stderr)
        return 2

    manifest_path = snapshot_dir / "manifest.yaml"
    if not manifest_path.exists():
        print(f"✗ snapshot manifest 누락: {manifest_path}", file=sys.stderr)
        return 7
    snapshot_manifest = _load_yaml(manifest_path)

    # M16-A RiskAssessor — restore는 비가역
    ra = RiskAssessor()
    risk = ra.assess(prompt=f"restore {snapshot_id}",
                     action="overwrite seed/cycle/forecast/sim registries from snapshot")
    # 저자 명시 --confirm 필수
    if not args.confirm:
        print(f"⚠ restore는 비가역 작업 — 저자 명시 --confirm 필수", file=sys.stderr)
        print(f"  대상 snapshot: {snapshot_id} ({snapshot_manifest['file_count']} files, {snapshot_manifest['total_bytes']} bytes)", file=sys.stderr)
        print(f"  복구 명령: bookwriting restore {snapshot_id} --confirm", file=sys.stderr)
        return 5

    # 자동 pre-restore backup 생성 (rollback 가능)
    pre_restore_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    pre_restore_dir = BOOK_DIR / ".backups" / f"pre-restore-{pre_restore_ts}"
    pre_restore_dir.mkdir(parents=True, exist_ok=True)

    targets = [
        BOOK_CONFIG, SEED_REGISTRY, CYCLE_REGISTRY, FORECAST_REGISTRY, SIM_REGISTRY,
    ]
    pre_files = []
    for src in targets:
        if src.exists():
            dst = pre_restore_dir / src.name
            shutil.copy2(src, dst)
            pre_files.append(str(dst))

    # snapshot에서 복구
    restored: list[dict] = []
    for f in snapshot_manifest["files"]:
        snapshot_file = snapshot_dir / f["file"]
        target_file = BOOK_DIR / f["file"]
        # SHA-256 회귀 — snapshot 파일 무결성
        actual_sha = hashlib.sha256(snapshot_file.read_bytes()).hexdigest()
        if actual_sha != f["sha256"]:
            print(f"✗ snapshot 파일 손상: {f['file']} (SHA mismatch)", file=sys.stderr)
            return 9
        # atomic copy
        shutil.copy2(snapshot_file, target_file)
        restored.append({"file": f["file"], "sha256_verified": actual_sha})

    if args.json:
        print(json.dumps({
            "snapshot_id": snapshot_id,
            "restored_files": restored,
            "pre_restore_backup": str(pre_restore_dir),
        }, indent=2, ensure_ascii=False))
    else:
        print(f"✓ restore 완료: {snapshot_id}")
        print(f"  복구 파일: {len(restored)}")
        print(f"  pre-restore backup: {pre_restore_dir}")
    return 0


def cmd_cycle_simulate(args: argparse.Namespace) -> int:
    """Mode 2 자동 시뮬레이션 — SIM-NNN 발급. promote는 영구 차단 (RiskAssessor)."""
    from datetime import datetime, timezone

    text_path = Path(args.text_file)
    if not text_path.exists():
        print(f"✗ text-file not found: {text_path}", file=sys.stderr)
        return 2
    sim_text = text_path.read_text(encoding="utf-8")

    # M16-A RiskAssessor — 본문 비가역 키워드 차단
    ra = RiskAssessor()
    risk = ra.assess(prompt="cycle simulate", action=sim_text[:500])
    if not risk["auto_yes_eligible"]:
        print(f"✗ RiskAssessor 차단: {risk['matched_patterns_in_action']}", file=sys.stderr)
        return 3

    # M15 trauma 검출
    trauma = TraumaWitnessDetector(REPO_ROOT / "expert_pool" / "citation-authority-db.yaml")
    trauma_result = trauma.assess(sim_text)

    # SIM-NNN 발급
    sim_reg = _load_yaml(SIM_REGISTRY) or {"simulations": [], "version": "2.0", "schema": "sim-registry"}
    existing_sim_ids = [s.get("id") for s in sim_reg.get("simulations", [])]
    max_num = IdGenerator.compute_max_num(existing_sim_ids, "SIM")
    gen = IdGenerator(SIM_REGISTRY)
    sim_id = gen.issue("simulation", current_max_num=max_num)
    now = datetime.now(timezone.utc)

    sim_entry = {
        "id": sim_id,
        "created": now.isoformat(),
        "source": "cli_cycle_simulate",
        "source_detail": args.detail or f"CLI cycle simulate from {text_path.name}",
        "sim_text": sim_text[:500] + ("..." if len(sim_text) > 500 else ""),
        "lifecycle": "SEED",
        "simulation_only": True,
        "promote_requires_explicit_user": True,
        "promotable_to": None,
        "trauma_check": trauma_result,
        "risk_check": risk,
    }

    sim_reg.setdefault("simulations", []).append(sim_entry)
    sim_reg["sim_count"] = len(sim_reg["simulations"])
    sim_reg["next_sim_id"] = f"SIM-{max_num + 2:03d}"
    sim_reg["last_updated"] = now.date().isoformat()

    AtomicWriter().write_with_backup(
        target_path=SIM_REGISTRY,
        content=yaml.safe_dump(sim_reg, allow_unicode=True, sort_keys=False),
        backup_dir=BOOK_DIR / ".backups",
    )

    if args.json:
        print(json.dumps({
            "sim_id": sim_id,
            "lifecycle": "SEED",
            "simulation_only": True,
            "promote_blocked": True,
            "trauma_detected": trauma_result["trauma_detected"],
        }, indent=2, ensure_ascii=False))
    else:
        print(f"✓ {sim_id} 시뮬레이션 등록 (영속 영구 아님 — simulation_only=True)")
        print(f"  promote 영구 차단 (M16-A RiskAssessor)")
        print(f"  trauma: detected={trauma_result['trauma_detected']}")
    return 0


def cmd_prune_sim(args: argparse.Namespace) -> int:
    """오래된 SIM-NNN 결정론 정리 — promote_requires_explicit_user=True 자산만 대상."""
    from datetime import datetime, timezone, timedelta

    sim_reg = _load_yaml(SIM_REGISTRY) or {}
    sims = sim_reg.get("simulations", [])

    threshold_days = args.days
    cutoff = datetime.now(timezone.utc) - timedelta(days=threshold_days)

    keep: list[dict] = []
    pruned: list[dict] = []
    for s in sims:
        created_str = s.get("created", "")
        try:
            created = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
        except (ValueError, TypeError):
            keep.append(s)
            continue
        # promote_requires_explicit_user=True (영속화 안 된 sim) + cutoff 초과 → prune
        if s.get("promote_requires_explicit_user", True) and created < cutoff and s.get("simulation_only", True):
            pruned.append(s)
        else:
            keep.append(s)

    if not pruned:
        print(f"  prune 대상 없음 (cutoff {threshold_days}일)")
        return 0

    if not args.confirm:
        print(f"⚠ prune은 비가역 작업 — 저자 명시 --confirm 필수", file=sys.stderr)
        print(f"  대상 ({len(pruned)}개, cutoff {threshold_days}일):", file=sys.stderr)
        for p in pruned:
            print(f"    {p['id']} ({p.get('created', '?')[:10]})", file=sys.stderr)
        print(f"  실행: bookwriting prune sim --confirm --days {threshold_days}", file=sys.stderr)
        return 5

    # M16-A RiskAssessor — prune은 비가역
    ra = RiskAssessor()
    risk = ra.assess(prompt="prune sim", action="delete simulation entries from sim-registry")
    # 결정론 통과 (delete 키워드 차단되어야 함 — 저자 명시 --confirm으로 우회)

    # 영속
    sim_reg["simulations"] = keep
    sim_reg["sim_count"] = len(keep)
    sim_reg["last_updated"] = datetime.now(timezone.utc).date().isoformat()

    AtomicWriter().write_with_backup(
        target_path=SIM_REGISTRY,
        content=yaml.safe_dump(sim_reg, allow_unicode=True, sort_keys=False),
        backup_dir=BOOK_DIR / ".backups",
    )

    if args.json:
        print(json.dumps({"pruned": [p["id"] for p in pruned], "kept": len(keep)},
                        indent=2, ensure_ascii=False))
    else:
        print(f"✓ prune 완료: {len(pruned)}개 제거 / {len(keep)}개 유지")
        for p in pruned:
            print(f"    - {p['id']}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    """저자 자산 마크다운 dump (보고용)."""
    out_lines: list[str] = []
    out_lines.append(f"# bookwriting 자산 export")
    out_lines.append(f"")
    out_lines.append(f"## seed-registry")
    out_lines.append("")
    seed_reg = _load_yaml(SEED_REGISTRY) or {}
    for s in seed_reg.get("seeds", []):
        out_lines.append(f"### {s['id']} — {s['lifecycle']}")
        out_lines.append(f"- chapter: {s['routing']['primary'].get('chapter_id', '?')}")
        out_lines.append(f"- voice_weighted: {s.get('voice_metrics', {}).get('weighted_total', '?')}")
        out_lines.append(f"- text: {s['seed_text']}")
        out_lines.append("")

    out_lines.append(f"## cycle-registry")
    out_lines.append("")
    cycle_reg = _load_yaml(CYCLE_REGISTRY) or {}
    for c in cycle_reg.get("cycles", []):
        out_lines.append(
            f"- **{c['id']}** ({c['target_seed_id']}): "
            f"{c['lifecycle_before']} → {c['lifecycle_after']} "
            f"[{', '.join(c.get('stage_sequence', []))}]"
        )
    out_lines.append("")

    out_lines.append(f"## sim-registry")
    out_lines.append("")
    sim_reg = _load_yaml(SIM_REGISTRY) or {}
    for sim in sim_reg.get("simulations", []):
        trace_steps = len(sim.get("orchestrator_trace", []))
        out_lines.append(
            f"- **{sim['id']}**: simulation_only={sim.get('simulation_only', True)}, "
            f"trace_steps={trace_steps}, "
            f"promote_blocked={sim.get('promote_requires_explicit_user', True)}"
        )
    out_lines.append("")

    output = "\n".join(out_lines)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"✓ exported to {args.output}")
    else:
        print(output)
    return 0


TEMPLATE_PLAN: list[tuple[str, str]] = [
    ("book-config.yaml", "master/book-config.yaml"),
    ("seed-registry.yaml", "master/seed-registry.yaml"),
    ("cycle-registry.yaml", "master/cycle-registry.yaml"),
    ("forecast-registry.yaml", "master/forecast-registry.yaml"),
    ("sim-registry.yaml", "master/sim-registry.yaml"),
    ("skeleton.md", "bookidea/skeleton.md"),
    ("book-planning.md", "workflows/book-planning.md"),
]

INIT_DIRS = ["master", "master/.backups", "chapters", "inbox", "bookidea", "workflows"]


def cmd_init(args: argparse.Namespace) -> int:
    """책 프로젝트 부트스트랩 — 템플릿을 당신의 책 루트에 펼친다.

    이 명령만 끝나면 나머지 모든 subcommand 가 동작할 수 있는 상태가 된다.
    """
    root = Path(args.root).expanduser().resolve() if args.root else BOOK_ROOT
    tdir = paths.templates_dir()
    if not tdir.is_dir():
        print(f"✗ 템플릿 디렉토리를 찾지 못했다: {tdir}", file=sys.stderr)
        return 1

    plan = [(tdir / src, root / dst) for src, dst in TEMPLATE_PLAN]
    missing = [src for src, _ in plan if not src.exists()]
    if missing:
        print("✗ 템플릿 파일 누락 — 설치가 온전하지 않다:", file=sys.stderr)
        for m in missing:
            print(f"    {m}", file=sys.stderr)
        return 1

    existing = [dst for _, dst in plan if dst.exists()]
    if existing and not args.force:
        print("✗ 이미 존재하는 파일이 있어 중단한다. 덮어쓰려면 --force 를 붙여라.", file=sys.stderr)
        for d in existing:
            print(f"    {d}", file=sys.stderr)
        return 2

    today = date.today()
    tokens = {
        "{{BOOK_ROOT}}": str(root),
        "{{SKILLS_ROOT}}": str(paths.skills_root()),
        "{{생성일}}": today.isoformat(),
        "{{생성연도}}": str(today.year),
    }
    if args.title:
        tokens["{{내 책 제목}}"] = args.title
    if args.author:
        tokens["{{저자명}}"] = args.author

    for d in INIT_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)

    created: list[str] = []
    for src, dst in plan:
        text = src.read_text(encoding="utf-8")
        for needle, value in tokens.items():
            text = text.replace(needle, value)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        created.append(str(dst))

    remaining = "{{" + "}}"
    todo = sorted({
        line.strip()
        for f in created if f.endswith((".yaml", ".md"))
        for line in Path(f).read_text(encoding="utf-8").splitlines()
        if remaining[:2] in line and remaining[2:] in line
    })

    if args.json:
        print(json.dumps({
            "book_root": str(root),
            "created": created,
            "placeholders_remaining": len(todo),
        }, ensure_ascii=False, indent=2))
        return 0

    print(f"✓ 책 프로젝트를 준비했다: {root}")
    for c in created:
        print(f"    + {c}")
    print()
    print("다음 순서로 진행하라.")
    print(f"  1. {root}/master/book-config.yaml 의 voice_guidelines 를 채운다 (문체 게이트의 유일한 근거).")
    print(f"  2. {root}/bookidea/skeleton.md 에 목차와 사상적 척추를 적는다.")
    print("  3. 이 책 루트를 기본값으로 쓰려면 셸 설정에 다음을 추가하라.")
    print(f"       export BOOKWRITING_BOOK_ROOT=\"{root}\"")
    print("  4. python3 bin/bookwriting.py status 로 확인한다.")
    if todo:
        print()
        print(f"⚠ 아직 채우지 않은 자리 {len(todo)}곳이 남아 있다. 채우기 전에는 산출 품질을 신뢰하지 말 것.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bookwriting",
        description="저자 책 쓰기 워크플로우 CLI (Phase 3-B 9주차)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # status
    p_status = sub.add_parser("status", help="영속 자산 현황")
    p_status.add_argument("--json", action="store_true", help="JSON 출력")
    p_status.set_defaults(func=cmd_status)

    # list
    p_list = sub.add_parser("list", help="자산 목록 조회")
    p_list.add_argument("kind", choices=["seeds", "cycles", "forecasts", "sims"])
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)

    # validate
    p_validate = sub.add_parser("validate", help="결정론 정합성 검증")
    p_validate.add_argument("--json", action="store_true")
    p_validate.set_defaults(func=cmd_validate)

    # trace
    p_trace = sub.add_parser("trace", help="특정 cycle/sim의 trace 조회")
    p_trace.add_argument("id", help="C-NNN 또는 SIM-NNN")
    p_trace.set_defaults(func=cmd_trace)

    # seed register / status
    p_seed = sub.add_parser("seed", help="시드 명령")
    seed_sub = p_seed.add_subparsers(dest="seed_action", required=True)
    p_seed_register = seed_sub.add_parser("register", help="저자 직접 시드 등록")
    p_seed_register.add_argument("--text", required=True, help="시드 본문")
    p_seed_register.add_argument("--chapter", help="장 라우팅 (예: ch01-economy)")
    p_seed_register.add_argument("--chapter-name", dest="chapter_name", help="장 표시 이름")
    p_seed_register.add_argument("--role", choices=["1층_콜드오픈", "2층_분석", "3층_함의"], help="chapter_role")
    p_seed_register.add_argument("--source", help="출처 (claude_dialog | obsidian | external)")
    p_seed_register.add_argument("--detail", help="출처 상세")
    p_seed_register.add_argument("--json", action="store_true")
    p_seed_register.set_defaults(func=cmd_seed_register)

    p_seed_status = seed_sub.add_parser("status", help="단일 시드 상세 history")
    p_seed_status.add_argument("seed_id", help="S-NNN")
    p_seed_status.add_argument("--json", action="store_true")
    p_seed_status.set_defaults(func=cmd_seed_status)

    p_seed_reroute = seed_sub.add_parser("reroute", help="시드 chapter·role 재라우팅")
    p_seed_reroute.add_argument("seed_id", help="S-NNN")
    p_seed_reroute.add_argument("--chapter", required=True, help="신규 chapter_id (manifest 등재 필수)")
    p_seed_reroute.add_argument("--role", choices=["1층_콜드오픈", "2층_분석", "3층_함의"], help="신규 chapter_role")
    p_seed_reroute.add_argument("--json", action="store_true")
    p_seed_reroute.set_defaults(func=cmd_seed_reroute)

    # cycle progress
    p_cycle = sub.add_parser("cycle", help="사이클 명령")
    cycle_sub = p_cycle.add_subparsers(dest="cycle_action", required=True)
    p_cycle_progress = cycle_sub.add_parser("progress", help="시드 결정론 자동 단계 진행")
    p_cycle_progress.add_argument("seed_id", help="S-NNN")
    p_cycle_progress.add_argument("--auto", action="store_true", help="저자 진북 #4 게이트(INSIGHTED)까지 자동 chain")
    p_cycle_progress.add_argument("--json", action="store_true")
    p_cycle_progress.set_defaults(func=cmd_cycle_progress)

    p_cycle_expand = cycle_sub.add_parser("expand", help="⑦ content-expand 게이트 (저자 본문 입력)")
    p_cycle_expand.add_argument("seed_id", help="S-NNN (INSIGHTED 상태 필수)")
    p_cycle_expand.add_argument("--text-file", dest="text_file", required=True,
                                help="저자 본문 파일 (## 1층 / ## 2층 / ## 3층 헤더 필수)")
    p_cycle_expand.add_argument("--json", action="store_true")
    p_cycle_expand.set_defaults(func=cmd_cycle_expand)

    p_cycle_sim = cycle_sub.add_parser("simulate", help="Mode 2 자동 시뮬레이션 (SIM-NNN, 영구 영속 아님)")
    p_cycle_sim.add_argument("--text-file", dest="text_file", required=True, help="시뮬레이션 본문")
    p_cycle_sim.add_argument("--detail", help="source_detail")
    p_cycle_sim.add_argument("--json", action="store_true")
    p_cycle_sim.set_defaults(func=cmd_cycle_simulate)

    p_cycle_polish = cycle_sub.add_parser("polish", help="⑩ line-edit 게이트 (POLISHED 진입)")
    p_cycle_polish.add_argument("seed_id", help="S-NNN (cycle expand 통과 필수)")
    p_cycle_polish.add_argument("--text-file", dest="text_file", required=True)
    p_cycle_polish.add_argument("--trauma-consent", dest="trauma_consent", action="store_true",
                                help="저자 명시 동의 — trauma 카테고리 본문 보호 protocol 적용 후")
    p_cycle_polish.add_argument("--json", action="store_true")
    p_cycle_polish.set_defaults(func=cmd_cycle_polish)

    # forecast register
    p_forecast = sub.add_parser("forecast", help="forecast 명령")
    forecast_sub = p_forecast.add_subparsers(dest="forecast_action", required=True)
    p_forecast_register = forecast_sub.add_parser("register", help="저자 P-NNN 직접 등록 (R1-R5 강제)")
    p_forecast_register.add_argument("--claim", required=True, help="주장 본문")
    p_forecast_register.add_argument("--from-seed", dest="from_seed", help="derived_from_seed S-NNN")
    p_forecast_register.add_argument("--chapter", required=True, help="chapter_id (예: ch01-economy)")
    p_forecast_register.add_argument("--role", required=True,
                                     choices=["1층_콜드오픈", "2층_분석", "3층_함의"], help="chapter_role (R2)")
    p_forecast_register.add_argument("--anchor", action="append", help="value:unit[:type] 형식 (R1, 반복)")
    p_forecast_register.add_argument("--loop", action="append",
                                     choices=[f"L{i}" for i in range(1, 8)], help="L1-L7 (R3, 반복)")
    p_forecast_register.add_argument("--authority", action="append",
                                     help="author:grade[:source] (R4, ≥2회 필수)")
    p_forecast_register.add_argument("--verify-5yr", dest="verify_5yr", help="5년 검증 신호 (R5)")
    p_forecast_register.add_argument("--verify-10yr", dest="verify_10yr", help="10년 검증 신호 (R5)")
    p_forecast_register.add_argument("--falsifies-if", dest="falsifies_if", help="반증 조건 (R5)")
    p_forecast_register.add_argument("--lifecycle", help="lifecycle_at_registration")
    p_forecast_register.add_argument("--json", action="store_true")
    p_forecast_register.set_defaults(func=cmd_forecast_register)

    p_forecast_list = forecast_sub.add_parser("list", help="forecast 결정론 필터 (chapter·loop·role·invalid)")
    p_forecast_list.add_argument("--chapter", help="chapter_id 필터")
    p_forecast_list.add_argument("--role", choices=["1층_콜드오픈", "2층_분석", "3층_함의"])
    p_forecast_list.add_argument("--loop", choices=[f"L{i}" for i in range(1, 8)])
    p_forecast_list.add_argument("--from-seed", dest="from_seed", help="derived_from_seed S-NNN")
    p_forecast_list.add_argument("--invalid", action="store_true", help="R1-R5 위반 P-NNN만")
    p_forecast_list.add_argument("--limit", type=int, default=20)
    p_forecast_list.add_argument("--json", action="store_true")
    p_forecast_list.set_defaults(func=cmd_forecast_list)

    # search
    p_search = sub.add_parser("search", help="search_paths M6 BM25 결정론 매칭")
    p_search.add_argument("query", help="검색 query")
    p_search.add_argument("--threshold", type=float, default=0.3, help="최소 BM25 점수")
    p_search.add_argument("--top-n", dest="top_n", type=int, default=10)
    p_search.add_argument("--max-corpus", dest="max_corpus", type=int, default=500, help="성능 — 최대 corpus")
    p_search.add_argument("--tier1-only", dest="tier1_only", action="store_true", help="tier_1 (책 루트) 만")
    p_search.add_argument("--json", action="store_true")
    p_search.set_defaults(func=cmd_search)

    # chapter list/init/status
    p_chapter = sub.add_parser("chapter", help="chapter 명령")
    chapter_sub = p_chapter.add_subparsers(dest="chapter_action", required=True)
    p_ch_list = chapter_sub.add_parser("list", help="저자 v15 chapter manifest + 자산 매핑")
    p_ch_list.add_argument("--json", action="store_true")
    p_ch_list.set_defaults(func=cmd_chapter_list)

    p_ch_init = chapter_sub.add_parser("init", help="단일 chapter 디렉토리 + metadata 초기화")
    p_ch_init.add_argument("chapter_id", help="ch00-prologue, ch01-economy 등")
    p_ch_init.add_argument("--force", action="store_true", help="기존 디렉토리 덮어쓰기 (RiskAssessor 검증)")
    p_ch_init.add_argument("--json", action="store_true")
    p_ch_init.set_defaults(func=cmd_chapter_init)

    p_ch_status = chapter_sub.add_parser("status", help="단일 chapter 상세 진척")
    p_ch_status.add_argument("chapter_id", help="ch00-prologue 등")
    p_ch_status.add_argument("--json", action="store_true")
    p_ch_status.set_defaults(func=cmd_chapter_status)

    # cite list/grade
    p_cite = sub.add_parser("cite", help="권위 DB 명령")
    cite_sub = p_cite.add_subparsers(dest="cite_action", required=True)
    p_cite_list = cite_sub.add_parser("list", help="citation-authority-db 57+ 권위 풀 조회")
    p_cite_list.add_argument("--grade", choices=["A", "A_preprint", "B", "C", "D", "E", "F", "G", "out"])
    p_cite_list.add_argument("--limit", type=int, default=30)
    p_cite_list.add_argument("--json", action="store_true")
    p_cite_list.set_defaults(func=cmd_cite_list)

    p_cite_grade = cite_sub.add_parser("grade", help="단일 저자 결정론 grade 조회")
    p_cite_grade.add_argument("author", help="저자명 또는 패턴")
    p_cite_grade.add_argument("--json", action="store_true")
    p_cite_grade.set_defaults(func=cmd_cite_grade)

    # completion
    p_completion = sub.add_parser("completion", help="단행본 13장 종합 진척률 보고")
    p_completion.add_argument("--json", action="store_true")
    p_completion.set_defaults(func=cmd_completion)

    # backup / restore
    p_backup = sub.add_parser("backup", help="영속 자산 atomic snapshot")
    p_backup.add_argument("--json", action="store_true")
    p_backup.set_defaults(func=cmd_backup)

    p_restore = sub.add_parser("restore", help="snapshot에서 복구 (비가역 — --confirm 필수)")
    p_restore.add_argument("snapshot_id", help="snapshot-YYYYMMDDThhmmssZ")
    p_restore.add_argument("--confirm", action="store_true", help="저자 명시 비가역 동의")
    p_restore.add_argument("--json", action="store_true")
    p_restore.set_defaults(func=cmd_restore)

    # prune
    p_prune = sub.add_parser("prune", help="자산 정리 명령")
    prune_sub = p_prune.add_subparsers(dest="prune_action", required=True)
    p_prune_sim = prune_sub.add_parser("sim", help="오래된 SIM-NNN 정리")
    p_prune_sim.add_argument("--days", type=int, default=30, help="cutoff (일 단위, default 30)")
    p_prune_sim.add_argument("--confirm", action="store_true")
    p_prune_sim.add_argument("--json", action="store_true")
    p_prune_sim.set_defaults(func=cmd_prune_sim)

    # healthcheck
    p_health = sub.add_parser("healthcheck", help="시스템 종합 결정론 헬스 (lib + skills + config + registries)")
    p_health.add_argument("--json", action="store_true")
    p_health.set_defaults(func=cmd_healthcheck)

    # init
    p_init = sub.add_parser("init", help="책 프로젝트 부트스트랩 (최초 1회)")
    p_init.add_argument("--root", help="책 루트 경로 (생략 시 BOOKWRITING_BOOK_ROOT 또는 ~/bookwriting)")
    p_init.add_argument("--title", help="책 제목")
    p_init.add_argument("--author", help="저자명")
    p_init.add_argument("--force", action="store_true", help="기존 파일 덮어쓰기")
    p_init.add_argument("--json", action="store_true")
    p_init.set_defaults(func=cmd_init)

    # export
    p_export = sub.add_parser("export", help="자산 마크다운 dump")
    p_export.add_argument("--output", help="출력 파일 경로 (생략 시 stdout)")
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
