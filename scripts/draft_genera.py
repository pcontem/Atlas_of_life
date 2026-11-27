"""Help draft the genus entries of a new volume from its harvested raw data (data/raw/<volume>/, harvest.py).

    python3 scripts/draft_genera.py <volume> dossier Genus [Genus ...]   # print everything known about each genus
    python3 scripts/draft_genera.py <volume> write <batch.yaml>          # write entries from a batch file

The dossier is for reading: PBDB record, species, occurrences by formation, the fixed Wikipedia revision (text,
taxobox, citations), Commons candidates (numbered as on the contact sheet) and the PhyloPic silhouette.

A batch file holds the hand-written part of each entry — what has to be read and judged:
    Genus:
      parent: <clade id>          incertae_sedis / placement_note (optional)
      summary, length_m, mass_kg, size_note, holotype, material, completeness, exceptional, biology
      type_species (only if PBDB/taxobox lack it, with type_species_note)
      images: [[<n on the contact sheet>, kind, caption], ...]
      literature: [<n of the Wikipedia citation>, ...]   original: <n of the citation that named it> (if PBDB lacks it)
      notes: [curation to-dos]
The mechanical part comes from the raw data: authority, ages, species, formations, the PBDB and Wikipedia
sources, the silhouette and the extant flag. Existing entries are overwritten only with --force.
Afterwards: fmt.py, make_formations.py, paleo_points.py, build.py, validate.py (CLAUDE.md §5).
"""
import collections, json, pathlib, re, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from make_formations import COUNTRY  # noqa: E402

TODAY_RAW = None


def raw(vol):
    d = ROOT / "data/raw" / vol
    j = lambda n: json.loads((d / n).read_text())
    gen = {r["taxon_name"]: r for r in j("pbdb_genera.json")["records"]}
    occ = collections.defaultdict(list)
    for row in j("pbdb_occs.json"):
        p = row.split("|")
        occ[p[0]].append(p)
    return dict(gen=gen, sp=j("pbdb_species.json")["species"], occ=occ, cols=j("pbdb_colls.json")["cols"],
                wiki=j("wiki.json")["pages"], wiki_date=j("wiki.json")["downloaded"],
                commons=j("commons.json")["files"], sil=j("phylopic.json")["silhouettes"],
                pbdb_date=j("pbdb_genera.json")["downloaded"],
                papers=j("papers.json")["papers"] if (d / "papers.json").exists() else {})


def files_of(R, g):
    """Commons candidates of a genus, numbered in the order of its contact sheet."""
    return [(t, f) for t, f in sorted(R["commons"].items()) if g in f["genera"] and f.get("thumb")]


def interval(a, b):
    return a if not b or b == a else f"{a}–{b}"


def occs_of(R, g, keep=None, genus_level=True):
    """Occurrences of a genus; with `keep` (species epithets) only those species, plus — if genus_level — the
    occurrences identified to the genus alone."""
    rows = R["occ"].get(g, [])
    if keep is None:
        return rows
    ok = lambda p: (p[1].split()[-1] in keep if len(p[1].split()) > 1 else genus_level)
    return [p for p in rows if ok(p)]


def formations(R, g, keep=None, genus_level=True):
    by = collections.OrderedDict()
    for p in occs_of(R, g, keep, genus_level):
        key = (p[3] or "Unnamed unit", p[6])
        by.setdefault(key, []).append(p)
    out = []
    for (form, cc), rows in sorted(by.items(), key=lambda kv: -len(kv[1])):
        num = lambda v: float(v) if v not in ("", None) else None
        mxs = [num(r[10]) for r in rows if num(r[10]) is not None]
        mns = [num(r[11]) for r in rows if num(r[11]) is not None]
        mx, mn = (max(mxs) if mxs else None), (min(mns) if mns else None)
        older = max(rows, key=lambda r: float(r[10] or 0))
        younger = min(rows, key=lambda r: float(r[11] or 999))
        out.append(dict(formation=form, group=next((r[5] for r in rows if r[5]), ""),
                        members=sorted({r[4] for r in rows if r[4]}), country=COUNTRY.get(cc, cc),
                        regions=sorted({r[7] for r in rows if r[7]}),
                        interval=interval(older[8], younger[9] or younger[8]), occurrences=len(rows), ma=[mn, mx]))
    return out


