# CFG23 P3/P4 audit — 2026-09-08

Terminal classification: **SUPPORTED** for the three exact pairwise
non-isomorphism decisions and automorphism counts below; **INCONCLUSIVE** for
exhaustive priority/corpus coverage. This is a bounded audit and does not turn
failure to find a source into evidence that no source exists.

Campaign base inspected: `6c300a4c14e9ef117d8c685f1577c7633a023e9e`.

## P3: exact colored-Levi audit

The comparison treats a configuration as a bipartite Levi graph with 23 point
vertices, 23 line vertices, and 92 edges. The primary notion is
**part-preserving isomorphism**. A second exact test allows a global swap of
the two parts, detecting duality/correlation. `python-igraph` 1.0.0 invokes
BLISS for colored canonical permutations; NetworkX 3.6.1 VF2 independently
tests isomorphism and directly verifies each returned edge map. A deterministic
independent relabeling of points and lines leaves both answers unchanged for
all three objects.

| Object | BLISS colored-Levi SHA-256 | part-preserving Aut | full uncolored Levi Aut | self-dual? |
|---|---|---:|---:|---|
| E1 rational (`7309c1e188360585-bc372d1fe46f0e80`) | `db292b0ac1c1b87370cc8c2b8f9201aef0fbeeeecd34cbc021c53b9ba1f4985a` | 4 (`V4`) | 8 | yes |
| E2 quadratic (`143bd9ddf2aa1263-990b67811d33c3fb`) | `df25d6e7eec1c86deb7cb987502962ebc02b284ec01900bbc281935761f5996f` | 8 (`C4 x C2`) | 16 | yes |
| Cuntz CT1-S1 | `2ec9fddf9787f5b2078718c5932bdd0647005c6b388c4b62f02eb4126338c0c4` | 8 (`D4`) | 8 | no |

All three BLISS digests differ. VF2 agrees that:

- E1 is not isomorphic to E2, even after swapping points and lines;
- E1 is not isomorphic to CT1-S1, even after swapping points and lines;
- E2 is not isomorphic to CT1-S1, even after swapping points and lines.

The packet phrase “8 abstract, 4 geometric” must not be applied indiscriminately
to both configurations. For E1, the part-preserving abstract automorphism
group has order 4; order 8 is the full uncolored Levi automorphism group and
includes point/line-swapping correlations. E1's four sign-change
collineations account for its order-4 part-preserving group. E2 has order 8
part-preserving and order 16 after correlations. Exact element-order and
commutativity checks identify the part-preserving groups as `V4` for E1,
`C4 x C2` for E2, and `D4` for CT1-S1. The graph audit alone does not
determine which of E2's eight part-preserving automorphisms are induced by
real projective collineations. The later exact calculation in
`../action-loci/guard_and_equivalence_receipt.json` checks all eight: four are
collineations of one real embedding and four exchange the conjugate
embeddings. Thus E2's geometric collineation group is V4.

### External-corpus boundary

No additional exact public `(23_4)` incidence table was recovered from the
bounded sources below, so there was no fourth public table to feed to BLISS.

