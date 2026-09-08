# Independent re-derivation — V4-symmetric `(23_4)` candidate cell

Task `v4-enumeration-completeness-audit-v1`, lane `DKW-LOI`, base
`ef19820a41e02e2def8b717bee65afbc8c2e11e9`. Authority: `RECONNAISSANCE`
until DKC intake. `decides = []`.

This memo is written *before* consulting the sidecar memo's proofs for
anything other than the statements to be audited, and every lemma below is
proved here from scratch. Section 15 compares the result to the sidecar's
`DERIVATION.md` (pinned blob `0292e5f7c97f5ba5545cb6df0319d5a38d77a5dc`)
and lists the differences that matter.

Finite parts are machine-checked in `code/theory_checks.py`, output
`output/item1_theory_checks.json`. Tags used throughout:

* **[ABS]** — follows from the abstract axioms alone: the linear-space pair
  condition plus equivariance. Holds for every abstract `V4`-equivariant
  `(n_4)` incidence structure.
* **[GEO]** — needs the real projective plane: uses the fixed-point
  geometry of `V4 <= PGL_3(R)`.

---

## 0. Scope, conventions, and the one definitional hinge

`V4 = {1, s_1, s_2, s_3}`, `s_3 = s_1 s_2`; indices `{i,j,k} = {1,2,3}`
always distinct. In code `V4 = {0,1,2,3}` under `XOR`, `s_i = i`.

**Definition (geometric `(n_4)` configuration).** A set of `n` distinct
points and `n` distinct lines of `RP^2` such that every one of the points
lies on exactly four of the lines and every one of the lines carries
exactly four of the points. Its *abstract type* is the induced incidence
structure.

**Remark 0.1 (the definitional hinge, and why it is not an assumption).**
In this definition the abstract incidence relation *is* the geometric one:
there is no room for a configuration point to lie on a configuration line
"without being recorded", because that line would then carry five
configuration points. Everything tagged **[GEO, forced ON]** below rests
on exactly this and on nothing else. If one instead worked with the weaker
notion sometimes used for drawings — an abstract configuration together
with a realisation permitted to have *extra* incidences — then the
forced-ON rows fail and the whole frame collapse (Theorem A) is false.
The census, and this audit, are about the standard notion. This is
recorded as a scope condition, not as a hidden assumption: it is forced by
the definition, but it must travel with the result.

The *linear-space pair condition* — two distinct points lie on at most one
common line, equivalently two distinct lines share at most one point — is
automatic in `RP^2` and is imposed as an axiom on abstract types.

---

## 1. Involutions in `PGL_3(R)`

**Lemma 1.** Every element of order 2 in `PGL_3(R)` is conjugate to
`sigma = diag(-1,1,1)`. It fixes pointwise a line `A` (its *axis*) and one
further point `c` not on `A` (its *centre*); its fixed lines are `A`
together with the full pencil of lines through `c`. There is no second
conjugacy class and no fixed-point-free involution.

*Proof.* Let `M in GL_3(R)` represent an involution, so `M^2 = lambda I`
with `lambda in R^*` and `M` not scalar. Taking determinants in dimension
three, `det(M)^2 = lambda^3`, so `lambda^3 > 0`, hence `lambda > 0`, hence
`lambda` has a real square root and `N = M / sqrt(lambda)` satisfies
`N^2 = I`.

*(This is the first of the two places where `R` is used essentially; see
Section 13. Over a field in which `lambda` need not be a square the
normalisation can fail. Over `C` it never fails.)*

`N^2 = I` and `char R != 2` give `R^3 = ker(N-I) (+) ker(N+I)`; `N` is not
scalar, so the eigenvalue multiplicities are `(1,2)` or `(2,1)`. In
`PGL_3` the overall sign is immaterial and
`diag(-1,-1,1) = -diag(1,1,-1) ~ diag(-1,1,1)` after permuting
coordinates, so there is a single class, represented by `sigma`.

Fixed points of `sigma` are the eigenvectors: the isolated point
`c = [1:0:0]` and every point of the line `A = {x_0 = 0}`; `c` is not on
`A`. Fixed lines are the fixed points of the transpose action, i.e. `A`
and every line through `c` (synthetically: a line through `c` meets `A` in
a fixed point, so it joins two fixed points and is fixed). `Fix(sigma)`
is nonempty, so no involution is fixed-point-free. `qed`

Machine control: `theory_checks.C4` verifies all of these statements on an
exact rational sample of `RP^2(Q)` (`output/item1_theory_checks.json`,
key `C4_real_model`, all `true`).

---

