# Next steps (Sauropodomorpha, second round)

## Done (branch entry/sauropodomorpha-9)
- Batches 9-13, 69 genus entries (ai-draft): Euhelopodidae (+ Quaesitosaurus), Mamenchisauridae, the remaining Rebbachisauridae, 18 Titanosauria,
  Titanosauriformes and Brachiosauridae. All images `unreviewed`; media fetched (the fetch script now skips unreadable files).
- `incertae_sedis` (M2): Quaesitosaurus, Volgatitan, Daanosaurus, Agustinia, Fushanosaurus (reasons in each `placement_note`).
- Type species written from general knowledge and flagged in `type_species_note`: Tangvayosaurus, Daanosaurus, Choconsaurus, Pelorosaurus, Lusotitan.
- Not written (no occurrence or no usable article): Zigongosaurus (no PBDB occurrence).

## Still to write (valid PBDB genera with a Wikipedia article, by PBDB parent; 145 left)
Aeolosaurini (5); Anchisauridae (2); Camarasauridae (1); Camarasauromorpha (1); Cetiosauridae (1); Colossosauria (4); Diamantinasauria (4); Dicraeosauridae (4); Diplodocinae (2); Diplodocoidea (1); Eusauropoda (10); Eutitanosauria (6); Flagellicaudata (1); Gravisauria (2); Guaibasauridae (1); Khebbashia (1); Lessemsauridae (2); Lirainosaurinae (3); Lithostrotia (14); Lognkosauria (4); Macronaria (4); Mamenchisauridae (1); Massopoda (4); Massospondylidae (2); Plateosauridae (3); Rinconsauria (12); Riojasauridae (1); Saltasauridae (4); Saltasaurinae (3); Saltasauroidea (3); Saturnaliidae (1); Sauropoda (5); Sauropodiformes (5); Sauropodomorpha (1); Somphospondyli (21); Turiasauria (4); Unaysauridae (2).
Also left out by scope (ichnogenera and oogenera, PBDB flags I/F: Brontopodus, Parabrontopodus, Megaloolithus, Otozoum...) and 46 names whose article is
missing or wrong in the harvest (Kholumolumo, Ammosaurus, Saturnalia, Qianlong, Wudingloong, Huayracursor, Ampelosaurus, Balochisaurus, Pakisaurus...).
Those need a new harvest request listing the correct article titles.

## Reminders
- Image picks for several batches came from file names and a single mosaic per batch; the Commons "TD.png" files are life restorations, not fossils.
- Check holotype numbers and sizes marked "not read"; check original naming papers where `pbdb_ref_is_literature` was used.

---

# Next steps (Sauropodomorpha)

## Done (this branch, entry/sauropodomorpha-4-8)
- New image harvest (`data/raw/sauropodomorpha/`, from branch data/harvest-sauro-2) adopted. 32 extra images added to 48 existing genus entries
  (all `unreviewed`). Clade entries have no image field, so "revise the clades with images" was done on the genera of those clades.
- 71 new genus entries (ai-draft) in batches 4-8:
  - 4 Plateosauria, 5 Sauropodiformes, 6 basal Sauropodomorpha (40 genera);
  - 7 basal Sauropoda: Gongxianosaurus, Kotasaurus, Barapasaurus, Ohmdenosaurus, Rhoetosaurus, Spinophorosaurus, Tazoudasaurus, Vulcanodon,
    Bagualia, Chebsaurus, Jobaria, Shunosaurus, Cetiosaurus, Patagosaurus, Amanzia;
  - 8 Rebbachisauridae and titanosaurs: Rebbachisaurus, Nigersaurus, Limaysaurus, Demandasaurus, Tataouinea, Amazonsaurus, Comahuesaurus,
    Zapalasaurus, Histriasaurus, Andesaurus, Argyrosaurus, Aegyptosaurus, Rapetosaurus, Dreadnoughtus, Isisaurus, Malawisaurus.
