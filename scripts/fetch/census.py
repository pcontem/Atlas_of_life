"""Census of a group's genera: which genera exist in PBDB, English Wikipedia and recent literature that the atlas lacks.

    python3 scripts/fetch/census.py <group> [<group> ...] [--since YEAR]

<group> is a key of data/census/sources.yaml (a volume folder such as `pseudosuchia`, or a clade that may become a
volume). Runs in GitHub Actions (.github/workflows/census.yml): the maintainers' sessions cannot reach these sites.

Three sources, one question each:
  PBDB         every valid genus of the base taxon (and the invalid names, to spot synonyms)
  Wikipedia    pages of the group's genus categories (sub-categories followed) that look like genus articles
  Literature   Crossref and Europe PMC papers since YEAR whose titles announce a new genus ("gen. et sp. nov.", "a new genus")

Writes data/raw/census/<group>/census_<date>.json and .md (and appends the .md to $GITHUB_STEP_SUMMARY).
Nothing in entries/ is changed: the census is a to-do list for people (and for the next harvest), never an edit.

A genus counts as *known* when it has an entry in any volume, is in an excluded.yaml, or waits in data/tree/backbone.json.
"""
import datetime, json, os, pathlib, re, sys, types
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/fetch"))
import harvest  # noqa: E402  (fetch helpers: mw, fetch_json, taxobox, pbdb_get)

TODAY = datetime.date.today().isoformat()
THIS_YEAR = datetime.date.today().year
DEFAULT_SINCE = THIS_YEAR - 3
# sub-categories that only repeat the same genera by place, date or author, or are not about taxa
SKIP_CAT = re.compile(r"stub|^lists? of|template|navigational|redirect|wikiproject|images? of|fossils? of|fossil record|"
                      r"by (country|location|continent|region|author)|extinct animals of|taxa named by|taxa described in|"
                      r"\bin (art|popular culture|fiction)|^\d{3,4}\b", re.I)
NOT_GENERA = {"Early", "Late", "Middle", "Upper", "Lower", "Cretaceous", "Jurassic", "Triassic", "Permian", "Eocene",
              "Miocene", "Oligocene", "Paleocene", "Pliocene", "Neogene", "Paleogene", "Mesozoic", "Cenozoic", "China",
              "Brazil", "Argentina", "Africa", "Europe", "Asia", "Morocco", "Mongolia", "Australia", "Gondwana"}


# ---------------------------------------------------------------- names
def is_form_taxon(rec):
    """PBDB flags: I = ichnotaxon (tracks, burrows), F = form taxon (eggs, isolated teeth…): not body-fossil genera."""
    return any(ch in (rec.get("flags") or "") for ch in "IF")


def year_of(text):
    m = re.search(r"\b(1[6-9]\d\d|20\d\d)\b", text or "")
    return int(m.group(1)) if m else None


def title_to_name(title):
    """A page title that can be a genus name: one capitalised word, optionally with a '(genus)'-style tag."""
    m = re.fullmatch(r"([A-Z][a-z]{2,})(?: \(([^)]*)\))?", title or "")
    if not m or (m.group(2) and not re.search(r"genus|extinct|fossil|reptile|dinosaur|pterosaur|crocodyl|archosaur", m.group(2))):
        return None
    return m.group(1)


HIGHER_SUFFIX = re.compile(r"(idae|inae|oidea|oidae|ineae|iformes|morpha)$")   # families, subfamilies, superfamilies, orders, clades
HIGHER_WORDS = re.compile(r"\b(family|subfamily|superfamily|clade|order|suborder|infraorder|tribe|group|grade)\b")


