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

ISO = {"AQ": "Antarctica", "BD": "Bangladesh", "BO": "Bolivia", "BG": "Bulgaria", "CZ": "Czech Republic", "EC": "Ecuador",
       "ET": "Ethiopia", "GE": "Georgia", "GR": "Greece", "HU": "Hungary", "ID": "Indonesia", "IL": "Israel", "IQ": "Iraq",
       "IR": "Iran", "KE": "Kenya", "KG": "Kyrgyzstan", "KR": "South Korea", "LA": "Laos", "LK": "Sri Lanka", "LS": "Lesotho",
       "LU": "Luxembourg", "LY": "Libya", "MG": "Madagascar", "ML": "Mali", "MM": "Myanmar", "MW": "Malawi", "MZ": "Mozambique",
       "NA": "Namibia", "NE": "Niger", "NG": "Nigeria", "NL": "Netherlands", "OM": "Oman", "PA": "Panama", "PE": "Peru",
       "PK": "Pakistan", "PL": "Poland", "PY": "Paraguay", "SA": "Saudi Arabia", "SD": "Sudan", "SE": "Sweden", "SN": "Senegal",
       "SY": "Syria", "TH": "Thailand", "TJ": "Tajikistan", "TN": "Tunisia", "TR": "Turkey", "TW": "Taiwan", "UA": "Ukraine",
       "UY": "Uruguay", "UZ": "Uzbekistan", "VE": "Venezuela", "VN": "Vietnam", "ZA": "South Africa", "ZM": "Zambia",
       "ZW": "Zimbabwe", "DZ": "Algeria", "CM": "Cameroon", "CD": "DR Congo", "AO": "Angola", "BW": "Botswana", "GA": "Gabon",
       "TD": "Chad", "HR": "Croatia", "SI": "Slovenia", "SK": "Slovakia", "RS": "Serbia", "IE": "Ireland", "NO": "Norway",
       "FI": "Finland", "PR": "Puerto Rico", "JM": "Jamaica", "DO": "Dominican Republic", "HT": "Haiti", "PH": "Philippines",
       "MY": "Malaysia", "PG": "Papua New Guinea", "NC": "New Caledonia", "FJ": "Fiji", "VU": "Vanuatu", "SB": "Solomon Islands",
       "GT": "Guatemala", "HN": "Honduras", "NI": "Nicaragua", "CR": "Costa Rica", "SV": "El Salvador", "BZ": "Belize",
       "GY": "Guyana", "SR": "Suriname", "GF": "French Guiana", "TT": "Trinidad and Tobago", "KH": "Cambodia", "NP": "Nepal",
       "AF": "Afghanistan", "KW": "Kuwait", "AE": "United Arab Emirates", "YE": "Yemen", "SO": "Somalia", "UG": "Uganda",
       "RW": "Rwanda", "BI": "Burundi", "MR": "Mauritania", "EH": "Western Sahara", "BF": "Burkina Faso", "GH": "Ghana",
       "CI": "Ivory Coast", "BJ": "Benin", "TG": "Togo", "SZ": "Eswatini", "MU": "Mauritius", "SC": "Seychelles", "CG": "Congo",
       "CF": "Central African Republic", "ER": "Eritrea", "DJ": "Djibouti", "MK": "North Macedonia", "AL": "Albania",
       "BA": "Bosnia and Herzegovina", "ME": "Montenegro", "LT": "Lithuania", "LV": "Latvia", "EE": "Estonia", "BY": "Belarus",
       "MD": "Moldova", "AM": "Armenia", "AZ": "Azerbaijan", "TM": "Turkmenistan", "IS": "Iceland", "SJ": "Svalbard",
       "AW": "Aruba", "CW": "Curaçao", "BS": "Bahamas", "CY": "Cyprus", "MT": "Malta"}
COUNTRY = {**ISO, **COUNTRY}
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
                pbdb_date=j("pbdb_genera.json")["downloaded"])


def files_of(R, g):
    """Commons candidates of a genus, numbered in the order of its contact sheet."""
    return [(t, f) for t, f in sorted(R["commons"].items()) if g in f["genera"] and f.get("thumb")]


def interval(a, b):
    return a if not b or b == a else f"{a}–{b}"