- `incertae_sedis` (M2): Efraasia, Yimenosaurus, Anchisaurus, Lamplughsaura, Plateosauravus, Guaibasaurus (batches 4-6); Histriasaurus within
  Rebbachisauridae (batch 8). Reasons are in each `placement_note`.
- The "Unnamed beds, Castrillo de la Reina" formation entry was removed: Goniopholis now links to the named formation created for Demandasaurus.

## Pending
- Not written, wrong or missing Wikipedia article in the harvest: Qianlong (article is the Qing emperor), Saturnalia (Roman festival),
  Wudingloong and Huayracursor (absent from the harvest).
- No image among the candidates: Gongxianosaurus, Comahuesaurus, Mbiresaurus, Sefapanosaurus; Mendozasaurus, Qijianglong and Garumbatitan have gaps.
- Opisthocoelicaudia: two photos are CC BY-SA 3.0 PL; `validate.py` rejects the string (see DECISIONS.md 2026-11-22); owner to decide.
- About 300 PBDB genera of the volume still have no entry (see the census in `data/raw/census/sauropodomorpha/`), e.g. the remaining Somphospondyli,
  Lithostrotia, Rinconsauria, Mamenchisauridae and the Pakistani/Indian titanosaurs.
- Several holotype numbers, sizes and original naming works are marked "not read" in the entries; they need the primary papers.

## Open questions
- Jobaria: upper mass estimate was cut in the text read; the age differs between Wikipedia (Bathonian-Oxfordian) and PBDB (Oxfordian-Tithonian).
- Gongxianosaurus: Sinemurian-Pliensbachian (Wikipedia) vs Toarcian (PBDB).
- Dreadnoughtus: the original 48-49 t is kept in the range; later re-evaluations give lower masses.
- Rapetosaurus: original-paper index 15 comes from the brief; check it is Curry Rogers and Forster 2001.
- All new images are `unreviewed`; Euhelopus image 10 was added without being looked at.

---

# Next steps (Pseudosuchia)

## Done
- 120 genus entries (ai-draft) added to the Pseudosuchia volume: 105 genera that were waiting in the backbone and 15 more from existing clades
  (Sebecus, Doratodon, Eremosuchus, Pholidosaurus, Sunosuchus, Pelagosaurus, Turnersuchus, Rukwasuchus, Stolokrosuchus, Scutarx,
  Calyptosuchus, Eosuchus, Susisuchus, Dromicosuchus, Luperosuchus).
- Images were taken from the automatic suggestions of the contact sheets, checked by file name; only batch 1 was looked at as a mosaic.
  All are `unreviewed`; use the triage page to confirm kinds and replace doubtful ones.

## Pending
- Six of the 17 names that had no PBDB occurrences were misspellings in the backbone; written under the correct spelling in a second step
  (Xilousuchus, Pseudhesperosuchus, Fruitachampsa, Gracilineustes, Phosphatosaurus, Rhacheosaurus). Pelagosuchus was a duplicate of Pelagosaurus
  (removed from the backbone). Phosphatosaurus has no image yet.
- Written without a formation (rule G10 relaxed on 2026-11-21, see DECISIONS.md; each has the locality in `curation.notes`, so they have no map
  point in Biota yet): Smok (Lipie Slaskie clay pit, Lisowice, Poland), Dyoplax (Schilfsandstein, Stuttgart, Germany), Stegomosuchus (Portland
  Formation, Massachusetts), Proexochokefalos (Marnes de Dives, Normandy), Thikarisuchus (Blackleaf Formation, Montana), Guarinisuchus (Maria
  Farinha Formation, Brazil), Zulmasuchus (Santa Lucia Formation, Bolivia). To give them a formation: coordinates from a cited source, then a
  formation entry and GPlates positions. They also have no images, no silhouette and, except Guarinisuchus and Zulmasuchus, no Wikipedia revision
  (the revision id could not be fetched from this session; harvest them to add it). Guarinisuchus is a subjective synonym of Hyposaurus in PBDB.
- Not written, no usable source found (no English Wikipedia page under that name, nothing in a web search): Domicosuchus, Euphorosuchus,
  Crocodileimus. Their backbone nodes stay. Euphorosuchus may be a misspelling of Eosphorosuchus (Ghost Ranch, New Mexico, described in 2026); not checked.
