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
