"""Build the website data from the entries.

    python3 scripts/build.py

Reads   entries/<volume>/_volume.yaml, clades/*.yaml, genera/*.yaml, excluded.yaml
        entries/formations/*.yaml  (formations: the places shown in Biota mode)
        data/raw/paleomaps/  (Merdith et al. 2021 coastlines + reconstructed formation positions)
        data/tree/backbone.json  (tree-of-life nodes that are not entries)
        data/raw/timescale/pbdb_ics_2024.json  (ICS chart intervals, for search by time)
Writes  site/data.json  (everything the encyclopedia shows)
        site/paleo/<Ma>.json  (one simplified coastline map per time step, loaded on demand)
        site/life.json  (the whole tree: backbone + every entry)

Never edit site/data.json or site/life.json by hand: they are overwritten here.
"""
import json, pathlib, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "entries"


def load(p):
    return yaml.safe_load(p.read_text())


def genus_to_site(e):
    """Map an entry file (readable names) to the compact keys the site uses."""
    g = dict(
        name=e["name"], clade=e["parent"], isd=e["incertae_sedis"], isnote=e["placement_note"],
        sum=e["summary"], ws=e["size"]["wingspan_m"], wsnote=e["size"]["note"],
        holotype=e["fossil_material"]["holotype"], material=e["fossil_material"]["material"],
        completeness=e["fossil_material"]["completeness"], exceptional=e["fossil_material"]["exceptional"],
        biology=e["biology"], author=e["authority"],
        fad=e["age"]["first_ma"], lad=e["age"]["last_ma"], early=e["age"]["early_interval"], late=e["age"]["late_interval"],
        type_species=e["type_species"], pbdb_occ=e["age"]["pbdb_occurrences"],
        species=[dict(name=s["name"], author=s["authority"], fad=s["first_ma"], lad=s["last_ma"],
                      interval=s["interval"], ref=s["reference"]) for s in e["species"]],
        formations=[dict(id=f.get("id"), formation=f["formation"], group=f["group"], members=f["members"], country=f["country"],
                         regions=f["regions"], interval=f["interval"], n=f["occurrences"], ma=f["ma"])
                    for f in e["formations"]],
        images=[dict(kind=i["kind"], file=i["file"], src=i["url"], page=i["page"], artist=i["artist"],
                     license=i["license"], licurl=i["license_url"], date=i["date"], caption=i["caption"],
                     w=i["width"], h=i["height"], local=i.get("local"), review=i.get("review")) for i in e["images"]],
        sources=e["sources"],
    )
    if e["age"].get("note"):
        g["dates_note"] = e["age"]["note"]
    if e.get("silhouette"):
        g["silhouette"] = e["silhouette"]
    if e.get("external"):
        g["external"] = e["external"]
    return g


def clade_to_site(e):
    return dict(id=e["id"], name=e["name"], parent=e["parent"], wiki=e["wikipedia"], sum=e["summary"], trank=e.get("taxon_rank"),
                diag=e["diagnosis"], notes=e["notes"], sources=e["sources"])


PALEO = ROOT / "data/raw/paleomaps"


def formations_to_site(genera):
    """Formation entries + their reconstructed positions; writes one coastline file per map time."""
    fdir = ENTRIES / "formations"
    if not fdir.is_dir():
        return [], None
    pts = json.loads((PALEO / "formation_points.json").read_text())
    maps = json.loads((PALEO / "merdith2021_coastlines.json").read_text())
    out_dir = ROOT / "site/paleo"
    out_dir.mkdir(exist_ok=True)
    for old in out_dir.glob("*.json"):
        old.unlink()
    times = sorted(int(t) for t in maps["maps"])
    for t in times:
        (out_dir / f"{t}.json").write_text(json.dumps(maps["maps"][str(t)], separators=(",", ":")))
    pos = {}  # (formation id, present lng, lat) -> {Ma: [palaeo lng, lat]}
    for t, rows in pts["points"].items():
        for fid, lng, lat, plng, plat in rows:
            if plng is not None:
                pos.setdefault((fid, round(lng, 3), round(lat, 3)), {})[int(t)] = [plng, plat]
    here = {}
    for g in genera:
        for f in g["formations"]:
            here.setdefault(f["id"], []).append(g["name"])
    forms = []
    for p in sorted(fdir.glob("*.yaml")):
        e = load(p)
        loc = e["location"]
        pp = pos.get((e["id"], round(loc["lng"] or 0, 3), round(loc["lat"] or 0, 3)), {})
        forms.append(dict(id=e["id"], name=e["name"], group=e["group"], country=e["country"], regions=e["regions"],
                          lat=loc["lat"], lng=loc["lng"], basis=loc["basis"], fad=e["age"]["first_ma"],
                          lad=e["age"]["last_ma"], agenote=e["age"]["note"], env=e["environment"], lith=e["lithology"],
                          sum=e["summary"], paleoenv=e["paleoenvironment"], sources=e["sources"],
                          genera=sorted(here.get(e["id"], [])), pp=pp, ncol=len(e["pbdb_collections"])))
    paleo = dict(times=times, model=maps["model"], citation=maps["citation"], licence=maps["licence"],
                 via=maps["via"], note=maps["note"])
    return forms, paleo


def main():
    backbone = json.loads((ROOT / "data/tree/backbone.json").read_text())
    known = {n[0] for n in backbone}
    clades, genera, excluded, metas, tree = [], [], [], [], list(backbone)
    for vol in sorted(ENTRIES.glob("*/_volume.yaml")):
        v = load(vol)
        d = vol.parent
        cl = [load(p) for p in sorted((d / "clades").glob("*.yaml"))]
        gn = [load(p) for p in sorted((d / "genera").glob("*.yaml"))]
        if v["attach_to"] not in known:
            sys.exit(f"{vol}: attach_to '{v['attach_to']}' is not in the tree backbone")
        for c in cl:
            clades.append(clade_to_site(c))
            tree.append([c["id"], c["name"], c["parent"] or v["attach_to"], "e", "", "c", 1])
        for g in gn:
            genera.append(genus_to_site(g))
            tree.append([g["name"], g["name"], g["parent"], "e", "", "g", 1])
        excluded += load(d / "excluded.yaml") or []
        metas.append(v)
    ts = json.loads((ROOT / "data/raw/timescale/pbdb_ics_2024.json").read_text())
    timescale = [dict(name=r[0], type=r[1], base=r[2], top=r[3], parent=r[4], no=r[5], color=r[6]) for r in ts["records"]]
    formations, paleo = formations_to_site(genera)
    m = metas[0]
    data = dict(meta=dict(title="Atlas of Life", group=", ".join(x["title"] for x in metas), built=m["built"],
                          method=m["method"]),
                clades=clades, genera=genera, excluded=excluded, formations=formations, paleo=paleo,
                timescale=timescale, timescale_source=ts["reference"] + " Via " + ts["source"] + ".")
    (ROOT / "site/data.json").write_text(json.dumps(data, ensure_ascii=False))
    (ROOT / "site/life.json").write_text(json.dumps(tree, ensure_ascii=False))
    print(f"built: {len(genera)} genera, {len(clades)} clades, {len(excluded)} excluded names, {len(formations)} formations, {len(tree)} tree nodes")


if __name__ == "__main__":
    main()