def authority(attr):
    return (attr or "").strip()


def species(R, g, keep=None):
    out = []
    for s in sorted(R["sp"].get(g, []), key=lambda s: s["taxon_name"]):
        if keep is not None and s["taxon_name"].split()[-1] not in keep:
            continue
        fa, la = s.get("firstapp_max_ma"), s.get("lastapp_min_ma")
        out.append(dict(name=s["taxon_name"], authority=authority(s.get("taxon_attr")), first_ma=fa, last_ma=la,
                        interval=interval(s.get("early_interval", ""), s.get("late_interval", "")) if fa else "",
                        reference=""))
    return out


def dossier(R, g):
    r, w, s = R["gen"].get(g, {}), R["wiki"].get(g, {}), R["sil"].get(g)
    print(f"===== {g} =====")
    print("PBDB:", json.dumps(r, ensure_ascii=False))
    for sp in species(R, g):
        print("  sp:", sp["name"], sp["authority"], sp["first_ma"], sp["last_ma"])
    for f in formations(R, g):
        print("  fm:", f["formation"], "|", f["group"], f["members"], f["country"], f["regions"], f["interval"], f["occurrences"], f["ma"])
    if w.get("missing"):
        print("WIKI: no article")
    else:
        flag = "" if w.get("about_genus") else "  (!) article may not be about this genus"
        print(f"WIKI: {w.get('title')} rev {w.get('revid')}{flag}")
        print("  taxobox:", json.dumps(w.get("taxobox"), ensure_ascii=False))
        print(re.sub(r"\n{2,}", "\n", w.get("text", ""))[:7000])
        for k, c in enumerate(w.get("cites", []), 1):
            who = c.get("last1") or c.get("last") or c.get("author1") or c.get("authors") or c.get("vauthors") or ""
            print(f"  [{k}] {who} {c.get('year') or c.get('date', '')} — {c.get('title')} — {c.get('journal', '')} {c.get('doi', '')}")
    for k, (t, f) in enumerate(files_of(R, g), 1):
        print(f"  img {k}: {t[5:]} | {f.get('LicenseShortName')} | {f.get('Artist', '')[:60]} | {f.get('ImageDescription', '')[:140]} | {f.get('found')}")
    if s:
        print("  silhouette:", s["matched"], s.get("depicts"), s["attribution"], s["license"], "genus level" if s["genus_level"] else "relative")


BAD_IMG = re.compile(r"(map\\b|range map|scale diagram|\\bsize|comparison|compar|phylogen|clad|diagram|chart|stamp|statue|model|sculpt|museum model|life-size|\.svg$|tamano|tamaño)", re.I)


def img_kind(t, f):
    d = (t + " " + f.get("ImageDescription", "")).lower()
    if re.search(r"skeletal (reconstruction|diagram)|skeletal\b", d):
        return "skeletal"
    if re.search(r"restoration|reconstruction|life |recreaci|reconstitu|paleoart|illustration|drawing|pencil", d) and not re.search(r"skull reconstruction", d):
        return "life"
    if re.search(r"skull|fossil|holotype|specimen|jaw|mandible|teeth|tooth|scute|osteoderm|vertebra|bone|mount|cast|skeleton|cranium|plate", d):
        return "fossil"
    return None


def auto_images(R, g, maxn=8):
    """Suggested gallery: candidates named after the genus, not charts/maps/models, kind guessed from the text."""
    out = []
    for k, (t, f) in enumerate(files_of(R, g), 1):
        lic = f.get("LicenseShortName", "")
        if not re.match(r"(CC0|Public domain|CC BY(-SA)? \d|CC BY-SA \d|CC BY \d|PD)", lic, re.I) or "NC" in lic or "ND" in lic:
            continue
        if BAD_IMG.search(t) or BAD_IMG.search(f.get("ImageDescription", "")[:80]) or g.lower() not in (t + f.get("ImageDescription", "")).lower():
            continue
        kd = img_kind(t, f)
        if kd:
            out.append((k, kd))
    return out[:maxn]


