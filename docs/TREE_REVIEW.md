# Tree review — 2026-11-16

Review of `data/tree/backbone.json` against current taxonomy (owner request). Method: every tree name was looked up in the
Paleobiology Database (`data/raw/tree/pbdb_lineage_2026-11-16.json`: accepted name, rank and full parent chain) and its
PBDB placement compared with the tree. Where PBDB and the tree disagree, the change was made only when PBDB agrees with
recent literature (Wikipedia revisions cited in the clade entries and their references); otherwise the tree was kept and
the case is listed under "Kept against PBDB". Informal groupings ("Basal X", "Uncertain position", "Unidentified") and
nodes pooling several families ("X and Y", "X and relatives") were removed: their members now sit directly in the real
clade above, genera from "uncertain position" groups carry the note *incertae sedis within X*, and genera whose PBDB
family was missing from the tree went into that family (added when at least two genera share it). Rule **T1** of the
validator keeps such groupings from coming back.

Result: 4,046 → 3,965 backbone nodes; 99 groupings removed, 21 families added.

## Groupings dissolved (99)

<details><summary>Show all</summary>

- Uncertain position removed — in Eurylaimides; informal grouping
- Basal felids removed — in Felidae; informal grouping
- Ursavini and relatives removed — in Ursidae; informal grouping
- Basal Pinnipedimorpha removed — in Pinnipedimorpha; informal grouping
- Basal arctoids removed — in Caniformia; informal grouping
- Basal Cervidae removed — in Cervidae; informal grouping
- Giant rodents (Dinomyidae and Neoepiblemidae) removed — in Caviomorpha; informal grouping
- Cuniculidae and Dasyproctidae removed — in Caviomorpha; grouping of several families, not a clade
- Toothed mysticetes removed — in Mysticeti; informal grouping
- Basal Chaeomysticeti removed — in Mysticeti; informal grouping
- Cetotheriidae and relatives removed — in Mysticeti; informal grouping
- Basal odontocetes removed — in Odontoceti; informal grouping
- Hyracodontidae and Paraceratheriidae removed — in Rhinocerotoidea; grouping of several families, not a clade
- Basal hominoids removed — in Catarrhini; informal grouping
- Petromuridae and Thryonomyidae removed — in Hystricomorpha; grouping of several families, not a clade
- Basal Oviraptorosauria removed — in Oviraptorosauria; informal grouping
- Basal Carnivoramorpha removed — in Pan-Carnivora; informal grouping
- Basal Tapiromorpha removed — in Perissodactyla; informal grouping
- Basal ruminants removed — in Ruminantia; informal grouping
- Basal Simiiformes removed — in Haplorhini; informal grouping
- Basal rodents removed — in Rodentia; informal grouping
- Basal coelurosaurs removed — in Compsognathidae; informal grouping
- Basal ornithomimosaurs removed — in Ornithomimosauria; informal grouping
- Intermediate tyrannosauroids removed — in Tyrannosauroidea; informal grouping
- Basal maniraptorans removed — in Maniraptora; informal grouping
- Gomphotheres and amebelodonts removed — in Elephantiformes; informal grouping
- Anthracobunidae and Cambaytheriidae removed — in Panperissodactyla; grouping of several families, not a clade
- Basal artiodactyls removed — in Artiodactyla; informal grouping
- Anoplotherioidea and relatives removed — in Artiodactyla; informal grouping
- Entelodontidae and relatives removed — in Artiodactyla; informal grouping
- Eocene bats removed — in Chiroptera; informal grouping
- Unidentified removed — in Chiroptera; informal grouping
- Fossil eulipotyphlans removed — in Eulipotyphla; informal grouping
- Zalambdalestidae and Anagalidae removed — in Anagaloidea; grouping of several families, not a clade
- Basal Crocodyloidea removed — in Crocodyloidea; informal grouping
- Basal Alligatoroidea removed — in Alligatoroidea; informal grouping
- Uncertain position removed — in Megalosauroidea; informal grouping
- Uncertain position removed — in Carnosauria; informal grouping
- Basal proboscideans removed — in Proboscidea; informal grouping
- Basal Paenungulata removed — in Paenungulata; informal grouping
- Uncertain position removed — in Cingulata; informal grouping
- Basal Megatherioidea removed — in Folivora; informal grouping
- Mesonychia, Arctocyonia and Periptychidae removed — in Eutheria; grouping of several families, not a clade
- Pantolesta and Pantodonta removed — in Eutheria; grouping of several families, not a clade
- Tillodontia and Taeniodonta removed — in Eutheria; grouping of several families, not a clade
- Anagaloidea and Leptictida removed — in Eutheria; grouping of several families, not a clade
- Basal ceratopsians removed — in Ceratopsia; informal grouping
- Basal Neoceratopsia removed — in Ceratopsia; informal grouping
- Basal Ceratopsoidea removed — in Ceratopsia; informal grouping
- Basal diplodocoids removed — in Diplodocoidea; informal grouping
- Basal camarasauromorphs removed — in Macronaria; informal grouping
- Basal Somphospondyli removed — in Macronaria; informal grouping
- Archaic eutherians (uncertain position) removed — in Eutheria; informal grouping
- Basal Metriorhynchoidea removed — in Metriorhynchoidea; informal grouping
- Basal eusuchians removed — in Eusuchia; informal grouping
- Early gavialoids removed — in Eusuchia; informal grouping
- Basal theropods (uncertain position) removed — in Neotheropoda; informal grouping
- Dilophosauridae and relatives removed — in Neotheropoda; informal grouping
- Basal sauropods removed — in Sauropoda; informal grouping
- Basal neornithischians removed — in Ornithopoda; informal grouping
- Ankylopollexia (non-hadrosaurs) removed — in Ornithopoda; informal grouping
- Basal Hadrosauroidea removed — in Ornithopoda; informal grouping
- Basal thyreophorans (outside Ankylosauria) removed — in Ankylosauria; informal grouping
- Basal ankylosaurs removed — in Ankylosauria; informal grouping
- Basal Cladotheria removed — in Trechnotheria; informal grouping
- Basal metatherians removed — in Metatheria; informal grouping
- Herpetotheriidae and Peradectidae removed — in Metatheria; grouping of several families, not a clade
- Basal and various notosuchians removed — in Notosuchia; informal grouping
- Advanced Ziphosuchia (Notosuchidae and Sphagesauridae) removed — in Notosuchia; informal grouping
- Other neosuchians removed — in Neosuchia; informal grouping
- Uncertain position (perhaps basal theropods) removed — in Herrerasauria; informal grouping
- Basal sauropodomorphs removed — in Sauropodomorpha; informal grouping
- Thecodontosauridae and relatives removed — in Sauropodomorpha; informal grouping
- Cynodonts and mammaliaforms removed — in Theriimorpha; informal grouping
- Various basal mammals removed — in Theriimorpha; informal grouping
- Basal monotremes removed — in Monotremata; informal grouping
- Basal pseudosuchians removed — in Pseudosuchia; informal grouping
- Position to be revised (Peirosauridae, a notosuchian) removed — in Pseudosuchia; informal grouping
- Basal poposauroids removed — in Poposauroidea; informal grouping
- Poposauridae and Shuvosauridae removed — in Poposauroidea; grouping of several families, not a clade
- Uncertain position removed — in Poposauroidea; informal grouping
- Basal loricatans removed — in Rauisuchia; informal grouping
- Erpetosuchidae and Gracilisuchidae removed — in Pseudosuchia; grouping of several families, not a clade
- Basal dinosauromorphs removed — in Avemetatarsalia; informal grouping
- Basal mammaliaforms removed — in Mammaliamorpha; informal grouping
- Colubroidea (uncertain position) removed — in Caenophidia; informal grouping
- Basal phytosaurs removed — in Phytosauria; informal grouping
- Basal cynodonts removed — in Cynodontia; informal grouping
- Jurassic squamates (uncertain position) removed — in Ophidia; informal grouping
- Vancleaveidae and relatives removed — in Archosauriformes; informal grouping
- Other archosauriforms (uncertain position) removed — in Archosauriformes; informal grouping
- Uncertain position removed — in Dinocephalia; informal grouping
- Basal anomodonts removed — in Anomodontia; informal grouping
- Basal sphenacodonts removed — in Sphenacodontidae; informal grouping
- Uncertain position removed — in Diadectomorpha; informal grouping
- Devonian stem tetrapods removed — in Tetrapoda; informal grouping
- Eocene fossils removed — in Syngnathiformes; informal grouping
- Unidentified removed — in Syngnathiformes; informal grouping
- Ediacaran biota (uncertain position) removed — in Metazoa; informal grouping

</details>

## Families added (21)

- Shuvosauridae (in Poposauroidea) — PBDB family of *Effigia*, *Shuvosaurus*, *Sillosuchus*, *Sonselasuchus*, which sat in informal groupings
- Candidodontidae (in Notosuchia) — PBDB family of *Malawisuchus*, *Pakasuchus*, *Thilastikosuchus*, which sat in informal groupings
- Sphagesauridae (in Notosuchia) — PBDB family of *Adamantinasuchus*, *Yacarerani*, *Armadillosuchus*, *Caipirasuchus*, *Morrinhosuchus*, *Sphagesaurus*, which sat in informal groupings
- Hylaeochampsidae (in Eusuchia) — PBDB family of *Hylaeochampsa*, *Iharkutosuchus*, *Acynodon*, which sat in informal groupings
- Alligatoridae (in Alligatoroidea) — PBDB family of *Brachychampsa*, *Stangerochampsa*, which sat in informal groupings
- Euhelopodidae (in Macronaria) — PBDB family of *Euhelopus*, *Huabeisaurus*, which sat in informal groupings
- Thescelosauridae (in Ornithopoda) — PBDB family of *Changmiania*, *Orodromeus*, *Oryctodromeus*, *Changchunsaurus*, *Fona*, *Haya*, *Jeholosaurus*, *Parksosaurus*, *Thescelosaurus*, which sat in informal groupings
- Charassognathidae (in Cynodontia) — PBDB family of *Charassognathus*, *Abdalodon*, which sat in informal groupings
- Aetiocetidae (in Mysticeti) — PBDB family of *Aetiocetus*, *Fucaia*, which sat in informal groupings
- Eomysticetidae (in Mysticeti) — PBDB family of *Tokarahia*, *Waharoa*, which sat in informal groupings
- Xenorophidae (in Odontoceti) — PBDB family of *Xenorophus*, *Cotylocara*, *Mirocetus*, *Inermorostrum*, which sat in informal groupings
- Numidotheriidae (in Proboscidea) — PBDB family of *Daouitherium*, *Numidotherium*, which sat in informal groupings
- Gomphotheriidae (in Elephantiformes) — PBDB family of *Archaeobelodon*, *Serbelodon*, *Amebelodon*, *Eubelodon*, *Aphanobelodon*, *Platybelodon*, *Cuvieronius*, *Gomphotherium*, *Notiomastodon*, *Rhynchotherium*, *Stegomastodon*, *Anancus*, *Konobelodon*, *Tetralophodon*, *Sinomastodon*, which sat in informal groupings
- Paraceratheriidae (in Rhinocerotoidea) — PBDB family of *Paraceratherium*, *Forstercooperia*, *Dzungariotherium*, *Juxia*, *Urtinotherium*, which sat in informal groupings
- Dichobunidae (in Artiodactyla) — PBDB family of *Messelobunodon*, *Dichobune*, which sat in informal groupings
- Anoplotheriidae (in Artiodactyla) — PBDB family of *Anoplotherium*, *Diplobune*, which sat in informal groupings
- Entelodontidae (in Artiodactyla) — PBDB family of *Archaeotherium*, *Brachyhyops*, *Daeodon*, *Entelodon*, which sat in informal groupings
- Ischyromyidae (in Rodentia) — PBDB family of *Ailuravus*, *Ischyromys*, *Masillamys*, *Paramys*, which sat in informal groupings
- Neoepiblemidae (in Caviomorpha) — PBDB family of *Phoberomys*, *Neoepiblema*, which sat in informal groupings
- Amphilemuridae (in Eulipotyphla) — PBDB family of *Pholidocercus*, *Macrocranion*, which sat in informal groupings
- Deltatheridiidae (in Metatheria) — PBDB family of *Sulestes*, *Deltatheridium*, *Lotheridium*, which sat in informal groupings