- Many holotype numbers, type species and original naming works are marked in `curation.notes` (several PBDB references are textbooks).
- Borealosuchus, Malawisuchus, Lorosuchus, Rukwasuchus, Rioarribasuchus, Zaraasuchus, Luperosuchus, Calyptosuchus have no image yet.
- Batrachotomus has no size (no sourced estimate read).

## Open questions
- Armadillosuchus: a 2026 review (Kitayama and Bertini) provisionally treats it as a synonym of Sphagesaurus huenei; kept as valid (PBDB).
- Pedeticosaurus: Clark and Sues (2002) proposed a nomen dubium; kept as valid (PBDB).
- Doratodon: a 2026 study suggests a paralligatorid, not a sebecosuchian; kept in Sebecosuchia (backbone).
- Duerosuchus, Lorosuchus, Comahuesuchus, Heptasuchus, Bergisuchus: PBDB and the backbone place them in different clades; the backbone was kept.

## Completion of the volume from PBDB (2026-11-21, branch entry/pseudosuchia-complete)
- About 190 more genus entries (ai-draft) written from the PBDB download of 2026-11-17 and the Wikipedia revisions in `wiki.json`. Entries without a
  Wikipedia page for the genus (e.g. Hadongsuchus, Khuzdarcroco, Sulaimanisuchus, Induszalim, Sakhibaghoon, Asifcroco, Rhamphostomopsis) rest on PBDB only.
  Almost all have no formation entry details beyond PBDB, no holotype number and often no original naming work (see `curation.notes`).
- Several type species were filled from the PBDB species list or from general knowledge (marked "not yet checked" in `type_species_note`).
- Gondwanasuchus and Stegomus went to `excluded.yaml`.
- Parent clades missing from the atlas (Shartegosuchidae, Itasuchidae, Paluxysuchidae, Aegyptosuchidae, Stromerosuchidae, Allodaposuchidae,
  Induszalimidae, Sulaimanisuchidae) were replaced by the nearest atlas clade with `incertae_sedis` and a `placement_note`; creating those clades would
  let the genera move down.
- Not written, no occurrence or source: Caimanosuchus, Eocenosuchus, Proalligator, Isselosaurus, Dollosuchus, Ferganosuchus, Thecachampsoides,
  Oweniasuchus, Pliogonodon, Symptosuchus, Fenhosuchus, Cladeiodon, Lythrosuchus, Browniella, Baroqueosuchus, Langstonia (no species in PBDB).
- Not written because of status: Mehliella and Batrachopus (trace fossils), Capellineosuchus (treated as a mosasaur by Wikipedia), Rhabdosaurus (Wikipedia
  redirects to Rhabdognathus), Pallisteria (informal name of Mambawakale), Rileyasuchus (phytosaur; phytosaurs stay outside the volume).
- Uncertain validity kept as entries with a note: Tienosuchus, Stromerosuchus, Stagonosuchus, Redondasuchus, Hypselorhachis.
- PBDB data are from 2026-11-17: genera described since then are missing.
- Many images are unchecked automatic suggestions (`unreviewed`); life restorations need the triage page.
- 18 more genera with no PBDB record (described 2024-2026, found in the Wikipedia lists "2025/2026 in archosaur paleontology") were added without formation:
  Ibirasuchus, Pseudogavialis, Sissokosuchus, Taihangosuchus, Tainrakuasuchus, Telkaralura, Wadisuchus, Paarthurnax, Antusuchus, Carinthiasuchus,
  Ctenosuchus, Eosphorosuchus, Galahadosuchus, Herugavialis, Labrujasuchus, Mandrasuchus, Kuttysuchus, Olkasuchus. They cite only the naming paper
  (the Wikipedia revision ids could not be fetched), have no images, and each curation note gives the formation and locality. Euphorosuchus was
  replaced by Eosphorosuchus (TREE_REVIEW.md). Pages for 2024 and earlier were not checked; the 2025/2026 pages were read only in part (first 100,000 characters).

