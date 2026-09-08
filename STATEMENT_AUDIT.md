# What the formal statement says

The sole advertised theorem is `Config23.exists_configuration`.
Challenge.lean contains its independent statement; Solution.lean contains
the actual coordinates and proof. Solution never imports Challenge.

Points are pairs of Mathlib real numbers. Lines are real coefficient triples
representing the ordinary affine equation ax+by+c=0. A nonzero normal (a,b)
ensures each equation defines a straight line, excluding both the empty set
and the entire plane. Two such equations define the same line exactly when
their coefficient triples are proportional. `DifferentLines` requires one
of the three 2x2 minors to be nonzero, excluding that possibility.

The length-23 point list has pairwise unequal entries. The length-23 line
list has pairwise nonproportional equations. List counts therefore coincide
with counts of distinct geometric objects, not multiplicities. Each degree
counts all zero evaluations against the entire opposite list; an unintended
fifth incidence makes the formal proposition false. The points all have
finite coordinates. No generic-position assumption or approximate tolerance
is used. Additional joins not selected as configuration lines are permitted
by the usual selected-set definition.

`IsConfiguration n k` is a generic coordinate spelling of this definition;
it does not encode the desired answer, a particular incidence graph or the
witness. The existential theorem supplies its two lists with no hypotheses.
All actual fractions, the coordinate chart and all arithmetic are in Solution.
Challenge imports only Mathlib modules; it is 35 lines and 1548 bytes.

The formal result does not assert that these are the only realizations,
classify V4 actions, formalize publication priority, or prove rationality as
a separate quantified property. Its displayed witness uses rational arithmetic,
and the informal proof provides its compact rational description. No census
certificate or search code is a premise. The optional Std-only certificate is
a separate arithmetic check, not an imported axiom or dependency.

Research interest is the explicit existence construction for the historically
remaining 23-point case of geometric four-configurations. This is the full
existence statement expressed in coordinates, rather than an intermediate
lemma standing in for it. The bounded literature history is in LITERATURE.md;
no source author's endorsement or independent human peer review is implied.
