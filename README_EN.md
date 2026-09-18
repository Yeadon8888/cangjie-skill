<div align="center">

**English** | [中文](README.md)

# Cangjie.skill

> *Cangjie observed the tracks of birds and beasts, understood how their patterns differed, and created writing.*

<br>

> *Don't make AI sound like them. Make AI think like them.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)

<br>

Cangjie turned traces in the world into written symbols.<br>
Cangjie.skill turns traces in a person's words, actions, and decisions into an executable cognitive context.

<br>

**Feed it books, interviews, essays, or transcripts. It extracts how a person formed their beliefs, made real decisions, learned from failure, and lived with contradictions—then packages that context as an Agent Skill.**

<br>

Built on the MIT-licensed architecture of [Nuwa.skill](https://github.com/alchaincyf/nuwa-skill), with thanks to [Hua Shu](https://x.com/AlchainHust).

[Why it is different](#cangjie-vs-nuwa) · [Results](#results) · [Ready-made-skills](#ready-made-skills) · [Install](#installation) · [How-it-works](#how-it-works)

</div>

---

## Cangjie vs Nuwa

Nuwa is an excellent persona-distillation tool. Cangjie takes its architecture in a deliberately different direction:

| | Nuwa | Cangjie |
|---|---|---|
| **Core idea** | Role-play + thinking frameworks | Cognitive-context injection |
| **Extraction focus** | Mental models + expression DNA + decision heuristics | **Belief-formation stories** + **real decision retrospectives** + **failure lessons** + **internal contradictions** |
| **Intentionally omitted** | — | Generic opinions, explicit reasoning recipes, exhaustive style rules |
| **Design principle** | Tell the model how to reason step by step | Tell the model what happened to this person and why they believe what they believe |
| **Moat** | Complete persona reproduction | Knowledge a general model cannot infer on its own |

### Why this design?

Modern models already reason well, adapt their style, and know an increasing amount of public information. Features built mainly on explicit reasoning steps or detailed stylistic imitation become less valuable as models improve.

Cangjie focuses on context that model improvements cannot manufacture:

| Generic and increasingly commoditized ❌ | Cangjie's focus ✅ |
|:---:|:---:|
| “Independent thinking matters.” | “I learned to value independent thinking after seeing thousands of YC applications and noticing that the best ideas were initially rejected by almost everyone.” |
| “Step 1: classify the problem.” | “When I hear a startup idea, my instinct is to ask where it came from: a real pain or an invented one?” |
| “Prefer short sentences and three analogies per thousand words.” | “I speak directly, use simple words, and say ‘I suspect’ when I am uncertain.” |

---

## Results

We distilled Paul Graham from the same 140 KB, six-dimensional research set with both Nuwa and Cangjie, then asked:

> **“I have written a technical blog for three years. Someone suggested monetizing it with a paid community, but I worry that charging will corrupt the work. What do you think?”**

The Nuwa version mainly quoted familiar ideas and framework names. The Cangjie version challenged the hidden assumption that “free means pure and paid means corrupted,” then contrasted PG's structurally free writing—supported by income elsewhere—with the user's potentially unsustainable situation.

### Blind evaluation: 3 rounds × 6 dimensions × 10 points

| | Round 1 | Round 2 | Round 3 | Total |
|---|:---:|:---:|:---:|:---:|
| **Cangjie v3** | 53 | 53 | 54 | **160** |
| **Nuwa** | 45 | 45 | 45 | **135** |

> Evaluator: “Cangjie v3 does not merely repeat what PG said. It reasons the way PG would.”

---

## Ready-made Skills

Each distilled thinker is published as an independently installable Agent Skill:

| Thinker | Focus | Repository | Install |
|---|---|---|---|
| **Paul Graham** | Startups, writing, independent thought | [paul-graham-skill](https://github.com/Yeadon8888/paul-graham-skill) | `npx skills add Yeadon8888/paul-graham-skill` |
| **Alfred Adler** | Individual psychology, task separation, courage | [adler-skill](https://github.com/Yeadon8888/adler-skill) | `npx skills add Yeadon8888/adler-skill` |
| **Fengge** | Realism, demystification, loss-cutting | [fengge-skill](https://github.com/Yeadon8888/fengge-skill) | `npx skills add Yeadon8888/fengge-skill` |

Want somebody else? Install Cangjie and ask it to distill that person.

---

## Installation

```bash
npx skills add Yeadon8888/cangjie-skill
```

Then ask your skill-compatible coding agent:

```text
Use Cangjie to distill Charlie Munger.
Build a thinking skill for Zhang Yiming.
Distill Richard Feynman's cognitive approach.
```

After generation, use the result directly:

```text
Analyze this investment using Munger's way of thinking.
How would Paul Graham assess my startup idea?
Explain quantum computing through Feynman's perspective.
```

---

## What Cangjie Distills

The goal is not to reproduce *how somebody talks*. It is to preserve *why they think the way they do*.

| Layer | What Cangjie preserves |
|---|---|
| **Beliefs** | The belief plus the story that formed it |
| **Decisions** | Real choices, the reasoning at the time, and hindsight |
| **Failures** | Lessons the person acknowledged themselves |
| **Contradictions** | Unresolved tensions, kept rather than artificially reconciled |
| **Boundaries** | Specific domains where the person's judgment should not be trusted |
| **Thinking habits** | First-person habits with named frameworks internalized naturally |
| **Expression** | Only the strongest preferences and prohibitions |

### Honest boundaries are mandatory

Every generated Skill must state what it cannot do:

- The cognition is reconstructed from limited evidence and does not represent the real person's current position.
- Out-of-domain areas must be named specifically.
- Information must have a cutoff date.
- Inferences from behavior must be distinguished from the person's explicit statements.

---

## How It Works

```text
Phase 0  Route the request and confirm the subject
Phase 1  Collect evidence across six source dimensions
Phase 2  Extract irreplaceable cognitive context
Phase 3  Build the v3 cognitive-injection Skill
Phase 4  Validate quality and evidence coverage
```

### Extraction priority

```text
1. Belief-formation stories       highest
2. Real decision retrospectives  high
3. Failures and self-correction  high
4. Internal contradictions       high
5. Explicit cognitive boundaries medium
6. Repeated thinking habits      medium
7. Generic opinions and quotes   low unless backed by a unique story
```

### The generated Skill structure

```text
Who I am
My cognitive context
  ├─ Beliefs and where they came from
  ├─ Important decisions and hindsight
  ├─ Failures and corrections
  ├─ Unresolved contradictions
  └─ What I do not understand
How I tend to examine problems
What I refuse to do
How I communicate
Evidence sources
```

See [`references/extraction-framework.md`](references/extraction-framework.md) for the complete methodology.

---

## Why v3

Cangjie went through three evaluated designs:

| Version | Design | Blind score | Main problem |
|---|---|:---:|---|
| v1 | Explicit Step 1/2/3 reasoning | 145 | Over-instruction constrained the model |
| v2 | Pure cognitive injection | 132 | Removing everything also removed useful named frameworks |
| **v3** | **Cognitive injection + named frameworks as habits** | **160** | Best balance |

The important distinction is that a framework such as “Do Things That Don't Scale” is not encoded as a mandatory procedure. It becomes a natural habit: “When I see an early-stage problem, my instinct is to ask whether we can first solve it manually.”

---

## Repository Structure

```text
cangjie-skill/
├── SKILL.md                         # The Cangjie meta-skill
├── references/
│   ├── extraction-framework.md      # Evidence-first extraction method
│   ├── research-guide.md            # Source and research-note guidance
│   └── skill-template.md            # v3 output template
├── scripts/
│   ├── quality_check.py             # 12-part v3 quality gate
│   └── compile-prompt.py            # Skill-to-API prompt compiler
├── tests/
│   └── test_tools.py                # Regression tests
├── examples/
│   ├── paul-graham-perspective/
│   └── adler-perspective/
└── LICENSE
```

---

## Tooling

### Skill-to-Prompt compiler

Convert a generated `SKILL.md` into an API-ready system prompt:

```bash
python3 scripts/compile-prompt.py examples/paul-graham-perspective/SKILL.md
```

The compiler preserves identity, belief origins, decisions, failures, tensions, boundaries, thinking habits, guardrails, and communication style. It fails loudly when required v3 sections are missing instead of silently emitting an empty prompt.

Write the compiled prompt to a file:

```bash
python3 scripts/compile-prompt.py \
  examples/paul-graham-perspective/SKILL.md \
  --output paul-graham-prompt.md
```

### Quality validation

```bash
python3 scripts/quality_check.py examples/paul-graham-perspective/SKILL.md
```

The 12-part gate checks belief-formation evidence, decision hindsight, acknowledged failures, internal contradictions, cognitive boundaries, first-person consistency, red lines, source coverage, and the absence of deprecated Step 1/2/3 reasoning recipes.

Run the regression suite:

```bash
python3 -m unittest discover -s tests -v
```

---

## Acknowledgements

- [Nuwa.skill](https://github.com/alchaincyf/nuwa-skill) — the MIT-licensed architectural foundation.
- [Colleague.skill](https://github.com/titanwings/colleague-skill) — evidence that distilling a person's thinking into a reusable skill is possible.

---

<div align="center">

**Nuwa** distills how people speak.<br>
**Cangjie** distills why they think the way they do.<br><br>
*This is not role-play. It is cognitive context.*

<br>

MIT License

</div>