def auto_original(R, g):
    """Index of the Wikipedia citation that looks like the naming paper (same first author and year as the authority)."""
    r, w = R["gen"].get(g, {}), R["wiki"].get(g, {})
    m = re.match(r"\(?([^\d]+?)\s(?:et al\.?\s|and .*?\s)?(\d{4})", r.get("taxon_attr") or "")
    if not m:
        return None
    who, yr = m.group(1).split()[0].lower(), m.group(2)
    for k, c in enumerate(w.get("cites", []), 1):
        a = (c.get("last1") or c.get("last") or c.get("author1") or c.get("authors") or c.get("vauthors") or "").lower()
        if yr in (c.get("year") or c.get("date") or "") and who[:5] in a:
            return k
    return None


def brief(R, g):
    """A short dossier: the facts an entry needs, for batch drafting."""
    r, w, s = R["gen"].get(g, {}), R["wiki"].get(g, {}), R["sil"].get(g)
    print(f"##### {g} | {r.get('taxon_attr')} | PBDB parent {r.get('parent_name')} / {r.get('family')} | "
          f"{r.get('early_interval')}–{r.get('late_interval', '')} {r.get('firstapp_max_ma')}–{r.get('lastapp_min_ma')} Ma | occ {r.get('n_occs')}")
    print("  ref:", (r.get("primary_reference") or "")[:220])
    print("  sp:", "; ".join(f"{x['name'].split()[-1]} {x['authority']}" for x in species(R, g)))
    print("  fm:", "; ".join(f"{f['formation']} ({f['country']}, {f['interval']}, {f['occurrences']})" for f in formations(R, g)[:4]))
    if w.get("missing"):
        print("  WIKI: none")
    else:
        t = w.get("text", "")
        tb = w.get("taxobox", {})
        print(f"  WIKI {w['title']} rev {w['revid']}{'' if w.get('about_genus') else ' (!not about genus)'} | type: {tb.get('type_species', '')[:80]}")
        sents = re.split(r"(?<=[.!?])\s+", re.sub(r"\n+", " ", t))
        lead = " ".join(sents[:6])
        print("  LEAD:", lead[:700])
        keys = re.compile(r"(\d(\.\d+)? ?(m|metres|meters|cm|kg|ft)\b|length|long\b|weigh|holotype|specimen|[A-Z]{2,}[ -]?[A-Z]*\s?\d{2,}|diet|ate|fed|prey|teeth)", re.I)
        extra = [x for x in sents[6:] if keys.search(x)][:10]
        print("  MORE:", " ".join(extra)[:1600])
        cs = [(k, c) for k, c in enumerate(w.get("cites", []), 1) if c.get("doi") or c.get("journal")]
        print(f"  ORIG? {auto_original(R, g)} | CITES:", " | ".join(f"[{k}] {(c.get('last1') or c.get('last') or c.get('author1') or c.get('authors') or '')[:14]} {(c.get('year') or c.get('date') or '')[:4]} {c.get('title', '')[:45]}"
                                     for k, c in cs[:9]))
    pp = R["papers"].get(g, [])
    if pp:
        print("  PAPERS:", " | ".join(f"[p{k}] {x.get('year')} {(x.get('authors') or '')[:16]} {x['title'][:60]}" for k, x in enumerate(pp[:5], 1)))
        if w.get("missing") or not w.get("about_genus"):
            print("  ABS p1:", (pp[0].get("abstract") or "")[:700])
    fl = files_of(R, g)
    print("  IMG auto:", " | ".join(f"{k}:{kd}:{fl[k - 1][0][5:40]}" for k, kd in auto_images(R, g)))
    if s:
        print(f"  SIL: {s['matched']}{'' if s['genus_level'] else ' (relative)'} {s['license'].split('/')[-3:-1]}")


def cite_text(c):
    names = []
    for k in range(1, 30):
        last, first = c.get(f"last{k}") or (c.get("last") if k == 1 else None), c.get(f"first{k}") or (c.get("first") if k == 1 else None)
        if not last:
            break
        names.append(f"{last}, {first}" if first else last)
    who = "; ".join(names) or c.get("authors") or c.get("vauthors") or c.get("author1") or c.get("author") or ""
    year = c.get("year") or (c.get("date") or "")[:4]
    bits = [f"{who} {year}.".strip(), c.get("title", "").rstrip(".") + "."]
    if c.get("journal"):
        bits.append(c["journal"] + (f" {c['volume']}" if c.get("volume") else "") + (f"({c['issue']})" if c.get("issue") else "")
                    + (f": {c['pages']}" if c.get("pages") else "") + ".")
    elif c.get("publisher"):
        bits.append(c["publisher"] + ".")
    if c.get("doi"):
        bits.append(f"doi:{c['doi']}")
    return " ".join(b for b in bits if b and b != ".")


