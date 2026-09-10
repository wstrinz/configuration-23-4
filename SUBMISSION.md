# Export and submission handoff

The contents of this directory form a standalone repository root. They include
the actual proof development, so the metadata identifies it as substantive
development rather than a wrapper around a private campaign dependency.
No parent-relative path or private Git remote is required for the build.

## Export

Run `python3 scripts/export_release.py` to create an exact source manifest
and release.zip. The exporter includes only its declared release file families,
refuses symlinks and large files, and omits build caches, Git history and
compiled output. `python3 scripts/export_release.py --check` verifies the
manifest. The archive's executable bits preserve the verification shell scripts.

The maintainer authorized this focused public repository on 2026-09-08.
Its root contains the verified release sources including dotfiles.
The root LICENSE is MIT, as selected by Will Strinz. No license is assigned to
unrelated files in the original campaign by this export.

## Archived submission record

The public repository's Zenodo integration and citation metadata are recorded
in [ZENODO.md](ZENODO.md). Release `v1.0.1` has version DOI
`10.5281/zenodo.22663385`. Palomar registered its exact commit
`94fc8964562fa9e246c8c7b1657e2e135bda35f6` as
[PALOMAR-2026-09-08-000004 v1](https://palomar-registry.org/entry.html?id=PALOMAR-2026-09-08-000004&version=1).

The following checklist records the intake preparation used for that snapshot:

1. Incorporate the parallel literature review, updating LITERATURE.md and
   formalization.yaml if it finds prior constructions or source corrections.
   Existing wording avoids asserting publication priority.
2. Run the provided CI in the focused repository. Local Linux checks are
   recorded, but a GitHub Actions run is a distinct environment and must be
   observed rather than inferred from its workflow file.
3. Verify metadata, archive hashes, root license and the exact public commit.
   Regenerate the export manifest if any tracked release input changes.
4. Choose the full 40-character SHA of the pushed focused-repository commit.
   Do not submit the earlier private campaign SHA or use a moving branch name.

## Palomar inputs

Use wstrinz/configuration-23-4 and its final full commit SHA. The
project directory is the repository root. Conventional paths are:

```
Challenge.lean
Solution.lean
comparator.json
formalization.yaml
```

The compared theorem is Config23.exists_configuration. Will Strinz is the
author and responsible maintainer. A maintainer submission can declare that
relationship; an agent acting for the maintainer needs explicit submission
authorization. No approval from a cited background-source author is claimed.

Follow the current instructions at https://palomar-registry.org/how-to-submit.
An agent must read https://submit.palomar-registry.org/llms.txt and use its
documented protocol rather than drive the browser form. Repository/tag/gist
authorization and registration occur outside the build. Both were completed for
the immutable `v1.0.1` snapshot.

Palomar's automated review and independent kernel checks do not establish
publication priority or constitute human expert peer review. The maintainer
separately approved permanent registration after reading the completed review.

The later `v1.1.0` GitHub/Zenodo release publishes the broader V4-sector
evidence. It does not change the scope of Palomar registration v1, which
remains attached to the `v1.0.1` existence snapshot.
Its immutable version DOI is
[10.5281/zenodo.22666118](https://doi.org/10.5281/zenodo.22666118).

Release `v1.2.0` adds the checked acknowledgment and comparison record for
Wenhao Lu's independent work. It is archived under immutable version DOI
[10.5281/zenodo.22690324](https://doi.org/10.5281/zenodo.22690324) at exact
release commit `7a5845d67485c507bee8cfb74c7e524097bc55ca`.
