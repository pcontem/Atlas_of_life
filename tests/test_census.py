"""Offline tests of scripts/fetch/census.py: the network functions are replaced by fakes whose answers have the shapes
PBDB, the MediaWiki API, Crossref and Europe PMC return. Run: python3 tests/test_census.py"""
import pathlib, sys, types
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/fetch"))
import census, harvest  # noqa: E402

# ---- small pure functions
assert census.year_of("Marsh 1876") == 1876 and census.year_of("(Smith and Jones, 2025)") == 2025 and census.year_of("") is None
assert census.title_to_name("Pteranodon") == "Pteranodon" and census.title_to_name("Caiman (genus)") == "Caiman"
assert census.title_to_name("List of pterosaurs") is None and census.title_to_name("Pteranodon longiceps") is None
assert census.title_to_name("Mercury (planet)") is None and census.title_to_name("Ab") is None
gen_page = "{{Automatic taxobox\n| taxon = Foosuchus\n| type_species = †''Foosuchus bar''\n| authority = Smith, 2025\n}}\n'''Foosuchus''' is a genus."
clade_page = "{{Automatic taxobox\n| taxon = Pseudosuchia\n| authority = Zittel, 1887\n}}\n'''Pseudosuchia''' is a clade of archosaurs."
lead_only = "{{Speciesbox\n| genus = Barsaurus\n}}\n'''''Barsaurus''''' was an extinct genus of reptiles."
assert census.wiki_is_genus(gen_page, "Foosuchus") and not census.wiki_is_genus(clade_page, "Pseudosuchia")
assert census.wiki_is_genus(lead_only, "Barsaurus")
family_page = "{{Automatic taxobox\n| taxon = Anurognathidae\n| type_genus = Anurognathus\n}}\n'''Anurognathidae''' is a family of pterosaurs that includes the genus Anurognathus."
family_nobox = "'''Fooidae''' is a family of reptiles, containing the genus Foosuchus."
clade_lead = "'''Zedia''' is a clade of archosaurs; its best known genus is Zedosaurus."
sub_genus = "'''Nipponopterus''' is an extinct genus of pterosaur from Japan."
assert not census.wiki_is_genus(family_page, "Anurognathidae") and not census.wiki_is_genus(family_nobox, "Fooidae")
tribe_box = "{{Automatic taxobox\n| taxon = Zedus\n| type_genus = Zedosaurus\n}}\n'''Zedus''' is an extinct genus of reptile."
assert not census.wiki_is_genus(tribe_box, "Zedus")      # a taxobox with type_genus is a higher taxon whatever the lead says
assert not census.wiki_is_genus(clade_lead, "Zedia") and census.wiki_is_genus(sub_genus, "Nipponopterus")
assert not census.wiki_is_genus(gen_page, "Mekosuchinae") and not census.wiki_is_genus(gen_page, "Crocodylomorpha")   # family-like names never pass
assert census.is_form_taxon(dict(flags="IF")) and census.is_form_taxon(dict(flags="I")) and census.is_form_taxon(dict(flags="F"))
assert not census.is_form_taxon(dict(flags="B")) and not census.is_form_taxon(dict()) and not census.is_form_taxon(dict(flags=None))
t = {
    "Foosuchus barensis gen. et sp. nov., a Late Triassic aetosaur from Brazil": ["Foosuchus"],
    "Quxosaurus zed, a new pterosaur from the Cretaceous of China": ["Quxosaurus"],
    "A new genus of azhdarchid from Morocco: Nixopteryx": ["Nixopteryx"],
    "Redescription of Pteranodon and its relatives": [],
    "A new genus of crocodylomorph from Cretaceous, Early Jurassic gen. nov.": [],
}
for title, want in t.items():
    assert census.genus_leads(title) == want, (title, census.genus_leads(title))

# ---- Wikipedia category crawl against a fake MediaWiki
CATS = {
    "Category:Root": [dict(ns=0, title="Alphasaurus"), dict(ns=14, title="Category:Child"), dict(ns=14, title="Category:Root stubs"),
                      dict(ns=14, title="Category:Fossils of Brazil")],
    "Category:Child": [dict(ns=0, title="Betasuchus"), dict(ns=0, title="Alphasaurus"), dict(ns=14, title="Category:Grandchild")],
    "Category:Grandchild": [dict(ns=0, title="Gammasaurus")],
    "Category:Empty": [],
    "Category:Root stubs": [dict(ns=0, title="Stubsaurus")],
    "Category:Fossils of Brazil": [dict(ns=0, title="Brazilosaurus")],
}
calls = []
queries = []


