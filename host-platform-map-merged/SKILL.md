---
name: host-platform-map-merged
description: Build and use a thin, reusable orientation reference for a large, poorly-documented host platform you write addons/plugins against (ERPs like Odoo, big frameworks, CMS/editor plugin SDKs, monorepo platforms). Use this whenever you're starting feature work against such a host and need to answer "does this need custom code, where do I look, or can it just be configured?", whenever you find yourself repeatedly grepping a huge vendored source to orient, or when you want to create or refresh a map/cookbook of the host's extension surface. Reach for it even if the user doesn't say "skill" — if they're about to deep-analyze or document someone else's large codebase to make extending it easier, this is the approach.
---

# host-platform-map

You're working in a repo that extends a large host platform — its source is
vendored or installed nearby, it's poorly documented for extenders, and every
feature starts with the same tax: *where in this huge thing do I even look, and
does this need code at all?* This skill kills that tax cheaply and durably.

## Quick start

1. Run `python3 scripts/gen-map.py <host-source-dir>` to generate the module map.
2. Read [references/bootstrap.md](references/bootstrap.md) for the full Bootstrap how-to.
3. See [references/EXAMPLES.md](references/EXAMPLES.md) for a finished reference to model.

## The core idea: document the thin layer, not the source

The tempting move is to deep-analyze the host source and write it all up. **Don't.**
The source is large, version-pinned, and already sitting right there — greppable on
demand, always accurate, never stale. Prose that re-narrates it is just a worse,
staler copy that misleads the moment the host updates.

The leverage is the **thin layer grep doesn't give you**. Three artifacts:

1. **Map** — which module/package owns which concept, so you know *where* to grep.
   The bottleneck is never "read this class," it's "which of N modules is even
   responsible for this." Highest-value artifact.
2. **Cookbook** — the idiomatic extension pattern per *type* of change (extend a
   model, inherit a view/template, override a report, override assets, register a
   hook…), each pointing at **one real working example**. Stable across versions.
3. **Decision routing** — config vs custom code vs third-party. Most "features"
   don't need code; make the no-code path the obvious first check.

One rule ties all three together: **point, don't copy.** Link to source paths and
real examples; never paste code bodies. Pointers self-heal across host versions;
pasted code rots and starts lying.

Keep it thin. The win is orientation, not coverage.

## Modes

### Bootstrap — the reference doesn't exist yet

Full how-to in [references/bootstrap.md](references/bootstrap.md) — read it before
building. In brief:

1. Locate the host source and its version/build id.
2. Generate the map from machine-readable descriptors (`gen-map.py`), then **trim**
   to the modules the project actually builds against.
3. Build the cookbook from real examples already in the repo — one pointer per
   change-type.
4. Write the decision tree: config → custom code → third-party.
5. Place as a separate top-level file in the target repo; stamp the host version
   at the top.

Bias to minimal: map + a handful of patterns for the common cases. Stop there.

### Consult — the reference exists, you're doing a feature

1. Start at the decision tree: can this be configuration? Check that path first.
2. If it needs code, use the map to pinpoint the owning module, then grep the real
   source there. The reference points; the source is ground truth.
3. Match the change to a cookbook pattern and follow its example.
4. Fill any gap back into the reference as you go — it improves through use.

### Maintain — the host version changed

The version stamp is the trigger. Because the reference is pointer-based, most of
it survives a bump untouched: rerun `gen-map.py` and spot-check that cookbook
example paths still resolve. Re-validate on a deliberate upgrade only, never on a
schedule. Add it to the project's upgrade checklist.

## Guardrails

- Pointer-heavy, code-light. Pasting source bodies → stop, link instead.
- No per-model/per-class prose — that's what grep is for.
- Generated over hand-written wherever metadata allows (the map especially).
- Done = map + enough patterns for the common cases. Resist completeness.

## Resources

- [references/bootstrap.md](references/bootstrap.md) — full Bootstrap how-to, with ecosystem guidance and live introspection
- [references/EXAMPLES.md](references/EXAMPLES.md) — a complete worked example of a finished reference
- [scripts/gen-map.py](scripts/gen-map.py) — generate the module map table from descriptors