def wiki_is_genus(wikitext, name):
    """An article about a genus: its taxobox names a type species, or the lead sentence says "is a … genus".
    Family and clade articles (type_genus in the taxobox, a higher-taxon word in the lead, a family-like name) are not."""
    if HIGHER_SUFFIX.search(name):
        return False
    tb = harvest.taxobox(wikitext)
    if tb.get("type_species"):
        return True
    if "type_genus" in wikitext[:3000] and "type_species" not in wikitext[:3000]:
        return False
    m = re.search(r"'''+\s*(?:\[\[)?" + re.escape(name) + r"[^.]{0,80}?\b(?:is|was|are|were) (?:a|an|the) ([^.]{0,100}?)\bgenus\b", wikitext[:4000])
    return bool(m) and not HIGHER_WORDS.search(m.group(1))


LEADS = [  # a new genus announced in a title: "Foo bar gen. et sp. nov.", "Foo bar, a new …", "a new genus … : Foo"
    re.compile(r"\b([A-Z][a-z]{3,})\s+[a-z]{3,},?\s*(?:gen\.?\s*(?:et|&|and)\s*sp\.?\s*nov\.?|gen\.?\s*nov\.?|n\.\s*gen\.)"),
    re.compile(r"^([A-Z][a-z]{3,})\s+[a-z]{3,},?\s+(?:a|an)\s+new\b"),
    re.compile(r"\bnew\s+genus\b[^:;,]{0,80}[:;,]\s*(?:the\s+)?([A-Z][a-z]{3,})\b"),
]


def genus_leads(title):
    out = []
    for rx in LEADS:
        for m in rx.finditer(title or ""):
            if m.group(1) not in NOT_GENERA and m.group(1) not in out:
                out.append(m.group(1))
    return out


# ---------------------------------------------------------------- network (replaced by fakes in tests)
def pbdb_taxa(base, status):
    return harvest.pbdb_get("taxa/list.json", base_name=base, rank="genus", taxon_status=status,
                            show="attr,app,parent,class", vocab="pbdb")


def wiki_category_pages(roots, depth=3, cap=8000):
    """-> (pages {title: category it was found in}, roots that do not exist, truncated?, layout). Sub-categories are followed.
    layout[category] = {"pages": n, "subcats": [followed], "skipped": [not followed]} for the roots and their sub-categories
    one level down, so an empty result can be diagnosed from the report."""
    pages, missing, queue, seen, layout = {}, [], [(r, 0) for r in roots], set(), {}
    while queue:
        cat, d = queue.pop(0)
        if cat in seen:
            continue
        seen.add(cat)
        title = cat if cat.startswith("Category:") else "Category:" + cat
        n_here, cont, followed, skipped, n_pages = 0, {}, [], [], 0
        while True:
            r = harvest.mw(harvest.WIKI, action="query", list="categorymembers", cmtitle=title, cmlimit=500,
                           cmtype="page|subcat", **cont)
            for m in r.get("query", {}).get("categorymembers", []):
                n_here += 1
                if m["ns"] == 14:
                    sub = m["title"]
                    if d < depth and not SKIP_CAT.search(sub[len("Category:"):]):
                        queue.append((sub, d + 1))
                        followed.append(sub)
                    else:
                        skipped.append(sub)
                elif m["ns"] == 0:
                    n_pages += 1
                    pages.setdefault(m["title"], title)
            if "continue" not in r or len(pages) >= cap:
                break
            cont = r["continue"]
        if d <= 1:
            layout[title] = dict(pages=n_pages, subcats=followed[:40], skipped=skipped[:40])
        if n_here == 0 and d == 0:  # empty root: does the category exist at all?
            q = harvest.mw(harvest.WIKI, action="query", titles=title, prop="info").get("query", {})
            if any(p.get("missing") for p in q.get("pages", [])):
                missing.append(title)
        if len(pages) >= cap:
            return pages, missing, True, layout
    return pages, missing, False, layout


def wiki_suggest_categories(missing_cats, limit=8):
    """-> {missing category title: [existing category titles found by searching its words]} (to fix sources.yaml)."""
    out = {}
    for t in missing_cats:
        words = re.sub(r"^Category:(?:Prehistoric )?", "", t)
        group_word = next((w for w in words.split() if w.lower() not in ("genera", "genus")), words)
        for q in dict.fromkeys((words, group_word)):  # the full phrase first, then the group word alone
            r = harvest.mw(harvest.WIKI, action="query", list="search", srsearch=q, srnamespace=14, srlimit=limit)
            out[t] = [x["title"] for x in r.get("query", {}).get("search", [])]
            if out[t]:
                break
    return out