## 2. Normal form of `V4 <= PGL_3(R)`

**Lemma 2.** In suitable coordinates `s_1 = diag(-1,1,1)`,
`s_2 = diag(1,-1,1)`, `s_3 = diag(1,1,-1)`. The centres `c_1, c_2, c_3`
are the coordinate points; they form a triangle, and the axis of `s_i` is
the opposite side `A_i = line(c_j, c_k) = {x_i = 0}`.

*Proof.* Lift `s_1, s_2` to `M_1, M_2` with `M_1^2 = M_2^2 = I`
(Lemma 1). Commutation in `PGL` gives `M_1 M_2 M_1^{-1} = lambda M_2` for
some scalar `lambda`. Two independent arguments force `lambda = 1`:

* determinants: `det(M_2) = lambda^3 det(M_2)`, so `lambda^3 = 1`, and
  over `R` the only real cube root of 1 is 1;
* squares (field-free, and therefore the argument this audit prefers):
  `M_1 M_2^2 M_1^{-1} = lambda^2 M_2^2`, i.e. `I = lambda^2 I`, so
  `lambda = +-1`; combined with `lambda^3 = 1`, `lambda = 1`.

So the lifts genuinely commute; there is no "anticommuting'' or
Heisenberg branch. Commuting real involutive matrices are simultaneously
diagonalisable. In a common eigenbasis, after a sign normalisation in
`PGL` and a coordinate permutation, `M_1 = diag(-1,1,1)`; `M_2` is then
diagonal with entries `+-1`, not `+-I` and not `+-M_1`, so up to sign it
is `diag(1,-1,1)` or `diag(1,1,-1)`, and a further swap of the last two
coordinates (which fixes `M_1`) makes it `diag(1,-1,1)`. Then
`s_3 = s_1 s_2 = diag(-1,-1,1) ~ diag(1,1,-1)`. Reading off centres and
axes gives the statement. `qed`

**Lemma 3 (fixed sets).** With the normal form:

* the common fixed points of `V4` are exactly `c_1, c_2, c_3`; the common
  fixed lines are exactly `A_1, A_2, A_3`; `c_i` lies on `A_j` and `A_k`
  and not on `A_i`; `A_i cap A_j = {c_k}`;
* `Fix(s_i)` (points) `= {c_i} u A_i`; the points fixed by `s_i` and by no
  other involution are `A_i \ {c_j, c_k}`;
* the lines fixed by `s_i` are `{A_i} u pencil(c_i)`; those fixed by `s_i`
  alone are `pencil(c_i) \ {A_j, A_k}`.

*Proof.* Immediate from Lemma 1 applied to each `s_i` in normal form; e.g.
`Fix(s_1) cap Fix(s_2) = ({c_1} u A_1) cap ({c_2} u A_2) = {c_1,c_2,c_3}`
using `c_1 in A_2`, `c_2 in A_1`, `A_1 cap A_2 = {c_3}`. `qed`

The normaliser of this `V4` in `PGL_3(R)` contains the permutation
matrices, which act on `{s_1,s_2,s_3}` as the full `S_3`; conjugating by
them relabels the indices and preserves projective equivalence. This is
the "global `S_3`" used for the WLOG in Section 12.

---

## 3. Faithfulness

**Lemma 4.** If `X` is a `(23_4)` (or `(22_4)`) configuration invariant
under `V4 <= PGL_3(R)`, then the induced action of `V4` on the abstract
incidence structure of `X` is faithful. **[GEO]**

*Proof.* Suppose `s_i` fixes every configuration point. By Lemma 3 every
configuration point then lies in `{c_i} u A_i`, so at least `22` of them
lie on the single line `A_i`. Any configuration line `l != A_i` carries
four configuration points, at least three of which are on `A_i`; three
distinct points on both `l` and `A_i` force `l = A_i`, a contradiction.
Hence no non-identity element of `V4` acts trivially on points, and the
map `V4 -> Aut(X)` is injective. `qed`

So an equivariant abstract type is an abstract configuration together with
an embedded copy of `V4` in its automorphism group.

---

## 4. Orbit taxonomy and parity

Orbit sizes are `4, 2, 1` with stabilisers `1`, `<s_i>`, `V4`.

**Lemma 5.** For a `V4`-invariant geometric configuration: **[GEO]**

* a size-1 point orbit is one of `c_1, c_2, c_3`;
* a size-2 point orbit with stabiliser `<s_i>` consists of two points of
  `A_i \ {c_j, c_k}` interchanged by `s_j` (equivalently `s_k`);
