"""Refresh the PBDB downloads of each volume (runs in GitHub Actions: .github/workflows/data-refresh.yml).

    python3 scripts/fetch/pbdb.py [volume ...]     # default: every volume in entries/

Writes data/raw/<volume>/pbdb_occs.json   occurrences of the volume's root taxon, one row per occurrence:
        genus|accepted_name|identified_name|formation|member|group|cc|state|early|late|max_ma|min_ma|
        col:<n>|ref:<n>|lng|lat|geogcomments   (the layout make_formations.py reads)
       data/raw/<volume>/pbdb_colls.json  collections: every collection with an occurrence, plus every
        collection of each formation named in the genus entries (coordinates, environment, lithology)
       /tmp/pbdb_report.md                genera PBDB lists as valid that the atlas has neither as an
        entry nor in excluded.yaml (for the pull-request text)
Genus entries are never changed here: they are curated by hand.
"""
import datetime, json, pathlib, sys, time, urllib.parse, urllib.request
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
API = "https://paleobiodb.org/data1.2"
COLL_FIELDS = ["collection_no", "lng", "lat", "collection_name", "max_ma", "min_ma", "environment", "lithology1",
               "lithology2", "cc", "state", "formation", "geological_group", "member", "n_occs", "reference_no"]


def get(path, **params):
    url = f"{API}/{path}?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "atlas-of-life data refresh"}), timeout=120) as r:
                return json.loads(r.read())["records"]
        except Exception as e:  # network hiccup: wait and retry
            if attempt == 3:
                raise SystemExit(f"PBDB request failed: {url}: {e}")
            time.sleep(5 * (attempt + 1))


def occ_row(r):
    """One PBDB occurrence (vocab=pbdb) -> the pipe-separated row, or None if not identified to a genus."""
    if r.get("accepted_rank") not in ("genus", "subgenus", "species", "subspecies"):
        return None
    genus = r["accepted_name"].split()[0]
    f = lambda k: str(r.get(k, "") or "")
    return "|".join([genus, f("accepted_name"), f("identified_name"), f("formation"), f("member"), f("geological_group"),
                     f("cc"), f("state"), f("early_interval"), f("late_interval"), f("max_ma"), f("min_ma"),
                     "col:" + f("collection_no"), "ref:" + f("reference_no"), f("lng"), f("lat"), f("geogcomments")])


def coll(r):
    return {k: r.get(k) for k in COLL_FIELDS}


def formation_names(vol):
    sys.path.insert(0, str(ROOT / "scripts"))
    from make_formations import parts
    names = set()
    for gp in (ROOT / "entries" / vol / "genera").glob("*.yaml"):
        for f in yaml.safe_load(gp.read_text())["formations"]:
            if f["formation"] != "Unnamed unit":
                names |= {n for n in parts(f["formation"]) if not n.endswith(" Group")}
    return sorted(names)


def refresh(vol):
    meta = yaml.safe_load((ROOT / "entries" / vol / "_volume.yaml").read_text())
    raw = ROOT / "data/raw" / vol
    raw.mkdir(parents=True, exist_ok=True)
    recs = get("occs/list.json", base_name=meta["title"], show="coords,loc,strat", vocab="pbdb")
    rows = [x for x in (occ_row(r) for r in recs) if x]
    (raw / "pbdb_occs.json").write_text(json.dumps(rows, ensure_ascii=False))
    ids = sorted({r.split("|")[12][4:] for r in rows}, key=int)
    cols = {}
    for i in range(0, len(ids), 150):
        for r in get("colls/list.json", id=",".join(ids[i:i + 150]), show="geo,lith,loc,strat", vocab="pbdb"):
            cols[str(r["collection_no"])] = coll(r)
    byname = {n: [coll(r) for r in get("colls/list.json", formation=n, show="geo,lith,loc,strat", vocab="pbdb")]
              for n in formation_names(vol)}
    (raw / "pbdb_colls.json").write_text(json.dumps(dict(cols=cols, byname=byname,
                                                         downloaded=datetime.date.today().isoformat()), ensure_ascii=False))
    # genera PBDB has that the atlas does not (new descriptions, or names to add to excluded.yaml)
    have = {p.stem for p in (ROOT / "entries" / vol / "genera").glob("*.yaml")}
    have |= {x["name"] for x in yaml.safe_load((ROOT / "entries" / vol / "excluded.yaml").read_text()) or []}
    new = sorted({r.split("|")[0] for r in rows} - have)
    print(f"{vol}: {len(rows)} occurrences, {len(cols)} collections, {len(byname)} formations; {len(new)} genera not in the atlas")
    return vol, new


def main():
    vols = sys.argv[1:] or sorted(p.parent.name for p in (ROOT / "entries").glob("*/_volume.yaml"))
    report = ["## PBDB genera not in the atlas", ""]
    for vol, new in map(refresh, vols):
        report.append(f"- **{vol}**: " + (", ".join(f"*{g}*" for g in new) if new else "none"))
    pathlib.Path("/tmp/pbdb_report.md").write_text("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