def wiki_probe(titles):
    """-> {page title: [its visible categories]}: shows how Wikipedia files a group (for choosing `categories` in sources.yaml)."""
    out = {}
    for t in titles:
        r = harvest.mw(harvest.WIKI, action="query", prop="categories", titles=t, cllimit=500, clshow="!hidden", redirects=1)
        for p in r.get("query", {}).get("pages", []):
            out[t] = [c["title"] for c in p.get("categories", [])]
    return out


def wiki_texts(titles):
    """-> {title: {"wikitext", "ts"}} (latest revision; titles without a page are left out)."""
    out = {}
    for i in range(0, len(titles), 40):
        r = harvest.mw(harvest.WIKI, action="query", prop="revisions", rvprop="timestamp|content", rvslots="main",
                       titles="|".join(titles[i:i + 40]))
        for p in r.get("query", {}).get("pages", []):
            if p.get("missing") or "revisions" not in p:
                continue
            rv = p["revisions"][0]
            out[p["title"]] = dict(wikitext=rv["slots"]["main"]["content"], ts=rv["timestamp"])
    return out


def wiki_redirects(names):
    """-> {name: {"missing": bool, "redirect": target or None}} for names looked up as article titles."""
    out = {}
    for i in range(0, len(names), 40):
        chunk = names[i:i + 40]
        q = harvest.mw(harvest.WIKI, action="query", redirects=1, titles="|".join(chunk)).get("query", {})
        norm = {n["from"]: n["to"] for n in q.get("normalized", [])}
        red = {n["from"]: n["to"] for n in q.get("redirects", [])}
        pages = {p["title"]: p for p in q.get("pages", [])}
        for g in chunk:
            t = norm.get(g, g)
            tgt = red.get(t)
            p = pages.get(tgt or t, {})
            out[g] = dict(missing=bool(p.get("missing")), redirect=tgt)
    return out


def literature(terms, since):
    """Papers since `since` whose titles announce a new genus; Crossref and Europe PMC, one query per term."""
    papers = {}
    for term in terms:
        r = harvest.fetch_json("https://api.crossref.org/works", {
            "query.bibliographic": f"{term} new genus", "filter": f"from-pub-date:{since}-01-01,type:journal-article",
            "rows": 100, "select": "DOI,title,issued,container-title", "sort": "published", "order": "desc"})
        for it in ((r or {}).get("message", {}).get("items") or []):
            title = (it.get("title") or [""])[0]
            yr = ((it.get("issued") or {}).get("date-parts") or [[None]])[0][0]
            papers.setdefault(it.get("DOI", title).lower(), dict(title=title, doi=it.get("DOI"), year=yr,
                              journal=(it.get("container-title") or [""])[0], via="crossref", term=term))
        r = harvest.fetch_json("https://www.ebi.ac.uk/europepmc/webservices/rest/search", {
            "query": f'("{term}") AND ("gen. nov" OR "new genus" OR "gen. et sp. nov") AND '
                     f"FIRST_PDATE:[{since}-01-01 TO {THIS_YEAR}-12-31]",
            "format": "json", "pageSize": 100, "resultType": "lite"})
        for it in ((r or {}).get("resultList", {}).get("result") or []):
            key = (it.get("doi") or it.get("title", "")).lower()
            papers.setdefault(key, dict(title=it.get("title", "").rstrip("."), doi=it.get("doi"),
                              year=int(it["pubYear"]) if str(it.get("pubYear", "")).isdigit() else None,
                              journal=it.get("journalTitle", ""), via="europepmc", term=term))
    return list(papers.values())


