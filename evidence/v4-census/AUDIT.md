# V4 enumeration-completeness audit v1 — artifacts

**Task:** `v4-enumeration-completeness-audit-v1`. **Lane:** `DKW-LOI`,
research Opus, delegation disabled. **Base:**
`ef19820a41e02e2def8b717bee65afbc8c2e11e9`. **Graph effect:** `NONE`.
**Authority:** `RECONNAISSANCE` until DKC intake. `decides = []`.

Audits whether the accepted 5,299-object corpus
(`artifacts/v4-sidecar-full-recanonicalization-v1/**`) exhausts every bare
`(23_4)` incidence type arising from a faithful geometric
`V4 <= PGL_3(R)` action. This is a proof/generator-completeness audit; it
is not an S0–S3 run and asserts nothing about geometric realizability.

## Frozen inputs and their pinned hashes

Sidecar source commit `858589eb36b2606460f1cb25966b490d857e0e77`, read as
inert data through `git cat-file` only; the sidecar's canonicalization
authority is never imported.

| blob sha1 | bytes | path at the sidecar commit |
|---|---|---|
| `0292e5f7c97f5ba5545cb6df0319d5a38d77a5dc` | 23318 | `artifacts/v4-cell-census-v1/DERIVATION.md` |
| `4418fbb43470365c66ab17a36209215f6a9d1ff3` | 11343 | `artifacts/v4-cell-census-v1/RECEIPT.md` |
| `0b17fcb301f9f2de90db18e5ee9bb5ce7e4a5381` | 50320 | `artifacts/v4-cell-census-v1/code/v4census.py` |
| `84a897cdbe56f1e2fa2cb3df1961eb17644efa32` | 3950 | `artifacts/v4-cell-census-v1/code/run_census.py` |
| `686fa9b42dbe6cefb1c55a7b749ca3880ffcd8fe` | 22691 | `artifacts/v4-cell-census-v1/output/summary.json` |

plus the 5,299 pins under
`artifacts/v4-cell-census-v1/output/types/*.json` at the same commit
(`output/item3a_corpus_soundness.json` records the count and the per-pin
blob binding). Current-main inputs actually loaded: the accepted
`artifacts/v4-coherent-canonical-form-pilot-v1/canonicalizer/coherent_ir.py`
(used only in `code/join.py`, packet item 6) and the accepted corpus
custody artifacts (read for reconciliation, not for authority).

## Directory map

- `PROOFS.md` — this lane's independent re-derivation: Lemmas 1–8,
  Theorem A (frame collapse), Theorem B (degree collapse), **Lemma D
  (free-orbit separation, new)**, **Theorem C (six-cell)**, Proposition
  N-A (the only normalisation used by this lane's enumerator), and the
  coefficient-field / real-vs-complex discussion.
- `code/av4.py` — independent library: `(n_4)` validator, `V4`
  representation validator, orbit taxonomy/inventory, the necessary
  conditions ("fences") re-implemented from `PROOFS.md`, and an
  individualisation–refinement canonical form seeded with the
  QUADRILATERAL (8-cycle) count, with an explicit verified-isomorphism
  extractor.
- `code/fastcanon.py` — a second, faster exact canonical form used only
  for internal de-duplication; checked to induce the same partition.
- `code/pins.py` — pinned-blob reader (`git cat-file --batch`).
- `code/theory_checks.py` — exhaustive machine checks of the finite parts
  (case table, Theorem A frame arithmetic, six-cell theorem, exact
  rational model of `V4 <= PGL_3(Q)`).
- `code/verify_corpus.py` — packet item 3 (soundness direction) on all
  5,299 pins.
- `code/indep_enum.py` — this lane's INDEPENDENT enumerator (packet items
  3 second direction and 5).
- `code/small_control.py` — exhaustive bounded controls at `n = 15`: a
  completely unnormalised brute force (orbits in increasing
  representative order) versus the normalised enumerator, with
  multiplicity against the explicitly constructed relabelling group.
- `code/small_control19.py` — the same control at `n = 19`, with a second,
  independently written brute-force search rule (exact-cover branching on
  the smallest deficient point); the two rules are cross-validated
  against each other at `n = 15`.