def fake_mw(api, **p):
    calls.append(p)
    if p.get("list") == "categorymembers":
        mem = CATS.get(p["cmtitle"], [])
        if p["cmtitle"] == "Category:Root" and "cmcontinue" not in p:  # paginate the root: first page, then the rest
            return dict(query=dict(categorymembers=mem[:1]), **{"continue": dict(cmcontinue="x", **{"continue": "-||"})})
        if p["cmtitle"] == "Category:Root":
            return dict(query=dict(categorymembers=mem[1:]))
        return dict(query=dict(categorymembers=mem))
    if p.get("prop") == "categories":
        assert p["clshow"] == "!hidden"
        return dict(query=dict(pages=[dict(title=p["titles"], categories=[dict(title="Category:Foo"), dict(title="Category:Bar")])]))
    if p.get("list") == "search":
        queries.append(p["srsearch"])
        assert p["srnamespace"] == 14
        if "genera" in p["srsearch"]:   # the full phrase finds nothing: the census must retry with the group word alone
            return dict(query=dict(search=[]))
        return dict(query=dict(search=[dict(title="Category:Real pseudosuchians"), dict(title="Category:Aetosaurs of Brazil")]))
    if p.get("prop") == "info":
        return dict(query=dict(pages=[dict(title=p["titles"], missing=True)] if "Nope" in p["titles"] else [dict(title=p["titles"])]))
    raise AssertionError(p)


real_mw = harvest.mw
harvest.mw = fake_mw
pages, missing, trunc, layout = census.wiki_category_pages(["Root", "Empty", "Nope"], depth=3)
harvest.mw = real_mw
assert set(pages) == {"Alphasaurus", "Betasuchus", "Gammasaurus"}, pages     # stubs and "Fossils of" skipped, sub-categories followed
assert missing == ["Category:Nope"] and not trunc, (missing, trunc)           # an empty category that exists is not "missing"
assert any(c.get("cmcontinue") == "x" for c in calls)                          # the continuation token was passed on
harvest.mw = fake_mw
_, _, trunc, _ = census.wiki_category_pages(["Root"], depth=3, cap=1)
harvest.mw = real_mw
assert trunc
# layout: what the roots hold, with the sub-categories that were followed and those skipped
assert layout["Category:Root"]["pages"] == 1 and layout["Category:Root"]["subcats"] == ["Category:Child"], layout["Category:Root"]
assert layout["Category:Root"]["skipped"] == ["Category:Root stubs", "Category:Fossils of Brazil"]
assert layout["Category:Child"]["pages"] == 2 and "Category:Grandchild" not in layout          # only two levels are recorded

harvest.mw = fake_mw
assert census.wiki_probe(["Tyrannosaurus"]) == {"Tyrannosaurus": ["Category:Foo", "Category:Bar"]}
sug = census.wiki_suggest_categories(["Category:Prehistoric pseudosuchians", "Category:Prehistoric pseudosuchian genera"])
harvest.mw = real_mw
assert queries == ["pseudosuchians", "pseudosuchian genera", "pseudosuchian"], queries   # "Prehistoric" never reaches the search; fallback = group word
assert sug == {"Category:Prehistoric pseudosuchians": ["Category:Real pseudosuchians", "Category:Aetosaurs of Brazil"],
               "Category:Prehistoric pseudosuchian genera": ["Category:Real pseudosuchians", "Category:Aetosaurs of Brazil"]}, sug

# ---- command line
assert census.parse_args(["pseudosuchia", "pterosauria", "--since", "2021"]) == (["pseudosuchia", "pterosauria"], 2021)
assert census.parse_args(["--since", "2020", "theropoda"]) == (["theropoda"], 2020)
assert census.parse_args(["theropoda"]) == (["theropoda"], census.DEFAULT_SINCE)

# ---- the census itself
atlas = dict(entries={"Alphasaurus": "demo", "Betasuchus": "demo", "Oldname": "demo", "Elsewhere": "other"},
             excluded={"Deadname": "nomen dubium"}, backbone={"Waitingosaurus"})
PBV = [dict(taxon_name=n, taxon_attr=a, firstapp_max_ma=1, lastapp_min_ma=0, parent_name="P", flags="IF" if n == "Trackus" else None)
       for n, a in [("Alphasaurus", "Smith 1900"), ("Betasuchus", "Jones 1950"), ("Newsuchus", "Doe 2025"), ("Oldsaurus", "Marsh 1880"), ("Aaasaurus", "Owen 1850"), ("Trackus", "Hitch 1836"),
                    ("Waitingosaurus", "Roe 1990"), ("Elsewhere", "X 2000"), ("Deadname", "Q 1900")]]
PBI = [dict(taxon_name="Oldname", difference="subjective synonym of Alphasaurus")]
WIKI = {"Foosuchus": gen_page, "Pseudosuchia": clade_page, "Alphasaurus": "x"}


