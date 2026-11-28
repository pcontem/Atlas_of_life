# Next steps — Aves II (waterbirds and shorebirds)

Done (2026-11-28): census, harvest, clade sources; 28 clade entries; 277 genus drafts. Because of the size of the volume, every genus
summary is a thin first draft written from PBDB data (family, age, countries): the cited Wikipedia revision (kept as a source when it is
about the genus) has not yet been read for the text, holotype and biology say "Not given in the sources used", and images were chosen
from Commons file names. excluded.yaml: PBDB synonyms.

Pending genera:
- No type species or no authority in the sources, not written: Archaeospheniscus Ardenna Arthrodytes Belonopterus Blasipus Calonectris Chlidonias Coenocorypha Colymboides Copepteryx Esacus Eudocimus Fregata Fregetta Heteroscelus Hydrobates Hydrophasianus Ibidorhynchus Kashinia Leucocarbo Leucophaeus Limicorallus Macrorhamphus Microcarbo Miopelecanus Nambashag Nautilornis Nectornis Nupharanassa Oceanodroma Oligocorax Onychoprion Paractitis Paraptenodytes Pelidna Phaetusa Phalaropus Philohela Phoebastria Precursor Pseudobulweria Rhinoptilus Sternalara Sula Telmatornis Thalasseus Totanus Tryngites Villetus Xenorhynchus.
- No PBDB occurrence or family outside the volume: see the pending list of work/mkbatch.py output (Ardeacites, Botaurites, Empeirodytes,
  Mioglareola, Scopus, Stercorarius…).
- Living genera without a fossil record are not in PBDB and not in the harvest.

To do: rewrite the summaries, holotype, material and biology of each genus from its Wikipedia revision and the literature (batches of
20–30 per clade); check the type species filled from general knowledge.

# Next steps — Aves I (Palaeognathae and Galloanserae)

Done (2026-11-28): census, harvest, clade sources; 27 clade entries; 226 genus drafts (living genera with `extant: true`; thin drafts from
PBDB alone for genera without a Wikipedia page, marked in curation.notes); excluded.yaml (40 synonyms); tree changes in
docs/TREE_REVIEW.md. Images, silhouettes and palaeo-positions come from media-fetch.yml.

Pending genera:
- No type species found in the sources (or no authority), not written: Argillipes Bambusicola Bucephala Caccabis Callipepla Callonetta Chaulelasmus Chauna Chloephaga Crypturellus Cyanochen Cygnopterus Cygnus Dendrocygna Emeus Emuarius Eoneornis Erismatura Euryanas Euryapteryx Eutelornis Francolinus Loxornis Manuherikia Marila Nettapus Nettion Nothocercus Nyroca Odontophorus Olar Oressochen Ortalis Oxyura Palaeocryptonyx Palaeortyx Paracygnopterus Paraortyx Parapavo Pediocaetes Pinpanetta Pliogallus Pternistis Querquedula Syrmaticus Tachyeres Taoperdix Tinamisornis.
- No PBDB occurrence (fossil genera): Ameripodius, Aminornis, Anserobranta, Archaealectrornis, Archaeophasianus, Chenornis, Cygnanser,
  Cygnavus, Ergilornis, Metapteryx, Miogallus, Percolinus, Pirortyx, Pleistoanser, Proceriavis, Pseudapteryx, Ptenornis, Quercymegapodius,
  Roveretornis, Schaubortyx, Teleornis, Tirarinetta.
- Wikipedia-only genera (46, census): Asteriornis, Garganornis, Centuriavis, Agelastes, Arborophila, Guttera… — need manual age and
  species data.
- Living genera that PBDB does not list (no fossil record) are not in the harvest at all: a source for the full list of living genera
  (e.g. the IOC World Bird List) has to be chosen by the owner.

Open questions for the owner:
- The volume is the root of the crown group (Aves); Neoaves volumes will attach to Neognathae.
- Many type species are filled from general knowledge (type_species_note says so): check.

# Next steps — Avialae (Mesozoic birds outside the crown)

Done (2026-11-27): census, scope (one volume, no crown birds, no form taxa), harvest, clade sources; 21 clade entries; 200 genus
entries (drafts, `origin: ai-draft`, images chosen automatically from file names); `excluded.yaml` (22 names: 17 synonyms, 4 PBDB
nomina dubia, Archaeoraptor); tree changes in docs/TREE_REVIEW.md. Images, silhouettes and palaeo-positions come from media-fetch.yml.

Pending genera (not written):
- No usable source in the harvest: Crateropteryx, Platanavis (no Wikipedia page), Proornis (page redirects to the Sinuiju Formation).
- Crown or probable crown birds, for the Aves volumes: see docs/TREE_REVIEW.md (2026-11-27).
- Qianshanornis and Qinornis (Paleocene) are outside the volume; Camptodontus is the preoccupied name of Camptodontornis (not listed).

Open questions for the owner:
- Possible synonyms kept as entries: Wellnhoferia (Archaeopteryx?), Boluochia (Longipteryx?), Cuspirostrisornis (Cathayornis?),
  Vescornis/Jibeinia, Omnivoropteryx (Sapeornis?); Cerebavis and the feather taxa Ilerdopteryx, Praeornis, Cretaaviculus as nomina dubia?
- Archaeopteryx species: only A. lithographica and A. albersdoerferi kept (PBDB also lists bavarica, macrura, oweni).
- Many entries say "Not given in the sources used" or "number in <original paper>": they need the primary paper (papers.json).
- Run the triage page for avialae: images were picked from file names without a visual check.

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
