"""Rewrite every entry file in the canonical YAML layout (key order kept, short lists inline).

    python3 scripts/fmt.py          # rewrite in place
    python3 scripts/fmt.py --check  # exit 1 if any file is not formatted

Run after editing entries so diffs stay small and reviewable.
"""
import pathlib, sys
import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


class Dumper(yaml.SafeDumper):
    pass


def _str(d, s):
    return d.represent_scalar("tag:yaml.org,2002:str", s, style="|" if "\n" in s else None)


def _list(d, v):
    flow = all(isinstance(x, (int, float, str, type(None))) for x in v) and sum(len(str(x)) for x in v) < 70
    return d.represent_sequence("tag:yaml.org,2002:seq", v, flow_style=flow)


Dumper.add_representer(str, _str)
Dumper.add_representer(list, _list)


def dumps(obj):
    return yaml.dump(obj, Dumper=Dumper, sort_keys=False, allow_unicode=True, width=110)


def main():
    check = "--check" in sys.argv
    bad = []
    for p in sorted((ROOT / "entries").rglob("*.yaml")):
        text = p.read_text()
        new = dumps(yaml.safe_load(text))
        if new != text:
            bad.append(p.relative_to(ROOT))
            if not check:
                p.write_text(new)
    if check and bad:
        print("not formatted:", *bad, sep="\n  ")
        sys.exit(1)
    print(f"{'unformatted' if check else 'formatted'}: {len(bad)} file(s)")


if __name__ == "__main__":
    main()