def license_url(f):
    u = f.get("LicenseUrl") or ""
    return u.replace("http://", "https://")


def image(files, n, kind, cap, artist=None):
    t, f = files[n - 1]
    return dict(kind=kind, file=t[5:], url=f["url"] if f.get("width", 0) <= 1600 else f["thumb"].replace("330px-", "960px-"),
                page=f["page"], artist=artist or f.get("Artist") or "Unknown (no author on the Commons page)",
                license=f.get("LicenseShortName", ""), license_url=license_url(f),
                date=(f.get("DateTimeOriginal") or "")[:10], caption=cap, width=f.get("width"), height=f.get("height"),
                review="unreviewed")


def addimg(R, vol, specs):
    """Add Commons candidates to existing entries: specs = ["Genus:n:kind:caption", ...]."""
    for spec in specs:
        g, n, kind, cap = spec.split(":", 3)
        p = ROOT / "entries" / vol / "genera" / f"{g}.yaml"
        e = yaml.safe_load(p.read_text())
        im = image(files_of(R, g), int(n), kind, cap)
        if any(x["page"] == im["page"] for x in e.get("images") or []):
            continue
        e.setdefault("images", []).append(im)
        p.write_text(yaml.safe_dump(e, allow_unicode=True, sort_keys=False, width=120))
        print("added", g, n)


def addoa(vol, specs):
    """Add open-access article figures (data/raw/<vol>/oa_figures.json) to entries: specs = ["Genus:n:kind:caption"],
    n = number on the oa_<Genus> contact sheet. Follows CLAUDE.md I2 for article figures and lists the article
    as a literature source."""
    oa = json.loads((ROOT / "data/raw" / vol / "oa_figures.json").read_text())["figures"]
    for spec in specs:
        g, n, kind, cap = spec.split(":", 3)
        f = oa[g][int(n) - 1]
        p = ROOT / "entries" / vol / "genera" / f"{g}.yaml"
        e = yaml.safe_load(p.read_text())
        page = f"https://doi.org/{f['doi']}" if f.get("doi") else f"https://europepmc.org/article/PMC/{f['pmcid']}"
        if any(x.get("file") == f"{f['pmcid']} {f['label']}" for x in e.get("images") or []):
            continue
        lic = {"cc by": "CC BY 4.0", "cc0": "CC0"}.get((f.get("license") or "").lower(), f.get("license", ""))
        m = re.match(r"^(.*?)\.?\s(\d{4})\.\s", f.get("cite") or "")
        authors, year = (m.group(1), m.group(2)) if m else (f.get("cite", ""), "")
        journal = (f.get("cite") or "").rstrip(". ").split(". ")[-1]
        first = authors.split(",")[0].split()[0] if authors else ""
        short = f"{first}{' et al.' if authors.count(',') > 1 else ''} {year}".strip()
        e.setdefault("images", []).append(dict(
            kind=kind, file=f"{f['pmcid']} {f['label']}".strip(), url=f["img"], page=page,
            artist=f"{authors} ({journal}, {year})",
            license=lic, license_url="https://creativecommons.org/licenses/by/4.0/" if lic.startswith("CC BY") else "https://creativecommons.org/publicdomain/zero/1.0/",
            date=year, caption=f"{f['label']}, {short}: {cap}".strip(), width=None, height=None, review="unreviewed"))
        e["curation"].setdefault("notes", [])
        note = "Licence version of open-access figures recorded as CC BY 4.0 from Europe PMC's 'cc by'; check on the article page."
        if lic.startswith("CC BY") and note not in e["curation"]["notes"]:
            e["curation"]["notes"].append(note)
        if not any(f["pmcid"] in (x.get("text", "") + x.get("url", "")) for x in e["sources"]):
            e["sources"].insert(1, dict(kind="literature", text=f"{f['cite']} {f['pmcid']}.", url=page))
        p.write_text(yaml.safe_dump(e, allow_unicode=True, sort_keys=False, width=120))
        print("added", g, n)


