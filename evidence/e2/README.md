# E2: the quadratic configuration

[`witness.json`](witness.json) gives 23 points and 23 line covectors over
`Q(w)`, where `w^2=17`.  Each field element is stored as `[a,b]` for
`a+b*w`.  Both real embeddings have exactly the prescribed 92 incidences and
437 nonincidences, with all points and lines distinct.

For the positive embedding `w=sqrt(17)`, the symmetric matrix

```text
S = diag(2, (sqrt(17)-1)/4, 1)
```

maps the point set bijectively to the line set according to the permutation in
[`verification.json`](verification.json).  It defines a polarity because it is
symmetric and nonsingular.  It is positive definite because `sqrt(17)>4`, so
all three diagonal entries are positive.

Run the dependency-free exact checker with Node.js 18 or later:

```sh
node evidence/e2/verify.mjs
```

The checker performs all 529 determinant tests, all 529 point-line dot-product
tests, distinctness checks, four corruption controls and all 23 polarity image
checks.  The two real embeddings are projectively equivalent after relabeling;
the exact matrix and all 46 transported point/line checks are recorded in
[`../action-loci/guard_and_equivalence_receipt.json`](../action-loci/guard_and_equivalence_receipt.json).