* a size-4 point orbit consists of points lying on no axis and at no
  vertex — because *a point of `A_i` is `s_i`-fixed*, `A_i` being fixed
  pointwise.

Dually for lines, using `pencil(c_i)` in place of `A_i`. `qed`

**Notation.** `f` = number of vertices used as configuration points,
`b_i` = number of point 2-orbits with stabiliser `<s_i>`, `a` = number of
free point 4-orbits; `f*, b*_i, a*` dually. Write `b = b_2 + b_3` and
`b* = b*_2 + b*_3` once the frame index has been normalised to 1.

**Lemma 6 (parity).** `23 = 4a + 2(b_1+b_2+b_3) + f`, so `f` is odd and
`f in {1,3}`; dually `f* in {1,3}`. (For `n = 22`: `f, f* in {0,2}`.)
In particular a `V4`-symmetric `(23_4)` always uses at least one vertex
and at least one axis. `qed`

---

## 5. The incidence-orbit case table

Let `P` be a point orbit with stabiliser `H` and `L` a line orbit with
stabiliser `K`. The incidence relation restricted to `P x L` is a
`V4`-invariant subset of `P x L`, hence a union of `V4`-orbits of flags,
which we call *classes*. Because `V4` is abelian, the number of classes is
`4 / |HK|`.

`code/theory_checks.py::case_table` enumerates, for all nine
`(H, K)` shapes, **every** invariant relation and reports the number of
classes, the largest number of simultaneous classes compatible with the
pair condition, and the per-class degree gain. The machine output
(`C1_case_table`) is:

| point x line | orbit sizes | #classes | max simultaneous | gain (pt, ln) |
|---|---|---|---|---|
| free x free | 4,4 | 4 | **1** | 1,1 |
| free x `<s_i>` | 4,2 | 2 | **1** | 1,2 |
| free x `V4` | 4,1 | 1 | 1 | 1,4 |
| `<s_i>` x free | 2,4 | 2 | **1** | 2,1 |
| `<s_i>` x `<s_i>` | 2,2 | 2 | **1** | 1,1 |
| `<s_i>` x `<s_j>`, `i!=j` | 2,2 | 1 | **0** | 2,2 |
| `<s_i>` x `V4` | 2,1 | 1 | 1 | 1,2 |
| `V4` x free | 1,4 | 1 | 1 | 4,1 |
| `V4` x `<s_i>` | 1,2 | 1 | 1 | 2,1 |
| `V4` x `V4` | 1,1 | 1 | 1 | 1,1 |

Every entry in the "max simultaneous" column is **[ABS]**: it is a pure
consequence of the pair condition. In particular:

**Lemma 7 [ABS].** A point with stabiliser `<s_i>` never lies on a line
with stabiliser `<s_j>`, `i != j`. (Machine: the `0` in the table.)
Hand proof: `p = s_i p in s_i l != l` and `s_j p = s_k p` lies on
`s_j l = l` and on `s_k l = s_i l`, so the two distinct points `p, s_j p`
lie on the two distinct lines `l, s_i l`. `qed`

**Lemma 8 [ABS].** At most one class occurs between any given point orbit
and line orbit. Consequences used later: a free line orbit carries at most
one point 2-orbit of each fixed index `i` (but may carry 2-orbits of
different indices), and a free line orbit meets a given free point orbit
in at most one class ("twist"). `qed`

The **[GEO]** content is the *forcing*: which classes must be present or
absent in a realisation. From Lemma 3 and Remark 0.1:

| | forced |
|---|---|
| `c_i in A_j`, `i != j` | **ON** [GEO] |
| `c_i in A_i` | OFF [GEO] |
| `c_i` on every line of every `<s_i>`-line orbit | **ON** [GEO] |
| `c_i` on a `<s_j>`-line orbit, `j != i` | OFF [GEO] (else the line is `A_k`) |
| `c_i` on a free line | OFF [GEO] |
| every `<s_i>`-point on `A_i` | **ON** [GEO] |
| a `<s_i>`-point on `A_j`, `j != i` | OFF [GEO] |
| a free point on any axis | OFF [GEO] |

The two remaining geometric restrictions are not forcings of a single
class but *exclusions between classes*:

**Fence GF1 [GEO].** No configuration line other than `A_i` carries two
points of `<s_i>`-type. (All such points lie on the plane line `A_i`; a
second common line would meet `A_i` twice.) Residual content beyond
[ABS]: an `<s_i>`-line orbit is matched with at most one `<s_i>`-point
orbit.

**Fence GF2 [GEO], dual.** No `<s_i>`-point lies on lines of two different
`<s_i>`-line orbits. (All such lines pass through `c_i`; two of them
through a second common point would coincide.)

