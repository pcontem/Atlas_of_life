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
- Formation clean-up (owner: units of the same formation and unnamed units cluttered the map):
  units are merged only when they are the same formation — other names of the same unit (with
  source), units PBDB records as members of a formation, and beds without a formation placed per
  PBDB collection (member/collection name → formation; else PBDB group → "<Group> Group (beds not
  assigned to a formation)"; else one entry per site). 101 → 93 entries; Solnhofen is now the
  Altmühltal Formation (Solnhofen Member), Rauhut et al. 2017. Distinct formations close together
  (e.g. Crato and Romualdo, Altmühltal and Mörnsheim) stay separate entries; on the map, points that
  overlap on screen are drawn as one cluster marker that splits when zooming in.
- Biota zoom made finer (owner: ×8 did not separate the formations): up to ×96, the factor shown
  under the buttons, double-click on a cluster zooms ×4; at the deepest zoom, points that still
  overlap (sites a few km apart or the same site) fan out around their spot. The coastlines stay
  simplified to 0.3°, so at high zoom they are only indicative.
- Scaling (owner asked for the four changes):
  1. **Lazy loading**: `data.json` is now an index (891 → 323 KB for 126 genera); each full genus
     entry is its own file `site/g/<Genus>.json`, fetched when its page opens.
  2. **Images out of main**: the owner chose GitHub Releases, but release assets cannot be created
     or edited from the sessions that maintain the atlas (403). Same goal with plain git instead: the
     images live on the branch `media`, kept as a single commit that `scripts/media.py push` replaces
     (no old versions pile up); main keeps only `media/manifest.json`; the Pages workflow pulls them
     before publishing. 240-px thumbnails added for every image. Note: the published site is still
     subject to GitHub Pages' 1 GB limit; this change keeps the repository history light, it does not
     raise that limit (images ≈ 230 KB per genus incl. thumbnails → about 4,000 genera).
  3. **Automated data refresh** in GitHub Actions (PBDB + GPlates → PR), monthly and on demand.
  4. **Collapsible taxa groups** (by volume, then parent clade) in the Biota card and formation entry.
- Interface (owner): Biota search box (genus or formation); "Excluded names" and "About & sources"
  merged into one Encyclopedia tab; the Encyclopedia sub-tabs moved to their own bar, apart from
  the mode selector; all Portuguese removed from the atlas (177 backbone names and notes translated;
  L1 now checks the whole backbone); the root page "Life" became the start page: an introduction to
  life on Earth (sourced to fixed revisions of six Wikipedia articles) with 19 openly licensed
  pictures of very different groups, each linking to its place in the tree (`entries/home.yaml`,
  rules H1–H3).
- Contributions and reviews (owner chose option A, GitHub only): AI builds the drafts, people
  review them. Issue forms (correction, review, image, new genus), a PR template with checklists,
  CODEOWNERS, labels, and branch protection on `main` (1 approval by someone other than the author,
  stale approvals dismissed, `check` required; the owner can still merge as admin). Every entry's
  `curation` gained `origin` (ai-draft | human) and `reviews` (by, on, scope, verdict, notes,
  confirmed_by, confirmed_on); all 240 existing entries are `origin: ai-draft`. **Two-person rule:**
  `checked` needs an accepted full review confirmed by a second person (validator Q1–Q3). The site
  shows an "AI draft" badge and a "Review & contribute" card with pre-filled issue links. A monthly
  workflow opens an audit issue with 5 random checked entries. Still open for the owner: the licence
  of text and code, who is invited as reviewer, and whether 2 approvals are required for
  classification changes (for now the second-reviewer rule is in the PR checklist, not enforced by GitHub).
- Image review form without tick boxes (owner: the criteria are too complex and group-specific to
  tick). The reviewer describes the assessment and sources in free text, which a reviewer or the AI
  reads. Rule I4 states general criteria for any group; group-specific points are guidance under
  `restoration_checks` in each volume's `_volume.yaml` (Pterosauria: pycnofibres, wing membrane to
  the ankle, crest/teeth/skull).
