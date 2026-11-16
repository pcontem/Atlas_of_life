# Atlas of Life — instructions for Claude

Read this file in full before any change. It is the project's contract: if a request conflicts
with it, say so and ask before going ahead.

## 1. What this project is

A visual, fully sourced encyclopedia of **life on Earth** (no fictional or built worlds), organised
as a tree of life. It is built volume by volume. **Pterosauria is the pilot volume.**

**Current phase: consolidating Pterosauria.** No new volume (e.g. Dinosauria) is started until
`python3 scripts/validate.py --strict` passes with zero issues for Pterosauria. Work in this phase
fixes entries, sources, images and the site; it does not add groups.

The website language is **English**. Conversation with the owner may be in Portuguese.
The word for a page about a taxon is **entry** (never "ficha").

## 2. Repository map

| Path | What it is | Edit by hand? |
|---|---|---|
| `entries/<volume>/genera/<Genus>.yaml` | one genus entry | **yes — source of truth** |
| `entries/<volume>/clades/<id>.yaml` | one clade entry | **yes — source of truth** |
| `entries/<volume>/excluded.yaml` | names left out (nomina dubia etc.) and why | yes |
| `entries/formations/<id>.yaml` | one geological formation (a place in Biota mode), shared by all volumes | **yes** (prose); PBDB fields via script |
| `entries/home.yaml` | the start page ("Life on Earth"): intro text, sources, group pictures with credits | yes |
| `entries/<volume>/_volume.yaml` | volume root clade and where it attaches to the tree | rarely |
| `data/tree/backbone.json` | tree-of-life nodes that are not entries yet | rarely |
| `data/raw/` | downloads from PBDB, Wikipedia, Commons, PhyloPic (provenance); `timescale/` = ICS chart v2024/12 via PBDB | **never** |
| `scripts/build.py` | entries → `site/data.json` + `site/life.json` | code |
| `scripts/validate.py` | checks the rules in §4 | code |
| `scripts/fmt.py` | canonical YAML layout | code |
| `scripts/paleo_points.py` | keeps the reconstructed formation positions in step with the entries | code |
| `scripts/make_formations.py` | creates/refreshes formation entries from genus entries + PBDB collections; links genera to them | code |
| `data/raw/paleomaps/` | Merdith et al. 2021 coastlines per time step + reconstructed formation positions (GPlates Web Service) | **never** |
| `scripts/legacy/` | prototype code, kept for history | never |
| `site/` | the static website (`index.html`, `css/`, `js/`, `vendor/`) | code |
| `site/data.json`, `site/life.json`, `site/g/*.json`, `site/paleo/*.json` | **generated** by build.py: the index every view loads, the tree, one full genus entry per file (loaded on demand), the maps | **never** |
| `site/img/`, `site/sil/` | images and silhouettes — **not in main**: they live on the branch `media` (one commit, replaced on each update) | via `scripts/media.py` |
| `media/manifest.json` | path, size, sha256 and volume of every media file (the validator checks against it) | via `scripts/media.py` |
| `scripts/media.py` | `pull` the images into site/, `push` new ones (makes 240-px thumbnails, updates the manifest) | code |
| `scripts/fetch/` | `pbdb.py`, `gplates.py`: download fresh PBDB and GPlates data (run by the data-refresh workflow) | code |
| `tests/screenshots.py` | visual smoke test of every view | code |
| `docs/CONSOLIDATION.md` | generated to-do list (`validate.py --report`) | never |
| `docs/DECISIONS.md` | log of project decisions and why | yes, append only |

Site code, one file per view: `js/core.js` (state, routing), `sidebar.js`, `entry-genus.js`
(incl. size diagram), `entry-clade.js`, `timeline.js`, `index-search.js`, `pages.js`
(excluded, about), `tree-of-life.js`, `biota.js` (Biota mode), `entry-formation.js` (formation entries), `home.js` (start page), `main.js` (start-up, must load last). Plain scripts sharing
global scope, no bundler.

## 3. Golden rules

1. **Every fact has a source** listed in the entry's `sources`. If you cannot source it, leave it out.
2. **Never invent.** Not a date, a measurement, a specimen number, an author or a type species.
   If a value is uncertain, write that in the matching `note` field and add a curation note.
