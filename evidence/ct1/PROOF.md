# CT-1 capstone repair v1 (Lane DKA, task `ct1-capstone-repair-v1`)

**Task/lane IDs:** `ct1-capstone-repair-v1`, DKW-LSA
**Branch:** `agent/local-sonnet/ct1-capstone-repair-v1`
**Execution base:** `f4065602c45e8f660ff68f41214dd1272daa872b`
**Accepted mathematical base:** `4aab945c0d6bf87aca04e0639d8b5e9abceb4c2d`
**Scope:** repair the rejected CT-1 chart-cover capstone
(`results/accepted/2026-08-23-ct1-chart-cover-components-v1.md`) without
using the 31 scalar `CHART` guards `L(v) = v0+2*v1+5*v2 != 0`, using only
exact construction facts and the five genuine forbidden-fifth factors of
the already-accepted saturation.

All computation is reproducible from committed scripts (pure Python,
`fractions.Fraction`-based exact Gaussian-rational arithmetic reused
byte-for-byte from the accepted `ct1_checker.py`; no floating point, no new
CAS run):

```
python artifacts/ct1-capstone-repair-v1/construction/replay_general.py
python artifacts/ct1-capstone-repair-v1/analysis/structural_checks.py
python artifacts/ct1-capstone-repair-v1/analysis/verify_saturation_2points.py
python artifacts/ct1-capstone-repair-v1/analysis/automorphism.py
```

## 0. What is inherited and what is not (task item 1)

**Inherited (accepted, composed with, never re-derived here):**

- The CT1-PRES-V1 frame-fixed presentation itself: `Q[t1,...,t6]`, 14 raw
  closed-incidence generators, 437 forbidden-fifth guards
  (`results/accepted/2026-08-23-ct1-realization-presentation-v1.md`).
- The 63-nonempty-infinity-stratum sweep (all void: 27 by identically-zero
  guard, 36 by degenerate collision) and the frame general-position
  argument's *combinatorial shape*
  (`results/accepted/2026-08-23-ct1-chart-cover-components-v1.md`
  explicitly accepts these two pieces; only the capstone chain-closure step
  is rejected).
- The exact saturation identity `I : g^infinity = J`,
  `g = (1-t3)(1-t6)*t6*(1-t2*t3)*(t6-t4)`,
  `J = (2*t6-1, 2*t4-2*t5+1, t3-2*t5+1, t2+2*t5-2, t1+2*t5-1,
  8*t5^2-12*t5+5)` (`results/accepted/2026-08-23-ct1-restricted-chart-exhaustion.md`,
  `artifacts/ct1-elimination-v1/ELIMINATION.md`).

**Explicitly NOT inherited:**

- `output/capstone_certificate.json`'s `overall.chain_holds` field.
- `capstone_coverage_certificate.py` item 3's conclusion ("the 31 CHART
  guards are redundant") and everything built on it. That argument proves
  a constructed cross-product vector `v` is nonzero; it does **not** prove
  the specific linear functional `L(v) = v0+2*v1+5*v2` is nonzero (`v`
  nonzero does not imply `L(v)` nonzero — `v` can be nonzero and still lie
  in the hyperplane `L=0`). The rejected certificate's checker never
  evaluated the 31 `L(v)` polynomials at all. **This repair never
  evaluates or references any of the 31 `L(v)` guards anywhere below**
  (enforced at run time in `structural_checks.py`, which greps its own
  source for `chart_guards` field access and fails if any executable
  reference is found outside that one check).

## 1. Lemma B: global distinctness from prescribed non-incidence