- Image storage moves to Cloudflare R2 (owner's choice: most flexible while free; the site stays on
  GitHub Pages). Reason: GitHub Pages sites may not exceed 1 GB, about 4,000 genera at ~250 KB of images
  each. R2's free tier gives 10 GB of storage with free egress (~40,000 genera), then $0.015/GB/month.
  The `media` branch stays the reference copy; a workflow syncs it to the bucket; `media/config.json`
  `base_url` switches the site to the bucket. Hotlinking Wikimedia Commons was rejected: files can be
  changed or deleted there, and since 2026 non-standard thumbnail sizes are refused. Note: Cloudflare
  marks the free `r2.dev` address as rate-limited and not meant for production; a custom domain (~$10 a
  year) is the long-term address. Only `base_url` changes when switching.
- Phase rule removed (owner, 2026-11-16): clade entries for the whole tree of life may be written now, not
  only after Pterosauria is consolidated. Scope: all 787 named clade nodes of the backbone (89 informal
  groupings get none), full entries (as for Pterosauria clades), written in batches by group, one PR per
  batch. New files in `entries/tree/clades/`; the structure stays in `backbone.json`. Sources harvested on
  2026-11-16 in the browser: Wikipedia (title, fixed revision, text, citations of that revision) and PBDB
  (rank, authority, primary reference).
- Tree taxonomy review (owner, 2026-11-16): authority = PBDB + recent literature (changes only where they
  agree; disagreements kept and listed). Informal groupings and multi-family nodes removed (99), members placed
  in the real clade or in their PBDB family (21 families added), 15 clades moved, 135 genera placed more
  precisely, duplicate nodes merged, Portuguese leftovers renamed. New validator rule T1. Full log and open
  questions: docs/TREE_REVIEW.md.
- The tree must be an approximate phylogeny of nested clades, like the Pterosauria volume, not a set of
  groupings (owner, 2026-11-17). Each group is restructured from recent cladograms (Wikipedia {{clade}}
  diagrams of the cited revisions, with their source studies) checked against PBDB, before its clade entries
  are written. Pseudosuchia done first: 10 clades added (Suchia, Paracrocodylomorpha, Loricata, Solidocrania,
  Mesoeucrocodylia, Protosuchidae, Gobiosuchidae, Longirostres, Gavialidae, Desmatosuchia), the grades
  Rauisuchia and Protosuchia removed.

## 2026-11-17 — Pseudosuchia genus volume started
- Owner request: genus entries for all 646 valid PBDB genera of Pseudosuchia, by the Pterosauria method; size as
  body length plus mass when published; images written together with the text.
- The 59 Pseudosuchia clade entries move from `entries/tree/clades` to the new volume `entries/pseudosuchia/clades`
  and their nodes leave `backbone.json`; compound ids lose their prefix (`crocodylia__alligatoroidea` →
  `alligatoroidea`). Backbone genera of the group stay in the outline until their entry is written.
- Size generalised: `size_measure` per volume (`wingspan` | `length`), `length_m`, optional `mass_kg`; genus
  `extant` flag; volume clades living/extinct computed from the genera below them.
- Raw material is downloaded by a GitHub Actions workflow (`harvest.yml`), since the runners reach PBDB,
  Wikipedia, Commons and PhyloPic directly.
- Scope of the volume (2026-11-17): PBDB's 646 valid genera of Pseudosuchia include 33 ichno- and egg form-genera
  (flags I/F: footprints such as *Chirotherium*, *Batrachopus*; eggs such as *Krokolithes*) — not entries, since an
  entry is a body-fossil or living genus — and 29 phytosaurs, which the atlas tree keeps outside Archosauria
  (TREE_REVIEW: "Phytosauria … kept where it was"); they get entries with Archosauriformes. PBDB's living flag is
  wrong for some fossil and ichno genera, so `extant` is set by hand.
- Living genera: image kind `photo` (photographs of the living animal), at most the article's pictures; formations
  only the named units with fossils of the accepted species; ages from those occurrences, `last_ma: 0`.
- `scripts/make_formations.py`: beds without a formation are matched to a genus item by country as well as region
  (unnamed Tanzanian beds were being filed under Chad); the ISO country table moved there from the drafting helper.
