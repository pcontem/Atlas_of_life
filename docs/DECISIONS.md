# Decisions

Append-only log. Newest at the bottom. Each line: date — decision — why.

## 2026-11-15 (prototype phase, decided with the owner in chat)

- Scope is life on Earth only; the earlier "Antichton" built-world framing is dropped.
- The genus is the unit of an entry; species are listed inside the genus entry (species-level
  entries would multiply work without adding much for fossil taxa).
- Every clade node is also an entry describing the group.
- Extinct genera must list their geological formations and the known fossil material
  (holotype, material, completeness, exceptional preservation).
- Incertae sedis taxa sit under the most exclusive clade with consensus support.
- Nomina dubia (and nuda, inquirenda) are excluded from the tree and listed with their reason.
- Every piece of information must be sourced.
- Images: real photographs and credited paleoart from Wikimedia Commons and PhyloPic only.
  No AI-generated images. Each genus has a size comparison with a 1.8 m human.
- Entries are written in English. The term is "entry", not "ficha".
- Pterosauria is the pilot volume.
- Website: Encyclopedia and Cladogram modes share one selection; opening an entry is done from
  the top bar only; double click opens/closes cladogram nodes; Search + Prune in the cladogram;
  Timeline follows the selected entry and is condensed to 3 sub-clade levels by default; Index
  has name, type and clade filters; no special-casing of the pilot group in code.

## 2026-11-15 (repository set-up)

- Entries are stored as one YAML file per genus/clade (`entries/`) and are the source of truth;
  `site/data.json` is generated. Reason: small, reviewable diffs and one file per request.
- Consolidate Pterosauria before any new volume. "Consolidated" = `validate.py --strict` passes.
- PhyloPic silhouettes under CC BY-NC are tolerated while the atlas is non-commercial, but are
  listed as consolidation issues to replace. ND licences are never used.
- The PBDB "type species" field proved unreliable (Pterodactylus and Scaphognathus came out
  wrong); type species are checked against the original description during consolidation.
- d3 is vendored in `site/vendor/` so the site has no runtime network dependency.

## 2026-11-15 (owner request)

- The excluded-names list holds only real published names rejected as invalid (nomina dubia,
  nuda, inquirenda, junior synonyms). Misspellings and duplicates of the prototype's list
  (Linglongopterus, Diocephalus, Pterodactyle) are removed; they were never real names.
- The "Cladogram" mode is renamed **Tree of life**: the view is an outline of the classification
  (ranks and groups), not a cladogram built from a phylogenetic analysis. URL `#tree-of-life`
  (the old `#cladogram` still works).
- Tree-of-life search shows ranked suggestions and centres the found sub-tree on screen.
- In the Tree of life, double-clicking the info card of the selected node opens its entry in the
  encyclopedia (in addition to the Encyclopedia button). Double-clicking a node still only
  opens/closes it.
- The Tree of life has a **Radial** layout besides the Linear one, drawn around the selected group
  (the whole tree in radial form is unreadable: ~30 rings of ancestors); both share selection, open
  groups, search, prune and the info card.
- Radial branches are drawn as elbows (arc along the parent's ring, then a straight spoke) and
  each classification level is one equally spaced ring, so divergence points are readable.
- Radial view restyled after an example from the owner (circular phylogeny): tips aligned on the
  outer circle, internal groups on equally spaced level rings, elbow branches, coloured sectors
  for the main groups (the largest group is split into its sub-clades, max 12 colours).
- Radial sectors: each tip is coloured by the least inclusive open group that contains it (not
  by the top-level group), so colours follow the part of the tree being explored.
- Index search has a "Search by" selector: Name, Clade or Time. Time search uses the ICS
  International Chronostratigraphic Chart v2024/12 as served by PBDB (`data/raw/timescale/`),
  the same timescale PBDB uses for the genus ages; an entry matches when its range overlaps the
  interval. Note: the Timeline and the genus time bar still draw the Jurassic/Cretaceous boundary
  at 145 Ma (older chart); to align with 143.1 Ma in a later change.
- Timeline and entry time bars cover the whole of Earth history (Hadean to Holocene) using the
  ICS chart from PBDB, including the Precambrian eons, eras and periods; the hard-coded
  Triassic–Cretaceous bands (with the old 145 Ma boundary) are gone.
- Index filters stack (AND): each Name / Clade / Time filter becomes a removable chip, so e.g.
  "inside Pterodactyloidea" + "lived in the Aptian" can be combined.
- Timeline simplified: only the direct subdivisions of the selected group (no condensed / all
  genera toggle), with a "↑ Parent group" button. The Earth-history strip uses a logarithmic
  age scale, because recent time is divided much more finely in the ICS chart.
- Earth-history strip: log offset raised from 1 to 50 Myr (owner: Cenozoic was too wide);
  now Cenozoic ≈ 19 %, Mesozoic ≈ 21 %, Paleozoic ≈ 15 %, Precambrian ≈ 45 % of the strip.
  In the Timeline a double-click on a genus opens its entry.
- Excluded names are placed in the tree (`parent` in excluded.yaml, from PBDB taxonomy) and the
  Excluded names page shows only those placed directly in the selected node, with sub-groups to
  go down into and a parent button, so every level stays navigable.
- "Genera through time" moved from clade pages to the Timeline (mode "All genera"). New Timeline
  mode "Diversity": genera known at each moment per subdivision (range-through counting from the
  PBDB first/last appearances) and ghost lineages back to the oldest record of the parent group
  (minimum divergence implied by the record; no phylogenetic dating is attempted).
- Clade pages list incertae sedis genera under their own heading "Incertae sedis".