def formations(R, g):
    by = collections.OrderedDict()
    for p in R["occ"].get(g, []):
        key = (p[3] or "Unnamed unit", p[6])
        by.setdefault(key, []).append(p)
    out = []
    for (form, cc), rows in sorted(by.items(), key=lambda kv: -len(kv[1])):
        mx = max(float(r[10]) for r in rows if r[10])
        mn = min(float(r[11]) for r in rows if r[11])
        older = max(rows, key=lambda r: float(r[10] or 0))
        younger = min(rows, key=lambda r: float(r[11] or 999))
        out.append(dict(formation=form, group=next((r[5] for r in rows if r[5]), ""),
                        members=sorted({r[4] for r in rows if r[4]}), country=COUNTRY.get(cc, cc),
                        regions=sorted({r[7] for r in rows if r[7]}),
                        interval=interval(older[8], younger[9] or younger[8]), occurrences=len(rows), ma=[mn, mx]))
    return out


def authority(attr):
    return (attr or "").strip()


def species(R, g):
    out = []
    for s in sorted(R["sp"].get(g, []), key=lambda s: s["taxon_name"]):
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


def write(R, vol, batch, force=False):
    B = yaml.safe_load(pathlib.Path(batch).read_text())
    out = ROOT / "entries" / vol / "genera"
    for g, h in B.items():
        p = out / f"{g}.yaml"
        if p.exists() and not force:
            print(f"skip {g}: entry exists (use --force)")
            continue
        r, w = R["gen"][g], R["wiki"].get(g, {})
        cites = w.get("cites", [])
        sources = []
        if h.get("original"):
            sources.append(dict(kind="original", text=cite_text(cites[h["original"] - 1])))
        elif r.get("primary_reference") and not h.get("pbdb_ref_is_literature"):
            sources.append(dict(kind="original", text=re.sub(r"<[^>]+>", "", r["primary_reference"])))
        for k in h.get("literature", []):
            sources.append(dict(kind="literature", text=cite_text(cites[k - 1])))
        sources.append(dict(kind="database", text=f"Paleobiology Database — taxon and occurrence records for {g} (downloaded {R['pbdb_date']}).",
                            url=f"https://paleobiodb.org/classic/basicTaxonInfo?taxon_name={g}"))
        if w and not w.get("missing") and h.get("use_wiki", True):
            sources.append(dict(kind="encyclopedia", text=f"Wikipedia contributors. “{w['title']}”. English Wikipedia, revision {w['revid']}.",
                                url=f"https://en.wikipedia.org/w/index.php?title={w['title'].replace(' ', '_')}&oldid={w['revid']}"))
        sp = species(R, g)
        ts = h.get("type_species") or ""
        for s in sp:
            if s["name"] == ts or (not ts and len(sp) == 1):
                s["reference"] = "original description"
        fa, la = r.get("firstapp_max_ma"), r.get("lastapp_min_ma")
        files = files_of(R, g)
        images = []
        for n, kind, cap in h.get("images", []):
            t, f = files[n - 1]
            images.append(dict(kind=kind, file=t[5:], url=f["url"] if f.get("width", 0) <= 1600 else f["thumb"].replace("330px-", "960px-"),
                               page=f["page"], artist=h.get("artists", {}).get(n) or f.get("Artist") or "Unknown (no author on the Commons page)",
                               license=f.get("LicenseShortName", ""), license_url=license_url(f),
                               date=(f.get("DateTimeOriginal") or "")[:10], caption=cap, width=f.get("width"), height=f.get("height"),
                               review="unreviewed"))
        e = dict(name=g, rank="genus", parent=h["parent"], incertae_sedis=bool(h.get("incertae_sedis")),
                 placement_note=h.get("placement_note", ""), authority=authority(r.get("taxon_attr")).strip("()"),
                 type_species=ts, type_species_note=h.get("type_species_note", ""), summary=h["summary"])
        if r.get("is_extant") in ("extant", True, 1, "1"):
            e["extant"] = True
        size = {"length_m": h.get("length_m")}
        if h.get("mass_kg"):
            size["mass_kg"] = h["mass_kg"]
        size["note"] = h.get("size_note", "")
        e.update(size=size,
                 age=dict(first_ma=fa if fa is not None else h.get("first_ma"), last_ma=la if la is not None else h.get("last_ma"),
                          early_interval=r.get("early_interval") or h.get("early_interval", ""),
                          late_interval=r.get("late_interval", "") if r.get("late_interval") != r.get("early_interval") else "",
                          pbdb_occurrences=int(r.get("n_occs") or 0), note=h.get("age_note", "")),
                 species=sp, formations=h.get("formations") or formations(R, g),
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


if __name__ == "__main__":
    vol, cmd, *rest = sys.argv[1:]
    R = raw(vol)
    if cmd == "dossier":
        for g in rest:
            dossier(R, g)
    elif cmd == "write":
        write(R, vol, rest[0], force="--force" in rest)