- Images (2026-11-17): 23 of the first 52 Pseudosuchia genera had no free picture on Commons beyond navigation-box
  images of other genera. The harvest now also collects figures of CC BY / CC0 open-access articles from Europe
  PMC whose caption names the genus (`data/raw/<volume>/oa_figures.json`, contact sheets on branch
  `sheets/<volume>-oa`), the second image source of CLAUDE.md §4.4. The request-file workflows no longer run on main.

## 2026-11-19 — Clade work queue
- `docs/QUEUE.md` is the ordered list of backbone clades still without an entry, with the working
  procedure for Claude, so a new session needs no chat history: read CLAUDE.md and QUEUE.md, take the
  next batch (10 by default), write the entries (§4.2b), run fmt/build/validate, re-run `scripts/queue.py`.
- The file is generated (`python3 scripts/queue.py`): done = an entry file exists; order = top-down walk of
  the backbone (parents first), with optional priority subtrees in `docs/queue_priority.txt`.

## 2026-11-19 — Image triage page
- Owner request: classify candidate images by clicking a button and have them added to the genera automatically.
- `tools/triage/index.html` (one static page, no build) loads `data/triage/<volume>.json` — the Commons and
  open-access candidates of `data/raw/<volume>/`, generated by `scripts/triage_data.py` — and the earlier decisions.
  Buttons: photo / life / fossil / skeletal / reject, and accepted / outdated / unreviewed for images already in an
  entry. Disallowed licences and `photo` for extinct genera cannot be chosen.
- Send = a new branch `triage/<volume>-<time>` with one file `data/triage/<volume>_decisions/<time>.json` (one file
  per send, so sends never conflict), written through the GitHub API with the owner's fine-grained token (kept only
  in the browser). `.github/workflows/triage-apply.yml` applies it (`scripts/apply_triage.py`, reusing
  `draft_genera.py addimg|addoa`), fetches the files into the media store, validates and opens a pull request.
  Nothing reaches `main` without that PR.
- The page shows Commons and article images directly from their sites (it is a tool, not part of the published site,
  so the §6 rule against remote images does not apply to it).
- Volumes from before `harvest.py` (Pterosauria) have no candidate file yet.
- Triage page hides pictures of relatives by default (owner, 2026-11-19): `triage_data.py` marks a candidate `other`
  when its file name or description names another genus of the volume and not the genus itself, one of its
  synonyms (PBDB, excluded.yaml) or one of its species epithets. About 55% of the Pseudosuchia candidates; nothing is
  deleted, a checkbox shows them.

## 2026-11-21 — Queue split: general clades vs production units
- Owner request: a queue where a less inclusive clade is written together with ALL its genera; very inclusive
  clades stay "entry only".
- `scripts/queue.py` now writes two files. `docs/QUEUE.md` = general clades (entry only). `docs/QUEUE_GENERA.md` =
  production units: the most inclusive clades with at most `UNIT_MAX` (default 30) genera, plus blocks of genera
  sitting directly in a general clade (chunked by 30), plus genera still waiting inside a volume (Pseudosuchia, 184).
- One unit = one conversation = one branch/PR (clade entries first, then one genus batch, `atlas-entries` skill).
- Redundancy: genera with an entry in any volume are ticked automatically; backbone nodes for Caiman, Mecistops and
  Paleosuchus (entries exist, parents already in the Pseudosuchia volume) are still to be removed from `backbone.json`.
- 2026-11-21 (follow-up): a production unit must also have at most `CLADE_MAX` (default 12) sub-clades, so very inclusive clades
  with few known genera (Archaeplastida, Embryophyta) stay general until their subtree is filled in.

## 2026-11-21 — G10 relaxed: a genus may be drafted without a formation
- Owner request: write the pseudosuchian genera that PBDB has no occurrences for, and note the missing formation in `docs/NEXT.md`.
- G10 is now an error only for a genus with no formation **and** no curation note; with a note it is a consolidation (S) issue, so the
  entry may stay a draft. Items that exist still need `formation` and `country`. Such genera have no map point in Biota.
- The genus page shows "No formation is recorded for this genus yet". CLAUDE.md §4.1 updated to match.

## 2026-11-21 — Genus spotlight on the Index
- Owner request: a genus exploration tool beside the Index, like the "Species spotlight" column of prehistoric-wildlife.com: thumbnail of a reconstruction plus the genus name.
- Built in `site/js/index-search.js` and `atlas.css` (no new data, no build step): random genera with a full entry and a non-outdated `life` image, three at a time, following the Index filters, with a Shuffle button. CLAUDE.md §6 updated.

