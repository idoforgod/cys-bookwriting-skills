# cys-bookwriting-skills

**A Claude Code skill pack for actually finishing a book.**
It turns one raw idea into a paragraph of manuscript through 11 stages, forcing every output past a voice check and a citation check.

[한국어](README.md) · [MIT License](LICENSE)

> **Note on language.** The skills, specs, and prompts are written in **Korean**, and the voice rules assume Korean prose.
> This English README explains what the pack does and how to install it; using it in another language means adapting `voice-gate`'s sentence rules.

---

## Why this exists

Ask an AI to "write a chapter on this" and you get something plausible. The trouble starts after that.

- **The voice isn't yours.** Three chapters read like three different authors.
- **Citations are missing, or worse, invented.** Sentences beginning "according to one report" pile up.
- **Predictions can't be falsified.** "Things will change dramatically" is rhetoric, not a forecast.
- **You lose sight of the whole book.** By chapter 12 you can't recall what chapter 3 claimed.

This pack makes a **machine** check all four. It never asks an LLM "does this sound like my voice?"
There are Python modules that compute the score, and work stops when a threshold isn't met.

> This started as one futurist's private system for writing his own book. It has been generalized so anyone can point it at theirs.

---

## What's inside

### An 11-stage pipeline

The path from a seed idea to finished prose. Each stage is its own skill and consumes the previous stage's output.

| # | Skill | What it does |
|---|---|---|
| ① | `bookwriting-absorb-master` | Classify source material, register seeds, route to chapters |
| ② | `bookwriting-fact-anchor-master` | Pin facts and figures; detect duplicates and conflicts |
| ③ | `bookwriting-systemlink-master` | Find related assets in your registered corpus (BM25) |
| ④ | `bookwriting-evidence-collect-master` | Gather citable evidence, grade its authority (2+ tiers required) |
| ⑤ | `bookwriting-evidence-link-master` | Bind evidence to claims; surface unsupported claims |
| ⑥ | `bookwriting-insight-synthesis-master` | Synthesize evidence into insight propositions |
| ⑦ | `bookwriting-content-expand-master` | Expand insight into prose (where you step in) |
| ⑧ | `bookwriting-narrative-craft-master` | Assemble scenes and narrative |
| ⑨ | `bookwriting-structure-review-master` | Audit chapter structure, layer ratios, orphaned seeds |
| ⑩ | `bookwriting-line-edit-master` | Line editing; strip AI tone |
| ⑪ | `bookwriting-cross-chapter-relink-master` | Reconcile cross-chapter links and redundancy |

`bookwriting-master` orchestrates all eleven, and **70 sub-skills** handle the details beneath them.

One optional skill sits alongside them: `bookwriting-notebooklm-bridge`, the only route to outside material, and it runs **only when you invoke it explicitly**. Off by default.

The last skill is `bookwriting-sentence-edit-master` — a **final polishing pass**: paste a manuscript and it strips AI phrasing and self-rebuttal, keeps footnote numbers, tables and citation sources intact, and returns the polished full text as a file. It is split into **7 sub-skills**: context sheet → style alignment → AI-phrase removal → self-rebuttal removal → enrichment → manuscript-invariant check → output. It runs standalone, outside the pipeline, and is genre-, field- and audience-agnostic.

That totals 16 = 11 pipeline stages + 2 gates + 1 orchestrator + 1 optional bridge + 1 final polish.

### Two always-on gates

These apply to **every** output, at every stage.

| Skill | What it blocks |
|---|---|
| `voice-gate` | Prose that drifts from your voice. Below `voice_score 0.7` triggers a rewrite; final manuscript requires `0.85` |
| `citation-gate` | Hallucination. Five signals — missing source file, vague attribution, missing metadata, malformed URL/DOI, unsourced statistics — and **Critical stops work immediately** |

### 18 deterministic modules

The points where judgment is deliberately taken away from the LLM. Implemented as Python under `lib/`.

`VoiceScorer` · `HallucinationDetector` · `AuthorityGrader` · `QuantitativeExtraction` · `LayerRatioMeasurer` ·
`RelevanceScorer (BM25)` · `IdGenerator` · `SignaturePatternApplier` · `AITonePurger` · `AtomicWriter` ·
`ForecastRegistrySyncer` · `R4MultiLayerVerifier` · `LifecycleStateMachine` · `OrchestratorTracer` ·
`TraumaWitnessDetector` · `RiskAssessor` · `FactExtractor` · `AuthorWellnessGatekeeper`

### The five forecast rules (R1–R5)

If your book makes claims about the future, this is the heart of it. Registering a prediction requires all five.

- **R1 Quantitative anchor** — not "grows a lot" but "3× within 10 years"
- **R2 Chapter role** — cold open / analysis / implications
- **R3 System loop** — which feedback loop (L1–L7) it belongs to
- **R4 Multi-tier authority** — supported by at least two different authority grades
- **R5 Verification signal and falsifier** — **what observation would prove this wrong**

A prediction you can't write R5 for doesn't go in the book. That single rule separates a futures book from a fortune teller.

---

## Requirements

- **Python 3.9+** and **PyYAML**
- **Claude Code**

---

## Install

```bash
git clone https://github.com/idoforgod/cys-bookwriting-skills.git
cd cys-bookwriting-skills
./install.sh --book-root ~/my-book
```

