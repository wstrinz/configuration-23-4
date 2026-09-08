# Cuntz CT1-S1 comparison

This directory concerns the specific CT1-S1 incidence type reconstructed from
Cuntz's complex `(23_4)` example.  It does not make a statement about every
complex example in that paper.

[`PROOF.md`](PROOF.md) gives the chart-cover argument and exact saturated ideal.
After a projective frame is fixed, every valid characteristic-zero realization
lies in the two-point scheme

```text
8*t5^2 - 12*t5 + 5 = 0,
```

with all other parameters affine-linear in `t5`.  Its discriminant is `-16`,
so the two solutions are conjugate over `Q(i)` and neither is real.  The
structural, saturation, and automorphism receipts are retained beside the
proof.  The independent [combinatorial audit](../combinatorics/REPORT.md)
confirms that CT1-S1 is nonisomorphic to both E1 and E2, with or without a
global point-line swap.