NET = types.SimpleNamespace(pbdb=pbdb_taxa, wiki_pages=wiki_category_pages, wiki_texts=wiki_texts, wiki_suggest=wiki_suggest_categories, wiki_probe=wiki_probe,
                            wiki_redirects=wiki_redirects, literature=literature)


# ---------------------------------------------------------------- the atlas
def load_atlas():
    entries = {p.stem: p.parent.parent.name for p in (ROOT / "entries").glob("*/genera/*.yaml")}
    excluded = {}
    for p in (ROOT / "entries").glob("*/excluded.yaml"):
        for x in yaml.safe_load(p.read_text()) or []:
            excluded[x["name"]] = x.get("status", "")
    backbone = {n[1] for n in json.loads((ROOT / "data/tree/backbone.json").read_text()) if n[5] == "g"}
    return dict(entries=entries, excluded=excluded, backbone=backbone)


# ---------------------------------------------------------------- the census
def run_census(group, cfg, since, atlas, net=NET):
    pbv = {r["taxon_name"]: r for r in net.pbdb(cfg["pbdb"], "valid")}
    pbi = {r["taxon_name"]: r for r in net.pbdb(cfg["pbdb"], "invalid")}
    known = set(atlas["entries"]) | set(atlas["excluded"]) | atlas["backbone"]
    mine = {g for g, v in atlas["entries"].items() if v == group}  # entries of this volume (empty for a future volume)

    # Wikipedia: pages of the genus categories that are, or look like, genus articles
    w = cfg.get("wikipedia") or {}
    pages, missing_cats, truncated, layout = (net.wiki_pages(w.get("categories", []), w.get("depth", 3)) if w.get("categories")
                                              else ({}, [], False, {}))
    cand = {}  # genus name -> page title
    for t in pages:
        n = title_to_name(t)
        if n:
            cand.setdefault(n, t)
    to_read = sorted(t for n, t in cand.items() if n not in known and n not in pbv)  # PBDB-valid ones need no check
    texts = net.wiki_texts(to_read) if to_read else {}
    wiki_genera = {}  # genus -> {"title", "year"} for pages in categories that are genus articles
    for n, t in cand.items():
        if n in known or n in pbv:  # in the atlas, or PBDB already vouches that it is a genus
            wiki_genera[n] = dict(title=t, year=None)
        elif t in texts and wiki_is_genus(texts[t]["wikitext"], n):
            tb = harvest.taxobox(texts[t]["wikitext"])
            wiki_genera[n] = dict(title=t, year=year_of(tb.get("authority")))

    suggestions = net.wiki_suggest(missing_cats) if missing_cats else {}
    probe = net.wiki_probe(w.get("probe", [])) if w.get("probe") else {}

    # genera missing from the atlas, newest first
    missing, form_taxa = [], []
    for n in sorted((set(pbv) | set(wiki_genera)) - known):
        r = pbv.get(n, {})
        if is_form_taxon(r):
            form_taxa.append(dict(name=n, authority=r.get("taxon_attr", ""), flags=r.get("flags"), family=r.get("family")))
            continue
        yr = year_of(r.get("taxon_attr")) or (wiki_genera.get(n) or {}).get("year")
        missing.append(dict(name=n, authority=r.get("taxon_attr", ""), year=yr, recent=bool(yr and yr >= since),
                            in_pbdb=n in pbv, in_wikipedia=n in wiki_genera,
                            wikipedia=(wiki_genera.get(n) or {}).get("title"),
                            first_ma=r.get("firstapp_max_ma"), last_ma=r.get("lastapp_min_ma"),
                            parent=r.get("parent_name"), family=r.get("family"),
                            pbdb_invalid=(pbi[n].get("difference") or "invalid") if n in pbi else None))
    missing.sort(key=lambda m: (not m["recent"], -(m["year"] or 0), m["name"]))

    # waiting in the backbone and confirmed by a source: the unwritten part of the list that is already known
    waiting = sorted(n for n in atlas["backbone"] if n in pbv or n in wiki_genera)

    # entries of this volume that no source confirms (misspelling? synonym? sunk?), with what Wikipedia says
    unconfirmed = sorted(g for g in mine if g not in pbv and g not in wiki_genera)
    red = net.wiki_redirects(unconfirmed) if unconfirmed else {}
    atlas_unconfirmed = [dict(name=g, pbdb=(pbi[g].get("difference") or "invalid") if g in pbi else None,
                              wikipedia=("no article" if red.get(g, {}).get("missing") else
                                         f"redirects to {red[g]['redirect']}" if red.get(g, {}).get("redirect") else "has an article"))
                         for g in unconfirmed]
    atlas_invalid = sorted(g for g in mine if g in pbi and g in pbv) + sorted(g for g in mine if g in pbi and g not in pbv)

    # literature leads: genus names announced in titles since `since` that the atlas, PBDB and Wikipedia do not have
    leads = []
    for p in net.literature(cfg.get("literature", []), since) if cfg.get("literature") else []:
        for n in genus_leads(p["title"]):
            leads.append(dict(name=n, known=n in known, in_pbdb=n in pbv, in_wikipedia=n in wiki_genera, **p))
    leads.sort(key=lambda x: (x["known"], x["in_pbdb"], -(x.get("year") or 0), x["name"]))
    return dict(group=group, date=TODAY, since=since, config=cfg,
                counts=dict(pbdb_valid=len(pbv), pbdb_invalid=len(pbi), wikipedia_pages=len(pages), wikipedia_genera=len(wiki_genera),
                            atlas_entries_in_group=len(mine), missing=len(missing), form_taxa=len(form_taxa), missing_recent=sum(m["recent"] for m in missing),
                            waiting_in_backbone=len(waiting), atlas_unconfirmed=len(atlas_unconfirmed), leads=len(leads),
                            leads_new=sum(not x["known"] and not x["in_pbdb"] for x in leads)),
                missing=missing, form_taxa=form_taxa, waiting_in_backbone=waiting, atlas_unconfirmed=atlas_unconfirmed, atlas_pbdb_invalid=atlas_invalid,
                literature_leads=leads, wikipedia_missing_categories=missing_cats, wikipedia_category_suggestions=suggestions, wikipedia_layout=layout, wikipedia_probe=probe,
                wikipedia_truncated=truncated)


