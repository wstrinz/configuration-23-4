# Zenodo release and citation

This repository is archived by Zenodo under MIT. Its stable concept DOI is:

- concept DOI: [10.5281/zenodo.22662692](https://doi.org/10.5281/zenodo.22662692)

The Palomar-registered release, `v1.0.1`, dated 2026-09-08, has these immutable
links:

- version DOI: [10.5281/zenodo.22663385](https://doi.org/10.5281/zenodo.22663385)
- record: https://zenodo.org/records/22663385
- source release: https://github.com/wstrinz/configuration-23-4/releases/tag/v1.0.1

It records commit `94fc8964562fa9e246c8c7b1657e2e135bda35f6`, the snapshot registered as
[PALOMAR-2026-09-08-000004 v1](https://palomar-registry.org/entry.html?id=PALOMAR-2026-09-08-000004&version=1).

Release `v1.1.0` adds the E2 witness and polarity, the V4 completeness and
exclusion receipts, exact classification of the two survivor loci, the
E1/E2/CT1-S1 combinatorial audit, and the correspondence-ready one-page PDF.
It is a GitHub/Zenodo evidence release; the Palomar record above remains a
registration of the narrower `v1.0.1` Lean-existence snapshot.

The initial release, `v1.0.0`, has these immutable links:

- version DOI: [10.5281/zenodo.22662693](https://doi.org/10.5281/zenodo.22662693)
- record: https://zenodo.org/records/22662693
- source release: https://github.com/wstrinz/configuration-23-4/releases/tag/v1.0.0

The concept DOI identifies the continuing project. The version DOI identifies
the immutable `v1.0.0` snapshot at commit
`09cff2fef8e135cfe8cd0946ca791b3f3e88f723`.

The inspected example is
[plane-jacobian-72-108](https://github.com/wstrinz/plane-jacobian-72-108).
Its CITATION.cff uses concept DOI `10.5281/zenodo.21534895` and separately labels
a historical version DOI. Neither identifier belongs to this construction.

## Verification

The `v1.0.1` record was independently downloaded and integrity-checked before
the evidence release. The `v1.1.0` record and archive are checked separately
after the GitHub-Zenodo integration creates them.

The concept DOI belongs in the README badge and CITATION.cff. Do not put it into
.zenodo.json's `doi` field: that field identifies
the individual record. Let the GitHub integration allocate each release DOI.
Do not move the published tag to include the DOI after the fact. The first
archive can legitimately contain pre-DOI citation metadata. Later metadata
commits and Palomar submissions should identify their own exact commit, and
must not be described as byte-identical to an earlier archive.

Zenodo prefers .zenodo.json when both metadata files exist, so keep author,
title, license and release information synchronized. No token or publishing
workflow is needed in this package for the normal GitHub integration.

Procedure sources checked 2026-09-08:
- [Enable a repository](https://help.zenodo.org/docs/github/enable-repository/)
- [Describe software and metadata precedence](https://help.zenodo.org/docs/github/describe-software/)
- [Archive software](https://help.zenodo.org/docs/github/archive-software/)

## Sharing artwork

Use `assets/sharing-cover.png` for a social post; its generation prompt and
provenance are recorded in `assets/README.md`. The artwork is interpretive.
Use `configuration.svg` and `coordinates.json` for exact geometry.