3. **No AI-generated images**, ever. Only photographs and published, credited paleoart (§4.4).
4. **Own words.** Paraphrase sources; never copy sentences. Quote at most a short phrase, in quotes.
5. **The genus is the unit.** One entry per valid genus; species are listed inside it.
6. **Only valid taxa.** Nomina dubia, nuda and inquirenda go to
   `excluded.yaml`, never into the tree.
7. **Generated files are not edited.** Change the entry, then run `build.py`.
8. **Small steps.** One request = one focused change = one commit.

## 4. Entry rules

Rule codes match the messages of `scripts/validate.py`.
**E** = error (must pass on every commit). **S** = consolidation rule (may fail while an entry is a
`draft`; must pass for the volume to be consolidated). **M** = manual rule (not checkable by the
script; check it yourself when you touch the entry).

### 4.1 Genus entry — fields and rules

```yaml
name: Pteranodon                  # G1 E  = file name; unique in the atlas; not in excluded.yaml
rank: genus                       # G1 E
parent: pteranodontia             # G2 E  id of the most exclusive clade with consensus support
incertae_sedis: false             # G3 E  true when placement below `parent` is disputed
placement_note: ''                # G3 E  required if incertae_sedis: which analyses disagree
authority: Marsh 1876             # G4 E  "Author(s) year", as in PBDB / original description
type_species: Pteranodon longiceps  # G5 E belongs to the genus · S: in species list and verified
type_species_note: ''             # G5    how it was established if not from PBDB; empty = PBDB
summary: One sentence.            # G7 E  non-empty · S: one sentence, ends with ".", ≤170 chars
size:
  wingspan_m: [3.8, 7.6]          # G8 E  [min, max] in metres (same value twice if one estimate)
  note: Females about 3.8 m; ...  # G8 S  required when wingspan_m is null (say why unknown)
age:
  first_ma: 89.8                  # G9 E  first_ma ≥ last_ma > 0
  last_ma: 72.2
  early_interval: Coniacian       # G9 E  ICS stage/age names
  late_interval: Campanian
  pbdb_occurrences: 43            # G9 E  if 0, age.note must say where the age comes from
  note: ''
species:                          # G6 S  at least the type species
- name: Pteranodon longiceps      # G6 E  starts with the genus name
  authority: (Marsh 1876)         # G6 E  has a year; parentheses = original genus differed
  first_ma: 85.7                  #       may be null
  last_ma: 72.2
  interval: Santonian–Campanian
  reference: original description
formations:                       # G10 E at least one; each with formation and country
- formation: Niobrara
  group: Colorado
  members: [Smoky Hill Chalk]
  country: United States
  regions: [Kansas]
  interval: Coniacian–Santonian
  occurrences: 25                 #       PBDB occurrence count, null if not from PBDB
  ma: [83.6, 89.8]
fossil_material:                  # G11 E holotype and material non-empty
  holotype: YPM 1117 skull (P. longiceps) — Smoky Hill Chalk, Niobrara Formation, Kansas.
  material: About 1,200 specimens, ...
  completeness: multiple          # G11 E complete | near-complete | partial | fragmentary | multiple
  exceptional: ''                 #       soft tissue, gut contents, eggs... ('' if none)
biology: Diet, locomotion, ...    # G12 E non-empty; only what the sources support
images: [...]                     # §4.4
silhouette: {...}                 # §4.4
sources: [...]                    # §4.5
curation:                         # §4.6
  status: draft
  origin: ai-draft
  checked_by: ''
  checked_on: ''
  notes: []
  reviews: []
```

Completeness scale (G11): **complete** = whole skeleton incl. skull; **near-complete** = most of
skeleton incl. skull; **partial** = substantial part of one individual; **fragmentary** = isolated
bones or a few pieces; **multiple** = many individuals that together cover the skeleton.

Manual rules for genera:
- **M1 Validity.** A genus is valid if PBDB or the most recent revision treats it as valid. If recent
  literature sinks it, move it to `excluded.yaml` (status `junior synonym` or `nomen dubium`) with
  the reference.
