"""Create or refresh formation entries from the genus entries and PBDB collection data.

    python3 scripts/make_formations.py

Reads   entries/*/genera/*.yaml                    (each genus lists its formations)
        data/raw/<volume>/pbdb_occs.json           (occurrences: genus, formation, collection, coordinates)
        data/raw/<volume>/pbdb_colls.json          (PBDB collections: coordinates, environment, lithology)
Writes  entries/formations/<id>.yaml               (one per formation; created if missing)
        the `id` of each formation item in the genus entries (links genus -> formation)

Only the PBDB-derived fields are refreshed (country, regions, location, age, environment,
lithology, pbdb_collections). Hand-written fields (summary, paleoenvironment, extra sources,
curation) are never overwritten. Run fmt.py afterwards.
"""
import collections, json, pathlib, re, statistics, unicodedata
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
FORM = ROOT / "entries/formations"
COUNTRY = {"AR": "Argentina", "AU": "Australia", "BR": "Brazil", "CA": "Canada", "CL": "Chile", "CN": "China",
           "CO": "Colombia", "CU": "Cuba", "DE": "Germany", "DK": "Denmark", "EG": "Egypt", "ES": "Spain",
           "FR": "France", "GB": "United Kingdom", "UK": "United Kingdom", "GL": "Greenland", "IT": "Italy",
           "JO": "Jordan", "KZ": "Kazakhstan", "LB": "Lebanon", "MA": "Morocco", "MN": "Mongolia", "MX": "Mexico",
           "PT": "Portugal", "RO": "Romania", "TZ": "Tanzania", "US": "United States", "AT": "Austria",
           "CH": "Switzerland", "BE": "Belgium", "RU": "Russia", "IN": "India", "JP": "Japan", "NZ": "New Zealand"}


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# PBDB spellings of the same unit -> the name used for its formation entry
ALIASES = {"Posidonienschiefer": "Posidonia Shale"}


def parts(name):
    """'Dolomia di Forni / Calcari di Zorzino' -> both; 'Caiuá Group (Rio Paraná / Goio-Erê)' -> all three."""
    m = re.match(r"(.*?)\s*\((.*)\)\s*$", name.strip())
    raw = re.split(r"\s*/\s*", m.group(1)) + re.split(r"\s*/\s*", m.group(2)) if m else re.split(r"\s*/\s*", name)
    out = [re.sub(r"\s+Formation$", "", x).strip() for x in raw if x.strip()]
    return [ALIASES.get(x, x) for x in out]


def same(a, b):
    a, b = a.lower(), b.lower()
    return bool(a) and bool(b) and (a.startswith(b) or b.startswith(a))


def med(v):
    return round(statistics.median(v), 3)