# Next steps (Sauropodomorpha)

## Done
- 21 clade entries (2026-11-21) and batch 1 of genera (2026-11-22): the sixteen Diplodocoidea genera listed in DECISIONS.md (PR 44).
- Batch 2 (2026-11-22): Brachiosaurus, Abydosaurus, Cedarosaurus, Europasaurus, Giraffatitan, Sauroposeidon, Euhelopus, Huabeisaurus, Abrosaurus, Camarasaurus, Liaoningotitan, Garumbatitan, Wintonotitan, Mierasaurus, Moabosaurus, Turiasaurus; Diplodocus images added from the Seismosaurus contact sheet.

- Batch 3 (2026-11-22): Argentinosaurus, Futalognkosaurus, Mendozasaurus, Patagotitan, Rinconsaurus, Analong, Mamenchisaurus, Omeisaurus, Qijianglong, Xinjiangtitan, Nemegtosaurus, Alamosaurus, Opisthocoelicaudia, Ibirania, Neuquensaurus, Saltasaurus. Jichuanlong (backbone node only) is not in the harvest and is still pending.

- Batches 4-13 (2026-11-22, PR 47 and 48): 140 genera, plus 32 images on existing entries.
- Batches 14-24 (2026-11-22): 168 more genera, covering every valid PBDB genus that has a usable English Wikipedia article (Lithostrotia, Eutitanosauria, Rinconsauria, Lognkosauria, Somphospondyli, Eusauropoda, Turiasauria, Dicraeosauridae, Diplodocinae, basal Sauropoda and Sauropodomorpha). Ichnogenera and oogenera stay out by scope.

## Pending
- Genera still without an entry: names with no usable Wikipedia article (Kholumolumo, Saturnalia, Qianlong, Wudingloong, Huayracursor and about 40 more; Zigongosaurus has no PBDB occurrence, Adamantisaurus has none either) need a new harvest. Actiosaurus (a Wikipedia page of doubtful group), Nopcsaspondylus (dubious per Wikipedia) and Coloradia (the Wikipedia page is a moth) were not written; owner to decide on excluded.yaml.
- Many entries say "not read in the sources consulted" for holotype or size: the briefs came from the Wikipedia leads. Fill them from the naming papers when reviewing. Type species written from general knowledge are marked in `type_species_note`.
- Harvest gap: the Wikipedia article pictures were not captured for about 200 of the 449 pages (empty `files`), and the Commons category step takes only the first 15 files, so some genera lack good candidates (Garumbatitan has none). Re-harvest with a fix or add images by hand.
- Holotype numbers not read for Apatosaurus, Brontosaurus, Barosaurus, Diplodocus, Tornieria, Dicraeosaurus, Amargasaurus, Suuwassea, Bajadasaurus;
  Kaatedocus (SMA 004), Supersaurus (BYU 9025) and Haplocanthosaurus (CM 572) need confirmation against the naming papers.
- Images were chosen from the contact sheets by file name and a look at one mosaic per half of the batch; all `unreviewed`. Use the image picker to confirm.
- Lingwulong: age and formation (Yanan vs Zhiluo) and placement (Xu et al. 2018 vs Mannion and Moore 2025) unresolved.
- Formation entries for the new genera need summary and paleoenvironment text (F5).

## Open questions
- Licence strings with a port (CC BY 2.5 AR for the Titanomachya holotype photo, CC BY-SA 3.0 PL for Opisthocoelicaudia) are rejected by the validator; those photos are left out. Allow ported versions, or keep them out?
- Jobaria and Gongxianosaurus age conflicts; Tehuelchesaurus, Atlasaurus, Australodocus, Liubangosaurus and Cetiosauriscus placements are marked `incertae_sedis`.
- Confirm the new G8 size limits (60 m, 150,000 kg) in `scripts/validate.py`.
- Gigantosaurus Fraas 1908 is listed as a junior synonym of Barosaurus (PBDB), although its type species became Tornieria africana; check.