- **M2 Placement.** `parent` is the most exclusive clade on which recent analyses agree. If they
  disagree, place the genus in the deepest clade they share, set `incertae_sedis: true` and explain
  in `placement_note` (name the conflicting analyses).
- **M3 Species list.** Only valid species of the genus. Species moved to another genus are not
  listed here (the other genus lists them).
- **M4 Size.** Pterosaurs use wingspan. Give the range of adult estimates from the sources;
  `size.note` says which specimens/sexes/methods. Juveniles are not used for the range.
- **M5 Ages.** From PBDB occurrences when possible. Otherwise use the ICS boundaries of the stage
  named in the description and say so in `age.note`.

### 4.2 Clade entry

```yaml
id: tapejaridae          # C1 E  lowercase = file name
name: Tapejaridae
rank: clade              # C1 E
taxon_rank: family       # C4 E  Linnaean rank from PBDB/literature, or "unranked clade"
taxon_rank_source: ...   # C4 E
parent: azhdarchoidea    # C1 E  clade of the same volume; null only for the volume root
wikipedia: Tapejaridae   # article title used as a source (may differ from the clade name)
summary: One sentence.   # C2 E
diagnosis:               # C2 E  at least two features that define the group
- ...
notes: Classification debates, size range, notable members.
sources: [...]           # S1 E, S2 S (needs primary literature)
curation: {...}          # Q1
```
- **C3 E** Parent chains reach the root without loops; every clade contains at least one genus.
- **C4 E** `taxon_rank` (family, superfamily, suborder, order… or `unranked clade`) with
  `taxon_rank_source` (PBDB taxonomy or a publication). Used by the Timeline resolution menu.
- **M6** Clades are only created when needed to place genera with consensus; no empty ranks.

### 4.3 Excluded names (`excluded.yaml`)

`name`, `author`, `status` (X1 E: `nomen dubium | nomen nudum | nomen inquirendum |
junior synonym`), `ref` (the publication that established the status) and/or `source`,
`parent` (X2 E: the clade id or genus of the volume where the name belongs — the genus for a
species of a valid genus, otherwise the deepest atlas group among its PBDB parent taxa) and
`placement` (how the parent was chosen).
Only real, published names whose validity is rejected go here. Misspellings, duplicates and
vernacular forms are simply corrected in the entries and **not** listed.

### 4.4 Images

Each genus has a **gallery**: any number of images per kind up to 8 (I1 E), never the same
Commons file twice. Kinds: `life` (life restoration), `fossil` (photo of the actual fossil, a
cast or a mount, or a scientific figure of the specimen), `skeletal` (skeletal reconstruction).
The site shows one tab per kind with thumbnails. Not accepted at all: museum models and
sculptures, theme-park statues, stamps, posters, pre-1950 restorations, maps, faunal or size
comparison charts, AI-generated images, and photos of other taxa.

- **I2 E** Every image has `url`, `page`, `artist`, `license`, `caption`. `page` is the Wikimedia
  Commons file page, or `https://doi.org/<doi>` for a figure from an open-access article (then
  `file` = `<PMCID> <figure label>`, `artist` = the article's authors with journal and year, the
  caption starts with the figure label and short citation, and the article is also listed in the
  genus `sources` as `literature`). If Commons names no author, write `Unknown (...)` and why.
- **I3 E** Allowed licences: CC0, public domain, CC BY, CC BY-SA (any version).
  Non-commercial (CC BY-NC*) is tolerated only for PhyloPic silhouettes and is an **S** issue to
  replace. No-derivatives (ND) and "all rights reserved" are never allowed.
- **I4** `review`: `unreviewed | accepted | outdated`. **S:** every `life` image must be `accepted`.
  A life restoration is `accepted` only when it matches current knowledge: pycnofibres present;
  wing membrane reaching the ankle; crest, teeth and skull proportions consistent with the known
  material; no features contradicted by the sources. Claude may propose a verdict with reasons;
  the owner decides. Mark replaced or contradicted art `outdated` and look for a better one.
