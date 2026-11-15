import json, re, importlib.util, collections, datetime

def load(p):
    spec = importlib.util.spec_from_file_location("m", p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

F = {}
for i in range(6):
    F.update(load(f"fichas/b{i}.py").F)
C = load("fichas/clades.py").C
cid = {c["id"] for c in C}

pb = json.load(open("data/pbdb_taxa.json"))
occs = json.load(open("data/pbdb_occs.json"))
wiki = json.load(open("data/wiki.json"))
wcl = json.load(open("data/wiki_clades.json"))
ii = json.load(open("data/imageinfo.json"))
sel = json.load(open("data/img_selection.json"))
pp = json.load(open("data/phylopic.json"))
R = pb["R"]

# ---- manual data for genera absent from PBDB (sourced from Wikipedia articles / original descriptions) ----
MAN = {
 "Altmuehlopterus": dict(att="Vidovic & Martill 2017", fea=152.1, lla=145.0, tei="Tithonian", tli="", sp=[("Altmuehlopterus rhamphastinus","(Wagner 1851)")]),
 "Cascocauda": dict(att="Yang et al. 2022", fea=166.1, lla=157.3, tei="Callovian", tli="Oxfordian", sp=[("Cascocauda rong","Yang et al. 2022")]),
 "Huaxiadraco": dict(att="Pêgas et al. 2023", fea=121.4, lla=113.2, tei="Aptian", tli="", sp=[("Huaxiadraco corollatus","(Lü et al. 2006)")]),
 "Laueropterus": dict(att="Hone 2026", fea=152.1, lla=145.0, tei="Tithonian", tli="", sp=[("Laueropterus vitriolus","Hone 2026")]),
 "Lingyuanopterus": dict(att="Xu, Jiang & Wang 2022", fea=121.4, lla=113.2, tei="Aptian", tli="", sp=[("Lingyuanopterus camposi","Xu, Jiang & Wang 2022")]),
 "Makrodactylus": dict(att="Hone et al. 2025", fea=152.1, lla=145.0, tei="Tithonian", tli="", sp=[("Makrodactylus oligodontus","Hone et al. 2025")]),
 "Meilifeilong": dict(att="Wang et al. 2023", fea=121.4, lla=113.2, tei="Aptian", tli="", sp=[("Meilifeilong youhao","Wang et al. 2023"),("Meilifeilong sanyainus","(Ji et al. 2023)")]),
 "Propterodactylus": dict(att="Spindler 2024", fea=152.1, lla=149.0, tei="Tithonian", tli="", sp=[("Propterodactylus frankerlae","Spindler 2024")]),
 "Skiphosoura": dict(att="Hone et al. 2024", fea=152.1, lla=145.0, tei="Tithonian", tli="", sp=[("Skiphosoura bavarica","Hone et al. 2024")]),
 "Torukjara": dict(att="Pêgas 2024", fea=121.4, lla=72.2, tei="Aptian", tli="Campanian", sp=[("Torukjara bandeirae","Pêgas 2024")]),
 "Diopecephalus": dict(att="Seeley 1871", fea=150.8, lla=148.5, tei="Early Tithonian", tli="", sp=[("Diopecephalus kochi","(Wagner 1837)")]),
 "Linlongopterus": dict(att="Rodrigues et al. 2015", fea=121.4, lla=113.2, tei="Aptian", tli="", sp=[("Linlongopterus jennyae","Rodrigues et al. 2015")]),
}
MAN_FORM = {
 "Altmuehlopterus": [("Mörnsheim","DE","Bavaria","Tithonian")],
 "Cascocauda": [("Tiaojishan","CN","Hebei","Callovian–Oxfordian")],
 "Huaxiadraco": [("Jiufotang","CN","Liaoning","Aptian")],
 "Laueropterus": [("Mörnsheim","DE","Bavaria","Tithonian")],
 "Lingyuanopterus": [("Jiufotang","CN","Liaoning","Aptian")],
 "Makrodactylus": [("Mörnsheim","DE","Bavaria","Tithonian")],
 "Meilifeilong": [("Jiufotang","CN","Liaoning","Aptian")],
 "Propterodactylus": [("Painten","DE","Bavaria","Kimmeridgian–Tithonian")],
 "Skiphosoura": [("Mörnsheim","DE","Bavaria","Tithonian")],
 "Torukjara": [("Caiuá Group (Rio Paraná / Goio-Erê)","BR","Paraná","Early Cretaceous")],
 "Diopecephalus": [("Solnhofen (Altmühltal)","DE","Bavaria","Early Tithonian")],
 "Linlongopterus": [("Jiufotang","CN","Liaoning","Aptian")],
}
WIKI_EXTRA = {
 "Diopecephalus": dict(title="Diopecephalus", revid=1313891814, fig=("Pterodactylus_kochi_2.jpg","Fossil in Augsburg Naturmuseum"),
    ii=dict(thumb="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Pterodactylus_kochi_2.jpg/960px-Pterodactylus_kochi_2.jpg", page="https://commons.wikimedia.org/wiki/File:Pterodactylus_kochi_2.jpg", artist="Tiia Monto", lic="CC BY-SA 3.0", licurl="https://creativecommons.org/licenses/by-sa/3.0", date="2017-08-10", w=1545, h=948, desc="Pterodactylus kochi fossil in Augsburg Naturmuseum."),
    refs=["Vidovic, S. U.; Martill, D. M. (2017). The taxonomy and phylogeny of Diopecephalus kochi (Wagner, 1837) and Germanodactylus rhamphastinus (Wagner, 1851). Geological Society, London, Special Publications 455: 125–147. doi:10.1144/SP455.12",
          "Smyth, R. S. H.; Unwin, D. M. (2024). Re-evaluation of Pterodactylus antiquus and Diopecephalus kochi: two troublesome taxonomic concepts. Journal of Systematic Palaeontology 22(1): 2421845. doi:10.1080/14772019.2024.2421845",
          "Bennett, S. C. (2013). New information on body size and cranial display structures of Pterodactylus antiquus, with a revision of the genus. Paläontologische Zeitschrift 87(2): 269–289. doi:10.1007/s12542-012-0159-8"]),
 "Linlongopterus": dict(title="Linlongopterus", revid=1376208300, fig=None, ii=None,
    refs=["Rodrigues, T.; Jiang, S.; Cheng, X.; Wang, X.; Kellner, A. W. A. (2015). A new toothed pteranodontoid (Pterosauria, Pterodactyloidea) from the Jiufotang Formation (Lower Cretaceous, Aptian) of China and comments on Liaoningopterus gui Wang and Zhou, 2003. Historical Biology 27(6): 782–795. doi:10.1080/08912963.2015.1033417",
          "Xu, Y.; Jiang, S.; Wang, X. (2024). The restudy of Haopterus gracilis from the Yixian Formation, Liaoning, China. Cretaceous Research 162: 105933. doi:10.1016/j.cretres.2024.105933"]),
}
CC = {"AR":"Argentina","AT":"Austria","AU":"Australia","BR":"Brazil","CA":"Canada","CH":"Switzerland","CN":"China","CO":"Colombia","CU":"Cuba","DE":"Germany","EG":"Egypt","ES":"Spain","FR":"France","GL":"Greenland","IT":"Italy","JO":"Jordan","KZ":"Kazakhstan","LB":"Lebanon","LU":"Luxembourg","MA":"Morocco","MN":"Mongolia","MX":"Mexico","PT":"Portugal","RO":"Romania","TZ":"Tanzania","UK":"United Kingdom","US":"United States"}

G = {g.split("|")[0]: g.split("|") for g in pb["G"]}
SP = collections.defaultdict(list)
for s in pb["S"]:
    p = s.split("|"); SP[p[0].split(" ")[0]].append(p)

# formations from PBDB occurrences
FORM = collections.defaultdict(dict)
for o in occs:
    p = o.split("|")
    g, tna, idn, sfm, smb, sgr, cc, stp, oei, oli, eag, lag = p[:12]
    if not g: continue
    key = (sfm or "Unnamed unit", cc)
    d = FORM[g].setdefault(key, dict(formation=sfm or "Unnamed unit", group=sgr, members=set(), country=CC.get(cc, cc), regions=set(), ints=set(), n=0, ma=[999, 0]))
    if smb: d["members"].add(smb)
    if stp: d["regions"].add(stp)
    d["ints"].add(oei + ("–" + oli if oli else ""))
    d["n"] += 1
    try:
        d["ma"][0] = min(d["ma"][0], float(lag)); d["ma"][1] = max(d["ma"][1], float(eag))
    except: pass

def fmt_forms(g):
    out = []
    for d in sorted(FORM.get(g, {}).values(), key=lambda x: -x["n"]):
        out.append(dict(formation=d["formation"], group=d["group"], members=sorted(d["members"])[:4], country=d["country"],
                        regions=sorted(d["regions"])[:3], interval=" / ".join(sorted(d["ints"]))[:80], n=d["n"], ma=d["ma"] if d["ma"][0] < 999 else None))
    return out

def wiki_refs(g, refs, limit=6):
    """References from the Wikipedia article that name the genus (descriptions, redescriptions)."""
    keep = []
    for r in refs or []:
        if r.startswith(".mw-parser") or len(r) < 30: continue
        if g.lower() in r.lower() and r not in keep:
            keep.append(re.sub(r"\s*(ISSN|S2CID|PMID|PMC|Bibcode)[^.]*\.", "", r).strip())
    return keep[:limit]

def img_record(fn, kind, caption):
    if not fn or fn not in ii: return None
    x = ii[fn]
    thumb = (x.get("thumb") or x.get("url") or "").split("?")[0]
    return dict(kind=kind, file=fn, src=thumb, page=x.get("page"), artist=x.get("artist"), license=x.get("lic"), licurl=x.get("licurl"),
                date=x.get("date"), caption=caption, w=x.get("w"), h=x.get("h"))

genera = []
for g, f in sorted(F.items()):
    assert f["clade"] in cid, (g, f["clade"])
    rec = dict(name=g, clade=f["clade"], isd=f["isd"], isnote=f["isnote"], sum=f["sum"], ws=f["ws"], wsnote=f["wsnote"],
               holotype=f["ho"], material=f["el"], completeness=f["comp"], exceptional=f["exc"], biology=f["bio"])
    src = []
    if g in G:
        p = G[g]
        AGEFIX = {"Luopterus": (166.1, 157.3, "Callovian", "Oxfordian", "Luopterus mutoudengensis"), "Carniadactylus": (227.3, 208.5, "Norian", "", "Carniadactylus rosenfeldi")}
        if p[2] == "":
            a = AGEFIX[g]; rec.update(author=p[1], fad=a[0], lad=a[1], early=a[2], late=a[3], type_species=a[4], pbdb_occ=0,
                                      dates_note="PBDB lists no occurrences under this genus name (they are filed under its former name); age bracket from the literature stage.")
        else:
            rec.update(author=p[1], fad=float(p[2]), lad=float(p[3]), early=p[4], late=p[5], type_species=p[8], pbdb_occ=int(p[10]))
        rid = p[9]
        if rid in R: src.append(dict(kind="original", text=R[rid]))
        rec["species"] = [dict(name=s[0], author=s[1], fad=float(s[2]) if s[2] else None, lad=float(s[3]) if s[3] else None,
                               interval=s[4] + ("–" + s[5] if s[5] else ""), ref=R.get(s[6], "")) for s in sorted(SP.get(g, []))]
        rec["formations"] = fmt_forms(g) or ([dict(formation="Tiaojishan", group="", members=[], country="China", regions=["Hebei"], interval="Callovian–Oxfordian", n=None, ma=None)] if g=="Luopterus" else [dict(formation="Dolomia di Forni / Calcari di Zorzino", group="", members=[], country="Italy", regions=["Friuli","Lombardy"], interval="Norian", n=None, ma=None)] if g=="Carniadactylus" else [])
        src.append(dict(kind="database", text=f"Paleobiology Database — taxon and occurrence records for {g} (downloaded {datetime.date(2026,11,15).isoformat()}).", url=f"https://paleobiodb.org/classic/basicTaxonInfo?taxon_name={g}"))
    else:
        m = MAN[g]
        rec.update(author=m["att"], fad=m["fea"], lad=m["lla"], early=m["tei"], late=m["tli"], type_species=m["sp"][0][0], pbdb_occ=0)
        rec["species"] = [dict(name=a, author=b, fad=None, lad=None, interval="", ref="") for a, b in m["sp"]]
        rec["formations"] = [dict(formation=a, group="", members=[], country=CC.get(b, b), regions=[c], interval=d, n=None, ma=None) for a, b, c, d in MAN_FORM[g]]
        rec["dates_note"] = "Age bracket from the stage named in the literature (ICS International Chronostratigraphic Chart); not in PBDB at time of download."
    # Wikipedia
    if g in wiki and wiki[g].get("text"):
        w = wiki[g]
        src.append(dict(kind="encyclopedia", text=f"Wikipedia contributors. “{w['title']}”. English Wikipedia, revision {w['revid']}.", url=f"https://en.wikipedia.org/w/index.php?title={w['title'].replace(' ','_')}&oldid={w['revid']}"))
        for r in wiki_refs(g, w.get("refs")): src.append(dict(kind="literature", text=r))
        life = sel["life"].get(g); fos = sel["fossil"].get(g)
        caps = {fn: cap for fn, cap in w.get("figs", [])}
        imgs = []
        if life: imgs.append(img_record(life, "life", caps.get(life, "Life restoration").replace("[infobox] ", "")))
        if fos: imgs.append(img_record(fos[0], "fossil", fos[1].replace("[infobox] ", "")))
        rec["images"] = [x for x in imgs if x]
    elif g in WIKI_EXTRA:
        w = WIKI_EXTRA[g]
        src.append(dict(kind="encyclopedia", text=f"Wikipedia contributors. “{w['title']}”. English Wikipedia, revision {w['revid']}.", url=f"https://en.wikipedia.org/w/index.php?title={w['title']}&oldid={w['revid']}"))
        for r in w["refs"]: src.append(dict(kind="literature", text=r))
        rec["images"] = []
        if w["fig"]:
            x = w["ii"]; rec["images"].append(dict(kind="fossil", file=w["fig"][0], src=x["thumb"], page=x["page"], artist=x["artist"], license=x["lic"], licurl=x["licurl"], date=x["date"], caption=w["fig"][1], w=x["w"], h=x["h"]))
    # PhyloPic
    s = pp.get(g)
    if s:
        rec["silhouette"] = dict(src=s.get("vector") or s.get("png"), page=s["page"], attribution=s.get("attribution") or s.get("contrib") or "Unknown",
                                 license=s["lic"], depicts=s.get("specific"), matched=s["matched"], genus_level=(s["matched"] == g or (s.get("specific") or "").split(" ")[0] == g), w=s["w"], h=s["h"],
                                 flight_pose=(s["w"] / s["h"] >= 1.7))
    rec["sources"] = src
    genera.append(rec)

# clades
clades = []
for c in C:
    c = dict(c)
    w = wcl.get(c["wiki"]) or {}
    c["sources"] = []
    if w.get("revid"):
        c["sources"].append(dict(kind="encyclopedia", text=f"Wikipedia contributors. “{w['title']}”. English Wikipedia, revision {w['revid']}.", url=f"https://en.wikipedia.org/w/index.php?title={w['title'].replace(' ','_')}&oldid={w['revid']}"))
    for r in c.pop("refs"): c["sources"].append(dict(kind="literature", text=r))
    clades.append(c)

# excluded names (nomina dubia / nuda) from PBDB
excluded = []
for x in pb["X"]:
    nam, att, tdf, rid = x.split("|")
    status = "nomen nudum" if "nudum" in tdf else ("nomen inquirendum" if "inquirenda" in tdf else "nomen dubium")
    excluded.append(dict(name=nam, author=att, status=status, ref=R.get(rid, ""), source="Paleobiology Database"))
excluded.append(dict(name="Pterodactyle", author="", status="duplicate", ref="", source="French vernacular form of Pterodactylus in the original list; merged into Pterodactylus."))
excluded.append(dict(name="Linglongopterus", author="", status="misspelling", ref="", source="Spelling in the original list; the valid genus is Linlongopterus Rodrigues et al. 2015."))
excluded.append(dict(name="Diocephalus", author="", status="misspelling", ref="", source="Spelling in the original list; the genus is Diopecephalus Seeley 1871."))

for g in genera:
    if g["name"]=="Makrodactylus": g["images"]=[]

data = dict(meta=dict(title="Atlas of Life", group="Pterosauria", built="2026-11-15",
                      method="Ages, authorities, species and formations from the Paleobiology Database; descriptive data paraphrased from the cited literature and English Wikipedia; images from Wikimedia Commons and PhyloPic with their licences."),
            clades=clades, genera=genera, excluded=excluded)
json.dump(data, open("data/atlas_pterosauria.json", "w"), ensure_ascii=False)
print(len(genera), "genera;", len(clades), "clades;", len(excluded), "excluded")
print("with life image:", sum(1 for g in genera if any(i["kind"]=="life" for i in g.get("images",[]))),
      "| fossil only:", sum(1 for g in genera if g.get("images") and not any(i["kind"]=="life" for i in g["images"])),
      "| no image:", [g["name"] for g in genera if not g.get("images")])
print("species total:", sum(len(g["species"]) for g in genera), "| genera w/o formations:", [g["name"] for g in genera if not g["formations"]])
print("size known:", sum(1 for g in genera if g["ws"]))

