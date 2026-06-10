# Bootstrapping the reference

Detailed how-to for the **Bootstrap** mode in [SKILL.md](../SKILL.md). Read this
before building the reference. The goal is a thin, pointer-based orientation aid —
not a re-documentation of the host. Odoo appears throughout only as a worked
example; the method is the same for any large host platform.

## 0. Orient first

Before writing anything, find two things:

- **Where the host source lives** — a vendored directory, an install path,
  `node_modules`, a plugins folder. You'll point at it constantly.
- **The host's version/build id** — you'll stamp the reference with it so future
  readers know what it describes and when to re-validate.

*Odoo example:* source under `odoo_src/usr/lib/python3/dist-packages/`
(`odoo/` core + `addons/`), version in the build label (e.g. `19.0`, deb build
`20260504`).

## 1. The map — generate, don't hand-write

The map answers "which module owns this concept." Build it from the host's
**machine-readable module descriptors**, so it's regenerable and never stale by
construction. Aggregate name + category/summary + dependencies into one scannable
table or list.

Where the descriptors live, by ecosystem:

| Ecosystem | Descriptor | Useful fields |
|---|---|---|
| Odoo | `__manifest__.py` per addon | `name`, `category`, `summary`, `depends` |
| Node / npm | `package.json` per package | `name`, `description`, `keywords`, `dependencies` |
| VS Code / editor ext | `package.json` `contributes` block | contribution points, activation events |
| WordPress / CMS plugins | plugin header comment | `Plugin Name`, `Description`, `Requires` |
| Python packages | `pyproject.toml` / entry points | name, summary, entry-point groups |

*Odoo example* — list every addon's identity and dependencies:

```bash
grep -rl "__manifest__.py" odoo_src/usr/lib/python3/dist-packages/addons/ | head
# then parse name/category/summary/depends out of each manifest into a table
```

Write a small script that walks the descriptors and emits the table; commit the
script next to the reference so the map can be regenerated after an upgrade. Don't
transcribe 1000 modules by hand — and don't try to cover all of them. Favor the
modules the project actually builds against; the rest are discoverable by grep
when a feature needs them.

## 2. The cookbook — patterns from real examples

For each common *type* of change, record the idiomatic pattern as a **pointer to
one real working example** plus a "grep this first" pointer to the parent being
extended. Prefer examples that already exist in the repo's own custom module —
they're proven against this exact host version.

Format each entry like:

> **To do X:** inherit/override `<host symbol>` as in `<path/to/real/example>`.
> Find the parent first: `grep -rn "<parent symbol>" <host source path>`.

*Odoo worked examples* — the patterns worth capturing for most addon work:

| Change type | Pattern | Grep-first pointer |
|---|---|---|
| Add fields/logic to a model | `_inherit = 'model.name'` | `grep -rn "class <Model>" addons/<owner>/models/` |
| Compose a new model from another | `_inherits` delegation | the parent model's class |
| Tweak a form/list/search view | view inheritance via `xpath` | `grep -rn "<view id>" addons/<owner>/views/` |
| Change a printable report | QWeb template inheritance (`inherit_id`) | the report template id in the owner addon |
| Change front-end behavior | OWL component / asset bundle override | the component or asset in `web`/owner addon |
| Run code on a schedule | `ir.cron` data record | existing crons in the owner addon |

Keep each pattern to a couple of lines. The example carries the detail; the
reference just routes you to it.

## 3. The decision tree — config vs code vs third-party

Most requests don't need code. Make the no-code path the first check. A minimal
tree:

1. **Configuration?** Can the host do this through settings/admin/declarative
   config? If plausibly yes, verify before writing code (live introspection below
   makes this fast). This is the most common and cheapest outcome.
2. **Custom code?** If config can't, identify the change-type, find it in the
   cookbook, use the map to locate the owning module, grep for the parent symbol.
3. **Third-party?** A maintained extension that already solves it — note as a lead,
   then out of scope for the reference (don't evaluate vendors here).

If the project already has a decision vocabulary, map onto it rather than inventing
one. *Odoo example:* this repo's `docs/STRUCTURE.md` uses **App / Configuration /
Custom code** as the `Solution:` field — reuse those exact words.

## 4. Optional — live introspection

Only when the host runs against a live instance/DB and "is this already
installed/configured?" is a recurring question. Introspecting the running instance
beats reading generic source, because it reflects the **actual configured state**.
Keep it to a handful of queries the reader can copy.

Generic approach: use the host's own shell/console/ORM (not raw SQL where an ORM
exists — the ORM layer carries semantics the raw schema loses) to ask:

- Which modules/plugins are installed and active?
- What configuration parameters / feature flags are set?
- Does a model/field/setting for this concept already exist?

*Odoo example:* `docker compose run --rm odoo shell -d <db>`, then query
`ir.module.module` (installed modules), `ir.config_parameter` (settings),
`ir.model` / `ir.model.fields` (does this field already exist?). The repo's
restored production dump is a ready stand-in for the live instance.

Note when introspection needs a restored dump or running instance, so a reader
without one knows to skip it.

## 5. Stamp, place, and stop

- **Stamp** the host version/build id at the top of the reference.
- **Place** it as a separate top-level file in the target repo, easy to find —
  not buried in a docs taxonomy, not folded into an existing agent guide (unless
  the user prefers otherwise).
- **Stop** once the map plus a handful of patterns cover the common cases. Note in
  the reference that the long tail is intentionally grep-on-demand, so a future
  reader doesn't mistake the thinness for incompleteness.

## Staleness defense (recap)

- Version stamp + pointer-based content = the reference survives most upgrades
  untouched.
- Regenerate the map (it's script output) and spot-check cookbook example paths on
  a deliberate host upgrade — add that to the project's upgrade checklist.
- Re-validate on upgrade only, never on a schedule.
