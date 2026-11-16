"""Site images live outside the main history: on the branch `media` of this repository, kept as a single
commit that is replaced on every push (so old versions never accumulate). The Pages workflow checks it
out into site/ before publishing; main only carries media/manifest.json.

    python3 scripts/media.py thumbs     # make 240-px thumbnails (site/img/thumb/...) for every image
    python3 scripts/media.py manifest   # rewrite media/manifest.json from site/img and site/sil
    python3 scripts/media.py push       # thumbs + manifest + replace the `media` branch with site/img + site/sil
    python3 scripts/media.py pull       # fetch the `media` branch and unpack it into site/ (then verify)
    python3 scripts/media.py verify     # every file of the manifest is in site/ with the right checksum

media/manifest.json records path, size, sha256 and volume of every file; the validator checks image
paths against it. site/img and site/sil are git-ignored on main.
(A GitHub release was the first choice, but release assets cannot be written from the sessions that
maintain this atlas; a single-commit branch gives the same result with plain git.)
"""
import hashlib, io, json, pathlib, subprocess, sys, tarfile
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
MAN = ROOT / "media/manifest.json"
THUMB = 240


def media_files():
    return sorted(p for d in ("img", "sil") for p in (SITE / d).rglob("*") if p.is_file())


def thumb_path(rel):
    """img/gallery/X.webp -> img/thumb/gallery/X.webp ; img/X_life.webp -> img/thumb/X_life.webp"""
    return "img/thumb/" + rel[4:]


def thumbs():
    from PIL import Image
    n = 0
    for p in media_files():
        rel = p.relative_to(SITE).as_posix()
        if not rel.startswith("img/") or rel.startswith("img/thumb/"):
            continue
        t = SITE / thumb_path(rel)
        if t.exists() and t.stat().st_mtime >= p.stat().st_mtime:
            continue
        t.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(p)
        im.thumbnail((THUMB, THUMB))
        im.save(t, "WEBP", quality=80)
        n += 1
    print(f"thumbs: {n} made")


def volume_of():
    """path -> volume whose genus entries use it (images, their thumbnails, silhouettes)."""
    owner = {}
    for gp in sorted((ROOT / "entries").glob("*/genera/*.yaml")):
        vol, e = gp.parent.parent.name, yaml.safe_load(gp.read_text())
        paths = [i.get("local") or f"img/{''.join(c for c in e['name'] if c.isalpha())}_{i['kind']}.webp" for i in e.get("images") or []]
        if e.get("silhouette"):
            paths.append("sil/" + e["silhouette"]["page"].split("/images/")[-1] + ".webp")
        for p in paths:
            owner.setdefault(p, vol)
            if p.startswith("img/"):
                owner.setdefault(thumb_path(p), vol)
    return owner


def manifest():
    owner, man = volume_of(), {}
    for p in media_files():
        rel = p.relative_to(SITE).as_posix()
        b = p.read_bytes()
        man[rel] = dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), volume=owner.get(rel, ""))
    MAN.parent.mkdir(exist_ok=True)
    MAN.write_text(json.dumps(man, indent=0, sort_keys=True))
    print(f"manifest: {len(man)} files, {sum(v['bytes'] for v in man.values()) / 1e6:.1f} MB")
    return man


def git(*args, cwd=ROOT, **kw):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, **kw)
    if r.returncode:
        sys.exit(f"git {' '.join(args)}: {r.stderr.decode()[:400]}")
    return r.stdout


def push():
    import shutil, tempfile
    thumbs()
    manifest()
    remote = git("remote", "get-url", "origin").decode().strip()
    with tempfile.TemporaryDirectory() as tmp:
        for d in ("img", "sil"):
            shutil.copytree(SITE / d, pathlib.Path(tmp) / d)
        (pathlib.Path(tmp) / "README.md").write_text(
            "Images of the Atlas of Life site (served under site/). Replaced on every update by "
            "`python3 scripts/media.py push` on main; do not edit here.\n")
        git("init", "-q", "-b", "media", cwd=tmp)
        git("add", "-A", cwd=tmp)
        git("-c", "user.name=atlas-media", "-c", "user.email=atlas-media@users.noreply.github.com",
            "commit", "-q", "-m", "Site images snapshot", cwd=tmp)
        git("-c", "push.negotiate=true", "push", "-q", "-f", remote, "media:media", cwd=tmp)
    print("media branch replaced with the current images")


def pull():
    git("fetch", "-q", "--depth", "1", "origin", "media")
    tar = git("archive", "FETCH_HEAD", "img", "sil")
    man = json.loads(MAN.read_text())
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        for m in t.getmembers():
            if m.isfile() and m.name in man and ".." not in m.name:  # only files the manifest knows
                (SITE / m.name).parent.mkdir(parents=True, exist_ok=True)
                (SITE / m.name).write_bytes(t.extractfile(m).read())
    verify()


def verify():
    man, bad = json.loads(MAN.read_text()), []
    for rel, v in man.items():
        p = SITE / rel
        if not p.exists() or hashlib.sha256(p.read_bytes()).hexdigest() != v["sha256"]:
            bad.append(rel)
    if bad:
        sys.exit(f"{len(bad)} media file(s) missing or different, e.g. {bad[:3]}")
    print(f"verify: {len(man)} media files OK")


if __name__ == "__main__":
    {"thumbs": thumbs, "manifest": manifest, "push": push, "pull": pull, "verify": verify}[sys.argv[1]]()