## Clades moved (15)

- Amphicyonidae (bear-dogs): Canidae → Caniformia — a caniform family of its own, not part of Canidae (PBDB; Wikipedia)
- Alligatorinae: Alligatoroidea → Alligatoridae — subfamily of Alligatoridae (PBDB; Wikipedia)
- Caimaninae: Alligatoroidea → Alligatoridae — subfamily of Alligatoridae (PBDB; Wikipedia)
- Lissamphibia: Tetrapoda → Temnospondyli — majority (temnospondyl) hypothesis of lissamphibian origin, as in PBDB; a lepospondyl origin is still argued
- Cetacea: Artiodactyla → Whippomorpha — whales are the sister group of hippos within Whippomorpha (PBDB; molecular consensus)
- Archosauria: Archosauriformes → Eucrocopoda — Eucrocopoda = euparkeriids, proterochampsians and archosaurs (PBDB; Ezcurra 2016)
- Felidae: Feliformia → Feloidea — Felidae belongs to Feloidea (PBDB)
- Sauropoda: Sauropodomorpha → Sauropodiformes — Sauropodiformes includes Sauropoda (PBDB)
- Caenophidia: Ophidia → Alethinophidia — Caenophidia is a subgroup of Alethinophidia (PBDB; Wikipedia)
- Typothoracinae: Aetosauridae → Aetosaurinae — Typothoracinae is nested within Aetosaurinae (PBDB; Parker 2016)
- Planocraniidae: Eusuchia → Crocodylia — planocraniids are crocodylians (PBDB)
- Akidnognathidae: Therocephalia → Eutherocephalia — akidnognathids are eutherocephalians (PBDB)
- Avialae: Maniraptora → Paraves — Avialae is a subgroup of Paraves (PBDB; Wikipedia)
- Morganucodonta: Basal mammaliaforms → Mammaliaformes — morganucodontans are mammaliaforms (PBDB)
- Docodonta: Basal mammaliaforms → Mammaliaformes — docodonts are mammaliaforms (PBDB)

## Genera placed (135)

<details><summary>Show all</summary>

- *Effigia*: Poposauridae and Shuvosauridae → Shuvosauridae — PBDB family Shuvosauridae
- *Shuvosaurus*: Poposauridae and Shuvosauridae → Shuvosauridae — PBDB family Shuvosauridae
- *Sillosuchus*: Poposauridae and Shuvosauridae → Shuvosauridae — PBDB family Shuvosauridae
- *Sonselasuchus*: Poposauridae and Shuvosauridae → Shuvosauridae — PBDB family Shuvosauridae
- *Malawisuchus*: Basal and various notosuchians → Candidodontidae — PBDB family Candidodontidae
- *Pakasuchus*: Basal and various notosuchians → Candidodontidae — PBDB family Candidodontidae
- *Thilastikosuchus*: Basal and various notosuchians → Candidodontidae — PBDB family Candidodontidae
- *Adamantinasuchus*: Advanced Ziphosuchia → Sphagesauridae — PBDB family Sphagesauridae
- *Yacarerani*: Advanced Ziphosuchia → Sphagesauridae — PBDB family Sphagesauridae
- *Armadillosuchus*: Advanced Ziphosuchia → Sphagesauridae — PBDB family Sphagesauridae
- *Caipirasuchus*: Advanced Ziphosuchia → Sphagesauridae — PBDB family Sphagesauridae
- *Morrinhosuchus*: Advanced Ziphosuchia → Sphagesauridae — PBDB family Sphagesauridae
- *Sphagesaurus*: Advanced Ziphosuchia → Sphagesauridae — PBDB family Sphagesauridae
- *Hylaeochampsa*: Basal eusuchians → Hylaeochampsidae — PBDB family Hylaeochampsidae
- *Iharkutosuchus*: Basal eusuchians → Hylaeochampsidae — PBDB family Hylaeochampsidae
- *Acynodon*: Basal eusuchians → Hylaeochampsidae — PBDB family Hylaeochampsidae
- *Brachychampsa*: Basal Alligatoroidea → Alligatoridae — PBDB family Alligatoridae
- *Stangerochampsa*: Basal Alligatoroidea → Alligatoridae — PBDB family Alligatoridae
- *Euhelopus*: Basal Somphospondyli → Euhelopodidae — PBDB family Euhelopodidae
- *Huabeisaurus*: Basal Somphospondyli → Euhelopodidae — PBDB family Euhelopodidae
- *Changmiania*: Basal neornithischians → Thescelosauridae — PBDB family Thescelosauridae
- *Orodromeus*: Basal neornithischians → Thescelosauridae — PBDB family Thescelosauridae
- *Oryctodromeus*: Basal neornithischians → Thescelosauridae — PBDB family Thescelosauridae
- *Changchunsaurus*: Basal neornithischians → Thescelosauridae — PBDB family Thescelosauridae
- *Fona*: Basal neornithischians → Thescelosauridae — PBDB family Thescelosauridae
- *Haya*: Basal neornithischians → Thescelosauridae — PBDB family Thescelosauridae
- *Jeholosaurus*: Basal neornithischians → Thescelosauridae — PBDB family Thescelosauridae
- *Parksosaurus*: Basal neornithischians → Thescelosauridae — PBDB family Thescelosauridae
- *Thescelosaurus*: Basal neornithischians → Thescelosauridae — PBDB family Thescelosauridae
- *Charassognathus*: Basal cynodonts → Charassognathidae — PBDB family Charassognathidae
- *Abdalodon*: Basal cynodonts → Charassognathidae — PBDB family Charassognathidae
- *Aetiocetus*: Toothed mysticetes → Aetiocetidae — PBDB family Aetiocetidae
- *Fucaia*: Toothed mysticetes → Aetiocetidae — PBDB family Aetiocetidae
- *Tokarahia*: Basal Chaeomysticeti → Eomysticetidae — PBDB family Eomysticetidae
- *Waharoa*: Basal Chaeomysticeti → Eomysticetidae — PBDB family Eomysticetidae
- *Xenorophus*: Basal odontocetes → Xenorophidae — PBDB family Xenorophidae
- *Cotylocara*: Basal odontocetes → Xenorophidae — PBDB family Xenorophidae
- *Mirocetus*: Basal odontocetes → Xenorophidae — PBDB family Xenorophidae
- *Inermorostrum*: Basal odontocetes → Xenorophidae — PBDB family Xenorophidae
- *Daouitherium*: Basal proboscideans → Numidotheriidae — PBDB family Numidotheriidae
- *Numidotherium*: Basal proboscideans → Numidotheriidae — PBDB family Numidotheriidae
- *Archaeobelodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Serbelodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Amebelodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Eubelodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Aphanobelodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Platybelodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Cuvieronius*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Gomphotherium*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Notiomastodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Rhynchotherium*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Stegomastodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Anancus*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Konobelodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Tetralophodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Sinomastodon*: Gomphotheres and amebelodonts → Gomphotheriidae — PBDB family Gomphotheriidae
- *Paraceratherium*: Hyracodontidae and Paraceratheriidae → Paraceratheriidae — PBDB family Paraceratheriidae
- *Forstercooperia*: Hyracodontidae and Paraceratheriidae → Paraceratheriidae — PBDB family Paraceratheriidae
- *Dzungariotherium*: Hyracodontidae and Paraceratheriidae → Paraceratheriidae — PBDB family Paraceratheriidae
- *Juxia*: Hyracodontidae and Paraceratheriidae → Paraceratheriidae — PBDB family Paraceratheriidae
- *Urtinotherium*: Hyracodontidae and Paraceratheriidae → Paraceratheriidae — PBDB family Paraceratheriidae
- *Messelobunodon*: Basal artiodactyls → Dichobunidae — PBDB family Dichobunidae
- *Dichobune*: Basal artiodactyls → Dichobunidae — PBDB family Dichobunidae
- *Anoplotherium*: Anoplotherioidea and relatives → Anoplotheriidae — PBDB family Anoplotheriidae
- *Diplobune*: Anoplotherioidea and relatives → Anoplotheriidae — PBDB family Anoplotheriidae
- *Archaeotherium*: Entelodontidae and relatives → Entelodontidae — PBDB family Entelodontidae
- *Brachyhyops*: Entelodontidae and relatives → Entelodontidae — PBDB family Entelodontidae
- *Daeodon*: Entelodontidae and relatives → Entelodontidae — PBDB family Entelodontidae
- *Entelodon*: Entelodontidae and relatives → Entelodontidae — PBDB family Entelodontidae
- *Ailuravus*: Basal rodents → Ischyromyidae — PBDB family Ischyromyidae
- *Ischyromys*: Basal rodents → Ischyromyidae — PBDB family Ischyromyidae
- *Masillamys*: Basal rodents → Ischyromyidae — PBDB family Ischyromyidae
- *Paramys*: Basal rodents → Ischyromyidae — PBDB family Ischyromyidae
- *Phoberomys*: Giant rodents → Neoepiblemidae — PBDB family Neoepiblemidae
- *Neoepiblema*: Giant rodents → Neoepiblemidae — PBDB family Neoepiblemidae
- *Pholidocercus*: Fossil eulipotyphlans → Amphilemuridae — PBDB family Amphilemuridae
- *Macrocranion*: Fossil eulipotyphlans → Amphilemuridae — PBDB family Amphilemuridae
- *Sulestes*: Basal metatherians → Deltatheridiidae — PBDB family Deltatheridiidae
- *Deltatheridium*: Basal metatherians → Deltatheridiidae — PBDB family Deltatheridiidae
- *Lotheridium*: Basal metatherians → Deltatheridiidae — PBDB family Deltatheridiidae
- *Kaupitherium*: Sirenia → Dugongidae — PBDB places it in Dugongidae
- *Crenatosiren*: Sirenia → Dugongidae — PBDB places it in Dugongidae
- *Corystosiren*: Sirenia → Dugongidae — PBDB places it in Dugongidae
- *Nanosiren*: Sirenia → Dugongidae — PBDB places it in Dugongidae
- *Rytiodus*: Sirenia → Dugongidae — PBDB places it in Dugongidae
- *Metaxytherium*: Sirenia → Dugongidae — PBDB places it in Dugongidae
- *Dorcopsulus*: Macropodiformes → Macropodidae — PBDB places it in Macropodidae
- *Cookeroo*: Macropodiformes → Macropodidae — PBDB places it in Macropodidae
- *Protemnodon*: Macropodiformes → Macropodidae — PBDB places it in Macropodidae
- *Bohra*: Macropodiformes → Macropodidae — PBDB places it in Macropodidae
- *Eotrachodon*: Basal Hadrosauroidea → Hadrosauridae — PBDB places it in Hadrosauridae
- *Aquilarhinus*: Basal Hadrosauroidea → Hadrosauridae — PBDB places it in Hadrosauridae
- *Hadrosaurus*: Basal Hadrosauroidea → Hadrosauridae — PBDB places it in Hadrosauridae
- *Cetotherium*: Cetotheriidae and relatives → Cetotheriidae — PBDB places it in Cetotheriidae
- *Herpetocetus*: Cetotheriidae and relatives → Cetotheriidae — PBDB places it in Cetotheriidae
- *Piscobalaena*: Cetotheriidae and relatives → Cetotheriidae — PBDB places it in Cetotheriidae
- *Eumegamys*: Giant rodents → Dinomyidae — PBDB places it in Dinomyidae
- *Josephoartigasia*: Giant rodents → Dinomyidae — PBDB places it in Dinomyidae
- *Telicomys*: Giant rodents → Dinomyidae — PBDB places it in Dinomyidae
- *Sinoconodon*: Basal mammaliaforms → Mammaliaformes — PBDB places it in Mammaliaformes
- *Hadrocodium*: Basal mammaliaforms → Mammaliaformes — PBDB places it in Mammaliaformes
- *Ballusia*: Ursavini and relatives → Ursinae — PBDB places it in Ursinae
- *Ursavus*: Ursavini and relatives → Ursinae — PBDB places it in Ursinae
- *Cebupithecia*: Platyrrhini → Pitheciidae — PBDB places it in Pitheciidae
- *Caipora*: Platyrrhini → Atelidae — PBDB places it in Atelidae
- *Protopithecus*: Platyrrhini → Atelidae — PBDB places it in Atelidae
- *Phascolonus*: Vombatiformes → Vombatidae — PBDB places it in Vombatidae
- *Ramsayia*: Vombatiformes → Vombatidae — PBDB places it in Vombatidae
- *Eekaulostomus*: Eocene fossils → Aulostomoidea — PBDB places it in Aulostomoidea
- *Fistularioides*: Eocene fossils → Fistulariidae — PBDB places it in Fistulariidae
- *Ebrachosuchus*: Basal phytosaurs → Parasuchidae — PBDB places it in Parasuchidae
- *Patagosuchus*: Position to be revised → Peirosauridae — PBDB places it in Peirosauridae
- *Borealosuchus*: Basal eusuchians → Crocodylia — PBDB places it in Crocodylia
- *Portugalosuchus*: Basal eusuchians → Gavialoidea — PBDB places it in Gavialoidea
- *Argochampsa*: Early gavialoids → Gavialoidea — PBDB places it in Gavialoidea
- *Thoracosaurus*: Early gavialoids → Gavialoidea — PBDB places it in Gavialoidea
- *Purgatorius*: Eutheria → Plesiadapiformes — PBDB places it in Plesiadapiformes
- *Waipatia*: Basal odontocetes → Platanistoidea — PBDB places it in Platanistoidea
- *Aulophyseter*: Physeteroidea → Physeteridae — PBDB places it in Physeteridae
- *Pebanista*: Platanistoidea → Platanistidae — PBDB places it in Platanistidae
- *Styriofelis*: Basal felids → Felinae — PBDB places it in Felinae
- *Amphiorycteropus*: Tubulidentata → Orycteropodidae — PBDB places it in Orycteropodidae
- *Aegyptopithecus*: Basal Simiiformes → Catarrhini — PBDB places it in Catarrhini
- *Pachylemur*: Lemuriformes → Lemuridae — PBDB places it in Lemuridae
- *Leontocebus*: Platyrrhini → Callitrichidae — PBDB places it in Callitrichidae
- *Megapedetes*: Anomaluromorpha → Pedetidae — PBDB places it in Pedetidae
- *Loncheres*: Octodontoidea → Echimyidae — PBDB places it in Echimyidae
- *Silvacola*: Fossil eulipotyphlans → Erinaceidae — PBDB places it in Erinaceidae
- *Thylophorops*: Didelphimorphia → Didelphidae — PBDB places it in Didelphidae
- *Caloprymnus*: Macropodiformes → Potoroidae — PBDB places it in Potoroidae
- *Nimiokoala*: Vombatiformes → Phascolarctidae — PBDB places it in Phascolarctidae
- *Bocatherium*: Cynodonts and mammaliaforms → Tritylodontidae — PBDB places it in Tritylodontidae
- *Bienotherium*: Cynodonts and mammaliaforms → Tritylodontidae — PBDB places it in Tritylodontidae
- *Hydrodamalis*: Sirenia → Dugongidae — PBDB places it in Dugongidae
- *Eotheroides*: Sirenia → Dugongidae — PBDB places it in Dugongidae

