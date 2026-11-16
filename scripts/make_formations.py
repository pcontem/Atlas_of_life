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


# Names of the same unit -> the name used for its formation entry, with the reason (shown on the entry)
ALIASES = {
    "Posidonienschiefer": ("Posidonia Shale", "German name of the Posidonia Shale (both spellings are used in PBDB)."),
    "Calcari di Zorzino": ("Zorzino Limestone", "Italian name of the Zorzino Limestone."),
    "Solnhofen": ("Altmühltal", "The Solnhofen limestones are the Solnhofen Member of the Altmühltal Formation "
                  "(Niebuhr & Pürner 2014; Rauhut et al. 2017, Zitteliana 89: 305–329)."),
}
MERGE_SOURCES = {"Altmühltal": dict(kind="literature", text=(
    "Rauhut, O. W. M., López-Arbarello, A., Röper, M. & Rothgaenger, M. 2017. Vertebrate fossils from the Kimmeridgian "
    "of Brunn: the oldest fauna from the Solnhofen Archipelago (Late Jurassic, Bavaria, Germany). Zitteliana 89: 305–329 "
    "(uses the lithostratigraphy of Niebuhr & Pürner 2014: Solnhofen Member of the Altmühltal Formation)."),
    url="https://epub.ub.uni-muenchen.de/40470/1/17_rauhut_305_329.pdf")}


def parts(name):
    """'Dolomia di Forni / Calcari di Zorzino' -> both; 'Caiuá Group (Rio Paraná / Goio-Erê)' -> all three."""
    m = re.match(r"(.*?)\s*\((.*)\)\s*$", name.strip())
    raw = re.split(r"\s*/\s*", m.group(1)) + re.split(r"\s*/\s*", m.group(2)) if m else re.split(r"\s*/\s*", name)
    out = [re.sub(r"\s+Formation$", "", x).strip() for x in raw if x.strip()]
    res = []  # the entry's name first, then the other names of the same unit (used to match PBDB records)
    for x in out:
        for y in ([ALIASES[x][0], x] if x in ALIASES else [x]):
            if y not in res:
                res.append(y)
    return res


def same(a, b):
    a, b = a.lower(), b.lower()
    return bool(a) and bool(b) and (a.startswith(b) or b.startswith(a))


def med(v):
    return round(statistics.median(v), 3)


def unnamed_unit(c, f):
    """Where a collection with no formation belongs: (id, name, names, note).
    1. its member or collection name is a PBDB member of a named formation -> that formation;
    2. its collection name contains the name of a formation of the same country -> that formation;
    3. PBDB gives its group -> one unit for the group's unassigned beds in that country;
    4. else one locality per region and nearby site (rounded to 0.25 degrees)."""
    if c:
        for key in (c.get("member"), c.get("collection_name")):
            for (mem, cc), parent in MEMBER_OF.items():
                if key and cc == f["country"] and re.search(r"\b" + re.escape(mem.lower()) + r"\b", key.lower()):
                    return (slug(parent + " " + f["country"]), parent, [parent],
                            f"Beds recorded without a formation in PBDB ({c['collection_name']}) belong to the {mem}, a member of the {parent} Formation.")
        for n in sorted(FORM_NAMES.get(f["country"], ()), key=len, reverse=True):
            core = re.sub(r"(?i)\b(limestone|shale|clay|marls?|sandstone|mudstone|formation|beds?)\b", "", n).strip()
            if len(core) > 4 and re.search(r"\b" + re.escape(core.lower()) + r"\b", (c.get("collection_name") or "").lower()):
                return (slug(n + " " + f["country"]), n, [n],
                        f"PBDB collection “{c['collection_name']}” has no formation but is a locality of the {n}.")
        if c.get("geological_group"):
            g = c["geological_group"]
            return (slug(f"{g} group {f['country']}"), f"{g} Group (beds not assigned to a formation)", [],
                    f"PBDB places these beds in the {g} Group without naming the formation.")
        # same site (0.25° cell) and same age bucket = one locality; named after the site
        site = re.sub(r"\s*\(.*?\)|\s+layer.*$|\s*\[.*?\]", "", c["collection_name"]).strip()
        mid = (float(c["max_ma"]) + float(c["min_ma"])) / 2
        cell = f"{round(float(c['lat'])*4)/4} {round(float(c['lng'])*4)/4} {round(mid/5)}"
        SITE_ID.setdefault(cell, slug(f"unnamed {site} {f['country']}"))
        return (SITE_ID[cell],
                f"Unnamed beds, {site}", [], None)
    return None


