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
- Diversity mode shows the selected group as a whole (not one spindle per subdivision), with
  its own ghost lineage back to the oldest record of its parent group. All-genera bars are
  coloured by subdivision.
- Ghost lineages are measured against the sister groups (other subdivisions of the parent),
  each dated by its firm first appearance (`fad_firm`: youngest possible age of the oldest
  occurrence, or the end of the first stage named when there are no dated occurrences). The
  earlier rule used the maximum possible age of the parent's oldest record, so broadly dated
  occurrences (Caelestiventus "Late Triassic–Early Jurassic", Pterodactylus "Angulata /
  Kimmeridgian") gave almost every group a long ghost lineage. Groups in polytomies still get
  one when a sister is securely older, as they should.
- Ghost lineages revised again (owner): drawn only within the group's own range, as gaps in its
  record between first and last appearance. Comparisons with sister groups were dropped — the
  classification is full of polytomies, not binary splits, so they produced more ghost lineages
  than a resolved phylogeny would. (`fad_firm` removed from the build; no longer needed.)
- Timeline: "Subdivisions / All genera" replaced by a Resolution menu (Genus by default, then
  sub-group levels); bars always coloured by direct subdivision. The same menu sets what the
  Diversity mode counts (genera, or sub-groups of a given level).
- Timeline resolution is chosen by taxonomic rank (Genus, Family, Superfamily, Suborder…), not by
  depth. Clade entries gain `taxon_rank` from PBDB taxonomy (several pterosaur clades are unranked
  there and are never offered as a resolution). Bars use a more vivid palette.
- Genus entries now have image galleries (up to 8 per kind: life restorations, fossils,
  skeletal reconstructions). 359 images added from Wikimedia Commons (category trees per genus,
  licence- and AI-filtered, every one checked visually; 74 rejected: models, statues, park
  sculptures, dark or duplicate shots, old restorations, other taxa). All new reconstructions
  are `unreviewed` for accuracy.

## 2026-11-16

- No permission requests to artists. Artwork without a compatible open licence (DeviantArt,
  ArtStation, personal sites…) is only linked from the entry (`external`, rule I7), never
  copied. Other free sources (CC BY open-access papers, Smithsonian Open Access, BHL, Flickr CC)
  may be copied, with the licence recorded per image.
- Galleries gain figures from open-access articles (CC BY, found through Europe PMC/PMC): 44
  figures (29 fossil, 6 life, 9 skeletal) for 22 genera, from 63 candidate articles and 89
  downloaded figures; 22 dropped as copies of figures already taken from Commons (image-hash
  comparison per genus), 23 rejected on the contact sheet (charts, CT renderings, schematic
  outlines, a shark tooth, insects of the beetle genus *Sordes*, a figure of *Sinopterus* filed
  under *Huaxiadraco*). Image `page` may now be the article's DOI link (validator I2); each
  article is also added to the genus sources. Figures kept at 1000 px so their labels stay
  legible. All are `unreviewed`.
- New third mode, **Biota** (owner's design): a time slider moves a palaeogeographic map; the
  formations with atlas taxa are points; double-click opens the place's environment and the taxa
  that shared it. Choices made with the owner:
  - Map: vector coastlines from the **Merdith et al. (2021)** plate model (1000–0 Ma, CC BY 4.0,
    Zenodo), fetched from the GPlates Web Service and stored simplified in `data/raw/paleomaps/`
    (every 5 Myr to 540 Ma, every 20 Myr to 1000 Ma). Chosen over Müller et al. 2019 (only 250 Ma,
    too short for the whole atlas) and over Scotese PALEOMAP images (licence unclear). Formation
    points are reconstructed with the same model, so points and continents agree. The model is in a
    palaeomagnetic frame: palaeolatitudes are meaningful, longitudes are not. Coastlines are
    present-day shorelines carried back in time; ancient seaways are not drawn.
  - Biota lists **only atlas entries** (for now only pterosaurs); no PBDB faunal lists.
  - Places are a **new entry type**, `entries/formations/`, shared by all volumes: PBDB fields
    (location, age, environment, lithology) generated by `scripts/make_formations.py`, prose
    (`summary`, `paleoenvironment`) written by hand with sources (rules F1–F5). 101 formation
    entries created as drafts (unnamed units are one locality per genus); their prose is open
    consolidation work (F5, S2, Q1).
- Biota (owner): the slider and the era/period strip use a gently non-linear scale
  (1 − (age/1000)^0.6) so recent times get more room; a single click on a formation shows its card
  beside the map, a double-click opens the formation's own encyclopedia entry (`#formation/<id>`,
  new view `entry-formation.js`), also linked from the formation table of genus entries.
- Biota map zoom (owner): scroll/drag and + / − / ⟲, up to ×8 (coastlines are simplified to
  0.3°, so closer zooms would only show their simplification), kept across time steps.
  New Encyclopedia sub-tab **Formations** (owner: "a section of geological formations"), between
  Timeline and Excluded names, listing and filtering all formation entries.
