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

Its immutable links are:

- version DOI: [10.5281/zenodo.22666118](https://doi.org/10.5281/zenodo.22666118)
- GitHub release: [v1.1.0](https://github.com/wstrinz/configuration-23-4/releases/tag/v1.1.0)
- exact release commit: [`bba394fbe2667b0fafc10efd72b427becc4ddaaa`](https://github.com/wstrinz/configuration-23-4/commit/bba394fbe2667b0fafc10efd72b427becc4ddaaa)

Release `v1.2.0` adds the checked acknowledgment and comparison record for
Wenhao Lu's independent work. Its immutable links are:

- version DOI: [10.5281/zenodo.22690324](https://doi.org/10.5281/zenodo.22690324)
- record: https://zenodo.org/records/22690324
- GitHub release: [v1.2.0](https://github.com/wstrinz/configuration-23-4/releases/tag/v1.2.0)
- exact release commit: [`7a5845d67485c507bee8cfb74c7e524097bc55ca`](https://github.com/wstrinz/configuration-23-4/commit/7a5845d67485c507bee8cfb74c7e524097bc55ca)

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

The `v1.2.0` Zenodo archive was independently downloaded and passed a complete
ZIP integrity test. It is `wstrinz/configuration-23-4-v1.2.0.zip`, 3,052,383
bytes, with MD5 `4bbaa97a21938f136ebcecd79361e8ff` and SHA-256
`76600baf258f79e1ad8c8519151105837e32a3f49feb52f073f72d86c642516f`.
Its root identifies release commit `7a5845d`; it contains the independent-work
acknowledgment and verification receipt, the public evidence tree, and
`docs/exact-one-page.pdf`. That PDF has SHA-256
`830a8dadcb470191ed2d06afd9943c24a20962a9bff853a11566d9b6c9dcadf0`, matching
the checked repository attachment byte for byte.

The `v1.1.0` Zenodo archive was independently downloaded and passed a complete
ZIP integrity test. It is `wstrinz/configuration-23-4-v1.1.0.zip`, 3,048,037
bytes, with MD5 `969603c48285a15fb7812b651b9ba75a`; its root identifies release
commit `bba394f`. It contains the public evidence tree and
`docs/exact-one-page.pdf`. That PDF has SHA-256
`830a8dadcb470191ed2d06afd9943c24a20962a9bff853a11566d9b6c9dcadf0`, matching
the checked repository attachment byte for byte.

The earlier `v1.0.1` archive was also independently downloaded and
integrity-checked before the evidence release.

## Independent work

Wenhao Lu independently obtained the same two configurations and an
independent classification of the Klein-four-symmetric case by a different
computational route. His draft was communicated to the maintainer on September
9, 2026; Lu reports that it was written September 6 and submitted as JMM 2027
abstract 66522 on September 7. The public source and local replay scope are
recorded in [evidence/independent-work](evidence/independent-work/README.md).

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
