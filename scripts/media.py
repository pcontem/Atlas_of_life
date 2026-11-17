"""Site images live outside the main history: on the branch `media` of this repository, kept as a single
commit that is replaced on every push (so old versions never accumulate). The Pages workflow checks it
out into site/ before publishing; main only carries media/manifest.json.

    python3 scripts/media.py thumbs     # make 240-px thumbnails (site/img/thumb/...) for every image
    python3 scripts/media.py manifest   # rewrite media/manifest.json from site/img and site/sil
    python3 scripts/media.py push       # thumbs + manifest + replace the `media` branch with site/img + site/sil
    python3 scripts/media.py pull       # fetch the `media` branch and unpack it into site/ (then verify)
    python3 scripts/media.py verify     # every file of the manifest is in site/ with the right checksum
    python3 scripts/media.py fetch [vol] # download images/silhouettes the entries reference but the store lacks
    python3 scripts/media.py sync       # upload site/img + site/sil to the Cloudflare R2 bucket (only what changed)

Serving: when media/config.json has a base_url, the site loads the images from that public R2 bucket and
the Pages workflow no longer publishes them (no 1 GB GitHub Pages limit). The `media` branch stays the
reference copy; .github/workflows/media-sync.yml copies it to R2 whenever it changes.

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
    import os
    # in GitHub Actions the checkout's credentials do not apply to the temporary repository: pass a token URL
    remote = os.environ.get("MEDIA_REMOTE") or git("remote", "get-url", "origin").decode().strip()
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


UA = {"User-Agent": "AtlasOfLife/1.0 (https://github.com/pcontem/Atlas_of_life; media fetch)"}


def download(url):
    import time, urllib.request
    for k in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except Exception as e:
            if k == 3:
                print(f"  ! {url}: {e}")
                return None
            time.sleep(5 * (k + 1))


def fetch(vol=None):
    """Download the images and silhouettes that genus entries reference but the media store lacks (images without
    `local`, or whose local file is missing): gallery images -> img/gallery/<Genus>_<nnn>.webp (max 800 px),
    silhouettes -> sil/<uuid>.webp (from PhyloPic's PNG). Writes `local` (and the silhouette's w/h) into the entry.
    Needs web access: run in GitHub Actions (.github/workflows/media-fetch.yml), after `pull`."""
    import re, time
    from PIL import Image
    taken = {p.name for p in (SITE / "img/gallery").glob("*.webp")} if (SITE / "img/gallery").exists() else set()
    (SITE / "img/gallery").mkdir(parents=True, exist_ok=True)
    (SITE / "sil").mkdir(parents=True, exist_ok=True)
    done = 0
    for gp in sorted((ROOT / "entries").glob(f"{vol or '*'}/genera/*.yaml")):
        text = gp.read_text()
        e = yaml.safe_load(text)
        changed = False
        for im in e.get("images") or []:
            if im.get("local") and (SITE / im["local"]).exists():
                continue
            b = download(im["url"])
            time.sleep(0.5)
            if not b:
                continue
            k = 1
            while f"{e['name']}_{k:03d}.webp" in taken:
                k += 1
            name = f"{e['name']}_{k:03d}.webp"
            taken.add(name)
            pic = Image.open(io.BytesIO(b))
            pic = pic.convert("RGBA" if pic.mode in ("RGBA", "LA", "P") else "RGB")
            pic.thumbnail((800, 800))
            pic.save(SITE / "img/gallery" / name, "WEBP", quality=82)
            im["local"] = f"img/gallery/{name}"
            changed = True
            done += 1
        s = e.get("silhouette")
        if s:
            uuid = s["page"].split("/images/")[-1]
            dest = SITE / "sil" / f"{uuid}.webp"
            if not dest.exists() and s.get("png"):
                b = download(s["png"])
                if b:
                    pic = Image.open(io.BytesIO(b)).convert("RGBA")
                    pic.thumbnail((600, 600))
                    pic.save(dest, "WEBP", quality=85)
                    s["w"], s["h"] = pic.size
                    changed = True
                    done += 1
        if changed:
            gp.write_text(yaml.safe_dump(e, allow_unicode=True, sort_keys=False, width=120))
    print(f"fetch: {done} files downloaded")


CONTENT_TYPES = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".svg": "image/svg+xml"}


def sync():
    """Make the R2 bucket hold exactly the files of the manifest: upload missing or changed files (compared by
    MD5 = the ETag R2 returns for single-part uploads), delete img/ and sil/ objects the manifest no longer has.
    Needs boto3 and R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_BUCKET in the environment."""
    import os
    need = ["R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET"]
    missing = [k for k in need if not os.environ.get(k)]
    if missing:
        sys.exit("sync: missing " + ", ".join(missing))
    import boto3
    verify()
    s3 = boto3.client("s3", endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
                      aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
                      aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"], region_name="auto")
    bucket, man = os.environ["R2_BUCKET"], json.loads(MAN.read_text())
    remote = {}
    for prefix in ("img/", "sil/"):
        for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
            for o in page.get("Contents", []):
                remote[o["Key"]] = o["ETag"].strip('"')
    up = 0
    for rel in sorted(man):
        b = (SITE / rel).read_bytes()
        if remote.get(rel) == hashlib.md5(b).hexdigest():
            continue
        s3.put_object(Bucket=bucket, Key=rel, Body=b,
                      ContentType=CONTENT_TYPES.get(pathlib.Path(rel).suffix.lower(), "application/octet-stream"),
                      CacheControl="public, max-age=86400")
        up += 1
    gone = sorted(set(remote) - set(man))
    for i in range(0, len(gone), 1000):
        s3.delete_objects(Bucket=bucket, Delete={"Objects": [{"Key": k} for k in gone[i:i + 1000]]})
    print(f"sync: {up} uploaded, {len(gone)} deleted, {len(man) - up} unchanged · bucket {bucket}")


if __name__ == "__main__":
    cmd = {"thumbs": thumbs, "manifest": manifest, "push": push, "pull": pull, "verify": verify, "sync": sync, "fetch": fetch}[sys.argv[1]]
    cmd(*sys.argv[2:3])
