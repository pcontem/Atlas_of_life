"""Harvest the raw material for a new genus volume (runs in GitHub Actions: .github/workflows/harvest.yml).

    python3 scripts/fetch/harvest.py <volume> <PBDB base taxon> [--genera A,B,...] [--sheets DIR]

Writes data/raw/<volume>/ (provenance; never edited by hand):
  pbdb_genera.json    valid genera of the base taxon: authority, ages, parent/family/order, primary reference
  pbdb_species.json   valid species (authority, ages) grouped by genus
  pbdb_invalid.json   genus names PBDB treats as invalid (nomina dubia, synonyms...) with the reason
  pbdb_occs.json      occurrences, one pipe-separated row each (layout of scripts/fetch/pbdb.py)
  pbdb_colls.json     collections of those occurrences (coordinates, environment, lithology)
  wiki.json           per genus: English Wikipedia title, fixed revision, plain text, taxobox fields, citations
                      of that revision, files used in the article
  commons.json        per Commons file (article images + Category:<Genus> and its direct sub-categories):
                      licence, author, description, size, thumbnail address, where it was found
  phylopic.json       per genus: the PhyloPic silhouette of the genus, or of the closest relative found
and, with --sheets, one contact sheet per genus (numbered thumbnails of every candidate image) for visual review.
Genus entries are never written here: they are drafted and curated by hand (CLAUDE.md §4).
"""
import datetime, html, io, json, pathlib, re, sys, time, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/fetch"))
from pbdb import get as pbdb_get, occ_row, coll  # noqa: E402

UA = {"User-Agent": "AtlasOfLife/1.0 (https://github.com/pcontem/Atlas_of_life; data harvest for a sourced encyclopedia)"}
WIKI = "https://en.wikipedia.org/w/api.php"
COMMONS = "https://commons.wikimedia.org/w/api.php"
TODAY = datetime.date.today().isoformat()


def fetch_json(url, params=None, tries=4):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.loads(r.read())
        except Exception as e:
            code = getattr(e, "code", None)
            if code and 400 <= code < 500 and code != 429:  # not found etc.: retrying will not help
                return None
            if k == tries - 1:
                print(f"  ! {url[:160]}: {e}")
                return None
            time.sleep(3 * (k + 1))


def mw(api, **p):
    p.update(format="json", formatversion=2, maxlag=5)
    time.sleep(0.25)
    return fetch_json(api, p) or {}


# ---------- PBDB ----------
def pbdb(base):
    gen = pbdb_get("taxa/list.json", base_name=base, rank="genus", taxon_status="valid", show="attr,app,parent,class,ref", vocab="pbdb")
    sp = pbdb_get("taxa/list.json", base_name=base, rank="species", taxon_status="valid", show="attr,app,parent", vocab="pbdb")
    inv = pbdb_get("taxa/list.json", base_name=base, rank="genus", taxon_status="invalid", show="attr,parent,ref", vocab="pbdb")
    keep = ["taxon_no", "orig_no", "taxon_name", "taxon_attr", "taxon_rank", "parent_name", "family", "order", "class",
            "firstapp_max_ma", "firstapp_min_ma", "lastapp_max_ma", "lastapp_min_ma", "early_interval", "late_interval",
            "n_occs", "is_extant", "primary_reference", "reference_no", "accepted_name", "difference", "status"]
    slim = lambda r: {k: r.get(k) for k in keep if r.get(k) not in (None, "")}
    species = {}
    for r in sp:
        species.setdefault(r["taxon_name"].split()[0], []).append(slim(r))
    return [slim(r) for r in gen], species, [slim(r) for r in inv]


def occs(base):
    recs = pbdb_get("occs/list.json", base_name=base, show="coords,loc,strat", vocab="pbdb")
    rows = [x for x in (occ_row(r) for r in recs) if x]
    ids = sorted({r.split("|")[12][4:] for r in rows}, key=int)
    cols = {}
    for i in range(0, len(ids), 150):
        for r in pbdb_get("colls/list.json", id=",".join(ids[i:i + 150]), show="geo,lith,loc,strat", vocab="pbdb"):
            cols[str(r["collection_no"])] = coll(r)
    return rows, dict(cols=cols, byname={}, downloaded=TODAY)