</details>

## Duplicates merged (16)

- *Deinosuchus*: Alligatoroidea → Alligatoroidea — duplicate node merged
- *Diplocynodon*: Alligatoroidea → Alligatoroidea — duplicate node merged
- *Leidyosuchus*: Alligatoroidea → Alligatoroidea — duplicate node merged
- Alligatoroidea removed — duplicate of Alligatoroidea (crocodylia__alligatoroidea)
- *Compsognathus*: Compsognathidae → Compsognathidae — duplicate node merged
- *Huaxiagnathus*: Compsognathidae → Compsognathidae — duplicate node merged
- *Sinocalliopteryx*: Compsognathidae → Compsognathidae — duplicate node merged
- *Sinosauropteryx*: Compsognathidae → Compsognathidae — duplicate node merged
- *Juravenator*: Compsognathidae → Compsognathidae — duplicate node merged
- *Sciurumimus*: Compsognathidae → Compsognathidae — duplicate node merged
- *Ubirajara*: Compsognathidae → Compsognathidae — duplicate node merged
- *Xunmenglong*: Compsognathidae → Compsognathidae — duplicate node merged
- *Huadanosaurus*: Compsognathidae → Compsognathidae — duplicate node merged
- Compsognathidae removed — duplicate of Compsognathidae (compsognathidae)
- *Eomaia*: Eutheria → Eutheria — second "Eutheria" node merged into the real one
- Eutheria removed — informal duplicate of Eutheria

## Renamed (English) (5)

- Serpentes-tronco → Stem snakes
- Progimnospermas → Progymnosperms
- Gimnospermas → Gymnosperms
- Ostracodermes → Ostracoderms
- Condilartros → Condylarths

## Moved out of dissolved groupings (311)

<details><summary>Show all</summary>

