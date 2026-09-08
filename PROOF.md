# A compact rational construction of a geometric (23_4) configuration

Use homogeneous coordinates in the real projective plane. In every expression
below, epsilon and delta independently range over +1 and -1. The eight point
orbits are

```
P1: (1,0,0)
P2: (0,1,Â±1)
P3: (0,2,Â±3)
P4: (1,0,Â±1)
P5: (3,2 epsilon,2 delta)
P6: (2,2 epsilon,3 delta)
P7: (6,2 epsilon,5 delta)
P8: (6,2 epsilon,delta)
```

The eight line orbits, represented by coefficients of ax+by+cz=0, are

```
L1: (1,0,0)
L2: (0,1,Â±1)
L3: (0,3,Â±2)
L4: (1,Â±3,0)
L5: (1,2 epsilon,2 delta)
L6: (2,9 epsilon,6 delta)
L7: (2,5 epsilon,2 delta)
L8: (2,epsilon,2 delta)
```

Each list has orbit sizes s=(1,2,2,2,4,4,4,4), totaling 23.
All vectors are nonzero and primitive integer vectors with their first
nonzero coordinate positive. No two in either list agree: zero-coordinate
patterns together with the displayed nonzero coordinate ratios distinguish
the first four orbits; the displayed positive first
coordinates and absolute other coordinates distinguish the remaining orbits,
and the signs distinguish members. Primitive normalized integer vectors
represent the same real projective object only if they agree. Thus these
are 23 distinct points and 23 distinct lines.

The transformations diag(1,epsilon,delta) preserve both sets and incidence,
and act transitively on each displayed orbit. It is therefore enough to
check the line representative with all displayed signs positive. For those
eight representatives the numbers of zero dot products in the point orbits
are the following matrix M:

| |P1|P2|P3|P4|P5|P6|P7|P8|
|---|---|---|---|---|---|---|---|---|
|L1|0|2|2|0|0|0|0|0|
|L2|1|1|0|0|2|0|0|0|
|L3|1|0|1|0|0|2|0|0|
|L4|0|0|0|0|0|0|2|2|
|L5|0|1|0|0|0|1|1|1|
|L6|0|0|1|0|1|0|1|1|
|L7|0|0|0|1|1|1|0|1|
|L8|0|0|0|1|1|1|1|0|

This table requires only substitution of the displayed signs. For example,
L5=(1,2,2) evaluated on P7 gives 6+4 epsilon+10 delta, whose four values
are 20,0,12,-8. Thus M[5,7]=1. All the individual dot-product values are
also listed in orbit-verification.json for straightforward arithmetic review.
Every row sums to four, so every selected line contains exactly four selected
points, including the exclusion of every extra selected incidence.

Transitivity makes the degree constant within each point orbit. Counting
incidences into orbit Pj gives its degree as sum_i(s_i M_ij)/s_j.
The eight numerators are (4,8,8,8,16,16,16,16)=4s. Every selected point
therefore lies on exactly four selected lines. This proves existence.

For an entirely finite Euclidean realization apply the invertible projective
change (x,y,z) -> (x,y,3x+8z), determinant 8, and divide by the last
coordinate. None of the 23 denominators is zero. The affine coordinates are
(x/(3x+8z), y/(3x+8z)); line (a,b,c) becomes
(8a-3c)X+8bY+c=0. All these are ordinary straight lines: their first two
coefficients cannot both vanish, since such a line would have no finite
incident points, contradicting the already established four incidences.
Invertibility preserves all distinctness and incidences.

The five additional lines through three selected points are unselected lines.
The definition imposes degrees between the two selected sets; it does not
require every pair of points to join on a selected line or every intersection
of selected lines to be a selected point. The independent reconstruction
actually finds no line through more than four of the selected points.

## Formal verification

Solution.lean independently verifies the displayed construction directly over
Mathlib real numbers, including nonzero line normals, all pairwise
nonproportional line equations, distinct points, and both exact degree counts.
Challenge.lean states the existence theorem independently. See
STATEMENT_AUDIT.md for the coordinate definition and VERIFICATION.md for the
executed kernel and statement-comparison checks.

standalone/Witness.lean is also supplied as an optional Std-only integer
certificate. It uses ordinary decide and no axiom dependencies. Its scope is
finite integer arithmetic, whereas the main Solution states and proves the
real-affine result itself. Neither proof depends on the search census.
