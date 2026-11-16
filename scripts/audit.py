#!/usr/bin/env python3
"""Monthly audit sample: pick checked entries at random for a second look.

Prints a Markdown issue body. Used by .github/workflows/audit.yml; can also be run by hand.
    python3 scripts/audit.py [--n 5] [--seed 2026-12]
"""
import argparse, datetime, glob, os, random, sys
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://pcontem.github.io/Atlas_of_life/"


def entries():
    for path in sorted(glob.glob(os.path.join(ROOT, "entries", "**", "*.yaml"), recursive=True)):
        name = os.path.basename(path)
        if name.startswith("_") or name in ("excluded.yaml", "home.yaml"):
            continue
        with open(path, encoding="utf-8") as f:
            e = yaml.safe_load(f) or {}
        if not isinstance(e, dict) or "curation" not in e:
            continue
        rel = os.path.relpath(path, ROOT)
        if "/formations/" in rel:
            link = f"{SITE}#formation/{e['id']}"
        elif e.get("rank") == "genus":
            link = f"{SITE}#{e['name']}"
        else:
            link = f"{SITE}#{e['id']}"
        yield rel, e, link


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5, help="entries to sample")
    ap.add_argument("--seed", default=datetime.date.today().strftime("%Y-%m"))
    a = ap.parse_args()

    all_e = list(entries())
    checked = [x for x in all_e if (x[1]["curation"] or {}).get("status") == "checked"]
    reviewed = [x for x in all_e if (x[1]["curation"] or {}).get("reviews")]
    rng = random.Random(a.seed)
    sample = rng.sample(checked, min(a.n, len(checked)))

    out = [f"Monthly audit ({a.seed}). Entries: {len(all_e)} · with reviews: {len(reviewed)} · "
           f"checked: {len(checked)}.", ""]
    if not sample:
        out += ["No entry is `checked` yet, so there is nothing to audit this month.", ""]
    else:
        out += ["Re-check each entry below against its cited sources (CONTRIBUTING.md §7). "
                "Tick it when done; open a correction issue for any problem, and if a fact is wrong "
                "the entry goes back to `draft`.", ""]
        for rel, e, link in sample:
            c = e["curation"]
            title = e.get("name") or e.get("id")
            out.append(f"- [ ] [{title}]({link}) — `{rel}` · checked by {c.get('checked_by') or '?'} "
                       f"on {c.get('checked_on') or '?'}")
        out.append("")
    out.append("The auditor must not be the person who checked or confirmed the entry.")
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