**Fence-list completeness (relative statement).** Every incidence between
configuration elements falls under exactly one row of the case table, and
every geometric exclusion used above is one of: fixed-set membership
(Lemma 3), "two points determine a line" applied to `A_i`, "two lines meet
once" applied to `c_i`. Constraints not expressible at the level of the
abstract incidence type (harmonicity of the 2-orbits, real order/
separation, actual realisability) are **not** claimed. For a
*completeness* audit this asymmetry is the safe one: any further necessary
condition only shrinks the candidate list. The dangerous direction is a
fence that is **not** necessary; each fence above is proved necessary.

---

## 6. Theorem A — the frame collapses [GEO]

**Theorem A.** Every `V4`-symmetric geometric `(23_4)` uses exactly one
vertex `c_m` and exactly one axis `A_n`, and `m = n`. Moreover
`b_m = b*_m = 2`.

*Proof.* Let `V` be the set of chosen vertices and `W` the set of chosen
axes, `f = |V|`, `f* = |W|`. By the forcing table, for a chosen vertex
`c_i` the four lines through it are exactly the chosen axes `A_j`, `j != i`,
together with **all** lines of **all** `<s_i>`-line orbits:

    |W cap {j,k}| + 2 b*_i = 4        for every i in V.          (1)

Dually, for a chosen axis `A_i` the four points on it are exactly the
chosen vertices `c_j`, `j != i`, together with all `<s_i>`-points:

    |V cap {j,k}| + 2 b_i  = 4        for every i in W.          (2)

By Lemma 6, `f, f* in {1,3}`.

Assume `f = 3`. Summing (1) over `i = 1,2,3` and noting that each chosen
axis is counted for the two indices different from its own,
`2 f* + 2 (b*_1+b*_2+b*_3) = 12`. If `f* = 3` then every axis is chosen,
so (2) gives `2 + 2 b_i = 4`, i.e. `b_i = 1` for all `i`, and Lemma 6
becomes `23 = 3 + 6 + 4a`, i.e. `4a = 14` — impossible. If `f* = 1`, say
`W = {m}`, take `i in V` with `i != m` (possible since `f = 3`); then
`|W cap {j,k}| = 1` and (1) reads `1 + 2b*_i = 4` — impossible. So
`f != 3`, hence `f = 1`; dually `f* = 1`.

Write `V = {m}`, `W = {n}`. If `m != n`, (1) at `i = m` gives
`1 + 2 b*_m = 4` — impossible. So `m = n`, and then (1) and (2) give
`b*_m = 2` and `b_m = 2`. `qed`

**Exhaustive machine control.** `theory_checks.theorem_A_search` enumerates
*every* integer frame `(V, W, b, a, b*, a*)` satisfying (1), (2) and both
parity equations with `n = 23`, over `0 <= b_i, b*_i <= 11`. All `2700`
surviving frames have `(f, f*) = (1,1)` with `V = W`
(`C2_theoremA_surviving_shapes`). For `n = 22` the surviving shapes are
`(0,0)`, `(0,2)`, `(2,0)` — consistent with the accepted Cuntz `(22_4)`,
which has `f = f* = 0`.

**Where the geometry enters.** Equations (1) and (2) are *entirely*
[GEO]: they use forced-ON of rows `V x Lambda` and `V x L_i`, and
forced-OFF of `V x L_j (j != i)`, `V x G`, `P_j x Lambda_i (j != i)` and
`F x Lambda`. Abstractly none of these is forced, and abstractly `f = 3`
is not excluded. Theorem A is therefore a genuinely geometric theorem and
must not be quoted as an abstract one.

**WLOG.** Conjugating by a permutation matrix (Section 2) we take
`m = 1`. The residual relabelling group is the simultaneous swap `2 <-> 3`
of point and line indices.

---

## 7. Theorem B — degree collapse

Throughout `m = 1`. Write `x = c_1`, `L = A_1`, `P_i` for the point
2-orbits of index `i`, `M_i` for the line 2-orbits of index `i`, `F` for
free point orbits, `G` for free line orbits.

**Theorem B.**

1. `L` carries exactly the four `P_1`-points; `x` lies on exactly the four
   `M_1`-lines. `[GEO, = Theorem A]`
2. The two `P_1` orbits and the two `M_1` orbits are matched *bijectively*
   (one class each), and in addition each `P_1` orbit has exactly one
   class with a free line orbit, each `M_1` orbit exactly one class with a
   free point orbit. `[ABS given Theorem A]`
