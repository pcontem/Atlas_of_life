"""Living genera for the harvest (owner, 2026-11-28): names from the Catalogue of Life, photographs from iNaturalist.

PBDB only knows living genera that have a fossil record, so the harvest adds the accepted, non-extinct genera that
the Catalogue of Life (latest release, ChecklistBank dataset 3LR) lists under the volume's living base taxa, with
their authority, family and accepted living species. Photographs of living animals come from Wikimedia Commons
(harvest.commons) and from iNaturalist: the genus's taxon photos and the default photo of each species, kept only
when the photo itself is CC0, CC BY or CC BY-SA (iNaturalist applies version 4.0 of the Creative Commons
licences). iNaturalist candidates are written in the same record layout as commons.json, so contact sheets,
scripts/draft_genera.py and the triage page treat them like Commons files; their `page` is the iNaturalist photo page.

Used by scripts/fetch/harvest.py (--living <COL taxa>); needs web access (GitHub Actions).
"""
import re
import time

COL = "https://api.checklistbank.org/dataset/3LR"
INAT = "https://api.inaturalist.org/v1"
INAT_OK = {"cc0": ("CC0", "https://creativecommons.org/publicdomain/zero/1.0/"),
           "cc-by": ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/"),
           "cc-by-sa": ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/")}


def _usage(item):
    """A ChecklistBank search result -> (id, scientific name, authorship, rank, extinct, classification)."""
    u = item.get("usage") or item
    nm = u.get("name") or {}
    return (u.get("id") or item.get("id"), nm.get("scientificName") or u.get("label", ""), nm.get("authorship", ""),
            (nm.get("rank") or "").lower(), bool(u.get("extinct")), item.get("classification") or [])


def col_search(get, **params):
    """All results of a ChecklistBank name-usage search (paged by 1000)."""
    out, off = [], 0
    while True:
        r = get(f"{COL}/nameusage/search", dict(params, limit=1000, offset=off)) or {}
        res = r.get("result") or []
        out += res
        off += len(res)
        if not res or r.get("last") or off >= (r.get("total") or 0) or off >= 100000:
            return out
        time.sleep(0.2)


def col_taxon(get, name):
    """COL id of an accepted taxon given by its scientific name (exact match), or None."""
    for item in col_search(get, q=name, content="SCIENTIFIC_NAME", type="EXACT", status="accepted"):
        i, sci, _, rank, _, _ = _usage(item)
        if sci == name:
            return i
    return None


def col_genera(get, bases, skip=()):
    """Accepted, non-extinct genera under the COL taxa `bases` -> {genus: {col_id, url, authority, family, order,
    species: [{name, authority}]}}. Genera COL marks extinct, and names in `skip`, are left out."""
    out = {}
    for base in bases:
        tid = col_taxon(get, base)
        if not tid:
            print(f"  ! COL: no accepted taxon named {base}")
            continue
        res = col_search(get, TAXON_ID=tid, rank="genus", status="accepted", extinct="false")
        print(f"  COL {base} ({tid}): {len(res)} living genera")
        for item in res:
            i, sci, auth, rank, extinct, cl = _usage(item)
            if rank != "genus" or extinct or sci in skip or not re.fullmatch(r"[A-Z][a-z]+", sci or ""):
                continue
            ranks = {(c.get("rank") or "").lower(): c.get("name") for c in cl}
            out[sci] = dict(col_id=i, url=f"https://www.catalogueoflife.org/data/taxon/{i}", authority=auth,
                            family=ranks.get("family", ""), order=ranks.get("order", ""), species=[])
    for k, (g, d) in enumerate(sorted(out.items())):
        if k % 100 == 0:
            print(f"  COL species {k}/{len(out)}", flush=True)
        for item in col_search(get, TAXON_ID=d["col_id"], rank="species", status="accepted", extinct="false"):
            _, sci, auth, rank, extinct, _ = _usage(item)
            if rank == "species" and not extinct and sci.startswith(g + " "):
                d["species"].append(dict(name=sci, authority=auth))
        time.sleep(0.2)
    return out


def _photo(p, genus, taxon, found):
    """iNaturalist photo -> commons.json-style record, or None when its licence is not allowed (§4.4 I3)."""
    lic = INAT_OK.get((p.get("license_code") or "").lower())
    if not lic or not p.get("id"):
        return None
    sq = p.get("url") or p.get("square_url") or ""
    big = p.get("large_url") or sq.replace("/square.", "/large.")
    mid = p.get("medium_url") or sq.replace("/square.", "/medium.")
    dims = p.get("original_dimensions") or {}
    w, h = dims.get("width") or 0, dims.get("height") or 0
    if w and h and max(w, h) > 1024:  # the "large" size is at most 1024 px on its longer side
        s = 1024 / max(w, h)
        w, h = round(w * s), round(h * s)
    artist = re.sub(r"^\(c\)\s*", "", p.get("attribution") or "").split(",")[0].strip() or "Unknown (no name on iNaturalist)"
    return dict(genera=[genus], found=[found], url=big, page=f"https://www.inaturalist.org/photos/{p['id']}", thumb=mid,
                width=w, height=h, mime="image/jpeg", source="iNaturalist", Artist=artist, LicenseShortName=lic[0],
                LicenseUrl=lic[1], ImageDescription=f"Photograph of {taxon} on iNaturalist ({p.get('attribution', '')})"[:500])


def inat_photos(get, names, bases, cap=lambda n: 15):
    """Candidate photographs of living genera from iNaturalist -> {"File:iNaturalist photo <id>": record}.
    Genera are looked up inside the iNaturalist taxa named `bases` (avoids homonyms in other kingdoms)."""
    anc = []
    for b in bases:
        r = get(f"{INAT}/taxa", dict(q=b, is_active="true", per_page=10)) or {}
        anc += [t["id"] for t in r.get("results", []) if t.get("name") == b]
        time.sleep(1)
    files = {}
    for k, g in enumerate(sorted(names)):
        if k % 50 == 0:
            print(f"  iNaturalist {k}/{len(names)}", flush=True)
        r = get(f"{INAT}/taxa", dict(q=g, rank="genus", is_active="true", per_page=10,
                                    **({"taxon_id": ",".join(map(str, anc))} if anc else {}))) or {}
        hit = next((t for t in r.get("results", []) if t.get("name") == g and t.get("rank") == "genus"), None)
        time.sleep(1)
        if not hit:
            continue
        got = []
        full = (get(f"{INAT}/taxa/{hit['id']}") or {}).get("results") or [{}]
        time.sleep(1)
        for tp in full[0].get("taxon_photos") or []:
            got.append((tp.get("photo") or {}, (tp.get("taxon") or {}).get("name") or g, "iNaturalist taxon photos"))
        sp = get(f"{INAT}/taxa", dict(parent_id=hit["id"], rank="species", is_active="true", per_page=100)) or {}
        time.sleep(1)
        for t in sp.get("results", []):
            if t.get("default_photo"):
                got.append((t["default_photo"], t.get("name") or g, "iNaturalist species default photo"))
        n = 0
        for p, taxon, found in got:
            rec = _photo(p, g, taxon, found)
            key = f"File:iNaturalist photo {p.get('id')}"
            if not rec or key in files:
                continue
            files[key] = rec
            n += 1
            if n >= cap(g):
                break
    return files
