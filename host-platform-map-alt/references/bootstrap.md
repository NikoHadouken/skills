# Bootstrapping the reference

Detailed how-to for **Bootstrap** mode in [SKILL.md](../SKILL.md).
See [EXAMPLES.md](EXAMPLES.md) for a finished reference to use as a model.

The goal is a thin, pointer-based orientation aid — not a re-documentation of the
host. Odoo appears throughout as a worked example; the method is the same for any
large host platform.

## 0. Orient first

Find two things before writing anything:

- **Where the host source lives** — vendored directory, install path, `node_modules`,
  plugins folder. You'll point at it constantly.
- **The host's version/build id** — stamp the reference with it so future readers
  know what it describes and when to re-validate.

*Odoo:* source under `odoo_src/usr/lib/python3/dist-packages/` (`odoo/` core +
`addons/`), version in the build label (e.g. `17.0`, deb build `20260101`).

## 1. The map — generate, don't hand-write

The map answers "which module owns this concept." Build it from machine-readable
module descriptors so it's regenerable and never stale by construction.

Run the bundled script:

```bash
python3 scripts/gen-map.py <host-source-dir>
```

It auto-detects the ecosystem and emits a markdown table. Commit both the script
and its output next to the reference — the output is readable without running the
script; the script lets you regenerate after an upgrade.

Where descriptors live, by ecosystem:

| Ecosystem | Descriptor | Useful fields |
|---|---|---|
| Odoo | `__manifest__.py` per addon | `name`, `category`, `summary`, `depends` |
| npm / VS Code | `package.json` per package | `name`, `description`, `keywords`, `contributes` activation events |
| Python packages | `pyproject.toml` | `[project]` name/description, `[project.entry-points]` groups |
| WordPress plugins | PHP file header comment | `Plugin Name`, `Description`, `Requires`, `Requires PHP` |

Don't try to cover all modules — favor the ones the project actually builds against.
The rest are discoverable by grep when a feature needs them.

## 2. The cookbook — patterns from real examples

For each common change-type, record the idiomatic pattern as a pointer to one real
working example plus a "grep this first" hint. Prefer examples already in the
repo's own custom module — proven against this exact host version.

Format each entry as:

> **To do X:** inherit/override `<host symbol>` as in `<path/to/real/example>`.
> Find the parent first: `grep -rn "<parent symbol>" <host source path>`.

*Odoo patterns worth capturing for most addon work:*

| Change type | Pattern | Grep-first pointer |
|---|---|---|
| Add fields/logic to a model | `_inherit = 'model.name'` | `grep -rn "class <Model>" addons/<owner>/models/` |
| Compose model from another | `_inherits` delegation | the parent model's class |
| Tweak a form/list/search view | view inheritance via `xpath` | `grep -rn "<view id>" addons/<owner>/views/` |
| Change a printed report | QWeb `inherit_id` | the report template id in the owner addon |
| Change front-end behavior | OWL component / asset bundle override | the component or asset in `web`/owner addon |
| Run code on a schedule | `ir.cron` data record | existing crons in the owner addon |

Keep each entry to one or two lines. The example carries the detail; the reference
just routes you to it.

## 3. The decision tree — config vs code vs third-party

Make the no-code path the first check. Minimal tree:

1. **Configuration?** Can the host do this through settings/admin/declarative config?
   Verify before writing code — live introspection (below) makes this fast.
2. **Custom code?** Identify the change-type, find it in the cookbook, use the map
   to locate the owning module, grep for the parent symbol.
3. **Third-party?** A maintained extension that already solves it — note as a lead,
   out of scope for this reference.

If the project already has a decision vocabulary, map onto it rather than inventing
one. *Odoo example:* if the repo uses **App / Configuration / Custom code** as
`Solution:` values, reuse those exact words.

## 4. Live introspection (optional)

Only when the host runs against a live instance/DB and "is this already
installed/configured?" is a recurring question. Introspecting the running instance
beats reading generic source — it reflects the actual configured state.

Generic approach: use the host's own shell/console/ORM to ask:
- Which modules/plugins are installed and active?
- What config parameters/feature flags are set?
- Does a model/field/setting for this concept already exist?

*Odoo:* `docker compose run --rm odoo shell -d <db>`, then query
`ir.module.module` (installed modules), `ir.config_parameter` (settings),
`ir.model.fields` (does this field exist?). A restored production dump works as a
stand-in for the live instance.

Note when introspection needs a running instance so a reader without one knows to
skip it.

## 5. Stamp, place, and stop

- **Stamp** the host version/build id at the top of the reference.
- **Place** as a separate top-level file in the target repo — not buried in a
  `docs/` taxonomy, not folded into an existing agent guide (unless the user prefers
  otherwise). It's a developer orientation aid; make it easy to find.
- **Stop** once the map plus a handful of patterns cover the common cases. Note
  in the reference that the long tail is intentionally grep-on-demand, so a future
  reader doesn't mistake the thinness for incompleteness.

## Staleness defense

- Version stamp + pointer-based content = the reference survives most upgrades
  untouched.
- On a deliberate host upgrade: rerun `gen-map.py` and spot-check that cookbook
  example paths still resolve. Add that to the project's upgrade checklist.
- Re-validate on upgrade only — never on a schedule.