3. For `i in {2,3}`: no `P_i` orbit meets any `M_i` line; each `P_i` orbit
   has exactly two classes with two distinct free line orbits, and each
   `M_i` orbit exactly two classes with two distinct free point orbits.
   `[GEO — this is where GF2/GF1 are load-bearing]`
4. Degree equations for free orbits: for a free point orbit,
   `#M_1-classes + #M_2 + #M_3 + #G-classes = 4`; dually.  `[ABS]`
5. `4a = 18 - 2b`, `4a* = 18 - 2b*`, hence `b` and `b*` are odd and
   `b, b* in {1,3,5}`; the number of free-free classes is
   `e = 16 - 2b - 2b* >= 0`.

*Proof.* (1) is Theorem A. (2): a `P_1` point has degree
`1 (from L) + mu + 2 phi = 4`, where `mu` counts matched `M_1` orbits
(gain 1 each, table row `<s_1> x <s_1>`) and `phi` counts classes with
free line orbits (gain 2 each, row `<s_1> x free`); rows `<s_1> x <s_j>`
contribute nothing by Lemma 7. Thus `mu + 2 phi = 3`, so `mu` is odd, and
`mu <= b*_1 = 2` gives `mu = 1`, `phi = 1`. Dually an `M_1` line has
degree `1 (x) + mu' + 2 psi = 4` with `mu' = psi = 1`. Two orbits on each
side each matched exactly once gives a bijection.

(3): a `P_i` point (`i >= 2`) lies on no axis (`A_i` is not chosen; row
`<s_i> x Lambda_1` is forced off) and on no `M_j` line for `j != i`
(Lemma 7), so its degree is `mu + 2 phi = 4`. Fence **GF2** gives
`mu <= 1`; parity then forces `mu = 0`, `phi = 2`, and the two classes
involve distinct free line orbits by Lemma 8. Dually for `M_i`. Without
GF2 the abstract possibilities are `mu in {0,2,4}` — precisely the
abstract-valid, fence-invalid region.

(4) is the row list for a free orbit. (5): `23 = 1 + 2(2+b) + 4a` gives
`4a = 18 - 2b`, so `b` is odd, and dually. Counting the classes incident
with free point orbits: the two `M_1` orbits contribute one each, and each
of the `b*` orbits `M_2, M_3` contributes two, a total of `2 + 2b*`;
subtracting from `4a` gives `e = 4a - 2 - 2b* = 16 - 2b - 2b*`, and the
same count from the line side agrees. `qed`

---

## 8. Lemma D — free-orbit separation `[ABS]`

This lemma is **not** in the sidecar memo in this form; its `i = i'`,
`|N| = 1` special case appears there as addendum "B(2)+". It is the key
that closes the 48 empty cells by proof rather than by search.

**Lemma D.** Let `O != O'` be distinct line orbits with stabilisers
`<s_i>`, `<s_{i'}>`, and let `N(O)` be the set of free point orbits having
a class with `O`. Then

  (a) if `i = i'` then `N(O) cap N(O') = empty`;
  (b) if `i != i'` then `|N(O) cap N(O')| <= 1`.

*Proof.* Let `F in N(O) cap N(O')`. Index the four points of `F` by `V4`
via `q_h = h . q_0`. By the case table (row `free x <s_i>`) the class of
`O` with `F` puts on one line of `O` a full `<s_i>`-coset of `F` and on
the other line the complementary coset; likewise for `O'` with cosets of
`<s_{i'}>`.

(a) `i = i'`: the two lines of `O` and the two lines of `O'` each split
`F` into the *same* two `<s_i>`-cosets, so some line of `O` and some line
of `O'` carry the same coset, i.e. two common points. `O` and `O'` are
distinct orbits, hence disjoint, so these are two distinct lines — the
pair condition fails.

(b) `i != i'`: `<s_i> cap <s_{i'}> = 1` in `V4`, so a coset of `<s_i>`
meets a coset of `<s_{i'}>` in exactly one element. Hence any line of `O`
and any line of `O'` share exactly one point of `F`. If a second orbit
`F' in N(O) cap N(O')` existed, some line of `O` and some line of `O'`
would share one point of `F` and one of `F'` — two common points, again
contradicting the pair condition. `qed`

**Lemma D (dual).** Verbatim dual statement for distinct point 2-orbits
and their free *line* neighbourhoods, with the same proof (the pair
condition is self-dual). `qed`

**Corollary D1.** With Theorem B(2)-(3) and `m = 1`:

    2 <= a,        2 b*_i <= a   for i in {2,3};
    2 <= a*,       2 b_i  <= a*  for i in {2,3}.

