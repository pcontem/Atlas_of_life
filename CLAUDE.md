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
| `entries/<volume>/_volume.yaml` | volume root clade and where it attaches to the tree | rarely |
| `data/tree/backbone.json` | tree-of-life nodes that are not entries yet | rarely |
| `data/raw/` | downloads from PBDB, Wikipedia, Commons, PhyloPic (provenance); `timescale/` = ICS chart v2024/12 via PBDB | **never** |
| `scripts/build.py` | entries → `site/data.json` + `site/life.json` | code |
| `scripts/validate.py` | checks the rules in §4 | code |
| `scripts/fmt.py` | canonical YAML layout | code |
| `scripts/legacy/` | prototype code, kept for history | never |
| `site/` | the static website (`index.html`, `css/`, `js/`, `img/`, `sil/`, `vendor/`) | code |
| `site/data.json`, `site/life.json` | **generated** by build.py | **never** |
| `tests/screenshots.py` | visual smoke test of every view | code |
| `docs/CONSOLIDATION.md` | generated to-do list (`validate.py --report`) | never |
| `docs/DECISIONS.md` | log of project decisions and why | yes, append only |

Site code, one file per view: `js/core.js` (state, routing), `sidebar.js`, `entry-genus.js`
(incl. size diagram), `entry-clade.js`, `timeline.js`, `index-search.js`, `pages.js`
(excluded, about), `tree-of-life.js`, `main.js` (start-up, must load last). Plain scripts sharing
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
  checked_by: ''
  checked_on: ''
  notes: []
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

- **I2 E** Every image has `url`, `page` (the Wikimedia Commons file page), `artist`, `license`,
  `caption`. If Commons names no author, write `Unknown (...)` and why.
- **I3 E** Allowed licences: CC0, public domain, CC BY, CC BY-SA (any version).
  Non-commercial (CC BY-NC*) is tolerated only for PhyloPic silhouettes and is an **S** issue to
  replace. No-derivatives (ND) and "all rights reserved" are never allowed.
- **I4** `review`: `unreviewed | accepted | outdated`. **S:** every `life` image must be `accepted`.
  A life restoration is `accepted` only when it matches current knowledge: pycnofibres present;
  wing membrane reaching the ankle; crest, teeth and skull proportions consistent with the known
  material; no features contradicted by the sources. Claude may propose a verdict with reasons;
  the owner decides. Mark replaced or contradicted art `outdated` and look for a better one.
- **I5 E** The local copy exists: the image's `local` path under `site/` (gallery images:
  `img/gallery/<Genus>_<nnn>.webp`, max 800 px, WebP) or, for the original main images,
  `site/img/<Genus>_<kind>.webp`; silhouettes in `site/sil/<phylopic-uuid>.webp`. The site never
  loads remote images.
- Finding images: Commons categories `Category:<Genus>` and its sub-categories ("… fossils",
  "… life restorations", "… skeletal mounts", "… skulls"); every candidate is checked visually
  before it is added (keep a contact sheet), and gets `review: unreviewed`.
- **I6 S** Every genus has at least one image.
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

`curation.status`: `draft` (default) or `checked`.
- `checked` means someone went through every field against the cited sources, all its **S** rules
  pass and `notes` is empty. Fill `checked_by` (name) and `checked_on` (YYYY-MM-DD). **Q1.**
- Anything doubtful you notice goes into `curation.notes` as a short to-do — never silently.
- Claude may set `checked` only when the owner asks for it in the request.

### 4.7 Tree names

- **L1 S** Names of tree nodes shown on the way to a volume are in English (the backbone still has
  some Portuguese glosses such as "(linhagem das aves)").

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

- Two modes in the top bar: **Encyclopedia** and **Tree of life** (it is an outline of the
  classification, not a true cladogram, so never call it "cladogram" in the interface).
  Encyclopedia sub-tabs: **Index, Entry, Timeline, Excluded names, About & sources** (shown only in Encyclopedia mode; Encyclopedia
  stays highlighted on its sub-tabs).
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
- No group gets special treatment in code because it is the pilot (no hard-coded "pterosauria"
  defaults); the start page is the root of the tree.
- Images and libraries are served locally (no remote requests at runtime).

## 7. Getting data from the web

The build needs no network. Raw downloads live in `data/raw/` and are refreshed only on purpose.
In the original environment the shell could not reach external sites; downloads were made in a
browser with same-origin `fetch` on each site (scripts in `scripts/legacy/fetch/`). APIs used:
PBDB `data1.2` (taxa, occurrences, refs), English Wikipedia API (extracts, revisions, images),
Wikimedia Commons `imageinfo` (licences, authors), PhyloPic API (silhouettes).
Record the download date in the source text when you add new data.
