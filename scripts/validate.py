"""Check every entry against the rules in CLAUDE.md ("Entry rules").

    python3 scripts/validate.py            # errors only: must pass before every commit
    python3 scripts/validate.py --strict   # also the consolidation rules (goal: pass for Pterosauria)
    python3 scripts/validate.py --report   # write docs/CONSOLIDATION.md (to-do list per entry)

Each problem is printed with its rule code (e.g. G5) so it can be looked up in CLAUDE.md.
ERROR  = breaks the atlas; fix before committing.
STRICT = allowed while an entry is a draft; must be fixed before the volume is "consolidated".
"""
import json, pathlib, re, sys, collections
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "site"

COMPLETENESS = {"complete", "near-complete", "partial", "fragmentary", "multiple"}
IMAGE_KINDS = {"life", "fossil", "skeletal"}
IMAGE_REVIEW = {"unreviewed", "accepted", "outdated"}
MAX_PER_KIND = 8
SOURCE_KINDS = {"original", "literature", "database", "encyclopedia"}
LICENSE_OK = re.compile(r"^(CC0|Public domain|CC BY(-SA)? \d\.\d)$")
SIL_LICENSE_OK = re.compile(r"creativecommons\.org/(publicdomain|licenses/by(-sa)?/)")
CURATION = {"draft", "checked"}
TAXON_RANKS = {"kingdom", "phylum", "class", "subclass", "order", "suborder", "infraorder", "superfamily",
               "family", "subfamily", "tribe", "unranked clade"}
EXCLUDED_STATUS = {"nomen dubium", "nomen nudum", "nomen inquirendum", "junior synonym"}
YEAR = re.compile(r"\b(1[7-9]\d\d|20\d\d)\b")

problems = []  # (level, rule, where, message)


def err(rule, where, msg):
    problems.append(("ERROR", rule, where, msg))


def strict(rule, where, msg):
    problems.append(("STRICT", rule, where, msg))


def img_key(name, kind):
    return SITE / "img" / (re.sub(r"[^A-Za-z]", "", name) + "_" + kind + ".webp")


def check_sources(where, sources, need_original):
    if not sources:
        err("S1", where, "no sources")
        return
    for s in sources:
        if s.get("kind") not in SOURCE_KINDS:
            err("S1", where, f"source kind '{s.get('kind')}' not in {sorted(SOURCE_KINDS)}")
        if not (s.get("text") or "").strip():
            err("S1", where, "source without text")
        if s.get("kind") == "encyclopedia" and "oldid=" not in (s.get("url") or ""):
            err("S3", where, "Wikipedia source must link a fixed revision (url with oldid=)")
    kinds = {s.get("kind") for s in sources}
    if need_original and "original" not in kinds:
        strict("S2", where, "no 'original' source (the publication that named the taxon)")
    if not kinds & {"original", "literature"}:
        strict("S2", where, "only secondary sources (database/encyclopedia); add primary literature")