For any two **distinct** declared point ids `p != q` (of the 23), and *any*
realization `phi` of CT1-S1 — any assignment of the 23 points/23 lines to
`P^2(K)` satisfying every prescribed incidence **and** every prescribed
non-incidence (the genuine "exactly four" `(23,23,4,4)` condition;
`EVIDENCE_POLICY.md`: "incidence equalities without checked forbidden
incidences establish only the closed incidence scheme, not a geometric
`(23_4)` realization") — `phi(p)` and `phi(q)` are distinct projective
points, equivalently their nonzero representatives are nonproportional.

*Proof.* `p` has exactly 4 config lines; `p` and `q` share at most 1
config line (any two of the 23 points share at most one config line —
re-checked directly on the raw combinatorial data by
`structural_checks.py`'s `check_at_most_one_shared`, independent of and
not reusing `build_presentation.py`'s own `structural_sanity`). So at
least 3 of `p`'s 4 lines are not among `q`'s. Pick one such line `L`: `L`
is prescribed through `p`, so `phi(L).phi(p) = 0`; `L` is *not* prescribed
through `q`, so `(L,q)` is one of the declared 437 forbidden-fifth guards,
i.e. `phi(L).phi(q) != 0` for every valid realization. If `phi(p) =
phi(q)` these two facts contradict each other. Hence `phi(p) != phi(q)`.
Dually for lines. QED.

Consequence, used at every `meet`/`join` step below: if a step combines
two **declared-distinct** ids `p != q` (points for a `meet` building a
line; lines for a `join` building a point), the cross product `phi(p) x
phi(q)` is nonzero for *every* realization `phi` — a cross product
vanishes iff its two vectors are proportional, i.e. represent the same
projective point/line, which Lemma B rules out. No scalar functional of
the vector is needed anywhere in this step: "nonzero cross product" here
is exactly and only "the two projective objects are distinct."

`structural_checks.py` walks all 36 meet/join steps of the CT1-PRES-V1
construction log and exhibits, for each, an explicit forbidden-fifth
witness pair proving the relevant Lemma B instance: **23/23 `meet` steps
and 13/13 `join` steps**, all nonzero, none via any `CHART` guard. Full
detail in `output/structural_checks_report.json`.

## 2. Sequential projective-normalization proof (task item 2)

**No bihomogeneous compactified scheme is built anywhere in this
argument.** The claim is per-realization: given *any* actual realization
`phi` of CT1-S1 over a field `K` of characteristic `0`, we show `phi`,
run through CT1-PRES-V1's own deterministic construction order, is
well-defined at every step and resolves to a specific point of `V(I)`.

**Step 0 (frame).** `{0,1,4,11}` is in general position in *every*
realization, unconditionally — re-derived purely combinatorially in
`structural_checks.py`'s `check_frame_general_position` (independent
reproduction of `COVERAGE.md` section 4): each of the 4 triples
`{0,1,4},{0,1,11},{0,4,11},{1,4,11}` would force two distinct declared
config lines to coincide as actual coordinates if collinear, which is a
direct instance of the dual of Lemma B and hence impossible. So the unique
projectivity `g in PGL_3(K)` sending `phi(0),phi(1),phi(4),phi(11)` to the
standard frame `e1,e2,e3,(1:1:1)` always exists and is unique (standard
projective-frame fact, `lambda_i != 0` for all three scaling coefficients
— re-checked exactly at both known witnesses by `replay_general.py`'s
frame-determinant/lambda asserts, which fail loudly if ever violated).
Replace `phi` by `g . phi`; call it the *normalized* realization. Only
this normalized `phi` is discussed below.

**Step 1 (closed steps, induction on construction order).** At every
`meet(a,b)`/`join(a,b)` step where `a,b` are already-resolved declared ids,
Lemma B (section 1) gives `phi(a) != phi(b)`, hence the cross product is
nonzero, hence the newly-built line/point is well-defined and — by
induction — literally equal (as a projective point) to CT1-PRES-V1's own
symbolic formula for that step evaluated at whatever `t`-values have been
resolved so far (base case: the frame points match by construction; each
closed step reproduces the same cross-product formula from the same two
already-matched inputs).

**Step 2 (free-parameter steps).** At a free-parameter step, the
presentation's affine chart `w + t*v` together with the single excluded
direction `[v]` literally partitions the entire `P^1` of the known
carrier line. So `phi`'s actual point on that line is *either* `[v]`
(the `t = infinity` case) *or* `w + t*v` for a unique finite `t in K`. No
case is left uncovered and no compactified scheme is needed to say this —
it is the ordinary fact that a line's points are the affine chart plus one
point at infinity.

**Step 3 (ruling out infinity — composes with the accepted stratum
sweep).** If *any* of the 6 free points lands at its excluded direction,
the realization sits in one of the 63 nonempty infinity-pattern strata
`S subset {1,...,6}`. The already-accepted sweep
(`artifacts/ct1-chart-cover-v1/output/stratum_sweep_report.json`, composed
with here via `structural_checks.py`, not re-run) shows every one of
these 63 patterns is void: either a declared forbidden-fifth guard is
identically zero on that stratum (27 cases — an outright violation of the
"exactly four" definition for *every* value of the surviving parameters,
hence for `phi` too), or the deterministic construction hits a
`DEGENERATE_MEET`/`DEGENERATE_JOIN` — i.e. Lemma B's own conclusion
(two officially-distinct ids forced to the identical vector) fails
identically, which is impossible by section 1's Lemma B applied directly
to `phi`. Either way, `S` nonempty is impossible for **any** valid `phi`.

**Conclusion of section 2.** Every valid realization `phi`, after the
unique normalization of Step 0, has all six free parameters resolve to
**finite** values `(t1,...,t6) in K^6`, and at every step (free or closed)
`phi` agrees exactly with CT1-PRES-V1's symbolic construction evaluated at
that tuple. This is exactly "every valid finite normalized realization" —
now proven to be *every* valid realization, not merely an assumed
restriction.

## 3. `V(I) intersect D(g)` (task item 3)

Because `phi` agrees with the symbolic construction at `(t1,...,t6)`:

- Every one of the 14 raw closed-incidence generators is the symbolic
  difference of two sides of a prescribed incidence that `phi` genuinely
  satisfies — so every generator vanishes at `(t1,...,t6)`: **`(t1,...,t6)
  in V(I)`.**
- The five factors of `g = (1-t3)(1-t6)*t6*(1-t2*t3)*(t6-t4)` are each,
  literally, one specific forbidden-fifth guard expression (not a `CHART`
  guard — the distinction the coordinator's rejection turns on):

  | factor | forbidden-fifth pair | expr in `presentation.json` |
  |---|---|---|
  | `1-t3` | line 1, point 8 | `1 - t3` |
  | `1-t6` | line 2, point 11 | `1 - t6` |
  | `t6` | line 0, point 8 | `t6` |
  | `1-t2*t3` | line 1, point 3 | `-t2*t3 + 1` |
  | `t6-t4` | line 2, point 6 | `-t4 + t6` |

  (exact string match confirmed programmatically,
  `structural_checks.py`'s `check_g_factors`, table in
  `output/structural_checks_report.json`). Since `phi` is a genuine
  realization, every one of the 437 forbidden-fifth guards is nonzero at
  `phi`, in particular these five — so **`g(t1,...,t6) != 0`, i.e.
  `(t1,...,t6) in D(g)`.**

**No `CHART` guard is invoked at any point in this section.** The only
guards used are 437-list forbidden-fifth guards (the genuine "exactly
four" defining conditions) and Lemma B (an unconditional distinctness
fact, not a guard at all).

## 4. Composition with the accepted saturation and two-point replay (task item 4)

By section 3, every valid realization's normalized point
`(t1,...,t6)` lies in `V(I) intersect D(g)`. The accepted saturation
identity gives `V(I) intersect D(g) = V(I:g^infinity) intersect D(g) =
V(J) intersect D(g)`. So `(t1,...,t6) in V(J)`.

**`V(J)` has exactly two points**, verified here by elementary algebra,
not by re-trusting the accepted Singular `vdim` computation:
`verify_saturation_2points.py` solves `J`'s 6 generators directly (`t6 =
1/2`; `t1,t2,t3,t4` each an explicit affine-linear function of `t5`; `t5`
itself solving `8*t5^2-12*t5+5=0`, discriminant `-16 != 0`, hence exactly
2 roots, no multiplicity) and confirms the two resulting points are
**exactly** the two points `replay_general.py` independently resolves for
the Cuntz witness and its complex conjugate (`output/saturation_2points_report.json`).
Both points also satisfy `D(g)` (all 437 forbidden-fifth guards nonzero,
confirmed by `replay_general.py` for both, independent of the original
`ct1-elimination-v1/output/two_points_verify_report.json`).

**Field/projective-label scope (task item 4):** this argument is stated
and checked over `K` an algebraically closed field of characteristic `0`
(concretely `Qbar`, containing `Q(i)`; the discriminant argument needs
`char(K) != 2`, already implied by characteristic `0`). Realizations are
projective, i.e. points/lines of `P^2(K)`, coordinates up to a common
nonzero scalar; "the frame-fixing projectivity" means the unique element
of `PGL_3(K)`, and "labelled" means the combinatorial point/line ids
`0..22` are fixed identifiers, not interchangeable.

**Because the frame-fixing projectivity of Step 0 is unique for a given
`phi`**, two realizations are projectively equivalent (as *labelled*
structures — same combinatorial id assigned the same orbit) iff their
normalized `(t1,...,t6)` tuples are literally identical. So `V(J)`'s two
points correspond to **exactly two labelled `PGL_3(K)`-equivalence
classes** of realizations of CT-1 — no more (section 2-4 above), no fewer
(both are exhibited, independently replayed). Both require `t5 = 3/4 +/-
1/4*I`, so both have nonzero imaginary part in every one of the six
coordinates depending on `t5` — **neither is defined over any real
subfield of `K`**, for any embedding of `K` extending `Q(i)/Q`
(`8t5^2-12t5+5` has no real root regardless of which ordered/real-closed
field is used, since its discriminant `-16` is negative in `Q`, hence in
every ordered extension). Hence: **CT-1 (this specific accepted
`(23,23,4,4)` combinatorial incidence type) has no real projective
realization.**

## 5. Labelled automorphism group and the conjugate-point exchange test (task item 5)

`automorphism.py` computes `Aut(CT1-S1)` exactly: the point-line incidence
bipartite graph (23+23 vertices, 2-colored so every automorphism sends
points to points and lines to lines) is fed to the already-accepted exact
backtracking search `graph_automorphism.find_automorphisms`
(`orbit-automorphism-recovery-v1`, its own completeness argument re-cited,
not re-derived), independently re-verified here against the raw incidence
data directly (not the search module's internal representation) and
checked to form a genuine group (`verify_group_closure`).

**`|Aut(CT1-S1)| = 8`.**

`Aut(CT1-S1)` acts on the 2-element set of labelled `PGL`-equivalence
classes `{[phi_+], [phi_-]}` (section 4) via `sigma . [phi] := [phi o
sigma]` (well-defined: `phi o sigma` is again a valid realization of the
same abstract type since `sigma` preserves incidence, and post-composition
equivalence commutes with pre-composition). This action was tested
**directly on all 8 elements** (small enough that no generating-set
shortcut was needed): for each `sigma`, relabel the Cuntz witness by
`sigma`'s point-part, re-run the *entire* frame-normalize-and-replay
procedure from scratch at the fixed index set `{0,1,4,11}` (valid for
every `sigma` since general position there is unconditional, section 2
Step 0 — no dependence on `sigma` fixing the frame setwise), and read off
which of the two known points it lands on.

**Result: 4 of the 8 automorphisms fix both classes; the other 4 swap
them** (`output/automorphism_report.json`, `some_automorphism_swaps_the_two_conjugate_points:
true`). Every one of the 8 relabelled replays independently landed on
exactly one of the two known points (never a third value), confirming —
not merely assuming — the section 2-4 dichotomy under every relabelling.

**Labelled vs. unlabeled projective-class counts, kept distinct as
required:**

- **Labelled** (fixed combinatorial ids `0..22`, `PGL_3(K)`-equivalence
  only): **exactly 2** classes (section 4).
- **Unlabeled under part-preserving relabelling** (additionally quotient by
  the computed part-preserving `Aut(CT1-S1)`, i.e. two
  realizations counted as the same configuration if related by *any*
  relabelling composed with a projectivity): since `Aut(CT1-S1)` acts
  transitively on `{[phi_+],[phi_-]}` (a swap exists), the two labelled
  classes merge into **exactly 1** unlabeled class.

## 6. Verdict (task item 6)

**SUPPORTED.** The repaired chain is complete: section 1 (Lemma B) to
section 2 (sequential normalization, composing with the accepted
stratum sweep) to section 3 (`V(I) intersect D(g)`, using only the five
genuine forbidden-fifth `g`-factors, zero `CHART` guards) to section 4
(composition with the accepted `I:g^infinity=J` and independently
re-verified two-point locus) to section 5 (automorphism/conjugate-exchange
computation) is unbroken, and every load-bearing step is backed by an
independently re-runnable exact script (no numerics: all arithmetic is
exact `Q`/`Q(i)` rational or Gaussian-rational; no floating point,
sampling, or interval reasoning anywhere in this repair).

**Precise proposition proven:** every realization of CT-1's specific
labelled `(23,23,4,4)` combinatorial incidence type, over any field of
characteristic `0`, is — via the always-unique frame-fixing projectivity
— one of exactly two points of `V(J)`, both requiring `t5 = 3/4 +/- 1/4*I`
and hence non-real. **CT-1 has no real projective realization.** This is
an `EMPTY(R)`-style conclusion in the sense already used by the accepted
`2026-08-23-ct1-restricted-chart-exhaustion.md` (an exact, finite,
fully-enumerated algebraic point list with no real member — not a
Sturm/sign certificate, but the same evidentiary strength `EVIDENCE_POLICY.md`
recognizes for a "census closure"-style exact classification).

**Explicitly still open / out of scope**, unchanged from before this
repair:

1. Other, non-isomorphic abstract `(23,23,4,4)` combinatorial types —
   untouched; the campaign's general geometric-`(23_4)` question remains
   open.
2. Independent audit of this repaired chain by DKC or a second lane, per
   `AGENTS.md` (this lane's own vocabulary is `SUPPORTED`, not `accepted`).
3. A different frame/construction order was not independently re-run
   end-to-end (as `COVERAGE.md` section 5 item 3 already flagged; section 2
   above proves the *chosen* frame is always valid, so no other frame is
   *needed*, but this repair does not re-derive the same 14-generator
   ideal from a second frame).
4. GP cannot express the real-locus conclusion directly (campaign P0
   point-universe boundary); see section 7.

## 7. GP feedback mode: counterfactual proof memo (task item 6)

**The question.** Why was the 31-scalar-guard error (`v != 0` proven,
`L(v) != 0` claimed) visible only in artifacts and not caught earlier by
any typed GP check, and what minimal typed coverage/certificate link would
have exposed it sooner?

**What actually exists in GP's schema for exactly this check.** GP's
native `claim` event supports a structured `condition: {all: [{relation:
ZERO|NONZERO, expression}]}` on a `PREDICATE` claim at a model
(`portage_schema`): "`gp verify` also checks the condition at its own
model: ZERO by certified ideal membership and NONZERO by a certified empty
vanishing locus." This is *precisely* the typed mechanism the rejected
capstone needed: a `NONZERO` condition on each of the 31 `L(v)`
polynomials, checked against the raw closed-incidence model, would have
forced an explicit `gp verify` verdict — `VERIFIED`, `UNVERIFIED`, or a
`REFUTED` counterexample — instead of a free-text certificate
(`capstone_coverage_certificate.py`'s JSON `all_31_have_declared_forbidden_fifth_witness:
true`) that a human reader could and did mistake for "the guards hold."

**Two real experiments run against the live graph this session** (not
hypothetical — both events are in `.portage/graph.jsonl` of this
worktree, IDs `CL-CT1-REPAIR-CHARTGUARD-TEST` and
`CL-CT1-REPAIR-CHARTGUARD-TEST-SAT`):

1. `NONZERO` condition `1 - 2*t3` (the actual `L(v)` guard for
   `line 1 := meet(point 4, point 5)`) declared at `M-CT1-CLOSED` (the raw,
   unsaturated, `ideal_pending` closed-incidence model — the model the
   rejected capstone's 31-guard claim would have needed to be checked
   against, since it concerns the *raw* ideal, not the saturated one).
   `gp verify` returned **`UNVERIFIED`**: `"invalid exact membership
   polynomial: a sparse polynomial must contain exactly schema and
   terms"`.
2. The **identical** `NONZERO` condition on the **identical** expression,
   declared instead at `M-CT1-SAT-5GUARDS` (the clean, small, saturated
   6-generator model), **`VERIFIED`** cleanly: `"all 1 structured
   condition atoms were certified... every NONZERO has an exact
   unit-ideal certificate for its vanishing locus."`

**Diagnosis.** The mechanism is not missing and not broken in general —
experiment 2 proves the exact same condition-typed check works end to end
against clean model data. Experiment 1's failure is the *same* pre-existing
defect `artifacts/ct1-elimination-v1/ELIMINATION.md` section 6 already
found and flagged (`doubt`/`WITHDRAW`) months earlier in this campaign:
`M-CT1-CLOSED`'s `generators` field, as declared by the original
`ct1-realization-v1` task, stores `{expr, id, why}` dict objects for only
9 of its 14 accepted generators rather than 14 plain polynomial strings —
so any verify-time reduction against that model's ideal (whether an edge
check, as `ELIMINATION.md` tried, or a condition check, as tried here)
hits malformed input before the real mathematical question is ever
reached. This is graph hygiene of an *upstream* declaration, not a gap in
GP's vocabulary or in the condition-checking feature itself.

**What this means for "visible only in artifacts."** Even with clean
input, `NONZERO` on a raw, positive-dimensional (`dimension 3`) ideal is a
genuinely harder question than on the zero-dimensional saturated one —
`UNVERIFIED` (not `REFUTED`) is the honest answer GP's checker can give
without a fuller decomposition, and that is not a defect. The concrete,
actionable counterfactual is narrower and still real: had `M-CT1-CLOSED`
been declared with clean generator data from the start, and had the
worker declared the 31 `L(v)` guards as `NONZERO` conditions on it
(instead of only asserting a prose "forbidden-fifth witness" argument in
a Python script's docstring/JSON), `gp verify` would have returned
**`UNVERIFIED` for all 31 before the capstone certificate was ever
written** — an honest, visible "not yet checked" badge in the graph
itself, sitting right next to the claim, rather than a JSON boolean
(`all_31_have_declared_forbidden_fifth_witness: true`) that conflates "a
different, weaker fact was checked" with "this fact was checked." The
error would have been caught not by GP *deciding* the guards were false,
but by GP correctly refusing to let an unchecked structured claim masquerade
as a checked one — exactly `EVIDENCE_POLICY.md`'s ladder distinction
between `claimed` and `exact-checked`, made mechanically enforceable
instead of relying on a human coordinator to notice the gap by close
reading (as DKC in fact had to do here).

**Common minimum, with and without GP.** Both routes ultimately need the
same load-bearing mathematics: an explicit forbidden-fifth witness per
guard pair (combinatorial, no coordinates) plus, separately, an explicit
statement of *which* algebraic fact that witness actually establishes
(vector-nonzero, not scalar-nonzero). GP does not supply that
mathematical distinction — a human (or this repair) has to draw it — but
a typed `NONZERO` condition, once declared, *would* have forced the
distinction into the open the moment someone tried to certify the wrong
one, rather than after a full coordinator review cycle.

**Real-locus conclusions remain note-only in the graph**, per the
established campaign P0 boundary
(`results/accepted/2026-08-23-gp-point-universe-equivalence-gap.md`,
`OPERATIONS.md`'s GP point-scope guard): GP's `point_universe` vocabulary
(`BASE`/`ALGEBRAIC_CLOSURE`) has no ordered-real member, so section 6's
"CT-1 has no real realization" conclusion is not and cannot be declared as
an `EMPTY` claim against any GP model — it is recorded here in prose only,
exactly as `2026-08-23-ct1-restricted-chart-exhaustion.md` and
`COVERAGE.md` section 4.1 already did for the narrower restricted-chart
version of the same conclusion.

## 8. Artifacts and hashes

```
construction/replay_general.py
analysis/structural_checks.py
analysis/verify_saturation_2points.py
analysis/automorphism.py
output/structural_checks_report.json
output/saturation_2points_report.json
output/automorphism_report.json
```

(SHA-256 hashes in the lane receipt,
`results/inbox/2026-08-23-dka-ct1-capstone-repair-v1.md`.)

GP graph effect: two live `PREDICATE` condition claims recorded this
session (`CL-CT1-REPAIR-CHARTGUARD-TEST`, `UNVERIFIED`;
`CL-CT1-REPAIR-CHARTGUARD-TEST-SAT`, `VERIFIED`) as the section 7
counterfactual experiment. No new model, `EMPTY`, or `NONEMPTY` claim is
declared for this repair's own real-locus conclusion, for the reason
stated in section 7's last paragraph. Per this task's custody-recovery
instruction, the resulting `.portage/graph.jsonl` mutation and its
generated `.portage/artifacts/sha256/*` blobs are retained on disk (so the
graph state and this receipt stay mutually consistent for anyone who
re-runs `gp verify` in this worktree) but are **not included in this
task's git commit** — recorded as an explicit unresolved custody
obligation for the next lane/session that touches this worktree's graph
state, not silently dropped.