- `code/small_control19_resolve.py` — the honest `n = 19` comparison. The
  brute force fixes only the POINT orbit inventory, so it spans every
  admissible LINE inventory; a single-cell comparison must under-count.
  This script records each fence-valid type's recomputed line inventory
  and compares against the union over admissible cells.
- `code/replay_census.py` — packet item 4: replay of the pinned generator
  over all 54 nominal sub-cells, plus a `--nogamma` premature-prune
  control on a cell the producer's own receipt did not test.
- `code/abstract_probe.py`, `code/abstract_probe_repaired.py` — the
  producer's own frame relaxed (`abstract` mode) at `n = 23`, with and
  without the `D1` repair.
- `code/defect_probe.py`, `code/adversaries.py`, `code/adversaries2.py` —
  the planted-adversary battery and the D1 defect probe. These write
  patched copies of the pinned generator into the untracked scratch
  directory `_scratch_pinned/`, regenerated from the pinned blob on every
  run; no patched byte is committed.
- `code/canon_selfcheck.py` — canonical-form invariance/completeness/
  sensitivity/cross-agreement checks.
- `code/join.py` — packet item 6: bare-type and coherent-action joins.
- `output/*.json` — all receipts.
- `output/indep_cell_digests.json` — the compact evidence of the
  independent enumeration: the `av4` canonical digest of every type it
  found, per cell (including the two cells obtained by duality). The raw
  line lists are **not** committed: 4,009 types x 23 lines is several MB,
  over this campaign's 5 MiB new-tracked-blob threshold, and they are
  regenerable in about 45 minutes wall from the replay commands below.
  `output/indep_logs/*.log` keeps every per-cell and per-shard summary
  line (status, type count, leaf count, node count, seconds).
- `code/verify_from_receipts.py` — re-checks the headline set equalities
  from the committed compact indices alone, without re-enumerating.

## Replay

```
python code/theory_checks.py
python code/verify_corpus.py
python code/canon_selfcheck.py
python code/replay_census.py
python code/replay_census.py --nogamma 0,1,2,1 --cap 9000
python code/small_control.py
python code/small_control19.py 9000
python code/small_control19_resolve.py     # ~31 min; the honest n=19 join
python code/abstract_probe.py ; python code/abstract_probe_repaired.py
python code/defect_probe.py
python code/adversaries.py cheap
python code/adversaries.py a2 ; python code/adversaries.py a6
python code/adversaries2.py
python code/verify_from_receipts.py          # cheap: uses committed indices

# full re-enumeration (about 45 min wall on 12 cores); recreates output/indep/
python code/indep_enum.py --cell 0,1,1,0 --out output/indep/b01-bs10.json
python code/indep_enum.py --cell 0,1,1,2 --out output/indep/b01-bs12.json
python code/indep_enum.py --cell 0,1,2,1 --out output/indep/b01-bs21.json
for j in $(seq 0 11); do \
  python code/indep_enum.py --cell 0,1,0,1 --shard 3:$j \
    --out output/indep/shards/b01-bs01-s$j.json & done; wait
python code/join.py
```

The two remaining nonempty sub-cells are obtained inside `join.py` by
point–line duality, which is a bijection between the type sets of
`(b2,b3;b*2,b*3)` and `(b*2,b*3;b2,b3)`. `--shard SLOT:INDEX` splits the
search tree at one level; the union over `INDEX` is exactly the unsharded
run, checked exactly on `b01-bs21`
(`output/item5_shard_equivalence_check.json`).

## Precision / precondition notes

- `join.py` asserts `sys.flags.optimize == 0` before importing
  `coherent_ir`, matching that module's accepted deployment contract, and
  calls `coherent_digest_hex` only at the fixed default refinement
  setting.
- Everything in this lane is deterministic and seedless except the
  fixed-seed LCG used to generate relabellings inside
  `canon_selfcheck.py`.
- Raw pin bytes are not committed here; they are re-read from the pinned
  git objects on every run (`code/pins.py`), and the derived per-pin
  digest maps are written to `output/independent_bare_digests.json`.