def check_genus(e, path, clade_ids, excluded_names):
    n = e.get("name", "?")
    w = f"genus {n}"
    if path.stem != n:
        err("G1", w, f"file name {path.name} must be {n}.yaml")
    if n in excluded_names:
        err("G1", w, "also listed in excluded.yaml")
    if e.get("rank") != "genus":
        err("G1", w, "rank must be 'genus'")
    if e.get("parent") not in clade_ids:
        err("G2", w, f"parent '{e.get('parent')}' is not a clade of this volume")
    if e.get("incertae_sedis") not in (True, False):
        err("G3", w, "incertae_sedis must be true or false")
    if e.get("incertae_sedis") and not (e.get("placement_note") or "").strip():
        err("G3", w, "incertae sedis needs a placement_note explaining the conflicting placements")
    if not YEAR.search(e.get("authority") or ""):
        err("G4", w, "authority must be 'Author(s) year'")
    ts = e.get("type_species") or ""
    sp = e.get("species") or []
    if not ts:
        err("G5", w, "type_species is empty")
    elif not ts.startswith(n + " "):
        err("G5", w, f"type species '{ts}' does not belong to {n}")
    if ts and sp and ts not in [s["name"] for s in sp]:
        strict("G5", w, f"type species '{ts}' is not in the species list")
    if (e.get("type_species_note") or "").startswith("Filled from general knowledge"):
        strict("G5", w, "type species not verified against a source")
    if not sp:
        strict("G6", w, "no species listed (every valid genus has at least its type species)")
    for s in sp:
        if not s["name"].startswith(n + " "):
            err("G6", w, f"species '{s['name']}' does not start with the genus name")
        if not YEAR.search(s.get("authority") or ""):
            err("G6", w, f"species '{s['name']}' has no authority year")
    sm = (e.get("summary") or "").strip()
    if not sm:
        err("G7", w, "summary is empty")
    elif len(sm) > 170 or not sm.endswith("."):
        strict("G7", w, f"summary must be one sentence ending in '.', ≤170 characters (now {len(sm)})")
    size = e.get("size") or {}
    ws = size.get("wingspan_m")
    if ws is not None:
        if not (isinstance(ws, list) and len(ws) == 2 and all(isinstance(x, (int, float)) for x in ws) and 0 < ws[0] <= ws[1] < 15):
            err("G8", w, f"wingspan_m must be [min, max] in metres, got {ws}")
    elif not (size.get("note") or "").strip():
        strict("G8", w, "no wingspan: give one, or say in size.note why it is unknown")
    a = e.get("age") or {}
    fa, la = a.get("first_ma"), a.get("last_ma")
    if not (isinstance(fa, (int, float)) and isinstance(la, (int, float)) and fa >= la > 0):
        err("G9", w, f"age first_ma ≥ last_ma > 0 required, got {fa}, {la}")
    if not a.get("early_interval"):
        err("G9", w, "age.early_interval is empty")
    if not a.get("pbdb_occurrences") and not (a.get("note") or "").strip():
        err("G9", w, "age not from PBDB occurrences: age.note must say where it comes from")
    if not e.get("formations"):
        err("G10", w, "no geological formation")
    for f in e.get("formations") or []:
        if not f.get("formation") or not f.get("country"):
            err("G10", w, "formation without name or country")
    fm = e.get("fossil_material") or {}
    if not (fm.get("holotype") or "").strip() or not (fm.get("material") or "").strip():
        err("G11", w, "fossil_material needs holotype and material")
    if fm.get("completeness") not in COMPLETENESS:
        err("G11", w, f"completeness must be one of {sorted(COMPLETENESS)}")
    if not (e.get("biology") or "").strip():
        err("G12", w, "biology is empty")
    imgs = e.get("images") or []
    for i in imgs:
        iw = f"{w} image {i.get('file')}"
        if i.get("kind") not in IMAGE_KINDS:
            err("I1", iw, f"kind must be one of {sorted(IMAGE_KINDS)}")
        for k in ("url", "page", "artist", "license", "caption"):
            if not i.get(k):
                err("I2", iw, f"missing {k}")
        if "commons.wikimedia.org" not in (i.get("page") or ""):
            err("I2", iw, "page must be the Wikimedia Commons file page")
        if not LICENSE_OK.match(i.get("license") or ""):
            err("I3", iw, f"licence '{i.get('license')}' not allowed (CC0, public domain, CC BY, CC BY-SA)")
        if i.get("review") not in IMAGE_REVIEW:
            err("I4", iw, f"review must be one of {sorted(IMAGE_REVIEW)}")
        elif i.get("kind") == "life" and i["review"] != "accepted":
            strict("I4", iw, f"life restoration is '{i['review']}': review it for accuracy")
        loc = SITE / i["local"] if i.get("local") else img_key(n, i.get("kind", ""))
        if not loc.exists():
            err("I5", iw, f"local copy missing: {loc.relative_to(ROOT)}")
    per_kind = collections.Counter(i.get("kind") for i in imgs)
    for k, c in per_kind.items():
        if c > MAX_PER_KIND:
            err("I1", w, f"{c} images of kind '{k}' (max {MAX_PER_KIND})")
    if len({i.get("file") for i in imgs}) < len(imgs):
        err("I1", w, "the same Commons file is listed twice")
    if not imgs:
        strict("I6", w, "no image")
    sil = e.get("silhouette")
    if sil:
        lic = sil.get("license") or ""
        if "/by-nc" in lic and "-nd" not in lic:
            strict("I3", w, f"silhouette is non-commercial only ({lic}); replace with a CC0/BY/BY-SA one if available")
        elif not SIL_LICENSE_OK.search(lic):
            err("I3", w, f"silhouette licence not allowed: {lic}")
        if not sil.get("attribution"):
            err("I2", w, "silhouette without attribution")
        uid = (sil.get("page") or "").split("/images/")[-1]
        if not (SITE / "sil" / f"{uid}.webp").exists():
            err("I5", w, f"local silhouette missing: site/sil/{uid}.webp")
    check_sources(w, e.get("sources"), need_original=True)
    check_curation(w, e.get("curation"))