- *Pseudocalyptomena*: Uncertain position → Eurylaimides — out of the dissolved grouping "Uncertain position"
- *Proailurus*: Basal felids → Felidae — out of the dissolved grouping "Basal felids"
- *Pseudaelurus*: Basal felids → Felidae — out of the dissolved grouping "Basal felids"
- *Hyperailurictis*: Basal felids → Felidae — out of the dissolved grouping "Basal felids"
- *Potamotherium*: Basal Pinnipedimorpha → Pinnipedimorpha — out of the dissolved grouping "Basal Pinnipedimorpha"
- *Enaliarctos*: Basal Pinnipedimorpha → Pinnipedimorpha — out of the dissolved grouping "Basal Pinnipedimorpha"
- *Puijila*: Basal Pinnipedimorpha → Pinnipedimorpha — out of the dissolved grouping "Basal Pinnipedimorpha"
- *Amphicynodon*: Basal arctoids → Caniformia — out of the dissolved grouping "Basal arctoids"
- *Dicrocerus*: Basal Cervidae → Cervidae — out of the dissolved grouping "Basal Cervidae"
- *Procervulus*: Basal Cervidae → Cervidae — out of the dissolved grouping "Basal Cervidae"
- *Lagomeryx*: Basal Cervidae → Cervidae — out of the dissolved grouping "Basal Cervidae"
- *Longirostromeryx*: Basal Cervidae → Cervidae — out of the dissolved grouping "Basal Cervidae"
- Cuniculidae: Cuniculidae and Dasyproctidae → Caviomorpha — out of the dissolved grouping "Cuniculidae and Dasyproctidae"
- Dasyproctidae: Cuniculidae and Dasyproctidae → Caviomorpha — out of the dissolved grouping "Cuniculidae and Dasyproctidae"
- *Janjucetus*: Toothed mysticetes → Mysticeti — out of the dissolved grouping "Toothed mysticetes"
- *Coronodon*: Toothed mysticetes → Mysticeti — out of the dissolved grouping "Toothed mysticetes"
- *Llanocetus*: Toothed mysticetes → Mysticeti — out of the dissolved grouping "Toothed mysticetes"
- *Mystacodon*: Toothed mysticetes → Mysticeti — out of the dissolved grouping "Toothed mysticetes"
- *Maiabalaena*: Basal Chaeomysticeti → Mysticeti — out of the dissolved grouping "Basal Chaeomysticeti"
- *Parietobalaena*: Cetotheriidae and relatives → Mysticeti — out of the dissolved grouping "Cetotheriidae and relatives"
- *Diorocetus*: Cetotheriidae and relatives → Mysticeti — out of the dissolved grouping "Cetotheriidae and relatives"
- *Simocetus*: Basal odontocetes → Odontoceti — out of the dissolved grouping "Basal odontocetes"
- *Squalodon*: Basal odontocetes → Odontoceti — out of the dissolved grouping "Basal odontocetes"
- *Ankylorhiza*: Basal odontocetes → Odontoceti — out of the dissolved grouping "Basal odontocetes"
- *Macrokentriodon*: Basal odontocetes → Odontoceti — out of the dissolved grouping "Basal odontocetes"
- *Eggysodon*: Hyracodontidae and Paraceratheriidae → Rhinocerotoidea — out of the dissolved grouping "Hyracodontidae and Paraceratheriidae"
- *Hyracodon*: Hyracodontidae and Paraceratheriidae → Rhinocerotoidea — out of the dissolved grouping "Hyracodontidae and Paraceratheriidae"
- *Pliobates*: Basal hominoids → Catarrhini — out of the dissolved grouping "Basal hominoids"
- *Proconsul*: Basal hominoids → Catarrhini — out of the dissolved grouping "Basal hominoids"
- *Dendropithecus*: Basal hominoids → Catarrhini — out of the dissolved grouping "Basal hominoids"
- *Moropithecus*: Basal hominoids → Catarrhini — out of the dissolved grouping "Basal hominoids"
- *Oreopithecus*: Basal hominoids → Catarrhini — out of the dissolved grouping "Basal hominoids"
- Petromuridae: Petromuridae and Thryonomyidae → Hystricomorpha — out of the dissolved grouping "Petromuridae and Thryonomyidae"
- Thryonomyidae: Petromuridae and Thryonomyidae → Hystricomorpha — out of the dissolved grouping "Petromuridae and Thryonomyidae"
- *Incisivosaurus*: Basal Oviraptorosauria → Oviraptorosauria — out of the dissolved grouping "Basal Oviraptorosauria"
- *Ningyuansaurus*: Basal Oviraptorosauria → Oviraptorosauria — out of the dissolved grouping "Basal Oviraptorosauria"
- *Protarchaeopteryx*: Basal Oviraptorosauria → Oviraptorosauria — out of the dissolved grouping "Basal Oviraptorosauria"
- *Yuanyanglong*: Basal Oviraptorosauria → Oviraptorosauria — out of the dissolved grouping "Basal Oviraptorosauria"
- *Caudipteryx*: Basal Oviraptorosauria → Oviraptorosauria — out of the dissolved grouping "Basal Oviraptorosauria"
- *Similicaudipteryx*: Basal Oviraptorosauria → Oviraptorosauria — out of the dissolved grouping "Basal Oviraptorosauria"
- *Avimimus*: Basal Oviraptorosauria → Oviraptorosauria — out of the dissolved grouping "Basal Oviraptorosauria"
- *Miacis*: Basal Carnivoramorpha → Pan-Carnivora — out of the dissolved grouping "Basal Carnivoramorpha"
- *Paroodectes*: Basal Carnivoramorpha → Pan-Carnivora — out of the dissolved grouping "Basal Carnivoramorpha"
- *Tapocyon*: Basal Carnivoramorpha → Pan-Carnivora — out of the dissolved grouping "Basal Carnivoramorpha"
- *Vulpavus*: Basal Carnivoramorpha → Pan-Carnivora — out of the dissolved grouping "Basal Carnivoramorpha"
- *Dormaalocyon*: Basal Carnivoramorpha → Pan-Carnivora — out of the dissolved grouping "Basal Carnivoramorpha"
- *Viverravus*: Basal Carnivoramorpha → Pan-Carnivora — out of the dissolved grouping "Basal Carnivoramorpha"
- *Lophiodon*: Basal Tapiromorpha → Perissodactyla — out of the dissolved grouping "Basal Tapiromorpha"
- *Helaletes*: Basal Tapiromorpha → Perissodactyla — out of the dissolved grouping "Basal Tapiromorpha"
- *Heptodon*: Basal Tapiromorpha → Perissodactyla — out of the dissolved grouping "Basal Tapiromorpha"
- *Hyrachyus*: Basal Tapiromorpha → Perissodactyla — out of the dissolved grouping "Basal Tapiromorpha"
- *Lophialetes*: Basal Tapiromorpha → Perissodactyla — out of the dissolved grouping "Basal Tapiromorpha"
- *Thuliadanta*: Basal Tapiromorpha → Perissodactyla — out of the dissolved grouping "Basal Tapiromorpha"
- *Paracolodon*: Basal Tapiromorpha → Perissodactyla — out of the dissolved grouping "Basal Tapiromorpha"
- *Leptomeryx*: Basal ruminants → Ruminantia — out of the dissolved grouping "Basal ruminants"
- *Hypertragulus*: Basal ruminants → Ruminantia — out of the dissolved grouping "Basal ruminants"
- *Hypisodus*: Basal ruminants → Ruminantia — out of the dissolved grouping "Basal ruminants"
- *Bachitherium*: Basal ruminants → Ruminantia — out of the dissolved grouping "Basal ruminants"
- *Gelocus*: Basal ruminants → Ruminantia — out of the dissolved grouping "Basal ruminants"
- *Eosimias*: Basal Simiiformes → Haplorhini — out of the dissolved grouping "Basal Simiiformes"
- *Apidium*: Basal Simiiformes → Haplorhini — out of the dissolved grouping "Basal Simiiformes"
- *Catopithecus*: Basal Simiiformes → Haplorhini — out of the dissolved grouping "Basal Simiiformes"
- *Coelurus*: Basal coelurosaurs → Compsognathidae — out of the dissolved grouping "Basal coelurosaurs"
- *Ornitholestes*: Basal coelurosaurs → Compsognathidae — out of the dissolved grouping "Basal coelurosaurs"
- *Tanycolagreus*: Basal coelurosaurs → Compsognathidae — out of the dissolved grouping "Basal coelurosaurs"
- *Nqwebasaurus*: Basal ornithomimosaurs → Ornithomimosauria — out of the dissolved grouping "Basal ornithomimosaurs"
- *Harpymimus*: Basal ornithomimosaurs → Ornithomimosauria — out of the dissolved grouping "Basal ornithomimosaurs"
- *Pelecanimimus*: Basal ornithomimosaurs → Ornithomimosauria — out of the dissolved grouping "Basal ornithomimosaurs"
- *Shenzhousaurus*: Basal ornithomimosaurs → Ornithomimosauria — out of the dissolved grouping "Basal ornithomimosaurs"
- *Hexing*: Basal ornithomimosaurs → Ornithomimosauria — out of the dissolved grouping "Basal ornithomimosaurs"
- *Beishanlong*: Basal ornithomimosaurs → Ornithomimosauria — out of the dissolved grouping "Basal ornithomimosaurs"
- *Dilong*: Intermediate tyrannosauroids → Tyrannosauroidea — out of the dissolved grouping "Intermediate tyrannosauroids"
- *Khankhuuluu*: Intermediate tyrannosauroids → Tyrannosauroidea — out of the dissolved grouping "Intermediate tyrannosauroids"
- *Xiongguanlong*: Intermediate tyrannosauroids → Tyrannosauroidea — out of the dissolved grouping "Intermediate tyrannosauroids"
- *Appalachiosaurus*: Intermediate tyrannosauroids → Tyrannosauroidea — out of the dissolved grouping "Intermediate tyrannosauroids"
- *Bistahieversor*: Intermediate tyrannosauroids → Tyrannosauroidea — out of the dissolved grouping "Intermediate tyrannosauroids"
- *Dryptosaurus*: Intermediate tyrannosauroids → Tyrannosauroidea — out of the dissolved grouping "Intermediate tyrannosauroids"
- *Fukuivenator*: Basal maniraptorans → Maniraptora — out of the dissolved grouping "Basal maniraptorans"
- *Choerolophodon*: Gomphotheres and amebelodonts → Elephantiformes — out of the dissolved grouping "Gomphotheres and amebelodonts"
- *Anthracobune*: Anthracobunidae and Cambaytheriidae → Panperissodactyla — out of the dissolved grouping "Anthracobunidae and Cambaytheriidae"
- *Cambaytherium*: Anthracobunidae and Cambaytheriidae → Panperissodactyla — out of the dissolved grouping "Anthracobunidae and Cambaytheriidae"
- *Diacodexis*: Basal artiodactyls → Artiodactyla — out of the dissolved grouping "Basal artiodactyls"
- *Mixtotherium*: Anoplotherioidea and relatives → Artiodactyla — out of the dissolved grouping "Anoplotherioidea and relatives"
- *Cainotherium*: Anoplotherioidea and relatives → Artiodactyla — out of the dissolved grouping "Anoplotherioidea and relatives"
- *Dacrytherium*: Anoplotherioidea and relatives → Artiodactyla — out of the dissolved grouping "Anoplotherioidea and relatives"
- *Amphimeryx*: Anoplotherioidea and relatives → Artiodactyla — out of the dissolved grouping "Anoplotherioidea and relatives"
- *Xiphodon*: Anoplotherioidea and relatives → Artiodactyla — out of the dissolved grouping "Anoplotherioidea and relatives"
- *Archaeodon*: Entelodontidae and relatives → Artiodactyla — out of the dissolved grouping "Entelodontidae and relatives"
- *Andrewsarchus*: Entelodontidae and relatives → Artiodactyla — out of the dissolved grouping "Entelodontidae and relatives"
- *Onychonycteris*: Eocene bats → Chiroptera — out of the dissolved grouping "Eocene bats"
- *Icaronycteris*: Eocene bats → Chiroptera — out of the dissolved grouping "Eocene bats"
- *Hassianycteris*: Eocene bats → Chiroptera — out of the dissolved grouping "Eocene bats"
- *Baerus*: Unidentified → Chiroptera — out of the dissolved grouping "Unidentified"
- *Batodonoides*: Fossil eulipotyphlans → Eulipotyphla — out of the dissolved grouping "Fossil eulipotyphlans"
- *Zalambdalestes*: Zalambdalestidae and Anagalidae → Anagaloidea — out of the dissolved grouping "Zalambdalestidae and Anagalidae"
- *Anagale*: Zalambdalestidae and Anagalidae → Anagaloidea — out of the dissolved grouping "Zalambdalestidae and Anagalidae"
- *Asiatosuchus*: Basal Crocodyloidea → Crocodyloidea — out of the dissolved grouping "Basal Crocodyloidea"
- *Dongnanosuchus*: Basal Crocodyloidea → Crocodyloidea — out of the dissolved grouping "Basal Crocodyloidea"
- *Jiangxisuchus*: Basal Crocodyloidea → Crocodyloidea — out of the dissolved grouping "Basal Crocodyloidea"
- *Monolophosaurus*: Uncertain position → Megalosauroidea — out of the dissolved grouping "Uncertain position"
- *Chilesaurus*: Uncertain position → Megalosauroidea — out of the dissolved grouping "Uncertain position"
- *Gualicho*: Uncertain position → Carnosauria — out of the dissolved grouping "Uncertain position"
- *Eritherium*: Basal proboscideans → Proboscidea — out of the dissolved grouping "Basal proboscideans"
- *Phosphatherium*: Basal proboscideans → Proboscidea — out of the dissolved grouping "Basal proboscideans"
- *Barytherium*: Basal proboscideans → Proboscidea — out of the dissolved grouping "Basal proboscideans"
- *Moeritherium*: Basal proboscideans → Proboscidea — out of the dissolved grouping "Basal proboscideans"
- *Ocepeia*: Basal Paenungulata → Paenungulata — out of the dissolved grouping "Basal Paenungulata"
- *Pachyarmatherium*: Uncertain position → Cingulata — out of the dissolved grouping "Uncertain position"
- *Hapalops*: Basal Megatherioidea → Folivora — out of the dissolved grouping "Basal Megatherioidea"
- *Diabolotherium*: Basal Megatherioidea → Folivora — out of the dissolved grouping "Basal Megatherioidea"
- Arctocyonidae: Mesonychia, Arctocyonia and Periptychidae → Eutheria — out of the dissolved grouping "Mesonychia, Arctocyonia and Periptychidae"
- Mesonychia: Mesonychia, Arctocyonia and Periptychidae → Eutheria — out of the dissolved grouping "Mesonychia, Arctocyonia and Periptychidae"
- Periptychidae: Mesonychia, Arctocyonia and Periptychidae → Eutheria — out of the dissolved grouping "Mesonychia, Arctocyonia and Periptychidae"
- Triisodontidae: Mesonychia, Arctocyonia and Periptychidae → Eutheria — out of the dissolved grouping "Mesonychia, Arctocyonia and Periptychidae"
- Pantolesta: Pantolesta and Pantodonta → Eutheria — out of the dissolved grouping "Pantolesta and Pantodonta"
- Pantodonta: Pantolesta and Pantodonta → Eutheria — out of the dissolved grouping "Pantolesta and Pantodonta"
- Tillodontia: Tillodontia and Taeniodonta → Eutheria — out of the dissolved grouping "Tillodontia and Taeniodonta"
- Taeniodonta: Tillodontia and Taeniodonta → Eutheria — out of the dissolved grouping "Tillodontia and Taeniodonta"
- Apatotheria: Tillodontia and Taeniodonta → Eutheria — out of the dissolved grouping "Tillodontia and Taeniodonta"
- Anagaloidea: Anagaloidea and Leptictida → Eutheria — out of the dissolved grouping "Anagaloidea and Leptictida"
- Leptictida: Anagaloidea and Leptictida → Eutheria — out of the dissolved grouping "Anagaloidea and Leptictida"
- Didymoconidae: Anagaloidea and Leptictida → Eutheria — out of the dissolved grouping "Anagaloidea and Leptictida"
- *Yinlong*: Basal ceratopsians → Ceratopsia — out of the dissolved grouping "Basal ceratopsians"
- *Chaoyangsaurus*: Basal ceratopsians → Ceratopsia — out of the dissolved grouping "Basal ceratopsians"
- *Hualianceratops*: Basal ceratopsians → Ceratopsia — out of the dissolved grouping "Basal ceratopsians"
- *Xuanhuaceratops*: Basal ceratopsians → Ceratopsia — out of the dissolved grouping "Basal ceratopsians"
- *Liaoceratops*: Basal Neoceratopsia → Ceratopsia — out of the dissolved grouping "Basal Neoceratopsia"
- *Archaeoceratops*: Basal Neoceratopsia → Ceratopsia — out of the dissolved grouping "Basal Neoceratopsia"
- *Aquilops*: Basal Neoceratopsia → Ceratopsia — out of the dissolved grouping "Basal Neoceratopsia"
- *Auroraceratops*: Basal Neoceratopsia → Ceratopsia — out of the dissolved grouping "Basal Neoceratopsia"
- *Graciliceratops*: Basal Neoceratopsia → Ceratopsia — out of the dissolved grouping "Basal Neoceratopsia"
- *Asiaceratops*: Basal Neoceratopsia → Ceratopsia — out of the dissolved grouping "Basal Neoceratopsia"
- *Mosaiceratops*: Basal Neoceratopsia → Ceratopsia — out of the dissolved grouping "Basal Neoceratopsia"
- *Yamaceratops*: Basal Neoceratopsia → Ceratopsia — out of the dissolved grouping "Basal Neoceratopsia"
- *Zuniceratops*: Basal Ceratopsoidea → Ceratopsia — out of the dissolved grouping "Basal Ceratopsoidea"
- *Turanoceratops*: Basal Ceratopsoidea → Ceratopsia — out of the dissolved grouping "Basal Ceratopsoidea"
- *Haplocanthosaurus*: Basal diplodocoids → Diplodocoidea — out of the dissolved grouping "Basal diplodocoids"
- *Abrosaurus*: Basal camarasauromorphs → Macronaria — out of the dissolved grouping "Basal camarasauromorphs"
- *Camarasaurus*: Basal camarasauromorphs → Macronaria — out of the dissolved grouping "Basal camarasauromorphs"
- *Liaoningotitan*: Basal Somphospondyli → Macronaria — out of the dissolved grouping "Basal Somphospondyli"
- *Garumbatitan*: Basal Somphospondyli → Macronaria — out of the dissolved grouping "Basal Somphospondyli"
- *Wintonotitan*: Basal Somphospondyli → Macronaria — out of the dissolved grouping "Basal Somphospondyli"
- Dinocerata: Archaic eutherians → Eutheria — out of the dissolved grouping "Archaic eutherians (uncertain position)"
- *Pelagosuchus*: Basal Metriorhynchoidea → Metriorhynchoidea — out of the dissolved grouping "Basal Metriorhynchoidea"
- *Teleidosaurus*: Basal Metriorhynchoidea → Metriorhynchoidea — out of the dissolved grouping "Basal Metriorhynchoidea"
- *Confractosuchus*: Basal eusuchians → Eusuchia — out of the dissolved grouping "Basal eusuchians"
- *Allodaposuchus*: Basal eusuchians → Eusuchia — out of the dissolved grouping "Basal eusuchians"
- *Duerosuchus*: Basal eusuchians → Eusuchia — out of the dissolved grouping "Basal eusuchians"
- *Eodromaeus*: Basal theropods → Neotheropoda — out of the dissolved grouping "Basal theropods (uncertain position)"
- *Anteavis*: Basal theropods → Neotheropoda — out of the dissolved grouping "Basal theropods (uncertain position)"
- *Cryolophosaurus*: Dilophosauridae and relatives → Neotheropoda — out of the dissolved grouping "Dilophosauridae and relatives"
- *Dilophosaurus*: Dilophosauridae and relatives → Neotheropoda — out of the dissolved grouping "Dilophosauridae and relatives"
- *Notatesseraeraptor*: Dilophosauridae and relatives → Neotheropoda — out of the dissolved grouping "Dilophosauridae and relatives"
- *Sinosaurus*: Dilophosauridae and relatives → Neotheropoda — out of the dissolved grouping "Dilophosauridae and relatives"
- *Gongxianosaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Kotasaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Barapasaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Ohmdenosaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Rhoetosaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Spinophorosaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Tazoudasaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Vulcanodon*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Bagualia*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Chebsaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Jobaria*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Shunosaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Cetiosaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Patagosaurus*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Amanzia*: Basal sauropods → Sauropoda — out of the dissolved grouping "Basal sauropods"
- *Kulindadromeus*: Basal neornithischians → Ornithopoda — out of the dissolved grouping "Basal neornithischians"
- *Nanosaurus*: Basal neornithischians → Ornithopoda — out of the dissolved grouping "Basal neornithischians"
- *Yandusaurus*: Basal neornithischians → Ornithopoda — out of the dissolved grouping "Basal neornithischians"
- *Convolosaurus*: Basal neornithischians → Ornithopoda — out of the dissolved grouping "Basal neornithischians"
- *Hypsilophodon*: Basal neornithischians → Ornithopoda — out of the dissolved grouping "Basal neornithischians"
- *Gideonmantellia*: Basal neornithischians → Ornithopoda — out of the dissolved grouping "Basal neornithischians"
- *Cumnoria*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Camptosaurus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Bayannurosaurus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Fukuisaurus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Iguanacolossus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Istiorachis*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Lurdusaurus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Magnamanus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Ouranosaurus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Proa*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Bolong*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Jinzhousaurus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Mantellisaurus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Iguanodon*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Altirhinus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Choyrodon*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Equijubus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Haolong*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Probactrosaurus*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Xuwulong*: Ankylopollexia → Ornithopoda — out of the dissolved grouping "Ankylopollexia (non-hadrosaurs)"
- *Gongshuilong*: Basal Hadrosauroidea → Ornithopoda — out of the dissolved grouping "Basal Hadrosauroidea"
- *Bactrosaurus*: Basal Hadrosauroidea → Ornithopoda — out of the dissolved grouping "Basal Hadrosauroidea"
- *Gobihadros*: Basal Hadrosauroidea → Ornithopoda — out of the dissolved grouping "Basal Hadrosauroidea"
- *Levnesovia*: Basal Hadrosauroidea → Ornithopoda — out of the dissolved grouping "Basal Hadrosauroidea"
- *Plesiohadros*: Basal Hadrosauroidea → Ornithopoda — out of the dissolved grouping "Basal Hadrosauroidea"
- *Tethyshadros*: Basal Hadrosauroidea → Ornithopoda — out of the dissolved grouping "Basal Hadrosauroidea"
- *Paludohadros*: Basal Hadrosauroidea → Ornithopoda — out of the dissolved grouping "Basal Hadrosauroidea"
- *Laquintasaura*: Basal thyreophorans → Ankylosauria — out of the dissolved grouping "Basal thyreophorans (outside Ankylosauria)"
- *Scutellosaurus*: Basal thyreophorans → Ankylosauria — out of the dissolved grouping "Basal thyreophorans (outside Ankylosauria)"
- *Jakapil*: Basal thyreophorans → Ankylosauria — out of the dissolved grouping "Basal thyreophorans (outside Ankylosauria)"
- *Scelidosaurus*: Basal thyreophorans → Ankylosauria — out of the dissolved grouping "Basal thyreophorans (outside Ankylosauria)"
- *Kunbarrasaurus*: Basal ankylosaurs → Ankylosauria — out of the dissolved grouping "Basal ankylosaurs"
- *Minmi*: Basal ankylosaurs → Ankylosauria — out of the dissolved grouping "Basal ankylosaurs"
- *Stegouros*: Basal ankylosaurs → Ankylosauria — out of the dissolved grouping "Basal ankylosaurs"
- *Spicomellus*: Basal ankylosaurs → Ankylosauria — out of the dissolved grouping "Basal ankylosaurs"
- *Liaoningosaurus*: Basal ankylosaurs → Ankylosauria — out of the dissolved grouping "Basal ankylosaurs"
- *Chuanqilong*: Basal ankylosaurs → Ankylosauria — out of the dissolved grouping "Basal ankylosaurs"
- *Vincelestes*: Basal Cladotheria → Trechnotheria — out of the dissolved grouping "Basal Cladotheria"
- *Sinodelphys*: Basal metatherians → Metatheria — out of the dissolved grouping "Basal metatherians"
- *Asiatherium*: Basal metatherians → Metatheria — out of the dissolved grouping "Basal metatherians"
- *Didelphodon*: Basal metatherians → Metatheria — out of the dissolved grouping "Basal metatherians"
- *Pucadelphys*: Basal metatherians → Metatheria — out of the dissolved grouping "Basal metatherians"
- *Anatoliadelphys*: Basal metatherians → Metatheria — out of the dissolved grouping "Basal metatherians"
- *Peratherium*: Herpetotheriidae and Peradectidae → Metatheria — out of the dissolved grouping "Herpetotheriidae and Peradectidae"
- *Herpetotherium*: Herpetotheriidae and Peradectidae → Metatheria — out of the dissolved grouping "Herpetotheriidae and Peradectidae"
- *Mimoperadectes*: Herpetotheriidae and Peradectidae → Metatheria — out of the dissolved grouping "Herpetotheriidae and Peradectidae"
- *Libycosuchus*: Basal and various notosuchians → Notosuchia — out of the dissolved grouping "Basal and various notosuchians"
- *Simosuchus*: Basal and various notosuchians → Notosuchia — out of the dissolved grouping "Basal and various notosuchians"
- *Chimaerasuchus*: Basal and various notosuchians → Notosuchia — out of the dissolved grouping "Basal and various notosuchians"
- *Comahuesuchus*: Basal and various notosuchians → Notosuchia — out of the dissolved grouping "Basal and various notosuchians"
- *Lorosuchus*: Basal and various notosuchians → Notosuchia — out of the dissolved grouping "Basal and various notosuchians"
- *Mariliasuchus*: Advanced Ziphosuchia → Notosuchia — out of the dissolved grouping "Advanced Ziphosuchia (Notosuchidae and Sphagesauridae)"
- *Notosuchus*: Advanced Ziphosuchia → Notosuchia — out of the dissolved grouping "Advanced Ziphosuchia (Notosuchidae and Sphagesauridae)"
- *Isisfordia*: Other neosuchians → Neosuchia — out of the dissolved grouping "Other neosuchians"
- *Varanosuchus*: Other neosuchians → Neosuchia — out of the dissolved grouping "Other neosuchians"
- *Daemonosaurus*: Uncertain position → Herrerasauria — out of the dissolved grouping "Uncertain position (perhaps basal theropods)"
- *Tawa*: Uncertain position → Herrerasauria — out of the dissolved grouping "Uncertain position (perhaps basal theropods)"
- *Ptychotherates*: Uncertain position → Herrerasauria — out of the dissolved grouping "Uncertain position (perhaps basal theropods)"
- *Buriolestes*: Basal sauropodomorphs → Sauropodomorpha — out of the dissolved grouping "Basal sauropodomorphs"
- *Eoraptor*: Basal sauropodomorphs → Sauropodomorpha — out of the dissolved grouping "Basal sauropodomorphs"
- *Mbiresaurus*: Basal sauropodomorphs → Sauropodomorpha — out of the dissolved grouping "Basal sauropodomorphs"
- *Guaibasaurus*: Basal sauropodomorphs → Sauropodomorpha — out of the dissolved grouping "Basal sauropodomorphs"
- *Pampadromaeus*: Basal sauropodomorphs → Sauropodomorpha — out of the dissolved grouping "Basal sauropodomorphs"
- *Panphagia*: Basal sauropodomorphs → Sauropodomorpha — out of the dissolved grouping "Basal sauropodomorphs"
- *Saturnalia*: Basal sauropodomorphs → Sauropodomorpha — out of the dissolved grouping "Basal sauropodomorphs"
- *Bagualosaurus*: Basal sauropodomorphs → Sauropodomorpha — out of the dissolved grouping "Basal sauropodomorphs"
- *Thecodontosaurus*: Thecodontosauridae and relatives → Sauropodomorpha — out of the dissolved grouping "Thecodontosauridae and relatives"
- *Pantydraco*: Thecodontosauridae and relatives → Sauropodomorpha — out of the dissolved grouping "Thecodontosauridae and relatives"
- *Asylosaurus*: Thecodontosauridae and relatives → Sauropodomorpha — out of the dissolved grouping "Thecodontosauridae and relatives"
- *Arcusaurus*: Thecodontosauridae and relatives → Sauropodomorpha — out of the dissolved grouping "Thecodontosauridae and relatives"
- *Brasilodon*: Cynodonts and mammaliaforms → Theriimorpha — out of the dissolved grouping "Cynodonts and mammaliaforms"
- *Sioconodon*: Cynodonts and mammaliaforms → Theriimorpha — out of the dissolved grouping "Cynodonts and mammaliaforms"
- *Adelobasileus*: Cynodonts and mammaliaforms → Theriimorpha — out of the dissolved grouping "Cynodonts and mammaliaforms"
- *Fruitafossor*: Various basal mammals → Theriimorpha — out of the dissolved grouping "Various basal mammals"
- *Yeotherium*: Various basal mammals → Theriimorpha — out of the dissolved grouping "Various basal mammals"
- *Fossomanus*: Various basal mammals → Theriimorpha — out of the dissolved grouping "Various basal mammals"
- *Steropodon*: Basal monotremes → Monotremata — out of the dissolved grouping "Basal monotremes"
- *Kollikodon*: Basal monotremes → Monotremata — out of the dissolved grouping "Basal monotremes"
- *Nundasuchus*: Basal pseudosuchians → Pseudosuchia — out of the dissolved grouping "Basal pseudosuchians"
- *Ticinosuchus*: Basal pseudosuchians → Pseudosuchia — out of the dissolved grouping "Basal pseudosuchians"
- *Qianosuchus*: Basal poposauroids → Poposauroidea — out of the dissolved grouping "Basal poposauroids"
- *Benggwigwishingasuchus*: Basal poposauroids → Poposauroidea — out of the dissolved grouping "Basal poposauroids"
- *Mandasuchus*: Basal poposauroids → Poposauroidea — out of the dissolved grouping "Basal poposauroids"
- *Poposaurus*: Poposauridae and Shuvosauridae → Poposauroidea — out of the dissolved grouping "Poposauridae and Shuvosauridae"
- *Smok*: Uncertain position → Poposauroidea — out of the dissolved grouping "Uncertain position"
- *Batrachotomus*: Basal loricatans → Rauisuchia — out of the dissolved grouping "Basal loricatans"
- *Decuriasuchus*: Basal loricatans → Rauisuchia — out of the dissolved grouping "Basal loricatans"
- *Heptasuchus*: Basal loricatans → Rauisuchia — out of the dissolved grouping "Basal loricatans"
- *Prestosuchus*: Basal loricatans → Rauisuchia — out of the dissolved grouping "Basal loricatans"
- *Saurosuchus*: Basal loricatans → Rauisuchia — out of the dissolved grouping "Basal loricatans"
- *Fasolasuchus*: Basal loricatans → Rauisuchia — out of the dissolved grouping "Basal loricatans"
- *Youngosuchus*: Basal loricatans → Rauisuchia — out of the dissolved grouping "Basal loricatans"
- *Etjosuchus*: Basal loricatans → Rauisuchia — out of the dissolved grouping "Basal loricatans"
- Gracilisuchidae: Erpetosuchidae and Gracilisuchidae → Pseudosuchia — out of the dissolved grouping "Erpetosuchidae and Gracilisuchidae"
- Erpetosuchidae: Erpetosuchidae and Gracilisuchidae → Pseudosuchia — out of the dissolved grouping "Erpetosuchidae and Gracilisuchidae"
- *Lagosuchus*: Basal dinosauromorphs → Avemetatarsalia — out of the dissolved grouping "Basal dinosauromorphs"
- *Marasuchus*: Basal dinosauromorphs → Avemetatarsalia — out of the dissolved grouping "Basal dinosauromorphs"
- *Saltopus*: Basal dinosauromorphs → Avemetatarsalia — out of the dissolved grouping "Basal dinosauromorphs"
- *Pseudotribos*: Basal mammaliaforms → Mammaliamorpha — out of the dissolved grouping "Basal mammaliaforms"
- *Oxyrhabdium*: Colubroidea → Caenophidia — out of the dissolved grouping "Colubroidea (uncertain position)"
- *Diandongosuchus*: Basal phytosaurs → Phytosauria — out of the dissolved grouping "Basal phytosaurs"
- *Thrinaxodon*: Basal cynodonts → Cynodontia — out of the dissolved grouping "Basal cynodonts"
- *Dvinia*: Basal cynodonts → Cynodontia — out of the dissolved grouping "Basal cynodonts"
- *Procynosuchus*: Basal cynodonts → Cynodontia — out of the dissolved grouping "Basal cynodonts"
- *Vetusodon*: Basal cynodonts → Cynodontia — out of the dissolved grouping "Basal cynodonts"
- *Galesaurus*: Basal cynodonts → Cynodontia — out of the dissolved grouping "Basal cynodonts"
- *Breugnathair*: Jurassic squamates → Ophidia — out of the dissolved grouping "Jurassic squamates (uncertain position)"
- *Vancleavea*: Vancleaveidae and relatives → Archosauriformes — out of the dissolved grouping "Vancleaveidae and relatives"
- *Litorosuchus*: Vancleaveidae and relatives → Archosauriformes — out of the dissolved grouping "Vancleaveidae and relatives"
- *Kranosaura*: Other archosauriforms → Archosauriformes — out of the dissolved grouping "Other archosauriforms (uncertain position)"
- *Polymorphodon*: Other archosauriforms → Archosauriformes — out of the dissolved grouping "Other archosauriforms (uncertain position)"
- *Marcianosuchus*: Other archosauriforms → Archosauriformes — out of the dissolved grouping "Other archosauriforms (uncertain position)"
- *Phthinosuchus*: Uncertain position → Dinocephalia — out of the dissolved grouping "Uncertain position"
- *Biseridens*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Patranomodon*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Anomocephalus*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Tiarajudens*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Otsheria*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Suminia*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Ulemica*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Venyukovia*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Galechirus*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Galepus*: Basal anomodonts → Anomodontia — out of the dissolved grouping "Basal anomodonts"
- *Haptodus*: Basal sphenacodonts → Sphenacodontidae — out of the dissolved grouping "Basal sphenacodonts"
- *Palaeohatteria*: Basal sphenacodonts → Sphenacodontidae — out of the dissolved grouping "Basal sphenacodonts"
- *Pantelosaurus*: Basal sphenacodonts → Sphenacodontidae — out of the dissolved grouping "Basal sphenacodonts"
- *Cutleria*: Basal sphenacodonts → Sphenacodontidae — out of the dissolved grouping "Basal sphenacodonts"
- *Asaphestera*: Uncertain position → Diadectomorpha — out of the dissolved grouping "Uncertain position"
- *Ichthyostega*: Devonian stem tetrapods → Tetrapoda — out of the dissolved grouping "Devonian stem tetrapods"
- *Aulorhamphus*: Eocene fossils → Syngnathiformes — out of the dissolved grouping "Eocene fossils"
- *Gerpegezhus*: Eocene fossils → Syngnathiformes — out of the dissolved grouping "Eocene fossils"
- *Pterygocephalus*: Eocene fossils → Syngnathiformes — out of the dissolved grouping "Eocene fossils"
- *Rhamphosus*: Eocene fossils → Syngnathiformes — out of the dissolved grouping "Eocene fossils"
- *Australyichthys*: Unidentified → Syngnathiformes — out of the dissolved grouping "Unidentified"
- *Charnia*: Ediacaran biota → Metazoa — out of the dissolved grouping "Ediacaran biota (uncertain position)"
- *Dickinsonia*: Ediacaran biota → Metazoa — out of the dissolved grouping "Ediacaran biota (uncertain position)"