## 2026-11-21 — Genus spotlight stays in view
- Bug: below 1100 px wide the column was switched to a static row and scrolled away with the list; on short windows the fixed column was taller than the window and cut the last card.
- Now sticky down to 700 px (compact 170 px column below 1250 px), with a maximum height of the window.

## 2026-11-21 — Genus spotlight scrolls with the Index
- Owner: the spotlight must move together with the list when scrolling, not stay fixed on screen. The sticky behaviour added earlier the same day is removed (the column is ordinary page content).

## 2026-11-21 — Genus spotlight shows 25 cards
- Owner: 25 cards instead of 3, still scrolling with the list and not stretched to the whole page height. Fewer when the filters match fewer genera.

## 2026-11-21 — Census of genera per group
- Owner: no genus list in the atlas is complete (the backbone counts are only a lower bound, and PBDB lags behind new descriptions), so every clade
  has to be checked against PBDB **and** Wikipedia (and the recent literature) for new discoveries.
- New tool `scripts/fetch/census.py` + `.github/workflows/census.yml` + `data/census/sources.yaml` (see CLAUDE.md §7). It only reports; entries are
  never changed automatically. Tested offline (`tests/test_census.py`, also run by `check.yml`); the live APIs can only be reached from GitHub Actions.
- To be done per group: run the census before planning or finishing its volume. Pseudosuchia and Pterosauria first.

## 2026-11-21 — Sauropodomorpha genus volume started
- Owner request: create the Sauropodomorpha volume, using the new census (`data/raw/census/sauropodomorpha/census_2026-11-21.md`:
  449 valid PBDB genera, 291 missing from the atlas, 39 of them named since 2023, 138 more waiting in the backbone, 41 form taxa).
- `entries/sauropodomorpha/` created (`_volume.yaml`, root clade entry, empty `excluded.yaml`); size measure `length`, as for Pseudosuchia.
  The root node leaves `backbone.json`; its sub-clades and the backbone genera stay in the outline until their entries are written.
  No Sauropodomorpha clade entry existed in `entries/tree/clades`, so none moved.
- Raw material is requested through `data/raw/harvest_request.json` (all PBDB genera of Sauropodomorpha; `harvest.yml` runs on the branch).
  Ichno- and oogenera (flags I/F) are not entries. Genera that only Wikipedia lists (e.g. Musango, Yantaloong) and literature leads need a
  check against PBDB before they are drafted.

## 2026-11-21 — Sauropodomorpha: scope and clade entries
- Owner: one volume (449 valid PBDB genera, close enough to the ~300 limit); ichnogenera and oogenera (PBDB flags I/F) stay out;
  clade entries are written together with the genera.
- 20 clade entries written from the backbone's Sauropodomorpha clades (Wikipedia revisions and PBDB records of 2026-11-16): Sauropodiformes,
  Sauropoda, Diplodocoidea, Rebbachisauridae, Dicraeosauridae, Diplodocidae, Apatosaurinae, Diplodocinae, Macronaria, Brachiosauridae,
  Titanosauria, Lognkosauria, Saltasauroidea, Euhelopodidae, Mamenchisauridae, Turiasauria, Unaysauridae, Plateosauridae,
  Massospondylidae, Riojasauridae. They moved from the backbone to `entries/sauropodomorpha/clades`; compound ids lost their prefix and the
  parents of the backbone genera were remapped. Tree structure unchanged. Authorities that PBDB and Wikipedia attribute differently
  (Rebbachisauridae, Dicraeosauridae, Saltasauroidea, Mamenchisauridae) are noted in `curation.notes`.
- Clades seen only in Wikipedia categories (Massopoda, Saturnaliidae, Anchisauria) are not added yet (M6): they come with the genera that need them.

## 2026-11-22 — Image picker: always current, and a name that cannot be confused with site/index.html
- Bug: the triage page showed old entries and images. It reads `data/triage/<volume>.json`, which was regenerated only inside the
  triage-apply workflow, so it stayed at 96 entries / 149 images / 583 genera while the atlas had 506 / 728 / 609.