# ---------- Wikipedia ----------
CITE = re.compile(r"\{\{\s*[Cc]ite (journal|book|web|news|conference|thesis)([\s\S]*?)\}\}")
CITE_KEYS = re.compile(r"^(last\d*|first\d*|author\d*|authors|vauthors|year|date|title|journal|volume|issue|pages|doi|"
                       r"publisher|url|chapter|isbn|pmid|pmc|website)$")


def cites(wt):
    out, seen = [], set()
    for m in CITE.finditer(wt):
        f = {"type": m.group(1)}
        for kv in m.group(2).split("|")[1:]:
            if "=" in kv:
                k, v = kv.split("=", 1)
                k, v = k.strip().lower(), v.strip()
                if v and CITE_KEYS.match(k):
                    f[k] = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", v)[:400]
        key = (f.get("doi") or f.get("title") or "").lower()
        if f.get("title") and key not in seen:
            seen.add(key)
            out.append(f)
    return out


TAXOBOX = ("type_species", "type_species_authority", "image", "image_caption", "fossil_range", "taxon", "authority",
           "parent", "subdivision_ranks", "subdivision", "synonyms")


def taxobox(wt):
    m = re.search(r"\{\{\s*(?:Automatic taxobox|Speciesbox|Taxobox)([\s\S]*?)\n\}\}", wt, re.I)
    if not m:
        return {}
    out = {}
    for line in m.group(1).split("\n|"):
        if "=" in line:
            k, v = line.split("=", 1)
            k = k.strip().lstrip("|").strip().lower()
            if k in TAXOBOX and v.strip():
                out[k] = v.strip()[:600]
    return out


GENUS_WORDS = re.compile(r"\b(genus|genera)\b", re.I)


def wiki(names):
    res = {}
    for i in range(0, len(names), 40):
        chunk = names[i:i + 40]
        r = mw(WIKI, action="query", redirects=1, prop="revisions|pageprops|images", rvprop="ids|timestamp|content",
               rvslots="main", ppprop="disambiguation", imlimit="max", titles="|".join(chunk))
        q = r.get("query", {})
        norm = {n["from"]: n["to"] for n in q.get("normalized", [])}
        red = {n["from"]: n["to"] for n in q.get("redirects", [])}
        pages = {p["title"]: p for p in q.get("pages", [])}
        for g in chunk:
            t = norm.get(g, g)
            t = red.get(t, t)
            p = pages.get(t)
            if not p or p.get("missing") or "revisions" not in p:
                res[g] = {"missing": True}
                continue
            rv = p["revisions"][0]
            wt = rv["slots"]["main"]["content"]
            res[g] = dict(title=p["title"], revid=rv["revid"], ts=rv["timestamp"], redirected=(t != g),
                          disambiguation="disambiguation" in p.get("pageprops", {}), taxobox=taxobox(wt),
                          cites=cites(wt), files=[im["title"] for im in p.get("images", [])
                                                  if re.search(r"\.(jpe?g|png|svg|tiff?|webp|gif)$", im["title"], re.I)])
    for k, (g, w) in enumerate(res.items()):
        if k % 50 == 0:
            print(f"  wikipedia text {k}/{len(res)}", flush=True)
        if w.get("missing"):
            continue
        e = mw(WIKI, action="query", prop="extracts", explaintext=1, exsectionformat="wiki", titles=w["title"])
        pg = (e.get("query", {}).get("pages") or [{}])[0]
        w["text"] = pg.get("extract", "")
        # a redirect to a family or a broader article is flagged so the entry does not mistake it for the genus
        w["about_genus"] = bool(re.search(rf"\b{re.escape(g)}\b[^.]{{0,120}}\b(is|was)\b[^.]{{0,80}}{GENUS_WORDS.pattern}",
                                          w["text"][:1500]))
    return res


# ---------- Commons ----------
META = ("Artist", "LicenseShortName", "LicenseUrl", "UsageTerms", "ImageDescription", "Credit", "DateTimeOriginal",
        "AttributionRequired", "Copyrighted", "Restrictions")