def report(c):
    n = c["counts"]
    L = [f"## Census: {c['group']} ({c['date']}, new = since {c['since']})", "",
         f"PBDB lists **{n['pbdb_valid']}** valid genera ({n['pbdb_invalid']} invalid names); Wikipedia pages read: {n['wikipedia_pages']}, "
         f"genus articles found: {n['wikipedia_genera']}. The atlas has {n['atlas_entries_in_group']} entries in this group.", "",
         f"- **{n['missing']}** genera are missing from the atlas ({n['missing_recent']} named since {c['since']}); "
         f"**{n['waiting_in_backbone']}** more are known and waiting in the backbone.",
         f"- {n['form_taxa']} PBDB names are form taxa (ichnogenera, oogenera…, PBDB flags I/F) and are listed apart, not as missing.",
         f"- {n['atlas_unconfirmed']} entries of this group are confirmed by neither PBDB nor Wikipedia; {n['leads']} literature leads "
         f"({n['leads_new']} not yet in PBDB or the atlas).", ""]
    if c["wikipedia_missing_categories"]:
        L += ["**Wikipedia categories not found (fix `data/census/sources.yaml`):**", ""]
        for cat in c["wikipedia_missing_categories"]:
            sug = c.get("wikipedia_category_suggestions", {}).get(cat) or []
            L.append(f"- {cat}" + (" — existing categories with these words: " + "; ".join(sug) if sug else ""))
        L.append("")
    if c.get("wikipedia_layout") and not c["counts"]["wikipedia_pages"]:
        L += ["**The Wikipedia crawl found no pages.** What the categories hold:", ""]
        for cat, v in c["wikipedia_layout"].items():
            L.append(f"- {cat}: {v['pages']} pages; sub-categories followed: {', '.join(v['subcats']) or 'none'}; "
                     f"skipped: {', '.join(v['skipped']) or 'none'}")
        L.append("")
    if c.get("wikipedia_probe"):
        L += ["**Categories of example pages (how Wikipedia files this group):**", ""]
        L += [f"- {t}: " + "; ".join(cats) for t, cats in c["wikipedia_probe"].items()]
        L.append("")
    if c["wikipedia_truncated"]:
        L += ["**The Wikipedia crawl hit its page cap**: narrow the categories or the depth.", ""]
    if c["missing"]:
        L += ["### Missing from the atlas", "", "| Genus | Authority | Age (Ma) | PBDB | Wikipedia | Note |", "|---|---|---|---|---|---|"]
        for m in c["missing"][:400]:
            age = f"{m['first_ma']}–{m['last_ma']}" if m["first_ma"] not in (None, "") else ""
            note = ("**new** " if m["recent"] else "") + (f"PBDB: {m['pbdb_invalid']}" if m["pbdb_invalid"] else "")
            L.append(f"| *{m['name']}* | {m['authority'] or m['year'] or ''} | {age} | {'yes' if m['in_pbdb'] else ''} | "
                     f"{'yes' if m['in_wikipedia'] else ''} | {note} |")
        if len(c["missing"]) > 400:
            L.append(f"\n… and {len(c['missing']) - 400} more in the JSON file.")
        L.append("")
    if c.get("form_taxa"):
        L += ["### Form taxa not counted as missing (ichnogenera, oogenera…)", "",
              ", ".join(f"*{f['name']}*" for f in c["form_taxa"]), ""]
    if c["atlas_unconfirmed"]:
        L += ["### Atlas entries that no source confirms", ""]
        L += [f"- *{a['name']}*: Wikipedia {a['wikipedia']}" + (f"; PBDB: {a['pbdb']}" if a["pbdb"] else "") for a in c["atlas_unconfirmed"]]
        L.append("")
    if c["atlas_pbdb_invalid"]:
        L += ["### Atlas entries that PBDB also lists as invalid names", "", ", ".join(f"*{g}*" for g in c["atlas_pbdb_invalid"]), ""]
    new = [x for x in c["literature_leads"] if not x["known"]]
    if new:
        L += ["### Literature leads (check each; titles are matched by pattern)", ""]
        L += [f"- *{x['name']}* — {x['title']} ({x.get('journal') or ''}, {x.get('year') or ''})"
              + (f" https://doi.org/{x['doi']}" if x.get("doi") else "") + (" · in PBDB" if x["in_pbdb"] else "") for x in new[:80]]
        L.append("")
    return "\n".join(L)


def parse_args(a):
    since = int(a[a.index("--since") + 1]) if "--since" in a else DEFAULT_SINCE
    groups = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] != "--since")]
    return groups, since


def main():
    groups, since = parse_args(sys.argv[1:])
    sources = yaml.safe_load((ROOT / "data/census/sources.yaml").read_text())
    atlas = load_atlas()
    parts = []
    for g in groups:
        if g not in sources:
            raise SystemExit(f"{g}: not in data/census/sources.yaml")
        print(f"census {g}…", flush=True)
        c = run_census(g, sources[g], since, atlas)
        out = ROOT / "data/raw/census" / g
        out.mkdir(parents=True, exist_ok=True)
        (out / f"census_{TODAY}.json").write_text(json.dumps(c, ensure_ascii=False, indent=1))
        md = report(c)
        (out / f"census_{TODAY}.md").write_text(md + "\n")
        print(md.split("\n\n")[1] if "\n\n" in md else md, flush=True)
        parts.append(md)
    text = "\n\n".join(parts) + "\n"
    pathlib.Path("/tmp/census_report.md").write_text(text)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(text)


if __name__ == "__main__":
    main()