</details>
## Later changes

- 2026-11-17 — Revueltosauridae: Aetosauria → Pseudosuchia. *Revueltosaurus* is the sister group of aetosaurs, not one of them (Parker 2005, 2022, cited in the Revueltosauridae entry); PBDB has no record of the family. A node "Aetosauriformes" would place it more precisely.

## Pseudosuchia restructured as a phylogeny (2026-11-17)

Owner: the tree must be an approximate phylogeny of nested clades, as in the Pterosauria volume. Structure from
Nesbitt (2011) for the pseudosuchian backbone, Leardi (2025) for early crocodylomorphs, Bronzati et al. (2012)
for crocodyliforms, the aetosaur and crocodilian cladograms of the cited Wikipedia revisions
(`data/raw/tree/cladograms_2026-11-17.json`), each checked against PBDB. Genera sit in the most exclusive clade
the sources agree on; where they disagree, in the deepest shared clade with an *incertae sedis* note.

- Suchia added in Pseudosuchia — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- Paracrocodylomorpha added in Suchia — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- Loricata added in Paracrocodylomorpha — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- Gracilisuchidae: Pseudosuchia → Suchia — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- Revueltosauridae: Pseudosuchia → Suchia — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- Aetosauria: Pseudosuchia → Suchia — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- *Ticinosuchus*: Pseudosuchia → Suchia — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- Poposauroidea: Pseudosuchia → Paracrocodylomorpha — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- *Heptasuchus*: Rauisuchia → Paracrocodylomorpha — PBDB
- *Batrachotomus*: Rauisuchia → Loricata — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- *Prestosuchus*: Rauisuchia → Loricata — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- *Saurosuchus*: Rauisuchia → Loricata — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- *Fasolasuchus*: Rauisuchia → Loricata — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- *Etjosuchus*: Rauisuchia → Loricata — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- Rauisuchidae: Rauisuchia → Loricata — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- Crocodylomorpha: Pseudosuchia → Loricata — Nesbitt 2011, as reproduced in the cited Wikipedia revision of Pseudosuchia, and PBDB
- *Decuriasuchus*: Rauisuchia → Suchia — PBDB places it in Suchia
- *Youngosuchus*: Rauisuchia → Suchia — former "rauisuchian", not resolved further in PBDB
- Rauisuchia removed — paraphyletic grade ("rauisuchians"); its members are loricatans or poposauroids (Nesbitt 2011)
- Solidocrania added in Crocodylomorpha — Leardi 2025 (Crocodylomorpha revision) and PBDB
- Crocodyliformes: Crocodylomorpha → Solidocrania — Leardi 2025; PBDB
- *Junggarsuchus*: Crocodylomorpha → Solidocrania — Leardi 2025; PBDB
- Protosuchidae added in Crocodyliformes — Bronzati et al. 2012 (Crocodyliformes revision) and PBDB
- Gobiosuchidae added in Crocodyliformes — Bronzati et al. 2012 and PBDB
- *Protosuchus*: Protosuchia → Protosuchidae — PBDB; Bronzati et al. 2012
- *Hoplosuchus*: Protosuchia → Protosuchidae — PBDB; Bronzati et al. 2012
- *Orthosuchus*: Protosuchia → Protosuchidae — PBDB; Bronzati et al. 2012
- *Gobiosuchus*: Protosuchia → Gobiosuchidae — PBDB; Bronzati et al. 2012
- *Zaraasuchus*: Protosuchia → Gobiosuchidae — PBDB; Bronzati et al. 2012
- *Pedeticosaurus*: Protosuchia → Crocodyliformes — former "protosuchian"; no family agreed
- *Stegomosuchus*: Protosuchia → Crocodyliformes — former "protosuchian"; no family agreed
- *Sichuanosuchus*: Protosuchia → Crocodyliformes — former "protosuchian"; no family agreed
- *Fruitachampsia*: Protosuchia → Crocodyliformes — former "protosuchian"; no family agreed
- Protosuchia removed — a grade of early crocodyliforms, not a clade (cited Wikipedia revision); replaced by Protosuchidae and Gobiosuchidae
- Mesoeucrocodylia added in Crocodyliformes — PBDB; Notosuchia + Neosuchia (Metasuchia in Bronzati et al. 2012)
- Notosuchia: Crocodyliformes → Mesoeucrocodylia — PBDB; Bronzati et al. 2012
- Neosuchia: Crocodyliformes → Mesoeucrocodylia — PBDB; Bronzati et al. 2012
- Thalattosuchia: Crocodyliformes → Crocodylomorpha — position debated (within Neosuchia or among early crocodylomorphs; cited Wikipedia revision); PBDB places it in Crocodylomorpha — deepest shared clade
- Peirosauridae: Notosuchia → Mesoeucrocodylia — inside Notosuchia in some analyses (2014 on), outside in others (Bronzati et al. 2012; PBDB) — deepest shared clade
- Longirostres added in Crocodylia — molecular phylogenies (Crocodylia revision) and PBDB: crocodiles and gharials closer to each other than to alligators
- Crocodyloidea: Crocodylia → Longirostres — molecular phylogenies; PBDB
- Gavialoidea: Crocodylia → Longirostres — molecular phylogenies; PBDB
- Gavialidae added in Gavialoidea — Gavialoidea revision cladogram (Gavialis + Tomistoma) and PBDB (with tomistomines and gryposuchines)
- *Gavialis*: Gavialoidea → Gavialidae — PBDB; Gavialoidea revision
- *Tomistoma*: Gavialoidea → Gavialidae — PBDB; Gavialoidea revision
- *Gryposuchus*: Gavialoidea → Gavialidae — PBDB; Gavialoidea revision
- *Piscogavialis*: Gavialoidea → Gavialidae — PBDB; Gavialoidea revision
- *Hanyusuchus*: Gavialoidea → Gavialidae — PBDB; Gavialoidea revision
- *Rhamphosuchus*: Gavialoidea → Gavialidae — PBDB; Gavialoidea revision
- *Toyotamaphimeia*: Gavialoidea → Gavialidae — PBDB; Gavialoidea revision
- *Megadontosuchus*: Gavialoidea → Gavialidae — PBDB; Gavialoidea revision
- Planocraniidae: Crocodylia → Eusuchia — recovered inside Crocodylia by Rio & Mannion 2021, outside by other analyses (cited Wikipedia revision) — deepest shared clade
- *Aetosauroides*: Aetosaurinae → Aetosauria — outside Stagonolepididae/Aetosauridae (aetosaur cladogram in the cited revision; PBDB)
- Desmatosuchia added in Aetosauridae — aetosaur cladogram in the cited Aetosauria revision and PBDB
- *Stagonolepis*: Aetosaurinae → Desmatosuchia — cladogram; PBDB
- Desmatosuchinae: Aetosauridae → Desmatosuchia — cladogram; PBDB
- *Neoaetosauroides*: Aetosaurinae → Desmatosuchinae — cladogram; PBDB
- *Rioarribasuchus*: Desmatosuchinae → Typothoracinae — cladogram (Paratypothoracisini); PBDB
- *Lotosaurus*: Ctenosauriscidae → Poposauroidea — its own lineage (Lotosauridae), not a ctenosauriscid (Nesbitt 2011 cladogram in the Poposauroidea revision)

