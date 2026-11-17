"""Build the website data from the entries.

    python3 scripts/build.py

Reads   entries/<volume>/_volume.yaml, clades/*.yaml, genera/*.yaml, excluded.yaml
        entries/formations/*.yaml  (formations: the places shown in Biota mode)
        data/raw/paleomaps/  (Merdith et al. 2021 coastlines + reconstructed formation positions)
        data/tree/backbone.json  (tree-of-life nodes that are not entries)
        data/raw/timescale/pbdb_ics_2024.json  (ICS chart intervals, for search by time)
Writes  site/data.json  (the index every view needs: clades, light genus records, formations, timescale)
        site/g/<Genus>.json  (one full genus entry each, loaded on demand by the entry page)
        site/paleo/<Ma>.json  (one simplified coastline map per time step, loaded on demand)
        site/life.json  (the whole tree: backbone + every entry)

Never edit site/data.json or site/life.json by hand: they are overwritten here.
"""
import json, pathlib, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRIES = ROOT / "entries"


def load(p):
    e = yaml.safe_load(p.read_text())
    if isinstance(e, dict) and "curation" in e:
        e["_src"] = p.resolve().relative_to(ROOT).as_posix()   # shown as "Edit this entry" on the site
    return e


def genus_to_site(e):
    """Map an entry file (readable names) to the compact keys the site uses."""
    g = dict(
        name=e["name"], clade=e["parent"], isd=e["incertae_sedis"], isnote=e["placement_note"],
        sum=e["summary"], wsnote=e["size"]["note"],
        holotype=e["fossil_material"]["holotype"], material=e["fossil_material"]["material"],
        completeness=e["fossil_material"]["completeness"], exceptional=e["fossil_material"]["exceptional"],
        biology=e["biology"], author=e["authority"],
        fad=e["age"]["first_ma"], lad=e["age"]["last_ma"], early=e["age"]["early_interval"], late=e["age"]["late_interval"],
        type_species=e["type_species"], pbdb_occ=e["age"]["pbdb_occurrences"],
        species=[dict(name=s["name"], author=s["authority"], fad=s["first_ma"], lad=s["last_ma"],
                      interval=s["interval"], ref=s["reference"]) for s in e["species"]],
        formations=[dict(ids=f["id"] if isinstance(f.get("id"), list) else [f.get("id")], formation=f["formation"], group=f["group"], members=f["members"], country=f["country"],
                         regions=f["regions"], interval=f["interval"], n=f["occurrences"], ma=f["ma"])
                    for f in e["formations"]],
        images=[dict(kind=i["kind"], file=i["file"], src=i["url"], page=i["page"], artist=i["artist"],
                     license=i["license"], licurl=i["license_url"], date=i["date"], caption=i["caption"],
                     w=i["width"], h=i["height"], local=i.get("local"), review=i.get("review")) for i in e["images"]],
        sources=e["sources"],
    )
    # size: wingspan (pterosaurs) or body length, plus body mass when published; [min, max]
    for key, k in (("wingspan_m", "ws"), ("length_m", "len"), ("mass_kg", "kg")):
        if key in e["size"]:
            g[k] = e["size"][key]
    if e.get("extant"):
        g["extant"] = True
    if e["age"].get("note"):
        g["dates_note"] = e["age"]["note"]
    if e.get("silhouette"):
        g["silhouette"] = e["silhouette"]
    if e.get("external"):
        g["external"] = e["external"]
    g["cur"] = curation_to_site(e)
    return g


def curation_to_site(e):
    c = e.get("curation") or {}
    return dict(status=c.get("status", "draft"), origin=c.get("origin", "ai-draft"), by=c.get("checked_by", ""),
                on=c.get("checked_on", ""), reviews=c.get("reviews") or [], src=e.get("_src", ""))


INDEX_KEYS = ("name", "clade", "isd", "sum", "ws", "len", "kg", "extant", "fad", "lad", "early", "late", "author", "type_species", "silhouette")


def genus_index(g, vol):
    """The light record every view needs (lists, tree, timeline, maps); the full entry is in site/g/<Name>.json.
    `images` holds only the representative image (first life restoration, else the first image)."""
    rep = next((i for i in g["images"] if i["kind"] == "life"), g["images"][0] if g["images"] else None)
    r = {k: g[k] for k in INDEX_KEYS if k in g}
    r.update(vol=vol, nsp=len(g["species"]), st=g["cur"]["status"], images=[rep] if rep else [],
             formations=[dict(ids=f["ids"], country=f["country"]) for f in g["formations"]])
    return r


def clade_to_site(e):
    return dict(id=e["id"], name=e["name"], parent=e["parent"], wiki=e["wikipedia"], sum=e["summary"], trank=e.get("taxon_rank"), trank_src=e.get("taxon_rank_source", ""),
                diag=e["diagnosis"], notes=e["notes"], sources=e["sources"], cur=curation_to_site(e))


PALEO = ROOT / "data/raw/paleomaps"