def check_curation(w, c):
    c = c or {}
    if c.get("status") not in CURATION:
        err("Q1", w, f"curation.status must be one of {sorted(CURATION)}")
        return
    if c["status"] == "checked":
        if not c.get("checked_by") or not c.get("checked_on"):
            err("Q1", w, "checked entries need checked_by and checked_on")
        if c.get("notes"):
            err("Q1", w, "checked entries cannot have open curation notes")
    else:
        strict("Q1", w, "draft: " + ("; ".join(c.get("notes") or []) or "not yet checked"))


def check_clade(e, path, clade_ids, root):
    w = f"clade {e.get('id')}"
    if path.stem != e.get("id"):
        err("C1", w, f"file name {path.name} must be {e.get('id')}.yaml")
    if e.get("id") != (e.get("id") or "").lower():
        err("C1", w, "id must be lowercase")
    if e.get("rank") != "clade":
        err("C1", w, "rank must be 'clade'")
    if e.get("id") == root:
        if e.get("parent") is not None:
            err("C1", w, "the volume root has parent: null (attach_to in _volume.yaml places it)")
    elif e.get("parent") not in clade_ids:
        err("C1", w, f"parent '{e.get('parent')}' is not a clade of this volume")
    if e.get("taxon_rank") not in TAXON_RANKS:
        err("C4", w, f"taxon_rank must be one of {sorted(TAXON_RANKS)} (from PBDB or the literature, with taxon_rank_source)")
    elif not e.get("taxon_rank_source"):
        err("C4", w, "taxon_rank_source is empty")
    if not (e.get("summary") or "").strip():
        err("C2", w, "summary is empty")
    if len(e.get("diagnosis") or []) < 2:
        err("C2", w, "diagnosis needs at least two features")
    check_sources(w, e.get("sources"), need_original=False)
    check_curation(w, e.get("curation"))


