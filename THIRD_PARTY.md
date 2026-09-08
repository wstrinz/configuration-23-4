# Third-party material

The root MIT license covers this project's original formalization and prose.
Dependencies retain their own licenses.

scripts/verify-comparator.sh and scripts/landrun-wrapper.sh are adapted from
PalomarRegistry/PalomarTemplate at commit
128a6c5ce5f48622e69927ccd639cbff401022e8 (Apache-2.0), via the maintainer's
earlier math-stuff packaging. The verification script's cache request is
narrowed to this project's Mathlib imports. The sandbox policy is preserved.
The upstream Apache license is in third_party/PalomarTemplate-LICENSE.

schema/v0.4.schema.json comes from mathlib-initiative/formalization.yaml at
99c678e569c7c4c0772db297c5ddd5e4c9b6322e. Its upstream license is included
as third_party/formalization-yaml-LICENSE. Metadata validation uses this
vendored immutable schema rather than a changing remote schema.

The Linux verification script pins Comparator, Lean4Export, NanoDa and Landrun
to full Git revisions. The dependency manifest pins Mathlib and its closure.
These projects' sources and licenses are fetched as build dependencies and
are not represented as authored by this project's maintainer.