def write(R, vol, batch, force=False):
    B = yaml.safe_load(pathlib.Path(batch).read_text())
    out = ROOT / "entries" / vol / "genera"
    for g, h in B.items():
        p = out / f"{g}.yaml"
        if p.exists() and not force:
            print(f"skip {g}: entry exists (use --force)")
            continue
        r, w = R["gen"].get(g, {}), R["wiki"].get(g, {})  # r is {} for genera PBDB does not list as valid
        cites = w.get("cites", [])
        sources = []
        if h.get("original"):
            sources.append(dict(kind="original", text=cite_text(cites[h["original"] - 1])))
        elif r.get("primary_reference") and not h.get("pbdb_ref_is_literature"):
            sources.append(dict(kind="original", text=re.sub(r"<[^>]+>", "", r["primary_reference"])))
        for k in h.get("literature", []):
            sources.append(dict(kind="literature", text=cite_text(cites[k - 1])))
        pp = R["papers"].get(g, [])
        for k in ([h["original_paper"]] if h.get("original_paper") else []) + h.get("papers", []):
            x = pp[k - 1]
            src = dict(kind="original" if k == h.get("original_paper") else "literature",
                       text=f"{x.get('authors', '').rstrip('.')} {x.get('year')}. {x['title'].rstrip('.')}. {x.get('journal', '')}."
                            + (f" doi:{x['doi']}" if x.get("doi") else ""))
            if x.get("doi"):
                src["url"] = f"https://doi.org/{x['doi']}"
            sources.insert(0, src) if src["kind"] == "original" else sources.append(src)
        if r:
          sources.append(dict(kind="database", text=f"Paleobiology Database — taxon and occurrence records for {g} (downloaded {R['pbdb_date']}).",
                              url=f"https://paleobiodb.org/classic/basicTaxonInfo?taxon_name={g}"))
        if w and not w.get("missing") and h.get("use_wiki", True):
            sources.append(dict(kind="encyclopedia", text=f"Wikipedia contributors. “{w['title']}”. English Wikipedia, revision {w['revid']}.",
                                url=f"https://en.wikipedia.org/w/index.php?title={w['title'].replace(' ', '_')}&oldid={w['revid']}"))
        keep = h.get("species")
        sp = h["species_manual"] if h.get("species_manual") else species(R, g, keep)  # species_manual: dicts, for genera without PBDB data
        ts = h.get("type_species") or ""
        if not ts:  # from the taxobox of the fixed Wikipedia revision, else the only valid PBDB species
            tb = re.sub(r"\{\{[^}]*\}\}|'|\[|\]", "", (w.get("taxobox") or {}).get("type_species", "")).strip()
            if w.get("about_genus") and re.fullmatch(rf"{g} [a-z]+", tb) and any(x["name"] == tb for x in sp):
                ts = tb; h.setdefault("type_species_note", f"Taxobox of Wikipedia revision {w['revid']}.")
            elif len(sp) == 1:
                ts = sp[0]["name"]
                h.setdefault("type_species_note", "The only valid species listed by PBDB.")
        for s in sp:
            if s["name"] == ts or (not ts and len(sp) == 1):
                s["reference"] = "original description"
        fa, la = r.get("firstapp_max_ma"), r.get("lastapp_min_ma")
        early, late, nocc = r.get("early_interval"), r.get("late_interval", ""), int(r.get("n_occs") or 0)
        if keep is not None:  # ages and counts from the occurrences of the accepted species only
            rows = occs_of(R, g, keep, h.get("genus_level_occs", True))
            nocc = len(rows)
            if rows:
                old = max(rows, key=lambda p: float(p[10] or 0))
                fa, early = float(old[10]), old[8]
            if h.get("extant"):
                la, late = 0, "Holocene"
        if h.get("extant"):
            la = 0
        files = files_of(R, g)
        images = [image(files, n, kind, ", ".join(str(c) for c in cap), h.get("artists", {}).get(n))
                  for n, kind, *cap in h.get("images", [])]
        e = dict(name=g, rank="genus", parent=h["parent"], incertae_sedis=bool(h.get("incertae_sedis")),
                 placement_note=h.get("placement_note", ""), authority=h.get("authority") or authority(r.get("taxon_attr")).strip("()"),
                 type_species=ts, type_species_note=h.get("type_species_note", ""), summary=h["summary"])
        if h.get("extant"):  # set by hand: PBDB's flag is wrong for some fossil and ichno genera
            e["extant"] = True
        size = {"length_m": h.get("length_m")}
        if h.get("mass_kg"):
            size["mass_kg"] = h["mass_kg"]
        size["note"] = h.get("size_note", "")
        e.update(size=size,
                 age=dict(first_ma=fa if fa is not None else h.get("first_ma"), last_ma=la if la is not None else h.get("last_ma"),
                          early_interval=early or h.get("early_interval", ""),
                          late_interval=late if late != early else "",
                          pbdb_occurrences=nocc, note=h.get("age_note", "")),
                 species=sp, formations=h.get("formations") or [f for f in formations(R, g, keep, h.get("genus_level_occs", True))
                                                                if not h.get("named_formations_only") or f["formation"] != "Unnamed unit"],
                 fossil_material=dict(holotype=h["holotype"], material=h["material"], completeness=h["completeness"],
                                      exceptional=h.get("exceptional", "")),
                 biology=h["biology"], images=images)
        s = R["sil"].get(g)
        if s and not h.get("no_silhouette"):
            e["silhouette"] = dict(src=s["vector"] or s["png"], png=s["png"], page=s["page"], attribution=s["attribution"],
                                   license=s["license"], depicts=s.get("depicts") or s["matched"], matched=s["matched"],
                                   genus_level=s["genus_level"])
        e["sources"] = sources
        e["curation"] = dict(status="draft", origin="ai-draft", checked_by="", checked_on="", notes=h.get("notes", []), reviews=[])
        p.write_text(yaml.safe_dump(e, allow_unicode=True, sort_keys=False, width=120))
        print("wrote", p.relative_to(ROOT))