- **I5 E** The image is in the media store: its `local` path under `site/` is listed in
  `media/manifest.json` (gallery images:
  `img/gallery/<Genus>_<nnn>.webp`, max 800 px, or `<Genus>_oa_<n>.webp`, max 1000 px for
  article figures with small labels; WebP) or, for the original main images,
  `site/img/<Genus>_<kind>.webp`; silhouettes in `site/sil/<phylopic-uuid>.webp`; every image also
  gets a 240-px copy in `site/img/thumb/…` for lists, cards and maps). The site never loads remote
  images. **Adding images:** `python3 scripts/media.py pull` (so site/ has all current images), put
  the new files in site/img, reference them in the entry, `python3 scripts/media.py push` (thumbnails,
  manifest, media branch), then commit the entry and `media/manifest.json` as usual.
- Finding images: Commons categories `Category:<Genus>` and its sub-categories ("… fossils",
  "… life restorations", "… skeletal mounts", "… skulls"); every candidate is checked visually
  before it is added (keep a contact sheet), and gets `review: unreviewed`. Second source:
  figures of CC BY / CC0 open-access articles found through Europe PMC (article licence checked
  per article; captions screened to drop phylogenies, maps, charts, CT renderings, schematic
  comparisons and figures of other taxa).
- **I6 S** Every genus has at least one image.
- **I7 E** `external`: artwork that may not be copied (e.g. DeviantArt, ArtStation, personal
  sites, journal figures under restrictive licences) is only **linked**, never downloaded:
  `kind`, `title`, `artist`, `site`, `url` (https, the artwork's own page), `accessed`
  (YYYY-MM-DD), `review` (same scale as I4). Max 6 per genus; shown under the gallery as
  "More reconstructions elsewhere". No permission requests: anything that would need one is a link.
- Free sources besides Commons (copy allowed, licence checked per item and recorded): figures of
  open-access papers under CC BY (PLOS ONE, PeerJ, Scientific Reports, Royal Society Open Science,
  Acta Palaeontologica Polonica, Fossil Record, Frontiers…; cite the paper in `caption`),
  Smithsonian Open Access (CC0), Biodiversity Heritage Library (public domain, fossil plates
  only), Flickr/Openverse items under CC BY or CC BY-SA, PhyloPic.
- Silhouettes come from PhyloPic, with `attribution`, `license`, `page`; `genus_level: false`
  means it depicts a relative (the site says so). Size diagram: a 1.8 m human beside a schematic
  pterosaur scaled to the maximum wingspan.

### 4.5 Sources

Each item: `kind`, `text` (full citation), `url` (optional).
- `original` — the publication that named the taxon. **S2:** every genus has one.
- `literature` — redescriptions, phylogenies, size or biology papers.
- `database` — PBDB (ages, formations, occurrences, species).
- `encyclopedia` — English Wikipedia; **S3 E:** always a fixed revision (`...&oldid=<rev>`).
- **S1 E** at least one source; kinds from the list; text non-empty.
- **S2 S** at least one `original` or `literature` source (Wikipedia alone is not enough).
- **M7** Prefer the most recent revision of a taxon. When sources disagree, say so in the relevant
  `note` and cite both.

### 4.6 Curation status

```yaml
curation:
  status: draft          # draft | checked
  origin: ai-draft       # Q2 E  ai-draft | human — who wrote the first version
  checked_by: ''
  checked_on: ''
  notes: []
  reviews:               # Q3 E  one item per review (issue "Submit a review" → PR)
  - by: Jane Doe         #       name; on = YYYY-MM-DD
    on: 2026-12-01
    scope: [all]         #       all | identity, classification, age, formations, size,
                         #       fossil_material, biology, images, sources, text
    verdict: accepted    #       accepted | changes | rejected
    notes: ''
    confirmed_by: ''     #       a second person, never the same as `by`
    confirmed_on: ''     #       required when confirmed_by is set
```
- **Two-person rule (Q1 E).** `checked` requires a review with `scope: [all]`, `verdict: accepted`,
  confirmed by a different person; `checked_by` = that review's `by`; `notes` empty; all **S** rules
  pass. Nobody confirms their own review.
- Anything doubtful you notice goes into `curation.notes` as a short to-do — never silently.
- Claude never sets `checked`, never records a review or confirmation in its own name, and never
  approves a pull request. Entries Claude drafts get `origin: ai-draft`.
- Contribution process, roles and audits: [`CONTRIBUTING.md`](CONTRIBUTING.md). GitHub side: issue
  forms in `.github/ISSUE_TEMPLATE/` (correction, review, image, new genus), the PR template,
  `CODEOWNERS`, branch protection on `main` (one approval by someone other than the author, stale
  approvals dismissed, `check` must pass), monthly `audit.yml` (random sample of checked entries,
  `scripts/audit.py`).

### 4.7 Formation entries (`entries/formations/<id>.yaml`)

A formation is a place where atlas taxa were found; Biota mode shows it on the map of its time.
Every formation item of a genus entry carries `id:` = the formation entry it belongs to.

```yaml
id: romualdo-brazil       # F1 E  = file name (slug of name + country); rank: formation; name; country
name: Romualdo
rank: formation
group: Santana
country: Brazil
regions: [Ceará, Pernambuco]
location:                 # F2 E  degrees; basis says how the point was chosen (PBDB collections)
  lat: -7.2
  lng: -39.576
  basis: median of 4 PBDB collections that yielded the atlas genera
age:                      # F2 E  first_ma ≥ last_ma ≥ 0; span of the dated beds with atlas taxa
  first_ma: 119.57
  last_ma: 113.2
  note: ...
environment: [lagoonal/restricted shallow subtidal]   # PBDB terms, most frequent first
lithology: [limestone, shale]                          # PBDB terms
pbdb_collections: ['12816', ...]
summary: One sentence.    # F5 S  what the formation is
paleoenvironment: ...     # F5 S  setting, climate, notable biota — own words, sourced
sources: [...]            # S1 E; S2 S needs literature, not only PBDB
curation: {...}           # Q1
```
- **F3 E** every genus formation item links an existing formation entry, and every formation is
  listed by at least one genus. Run `python3 scripts/make_formations.py` after adding formations to
  a genus: it creates the entry, fills the PBDB fields and the genus `id` links, and never touches
  `summary`, `paleoenvironment`, extra sources or curation.
- **F4 E** the formation's location has palaeo-positions in `data/raw/paleomaps/formation_points.json`
  (refresh them through the GPlates Web Service when a location changes; see §7).
- **Merging units of the same formation** (`scripts/make_formations.py`, every merge is written in
  the entry's `includes` and shown as "Units grouped here"): other names of the same unit
  (`ALIASES`, each with its reason/source: Posidonienschiefer → Posidonia Shale; Calcari di Zorzino →
  Zorzino Limestone; Solnhofen → Altmühltal Formation, Solnhofen Member); a unit PBDB records as a
  **member** of another formation goes into that formation (Alum Shale → Whitby Mudstone, Sharon
  Springs → Pierre Shale). Beds without a formation are placed **per PBDB collection**: (1) member
  or collection name = a PBDB member of a formation → that formation; (2) collection name contains a
  formation's name (same country) → that formation (Nusplingen quarry → Nusplingen Limestone);
  (3) PBDB gives a group → one entry "<Group> Group (beds not assigned to a formation)" per
  country; (4) otherwise one "Unnamed beds, <site>" entry per site (0.25° cell, 5-Myr age bucket).
  A genus item may then link several entries (`id: [a, b]`). Different formations are never merged.
- After changing formations run `python3 scripts/paleo_points.py`: it reuses known palaeo-positions,
  prunes unused ones and lists what still has to be fetched from GPlates (then merge the results
  with `python3 scripts/paleo_points.py results.json`).
- Biota lists only taxa with atlas entries; no PBDB faunal lists.

### 4.8 Tree names

- **L1 S** Everything in the tree backbone — node names and notes — is in English (the Portuguese
  glosses of the first prototype were translated on 2026-11-16; the validator flags any that return).

### 4.9 Start page (`entries/home.yaml`)

`title`, `lead`, `intro` (paragraphs in our own words), `hero` and `groups` (each `node` = a tree node
id, `label`, `image` with `file`, `page`, `artist`, `license`, `license_url`, `caption`, `local`),
`sources`. **H1 E** title and intro; **H2 E** every image complete, licence allowed (§4.4 I3) and in
the media store; **H3 E** every group node exists in the tree. Facts in the text follow §3 like any
entry (sources: fixed Wikipedia revisions or literature).

## 5. Workflow: from a request to a commit

Every request follows these steps. Do not skip validation or the visual check.

1. **Understand.** Restate the request in one line. If it touches §3 or §4, say which rules apply.
   If it is ambiguous or conflicts with this file, ask before editing.
2. **Branch.** `git switch -c <type>/<short-name>` (`entry/`, `fix/`, `site/`, `data/`, `docs/`).
3. **Change the source, not the output.**
   - Content → `entries/**.yaml` (then `python3 scripts/fmt.py`).
   - Website → `site/js/*.js`, `site/css/atlas.css`, `site/index.html`.
   - Never `site/data.json` / `site/life.json` / `data/raw/`.
4. **Build.** `python3 scripts/build.py`
5. **Validate.** `python3 scripts/validate.py` → must print `0 error(s)`.
   For consolidation work also run `--strict` and confirm the count went down.
6. **Look.** `python3 tests/screenshots.py [Genus]` and open the PNGs in `tests/out/` for the views
   you touched. For interactive changes, also test the interaction (click, search, switch view).
7. **Review the diff.** `git diff --stat` and `git diff` — only intended files changed.
8. **Commit.** One focused commit, message in English, imperative mood:
   ```
   <What changed, ≤60 chars>

   <Why, and anything a reviewer should know: sources used, rules affected.>
   ```
   Include `site/data.json` and `site/life.json` when the build changed them.
9. **Report.** Tell the owner what changed, what was checked, and anything left open
   (add it to `curation.notes` or `docs/DECISIONS.md`).
10. **Merge / publish.** After the owner is happy: push the branch, open a pull request, merge into
    `main`. GitHub Actions re-runs fmt/validate/build on every push (`.github/workflows/check.yml`)
    and publishes `site/` to GitHub Pages from `main` (`pages.yml`).
    `python3 scripts/validate.py --report` refreshes `docs/CONSOLIDATION.md` (commit it).

New project decisions (a rule changed, a licence policy, a UI convention) are appended to
`docs/DECISIONS.md` in the same commit, and this file is updated to match.

## 6. Website conventions (keep them when changing the site)

- Three modes in the header, on the right: **Encyclopedia**, **Tree of life** and **Biota** (the tree
  is an outline of the classification, not a true cladogram, so never call it "cladogram"). The
  Encyclopedia's sub-tabs sit **apart from the mode selector**, in their own bar under the header
  (shown only in Encyclopedia mode): **Index, Entry, Timeline, Formations, About & excluded names**.
  The last is one tab with two parts, switched by pills at the top: "About & sources" (`#about`)
  and "Excluded names" (`#excluded`). Clicking the title returns to the start page.
- **Start page** = the root of the tree ("Life", `#vida`): "Life on Earth" — lead, a short sourced
  introduction, a hero picture, links to the three modes, counts, and a grid of pictures of very
  different groups (bacteria to mammals); each card opens that group in the tree. Sources and
  picture credits at the bottom. Content from `entries/home.yaml`.
- **One selection shared by all views** (`cur` in `core.js`): the entry being read is the node
  highlighted in the Tree of life and the focus of the Timeline, and vice versa. Switching mode keeps it.
- Tree of life: **Linear / Radial** layout switch (same selection and open groups). The radial
  view is drawn around one group (the selected clade, or the group of a selected genus; Search
  re-centres it; "↑ Parent group" widens it; Root shows the whole tree). Radial drawing rules (circular tree, as
  in published circular phylogenies): every internal group sits on the ring of its level (equal
  spacing, dashed guide rings); all tips (genera and closed groups) sit on the outer circle; each
  branch leaves its parent along the parent's ring, then runs straight out; coloured sectors behind
  the tip labels give every tip the colour of the **least inclusive open group** that contains it
  (open sub-groups are drawn first so each group's own tips are contiguous), named outside;
  single click = select; double click = open/close a clade; **Search** (ranked
  suggestions, clades first, arrows + Enter) opens all sub-clades of the found clade, collapses the
  rest, selects it and centres the whole sub-tree on screen; **Prune** closes everything
  except the path to the selected node. An entry is opened from the top bar (Encyclopedia) or by
  double-clicking the info card of the selected node; double-clicking a tree node never opens it.
- Timeline: follows the selected entry. Two modes, **Ranges** and **Diversity**, plus a
  **Resolution** menu by taxonomic rank (Genus by default, then Family, Superfamily, Suborder…,
  only the ranks present below the selected group; ranks come from `taxon_rank` in the clade
  entries). Ranges draws one bar per unit of that rank (genera outside any unit of that rank are
  kept), in a vivid palette, coloured by the direct subdivision it belongs to, with a legend.
  Diversity draws one spindle for the selected group: thickness = number of units of that
  resolution known at each moment (range-through), scale on the left; dashed **ghost lineages**
  only inside the group's own range — stretches between its first and last record with no genus
  on record (no comparison with sister groups: the classification is not resolved into binary
  splits). Time units come only from the ICS chart in `D.timescale` (Hadean → Holocene); the main
  axis is linear with two rows chosen by window length (eon/era, era/period, period/epoch or
  epoch/age); the "Earth history" strip above is **logarithmic** (log of age + 50 Myr, so the
  Cenozoic stays smaller than the Mesozoic) with eon/era/period rows and marks where the window
  lies. "↑ Parent group" goes up; clicking a group row goes down into it. Click a
  row = select; double-click a genus = open its entry.
  Entry pages use the same units for their small time bar. Never hard-code period boundaries.
- Clade pages: genera sitting directly in the clade are split into "Genera placed directly here"
  and **"Incertae sedis"** (those with `incertae_sedis: true`).
- Excluded names: follows the selected entry and lists only the names placed **directly** in it,
  plus the sub-groups that hold more (with counts) and a "↑ Parent group" button.
- Index: A–Z with **stackable filters**: pick **Search by** (Name / Clade / Time), type, press
  Enter or "+ Add filter" to keep it as a chip, then add another; entries must match every chip
  (and the text being typed). Time = an ICS interval name or an age/range in Ma, matched when the
  stratigraphic range overlaps it. A type filter (Full entries / Clades / Genera / All) applies on top. Sidebar search with keyboard support.
- **Biota** (third mode in the top bar, `#biota`, deep link `#biota/<formation id>`): a **search
  box** (genera with formations on the map, and formations; arrows + Enter): a formation jumps to the
  middle of its record and opens its card; a genus becomes the selected entry (its formations get the
  dashed ring), the map goes to the time closest to the middle of its range at which one of its
  formations is shown, and that formation's card opens. A time slider
  (oldest left, present right, on a gently non-linear scale — position = 1 − (age/1000 Ma)^0.6 — so
  recent times get more room; ◀ ▶ step one map, arrow keys, an ICS era/period strip on the same
  scale that can be clicked,
  "⌖ Selected entry" jumps to the selected entry's time, "Next formations" to the next older time with
  new formations). The map (Equal Earth projection) shows the continents of that time from the
  Merdith et al. 2021 plate model (coastlines every 5 Myr to 540 Ma, every 20 Myr to 1000 Ma) and the
  formations whose dated beds overlap the time ± 2.5 Myr, placed at their reconstructed positions,
  coloured by environment (marine, coastal & lagoon, lake, river & land), sized by the number of
  atlas genera; formations of the selected entry get a dashed ring. Points closer than ~16 px on
  screen are drawn as one **cluster** marker with a count (recomputed after each zoom): hover lists
  them, click lists them beside the map, double-click zooms in ×4 towards them. **Zoom** (scroll, drag to pan,
  + / − / ⟲ buttons with the current factor shown; + zooms towards the highlighted formation; up to
  ×96; at the deepest zoom, points that still overlap — same or neighbouring sites — are fanned out
  around their spot with thin leader lines) is kept while the time
  changes, and points keep their size on screen. Hover = name; **click** = the
  formation's card beside the map (age, PBDB environment and rock types, palaeolatitude,
  palaeoenvironment text, the atlas taxa found there — click = select, double-click = open entry —
  and sources); **double-click** = the formation's encyclopedia entry.
- **Formations** section (`#formations`, Encyclopedia sub-tab): every formation entry in a table
  (name, group, country/region, ICS age range, atlas taxa, Biota link), filters stackable: text
  (name/country/region/group), environment chips, period menu, "only those of the selected entry";
  sort by oldest/youngest (grouped by period), name or number of genera; a row opens the entry.
- **Formation entries** (`#formation/<id>`, Encyclopedia mode, Formations tab): name, group, country,
  age, environment badge, summary; cards for palaeoenvironment, atlas taxa found there (grouped by
  clade), sources; time range, a small map of where it lay (mid time of its record) with
  "Explore in Biota", and the PBDB geology. Genus entries link each formation to its entry. Longitudes in the model are not constrained (palaeomagnetic frame): say so, never
  interpret them.
- No group gets special treatment in code because it is the pilot (no hard-coded "pterosauria"
  defaults); the start page is the root of the tree.
- **Review status** on every entry page (genus, clade, formation): a badge next to the title —
  "✓ Checked · <by> & <confirmed_by>", "AI draft · not yet reviewed" or "Draft · not yet reviewed" —
  and a **Review & contribute** card after Sources with the review history and buttons that open
  pre-filled GitHub issue forms (Suggest a correction, Submit a review, Review or suggest an image
  [genera only], **Edit this entry** → the entry's YAML in GitHub's web editor, which forks and opens
  a pull request; path from `cur.src`, How reviewing works → CONTRIBUTING.md). The issue forms only
  work once they are on `main` (GitHub reads them from the default branch).
- Images and libraries are served locally (no remote requests at runtime).
- **Loading:** `data.json` is a light index (clades, one short record per genus with its
  representative image, formations, timescale); the full genus entry (`g/<Genus>.json`) is fetched
  when its page is opened. Views other than the genus entry must work from the index alone. Lists,
  cards, the tree and maps use the 240-px thumbnails (`thumbSrc`); only the gallery's main image uses
  the full file.
- **Taxa of a place** (Biota card, formation entry) are grouped by volume and then by parent clade in
  collapsible groups; up to 12 taxa everything is open, above that the clade groups start closed with
  their count and first names.

## 7. Getting data from the web

The build needs no network. Raw downloads live in `data/raw/` and are refreshed only on purpose.
In the original environment the shell could not reach external sites; downloads were made in a
browser with same-origin `fetch` on each site (scripts in `scripts/legacy/fetch/`). APIs used:
PBDB `data1.2` (taxa, occurrences, refs), English Wikipedia API (extracts, revisions, images),
Wikimedia Commons `imageinfo` (licences, authors), PhyloPic API (silhouettes), PBDB `colls/list`
(formation coordinates, environment, lithology → `data/raw/<volume>/pbdb_colls.json`), GPlates Web
Service `reconstruct/coastlines` and `reconstruct/reconstruct_points` with `model=MERDITH2021`
(coastlines simplified in the browser: rings < 1 deg² dropped, Douglas–Peucker 0.3°, coordinates
×10 as integers → `data/raw/paleomaps/`).
Record the download date in the source text when you add new data.

**Automated refresh** (`.github/workflows/data-refresh.yml`, on demand and monthly — GitHub Actions
can reach the web even when the maintainer's session cannot): `scripts/fetch/pbdb.py` re-downloads
each volume's PBDB occurrences and collections (same file layouts), `make_formations.py` updates the
formation entries, `scripts/fetch/gplates.py` fetches missing palaeo-positions, then fmt/build/
validate, and a pull request `data/pbdb-refresh` is opened listing PBDB genera not yet in the atlas
and the validation result. Genus entries are never changed automatically. One-time setting:
Settings → Actions → General → "Allow GitHub Actions to create and approve pull requests".
The Pages workflow runs `scripts/media.py pull` before publishing.