*Proof.* The two `M_1` orbits have `|N| = 1` each and disjoint
neighbourhoods, so `a >= 2`. The `b*_i` orbits `M_i` (`i >= 2`) have
`|N| = 2` each and pairwise disjoint neighbourhoods, so `2 b*_i <= a`.
Dually. `qed`

---

## 9. The six-cell theorem

A *sub-cell* is `(b_2, b_3; b*_2, b*_3)` with `b = b_2+b_3` and
`b* = b*_2+b*_3` odd and `<= 5`, `b + b* <= 8`, taken up to the
simultaneous swap `2 <-> 3`. There are `108` such tuples and, since no
tuple is swap-fixed (`b` odd), exactly `54` sub-cells. This is the nominal
cell list the sidecar enumerated.

**Theorem C (six-cell).** Exactly six of the `54` nominal sub-cells can be
nonempty, namely

    b01-bs01, b01-bs10, b01-bs12, b01-bs21, b12-bs01, b12-bs10

(naming `b{b_2}{b_3}-bs{b*_2}{b*_3}`). The remaining `48` are empty.

*Proof.* `a = (18-2b)/4 in {4,3,2}` for `b in {1,3,5}` and dually. Apply
Corollary D1.

* `b = 5` gives `a = 2`, so `2b*_i <= 2`, i.e. `b*_i <= 1` and `b* <= 2`;
  `b*` odd forces `b* = 1`, so `a* = 4`, so `2b_i <= 4`, i.e. `b_i <= 2`
  and `b <= 4 < 5` — contradiction. All `b = 5` sub-cells are empty, and
  dually all `b* = 5` ones.
* `b = 3` gives `a = 3`, so `b*_i <= 1`, `b* <= 2`, hence `b* = 1`,
  `a* = 4`, hence `b_i <= 2`, which kills the split `(0,3)` and leaves
  `(1,2)` (canonical representative of `{(1,2),(2,1)}`). Surviving:
  `b12-bs01`, `b12-bs10`.
* `b = 1` gives `a = 4`, so `b*_i <= 2`, hence `b* <= 4`, hence
  `b* in {1,3}` with splits `(0,1),(1,0)` and `(1,2),(2,1)` — the split
  `(0,3)`/`(3,0)` is killed. And `b_i <= 2` holds automatically. Surviving:
  `b01-bs01, b01-bs10, b01-bs12, b01-bs21`. `qed`

Machine control: `theory_checks.six_cell_theorem` applies Corollary D1 to
all 54 nominal sub-cells and returns exactly these six
(`C3_six_cell_theorem`). This **matches the sidecar's six nonempty cells
exactly**, and upgrades its 48 "COMPLETE with 0 types'' search receipts to
a proof.

---

## 10. Normalisation N-A (used by this lane's independent enumerator)

Let `Gamma` be the group of `V4`-equivariant point relabellings preserving
the orbit-kind inventory: gauges of each 2-orbit, permutations of 2-orbits
of equal index, gauges (`XOR`-shifts) of each free orbit, permutations of
free orbits. Each generator commutes with the `V4` action, so it carries
equivariant structures to equivariant structures of the same abstract type.

Fix labels: `x = 0`; the two `<s_1>`-point orbits are `{1,2}` and `{3,4}`;
then the `<s_2>`- and `<s_3>`-orbits; then the free orbits
`F_o = {FB+4o+h : h in V4}`.

**Proposition N-A.** Every fence-valid labelled structure in a sub-cell is
carried by some `gamma in Gamma` to one in which

    the axis is        {1,2,3,4},
    one M_1 orbit rep  {0, 1, FB+0, FB+1},
    the other          {0, 3, FB+4, FB+5}.

*Proof.* The axis content is forced by Theorem A. Pick either `M_1` orbit
`O`; by Theorem B(2) each of its two lines carries `x`, one point of its
matched `P_1` orbit, and one `<s_1>`-coset of one free point orbit.
Permute the two `<s_1>`-point orbits so that `O`'s matched orbit is
`{1,2}` and gauge it so the point on the chosen line is `1`; permute the
free orbits so that `O`'s free orbit is `F_0` and gauge it so the coset is
`{FB+0, FB+1}`. Nothing else has been fixed, so these choices are
independent. `O`'s two lines are then `{0,1,FB,FB+1}` and its `s_2`-image
`{0,2,FB+2,FB+3}`; the first is lexicographically smaller.

