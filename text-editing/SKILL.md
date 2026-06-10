---
name: text-editing
description: Edit text or documents at the right level — proofreading (typos, spelling, punctuation), copyediting (clarity, word choice, flow while preserving voice), or developmental editing (restructure, reorganize, reshape for audience/purpose). Use when user asks to fix, improve, edit, proofread, revise, or rewrite a message, document, issue, or any piece of text.
---

# Text Editing

## Level selection

Pick the level from context. When in doubt, ask.

| Signal | Level |
|--------|-------|
| "spell check", "fix typos", "check grammar", "proofread" | **Proofreading** |
| "clean up", "improve wording", "fix this message" | **Copyediting** |
| "revise", "restructure", "rewrite for X audience", "make this an issue/doc" | **Developmental** |
| Chat message or short personal text | Default to **copyediting** |
| Issue, PR description, or internal doc with clear purpose | Default to **developmental** |

## Guardrails (all levels)

- **Never fabricate.** Do not add facts, claims, numbers, or details that aren't in the source. Editing improves how something is said, not what is true.
- **Preserve meaning.** Keep the author's intent and any technical precision. If a sentence is ambiguous, flag it — don't guess and rewrite it into a definite claim.
- **Keep the language.** Edit in the language the text was written in. Don't translate unless asked.
- **Keep the register.** Match the original's formality (casual chat stays casual; a formal doc stays formal).

## Levels

### Proofreading
Surface pass only. Fix: typos, spelling, punctuation, capitalization, formatting consistency. Do not change wording, sentence structure, or meaning. Show the corrected text and briefly note what changed.

> **Before:** `i think its ready, lets ship it tomorow if thats ok`
> **After:** `I think it's ready, let's ship it tomorrow if that's ok`

### Copyediting
Sentence-level improvements. Fix: word choice, awkward phrasing, redundancy, grammar, clarity. Preserve the author's voice and intent. Do not reorganize or add content. Output the revised text; note significant changes only if non-obvious.

> **Before:** `The reason why this is failing is because the cache is not being cleared in a proper way.`
> **After:** `This is failing because the cache isn't cleared properly.`

### Developmental
Big-picture rework. Reorganize structure, cut or expand sections, adjust tone and framing for the target audience or use case. State the changes made and why. For documents, produce a clean final version.

Derive the structure from the document's type and purpose — don't impose a fixed template. A bug report, a design doc, a tutorial, and an announcement each want a different shape. The example below is one such shape, not a default.

> **Before (an issue):** A wall of text mixing the bug, a repro, a theory, and a fix idea in no order.
> **After:** Structured as **Problem → Steps to reproduce → Expected vs actual → Proposed fix**, with the theory trimmed to one line.

## Workflows

### Fix a chat message
1. Infer whether the goal is correctness (proofreading) or also flow (copyediting)
2. Apply fixes, keep the register (casual/formal) of the original
3. Output the revised message only — no explanation unless something was ambiguous

### Improve an issue or PR description
1. Identify: what is the problem? what is the change? what is the impact?
2. Restructure around those three beats if not already present
3. Output a clean version with a summary of structural changes made

### Create a structured document
1. Ask for the target audience and purpose if not stated
2. Extract the core content and intent from the draft
3. Apply a logical structure (intro → body → action/conclusion)
4. Output the document, then list structural decisions made

## Output format

- Output the edited text first, in full
- For a long text with only sparse edits (e.g. proofreading), also list the specific changes so they aren't buried
- Keep explanations short — what changed and why, only if non-obvious
- If the level was inferred, name it at the top: `Editing level: copyediting`
