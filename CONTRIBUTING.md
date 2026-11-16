# Contributing to the Atlas of Life

The Atlas of Life is a sourced encyclopedia of life on Earth. Most entries start as **AI drafts**:
a first pass compiled from the cited sources (PBDB, open-access literature, fixed Wikipedia
revisions, Wikimedia Commons). Every draft is marked as such on the site until people have
checked it. This page explains how you can help and how reviews work.

> **Licence:** the licence for the atlas text and code is still to be decided by the owner.
> Images keep their own licences (listed with each image). Until a licence is published, please
> contribute only text written in your own words.

## 1. Roles

| Role | Who | Can do |
|---|---|---|
| **Contributor** | anyone with a GitHub account | open issues (corrections, reviews, images, new genera), open pull requests |
| **Reviewer** | people invited by the owner | approve pull requests, record reviews and confirmations in entries |
| **Owner** | @pcontem | merges, invites reviewers, decides disputes and policy |

## 2. How to suggest something (no coding needed)

Every entry page on the site has a **Review & contribute** card with buttons that open a
pre-filled GitHub issue:

- **Suggest a correction** — a wrong or missing fact. Give the current text, your proposed text and
  a source (publication or database record). Corrections without a source cannot be accepted.
- **Submit a review** — you checked part or all of an entry against its sources. Say which parts
  (scope) and your verdict: *accepted*, *needs changes* or *rejected*.
- **Review or suggest an image** — judge a life restoration against current knowledge, flag an
  outdated one, or propose a new openly licensed image (CC0, public domain, CC BY, CC BY-SA).
- **New genus or excluded name** — propose a genus that is missing, or a name that should be
  listed as excluded (nomen dubium, junior synonym…), with the reference.

You can also open these forms directly from the repository's *Issues → New issue*.

**Edit the entry yourself.** The card's **Edit this entry** button opens the entry's file in
GitHub's editor. Change the text, then *Commit changes… → Propose changes*: GitHub copies the
repository to your account (a fork) and opens a pull request for review. Nothing changes on the
site until a reviewer approves it. The file is YAML: keep the indentation and the field names, and
add any new source to `sources`.

## 3. Rules every change must follow

The full rules are in [`CLAUDE.md`](CLAUDE.md) §3–§4. In short:

1. **Every fact has a source** listed in the entry. If it cannot be sourced, it is left out.
2. **Nothing is invented** — no dates, measurements, specimen numbers or authors.
3. **Own words** — paraphrase sources; quote at most a short phrase.
4. **No AI-generated images**, ever. Artwork that may not be copied is only linked.
5. **Only valid taxa** in the tree; rejected names go to `excluded.yaml`.

## 4. Pull requests

1. Fork or branch, edit the YAML in `entries/` (never the generated files in `site/`).
2. Run `python3 scripts/fmt.py`, `python3 scripts/build.py`, `python3 scripts/validate.py`
   (must print `0 error(s)`).
3. Open the pull request and fill in the checklist of the template.
4. GitHub runs the same checks (`check`). A pull request is merged only when the checks pass and
   a reviewer other than the author has approved it. A new push dismisses earlier approvals.
5. Changes to classification, synonymy, or anything that marks an entry `checked` need a
   **second reviewer** (see §5).

## 5. Reviews recorded in entries

Each entry has a `curation` block:

```yaml
curation:
  status: draft            # draft | checked
  origin: ai-draft         # ai-draft | human — who wrote the first version
  checked_by: ''
  checked_on: ''
  notes: []                # open to-dos
  reviews:
  - by: Jane Doe
    on: 2026-12-01
    scope: [all]           # or parts: identity, classification, age, formations, size,
                           # fossil_material, biology, images, sources, text
    verdict: accepted      # accepted | changes | rejected
    notes: Checked against Bennett 1994 and PBDB.
    confirmed_by: John Roe # a second, different reviewer
    confirmed_on: 2026-12-05
```

**Two-person rule.** An entry becomes `checked` only when:

- a review with `scope: [all]` and `verdict: accepted` exists,
- it was **confirmed by a second person** (`confirmed_by` ≠ `by`),
- `checked_by` is the first reviewer, and
- `notes` is empty.

The validator enforces this (rules Q1–Q3), so a pull request that breaks it fails the checks.
Nobody confirms their own review, and nobody approves their own pull request.

## 6. AI drafts

- AI drafts are marked `origin: ai-draft`. The site shows an **"AI draft · not yet reviewed"**
  badge until the entry is checked.
- AI may build skeletons and do a first pass over genera, species, ages, formations and openly
  licensed images. It never sets an entry to `checked`, never approves a pull request, and never
  produces images.
- Pull requests made with AI help say so in the template.

## 7. Audits

Once a month a workflow opens an issue listing a random sample of `checked` entries. A reviewer
re-checks them against their sources; any problem is fixed through the usual correction process
and, if needed, the entry goes back to `draft`.

## 8. Disagreements

When sources disagree, the entry says so and cites both (CLAUDE.md M7). Disputes between
reviewers are discussed in the issue or pull request; the owner decides.
