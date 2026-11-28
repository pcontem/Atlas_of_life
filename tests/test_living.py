"""Offline tests of scripts/fetch/living.py (Catalogue of Life genera, iNaturalist photos) with fake API answers."""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "scripts/fetch"))
import living as L

L.time.sleep = lambda s: None


def usage(i, name, auth="", rank="genus", extinct=False, cl=()):
    return dict(id=i, classification=[dict(name=n, rank=r) for r, n in cl],
                usage=dict(id=i, name=dict(scientificName=name, authorship=auth, rank=rank), extinct=extinct))


def fake_col(url, params):
    if params.get("type") == "EXACT":
        return dict(result=[usage("AV", params["q"], rank="class")], last=True, total=1)
    if params.get("rank") == "genus":
        return dict(result=[usage("G1", "Anas", "Linnaeus, 1758", cl=[("order", "Anseriformes"), ("family", "Anatidae")]),
                            usage("G2", "Dodo", "x", extinct=True), usage("G3", "Struthio", "Linnaeus, 1758")], last=True, total=3)
    if params.get("rank") == "species":
        sp = {"G1": [usage("S1", "Anas platyrhynchos", "Linnaeus, 1758", rank="species"), usage("S2", "Anas extincta", rank="species", extinct=True)],
              "G3": [usage("S3", "Struthio camelus", "Linnaeus, 1758", rank="species")]}[params["TAXON_ID"]]
        return dict(result=sp, last=True, total=len(sp))
    return {}


def test_col():
    g = L.col_genera(fake_col, ["Aves"], skip={"Struthio"})
    assert set(g) == {"Anas"}, g
    assert g["Anas"]["family"] == "Anatidae" and g["Anas"]["order"] == "Anseriformes"
    assert [s["name"] for s in g["Anas"]["species"]] == ["Anas platyrhynchos"]
    assert g["Anas"]["url"].endswith("/G1")


def photo(i, lic):
    return dict(id=i, license_code=lic, attribution=f"(c) Jane Roe, some rights reserved ({lic})",
                url=f"https://inaturalist-open-data.s3.amazonaws.com/photos/{i}/square.jpg", original_dimensions=dict(width=2048, height=1536))


def fake_inat(url, params=None):
    params = params or {}
    if url.endswith("/taxa") and params.get("q") == "Aves":
        return dict(results=[dict(id=3, name="Aves")])
    if url.endswith("/taxa") and params.get("rank") == "genus":
        assert params.get("taxon_id") == "3"
        return dict(results=[dict(id=10, name=params["q"], rank="genus")])
    if url.endswith("/taxa/10"):
        return dict(results=[dict(taxon_photos=[dict(photo=photo(1, "cc-by"), taxon=dict(name="Anas platyrhynchos")),
                                                dict(photo=photo(2, "cc-by-nc"), taxon=dict(name="Anas acuta"))])])
    if params.get("parent_id") == 10:
        return dict(results=[dict(name="Anas crecca", default_photo=photo(3, "cc0")), dict(name="Anas x", default_photo=photo(1, "cc-by"))])
    return {}


def test_inat():
    f = L.inat_photos(fake_inat, ["Anas"], ["Aves"])
    assert set(f) == {"File:iNaturalist photo 1", "File:iNaturalist photo 3"}, f   # NC photo dropped, duplicate kept once
    a = f["File:iNaturalist photo 1"]
    assert a["LicenseShortName"] == "CC BY 4.0" and a["page"] == "https://www.inaturalist.org/photos/1"
    assert a["url"].endswith("/large.jpg") and a["thumb"].endswith("/medium.jpg") and (a["width"], a["height"]) == (1024, 768)
    assert a["Artist"] == "Jane Roe" and a["genera"] == ["Anas"] and a["source"] == "iNaturalist"
    assert f["File:iNaturalist photo 3"]["LicenseShortName"] == "CC0"


if __name__ == "__main__":
    test_col(); test_inat()
    print("living tests: all passed")
