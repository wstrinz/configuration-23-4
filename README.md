# A real affine (23_4) configuration

<p align="center">
  <img src="assets/all-finite-header.svg" width="100%" alt="All 23 points and 23 lines of the real (23,4) configuration">
</p>

There exist 23 distinct points and 23 distinct straight lines in the real
affine plane, with exactly four selected lines through each selected point
and exactly four selected points on each selected line.

This repository gives explicit rational coordinates and a Lean proof of
existence over the real numbers. The proof requires no search program,
numerical tolerance, census certificate or assumption about realizability.

## Read the result

- [Challenge.lean](Challenge.lean): the independent statement, 35 lines.
- [Solution.lean](Solution.lean): the coordinates and complete proof, 93 lines.
- [PROOF.md](PROOF.md): a compact arithmetic proof using eight sign orbits.
- [STATEMENT_AUDIT.md](STATEMENT_AUDIT.md): how the formal conditions express
  distinct real points and straight lines with exact degree four.
- [coordinates.json](coordinates.json): the rational homogeneous witness from
  which the displayed affine coordinates were obtained.
- [all-finite-header.svg](assets/all-finite-header.svg): the exact, orbit-colored
  chart used above, with all 23 points visible. The line at infinity is
  `x + 3z = 0`; [configuration.svg](configuration.svg) gives another all-finite
  chart optimized for compact affine coordinates.

The deliberate hole in Challenge is a statement for Comparator to check.
Solution does not import Challenge and has no unproved declarations.
The kernel axiom dependencies are the standard `propext`, `Classical.choice`
and `Quot.sound`. A separate [Std-only integer certificate](standalone/Witness.lean)
uses ordinary `decide` and no axioms.

## Build

Install Lean's standard elan toolchain manager, then run:

```sh
lake exe cache get Mathlib.Data.Real.Basic Mathlib.Data.List.Pairwise Mathlib.Tactic.NormNum
lake build
lean standalone/Witness.lean
```

The project pins Lean 4.32.0 and the full Mathlib dependency graph. The
committed modules are self-contained; Python and the original research
repository are not needed for this Lean build.

For metadata validation, using Python 3.10 or later:

```sh
python3 -m venv .cache/metadata
.cache/metadata/bin/pip install -r requirements-validation.txt
.cache/metadata/bin/python scripts/check_metadata.py
```

For the independent exported-proof checks, use Linux with Git, Lean/Lake,
Go 1.24 or later and Rust/Cargo installed:

```sh
bash scripts/verify-comparator.sh
python3 scripts/negative_controls.py
```

The second command belongs in a disposable checkout. It deliberately changes
Solution temporarily, tests rejection, restores the exact original bytes and
rebuilds. Do not run it concurrently with an editor or build. The verifier
retains the Landrun sandbox restrictions and enables NanoDa. Exact tool pins,
executed results and limitations are in [VERIFICATION.md](VERIFICATION.md).
The included GitHub Actions workflow repeats these checks after export.

## Scope and provenance

The formal theorem establishes existence over R. Its explicit witness has
rational coordinates; rationality is not a separate quantified Lean theorem.
No uniqueness, complete classification, or publication-priority claim is made.
[LITERATURE.md](LITERATURE.md) records dated historical sources and the limits
of the present literature audit. The construction addresses the existence
question discussed by [Cuntz (2017/2018)](https://arxiv.org/abs/1705.00927).

Will Strinz directed the project and is the author and responsible maintainer.
Codex assisted discovery, exact checks, formalization and packaging.
[formalization.yaml](formalization.yaml) discloses sources, automation and
review. There has been no independent human peer review or Palomar registration.
The project is MIT licensed; third-party materials retain the licenses
listed in [THIRD_PARTY.md](THIRD_PARTY.md).

## Release and submission

This is the focused public repository for the construction and formal proof.
See [SUBMISSION.md](SUBMISSION.md) for the export and final snapshot steps.
Palomar's submission host is https://submit.palomar-registry.org/.
Nothing here automatically submits or registers the project.

## Citation and sharing

See [ZENODO.md](ZENODO.md) for the first-release DOI handoff and
[CITATION.cff](CITATION.cff) for citation metadata. No DOI has been minted yet.
The [generated sharing cover](assets/sharing-cover.png) is available with its
[prompt and provenance](assets/README.md). The exact construction is also
available as a text-free [1500 x 900 PNG](assets/all-finite-header.png) for
sharing; use [the corresponding SVG](assets/all-finite-header.svg) when a
scalable figure is preferable.
