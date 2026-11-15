"""One-off migration (2026-11-15): split the prototype's site/data.json and
site/life.json into one YAML file per entry plus the tree backbone.

Kept for provenance only. After this migration the YAML files in entries/
are the source of truth; edit them, never data.json.
"""
import json, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
D = json.loads((ROOT / "site/data.json").read_text())
LIFE = json.loads((ROOT / "site/life.json").read_text())
VOL = ROOT / "entries/pterosauria"

# type species filled after the PBDB download (PBDB left the field empty)
FROM_MEMORY = {"Anhanguera", "Boreopterus", "Coloborhynchus", "Ctenochasma", "Darwinopterus", "Dendrorhynchoides",
               "Dimorphodon", "Eudimorphodon", "Gnathosaurus", "Maaradactylus", "Noripterus", "Nurhachius",
               "Nyctosaurus", "Pteranodon", "Rhamphorhynchus", "Sinopterus", "Tupandactylus"}
PBDB_EMPTY = {g for g in json.loads((ROOT / "data/raw/pterosauria/pbdb_taxa.json").read_text())["G"]}
pbdb_ts = {}
for row in PBDB_EMPTY:
    p = row.split("|")
    pbdb_ts[p[0]] = p[8] if len(p) > 8 else ""


class Dumper(yaml.SafeDumper):
    pass


def _str(d, s):
    style = "|" if "\n" in s else None
    return d.represent_scalar("tag:yaml.org,2002:str", s, style=style)


def _list(d, v):
    flow = all(isinstance(x, (int, float, str, type(None))) for x in v) and sum(len(str(x)) for x in v) < 70
    return d.represent_sequence("tag:yaml.org,2002:seq", v, flow_style=flow)


Dumper.add_representer(str, _str)
Dumper.add_representer(list, _list)


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.dump(obj, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=110))


def curation(notes):
    return dict(status="draft", checked_by="", checked_on="", notes=notes)


for g in D["genera"]:
    n = g["name"]
    notes = []
    ts_note = ""
    if n in FROM_MEMORY:
        ts_note = "Filled from general knowledge, not yet checked against the original description."
        notes.append("Verify type species against the original description.")
    elif not pbdb_ts.get(n) and n in pbdb_ts:
        ts_note = "PBDB gives no type species; taken as the only species listed."
    if not any(s["kind"] in ("original", "literature") for s in g["sources"]):
        notes.append("Only secondary sources: add the original description (primary literature).")
    if any(i["kind"] == "life" for i in g.get("images", [])):
        notes.append("Life restoration not yet reviewed for accuracy (see CLAUDE.md, images).")
    e = dict(
        name=n, rank="genus", parent=g["clade"],
        incertae_sedis=g["isd"], placement_note=g["isnote"],
        authority=g["author"], type_species=g.get("type_species", ""), type_species_note=ts_note,
        summary=g["sum"],
        size=dict(wingspan_m=g["ws"], note=g["wsnote"]),
        age=dict(first_ma=g["fad"], last_ma=g["lad"], early_interval=g["early"], late_interval=g["late"],
                 pbdb_occurrences=g["pbdb_occ"], note=g.get("dates_note", "")),
        species=[dict(name=s["name"], authority=s["author"], first_ma=s["fad"], last_ma=s["lad"],
                      interval=s["interval"], reference=s["ref"]) for s in g["species"]],
        formations=[dict(formation=f["formation"], group=f["group"], members=f["members"], country=f["country"],
                         regions=f["regions"], interval=f["interval"], occurrences=f["n"], ma=f["ma"])
                    for f in g["formations"]],
        fossil_material=dict(holotype=g["holotype"], material=g["material"], completeness=g["completeness"],
                             exceptional=g["exceptional"]),
        biology=g["biology"],
        images=[dict(kind=i["kind"], file=i["file"], url=i["src"], page=i["page"], artist=i["artist"],
                     license=i["license"], license_url=i["licurl"], date=i["date"], caption=i["caption"],
                     width=i["w"], height=i["h"], review="unreviewed") for i in g.get("images", [])],
        silhouette=g.get("silhouette"),
        sources=g["sources"],
        curation=curation(notes),
    )
    dump(VOL / "genera" / f"{n}.yaml", e)

for c in D["clades"]:
    e = dict(id=c["id"], name=c["name"], rank="clade", parent=c["parent"], wikipedia=c["wiki"],
             summary=c["sum"], diagnosis=c["diag"], notes=c["notes"], sources=c["sources"],
             curation=curation([]))
    dump(VOL / "clades" / f"{c['id']}.yaml", e)

dump(VOL / "excluded.yaml", D["excluded"])
dump(VOL / "_volume.yaml", dict(
    title="Pterosauria", root="pterosauria", attach_to="avemetatarsalia",
    built=D["meta"]["built"], method=D["meta"]["method"]))

covered = {g["name"] for g in D["genera"]} | {c["id"] for c in D["clades"]}
backbone = [n for n in LIFE if n[0] not in covered]
(ROOT / "data/tree/backbone.json").write_text(
    "[\n" + ",\n".join(json.dumps(n, ensure_ascii=False) for n in backbone) + "\n]\n")
print(len(D["genera"]), "genera,", len(D["clades"]), "clades,", len(backbone), "backbone nodes")
