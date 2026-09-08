# V4 completeness and direct-trade geometry intake

**Date:** 2026-08-29  
**Coordinator:** DKC  
**Global theorem status:** `OPEN`  
**Canonical graph effect:** `NONE`

This intake reconciles the terminal global-obstruction portfolio launched from
`ef19820a41e02e2def8b717bee65afbc8c2e11e9`.

## Landed custody

- V4 completeness audit: `4bfa6b3e`, `4646bf0f`, `d5a77321`.
- Classes 356/77 geometry audit: `65bcaef6`.
- Deficient-parent repair-locus lead: `bb9b0e16`.
- Class-357 Mac geometry producer: `cf01cfc3`.

All source worktrees were clean at landing. DKC ran the campaign verifier on
every local branch and on an isolated checkout of the Mac commit. The eleven
campaign tests passed in each case. Retained sidecar log bytes contain two
pre-existing trailing-space lines; they are evidence bytes, not campaign
source, and were not rewritten.

After intake, DKC marked the four portfolio lifecycle records and twenty older
terminal/expired local records complete. This was lifecycle reconciliation
only: no older unlanded branch was merged and no dirty worktree was cleaned or
removed. Active local and Mac rosters are empty; preserved worktrees remain the
custody surface for any later semantic sweep.

## V4 enumeration completeness accepted

For a bare geometric `(23_4)` configuration carrying a faithful
`V4 <= PGL_3(R)` action, its bare incidence type occurs in the frozen 5,299-pin
corpus. The audit independently re-derived the projective fences and generator
normal form, constructed a code-independent enumerator, and obtained exact
per-cell set agreement with the frozen corpus.

Exactly six of the 54 nominal storage cells survive the geometric and abstract
fences. The other 48 are empty by the new free-orbit separation lemma, rather
than merely by a completed search. DKC cold-replayed the finite theorem checks
and the compact per-cell join:

- all six independent/corpus cell sets agree;
- their bare union has exactly 5,299 types;
- cell memberships sum to 5,371, with 72 repeated memberships;
- `5371 = 5299 + 72`.

This corrects the earlier phrase “5,299 coherent-action classes.” The accepted
statement is 5,299 distinct **bare** types, with one stored action per pin and
5,371 distinct cell-tagged coherent actions exhibited by the census. The audit
does not exclude additional coherent actions on the same bare type within one
cell, so 5,371 is not promoted as a global total.

Completeness is only a candidate-list theorem. It proves neither that any of
the 5,299 types is geometrically realizable nor that the accepted S0--S3
filters decide one. The prepared cell-level quotient packet is now eligible
for a separately authorized launch.

## Classes 77, 356, and 357 accepted empty in characteristic zero

Together with the previously accepted Class 122 result, four of the fourteen
topological direct matching trades are now accepted nonrealizable over every
characteristic-zero field:

`77, 122, 356, 357`.

- **356:** the operative proof is synthetic. In every one of the eight clean
  ruler orientations, the forced construction makes `P0,P1,P5` collinear,
  while the pin forces `P0,P1` onto `L0` and forbids `P5` from `L0`. DKC
  replayed this short contradiction. The unit-ideal computation is retained
  only as corroboration.
- **77:** the repaired root-set-preserving reduction, complete chart coverage,
  exact endpoint contradictions, and independent Singular lex route are
  accepted. The historic `sqf_prim` producer route remains refuted and is not
  used. The unreduced primary decomposition remains inconclusive and is not
  needed for the conclusion.
- **357:** chart 100 has a designated residual `(P12,L4)` whose five factors
  are each forced nonzero by genuine forbidden incidences or forced-distinct
  construction contents. DKC cold-replayed the independent Singular-backed
  factor/division check; all factors and the product identity passed. The
  retained Singular, msolve, and Macaulay2 unit-ideal replays corroborate it.

The Class-357 evidence tree contains three intentional Mac symlinks. A Windows
checkout materializes them as link-text files, so DKC ran the cold mathematical
replay in the preserved Mac worktree and records the portability seam. It does
not affect the pinned hashes or conclusion.

No positive-characteristic claim is accepted for any of these classes.

## Deficient-parent theorem accepted; P14 held at candidate authority

The child/repair-locus equivalence is accepted for all 37 direct matching
trades, over every field. Deleting `P_STAR,L_STAR` gives the four-flag-deficient
Cuntz parent, and a child realization is equivalent to a guarded parent
realization satisfying the two concurrence and two collinearity equations plus
all inherited and STAR inequations. The 37 deficient cores are regenerated,
fingerprinted, pairwise non-isomorphic, and have trivial stabilizer under the
order-four parent automorphism group.

The same lane computed all fourteen accepted-topological repair loci empty in
characteristic zero, but that result remains **candidate authority**:

- it is one producer's fourteen per-row computation, not a common family
  obstruction;
- `minAssGTZ` demonstrably returns false emptiness on Class 1769 in this exact
  family;
- seven rows touch the affected component route; and
- the lead validated the method on a realizable Cuntz control but did not
  independently replay every row.

Accordingly P14 has `decides=[]` until the prepared independent audit rebuilds
every row without `childB/code/` and proves emptiness without `minAssGTZ`.

## Accepted scope

`decides=["completeness of the frozen 5299 bare-type corpus for faithful geometric V4 actions", "six feasible and 48 proof-empty V4 storage cells", "bare characteristic-zero nonrealizability of direct-trade classes 77, 356, and 357", "field-uniform child/guarded-repair-locus equivalence for all 37 direct trades", "exact 37-core deficient-parent atlas"]`

`does_not_decide=["geometric realizability of any V4 corpus type", "global total number of coherent V4 actions", "S0-S3 geometric attrition", "P14 all-fourteen characteristic-zero emptiness", "positive-characteristic realizability", "a common direct-trade family obstruction", "global geometric (23_4) existence"]`

DKC V4 COMPLETENESS AND TRADE GEOMETRY INTAKE COMPLETE
