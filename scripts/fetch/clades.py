"""Raw material for clade entries: English Wikipedia (fixed revision, text, citations) and the PBDB record of each
clade, plus the PBDB children of the clade (to see which taxa it contains).

    python3 scripts/fetch/clades.py <out.json> "Wikipedia title[=PBDB name]" ...

Runs in GitHub Actions (.github/workflows/clades.yml): the maintainer's shell cannot reach these sites. Writes the
same layout as data/raw/tree/clade_sources_*.json (`wikipedia`, `pbdb`, `refs`) so the clade entries are written from
it exactly as in CLAUDE.md §4.2/§4.2b. Nothing here edits an entry.
"""
import datetime, json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/fetch"))
from harvest import mw, WIKI, cites  # noqa: E402
from pbdb import get as pbdb_get  # noqa: E402


def wikipedia(title):
    r = mw(WIKI, action="query", redirects=1, prop="revisions", rvprop="ids|timestamp|content", rvslots="main", titles=title)
    q = r.get("query", {})
    p = (q.get("pages") or [{}])[0]
    if p.get("missing") or "revisions" not in p:
        return {"missing": True}
    rv = p["revisions"][0]
    wt = rv["slots"]["main"]["content"]
    e = mw(WIKI, action="query", prop="extracts", explaintext=1, exsectionformat="wiki", titles=p["title"])
    text = ((e.get("query", {}).get("pages") or [{}])[0]).get("extract", "")
    return dict(title=p["title"], redirected_from=(title if p["title"] != title else None), revid=rv["revid"],
                ts=rv["timestamp"], text=text, cites=cites(wt),
                cladograms=re.findall(r"\{\{\s*[Cc]lade[\s\S]{0,3500}", wt)[:2])


def pbdb(name):
    out = {}
    try:
        rec = pbdb_get("taxa/single.json", name=name, show="attr,parent,class,refattr", vocab="pbdb")
        out["record"] = rec[0] if isinstance(rec, list) and rec else rec
        kids = pbdb_get("taxa/list.json", name=name, rel="children", show="attr", vocab="pbdb")
        out["children"] = [dict(name=k.get("taxon_name"), rank=k.get("taxon_rank"), status=k.get("taxon_attr")) for k in kids]
    except SystemExit as e:  # name unknown to PBDB
        out["error"] = str(e)[:200]
    return out


def main():
    out, items = sys.argv[1], sys.argv[2:]
    res = dict(downloaded=datetime.date.today().isoformat(), wikipedia={}, pbdb={})
    for it in items:
        wt, _, pn = it.partition("=")
        res["wikipedia"][wt] = wikipedia(wt)
        res["pbdb"][pn or wt] = pbdb(pn or wt)
        w = res["wikipedia"][wt]
        print(wt, "->", w.get("title"), w.get("revid"), "| PBDB", "ok" if "record" in res["pbdb"][pn or wt] else "none", flush=True)
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
