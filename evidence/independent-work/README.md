# Independent work by Wenhao Lu

Wenhao Lu independently obtained the same two geometric `(23_4)`
configurations and an independent classification of the case admitting a
Klein four-group of collineations. His paper repository is:

- <https://github.com/welu2027/23_4-configuration>
- revision inspected: [`9e5cc941d0fea571eb997beb709978d3ffa4d3c7`](https://github.com/welu2027/23_4-configuration/commit/9e5cc941d0fea571eb997beb709978d3ffa4d3c7)
- inspection date: 2026-09-10

Lu's construction route is materially different from this project's search:
his draft describes a finite-field CP-SAT search for symmetric self-polar
configurations, lifting to characteristic zero, a `nauty` enumeration of 4,021
quotient structures, and exact Gröbner-basis and saturation computations in
Singular repeated in Macaulay2.

Lu first contacted the maintainer on September 8, 2026, and communicated the
draft on September 9. Lu reports that the draft was written September 6 and
that JMM 2027 abstract 66522 was submitted September 7. These dates are
attributed to Lu; this receipt does not independently certify the submission
system's version history.

## Local checks

The following commands were run from the inspected source revision:

```text
python code/check_23_4.py
python code/verify_23_4.py
```

Both passed. The first verifies the integral witness. The second verifies 23
distinct points, 23 polar lines, degree four on both sides, linearity, and no
absolute points for the quadratic self-polar witness, then independently
verifies the integral witness.

An exact set comparison confirms that Lu's integral point and line coordinates
equal E1 after the coordinate interchange `y <-> z`, up to homogeneous
rescaling. An independent bipartite-graph comparison confirms that Lu's
quadratic witness and E2 have isomorphic point-line incidence types. Lu's draft
also supplies the projective identification of the quadratic presentations.

Hashes of the inspected primary files and machine-readable results are in
[verification.json](verification.json).

## Scope

This receipt independently replays the two constructive witnesses and checks
their relationship to E1 and E2. It records, but does not replay, Lu's full
4,021-system classification. The two projects use different quotient and
canonicalization conventions; therefore no equality of intermediate census
counts is asserted here. The independently obtained classifications do agree
on the final result: exactly the same two projective classes survive in the
Klein-four sector.
