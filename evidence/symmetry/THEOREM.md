# Accepted result — real collineation symmetry has order at most four

**Accepted by:** DKC

**Date:** 2026-08-24

**Classification:** `PROOF` / `SUPPORTED`

**Theorem status:** accepted within CFG23; novelty not established

## Statement

For every geometric `(23_4)` configuration `X` in the real projective plane,
its collineation symmetry group satisfies

`Sym(X) <= PGL_3(R)` and `|Sym(X)| in {1,2,4}`.

If its order is four, then `Sym(X)` is the Klein four-group `V4`; a cyclic
order-four symmetry is impossible. This concerns collineations only. It does
not bound a group enlarged by correlations, prove that any surviving symmetry
type occurs, or constrain a hypothetical configuration with trivial symmetry.

## Proof audited at intake

The accepted 2-power theorem first reduces the problem to finite real
2-subgroups. The worker's self-contained argument then establishes:

1. `PGL_3(R)` is isomorphic to `SL_3(R)` through the unique determinant-one
   representative of each projective class.
2. Averaging an inner product conjugates every finite subgroup into `SO(3)`.
3. A central-involution argument shows that a finite 2-subgroup of `SO(3)` is
   cyclic or dihedral. In the dihedral case its cyclic subgroup consists of
   rotations about one common axis.
4. For cyclic `C_n`, or dihedral `D_n` of order `2n`, with `n >= 4` a power of
   two, the projective point-orbit sizes force the common pole `F` to be a
   configuration point. The dual orbit count forces the polar invariant line
   `L` to be a configuration line.
5. Exactly four configuration points lie on `L`, while `F` is not on `L`.
   The remaining `23-1-4=18` points lie in orbits whose sizes are multiples of
   `n`. Since no power of two `n >= 4` divides 18, all cyclic and dihedral
   cases of order at least eight are impossible. The same count excludes
   `C_4`; the exceptional `D_2 = V4` survives the necessary count.

The coordinator independently checked the group classification and the
projective fixed-locus/orbit argument, then replayed both retained exact
corroboration scripts. Their outputs were byte-stable and reported only
`C2` and `V4` as surviving action groups.

## Certificate custody

- Full proof candidate:
  `results/inbox/2026-08-23-dk-symmetry-action-classification-v1.md`,
  SHA-256
  `21EA19EE4AF92E731AE63DFD4AB4E1E70F80DF16B23FF345EB22ECA53E01650E`.
- Exact orbit replay:
  `artifacts/symmetry-action-classification-v1/verify_orbit_structure.py`,
  SHA-256
  `C7129714BF48D656BC8E52866AF6095E5E46DD6B6964AD1C8C0573AB94DB5C10`.
- Exact divisibility replay:
  `artifacts/symmetry-action-classification-v1/divisibility_scan.py`,
  SHA-256
  `DF3C1262BD3074CC1DDDB6DB8934772A853DFD25713709698BD2EE15C8EE9333`.

Replay:

```powershell
python artifacts/symmetry-action-classification-v1/verify_orbit_structure.py
python artifacts/symmetry-action-classification-v1/divisibility_scan.py
```

**Graph effect:** none. This is a projective group-theoretic proof, outside
Grand Portage's current ideal/transport claim vocabulary.