- `scripts/build.py` now also runs `scripts/triage_data.py` (every volume with a harvest), and `check.yml` fails when
  `data/triage/*.json` differs from the build — same rule as `site/data.json`. The Volume box lists the volumes found on the branch.
- `tools/triage/index.html` renamed to `tools/triage/atlas-image-picker.html` (two `index.html` files in the repository were easy to mix up).

## 2026-11-22 — Sauropodomorpha: first genus batch (Diplodocoidea) and size limits
- Batch 1 of the Sauropodomorpha volume: 16 genus entries (ai-draft) — Apatosaurus, Brontosaurus, Kaatedocus, Ardetosaurus, Barosaurus,
  Diplodocus, Galeamopus, Supersaurus, Tornieria, Haplocanthosaurus, Amargasaurus, Bajadasaurus, Brachytrachelopan, Dicraeosaurus,
  Suuwassea, Lingwulong. Their backbone nodes were removed; nine PBDB junior synonyms went to `excluded.yaml`.
- `scripts/validate.py` (G8): the upper limits of the size ranges were 25 m (any measure) and 20,000 kg, set for pterosaurs and
  pseudosuchians. They rejected normal sauropod values (Barosaurus 25–27 m, Supersaurus 33–39 m, Apatosaurus 16–22 t). New limits:
  length_m < 60 m (wingspan_m stays < 25 m) and mass_kg < 150,000 kg. Only a sanity bound; flagged for the owner to confirm.
- Kaatedocus and Lingwulong sit in Diplodocoidea as `incertae_sedis` (analyses disagree, M2); Diplodocus has no usable image among the harvested candidates.

## 2026-11-22 — Sauropodomorpha: batches 2 and 3
- 16 Macronaria/Turiasauria genera (batch 2) and 16 titanosaur and mamenchisaurid genera (batch 3: Lognkosauria, Mamenchisauridae, Saltasauroidea) written as ai-draft; PBDB junior synonyms added to `excluded.yaml`.
- Diplodocus images were taken from the contact sheet of its synonym Seismosaurus, because the harvest took only 15 loose Commons files for Diplodocus and missed the article pictures.
- Licence note: two Opisthocoelicaudia photos are CC BY-SA 3.0 PL (Polish port); `validate.py` rejects the string although CLAUDE.md allows CC BY-SA in any version. The photos were left out pending the owner's decision.

## 2026-11-22 — Harvest: image collection fixed
- Cause 1: the Wikipedia query `prop=images` (40 titles, `imlimit=max`) was read without following the API's `continue` token, so about 200 of 449 pages came back with no images. `harvest.py` now merges every answer through `mw_pages`.
- Cause 2: the Commons category step let the alphabetically first files of the main category fill the whole cap, so sub-categories (fossils, skulls, life restorations) were never reached. Each category now gets an equal share first, then the remaining slots are filled in order.
- Noise names (size comparisons, cladograms, maps, sculptures, stamps, posters, models, silhouettes) are dropped before the cap is counted.
- Existing raw data is not edited; a new harvest run regenerates `data/raw/sauropodomorpha/` and the contact sheets.

## 2026-11-22 — Sauropodomorpha: batches 4-8 and image revision
- New harvest adopted; extra images added to existing genus entries (clades have no image field, so they got none). 71 genera written in batches 4-8 as ai-draft, all images `unreviewed`.
- PBDB clades that the atlas has no entry for (e.g. Eutitanosauria, Lithostrotia) are mapped to the nearest atlas clade (Titanosauria); Histriasaurus is `incertae_sedis` within Rebbachisauridae (M2).
- Branch name: `entry/sauropodomorpha-1` already existed on GitHub with unrelated older history, so the work lives on `entry/sauropodomorpha-4-8`.

## 2026-11-22 — Sauropodomorpha: batches 9-13
- 69 more genera (Euhelopodidae, Mamenchisauridae, Rebbachisauridae, Titanosauria, Titanosauriformes, Brachiosauridae). PBDB clades with no atlas entry (Titanosauriformes) map to the nearest atlas clade (Macronaria).
- Ichnogenera and oogenera (PBDB flags I/F) stay out of the volume; names with no usable Wikipedia article wait for a new harvest.
