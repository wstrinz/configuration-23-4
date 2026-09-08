# Exact classification of the two surviving diagonal-V4 action loci

**SUPPORTED within the scope below:** E1 has exactly one complex and real
gauged point. E2 has exactly two complex points, both real; an explicit
projective collineation and incidence relabeling exchange them. Thus each
locus contributes one real projective class. No positive-dimensional
component occurs.

This package is inbox evidence with `decides=[]` and `graph_effect=NONE`.

## What “action locus” means

An action locus here is attached to one pinned coherent pair `(T,H)`: a
labelled abstract `(23_4)` incidence type `T` and a faithful, admissible,
part-preserving subgroup `H <= Aut_inc(T)` isomorphic to `V4`. Coherent action
classes in the 5,395-pair census have already been quotiented by incidence
automorphisms of `T` and by the six automorphisms of `V4`; point-line dual
actions were not identified.

For a geometric realization inducing this action, conjugate `H` in `PGL(3)`
to the diagonal sign group. Orbit stabilizers then force the coordinate
supports. The checker enumerates all nine choices for the fixed point and
fixed line axes; for E1 and E2 exactly one chart survives, recorded as
`fixed_coords=[0,0]`. Each orbit representative is normalized by its first
supported coordinate. Binomial incidence equations solve a signed monomial
torus map, and the residual diagonal centralizer is removed by a unimodular
two-coordinate gauge. The result has ten coordinates `x0,...,x9`.

The locus is **not one numerical neighborhood or one orthant**. It is the full
solution scheme over `Q` of the twelve gauged incidence equations on
`(G_m)^10`, so every real sign choice satisfying the equations is included.
Algebraically we compute

`(I : (x0*x1*...*x9)^infinity)`.

After solving this closed incidence scheme on the open torus, every candidate
is checked against all 92 selected incidences, all 437 forbidden incidences,
23-point distinctness, 23-line distinctness, and nonzero-vector/frame guards.
The classification is exhaustive for these two specified diagonal-action
loci. It does not exclude a deformation that breaks the V4 symmetry, and it
does not classify arbitrary realizations of either bare incidence type.

## Exact decomposition and real roots

| locus | complex primary components | component dimensions | complex points | real points | guarded points | projective classes |
|---|---:|---|---:|---:|---:|---:|
| E1 rational | 1 | `0` | 1 | 1 | 1 | 1 |
| E2 quadratic | 1 | `0` | 2 | 2 | 2 | 1 |

Singular's `primdecGTZ` reports one prime zero-dimensional component in each
case, with vector-space dimensions 1 and 2. Their reduced lexicographic bases
are:

```text
E1:
x0=3/2, x1=-2/3, x2=1, x3=1/3, x4=5/6,
x5=-1/6, x6=2, x7=9/2, x8=5/2, x9=-1/2.

E2:
x0=1-x9, x1=x9-1/2, x2=-1, x3=2*x9-3, x4=-2,
x5=-2*x9-1, x6=(1-x9)/2, x7=1/2, x8=2-x9,
2*x9^2-3*x9-1=0.
```

The E2 roots are `x9=(3 +/- sqrt(17))/4`, so both are real and simple.
`msolve 0.10.1` independently reports ideal degrees 1 and 2 and respectively
one and two certified real isolating boxes. SymPy 1.14.0 independently derives
the same saturated triangular bases. The full guard replay accepts every root
and records no extra incidence, missing incidence, duplicate, or zero vector.

For E2, the exact relabeling and matrix in
`guard_and_equivalence_receipt.json` send the minus embedding to the plus
embedding. In the retained normalization the matrix is projectively
`diag(1,-(1+sqrt(17))/4,1)`. All 23 point images and the inverse-transpose
images of all 23 lines were checked exactly. E1 and E2 are different abstract
incidence types, as independently confirmed by both BLISS and VF2.

Because both ideals are reduced and zero-dimensional, their points are
isolated inside these pinned symmetric loci. No claim of global rigidity in
the unrestricted realization space is made.

## Controls

The identical compiler, torus gauge, saturation, SymPy calculation, and
Singular calculation were run on:

| control | result |
|---|---|
| Cuntz `(22_4)` diagonal action | degree 2, polynomial `x11^2-x11-4`; known real locus recovered |
| excluded action `d6245d...` | unit ideal; agrees with `verification_b01-bs01.json` |
| excluded action `7b2805...` | unit ideal; agrees with `verification_bs10_004.json` |
| excluded action `ac61a2...` | unit ideal; agrees with `verification_torus_bs10_sweep.json` |

The three negative actions were sampled without replacement from all 5,393
excluded actions using Python `random.Random(2304)` on sorted pair IDs.

## Resulting theorem

Within each of the two specified faithful diagonal `V4` action loci, after
projective normalization and quotient by the diagonal centralizer, the E1
incidence equations have exactly one geometric real solution and the E2
equations have exactly two geometric real solutions. The E2 solutions are
Galois conjugate and projectively equivalent after an abstract incidence
automorphism. Consequently each action locus has exactly one geometric real
projective-equivalence class, and neither contains a movable component.

## Replay

From the campaign root:

```powershell
py artifacts/action-locus-classification-v1/build_exact_systems.py
py artifacts/action-locus-classification-v1/run_external_solvers.py
py artifacts/action-locus-classification-v1/check_guards_and_equivalence.py
py artifacts/action-locus-classification-v1/run_controls.py
```

The two external-solver scripts call the installed Singular 4.2.1 and msolve
0.10.1 binaries through WSL. Exact commands, input/output hashes, systems,
decompositions, isolating boxes, control sample, and guard results are retained
beside this file.