## Kept against PBDB (open questions for reviewers)

- **PBDB homonyms**, not real conflicts: *Archaea* (a spider genus in PBDB), Proboscidea (an insect group), Booidea, and genera such as *Lachesis*, *Regina*, *Aspidura*, *Hemiaspis*, *Cystophora*, *Trichechus*, *Cynocephalus*, *Gordonia*, *Rubidgea*, *Burnetia*, *Murina*, *Cuniculus*.
- **Snakes**: PBDB keeps an older scheme (e.g. vipers, elapids and lamprophiids in a broad Colubroidea, pythons and sand boas in Boidae). The tree follows the current molecular families (Viperidae, Elapoidea, Pythonidae, Erycidae, Charinidae…).
- **Feliform carnivores**: Herpestidae, Eupleridae and Hyaenidae stay in Herpestoidea (molecular classification); PBDB puts them in Viverroidea.
- **South American native ungulates** (Notoungulata, Astrapotheria, Pyrotheria, Xenungulata): PBDB places them in Afrotheria; collagen and molecular studies relate at least notoungulates and litopterns to Perissodactyla (Panperissodactyla). Kept in Meridiungulata as in the tree; the monophyly of Meridiungulata itself is doubtful.
- **Archelosauria vs Archosauromorpha**: PBDB nests turtles within Archosauromorpha (Archelosauria inside it); the tree keeps Archosauromorpha inside Archelosauria (turtles as its sister). Both views are current.
- **Phytosauria**: PBDB places it in Pseudosuchia; recent analyses often find it just outside Archosauria. Kept where it was.
- **Silesauridae** (PBDB: stem ornithischians), **Heterodontosauria** (PBDB: in Ornithopoda), **Desmostylia** (PBDB: in Perissodactyla), **Viperinae** (PBDB: in Crotalinae), **Homalopsidae** (PBDB: in Colubridae), **Erycidae** (PBDB: in Boidae), **Paralligatoridae** (PBDB: in Eusuchia), **Barbourofelidae** (PBDB: in Nimravidae), **Estemmenosuchidae** (PBDB: Gorgonopsia): kept, the literature is divided or disagrees with PBDB.
- **Bovid, cricetid, armadillo and sloth families/subfamilies**: PBDB lumps several (e.g. bovid tribes in Antilopinae, voles and New World rats in Cricetinae, armadillos in Dasypodidae); the tree keeps the separate groups recognised by current mammal classifications.
- **Archaic eutherians** (Arctocyonidae, Mesonychia, Periptychidae, Triisodontidae, Pantodonta, Pantolesta, Tillodontia, Taeniodonta, Dinocerata, Leptictida, Anagaloidea…): now directly in Eutheria; PBDB puts several in Laurasiatheria, but their placement is very uncertain.
- **Theriimorpha**: the tree uses it for several Mesozoic mammal groups; its contents should be checked against current definitions.
- Single genera where PBDB and recent work disagree and the tree was kept: *Eomaia*, *Sinodelphys*, *Asaphestera*, *Chilesaurus*, *Gualicho*, *Sciurumimus*, *Saltopus*, *Dickinsonia*, *Cryolophosaurus*, *Pseudotribos*, and genera PBDB puts deeper than the tree (e.g. titanosaurs in Saltasauroidea, anoplotheriids in Tylopoda, herpetotheriids in Marsupialia).

