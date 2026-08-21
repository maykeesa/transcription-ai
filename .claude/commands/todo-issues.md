---
description: Create GitHub issues from the open items in TODO.md, skipping the ones that already exist
allowed-tools: Bash(gh:*), Read
---

Sync `TODO.md` with the repository issues.

## Steps

1. Check authentication with `gh auth status`. If it fails, stop and ask the
   user to run `gh auth login` — do not try to work around it.

2. Read `TODO.md` at the project root.

3. List the issues that already exist, closed ones included:
   `gh issue list --state all --limit 200 --json number,title,state`

4. For every **unchecked** top-level item (`- [ ]`) in the TODO:
   - If an equivalent issue already exists, **skip it** and say so. Compare
     loosely — ignore case, accents and trailing punctuation; titles do not
     have to match character for character.
   - Otherwise, create the issue.

5. Checked items (`- [x]`) never become issues.

## Issue format

Keep the wording of the TODO, which is written in Portuguese.

- **Title**: the item text, without the `- [ ]`, without markdown (`**`,
  `` ` ``) and without the explanation that follows an em dash. Short.
- **Body**: whatever the title left out — the explanation after the em dash,
  when there is one. If the item has sub-items in the TODO, put them in the
  body as a task list (`- [ ] ...`), preserving their order.
- **Label**: the TODO section the item belongs to (Interface, Compatibilidade,
  Funcionalidades). Create the label first if it does not exist:
  `gh label create "<name>" --force`.

## Report

Finish with a table: title, action (created, with its number, or skipped) and
the reason for each skip. Never edit `TODO.md` — it stays the source of truth.