def fake_net():
    n = types.SimpleNamespace()
    n.pbdb = lambda base, status: {"valid": PBV, "invalid": PBI}[status]
    n.wiki_pages = lambda roots, depth=3, cap=8000: ({"Foosuchus": "Category:A", "Pseudosuchia": "Category:A", "Alphasaurus": "Category:A",
                                                        "List of things": "Category:A", "Waitingosaurus": "Category:A"}, ["Category:Gone"], False,
                                                       {"Category:A": dict(pages=5, subcats=["Category:B"], skipped=[])})
    n.wiki_texts = lambda titles: {t: dict(wikitext=WIKI[t], ts="2026-01-01T00:00:00Z") for t in titles if t in WIKI}
    n.wiki_probe = lambda titles: {t: ["Category:Probed"] for t in titles}
    n.wiki_suggest = lambda cats: {k: ["Category:Real"] for k in cats}
    n.wiki_redirects = lambda names: {g: dict(missing=False, redirect="Alphasaurus") for g in names}
    n.literature = lambda terms, since: [
        dict(title="Zedosuchus alpha gen. et sp. nov., a new crocodylomorph", doi="10.1/z", year=2025, journal="J Test", via="crossref", term="x"),
        dict(title="Newsuchus doe gen. nov. from Brazil", doi="10.1/n", year=2025, journal="J Test", via="crossref", term="x"),
        dict(title="Redescription of Alphasaurus", doi="10.1/a", year=2024, journal="J Test", via="crossref", term="x")]
    return n


cfg = dict(pbdb="Demo", wikipedia=dict(categories=["A"], probe=["Tyrannosaurus"]), literature=["demo"])
c = census.run_census("demo", cfg, 2023, atlas, fake_net())
miss = {m["name"]: m for m in c["missing"]}
assert set(miss) == {"Newsuchus", "Oldsaurus", "Foosuchus", "Aaasaurus"}, set(miss)       # known = entries, excluded, backbone; Deadname/Elsewhere/Waiting are known
assert miss["Newsuchus"]["recent"] and miss["Foosuchus"]["recent"] and not miss["Oldsaurus"]["recent"]
assert miss["Foosuchus"]["in_wikipedia"] and not miss["Foosuchus"]["in_pbdb"] and miss["Foosuchus"]["year"] == 2025
assert [m["name"] for m in c["missing"]] == ["Foosuchus", "Newsuchus", "Oldsaurus", "Aaasaurus"]   # recent first (A-Z), then old ones newest first
assert "Trackus" not in miss and [f["name"] for f in c["form_taxa"]] == ["Trackus"] and c["counts"]["form_taxa"] == 1   # ichnotaxa are apart
assert c["wikipedia_category_suggestions"] == {"Category:Gone": ["Category:Real"]}
assert "Pseudosuchia" not in miss                                              # a clade article is not a genus
assert c["waiting_in_backbone"] == ["Waitingosaurus"]
un = {a["name"]: a for a in c["atlas_unconfirmed"]}
assert set(un) == {"Oldname"}, un                                              # Alphasaurus and Betasuchus are confirmed by PBDB
assert un["Oldname"]["pbdb"].startswith("subjective synonym") and un["Oldname"]["wikipedia"] == "redirects to Alphasaurus"
assert c["atlas_pbdb_invalid"] == ["Oldname"]
leads = {x["name"]: x for x in c["literature_leads"]}
assert set(leads) == {"Zedosuchus", "Newsuchus"} and not leads["Zedosuchus"]["known"] and leads["Newsuchus"]["in_pbdb"]
assert c["literature_leads"][0]["name"] == "Zedosuchus"                        # leads absent from PBDB come first
assert c["wikipedia_missing_categories"] == ["Category:Gone"] and c["counts"]["missing_recent"] == 2
md = census.report(c)
assert c["wikipedia_probe"] == {"Tyrannosaurus": ["Category:Probed"]} and "Tyrannosaurus: Category:Probed" in md
assert "existing categories with these words: Category:Real" in md and "Trackus" in md and "form taxa" in md
assert "Foosuchus" in md and "Zedosuchus" in md and "Category:Gone" in md and "Oldname" in md and "10.1/z" in md

empty = fake_net()
empty.wiki_pages = lambda roots, depth=3, cap=8000: ({}, [], False, {"Category:Only subcats": dict(pages=0, subcats=[], skipped=["Category:X by country"])})
ce = census.run_census("demo", cfg, 2023, atlas, empty)
assert "found no pages" in census.report(ce) and "Category:X by country" in census.report(ce) and ce["wikipedia_layout"]
assert "found no pages" not in md                                  # a crawl that found pages does not print the layout

# a group with nothing configured still runs (a clade that may become a volume)
c2 = census.run_census("future", dict(pbdb="Demo"), 2023, atlas, fake_net())
assert c2["counts"]["wikipedia_pages"] == 0 and c2["atlas_unconfirmed"] == [] and c2["literature_leads"] == []
assert {m["name"] for m in c2["missing"]} == {"Newsuchus", "Oldsaurus", "Aaasaurus"}   # PBDB alone still works (form taxa apart)

# the real configuration parses and names real folders
import yaml
src = yaml.safe_load((ROOT / "data/census/sources.yaml").read_text())
assert {"pterosauria", "pseudosuchia"} <= set(src) and all("pbdb" in v for v in src.values())
a = census.load_atlas()
assert len(a["entries"]) > 600 and "Pteranodon" in a["entries"] and len(a["backbone"]) > 1000
print("census tests: all passed")