def strip_html(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def cap_for(n_species):
    """Candidates per genus (owner, 2026-11-17): at most 15, or one per species when the genus has more."""
    return max(15, n_species)


def commons(wikires, names, nsp, living=()):
    """Candidate pictures per genus, at most cap_for(species): the article's own pictures first, then (extinct
    genera only) Category:<Genus> and its sub-categories. Living genera use the article's pictures alone."""
    files = {}

    def add(title, genus, where):
        title = "File:" + title.split(":", 1)[1] if ":" in title else "File:" + title
        f = files.setdefault(title, {"genera": [], "found": []})
        if genus not in f["genera"]:
            f["genera"].append(genus)
        if where not in f["found"]:
            f["found"].append(where)

    for k, g in enumerate(names):
        if k % 50 == 0:
            print(f"  commons {k}/{len(names)}", flush=True)
        cap, got = cap_for(nsp.get(g, 0)), []
        art = [t for t in (wikires.get(g) or {}).get("files", []) if not re.search(r"(map|range|distribution|\.svg$|icon|logo|status)", t, re.I)]
        # the article's pictures that name the genus first; the others are often navigation-box pictures of
        # related genera, so they come last, after the Commons categories
        named = [t for t in art if g.lower() in t.lower()]
        other = [t for t in art if t not in named]
        for t in named:
            if len(got) < cap and t not in got:
                got.append(t)
                add(t, g, "wikipedia")
        if g in living:
            for t in other:
                if len(got) < cap and t not in got:
                    got.append(t)
                    add(t, g, "wikipedia")
            continue
        cats = [f"Category:{g}"]
        sub = mw(COMMONS, action="query", list="categorymembers", cmtitle=f"Category:{g}", cmtype="subcat", cmlimit=15)
        cats += [c["title"] for c in sub.get("query", {}).get("categorymembers", [])]
        for c in cats if len(got) < cap else []:
            if len(got) >= cap:
                break
            r = mw(COMMONS, action="query", list="categorymembers", cmtitle=c, cmtype="file", cmlimit=cap)
            for m in r.get("query", {}).get("categorymembers", []):
                t = "File:" + m["title"].split(":", 1)[1]
                if len(got) < cap and t not in got:
                    got.append(t)
                    add(t, g, c)
        for t in other:
            if len(got) < cap and t not in got:
                got.append(t)
                add(t, g, "wikipedia (other picture of the article)")
    titles = sorted(files)
    for i in range(0, len(titles), 40):
        r = mw(COMMONS, action="query", prop="imageinfo", iiprop="url|size|mime|extmetadata", iiurlwidth=330,
               titles="|".join(titles[i:i + 40]))
        for p in r.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [None])[0]
            if not ii or p["title"] not in files:
                continue
            md = ii.get("extmetadata", {})
            files[p["title"]].update(url=ii.get("url"), page=ii.get("descriptionurl"), thumb=ii.get("thumburl"),
                                     width=ii.get("width"), height=ii.get("height"), mime=ii.get("mime"),
                                     **{k: strip_html(md.get(k, {}).get("value", ""))[:500] for k in META if k in md})
    return files


# ---------- PhyloPic ----------
def phylopic(names, lineage):
    root = fetch_json("https://api.phylopic.org/") or {}
    build = root.get("build")
    out = {}
    for k, g in enumerate(names):
        if k % 50 == 0:
            print(f"  phylopic {k}/{len(names)}", flush=True)
        for name in [g] + lineage.get(g, []):
            n = fetch_json("https://api.phylopic.org/nodes", dict(build=build, filter_name=name.lower(), embed_items="true",
                                                                 embed_primaryImage="true", page=0))
            time.sleep(0.2)
            items = (n or {}).get("_embedded", {}).get("items", [])
            img = next((it.get("_embedded", {}).get("primaryImage") for it in items
                        if it.get("_embedded", {}).get("primaryImage")), None)
            if img:
                L = img["_links"]
                rasters = sorted(L.get("rasterFiles", []), key=lambda x: int(x["sizes"].split("x")[0]))
                out[g] = dict(uuid=img["uuid"], attribution=img.get("attribution") or L.get("contributor", {}).get("title"),
                              license=L.get("license", {}).get("href"), matched=name, genus_level=(name == g),
                              depicts=(L.get("specificNode") or {}).get("title"),
                              vector=(L.get("vectorFile") or {}).get("href"),
                              png=next((x["href"] for x in rasters if int(x["sizes"].split("x")[0]) >= 512), None),
                              page=f"https://www.phylopic.org/images/{img['uuid']}")
                break
    return out