MEMBER_OF, FORM_NAMES, SITE_ID = {}, collections.defaultdict(set), {}


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
                    # unnamed beds: each PBDB collection is placed on its own (one genus item may span several sites)
                    used = [o["col"] for o in occ[e["name"]] if not o["form"] and (not f["regions"] or o["state"] in f["regions"])]
                    units = {}
                    for c in used:
                        u = unnamed_unit(cols.get(c), f)
                        units.setdefault(u[0], (u, []))[1].append(c)
                    if not units:  # no collection: keep a per-genus locality
                        where = ", ".join(f["regions"]) or f["country"]
                        units[slug(f"unnamed {where} {e['name']}")] = ((slug(f"unnamed {where} {e['name']}"),
                            f"Unnamed beds, {where}", [], None), [])
                else:
                    names = parts(name)
                    first = re.split(r"\s*/\s*|\s*\(", name)[0].strip()
                    note = ALIASES[first][1] if first in ALIASES else None
                    parent = MEMBER_OF.get((names[0], f["country"]))
                    if parent and parent != names[0]:
                        note = f"PBDB records the {names[0]} as a member of the {parent} Formation."
                        names = [parent] + names
                    fid = slug(names[0] + " " + f["country"])
                    used = [o["col"] for o in occ[e["name"]] if any(same(o["form"], n) for n in names)]
                    units = {fid: ((fid, names[0], names, note), used)}
                ids = []
                for fid, ((_, title, names, note), used) in units.items():
                    d = forms.setdefault(fid, dict(name=title, names=set(), country=f["country"], regions=set(),
                                                   cols=set(), ma=[], genera=set(), group=set(), notes=set()))
                    d["names"] |= set(names)
                    d["regions"] |= set(f["regions"])
                    d["cols"] |= {c for c in used if c in cols}
                    if note:
                        d["notes"].add(note)
                    if f.get("group"):
                        d["group"].add(f["group"])
                    ma = [[float(cols[c]["min_ma"]), float(cols[c]["max_ma"])] for c in used if c in cols] if name == "Unnamed unit" else []
                    if ma:
                        d["ma"] += ma
                    elif f.get("ma") and name != "Unnamed unit":
                        d["ma"].append(f["ma"])
                    else:  # no PBDB age for this bed: fall back on the genus age
                        d.setdefault("gen_ma", []).append([e["age"]["last_ma"], e["age"]["first_ma"]])
                    d["genera"].add(e["name"])
                    ids.append(fid)
                new_id = ids[0] if len(ids) == 1 else sorted(ids)
                if f.get("id") != new_id:
                    f["id"] = new_id
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
            includes=sorted(d["notes"]),
            summary=e.get("summary", ""), paleoenvironment=e.get("paleoenvironment", ""),
            sources=e.get("sources") or ([MERGE_SOURCES[d["name"]]] if d["name"] in MERGE_SOURCES else []) + [dict(kind="database", text=(
                f"Paleobiology Database — collections of the {d['name']} (coordinates, environment, lithology; "
                f"downloaded 2026-11-16)."), url="https://paleobiodb.org/classic/displayCollResults?formation="
                + re.sub(r"\s+", "+", sorted(d["names"])[0] if d["names"] else ""))],
            curation=e.get("curation") or dict(status="draft", origin="ai-draft", checked_by="", checked_on="", notes=[], reviews=[]),
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
    # PBDB members of formations (member name, country) -> formation, and formation names per country
    CC = {v: k for k, v in COUNTRY.items()}
    for recs in BYNAME.values():
        for r in recs:
            m = r.get("member") or ""
            if len(m) >= 5 and r.get("formation") and m != r["formation"] and not re.match(r"(?i)(upper|lower|middle|basal|top)\b", m):
                MEMBER_OF.setdefault((r["member"], COUNTRY.get(r.get("cc"), r.get("cc"))), ALIASES.get(r["formation"], (r["formation"],))[0])
    for raw in (ROOT / "entries").glob("*/genera/*.yaml"):
        for f in yaml.safe_load(raw.read_text())["formations"]:
            if f["formation"] != "Unnamed unit":
                FORM_NAMES[f["country"]].add(parts(f["formation"])[0])
    main()
