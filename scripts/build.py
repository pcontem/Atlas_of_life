"""Build the website data from the entries.

    python3 scripts/build.py

Reads   entries/<volume>/_volume.yaml, clades/*.yaml, genera/*.yaml, excluded.yaml
        data/tree/backbone.json  (tree-of-life nodes that are not entries)
        data/raw/timescale/pbdb_ics_2024.json  (ICS chart intervals, for search by time)
Writes  site/data.json  (everything the encyclopedia shows)
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
        formations=[dict(formation=f["formation"], group=f["group"], members=f["members"], country=f["country"],
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
    m = metas[0]
    data = dict(meta=dict(title="Atlas of Life", group=", ".join(x["title"] for x in metas), built=m["built"],
                          method=m["method"]),
                clades=clades, genera=genera, excluded=excluded,
                timescale=timescale, timescale_source=ts["reference"] + " Via " + ts["source"] + ".")
    (ROOT / "site/data.json").write_text(json.dumps(data, ensure_ascii=False))
    (ROOT / "site/life.json").write_text(json.dumps(tree, ensure_ascii=False))
    print(f"built: {len(genera)} genera, {len(clades)} clades, {len(excluded)} excluded names, {len(tree)} tree nodes")


if __name__ == "__main__":
    main()