# ---------- contact sheets ----------
def sheets(files, names, outdir):
    from PIL import Image, ImageDraw
    outdir.mkdir(parents=True, exist_ok=True)
    for k, g in enumerate(names):
        if k % 50 == 0:
            print(f"  sheets {k}/{len(names)}", flush=True)
        cand = [(t, f) for t, f in sorted(files.items()) if g in f["genera"] and f.get("thumb")]
        if not cand:
            continue
        cols, cw, ch = 4, 330, 300
        rows = (len(cand) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cw, rows * ch), "white")
        d = ImageDraw.Draw(sheet)
        for k, (t, f) in enumerate(cand):
            x, y = (k % cols) * cw, (k // cols) * ch
            try:
                with urllib.request.urlopen(urllib.request.Request(f["thumb"], headers=UA), timeout=60) as r:
                    im = Image.open(io.BytesIO(r.read())).convert("RGB")
                im.thumbnail((cw - 10, ch - 40))
                sheet.paste(im, (x + 5, y + 5))
            except Exception:
                d.text((x + 10, y + 100), "(could not load)", fill="red")
            d.text((x + 5, y + ch - 32), f"{k + 1}. {t[5:][:44]}", fill="black")
            time.sleep(0.1)
        sheet.save(outdir / f"{g}.jpg", quality=70)


def main():
    a = sys.argv[1:]
    vol, base = a[0], a[1]
    only = a[a.index("--genera") + 1].split(",") if "--genera" in a else None
    sheet_dir = pathlib.Path(a[a.index("--sheets") + 1]) if "--sheets" in a else None
    raw = ROOT / "data/raw" / vol
    raw.mkdir(parents=True, exist_ok=True)
    w = lambda name, obj: (raw / name).write_text(json.dumps(obj, ensure_ascii=False, indent=0))
    print("PBDB taxa…")
    gen, species, inv = pbdb(base)
    names = sorted(r["taxon_name"] for r in gen)
    if only:
        names = [n for n in names if n in only]
    w("pbdb_genera.json", dict(downloaded=TODAY, base=base, records=gen))
    w("pbdb_species.json", dict(downloaded=TODAY, base=base, species=species))
    w("pbdb_invalid.json", dict(downloaded=TODAY, base=base, records=inv))
    print("PBDB occurrences and collections…")
    rows, cols = occs(base)
    w("pbdb_occs.json", rows)
    w("pbdb_colls.json", cols)
    print(f"Wikipedia ({len(names)} genera)…")
    wk = wiki(names)
    w("wiki.json", dict(downloaded=TODAY, pages=wk))
    print("Commons…", flush=True)
    living = {r["taxon_name"] for r in gen if r.get("is_extant") in ("extant", True, 1, "1")}
    nsp = {g: len(v) for g, v in species.items()}
    print(f"{len(living)} living genera (article pictures only); at most max(15, species) candidates per genus")
    files = commons(wk, names, nsp, living)
    w("commons.json", dict(downloaded=TODAY, files=files))
    print("PhyloPic…")
    lineage = {r["taxon_name"]: [x for x in (r.get("family"), r.get("parent_name"), r.get("order")) if x and x != "NO_FAMILY_SPECIFIED"]
               for r in gen}
    w("phylopic.json", dict(downloaded=TODAY, silhouettes=phylopic(names, lineage)))
    if sheet_dir:
        print("Contact sheets…")
        sheets(files, names, sheet_dir)
    print(f"done: {len(names)} genera, {len(rows)} occurrences, {len(files)} Commons files")


if __name__ == "__main__":
    main()
