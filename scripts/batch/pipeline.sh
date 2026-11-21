#!/bin/bash
# Atlas genus batches (see the atlas-entries skill): run after scripts/draft_genera.py write.
# after writing a batch: drop replaced backbone nodes, formations, positions to fetch, build, validate
set -e
cd "$(git rev-parse --show-toplevel)"
python3 - <<'PY'
import json,pathlib
B=json.load(open('data/tree/backbone.json'))
names={p.stem for p in pathlib.Path('entries').glob('*/genera/*.yaml')}
ex=set()
import yaml
for p in pathlib.Path('entries').glob('*/excluded.yaml'):
    ex|={x['name'] for x in (yaml.safe_load(p.read_text()) or [])}
nb=[n for n in B if not (n[5]=='g' and (n[1] in names or n[1] in ex))]
print(len(B)-len(nb),'backbone genus nodes removed')
open('data/tree/backbone.json','w').write('[\n'+',\n'.join(json.dumps(n,ensure_ascii=False) for n in nb)+'\n]\n')
PY
python3 scripts/fmt.py >/dev/null
before=$(git diff --name-only entries/formations)
python3 scripts/make_formations.py | tail -1
python3 scripts/fmt.py >/dev/null
# keep tie-order-only changes out of formations that were unchanged before
for f in $(git diff --name-only entries/formations); do
  if ! echo "$before" | grep -qx "$f" && [ "$(git diff -U0 "$f" | grep '^[-+][a-z]' | grep -v '^[-+]\(environment\|lithology\):' | wc -l)" = 0 ]; then git checkout -q -- "$f"; fi
done
python3 scripts/paleo_points.py | tail -1
python3 scripts/build.py
python3 scripts/validate.py | grep -v " F4 \| I5 " | tail -15
# remove formation entries no genus lists any more, if they were created on this branch (not on main)
for f in $(python3 scripts/validate.py | grep " F3 .*no genus entry lists" | sed 's/.*formation \([^:]*\):.*/\1/'); do
  if ! git cat-file -e origin/main:entries/formations/$f.yaml 2>/dev/null; then rm -f entries/formations/$f.yaml; echo "removed orphan $f"; fi
done
python3 scripts/paleo_points.py | tail -1
python3 scripts/build.py
python3 scripts/validate.py | grep -v " F4 \| I5 " | tail -6