`install.sh` does three things:

1. Verifies Python and PyYAML (installs PyYAML if missing)
2. **Symlinks** the 16 skills into `~/.claude/skills/` (use `--copy` to copy instead)
3. Scaffolds an empty book project if you pass `--book-root`

Add to your shell profile:

```bash
export BOOKWRITING_HOME="$HOME/cys-bookwriting-skills"
export BOOKWRITING_BOOK_ROOT="$HOME/my-book"
alias bookwriting="python3 $BOOKWRITING_HOME/bin/bookwriting.py"
```

To reverse it: `./install.sh --uninstall` — **removes only the skill links; your manuscript is untouched.**

---

## Getting started

### 1. Create a book project

```bash
bookwriting init --root ~/my-book --title "My Book" --author "My Name"
```

```
~/my-book/
├── master/
│   ├── book-config.yaml          ← all configuration lives here
│   ├── seed-registry.yaml        ← ideas (S-001, S-002 …)
│   ├── cycle-registry.yaml       ← writing cycles (C-001 …)
│   ├── forecast-registry.yaml    ← predictions (P-001 …)
│   └── sim-registry.yaml         ← auto-simulations (SIM-001 …)
├── chapters/
├── inbox/                        ← drop unsorted source material here
├── bookidea/skeleton.md          ← table of contents and core theses
└── workflows/book-planning.md
```

### 2. Fill in two files — skip this and the tool doesn't work

**`voice_guidelines` in `master/book-config.yaml`** is the **only** basis the voice gate has. Leave it empty and the gate is effectively off.

```yaml
voice_guidelines:
  vocabulary:
    preferred: ["your recurring concepts", "..."]   # 5+ recommended
    avoid:     ["phrasing you reject", "..."]
  sentence:
    max_length_chars: 80
  signature_expressions:
    - "This book is not about X but about Y"
```

**`bookidea/skeleton.md`** — your table of contents and the theses each chapter hangs from.

### 3. Register a seed and run it

```bash
bookwriting seed register --text "What remains when knowledge work costs nothing?" \
                          --chapter ch01 --role 2층_분석
bookwriting status
```

### 4. Call it from Claude Code

```
Use the bookwriting-master skill to run a cycle on S-001
```

---

## Commands

| Command | Purpose |
|---|---|
| `bookwriting init` | Bootstrap a book project (once) |
| `bookwriting status` | Overall asset status |
| `bookwriting list seeds\|cycles\|forecasts\|sims` | List assets |
| `bookwriting seed register\|status\|reroute` | Manage seeds |
| `bookwriting cycle progress\|expand\|simulate\|polish` | Advance a cycle |
| `bookwriting forecast register\|list` | Register predictions (R1–R5 enforced) |
| `bookwriting chapter list\|init\|status` | Manage chapters |
| `bookwriting cite list\|grade` | Query the authority DB |
| `bookwriting search` | BM25 search across registered corpus |
| `bookwriting validate` | Consistency checks |
| `bookwriting completion` | Whole-book progress |
| `bookwriting trace` | Trace a cycle's execution |
| `bookwriting backup\|restore\|prune` | Back up, restore, prune assets |
| `bookwriting healthcheck` | Verify install and configuration |
| `bookwriting export` | Dump assets as Markdown |

---

## Configuration

| Environment variable | Meaning | Default |
|---|---|---|
| `BOOKWRITING_BOOK_ROOT` | Book project root | upward search → `~/bookwriting` |
| `BOOKWRITING_REFERENCE_PATHS` | Personal reference paths (`:` separated) | none |
| `BOOKWRITING_HOME` | This repo's location (for the shell alias) | — |
| `CLAUDE_SKILLS_DIR` | Where skills get installed | `~/.claude/skills` |

Inspect how paths resolved:

```bash
python3 lib/paths.py
```

**No absolute paths are hardcoded.** Every path resolves through `lib/paths.py` alone.

---

## Things to know

- **The voice gate works only as well as you fill it in.** An empty `voice_guidelines` makes `voice_score` meaningless.
- **`expert_pool/citation-authority-db.yaml` is a sample.** Its 57 entries lean toward AI and futures research. **Replace it with your own field's authorities.**
- **Self-contained by design.** Nothing outside `search_paths` in `book-config.yaml` is ever read, and `exclude_patterns` separately blocks credentials and key files.
- **AI disclosure is enforced.** Past a configured ratio of AI-generated text, `authorship_policy` requires you to disclose the collaboration. That's a feature.
- **There's a wellness gate.** Late-night work, long stretches, and daily cycle caps are blocked. Disable with `author_wellness_policy.enabled: false`.

---

## Layout

```
cys-bookwriting-skills/
├── skills/          16 skills (+ 77 sub-skills)
├── lib/             18 deterministic modules + paths.py
├── bin/             bookwriting.py (CLI)
├── templates/       project scaffold used by `init`
├── specs/           design specifications (Korean)
├── docs/            design background (Korean)
├── expert_pool/     citation authority DB · module specs
└── install.sh
```

---

## Contributing

Issues and PRs welcome — especially:

- Authority DBs for other fields (medicine, law, business, humanities)
- Voice rules for languages other than Korean
- Accuracy improvements to the deterministic modules

---

## License

MIT — Copyright (c) 2026 최윤식 (Yoonsik Choi). Use it, change it, redistribute it.