def main():
    FORM.mkdir(parents=True, exist_ok=True)
    forms = {}
    for vol in sorted(p for p in (ROOT / "entries").iterdir() if (p / "genera").is_dir()):
        raw = ROOT / "data/raw" / vol.name
        if not (raw / "pbdb_colls.json").exists():
            continue
        cols = json.loads((raw / "pbdb_colls.json").read_text())["cols"]
        occ = collections.defaultdict(list)
        for r in json.loads((raw / "pbdb_occs.json").read_text()):
            p = r.split("|")
            occ[p[0]].append(dict(form=p[3], cc=p[6], state=p[7], col=p[12].split(":")[1]))
        for gp in sorted((vol / "genera").glob("*.yaml")):
            e = yaml.safe_load(gp.read_text())
            changed = False
            for f in e["formations"]:
                name = f["formation"]
                if name == "Unnamed unit":
                    # unnamed units are separate localities: one point per genus
                    where = ", ".join(f["regions"]) or f["country"]
                    fid = slug(f"unnamed {where} {e['name']}")
                    title, names = f"Unnamed unit, {where} ({e['name']} locality)", []
                    used = [o["col"] for o in occ[e["name"]] if not o["form"] and (not f["regions"] or o["state"] in f["regions"])]
                else:
                    names = parts(name)
                    fid, title = slug(names[0] + " " + f["country"]), names[0]
                    used = [o["col"] for o in occ[e["name"]] if any(same(o["form"], n) for n in names)]
                d = forms.setdefault(fid, dict(name=title, names=set(names), country=f["country"], regions=set(),
                                               cols=set(), ma=[], genera=set(), group=set()))
                d["names"] |= set(names)
                d["regions"] |= set(f["regions"])
                d["cols"] |= {c for c in used if c in cols}
                if f.get("group"):
                    d["group"].add(f["group"])
                if f.get("ma"):
                    d["ma"].append(f["ma"])
                else:  # no PBDB age for this bed: fall back on the genus age
                    d.setdefault("gen_ma", []).append([e["age"]["last_ma"], e["age"]["first_ma"]])
                d["genera"].add(e["name"])
                if f.get("id") != fid:
                    f["id"] = fid
                    changed = True
            if changed:
                gp.write_text(yaml.safe_dump(e, allow_unicode=True, sort_keys=False, width=110))
    for fid, d in sorted(forms.items()):
        basis = "PBDB collections that yielded the atlas genera"
        sel = [ALL_COLS[c] for c in d["cols"]]
        if not sel:
            cc = {k for k, v in COUNTRY.items() if v == d["country"]}
            for n in d["names"]:
                sel += [r for r in BYNAME.get(n, []) if r.get("cc") in cc or not cc]
            basis = "all PBDB collections of the formation in that country (none recorded with the atlas genera)"
        sel = [r for r in sel if r.get("lng") is not None]
        p = FORM / f"{fid}.yaml"
        e = yaml.safe_load(p.read_text()) if p.exists() else {}
        env = collections.Counter(r["environment"] for r in sel if r.get("environment"))
        lith = collections.Counter(r["lithology1"] for r in sel if r.get("lithology1"))
        new = dict(
            id=fid, name=e.get("name") or d["name"], rank="formation",
            group=e.get("group") or ", ".join(sorted(d["group"])) or "",
            country=d["country"], regions=sorted(d["regions"]),
            location=dict(lat=med([float(r["lat"]) for r in sel]) if sel else None,
                          lng=med([float(r["lng"]) for r in sel]) if sel else None,
                          basis=f"median of {len(sel)} {basis}" if sel else "no coordinates in PBDB"),
            age=dict(first_ma=max(m[1] for m in d["ma"] or d["gen_ma"]),
                     last_ma=min(m[0] for m in d["ma"] or d["gen_ma"]),
                     note=e.get("age", {}).get("note", "") or ("Span of the PBDB ages of the beds that yielded the atlas genera."
                          if d["ma"] else "No PBDB age for these beds: span of the age of the atlas genera found here.")),
            environment=[k for k, _ in env.most_common()],
            lithology=[k for k, _ in lith.most_common(4)],
            pbdb_collections=sorted((r["collection_no"] for r in sel), key=int),
            summary=e.get("summary", ""), paleoenvironment=e.get("paleoenvironment", ""),
            sources=e.get("sources") or [dict(kind="database", text=(
                f"Paleobiology Database — collections of the {d['name']} (coordinates, environment, lithology; "
                f"downloaded 2026-11-16)."), url="https://paleobiodb.org/classic/displayCollResults?formation="
                + re.sub(r"\s+", "+", sorted(d["names"])[0] if d["names"] else ""))],
            curation=e.get("curation") or dict(status="draft", checked_by="", checked_on="", notes=[]),
        )
        p.write_text(yaml.safe_dump(new, allow_unicode=True, sort_keys=False, width=110))
    print(f"{len(forms)} formations")


ALL_COLS, BYNAME = {}, {}
if __name__ == "__main__":
    for raw in (ROOT / "data/raw").glob("*/pbdb_colls.json"):
        j = json.loads(raw.read_text())
        ALL_COLS.update(j["cols"])
        for k, v in j["byname"].items():
            BYNAME.setdefault(k, []).extend(v)
    main()
