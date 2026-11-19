#!/bin/bash
# resolve rebase conflicts in generated files: take upstream positions, rebuild everything
cd "$(git rev-parse --show-toplevel)"
git show HEAD:data/raw/paleomaps/formation_points.json > data/raw/paleomaps/formation_points.json
for f in $(git diff --name-only --diff-filter=U); do case $f in site/*) git checkout --ours -- $f;; esac; done
python3 scripts/media.py pull | tail -1
scripts/batch/pipeline.sh 2>&1 | tail -2
git add -A && GIT_EDITOR=true git rebase --continue 2>&1 | tail -1