## Pseudosuchia becomes a volume (2026-11-17)
The 59 clade nodes of Pseudosuchia left `backbone.json` for `entries/pseudosuchia/clades` (same structure as
above). Ids with a prefix were shortened to the clade name in lower case (e.g. `notosuchia__sebecosuchia` →
`sebecosuchia`, `crocodylia__alligatoroidea__alligatoridae` → `alligatoridae`); the backbone genus nodes now
point to the new ids.

## Misspelled genus nodes of Pseudosuchia (2026-11-21)
Backbone genus nodes with misspelled names were replaced by entries under the valid spelling (PBDB and English Wikipedia):
Xilosuchus → Xilousuchus, Pseudohesperosuchus → Pseudhesperosuchus, Fruitachampsia → Fruitachampsa,
Gracilineusteus → Gracilineustes, Racheosaurus → Rhacheosaurus, Phosphatosuchus → Phosphatosaurus.
Pelagosuchus was a duplicate of Pelagosaurus (already an entry) and was removed.


## Euphorosuchus replaced by Eosphorosuchus (2026-11-21)
The backbone node "Euphorosuchus" had no source in PBDB or English Wikipedia. The 2026 genus Eosphorosuchus (Margulis-Ohnuma et al., Chinle Formation, New Mexico) is probably the intended name. The node was removed and Eosphorosuchus got a genus entry in Crocodylomorpha (source: the naming paper, Proceedings of the Royal Society B 2026).

