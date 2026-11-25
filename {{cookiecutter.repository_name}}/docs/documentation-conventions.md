---
title: Documentation conventions
description: What each docs directory holds and the rules every doc follows.
---

# Documentation conventions

## What each directory holds

| Directory | Holds | Kept current? |
|---|---|---|
| `docs/adr/` | Decisions in force: the rule, its reasoning and the options rejected | Yes, edited in place. A superseded decision is deleted; git keeps the history |

Every doc describes the present. There is no category of unmaintained docs. No plans, history, dates, ticket numbers, counts or rollout
notes: future work lives in the tracker, history in git. Superseded decisions and finished plans are deleted.

## Rules

- One topic per file, at most 300 lines. Split a file when different tasks need different halves; split into a directory beyond the
  limit. `AGENTS.md` has at most 150 lines outside tool-managed blocks.
- Lead with repository paths, written as plain backticked paths, so checks can detect dead references and drift.
- One home per fact. State it once and link to it. Name stable concepts, not values that change.
- Cite external knowledge (Jira, Confluence) by stable ID or URL; never copy it. Knowledge specific to this repository lives here;
  cross-repository knowledge stays outside and is linked.
- Record why next to the rule. A non-obvious rule that looks removable carries its reason, naming the enforcing test where possible.
  A code comment is optional, one line, and points to the doc.
- Use the names the code uses: classes, packages, files, modules and the internal project name. Define project-specific terms once.
- Code points to docs: the key class or package of a documented system links to its doc.
- Nothing that is not meant to be public in a public repository. No secrets or personal data anywhere.

## Frontmatter

Every doc starts with frontmatter that a check or an agent reads:

- `title`: the search title of the doc.
- `description`: one sentence, the search snippet.

Every directory has an `index.md` that links each doc in it.