def synonyms(R, vol, extra=None):
    """Add to excluded.yaml the genus names PBDB treats as junior synonyms (or that the batch lists in `extra`:
    {name: [senior genus, source text]}) whose senior genus already has an entry in this volume."""
    exp = ROOT / "entries" / vol / "excluded.yaml"
    ex = yaml.safe_load(exp.read_text()) or []
    have = {x["name"] for x in ex}
    entries = {p.stem for p in (ROOT / "entries" / vol / "genera").glob("*.yaml")}
    added = []
    for g, r in sorted(R["gen"].items()):
        if g in have or g in entries or r.get("flags"):
            continue
        if r.get("difference") in ("subjective synonym of", "objective synonym of") and r.get("accepted_name") in entries:
            ex.append(dict(name=g, author=r.get("taxon_attr", ""), status="junior synonym",
                           ref=f"{r['difference'].capitalize()} {r['accepted_name']} (Paleobiology Database taxonomy, downloaded {R['pbdb_date']})",
                           source="Paleobiology Database", parent=r["accepted_name"],
                           placement="the senior synonym named by PBDB"))
            added.append(g)
    for g, (senior, src) in (extra or {}).items():
        if g not in have and g not in added and senior in entries:
            r = R["gen"].get(g, {})
            ex.append(dict(name=g, author=r.get("taxon_attr", ""), status="junior synonym", ref=src,
                           source="English Wikipedia", parent=senior, placement="the senior synonym named in the source"))
            added.append(g)
    exp.write_text(yaml.safe_dump(ex, allow_unicode=True, sort_keys=False, width=120))
    print("excluded:", ", ".join(added) or "none")


if __name__ == "__main__":
    vol, cmd, *rest = sys.argv[1:]
    R = raw(vol)
    if cmd == "brief":
        for g in rest:
            brief(R, g)
    elif cmd == "dossier":
        for g in rest:
            dossier(R, g)
    elif cmd == "addoa":
        addoa(vol, rest)
    elif cmd == "addimg":
        addimg(R, vol, rest)
    elif cmd == "synonyms":
        synonyms(R, vol, yaml.safe_load(pathlib.Path(rest[0]).read_text()) if rest else None)
    elif cmd == "write":
        write(R, vol, rest[0], force="--force" in rest)