## 2026-11-22 — Sauropodomorpha, batch 3
- Rinconsaurus moved from Lognkosauria to Titanosauria (incertae sedis): the cited sources call it a titanosaurid related to Aeolosaurus (Rinconsauria / Aeolosauridae), none links it to Lognkosauria. PBDB parent is Rinconsauria.

## 2026-11-22 — Thyreophora volume (Ornithischia part A)
- Clade nodes of Thyreophora (Stegosauria, Huayangosauridae, Stegosauridae, Ankylosauria, Ankylosauridae, Nodosauridae) moved from the backbone to `entries/thyreophora`; their ids lost the `parent__` prefix (e.g. `ankylosauria__nodosauridae` → `nodosauridae`) and the waiting genus nodes were re-parented to the new ids.
- Polacanthidae removed as a node and its four genera (Gargoyleosaurus, Gastonia, Mymoorapelta, Polacanthus) placed directly in Ankylosauria until the family gets an entry (the Wikipedia revision could not be read); PBDB lists them as Polacanthidae. A 2023 review (Raven et al.) keeps Polacanthidae as a family within a split of the nodosaurids.

## 2026-11-22 — Marginocephalia volume (Ornithischia part A)
- Clade nodes of Marginocephalia (Ceratopsia, Pachycephalosauria, Psittacosauridae, Leptoceratopsidae, Protoceratopsidae, Ceratopsidae, Centrosaurinae, Chasmosaurinae) moved from the backbone to `entries/marginocephalia`; ids lost the `parent__` prefix (e.g. `ceratopsia__ceratopsidae__centrosaurinae` → `centrosaurinae`) and the waiting genus nodes were re-parented. The volume attaches to Neornithischia.

## 2026-11-23 — Basal thyreophorans out of Ankylosauria (literature over backbone)
Rule of 2026-11-23 (owner): where the backbone and the literature diverge, the literature wins.
- *Scutellosaurus*, *Scelidosaurus*: Ankylosauria → Thyreophora. Both are basal thyreophorans outside Eurypoda in recent analyses (Madzia et al. 2021 and the Thyreophora article cited in `entries/thyreophora/clades/thyreophora.yaml`).
- *Jakapil*: Ankylosauria → Thyreophora, *incertae sedis within Thyreophora*. Riguetti et al. 2022 (Scientific Reports 12:11621, doi:10.1038/s41598-022-15535-6) recover it as a basal thyreophoran outside Eurypoda or as a stem ankylosaur, depending on the data matrix; Fonseca et al. 2024 recover it as a basal ankylosaur. The deepest clade they share is Thyreophora (M2).
- *Laquintasaura*: Ankylosauria → Ornithischia, *incertae sedis within Ornithischia*. Barrett et al. 2014 described it as an early ornithischian, and later work (Baron et al. 2016, cited by Raven & Maidment) treats it as a probable basal thyreophoran; the deepest clade they share is Ornithischia (M2). It belongs to part B (basal ornithischians).
- Kept in Ankylosauria after checking: *Stegouros*, *Kunbarrasaurus*, *Minmi* (Parankylosauria, the earliest branch of Ankylosauria in Soto-Acuña et al. 2021, replicated in later analyses). The doubt noted on 2026-11-22 about Stegouros being outside Ankylosauria is withdrawn.
- *Lesothosaurus* (PBDB: Thyreophora; no backbone node): left out of the Thyreophora volume and reserved for Part B as *incertae sedis within Ornithischia*. Analyses disagree: Butler et al. 2008, Boyd 2015 and Baron et al. 2017a recover it (with *Laquintasaura*) as an early unarmoured thyreophoran, while other analyses place it outside Thyreophora (Yao et al. 2022, eLife 11:e75248, doi:10.7554/eLife.75248, summarising both views); by M2 it sits in the deepest shared clade. It is not written in the Thyreophora volume.

## 2026-11-24 — Ornithischia part B (branch entry/ornithischia-b)
- Volumes Ornithischia, Heterodontosauria and Ornithopoda created; their clade nodes (`ornithischia`, `heterodontosauria`, `ornithopoda`, `ornithopoda__elasmaria`, `__rhabdodontomorpha`, `__dryosauridae`, `__hadrosauridae` and its two subfamilies, `__thescelosauridae`) left the backbone for the clade entries.
- *Daurosaurus*, *Vectidromeus*, *Hypsilophodon*: kept directly in Ornithopoda as *incertae sedis*; the sources disagree (hypsilophodontid, euiguanodontian, neornithischian).
- Basal neornithischians (*Nanosaurus*, *Kulindadromeus*, *Yandusaurus* and others) placed in Ornithischia as *incertae sedis*: no Neornithischia clade is defined in this volume.
- Lesothosaurus, Laquintasaura, Pisanosaurus, Agilisaurus, Hexinlusaurus: *incertae sedis within Ornithischia* (see the 2026-11-23 notes above).

## 2026-11-25 — Ornithopoda subgroups (Iguanodontia and below)

Owner's request: organise the ornithopods in subgroups instead of leaving 87 genera directly in Ornithopoda; follow PBDB
and English Wikipedia. Raw material: `data/raw/tree/clade_sources_2026-11-25_ornithopoda.json` (Wikipedia revisions, texts and
citations; PBDB records and children), downloaded by `.github/workflows/clades.yml`.

New clade entries (all in `entries/ornithopoda/clades/`): Iguanodontia (infraorder), Euiguanodontia, Dryomorpha,
Ankylopollexia, Styracosterna, Iguanodontidae (family), Hadrosauroidea, Tenontosauridae (family). PBDB hierarchy followed:
Ornithopoda → Iguanodontia → Euiguanodontia → Dryomorpha → Ankylopollexia → Styracosterna → Hadrosauroidea → Hadrosauridae.
Existing clades moved: Rhabdodontomorpha → Iguanodontia (Tenontosauridae inside it, as in PBDB and Fonseca et al. 2024),
Elasmaria → Euiguanodontia, Dryosauridae → Dryomorpha, Hadrosauridae → Hadrosauroidea. Thescelosauridae stays in Ornithopoda
(PBDB); Fonseca et al. 2024 put it outside Cerapoda, still to be reviewed.

Genera moved from Ornithopoda to the subgroups: 79, by the PBDB parent of each genus checked against the lead of its English
Wikipedia article. Where the two disagree the genus sits in the deepest clade both share, with `incertae_sedis: true` (M2):
Bolong and Morelladon (Styracosterna), Altirhinus and Ouranosaurus (Ankylopollexia), Choyrodon (Iguanodontia). Not made:
Hadrosauriformes (PBDB: Siamodon, Brighstoneus, Proa, Comptonatus and Hadrosauroidea; the sources give no definition or diagnosis) and
Neoiguanodontia, so their genera sit in Styracosterna and Ankylopollexia, with a curation note; Telmatosauridae (PBDB family of 2026) and
Camptosauridae (PBDB lists no genus in it). Jinzhousaurus (backbone genus) moved to Iguanodontidae (PBDB). Iguanodon sits in
Iguanodontidae, the family defined from it, although PBDB puts it directly in Ankylopollexia. Hypsilophodon, Gideonmantellia, Vectidromeus,
Daurosaurus, Burianosaurus and the three elasmarian-candidates stay in Ornithopoda.

## 2026-11-26 — Theropoda I (non-maniraptoran theropods)

New volume `entries/theropoda1` with 36 clade entries and 254 genus entries. The volume root Theropoda attaches to Saurischia.
Backbone nodes replaced by volume clades were removed: Theropoda, Neotheropoda, Tetanurae, Coelurosauria, Ceratosauria,
Megalosauroidea, Compsognathidae, Megaraptora, Tyrannosauroidea, Ornithomimosauria, the grade Carnosauria, the legacy double-id nodes
of the PBDB-built backbone (e.g. `ceratosauria__abelisauridae`, `tyrannosauroidea__tyrannosauridae__albertosaurinae`) and Deinocheiridae
(no genus of its own: its genera sit in Ornithomimosauria). Maniraptora stays a backbone node below Coelurosauria; maniraptoran groups
(Alvarezsauria, Therizinosauria, Unenlagiidae and the rest of Maniraptora) are not in this volume.
Structure: Averostra → Ceratosauria (Ceratosauridae, Noasauridae, Abelisauridae → Brachyrostra → Furileusauria) and Tetanurae →
Megalosauroidea (Megalosauridae, Spinosauridae → Baryonychinae, Spinosaurinae; Piatnitzkysauridae), Avetheropoda → Allosauroidea
(Allosauridae, Metriacanthosauridae, Carcharodontosauria → Carcharodontosauridae, Neovenatoridae) and Coelurosauria (Tyrannosauroidea
→ Proceratosauridae, Tyrannosauridae → Tyrannosaurinae, Albertosaurinae; Compsognathidae; Ornithomimosauria → Ornithomimidae).
Megaraptora (with Megaraptoridae) is attached directly to Tetanurae: analyses place it among allosauroids or among coelurosaurs (M2).
Backbone genera moved: Eodromaeus and Anteavis → Theropoda (Anteavis has no entry), Chilesaurus → Tetanurae, Ubirajara → Compsognathidae,
Tromerosaurus → Tyrannosauridae; the misspelled node Baryonix was deleted (Baryonyx has an entry).
Placement rule as in the Ornithopoda review: PBDB parent checked against the lead of the English Wikipedia article; where they differ the
genus sits in the deepest clade both share with `incertae_sedis: true`. Left out of the volume: Anteavis, Protoavis, Sauropus,
Saurornithoides, Himeoolithus, Ovoraptor, Yaverlandia (not theropods of this volume or not valid genera in the sources used).
