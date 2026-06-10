---
name: host-platform-map
description: Build and use a thin, reusable orientation reference for a large, poorly-documented host platform you write addons/plugins against (ERPs like Odoo, big frameworks, CMS/editor plugin SDKs, monorepo platforms). Use this whenever you're starting feature work against such a host and need to answer "does this need custom code, where do I look, or can it just be configured?", whenever you find yourself repeatedly grepping a huge vendored source to orient, or when you want to create or refresh a map/cookbook of the host's extension surface. Reach for it even if the user doesn't say "skill" — if they're about to deep-analyze or document someone else's large codebase to make extending it easier, this is the approach.
---

# host-platform-map

You're working in a repo that extends a large host platform — its source is
vendored or installed nearby, it's poorly documented for extenders, and every
feature starts with the same tax: *where in this huge thing do I even look, and
does this need code at all?* This skill captures the cheapest durable way to kill
that tax.

## The core idea: document the thin layer, not the source

The tempting move is to deep-analyze the host source and write it all up. **Don't.**
The host source is large, usually version-pinned, and already sitting right there —
greppable on demand, always accurate, never stale. Prose that re-narrates it is
just a worse, staler copy that will mislead the moment the host updates.

The leverage is in the **thin layer grep doesn't give you**. Three artifacts:

1. **Map** — which module/package owns which concept, so you know *where* to grep.
   The real bottleneck is never "read this class," it's "which of N modules is even
   responsible for this." This is the single highest-value artifact.
2. **Cookbook** — the idiomatic extension pattern for each *type* of change (extend
   a model, inherit a view/template, override a report, override front-end assets,
   register a hook…), each pointing at **one real working example** in the host or
   in the existing custom code. These patterns are stable across versions.
3. **Decision routing** — config vs custom code vs third-party. Most "features"
   don't need code; the reference should make the no-code path the obvious first
   check.

One rule ties all three together: **point, don't copy.** Link to source paths and
real examples; never paste code bodies. Pointers self-heal across host versions;
pasted code rots and starts lying.

Keep it thin. The win is orientation, not coverage — a few pages of pointers, not
a re-documentation of the platform.

## Workflow — pick the mode you're in

### Bootstrap (the reference doesn't exist yet)

You're creating the reference. The detailed how-to lives in
[references/bootstrap.md](references/bootstrap.md) — **read it before building**,
it covers deriving the map from machine-readable metadata, building the cookbook
from real examples, and writing the decision tree. In short:

1. **Locate the host source and its metadata.** Find where the platform's code
   lives (vendored dir, `node_modules`, install path) and the machine-readable
   module descriptors (Odoo `__manifest__.py`, npm `package.json`, plugin
   headers). The descriptors are the map's raw material.
2. **Generate the map**, don't hand-write it. Aggregate the descriptors
   (name/category/summary/dependencies) into one scannable table. Because it's
   script output, it regenerates and never goes stale.
3. **Build the cookbook from what's already there.** For each common change-type,
   find one real working example (prefer the repo's own custom module) and record
   the pattern as a pointer: "to do X, inherit Y like `path/to/example` — grep
   `parent symbol` in `path/to/host` first."
4. **Write the decision tree** — config → custom code → third-party (out of
   scope). Map it onto the project's existing decision vocabulary if it has one.
5. **Stamp the host version** at the top (build/release id) and write everything
   to a **separate top-level reference file** in the target repo — not buried in a
   `docs/` taxonomy, not folded into an existing agent guide, unless the user says
   otherwise. It's a developer orientation aid and should be easy to find.

Bias to minimal: ship the map plus a handful of patterns that cover the common
cases. Stop there. You can always add a pattern when a real feature needs one.

### Consult (the reference exists — you're doing a feature)

1. Start from the **decision tree**: can this be configuration? If plausibly yes,
   check that path first (and consider live introspection — see below).
2. If it needs code, use the **map** to pinpoint the owning module, then **grep
   the real source** there for the exact class/symbol. The reference points; the
   source is ground truth.
3. Match the change to a **cookbook** pattern and follow its example.
4. If you hit a gap — a module the map doesn't cover, or a new pattern — add it
   back to the reference as you go. The reference improves through use.

### Maintain (the host version changed)

The version stamp is the trigger. Because the reference is pointer-based, most of
it survives a bump untouched; you mainly regenerate the map and spot-check that
cookbook example paths still resolve. Re-validate **only** on a deliberate host
upgrade — not on a schedule. Add this check to the project's upgrade checklist.

## Scope guardrails

- **Pointer-heavy, code-light.** If you're pasting source bodies, stop — link instead.
- **Never per-model/per-class prose.** That's what grep is for.
- **Generated over hand-written** wherever metadata allows (the map especially).
- **Done = the map plus enough patterns for the common cases.** Resist completeness;
  the long tail stays as grep-on-demand.

## Optional: live introspection

If the host runs against a live instance/database (an ERP, a CMS, a configured
app), a short introspection cheatsheet is the *best* answer to "is this already
installed / already configurable" — because it reflects the **actual configured
instance**, not the generic platform. Only worth it when config-vs-code is a real,
recurring question for this host. Keep it to a handful of queries; see
[references/bootstrap.md](references/bootstrap.md) for the generic approach.
