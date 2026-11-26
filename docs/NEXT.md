# Next steps — Theropoda I

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
