---
name: host-platform-map-alt
description: Build and use a thin orientation reference for large, poorly-documented host platforms you extend (ERPs like Odoo, CMS/plugin SDKs, npm monorepos, VS Code extensions). Use when starting feature work to answer "does this need code, where do I look, or can it just be configured?" — or when repeatedly grepping vendored source to orient. Also use when a user wants to create or refresh a module map, cookbook, or decision guide for any large extension surface.
---

# host-platform-map

## Quick start

1. Run `python3 scripts/gen-map.py <host-source-dir>` to generate the module map.
2. Read `references/bootstrap.md` for the full Bootstrap how-to.
3. See `references/EXAMPLES.md` for a finished reference to use as a model.

---

## The core idea

Document the thin layer grep doesn't give you. Three artifacts:

1. **Map** — which module owns which concept, so you know *where* to grep. The
   real bottleneck is never "read this class," it's "which of N modules is even
   responsible for this." Highest-value artifact.
2. **Cookbook** — idiomatic extension pattern per change-type, each pointing at
   one real working example. Stable across host versions.
3. **Decision routing** — config vs custom code vs third-party. The no-code path
   should be the obvious first check.

One rule ties all three together: **point, don't copy.** Link to source paths and
real examples; never paste code bodies. Pointers survive host upgrades; pasted
code rots.

---

## Modes

### Bootstrap — building the reference

See `references/bootstrap.md` for the full how-to. In brief:

1. Locate the host source and version stamp.
2. Generate the map from machine-readable descriptors — `gen-map.py` does this.
3. Build the cookbook from real examples already in the repo (one pointer per
   change-type).
4. Write the decision tree: config → custom code → third-party.
5. Place as a top-level file in the target repo; stamp the host version at the top.

Bias to minimal: map + handful of patterns. Stop there.

### Consult — feature work against an existing reference

1. Start at the decision tree: can this be configuration? Check that first.
2. Use the map to pinpoint the owning module, then grep the real source there.
3. Match to a cookbook pattern and follow its example pointer.
4. Fill gaps in the reference as you go — it improves through use.

### Maintain — after a host version bump

The version stamp at the top is the trigger. Because the reference is
pointer-based, most of it survives a bump untouched. On a deliberate upgrade:
rerun `gen-map.py`, spot-check that cookbook example paths still resolve. Add
this to the project's upgrade checklist. Never re-validate on a schedule.

---

## Guardrails

- Pointer-heavy, code-light. Pasting source bodies → stop, link instead.
- No per-model/per-class prose — that's what grep is for.
- Generated over hand-written wherever metadata allows (the map especially).
- Done = map + enough patterns for common cases. Resist completeness.

---

## Resources

- [`references/bootstrap.md`](references/bootstrap.md) — full Bootstrap how-to
- [`references/EXAMPLES.md`](references/EXAMPLES.md) — finished reference example
- [`scripts/gen-map.py`](scripts/gen-map.py) — generate the module map table
