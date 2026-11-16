"""Keep data/raw/paleomaps/formation_points.json in step with the formation entries.

    python3 scripts/paleo_points.py                 # reuse, prune, and list what still has to be fetched
    python3 scripts/paleo_points.py results.json    # merge positions fetched from the GPlates Web Service

Each formation needs its present-day location reconstructed (model MERDITH2021) at every map time
within its age range ± 2.5 Myr (or the nearest map time). Rows whose location is already known for that
time (e.g. a formation that only changed id) are reused; rows of locations no longer used are removed.
What is left is written to /tmp/paleo_request.json as {Ma: [[id, lng, lat], ...]}: fetch
https://gws.gplates.org/reconstruct/reconstruct_points/?points=lng,lat,...&time=Ma&model=MERDITH2021
for each time (in a browser if the shell has no network) and save {Ma: [[plng, plat], ...]} in the same
order; 999.99 means "not on a plate" and is stored as null.
"""
import json, pathlib, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
PTS = ROOT / "data/raw/paleomaps/formation_points.json"
MAPS = ROOT / "data/raw/paleomaps/merdith2021_coastlines.json"
REQ = pathlib.Path("/tmp/paleo_request.json")


def key(lng, lat):
    return round(lng, 3), round(lat, 3)


def main():
    P = json.loads(PTS.read_text())
    times = sorted(int(t) for t in json.loads(MAPS.read_text())["maps"])
    known = {}
    for t, rows in P["points"].items():
        for fid, lng, lat, a, b in rows:
            known[key(lng, lat) + (int(t),)] = [a, b]
    if len(sys.argv) > 1:  # merge fetched results
        req, res = json.loads(REQ.read_text()), json.loads(pathlib.Path(sys.argv[1]).read_text())
        for t, rows in req.items():
            for (fid, lng, lat), p in zip(rows, res[t]):
                known[key(lng, lat) + (int(t),)] = [None, None] if p[0] > 900 else [round(p[0], 3), round(p[1], 3)]
    out, missing = {}, {}
    for p in sorted((ROOT / "entries/formations").glob("*.yaml")):
        e = yaml.safe_load(p.read_text())
        a, loc = e["age"], e["location"]
        if loc["lat"] is None:
            continue
        ts = [t for t in times if a["last_ma"] - 2.5 <= t <= a["first_ma"] + 2.5] or \
             [min(times, key=lambda t: abs(t - (a["first_ma"] + a["last_ma"]) / 2))]
        for t in ts:
            k = key(loc["lng"], loc["lat"]) + (t,)
            if k in known:
                out.setdefault(str(t), []).append([e["id"], loc["lng"], loc["lat"], *known[k]])
            else:
                missing.setdefault(str(t), []).append([e["id"], loc["lng"], loc["lat"]])
    P["points"] = dict(sorted(out.items(), key=lambda kv: int(kv[0])))
    PTS.write_text(json.dumps(P, ensure_ascii=False, indent=0))
    REQ.write_text(json.dumps(missing))
    n = sum(map(len, missing.values()))
    print(f"{sum(map(len, out.values()))} positions kept; {n} still to fetch" + (f" (listed in {REQ})" if n else ""))


if __name__ == "__main__":
    main()
