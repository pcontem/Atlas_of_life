# Next steps — Avialae (Mesozoic birds outside the crown)

Done (2026-11-27): census (2 runs, group `avialae`); scope decided (one volume, no crown birds, no form taxa); harvest of the 215
Mesozoic genera with papers, contact sheets and the Wikipedia-only genera (`wiki_group: avialae`); clade sources for 33 candidate
clades (`data/raw/tree/clade_sources_2026-11-27_avialae.json`); volume skeleton (`_volume.yaml`, root clade Avialae,
Archaeopterygidae).

To do, in order:
- Clade structure from recent cladograms (Wikipedia revisions in the clade sources; Benito et al. 2026 review of avian systematics)
  checked against PBDB: Jeholornithiformes, Omnivoropterygidae, Pygostylia, Confuciusornithidae, Ornithothoraces, Enantiornithes
  and its families, Ornithuromorpha, Hongshanornithidae, Songlingornithidae, Gansuidae, Ornithurae, Hesperornithes,
  Ichthyornithes… (M6: only clades needed to place genera); changes in `docs/TREE_REVIEW.md`. Decide where the backbone node
  Aves (crown) hangs (inside Ornithurae in the literature).
- Synonyms and doubtful names to `excluded.yaml` before writing: PBDB lists as valid Archaeornis, Jurapteryx, Griphosaurus
  (Archaeopteryx), Shenzhouraptor (Jeholornis), Camptodontus/Camptodontornis, Hargeria, Lestornis and others without a
  Wikipedia page; Wikipedia-only Archaeoraptor (composite forgery), Liaoxiornis, Gallornis, Cretaaviculus.
- Wikipedia-only genera: drop the crown birds (Vegavis, Asteriornis, Teviornis, Polarornis, Neogaeornis…), check ages of the
  others (Beiguornis, Bellulornis, Brevidentavis, Gorgonavis, Magnusavis, Meemannavis, Novavis, Pujatopouli, Tenuicruris,
  Yuezhuornis, Maaqwi, Torotix, Lonchodytes, Tytthostonyx).
- Qianshanornis and Qinornis (PBDB first appearance exactly 66 Ma, Paleocene) are outside the volume.
- Write the genera with the atlas-entries procedure; images through the triage page.

# Next steps — Theropoda II

Done (2026-11-27): census (3 runs, base `Maniraptora^Aves^Avialae,Alvarezsauroidea,Therizinosauria`); harvest with scientific
articles (`papers.json`, `oa_figures.json`) and a Wikipedia retry; volume skeleton; 15 clade entries; 193 genus entries (drafts,
`origin: ai-draft`); `excluded.yaml` (Epidendrosaurus, Geminiraptor); 93 backbone genus nodes replaced; docs (TREE_REVIEW, DECISIONS).

Pending genera (not in the PBDB harvest base, or no usable source):
- In the backbone without an entry: Aorun, Infernogallus, Aurornis, Norellraptor.
- Found by the census only on Wikipedia, non-avian, to be checked and harvested by name: Dinevenator, Kank, Manipulonyx (2025–2026),
  Fujianvenator, Shishugounykus, Ojoraptorsaurus, Dalianraptor, Koparion, Kakuru, Bradycneme, Heptasteornis, Ornithodesmus.
  `harvest.py` only harvests PBDB names: a `--names` option for extra genera would be the next step.
- Tiantaisaurus: PBDB valid, but its English Wikipedia entry is the list of informally named dinosaurs; no other source harvested.
- Not entries: Ingenia and Nemegtia (PBDB lists them without species; preoccupied names replaced by Ajancingenia/Heyuannia and
  Nemegtomaia), Shuuvuia (misspelling of Shuvuuia).

Open questions for the owner:
- Tooth taxa kept as incertae sedis with a curation note (Paronychodon, Zapsalis, Richardoestesia, Pectinodon): keep or move to
  `excluded.yaml` as nomina dubia?
- Possible synonyms kept as separate entries: Eosinopteryx and Serikornis (Anchiornis?), Neuquenraptor (Unenlagia?), Balaur
  (Elopteryx?), Stenonychosaurus/Latenivenatrix/Troodon.
- Falcarius suarezarum (ex Geminiraptor) is not yet in the PBDB species list of Falcarius.
- Images were chosen from file names and descriptions without a contact-sheet check: run the triage page for theropoda2.
- Many entries say "Not given in the sources used" or carry a "check" note: they need the primary paper (now listed in papers.json).

# Next steps — Theropoda I (earlier)

Done: volume skeleton; 36 clade entries; 254 genus entries (drafts, `origin: ai-draft`); `excluded.yaml` (29 names: 9 chosen by hand, 20 PBDB
synonyms); backbone cleaned; docs. Images for the entries are fetched by `media-fetch.yml` (see the PR).

Pending genera (no usable source in the harvest, to be checked by hand): Altispinax (PBDB has no species or occurrence), Teihivenator
(its English Wikipedia page is the list of informally named dinosaurs), Lepidocheirosaurus (harvested page is Kulindadromeus),
Ornithomimidorum (no page, no occurrence). Kol and Ngexisaurus are in `excluded.yaml` for the same reason and can be revisited.

Open questions for the owner:
- Should the harvest also download scientific papers (Europe PMC, Crossref, OpenAlex → `data/raw/<volume>/papers.json`)? Proposal: a
  `--papers` option in `scripts/fetch/harvest.py`, as a separate commit.
- Genera whose validity is doubtful and may belong in `excluded.yaml`: Saurophaganax (chimeric), Protathlitis, Shuangbaisaurus (possible
  synonym of Sinosaurus), Sigilmassasaurus, Nanotyrannus (debated).
- Images were chosen from the harvest suggestions without a contact-sheet check for most genera; run the triage page on them.
- Many entries have "Not given in the sources used" in holotype, material or biology: they need the primary paper.

## Added 2026-11-27 (Wikipedia-recognised genera)
Written: Infernogallus, Aorun, Norellraptor, Dinevenator, Kank, Manipulonyx, Fujianvenator, Shishugounykus, Koparion, Bradycneme, Ornithodesmus.
Excluded: Aurornis (synonym of Anchiornis), Heptasteornis, Ojoraptorsaurus, Dalianraptor, Kakuru, Tiantaisaurus.
Open: no images yet (triage page); Shishugounykus holotype/material/biology from Qin et al. 2019; Chure 1994 for Koparion; Nanyuan and Sânpetru
formations need entries (Fujianvenator, Bradycneme have none); Bradycneme may be a synonym of Elopteryx (Stoicescu et al. 2024); check Xenovenator for robustus.