def clean_coastlines(polys):
    """Make the raw coastline polygons (coordinates ×10) safe for spherical drawing in d3.
    Vertices exactly on the antimeridian (±180°) near a pole confuse d3's antimeridian clipping, which
    then fills the whole globe (seen at 0 Ma); they are moved 0.1° inside. Slivers lying entirely on a
    pole (|lat| ≥ 89.5°, seen at 230 Ma) have no area and are dropped."""
    out = []
    for poly in polys:
        if all(abs(y) >= 895 for x, y in poly[0]):
            continue
        out.append([[[1799 if x >= 1800 else -1799 if x <= -1800 else x, y] for x, y in ring] for ring in poly])
    return out


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
        polys = clean_coastlines(maps["maps"][str(t)])
        (out_dir / f"{t}.json").write_text(json.dumps(polys, separators=(",", ":")))
    pos = {}  # (formation id, present lng, lat) -> {Ma: [palaeo lng, lat]}
    for t, rows in pts["points"].items():
        for fid, lng, lat, plng, plat in rows:
            if plng is not None:
                pos.setdefault((fid, round(lng, 3), round(lat, 3)), {})[int(t)] = [plng, plat]
    here = {}
    for g in genera:
        for f in g["formations"]:
            for fid in f["ids"]:
                here.setdefault(fid, []).append(g["name"])
    forms = []
    for p in sorted(fdir.glob("*.yaml")):
        e = load(p)
        loc = e["location"]
        pp = pos.get((e["id"], round(loc["lng"] or 0, 3), round(loc["lat"] or 0, 3)), {})
        forms.append(dict(id=e["id"], name=e["name"], group=e["group"], country=e["country"], regions=e["regions"],
                          lat=loc["lat"], lng=loc["lng"], basis=loc["basis"], fad=e["age"]["first_ma"],
                          lad=e["age"]["last_ma"], agenote=e["age"]["note"], env=e["environment"], lith=e["lithology"],
                          sum=e["summary"], paleoenv=e["paleoenvironment"], sources=e["sources"],
                          genera=sorted(set(here.get(e["id"], []))), pp=pp, includes=e.get("includes") or [],
                          cur=curation_to_site(e), ncol=len(e["pbdb_collections"])))
    paleo = dict(times=times, model=maps["model"], citation=maps["citation"], licence=maps["licence"],
                 via=maps["via"], note=maps["note"])
    return forms, paleo


def main():
    backbone = json.loads((ROOT / "data/tree/backbone.json").read_text())
    known = {n[0] for n in backbone}
    clades, genera, excluded, metas, tree = [], [], [], [], [list(n) for n in backbone]
    vol_clades = set()
    # clade entries for groups of the tree backbone (entries/tree/clades): the node keeps its place and name
    # in backbone.json and is marked as having an entry
    node_at = {n[0]: n for n in tree}
    for p in sorted((ENTRIES / "tree/clades").glob("*.yaml")):
        c = load(p)
        n = node_at.get(c["id"])
        if not n:
            sys.exit(f"{p}: '{c['id']}' is not in the tree backbone")
        n[6] = 1
        clades.append(dict(clade_to_site(c), scope="tree"))
    for vol in sorted(ENTRIES.glob("*/_volume.yaml")):
        v = load(vol)
        d = vol.parent
        cl = [load(p) for p in sorted((d / "clades").glob("*.yaml"))]
        gn = [load(p) for p in sorted((d / "genera").glob("*.yaml"))]
        if v["attach_to"] not in known:
            sys.exit(f"{vol}: attach_to '{v['attach_to']}' is not in the tree backbone")
        for c in cl:
            clades.append(clade_to_site(c))
            tree.append([c["id"], c["name"], c["parent"] or v["attach_to"], "", "", "c", 1])
        for g in gn:
            genera.append(genus_to_site(g))
            genera[-1]["vol"] = d.name
            tree.append([g["name"], g["name"], g["parent"], "v" if g.get("extant") else "e", "", "g", 1])
        vol_clades |= {c["id"] for c in cl}
        excluded += load(d / "excluded.yaml") or []
        metas.append(v)
    # volume clades: living if any genus below them (entry or backbone genus) is living, otherwise extinct
    up = {n[0]: n[2] for n in tree}
    living = set()
    for n in tree:
        if n[5] == "g" and n[3] == "v":
            k = n[2]
            while k and k not in living:
                living.add(k)
                k = up.get(k)
    for n in tree:
        if n[0] in vol_clades:
            n[3] = "v" if n[0] in living else "e"
    for c in clades:
        if c["id"] in vol_clades:
            c["status"] = "v" if c["id"] in living else "e"
    ts = json.loads((ROOT / "data/raw/timescale/pbdb_ics_2024.json").read_text())
    timescale = [dict(name=r[0], type=r[1], base=r[2], top=r[3], parent=r[4], no=r[5], color=r[6]) for r in ts["records"]]
    formations, paleo = formations_to_site(genera)
    home = load(ENTRIES / "home.yaml") if (ENTRIES / "home.yaml").exists() else None
    m = max(metas, key=lambda x: str(x["built"]))
    media_cfg = json.loads((ROOT / "media/config.json").read_text()) if (ROOT / "media/config.json").exists() else {}
    base = (media_cfg.get("base_url") or "").strip()
    data = dict(media_base=base + ("/" if base and not base.endswith("/") else ""),meta=dict(title="Atlas of Life", group=", ".join(x["title"] for x in metas), built=m["built"],
                          method=m["method"]),
                clades=clades, genera=genera, excluded=excluded, formations=formations, paleo=paleo, home=home,
                timescale=timescale, timescale_source=ts["reference"] + " Via " + ts["source"] + ".")
    # full genus entries, one file each, loaded when an entry page is opened
    gdir = ROOT / "site/g"
    gdir.mkdir(exist_ok=True)
    for old in gdir.glob("*.json"):
        old.unlink()
    for g in genera:
        (gdir / f"{g['name']}.json").write_text(json.dumps(g, ensure_ascii=False))
    data["genera"] = [genus_index(g, g["vol"]) for g in genera]
    (ROOT / "site/data.json").write_text(json.dumps(data, ensure_ascii=False))
    (ROOT / "site/life.json").write_text(json.dumps(tree, ensure_ascii=False))
    print(f"built: {len(genera)} genera, {len(clades)} clades, {len(excluded)} excluded names, {len(formations)} formations, {len(tree)} tree nodes")


if __name__ == "__main__":
    main()