The second `M_1` orbit `O'` is matched with the orbit `{3,4}` (Theorem
B(2): the matching is a bijection), and by **Lemma D(a)** its free point
orbit is *not* `F_0`. The gauge of `{3,4}` and the permutation/gauge of
the free orbits with index `>= 1` fix `O` pointwise as a line set, so they
are still available: gauge `{3,4}` so the point on the chosen line is `3`,
permute so the free orbit is `F_1` (possible because `a >= 2`, Corollary
D1) and gauge so the coset is `{FB+4, FB+5}`. The resulting representative
`{0,3,FB+4,FB+5}` is lexicographically smaller than its partner
`{0,4,FB+6,FB+7}`, and larger than `{0,1,FB,FB+1}`. `qed`

**No further normalisation is used by this lane's enumerator.** Every
other restriction it applies is a proved necessary condition: correct
orbit size, the pair condition, degree caps, the flag-count feasibility
bound of Section 11, the choice of the lexicographically least
representative *of a given orbit* (a per-orbit choice, always available),
and increasing representatives across interchangeable same-type slots
(a relabelling-free re-indexing of the slots themselves). Residual
relabelling duplication is removed at the leaves by an exact canonical
form. Consequently the completeness of this lane's enumerator depends only
on Theorems A, B, Lemma D and Proposition N-A.

**Control on N-A.** Proposition N-A is the one assumption this lane's
enumerator shares with the sidecar's, so it is tested where the shared
assumption can be removed entirely. At `n = 15` and `n = 19` a completely
unnormalised brute force (every `V4`-invariant set of line orbits whose
union is an `(n_4)` linear space on the fixed labelled point system; no
frame, no gauge fixing, no orderly rule, no representative convention, no
line inventory imposed) reproduces the N-A-normalised output exactly, as a
set and — at `n = 15` — with multiplicity. At `n = 19` this is a real
test: 109,056 labelled structures, 71 bare types, of which only 9 survive
the fences, and the normalised enumerator finds exactly those 9 (as a
union over the two line inventories that Corollary D1 admits at `n = 19`,
which are also the only two the brute force produces). See
`output/item5_small_controls.json`,
`output/item5_small_control_n19_resolved.json`.

---

## 11. A flag-count feasibility bound `[ABS + GEO]`

Used only as a search prune; proved necessary.

