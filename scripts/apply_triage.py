#!/usr/bin/env python3
"""Apply the decisions made in the triage tool (tools/triage/index.html) to the genus entries.

    python3 scripts/apply_triage.py <volume> [--dry-run] [--report FILE]

Reads every batch file in data/triage/<volume>_decisions/ (one per "Send to GitHub" in the tool, named by
date and time, applied in that order — a later decision on the same image replaces an earlier one):
    {"volume": "pseudosuchia", "created": "2026-11-19T16:40:00Z", "genera": {"Caiman": {
        "add":    [{"src": "commons", "key": "File:Caiman yacare.jpg", "kind": "photo", "caption": "..."},
                   {"src": "oa", "key": "PMC9892002 Extended Data Fig. 1", "kind": "life", "caption": "..."}],
        "reject": ["File:...", "PMC... Fig. 3"],
        "clear":  ["File:..."],            # decision withdrawn
        "review": {"https://commons.wikimedia.org/wiki/File:X.jpg": "accepted"}}}}
and edits entries/<volume>/genera/<Genus>.yaml with the same code as `draft_genera.py addimg|addoa`
(CLAUDE.md §4.4 I1-I3, I5): at most 8 images per kind, photos only for living genera, only allowed licences,
`review: unreviewed` for new images. Images are downloaded afterwards by `scripts/media.py fetch` (GitHub
Actions). It is safe to run again: what an entry already shows is skipped. `reject` only hides candidates in the
tool. Genera without an entry yet stay pending in the file.
"""
import json, pathlib, re, sys, io, contextlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import draft_genera as dg  # noqa: E402
from triage_data import clean_license, text  # noqa: E402

KINDS = ("photo", "life", "fossil", "skeletal")
REVIEWS = ("unreviewed", "accepted", "outdated")


def load(p):
    return yaml.safe_load(p.read_text())


def save(p, e):
    p.write_text(yaml.safe_dump(e, allow_unicode=True, sort_keys=False, width=120))


def merged(vol):
    """All batches of a volume folded into one decision per image: {genus: {"add": [...], "review": {...}}}."""
    state = {}
    for b in sorted((ROOT / "data/triage" / f"{vol}_decisions").glob("*.json")):
        for g, d in json.loads(b.read_text()).get("genera", {}).items():
            s = state.setdefault(g, {"items": {}, "review": {}})
            for a in d.get("add") or []:
                s["items"][a["key"]] = a
            for k in d.get("reject") or []:
                s["items"][k] = {"reject": True}
            for k in d.get("clear") or []:
                s["items"].pop(k, None)
            s["review"].update(d.get("review") or {})
    return {g: {"add": [a for a in s["items"].values() if not a.get("reject")], "review": s["review"]} for g, s in state.items()}


def apply(vol, dry=False):
    decisions = merged(vol)
    if not decisions:
        return ["No decisions."], 0
    R = dg.raw(vol)
    oa = json.loads((ROOT / "data/raw" / vol / "oa_figures.json").read_text())["figures"] if (ROOT / "data/raw" / vol / "oa_figures.json").exists() else {}
    log, changed = [], 0
    for g, d in sorted(decisions.items()):
        p = ROOT / "entries" / vol / "genera" / f"{g}.yaml"
        adds, revs = d.get("add") or [], d.get("review") or {}
        if not (adds or revs):
            continue
        if not p.exists():
            log.append(f"- **{g}**: no entry yet — {len(adds)} image(s) stay pending")
            continue
        for a in adds:
            e = load(p)
            imgs = e.get("images") or []
            kind, key, cap = a.get("kind"), a.get("key"), text(a.get("caption"), 400)
            if kind not in KINDS:
                log.append(f"- {g}: skipped {key} — unknown kind {kind!r}"); continue
            if kind == "photo" and not e.get("extant"):
                log.append(f"- {g}: skipped {key} — `photo` is only for living genera (I-rules, §4.4)"); continue
            if sum(1 for i in imgs if i["kind"] == kind) >= 8:
                log.append(f"- {g}: skipped {key} — already 8 {kind} images (I1)"); continue
            if a.get("src") == "commons":
                files = dg.files_of(R, g)
                idx = next((n for n, (t, _) in enumerate(files, 1) if t == key), None)
                if idx is None:
                    log.append(f"- {g}: skipped {key} — not among the harvested candidates"); continue
                f = files[idx - 1][1]
                lic = clean_license(f.get("LicenseShortName"))
                if not lic:
                    log.append(f"- {g}: skipped {key} — licence {f.get('LicenseShortName')!r} not allowed (I3)"); continue
                if any(i.get("page") == f["page"] for i in imgs):
                    log.append(f"- {g}: {key} is already in the entry"); continue
                if dry:
                    log.append(f"- {g}: would add {key} as {kind}"); continue
                with contextlib.redirect_stdout(io.StringIO()):
                    dg.addimg(R, vol, [f"{g}:{idx}:{kind}:{cap}"])
                e = load(p)
                im = e["images"][-1]
                im["license"] = lic
                im["artist"] = text(im["artist"], 200) or "Unknown (no author on the Commons page)"
                save(p, e)
            elif a.get("src") == "oa":
                figs = oa.get(g, [])
                idx = next((n for n, f in enumerate(figs, 1) if f"{f['pmcid']} {f['label']}".strip() == key), None)
                if idx is None:
                    log.append(f"- {g}: skipped {key} — not among the harvested article figures"); continue
                f = figs[idx - 1]
                if (f.get("license") or "").lower() not in ("cc by", "cc0"):
                    log.append(f"- {g}: skipped {key} — licence {f.get('license')!r} not allowed (I3)"); continue
                if any(i.get("file") == key for i in imgs):
                    log.append(f"- {g}: {key} is already in the entry"); continue
                if dry:
                    log.append(f"- {g}: would add {key} as {kind}"); continue
                with contextlib.redirect_stdout(io.StringIO()):
                    dg.addoa(vol, [f"{g}:{idx}:{kind}:{cap}"])
            else:
                log.append(f"- {g}: skipped {key} — unknown source {a.get('src')!r}"); continue
            log.append(f"- {g}: added {key} as `{kind}`")
            changed += 1
        if revs and not dry:
            e = load(p)
            n = 0
            for i in e.get("images") or []:
                v = revs.get(i.get("page"))
                if v in REVIEWS and i.get("review") != v:
                    i["review"] = v
                    n += 1
                    log.append(f"- {g}: {i.get('file') or i.get('page')} → review `{v}`")
            if n:
                save(p, e)
                changed += n
    return log, changed


if __name__ == "__main__":
    a = sys.argv[1:]
    vol = a[0]
    log, changed = apply(vol, "--dry-run" in a)
    body = "\n".join(log) or "Nothing to apply."
    print(body)
    print(f"{changed} change(s)")
    if "--report" in a:
        pathlib.Path(a[a.index("--report") + 1]).write_text(f"## Image triage: {vol}\n\n{body}\n\n{changed} change(s).\n")