- Cuntz's 2017/2018 primary paper prints CT-1 and reports at least three more
  complex examples, but supplies no exact data for those additional objects:
  [arXiv:1705.00927](https://arxiv.org/abs/1705.00927), DOI
  [10.26493/1855-3974.1402.733](https://doi.org/10.26493/1855-3974.1402.733).
  The campaign's earlier source-custody audit reached the same bounded result.
- Bokowski–Pilaud's topological enumeration paper reports applications at
  orders 18 and 19, not a published 23-point corpus:
  [arXiv:1210.0306](https://arxiv.org/abs/1210.0306). Their
  quasi-configuration paper constructs orders 37 and 43 and historically
  lists 23 as open; it does not provide a `(23_4)` list:
  [arXiv:1403.7939](https://arxiv.org/abs/1403.7939).
- Betten–Brinkmann–Pisanski, *Counting symmetric configurations v3*, concerns
  `(v_3)` configurations (tables through `v=18`, triangle-free through 21),
  rather than a `(23_4)` corpus: DOI
  [10.1016/S0166-218X(99)00143-2](https://doi.org/10.1016/S0166-218X(99)00143-2).
- [House of Graphs](https://houseofgraphs.org/) describes its principal
  searchable collection as curated “interesting” graphs rather than a
  complete list of all 46-vertex 4-regular bipartite girth-six graphs.
  Targeted current searches for `23_4`, Cuntz, and a 46-vertex Levi graph did
  not surface an exact candidate. This is “no match found in the targeted
  public search,” not proof that no relevant user-contributed entry exists.

### CT-1 lane status

The original CT1-S1 real-emptiness lane is **closed**. The accepted exact
result states that its characteristic-zero realization space modulo `PGL_3`
has exactly two conjugate `Q(i)` labelled classes and no point over any real
closed field. The result is specific to CT1-S1; it did not settle other
`(23_4)` incidence types. Evidence:
`results/accepted/2026-08-23-ct1-nonrealizability-v1.md` and the independent
cold audit `results/accepted/2026-08-24-ct1-theorem-diligence-v1.md`.

## P4: last-18-month literature refresh

Window: **2025-03-08 through 2026-09-08**. Searches covered arXiv notation
variants `(23_4)`, `23_4`, geometric/point-line configuration terms, and
combinations of Cuntz, Berman, Gévay, Pisanski, Pilaud, and Bokowski. Primary
full text was inspected where a result was plausibly relevant.

### Relevant or potentially confusable sources in the window

1. Gévay–Kiss–Pisanski, *The Grünbaum–Rigby configuration as a special
   Kárteszi configuration*, submitted **2025-12-21**
   ([arXiv:2512.18872](https://arxiv.org/abs/2512.18872)). Its construction
   produces `K(n;l,m)` configurations with `3n` points and `3n` lines. It
   proves facts about the `21_4` Grünbaum–Rigby case and a family whose sizes
   are multiples of three, so it does not construct or classify a `23_4`.
2. Berman–Gévay–Richter-Gebert–Tabachnikov, *Constructing Poncelet Polygons*,
   published **2026-07-04**
   ([journal article](https://link.springer.com/article/10.1007/s00454-026-00860-8),
   preprint [arXiv:2408.09225](https://arxiv.org/abs/2408.09225)). It constructs
   Poncelet 7-, 8-, and 10-gons and explains how these yield `(k n)_4`
   configurations. The full text does not supply a `23_4` result.
3. Berman–Gévay–Richter-Gebert–Tabachnikov, *When Grünbaum meets Poncelet:
   infinite classes of movable `(n_4)` configurations*, published online
   **2026-07-14**, DOI
   [10.1017/fms.2026.10254](https://doi.org/10.1017/fms.2026.10254)
   (preprint [arXiv:2408.09203](https://arxiv.org/abs/2408.09203)). The paper
   establishes movable Poncelet/celestial families and discusses the 21-point
   configuration. A full-text search did not locate a 23-point construction or
   a new assertion that 23 remained open.
4. Subercaseaux–Mackey–Qian–Heule, *Automated Symmetric Constructions in
   Discrete Geometry*, submitted **2025-05-30**
   ([arXiv:2506.00224](https://arxiv.org/abs/2506.00224)). Its “23-point
   configuration” is for the everywhere-unbalanced-points problem, not a
   point-line `(23_4)` configuration.
5. Krapivin–Przybocki–Heule, *Toward Satisfiability Modulo Realizability*,
   submitted **2026-07-03**
   ([arXiv:2607.02958](https://arxiv.org/abs/2607.02958)). Its 23-point result
   concerns empty convex polygons, not four-incidence configurations.

The Gray-configuration preprint [arXiv:2502.14484](https://arxiv.org/abs/2502.14484)
was submitted **2025-02-20**, sixteen days before the strict 18-month window;
it concerns 27 points and does not resolve the target.

### Bounded conclusion and proposed `LITERATURE.md` edits

No earlier real geometric `(23_4)` construction was located in this refresh.
That remains an **INCONCLUSIVE priority statement**: arXiv search and the
listed full texts cannot exclude unpublished, unindexed, recently submitted,
or differently described work.

The current `artifacts/existence-priority-audit-v1/LITERATURE.md` already
contains the Poncelet movable paper, automated-constructions paper, and the
correct bounded-absence language. Proposed additions:

- add the **2025-12-21 Kárteszi paper** and explain the `3n` size restriction;
- add the **2026-07-04 Constructing Poncelet Polygons** publication and state
  that its explicit 7/8/10-gon constructions do not yield order 23;
- state the strict refresh window and move the **2025-02-20 Gray paper** to a
  “just outside window” note;
- retain: “latest verified explicit open-status statement is October 2021”;
  none of the newly checked papers makes a later explicit 23-open statement.

## Receipts and replay

Inputs:

- E1: `rational_23_4.json`, SHA-256
  `68814038bfd8d6abde98b57338e3fa7bf64b5aad8c8089d771fb198091c4f038`
- E2: `quadratic_23_4.json`, SHA-256
  `aafc0cb955ef30a52440d25c06bcf495a631063dedb4610781f6ff889e49dc32`
- CT1-S1: `ct1_reconstruction.json`, SHA-256
  `65f9d6b7608bd6c0c1fa47b91b2cf6ff5bc3e5ef02070c0660c0471ee795ae01`

Files in this lane:

- `audit_isomorphism.py`
- `isomorphism_receipt.json`

Replay from the public repository root after installing
`evidence/requirements.txt`:

```sh
python evidence/combinatorics/audit_isomorphism.py
```
