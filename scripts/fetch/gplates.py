"""Fetch the palaeo-positions that scripts/paleo_points.py lists as missing, and merge them.

    python3 scripts/fetch/gplates.py

Calls the GPlates Web Service (reconstruct_points, model MERDITH2021) once per map time, then runs
`paleo_points.py <results>` so data/raw/paleomaps/formation_points.json is complete again.
"""
import json, pathlib, subprocess, sys, time, urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
REQ, RES = pathlib.Path("/tmp/paleo_request.json"), pathlib.Path("/tmp/paleo_results.json")


def main():
    subprocess.run([sys.executable, str(ROOT / "scripts/paleo_points.py")], check=True)
    req = json.loads(REQ.read_text())
    if not req:
        return
    res = {}
    for t, rows in req.items():
        pts = ",".join(f"{lng},{lat}" for _, lng, lat in rows)
        url = f"https://gws.gplates.org/reconstruct/reconstruct_points/?points={pts}&time={t}&model=MERDITH2021"
        for attempt in range(4):
            try:
                with urllib.request.urlopen(url, timeout=300) as r:
                    res[t] = json.loads(r.read())["coordinates"]
                break
            except Exception as e:
                if attempt == 3:
                    raise SystemExit(f"GPlates request failed ({t} Ma): {e}")
                time.sleep(10 * (attempt + 1))
        assert len(res[t]) == len(rows), f"{t} Ma: {len(res[t])} positions for {len(rows)} points"
    RES.write_text(json.dumps(res))
    subprocess.run([sys.executable, str(ROOT / "scripts/paleo_points.py"), str(RES)], check=True)


if __name__ == "__main__":
    main()
