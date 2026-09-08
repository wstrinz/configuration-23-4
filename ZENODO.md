# Zenodo release and citation

Prepared for Will Strinz under MIT as release `v1.0.0`, dated 2026-09-08.
No DOI has been minted for this package.
The public repository is https://github.com/wstrinz/configuration-23-4.
Its Zenodo integration was checked through the repository's GitHub hook list on
2026-09-08 and is not yet enabled. These files prepare that step; they do not
activate the integration.

The inspected example is
[plane-jacobian-72-108](https://github.com/wstrinz/plane-jacobian-72-108).
Its CITATION.cff uses concept DOI `10.5281/zenodo.21534895` and separately labels
a historical version DOI. Neither identifier belongs to this construction.

## Before the first release

1. Confirm `repository-code` in CITATION.cff matches the public repository.
   The repository URL is already populated for configuration-23-4.
2. In the maintainer's Zenodo account, open GitHub, sync the repositories, and
   enable this specific repository. Existing integration for another repository
   does not establish that this new one is enabled.
3. The selected release is tag `v1.0.0`, dated 2026-09-08. Matching values are
   populated in both metadata files. Regenerate manifest.json, commit, push,
   and observe the focused repository CI before publishing the GitHub release.
4. Publish the release from the reviewed immutable commit. Observe successful
   archival in Zenodo and verify the archived source, title, author, license,
   version and repository association. Record both returned DOI identifiers.

## After successful archival

Use the concept DOI for the continuing project and its README DOI badge. Use
the version DOI when citing the exact archived proof snapshot. In a subsequent
commit, add the observed concept DOI as `doi` in CITATION.cff and identify it as
a concept DOI in `identifiers`. If listing version DOIs, label each with its
specific release; never carry an old snapshot DOI forward as the new version.
Add DOI links to the README and release notes only after verifying them.

Do not put a concept DOI into .zenodo.json's `doi` field: that field identifies
the individual record. Let the GitHub integration allocate each release DOI.
Do not move the published tag to include the DOI after the fact. The first
archive can legitimately contain pre-DOI citation metadata. Later metadata
commits and Palomar submissions should identify their own exact commit, and
must not be described as byte-identical to an earlier archive.

Zenodo prefers .zenodo.json when both metadata files exist, so keep author,
title, license and release information synchronized. No token or publishing
workflow is needed in this package for the normal GitHub integration.

Sources checked 2026-09-08:
- [Enable a repository](https://help.zenodo.org/docs/github/enable-repository/)
- [Describe software and metadata precedence](https://help.zenodo.org/docs/github/describe-software/)
- [Archive software](https://help.zenodo.org/docs/github/archive-software/)

## Sharing artwork

Use `assets/sharing-cover.png` for a social post; its generation prompt and
provenance are recorded in `assets/README.md`. The artwork is interpretive.
Use `configuration.svg` and `coordinates.json` for exact geometry.
