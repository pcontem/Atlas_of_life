#!/usr/bin/env python3
"""Build data/triage/<volume>.json: every image candidate of a volume, in the shape the triage tool
(tools/triage/atlas-image-picker.html) loads — Commons files and open-access article figures per genus, what each entry
already shows, and which genera have an entry.

    python3 scripts/triage_data.py [<volume> ...]      (no argument = every volume that has a harvest)

Only reads data/raw/<volume>/ and entries/<volume>/ (no network). It is run by scripts/build.py, so the file is
always as current as site/data.json (check.yml fails when it is stale), and again by the triage-apply workflow.
Decisions made in the tool are kept apart, in data/triage/<volume>_decisions/.
"""
import html, json, pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
LICENSE_OK = re.compile(r"^(CC0|CC BY(?:-SA)? \d\.\d(?: [A-Za-z]{2,3})?)")


def clean_license(name):
    """Licence label in the form the validator accepts (I3), or None when the licence cannot be used.
    National ports ('CC BY-SA 3.0 ch') keep the base version; 'Public Domain' is normalised."""
    n = (name or "").strip()
    if n.lower() == "public domain":
        return "Public domain"
    m = LICENSE_OK.match(n)
    return m.group(0) if m else None


def text(s, limit=220):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= limit else s[: limit - 1].rstrip() + "…"


def name_index(vol, raw, genera, entries):
    """For each genus, the words that point to it: its name, its synonyms (PBDB accepted names, junior synonyms in
    excluded.yaml) and the epithets of its species (old combinations such as "Crocodylus cataphractus" for
    Mecistops). Also the set of every genus name of the volume, valid or not."""
    own = {g: {g} for g in set(genera) | set(entries)}
    allnames = set(own)
    recs = json.loads((raw / "pbdb_genera.json").read_text())["records"]
    if (raw / "pbdb_invalid.json").exists():
        recs += json.loads((raw / "pbdb_invalid.json").read_text())["records"]
    for r in recs:
        allnames.add(r["taxon_name"])
        a = r.get("accepted_name")
        if a and a != r["taxon_name"] and a in own:
            own[a].add(r["taxon_name"])
    exp = ROOT / "entries" / vol / "excluded.yaml"
    for x in (yaml.safe_load(exp.read_text()) if exp.exists() else None) or []:
        allnames.add(x["name"])
        if x.get("status") == "junior synonym" and x.get("parent") in own:
            own[x["parent"]].add(x["name"])
    epithets = {g: set() for g in own}
    sp = json.loads((raw / "pbdb_species.json").read_text())["species"] if (raw / "pbdb_species.json").exists() else {}
    for g, lst in sp.items():
        for x in lst if g in epithets else []:
            ep = (x.get("name") or x.get("taxon_name") or "").split()[-1:]
            if ep and len(ep[0]) >= 5:
                epithets[g].add(ep[0].lower())
    for g, e in entries.items():
        for x in e.get("species") or []:
            ep = x["name"].split()[-1]
            if len(ep) >= 5:
                epithets[g].add(ep.lower())
    return own, epithets, allnames


def relatives(g, txt, own, epithets, allnames):
    """Other genera a candidate names when it does not name this genus (its name, a synonym or a species
    epithet) — the sign of a picture of a relative taken from the genus's Wikipedia article or category tree."""
    words = set(re.findall(r"[A-Za-z]+", txt))
    low = {w.lower() for w in words}
    if any(n.lower() in low for n in own.get(g, {g})) or epithets.get(g, set()) & low:
        return []
    return sorted((words & allnames) - own.get(g, {g}))


def build(vol):
    raw = ROOT / "data/raw" / vol
    j = lambda n: json.loads((raw / n).read_text())
    genera = {r["taxon_name"]: r for r in j("pbdb_genera.json")["records"] if not r.get("flags")}
    commons = j("commons.json")["files"]
    oa = j("oa_figures.json")["figures"] if (raw / "oa_figures.json").exists() else {}
    entries = {}
    for p in (ROOT / "entries" / vol / "genera").glob("*.yaml"):
        e = yaml.safe_load(p.read_text())
        entries[e["name"]] = e
    own, epithets, allnames = name_index(vol, raw, genera, entries)
    by_genus = {}
    for title, f in sorted(commons.items()):
        if not f.get("thumb") or not (f.get("mime") or "").startswith("image/") or f.get("mime") == "image/svg+xml":
            continue
        for g in f["genera"]:
            by_genus.setdefault(g, []).append((title, f))
    out = []
    for name in sorted(set(genera) | set(entries)):
        e = entries.get(name)
        shown = {i.get("page") for i in (e or {}).get("images") or []}
        shown_files = {i.get("file") for i in (e or {}).get("images") or []}
        cands = []
        for title, f in by_genus.get(name, []):
            lic = clean_license(f.get("LicenseShortName"))
            cands.append(dict(key=title, thumb=f["thumb"], page=f["page"], w=f.get("width"), h=f.get("height"),
                              artist=text(f.get("Artist"), 90), license=f.get("LicenseShortName") or "?",
                              ok=bool(lic), caption=text(f.get("ImageDescription")), found=f.get("found", []),
                              inentry=f["page"] in shown,
                              other=relatives(name, f"{title} {text(f.get('ImageDescription'), 2000)}", own, epithets, allnames)))
        figs = []
        for f in oa.get(name, []):
            key = f"{f['pmcid']} {f['label']}".strip()
            lic = (f.get("license") or "").lower()
            figs.append(dict(key=key, img=f["img"], page=f"https://doi.org/{f['doi']}" if f.get("doi") else f"https://europepmc.org/article/PMC/{f['pmcid']}",
                             cite=text(f.get("cite"), 160), label=f["label"], caption=text(f.get("caption"), 300),
                             license=f.get("license") or "?", ok=lic in ("cc by", "cc0"), inentry=key in shown_files,
                             other=relatives(name, f.get("caption") or "", own, epithets, allnames)))
        if not (cands or figs or e):
            continue
        r = genera.get(name, {})
        out.append(dict(
            name=name, family=r.get("family") or r.get("parent_name") or (e or {}).get("parent", ""),
            extant=bool((e or {}).get("extant") or r.get("is_extant") == "extant"), has_entry=bool(e),
            existing=[dict(kind=i["kind"], url=i.get("url"), page=i.get("page"), artist=text(i.get("artist"), 90),
                           license=i.get("license"), caption=text(i.get("caption")), review=i.get("review", "unreviewed"))
                      for i in (e or {}).get("images") or []],
            commons=cands, oa=figs))
    return dict(volume=vol, genera=out)


def harvested_volumes():
    return sorted(p.parent.name for p in (ROOT / "data/raw").glob("*/commons.json"))


def main(vols=None, quiet=False):
    for vol in vols or harvested_volumes():
        if not (ROOT / "data/raw" / vol / "commons.json").exists():
            print(f"{vol}: no data/raw/{vol}/commons.json (volumes from before harvest.py are not supported)")
            continue
        d = build(vol)
        p = ROOT / "data/triage" / f"{vol}.json"
        p.parent.mkdir(exist_ok=True)
        p.write_text(json.dumps(d, ensure_ascii=False, separators=(",", ":")))
        n = sum(len(g["commons"]) + len(g["oa"]) for g in d["genera"])
        o = sum(1 for g in d["genera"] for c in g["commons"] + g["oa"] if c["other"])
        if not quiet:
            print(f"{p.relative_to(ROOT)}: {len(d['genera'])} genera, {n} candidates ({o} name only other genera), {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main(sys.argv[1:])