For a fixed index `i`, count flags between `<s_i>`-points and line orbits.
A free line orbit contains at most one `<s_i>`-point in a representative
(Lemma 8), hence exactly four such flags at most (the point and its
partner, each on two lines of the orbit). An `<s_i>`-line orbit carries at
most one `<s_i>`-point per line by GF1, hence at most two such flags. A
line orbit of index `j != i` carries none (Lemma 7); the axis carries four
(all of `P_1`) and is placed first. Hence, at any point of the search,

    sum over unsaturated <s_i>-points of (4 - deg)
        <=  4 * (#remaining free line slots) + 2 * (#remaining <s_i> slots).

`qed`

---

## 12. What "type" means, and the multiplicity question

The enumeration deduplicates by the **bare** isomorphism class of the
configuration (role-preserving isomorphism of the Levi graph), not by the
isomorphism class of the pair (configuration, `V4`-action). Two
consequences, both verified in Section 14 of the review packet:

* the corpus is a candidate list of **bare types**, which is exactly the
  target of this packet;
* the corpus is **not** a complete list of coherent-*action* classes. A
  bare type occurring in `k` distinct sub-cells carries at least `k`
  pairwise coherently-inequivalent fence-valid `V4` actions (distinct
  canonical sub-cells are inequivalent even after the `Aut(V4) = S_3`
  relabelling allowed by coherent equivalence, because the sub-cell list
  is already the quotient by that relabelling). The corpus stores one
  action per bare type.

---

## 13. Coefficient field, real vs complex, open loci

* **Where `R` is used essentially.** (i) Lemma 1's normalisation
  `M^2 = lambda I -> N^2 = I` needs `lambda` to be a square; over `R` this
  follows from `lambda^3 = det(M)^2 > 0`, over `C` it is automatic, over
  `Q` or a general field it can fail. (ii) Lemma 2's `lambda^3 = 1 =>
  lambda = 1`; but the square argument given in Section 2 removes the
  dependence, so Lemma 2 holds over every field of characteristic `!= 2`
  in which Lemma 1's normalisation is available.
* **Transport to `C`.** Lemmas 1-8, Theorems A, B, C all hold verbatim
  over `C` (indeed over any algebraically closed field of characteristic
  `!= 2`). Hence the same 54-cell/six-cell frame and the same candidate
  list bound the `C`-realisable `V4`-symmetric `(23_4)` types as well.
  Nothing here transports a *negative* result from `C` to `R` or back.
* **Characteristic 2** is entirely outside the scope: `V4` is unipotent in
  `PGL_3(F_{2^k})` and Lemma 1 fails.
* **Open loci.** Nothing in this memo is an open condition on a
  realisation space. The fences are closed combinatorial conditions on the
  incidence type; harmonicity (each `<s_i>`-point 2-orbit is harmonic with
  respect to `c_j, c_k` on `A_i`, and dually) is automatic in any
  equivariant realisation and therefore carries **no** combinatorial
  filtering power, though it does constrain any subsequent equivariant
  chart. Realisability over `R` — chirotope/orientation obstructions,
  Pappus-type incidence theorems, semialgebraic nonemptiness — is
  untouched.

---

## 14. What is *not* proved here

* No claim that any of the candidate types is realisable, equivariantly or
  at all.
* No claim that the fence list is *sufficient*; only that each fence is
  necessary.
* No claim about `S0`-`S3` filters.
* No claim that the abstract (fence-free) layer has been enumerated.

---

## 15. Differences from the sidecar's `DERIVATION.md`

Agreements (independently re-derived, not copied): Lemmas 1-6, the full
case table with its `[ABS]`/`[GEO]` split, fences GF1/GF2, Theorem A
(including the emptiness of the `f = 3` branch and the matching-index
conclusion), Theorem B, the 54-sub-cell frame, and the six nonempty cells.

Differences found:

* **D-A (arithmetic slip, non-load-bearing).** `DERIVATION.md` sec.6 says
  "8 `(b,b*)` cells, **60** sub-cells before the swap quotient". The
  correct counts are 108 before and 54 after; `RECEIPT.md` and the code
  both use 54, so nothing downstream depends on the "60".
* **D-B (strengthening).** The sidecar states the `|N| = 1` case of Lemma
  D as an implementation addendum ("B(2)+") and leaves the 48 empty cells
  to the search ("combinatorially empty ... verified by enumeration").
  Lemma D and Corollary D1 prove all 48 empty, so the 48 nominal cells are
  now reconciled by proof.
* **D-C (imprecision in N3, harmless).** `DERIVATION.md`'s N3 offers the
  candidate `{0,3,F0+2,F0+3}` for the second `M_1` slot, excluding only
  "the coset `{F0,F0+1}`". Lemma D(a) excludes the whole orbit `F_0`, so
  that candidate is never valid; the pinned generator does list it and
  relies on the pair check to reject it. Dead code, not a defect.
* **D-1 (a real generator defect; see `output/item5_defect_probe_D1.json`).**
  In `v4census.Search.gen_pairline` the coset selector
  `cos = lambda o, h: (freept(o, min(h, h^i)), freept(o, max(h, h^i)))`
  is enumerated over `h in (0,1)`. For `i = 1` this **collapses**:
  `h ^ 1` swaps `0` and `1`, so both calls return the `{0,1}`-coset and
  the complementary `<s_1>`-coset `{2,3}` is never generated. The
  generator therefore emits only 6 of the 12 stab-1 representatives.
  Reach analysis: in the load-bearing `n = 23` **fence** mode both stab-1
  line slots are FORCED, so `gen_pairline` is never called with `i = 1`
  and the 5,299-pin census is unaffected. The defect *is* reached by
  `n = 23` **abstract** mode, by `n = 22` fence mode whenever
  `b*_1 >= 2`, and by `n = 22` abstract mode whenever `b*_1 >= 1` — i.e.
  by several of the sidecar's own separation controls. In every reached
  configuration measured, a one-line repair changes no count.
* **D-E (a refuted control claim).** `RECEIPT.md` states that "for the six
  nonempty fence census cells, abstract mode adds nothing", on the
  strength of an argument about the single fence GF2 and an `n = 22`
  measurement. Measured at `n = 23`: abstract mode gives 8,031 types on
  `b01-bs01` (fence 1,361) and 7,623 on `b01-bs12` (fence 693). The
  correct statement, verified here set-for-set and with `D-1` repaired,
  is that **abstract mode adds no fence-valid type** — which is in fact
  the strongest single control in the whole file, because it removes the
  forced frame and not merely the orderly rule.
* **D-F (a silent algorithm change).** `build_gamma` returns `None` when
  `|Gamma| > 300000`, disabling the orderly rule for that cell without
  any receipt in `summary.json`. This fires on the six `b05-*` cells
  (`|Gamma| = 983040`). Those cells are empty (7 nodes each) and are now
  empty by Theorem C, so nothing is affected.