def check_volume(vdir, backbone, all_names):
    v = yaml.safe_load((vdir / "_volume.yaml").read_text())
    clades = {p: yaml.safe_load(p.read_text()) for p in sorted((vdir / "clades").glob("*.yaml"))}
    genera = {p: yaml.safe_load(p.read_text()) for p in sorted((vdir / "genera").glob("*.yaml"))}
    excluded = yaml.safe_load((vdir / "excluded.yaml").read_text()) or []
    clade_ids = {c["id"] for c in clades.values()}
    if v["root"] not in clade_ids:
        err("V1", vdir.name, f"root '{v['root']}' has no clade file")
    if v["attach_to"] not in backbone:
        err("V1", vdir.name, f"attach_to '{v['attach_to']}' is not in data/tree/backbone.json")
    ex_names = set()
    for x in excluded:
        if x.get("status") not in EXCLUDED_STATUS:
            err("X1", f"excluded {x.get('name')}", f"status must be one of {sorted(EXCLUDED_STATUS)}")
        if not (x.get("ref") or x.get("source")):
            err("X1", f"excluded {x.get('name')}", "needs ref or source")
        if x.get("parent") not in clade_ids and x.get("parent") not in {g["name"] for g in genera.values()}:
            err("X2", f"excluded {x.get('name')}", f"parent '{x.get('parent')}' must be a clade or genus of this volume")
        ex_names.add(x.get("name"))
    for p, c in clades.items():
        check_clade(c, p, clade_ids, v["root"])
    for p, g in genera.items():
        check_genus(g, p, clade_ids, ex_names)
        all_names[g["name"]].append(vdir.name)
    # every clade reaches the root and holds at least one genus
    parent = {c["id"]: c["parent"] for c in clades.values()}
    for cid in clade_ids:
        seen, k = set(), cid
        while k is not None and k not in seen:
            seen.add(k)
            k = parent.get(k)
        if k is not None:
            err("C3", f"clade {cid}", "parent chain loops")
    used = collections.Counter()
    for g in genera.values():
        k = g["parent"]
        while k:
            used[k] += 1
            k = parent.get(k)
    for cid in clade_ids:
        if not used[cid]:
            err("C3", f"clade {cid}", "contains no genus")
    # English names on the path from the root of life to the volume
    names = {n[0]: n for n in backbone.values()}
    k = v["attach_to"]
    while k:
        node = names.get(k)
        if not node:
            break
        if re.search(r"\((?:[^)]*\b(da|das|do|dos|com|linhagem|animais|répteis|aves)\b)", node[1]):
            strict("L1", f"tree node {k}", f"name is not in English: '{node[1]}'")
        k = node[2]
    return clades, genera


def main():
    args = set(sys.argv[1:])
    backbone = {n[0]: n for n in json.loads((ROOT / "data/tree/backbone.json").read_text())}
    all_names = collections.defaultdict(list)
    vols = sorted(p.parent for p in (ROOT / "entries").glob("*/_volume.yaml"))
    for vd in vols:
        check_volume(vd, backbone, all_names)
    for n, vs in all_names.items():
        if len(vs) > 1 or n in backbone:
            err("G1", f"genus {n}", "name appears more than once in the atlas")
    errors = [p for p in problems if p[0] == "ERROR"]
    stricts = [p for p in problems if p[0] == "STRICT"]
    if "--report" in args:
        write_report(stricts + errors)
    shown = problems if ("--strict" in args) else errors
    for lvl, rule, where, msg in shown:
        print(f"{lvl:6} {rule:3} {where}: {msg}")
    print(f"\n{len(errors)} error(s), {len(stricts)} consolidation issue(s) "
          f"({len({p[2] for p in stricts})} entries) — see CLAUDE.md for rule codes")
    fail = errors or ("--strict" in args and stricts)
    sys.exit(1 if fail else 0)


def write_report(items):
    by_rule = collections.Counter(p[1] for p in items)
    by_entry = collections.defaultdict(list)
    for lvl, rule, where, msg in items:
        by_entry[where.split(" image ")[0]].append(f"{rule} {msg}")
    lines = ["# Consolidation report", "",
             "Generated by `python3 scripts/validate.py --report`. Do not edit by hand.",
             "A volume is consolidated when `python3 scripts/validate.py --strict` passes.", "",
             "## Open issues by rule", "", "| Rule | Open |", "|---|---|"]
    lines += [f"| {r} | {c} |" for r, c in sorted(by_rule.items())]
    lines += ["", "## Open issues by entry", ""]
    for where in sorted(by_entry):
        lines.append(f"- **{where}**")
        lines += [f"  - {m}" for m in by_entry[where]]
    (ROOT / "docs/CONSOLIDATION.md").write_text("\n".join(lines) + "\n")
    print("wrote docs/CONSOLIDATION.md")


if __name__ == "__main__":
    main()
