# Exact evidence for the symmetric classification

This directory supports the computational statements that go beyond the Lean
existence theorem in the repository root.  The resulting bounded theorem is:

> Up to real projective equivalence and incidence relabeling, exactly two
> geometric `(23_4)` configurations admit a Klein four-group `V4` of
> collineations: the rational configuration E1 and the quadratic configuration
> E2 over `Q(sqrt(17))`.

It is a classification of the `V4` sector.  It does not classify configurations
whose collineation groups are trivial or `C2`, and it does not make a
publication-priority claim.

## Evidence chain

1. [The symmetry bound](symmetry/THEOREM.md) proves that the real collineation
   group of any geometric `(23_4)` has order `1`, `2`, or `4`, with the
   order-four case necessarily `V4`.  The exact finite checks are beside it.
2. [The V4 enumeration proof](v4-census/PROOFS.md) and its compact receipts
   establish completeness of the candidate corpus for faithful geometric V4
   actions.  The accepted-scope record is [ACCEPTED.md](v4-census/ACCEPTED.md).
3. [The independent exclusion replay](exclusion-replay/README.md) checks the
   proof corpus for all 5,393 excluded coherent action loci with zero terminal
   failures.  The two residual loci are E1 and E2.
4. [The exact action-locus classification](action-loci/README.md) uses saturated
   Groebner bases, primary decomposition and certified real-root isolation.
   E1 has one reduced real point.  E2 has two real conjugate points, related by
   an explicitly checked projectivity and relabeling.  Each locus therefore
   contributes one projective class and neither locus has a movable component.
5. [The combinatorial audit](combinatorics/REPORT.md) uses BLISS and an
   independent VF2 calculation.  E1, E2 and Cuntz's reconstructed CT1-S1 type
   are pairwise nonisomorphic, even when point-line exchange is permitted.

The retained solver inputs and outputs are exact.  The long census and replay
receipts preserve source hashes and command versions; reproducing the entire
census from first principles requires the research campaign identified in the
receipts, while the witnesses below are independently checkable from this
repository alone.

## Constructive witnesses

- E1 is the root-level [coordinates.json](../coordinates.json), checked by the
  Lean proof and the independent root-level verification files.
- [E2](e2/README.md) contains all 23 points, all 23 lines and a Node.js checker
  using exact arithmetic in `Q(sqrt(17))`.  It checks both real embeddings and
  an explicit positive-definite self-polarity for the positive embedding.
- [CT1-S1](ct1/PROOF.md) retains the exact chart-cover and saturation proof that
  its characteristic-zero realization space consists of two conjugate
  `Q(i)` points and hence has no real realization.

The root [one-page attachment](../docs/exact-one-page.pdf) is the compact E1
coordinate sheet intended for correspondence.

