"""Visual smoke test: serve site/ and take a screenshot of each main view.

    python3 tests/screenshots.py            # all views
    python3 tests/screenshots.py Tapejara   # also the entry page of one taxon

Needs Google Chrome or Chromium on the PATH. Images go to tests/out/ (git-ignored).
Open them and look: this is how a change is checked before committing.
Also fails if the page shows its "Could not load the data file" message.
"""
import http.server, pathlib, shutil, socketserver, subprocess, sys, threading, functools

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "tests/out"
VIEWS = {
    "entry-genus": "#Pteranodon",
    "entry-clade": "#pterosauria",
    "index": "#index",
    "timeline": "#time",
    "cladogram": "#cladogram",
    "excluded": "#excluded",
    "about": "#about",
}


def chrome():
    for c in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        if shutil.which(c):
            return c
    sys.exit("Chrome/Chromium not found")


def main():
    views = dict(VIEWS)
    for name in sys.argv[1:]:
        views["entry-" + name] = "#" + name
    OUT.mkdir(parents=True, exist_ok=True)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=str(ROOT / "site"))
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as srv:
        port = srv.server_address[1]
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        bad = []
        for name, frag in views.items():
            url = f"http://127.0.0.1:{port}/index.html{frag}"
            png = OUT / f"{name}.png"
            subprocess.run([chrome(), "--headless=new", "--no-sandbox", "--disable-gpu", "--window-size=1400,900",
                            "--virtual-time-budget=6000", f"--screenshot={png}", url],
                           capture_output=True, timeout=60)
            dom = subprocess.run([chrome(), "--headless=new", "--no-sandbox", "--disable-gpu",
                                  "--virtual-time-budget=6000", "--dump-dom", url],
                                 capture_output=True, text=True, timeout=60).stdout
            ok = png.exists() and "Could not load the data file" not in dom and "Loading…" not in dom
            print(("ok   " if ok else "FAIL ") + f"{name:14} {png.relative_to(ROOT)}")
            if not ok:
                bad.append(name)
        srv.shutdown()
    if bad:
        sys.exit(f"{len(bad)} view(s) failed: {', '.join(bad)}")


if __name__ == "__main__":
    main()
