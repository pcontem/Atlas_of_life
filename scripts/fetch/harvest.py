"""Harvest the raw material for a new genus volume (runs in GitHub Actions: .github/workflows/harvest.yml).

    python3 scripts/fetch/harvest.py <volume> <PBDB base taxon> [--genera A,B,...] [--sheets DIR] [--papers] [--wiki-group <census group>] [--extra A,B]
                                     [--living <COL taxa, comma-separated>] [--living-only]

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
  wiki_only.json      with --wiki-group: genera Wikipedia recognises (genus articles in the census categories) but PBDB lacks
  phylopic.json       per genus: the PhyloPic silhouette of the genus, or of the closest relative found
  col_living.json     with --living: living genera of the Catalogue of Life under the given taxa (authority, family,
                      accepted living species); those PBDB lacks are harvested too (Wikipedia, Commons, PhyloPic)
  inat.json           with --living: CC0 / CC BY / CC BY-SA photographs of the living genera from iNaturalist, in the
                      record layout of commons.json (scripts/fetch/living.py)
  papers.json         with --papers: per genus, scientific articles that name it (OpenAlex + Europe PMC): citation, DOI,
                      year, open-access status and licence, abstract (to find the primary literature; never copied into entries)
  oa_figures.json     with --papers (or --oa on data already harvested): figures of CC BY / CC0 articles naming the genus
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


def mw_pages(api, **p):
    """Like mw, but follows the API's `continue` token and merges the pages of every answer. A query with
    `imlimit=max` over 40 titles returns at most 500 images in all, so without this the pages that come last
    in the alphabet lost all their pictures (2026-11-22: 200 of 449 Sauropodomorpha pages had none)."""
    merged, norm, red, cont = {}, [], [], {}
    for _ in range(60):
        r = mw(api, **p, **cont)
        q = r.get("query", {})
        norm += q.get("normalized", [])
        red += q.get("redirects", [])
        for pg in q.get("pages", []):
            m = merged.setdefault(pg["title"], {})
            for k, v in pg.items():
                if isinstance(v, list):
                    m[k] = m.get(k, []) + v
                else:
                    m[k] = v
        cont = r.get("continue")
        if not cont:
            break
    return dict(query=dict(pages=list(merged.values()), normalized=norm, redirects=red))


# ---------- PBDB ----------
def pbdb(base):
    gen = pbdb_get("taxa/list.json", base_name=base, rank="genus", taxon_status="valid", show="attr,app,parent,class,ref", vocab="pbdb")
    sp = pbdb_get("taxa/list.json", base_name=base, rank="species", taxon_status="valid", show="attr,app,parent", vocab="pbdb")
    inv = pbdb_get("taxa/list.json", base_name=base, rank="genus", taxon_status="invalid", show="attr,parent,ref", vocab="pbdb")
    keep = ["taxon_no", "orig_no", "taxon_name", "taxon_attr", "taxon_rank", "parent_name", "family", "order", "class",
            "firstapp_max_ma", "firstapp_min_ma", "lastapp_max_ma", "lastapp_min_ma", "early_interval", "late_interval",
            "n_occs", "is_extant", "flags", "type_taxon_name", "primary_reference", "reference_no", "accepted_name", "difference", "status"]
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


def wiki_only_genera(group, pbdb_names, skip=()):
    """Genera that English Wikipedia recognises (articles in the group's categories of data/census/sources.yaml that
    are genus articles) but PBDB does not list as valid. Wikipedia recognition is enough to harvest them (owner,
    2026-11-27). Names already in the atlas (entries, excluded.yaml, backbone nodes without a PBDB record count too)
    are skipped only when excluded or already written; -> {genus: {"title", "category"}}."""
    import yaml
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import census
    cfg = yaml.safe_load((ROOT / "data/census/sources.yaml").read_text())[group]
    w = cfg.get("wikipedia") or {}
    pages, _, _, _ = census.wiki_category_pages(w.get("categories", []), w.get("depth", 3))
    atlas = census.load_atlas()
    cand = {}
    for t, cat in pages.items():
        n = census.title_to_name(t)
        if n and n not in pbdb_names and n not in atlas["excluded"] and n not in atlas["entries"] and n not in skip:
            cand.setdefault(n, (t, cat))
    out = {}
    titles = sorted(t for t, _ in cand.values())
    for i in range(0, len(titles), 40):
        chunk = titles[i:i + 40]
        r = mw(WIKI, action="query", prop="revisions", rvprop="content", rvslots="main", titles="|".join(chunk))
        for pg in r.get("query", {}).get("pages", []):
            if "revisions" not in pg:
                continue
            wt = pg["revisions"][0]["slots"]["main"]["content"]
            n = census.title_to_name(pg["title"])
            if n in cand and census.wiki_is_genus(wt, n):
                out[n] = dict(title=pg["title"], category=cand[n][1])
    return out


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


def wiki(names, titles=None):
    """titles: {genus: article title to ask for instead of the genus name} (e.g. "Mei (dinosaur)")."""
    titles = titles or {}
    res = {}
    for i in range(0, len(names), 40):
        chunk = names[i:i + 40]
        r = mw_pages(WIKI, action="query", redirects=1, prop="revisions|pageprops|images", rvprop="ids|timestamp|content",
               rvslots="main", ppprop="disambiguation", imlimit="max", titles="|".join(titles.get(g, g) for g in chunk))
        q = r.get("query", {})
        norm = {n["from"]: n["to"] for n in q.get("normalized", [])}
        red = {n["from"]: n["to"] for n in q.get("redirects", [])}
        pages = {p["title"]: p for p in q.get("pages", [])}
        for g in chunk:
            t = titles.get(g, g)
            t = norm.get(t, t)
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


def wiki_retry(wk):
    """Genera whose page is missing, a disambiguation page or not about the genus (Mei, Yi, Anzu…): ask again for
    "<Genus> (dinosaur)" and keep the answer only when that page is about the genus."""
    bad = [g for g, w in wk.items() if w.get("missing") or w.get("disambiguation") or not w.get("about_genus")]
    if not bad:
        return []
    new = wiki(bad, {g: f"{g} (dinosaur)" for g in bad})
    # a page asked for as "<Genus> (dinosaur)" is about the genus when it calls itself a genus near the start
    ok = lambda w: w.get("about_genus") or re.search(r"\bgenus\b", w.get("text", "")[:700])
    fixed = [g for g, w in new.items() if not w.get("missing") and not w.get("disambiguation") and ok(w)]
    for g in fixed:
        new[g]["about_genus"] = True
    for g in fixed:
        wk[g] = new[g]
    print(f"  wikipedia retry: {len(fixed)} of {len(bad)} pages found as '<Genus> (dinosaur)'")
    return fixed


# ---------- Commons ----------
META = ("Artist", "LicenseShortName", "LicenseUrl", "UsageTerms", "ImageDescription", "Credit", "DateTimeOriginal",
        "AttributionRequired", "Copyrighted", "Restrictions")


def strip_html(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


NOISE = re.compile(r"(size comparison|size chart|scale|cladogram|distribution|\bmap\b|sculpture|statue|stamp|poster|cartoon|\bmodel\b|diplosil|silhouette)", re.I)


def cap_for(n_species):
    """Candidates per genus (owner, 2026-11-17): at most 15, or one per species when the genus has more."""
    return max(15, n_species)


def commons(wikires, names, nsp, living=()):
    """Candidate pictures per genus, at most cap_for(species): the article's own pictures first, then
    Category:<Genus> and its sub-categories. Living genera read the categories too (owner, 2026-11-28; before, they
    used the article's pictures alone), after all the article's pictures."""
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
        cats = [f"Category:{g}"]
        sub = mw(COMMONS, action="query", list="categorymembers", cmtitle=f"Category:{g}", cmtype="subcat", cmlimit=15)
        cats += [c["title"] for c in sub.get("query", {}).get("categorymembers", [])]
        # Category:<Genus> alone could fill the whole cap with its first files in alphabetical order and leave the
        # sub-categories (fossils, skulls, life restorations, mounts) unread; so each category gives a share first
        # and the rest of the cap is filled afterwards. Charts, maps, models and the like are skipped.
        share = max(3, -(-cap // max(1, len(cats))))
        members = {}
        for c in cats if len(got) < cap else []:
            r = mw(COMMONS, action="query", list="categorymembers", cmtitle=c, cmtype="file", cmlimit=max(cap, 50))
            members[c] = ["File:" + m["title"].split(":", 1)[1] for m in r.get("query", {}).get("categorymembers", [])
                          if not NOISE.search(m["title"])]
        for limit in (share, cap):
            for c, ts in members.items():
                taken = 0
                for t in ts:
                    if len(got) >= cap or taken >= limit:
                        break
                    if t not in got:
                        got.append(t)
                        add(t, g, c)
                        taken += 1
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


# ---------- open-access article figures (Europe PMC) ----------
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"


def oa_one(g, max_articles=4):
    import xml.etree.ElementTree as ET
    q = f'"{g}" AND OPEN_ACCESS:y AND (LICENSE:"cc by" OR LICENSE:"cc0")'
    r = fetch_json(f"{EPMC}/search", dict(query=q, resultType="core", format="json", pageSize=25)) or {}
    arts = [a for a in r.get("resultList", {}).get("result", []) if a.get("pmcid")]
    arts.sort(key=lambda a: (g.lower() not in (a.get("title") or "").lower(), -int(a.get("pubYear") or 0)))
    figs = []
    for a in arts[:max_articles]:
        try:
            with urllib.request.urlopen(urllib.request.Request(f"{EPMC}/{a['pmcid']}/fullTextXML", headers=UA), timeout=40) as rr:
                root = ET.fromstring(rr.read())
        except Exception:
            continue
        for fig in root.iter("fig"):
            cap = re.sub(r"\s+", " ", " ".join("".join(c.itertext()) for c in fig.iter("caption"))).strip()
            if g.lower() not in cap.lower():
                continue
            gr = fig.find(".//graphic")
            href = gr.get("{http://www.w3.org/1999/xlink}href") if gr is not None else None
            if not href:
                continue
            lab = "".join(fig.find("label").itertext()).strip() if fig.find("label") is not None else ""
            figs.append(dict(pmcid=a["pmcid"], doi=a.get("doi"), license=a.get("license"),
                             cite=f"{a.get('authorString', '')} {a.get('pubYear', '')}. {a.get('title', '')} "
                                  f"{(a.get('journalInfo') or {}).get('journal', {}).get('title', '')}.",
                             label=lab, caption=cap[:600],
                             img=f"https://europepmc.org/articles/{a['pmcid']}/bin/{href}{'' if '.' in href else '.jpg'}"))
    return figs[:15]


def oa_figures(names, max_articles=4):
    """Figures that mention the genus in their caption, from CC BY / CC0 open-access articles in Europe PMC
    (8 genera at a time)."""
    from concurrent.futures import ThreadPoolExecutor
    out = {}
    with ThreadPoolExecutor(8) as ex:
        for k, (g, figs) in enumerate(zip(names, ex.map(lambda g: oa_one(g, max_articles), names))):
            out[g] = figs
            if k % 25 == 0:
                print(f"  oa {k}/{len(names)}", flush=True)
    return out


def oa_sheets(oa, outdir):
    from concurrent.futures import ThreadPoolExecutor
    outdir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda kv: oa_sheet(kv[0], kv[1], outdir), oa.items()))


def oa_sheet(g, figs, outdir):
    from PIL import Image, ImageDraw
    if True:
        if not figs:
            return
        cols, cw, ch = 4, 330, 300
        sheet = Image.new("RGB", (cols * cw, ((len(figs) + cols - 1) // cols) * ch), "white")
        d = ImageDraw.Draw(sheet)
        for k, f in enumerate(figs):
            x, y = (k % cols) * cw, (k // cols) * ch
            try:
                with urllib.request.urlopen(urllib.request.Request(f["img"], headers=UA), timeout=60) as r:
                    im = Image.open(io.BytesIO(r.read())).convert("RGB")
                im.thumbnail((cw - 10, ch - 40))
                sheet.paste(im, (x + 5, y + 5))
            except Exception:
                d.text((x + 10, y + 100), "(could not load)", fill="red")
            d.text((x + 5, y + ch - 32), f"{k + 1}. {f['pmcid']} {f['label']}"[:50], fill="black")
        sheet.save(outdir / f"oa_{g}.jpg", quality=70)


# ---------- scientific articles (OpenAlex + Europe PMC) ----------
OPENALEX = "https://api.openalex.org/works"
FOSSIL_WORDS = "(dinosaur OR dinosaurs OR theropod OR fossil OR Cretaceous OR Jurassic OR Triassic OR Paleocene OR Eocene OR Miocene)"


def _abstract(inv):
    if not inv:
        return ""
    pos = sorted((i, w) for w, ii in inv.items() for i in ii)
    return " ".join(w for _, w in pos)


def papers_one(g, per_source=12):
    """Articles whose title or abstract names the genus, with a fossil word to drop homonyms. Abstracts are cut to
    1500 characters so the file stays small; the full text is read from the DOI when an entry is written."""
    out = {}
    r = fetch_json(OPENALEX, {"filter": f'title_and_abstract.search:"{g}" AND {FOSSIL_WORDS}', "sort": "publication_year:desc",
                              "per-page": per_source, "mailto": "atlas-of-life@users.noreply.github.com"}) or {}
    for wk in r.get("results", []):
        doi = (wk.get("doi") or "").replace("https://doi.org/", "").lower() or None
        src = ((wk.get("primary_location") or {}).get("source") or {})
        oa = wk.get("open_access") or {}
        key = doi or wk.get("id")
        out[key] = dict(title=wk.get("display_name") or "", year=wk.get("publication_year"), doi=doi,
                        authors=", ".join(a["author"]["display_name"] for a in (wk.get("authorships") or [])[:8] if a.get("author")),
                        journal=src.get("display_name") or "", oa=bool(oa.get("is_oa")), oa_url=oa.get("oa_url"),
                        license=(wk.get("primary_location") or {}).get("license"), cited_by=wk.get("cited_by_count"),
                        in_title=g.lower() in (wk.get("display_name") or "").lower(),
                        abstract=_abstract(wk.get("abstract_inverted_index"))[:1500], found_in=["openalex"])
    r = fetch_json(f"{EPMC}/search", dict(query=f'(TITLE:"{g}" OR ABSTRACT:"{g}") AND {FOSSIL_WORDS}', resultType="core",
                                          format="json", pageSize=per_source, sort="P_PDATE_D desc")) or {}
    for a in r.get("resultList", {}).get("result", []):
        doi = (a.get("doi") or "").lower() or None
        key = doi or a.get("pmcid") or a.get("id")
        if key in out:
            out[key]["found_in"].append("europepmc")
            out[key]["pmcid"] = a.get("pmcid")
            if not out[key]["abstract"]:
                out[key]["abstract"] = re.sub(r"<[^>]+>", "", a.get("abstractText") or "")[:1500]
            continue
        out[key] = dict(title=a.get("title") or "", year=int(a["pubYear"]) if str(a.get("pubYear", "")).isdigit() else None,
                        doi=doi, pmcid=a.get("pmcid"), authors=a.get("authorString", "")[:300],
                        journal=((a.get("journalInfo") or {}).get("journal") or {}).get("title", ""),
                        oa=a.get("isOpenAccess") == "Y", oa_url=None, license=a.get("license"), cited_by=a.get("citedByCount"),
                        in_title=g.lower() in (a.get("title") or "").lower(),
                        abstract=re.sub(r"<[^>]+>", "", a.get("abstractText") or "")[:1500], found_in=["europepmc"])
    return sorted(out.values(), key=lambda x: (not x["in_title"], -(x["year"] or 0)))


def papers(names):
    from concurrent.futures import ThreadPoolExecutor
    out = {}
    with ThreadPoolExecutor(6) as ex:
        for k, (g, ps) in enumerate(zip(names, ex.map(papers_one, names))):
            out[g] = ps
            if k % 25 == 0:
                print(f"  papers {k}/{len(names)}", flush=True)
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


def all_names(raw):
    """PBDB genera of a harvested volume plus the Wikipedia-only ones (wiki_only.json) and the --extra ones."""
    n = {r["taxon_name"] for r in json.loads((raw / "pbdb_genera.json").read_text())["records"]}
    if (raw / "wiki_only.json").exists():
        n |= set(json.loads((raw / "wiki_only.json").read_text())["genera"])
    if (raw / "col_living.json").exists():
        n |= set(json.loads((raw / "col_living.json").read_text())["genera"])
    return sorted(n)


COL_SOURCE = "Catalogue of Life, latest release (ChecklistBank dataset 3LR), https://api.checklistbank.org/dataset/3LR"
INAT_SOURCE = "iNaturalist API v1 (taxon photos and species default photos; CC0, CC BY and CC BY-SA photos only)"


def written_genera(other_than=None):
    """Genera that already have an entry in a volume (other than `other_than`)."""
    return {p.stem for p in (ROOT / "entries").glob("*/genera/*.yaml") if p.parts[-3] != other_than}


def add_genera(raw, w, names, living=(), lineage=None, nsp=None, with_papers=True):
    """Wikipedia, Commons, PhyloPic (and, with_papers, articles and open-access figures) for `names`, merged into the
    files already harvested in `raw`. Returns the merged commons.json files."""
    def load(f, key, default):
        return json.loads((raw / f).read_text()) if (raw / f).exists() else {"downloaded": TODAY, key: default}
    wk = wiki(names)
    wiki_retry(wk)
    old = load("wiki.json", "pages", {})
    old["pages"].update(wk)
    old.setdefault("added", []).append(dict(downloaded=TODAY, genera=names))
    w("wiki.json", old)
    files = commons(wk, names, nsp or {}, set(living))
    oc = load("commons.json", "files", {})
    for t, f in files.items():
        if t in oc["files"]:
            oc["files"][t]["genera"] = sorted(set(oc["files"][t].get("genera", [])) | set(f["genera"]))
        else:
            oc["files"][t] = f
    w("commons.json", oc)
    pl = load("phylopic.json", "silhouettes", {})
    pl["silhouettes"].update(phylopic(names, lineage or {}))
    w("phylopic.json", pl)
    if with_papers:
        pp = papers(names)
        op = load("papers.json", "papers", {})
        op.setdefault("sources", ["OpenAlex", "Europe PMC"])
        op["papers"].update(pp)
        w("papers.json", op)
        oa = oa_figures(names)
        of = load("oa_figures.json", "figures", {})
        of["figures"].update(oa)
        w("oa_figures.json", of)
    return oc["files"]


def main():
    a = sys.argv[1:]
    vol, base = a[0], a[1]
    only = a[a.index("--genera") + 1].split(",") if "--genera" in a else None
    sheet_dir = pathlib.Path(a[a.index("--sheets") + 1]) if "--sheets" in a else None
    raw = ROOT / "data/raw" / vol
    raw.mkdir(parents=True, exist_ok=True)
    w = lambda name, obj: (raw / name).write_text(json.dumps(obj, ensure_ascii=False, indent=0))
    if "--oa" in a:  # open-access figures for the listed genera (or all), added to data already harvested
        names = only or all_names(raw)
        oaf = raw / "oa_figures.json"
        old = json.loads(oaf.read_text())["figures"] if oaf.exists() else {}
        new = oa_figures(names)
        old.update(new)
        w("oa_figures.json", dict(downloaded=TODAY, figures=old))
        if sheet_dir:
            oa_sheets(new, sheet_dir)
        print(f"done: {sum(len(v) for v in new.values())} figures for {len(new)} genera")
        return
    if "--living-only" in a:  # living genera (Catalogue of Life) and their photographs, added to data already harvested
        import living as L
        bases = a[a.index("--living") + 1].split(",")
        inv = {r["taxon_name"] for r in json.loads((raw / "pbdb_invalid.json").read_text())["records"]} if (raw / "pbdb_invalid.json").exists() else set()
        known = set(all_names(raw))
        col = L.col_genera(fetch_json, bases, skip=inv)
        w("col_living.json", dict(downloaded=TODAY, source=COL_SOURCE, bases=bases, genera=col))
        new = sorted(set(col) - known - written_genera())
        print(f"{len(col)} living genera in COL, {len(new)} not yet harvested: {', '.join(new[:40])}{' …' if len(new) > 40 else ''}")
        lineage = {g: [x for x in (col[g]["family"], col[g]["order"]) if x] for g in new}
        files = add_genera(raw, w, new, living=set(new), lineage=lineage, nsp={g: len(col[g]["species"]) for g in new}, with_papers=False)
        pb = json.loads((raw / "pbdb_genera.json").read_text())["records"] if (raw / "pbdb_genera.json").exists() else []
        living = (set(col) | {r["taxon_name"] for r in pb if r.get("is_extant") in ("extant", True, 1, "1")}) - written_genera(other_than=vol)
        nsp = {g: max(len(col.get(g, {}).get("species", [])), 1) for g in living}
        inat = L.inat_photos(fetch_json, sorted(living), bases, cap=lambda g: cap_for(nsp.get(g, 0)))
        w("inat.json", dict(downloaded=TODAY, source=INAT_SOURCE, files=inat))
        if sheet_dir:
            allf = json.loads((raw / "commons.json").read_text())["files"]
            allf.update(inat)
            sheets(allf, sorted(set(new) | living), sheet_dir)
        print(f"done: {len(new)} new living genera, {len(inat)} iNaturalist photos for {len(living)} living genera")
        return
    if "--extra" in a:  # genera that PBDB does not list as valid (Wikipedia-only, backbone nodes): added to data already harvested
        names = a[a.index("--extra") + 1].split(",")
        print(f"Extra genera by name: {names}")
        files = add_genera(raw, w, names, with_papers=True)
        if sheet_dir:
            sheets(files, names, sheet_dir)
        print(f"done: {len(names)} extra genera, {len(files)} Commons files")
        return
    if "--wiki-retry" in a:  # second try for wrong Wikipedia pages, on data already harvested
        wf = raw / "wiki.json"
        wk = json.loads(wf.read_text())
        fixed = wiki_retry(wk["pages"])
        wk["retried"] = dict(downloaded=TODAY, genera=fixed)
        w("wiki.json", wk)
        return
    if "--sheets-only" in a:  # contact sheets from data already harvested
        files = json.loads((raw / "commons.json").read_text())["files"]
        if (raw / "inat.json").exists():
            files.update(json.loads((raw / "inat.json").read_text())["files"])
        names = only or all_names(raw)
        sheets(files, names, sheet_dir)
        return
    w = lambda name, obj: (raw / name).write_text(json.dumps(obj, ensure_ascii=False, indent=0))
    print("PBDB taxa…")
    gen, species, inv = pbdb(base)
    names = sorted(r["taxon_name"] for r in gen)
    if only:
        names = [n for n in names if n in only]
    if "--wiki-group" in a:  # Wikipedia recognition is enough: genera of the group's Wikipedia categories PBDB lacks
        wo = wiki_only_genera(a[a.index("--wiki-group") + 1], set(names) | {r["taxon_name"] for r in inv})
        w("wiki_only.json", dict(downloaded=TODAY, group=a[a.index("--wiki-group") + 1], genera=wo))
        print(f"{len(wo)} genera known to Wikipedia but not valid in PBDB: {', '.join(sorted(wo))}")
        names = sorted(set(names) | set(wo))
    col, bases_l = {}, []
    if "--living" in a:  # living genera of the Catalogue of Life (PBDB only knows those with a fossil record)
        import living as L
        bases_l = a[a.index("--living") + 1].split(",")
        col = L.col_genera(fetch_json, bases_l, skip={r["taxon_name"] for r in inv} | written_genera(other_than=vol))
        if only:
            col = {g: d for g, d in col.items() if g in only}
        w("col_living.json", dict(downloaded=TODAY, source=COL_SOURCE, bases=bases_l, genera=col))
        print(f"{len(col)} living genera in COL, {len(set(col) - set(names))} of them not in PBDB")
        names = sorted(set(names) | set(col))
    w("pbdb_genera.json", dict(downloaded=TODAY, base=base, records=gen))
    w("pbdb_species.json", dict(downloaded=TODAY, base=base, species=species))
    w("pbdb_invalid.json", dict(downloaded=TODAY, base=base, records=inv))
    print("PBDB occurrences and collections…")
    rows, cols = occs(base)
    w("pbdb_occs.json", rows)
    w("pbdb_colls.json", cols)
    print(f"Wikipedia ({len(names)} genera)…")
    wk = wiki(names)
    wiki_retry(wk)
    w("wiki.json", dict(downloaded=TODAY, pages=wk))
    print("Commons…", flush=True)
    living = {r["taxon_name"] for r in gen if r.get("is_extant") in ("extant", True, 1, "1")} | set(col)
    nsp = {g: len(v) for g, v in species.items()}
    for g, d in col.items():
        nsp[g] = max(nsp.get(g, 0), len(d["species"]))
    print(f"{len(living)} living genera; at most max(15, species) candidates per genus")
    files = commons(wk, names, nsp, living)
    w("commons.json", dict(downloaded=TODAY, files=files))
    if col:
        print("iNaturalist photographs of the living genera…")
        inat = L.inat_photos(fetch_json, sorted(living & set(names)), bases_l, cap=lambda g: cap_for(nsp.get(g, 0)))
        w("inat.json", dict(downloaded=TODAY, source=INAT_SOURCE, files=inat))
        files = dict(files, **inat)
    print("PhyloPic…")
    lineage = {r["taxon_name"]: [x for x in (r.get("family"), r.get("parent_name"), r.get("order")) if x and x != "NO_FAMILY_SPECIFIED"]
               for r in gen}
    for g, d in col.items():
        lineage.setdefault(g, [x for x in (d["family"], d["order"]) if x])
    w("phylopic.json", dict(downloaded=TODAY, silhouettes=phylopic(names, lineage)))
    if "--papers" in a:
        print("Scientific articles…")
        pp = papers(names)
        w("papers.json", dict(downloaded=TODAY, sources=["OpenAlex", "Europe PMC"], papers=pp))
        print(f"  {sum(len(v) for v in pp.values())} articles, {sum(1 for v in pp.values() if not v)} genera without any")
        print("Open-access figures…")
        oa = oa_figures(names)
        w("oa_figures.json", dict(downloaded=TODAY, figures=oa))
        if sheet_dir:
            oa_sheets(oa, sheet_dir / "oa")
    if sheet_dir:
        print("Contact sheets…")
        sheets(files, names, sheet_dir)
    print(f"done: {len(names)} genera, {len(rows)} occurrences, {len(files)} candidate pictures (Commons and iNaturalist)")


if __name__ == "__main__":
    main()
