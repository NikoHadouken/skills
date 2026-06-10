# host-platform-map

A skill for building and using a thin, pointer-based orientation reference
(`HOST-MAP.md`) for a large, poorly-documented host platform you write
addons/plugins against. See [SKILL.md](SKILL.md) for the method.

## Recommended model

The skill has three modes with different demands — pick the model per mode, not
once. A skill can't select its own model, so this is guidance for whoever runs it
(e.g. `/model` in Claude Code, or the model on an agent).

| Mode | Model | Why |
|---|---|---|
| **Bootstrap** (build the reference) | **Sonnet 4.6** (`claude-sonnet-4-6`) by default; **Opus 4.8** for large/gnarly hosts | Judgment-dense, not token-heavy (see depth note). The hard parts — picking the *canonical* example per pattern, trimming noise, writing a correct decision tree — get baked into a durable artifact, so a wrong call misleads every later Consult. Sonnet handles this well; step up to Opus when the host is big or confusing and first-pass accuracy matters. Avoid Haiku for authoring — weaker example-selection gets baked in. |
| **Consult** (use the reference for a feature) | **Sonnet 4.6** (`claude-sonnet-4-6`) | Routine, frequent, latency-sensitive lookup — the map already did the orienting, so this is route-and-grep. Best speed/intelligence balance, same 1M context, cheaper. |
| **Maintain** (after a host upgrade) | **Sonnet 4.6** | Mostly mechanical (rerun `gen-map.py`, spot-check paths, re-stamp). Haiku 4.5 works for the purely mechanical parts but has 200K context and no `effort` param. |
| **`scripts/gen-map.py`** | none | Deterministic Python — no model in the loop. |

Relative pricing per 1M tokens (input / output): Opus 4.8 $5 / $25 · Sonnet 4.6
$3 / $15 · Haiku 4.5 $1 / $5.

**Depth note — Bootstrap reads shallowly by design.** It does not recursively read
every module. The map comes from machine-readable *descriptors* via `gen-map.py` (no
code bodies), and only a handful of real examples are read — just deeply enough to
point at them (*point, don't copy*). Token volume and runtime stay modest even on a
big host, so the model choice is about **judgment quality on a durable artifact**,
not read depth. (It's also why Opus isn't as costly here as a deep read would be, and
why Haiku's risk is output quality, not price.)

**Rule of thumb:** Sonnet is the default for both Bootstrap and Consult. Step
Bootstrap up to Opus only for hard hosts; drop to Haiku only for the mechanical
Maintain pass and running the script. Avoid the inverse errors — Opus on every
routine lookup, or Haiku authoring the durable cookbook.
