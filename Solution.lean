import Mathlib.Data.Real.Basic
import Mathlib.Data.List.Pairwise
import Mathlib.Tactic.NormNum

/-! A geometric (23_4) configuration in the real affine plane.
Points are pairs (x,y). Lines are triples (a,b,c) meaning a*x+b*y+c=0.
Nonzero normals exclude empty sets and the whole plane. A nonzero minor
between coefficient triples excludes proportional equations, hence repeated
geometric lines. Counts concern precisely the two selected finite sets.
-/
namespace Config23

abbrev Point := ℝ × ℝ
abbrev Line := ℝ × ℝ × ℝ

/-- Incidence with the ordinary affine straight line a*x+b*y+c=0. -/
def Incident (p : Point) (l : Line) : Prop := l.1*p.1 + l.2.1*p.2 + l.2.2 = 0

/-- Distinct projective coefficient triples: at least one 2-by-2 minor is nonzero. -/
def DifferentLines (l m : Line) : Prop :=
  l.1*m.2.1 ≠ m.1*l.2.1 ∨ l.1*m.2.2 ≠ m.1*l.2.2 ∨
  l.2.1*m.2.2 ≠ m.2.1*l.2.2

/-- Exactly n distinct real points and n distinct straight lines, each of degree k. -/
noncomputable def IsConfiguration (n k : ℕ) (ps : List Point) (ls : List Line) : Prop := by
  classical
  exact ps.length = n ∧ ls.length = n ∧ ps.Pairwise (· ≠ ·) ∧
    (∀ l ∈ ls, l.1 ≠ 0 ∨ l.2.1 ≠ 0) ∧ ls.Pairwise DifferentLines ∧
    (∀ p ∈ ps, (ls.filter fun l => decide (Incident p l)).length = k) ∧
    (∀ l ∈ ls, (ps.filter fun p => decide (Incident p l)).length = k)


noncomputable def points : List Point := [
  ((1 / 3), 0),
  (0, (1 / 8)),
  (0, (-1 / 8)),
  (0, (1 / 12)),
  (0, (-1 / 12)),
  ((1 / 11), 0),
  ((-1 / 5), 0),
  ((-3 / 7), (2 / 7)),
  ((3 / 25), (2 / 25)),
  ((3 / 25), (-2 / 25)),
  ((-3 / 7), (-2 / 7)),
  ((1 / 15), (1 / 15)),
  ((-1 / 9), (1 / 9)),
  ((-1 / 9), (-1 / 9)),
  ((1 / 15), (-1 / 15)),
  ((3 / 29), (1 / 29)),
  ((-3 / 11), (1 / 11)),
  ((-3 / 11), (-1 / 11)),
  ((3 / 29), (-1 / 29)),
  ((3 / 5), (1 / 5)),
  ((3 / 13), (-1 / 13)),
  ((3 / 13), (1 / 13)),
  ((3 / 5), (-1 / 5))]

noncomputable def lines : List Line := [
  (8, 0, 0),
  (3, 8, -1),
  (-3, 8, 1),
  (6, 24, -2),
  (-6, 24, 2),
  (8, -24, 0),
  (8, 24, 0),
  (14, 16, -2),
  (2, -16, 2),
  (2, 16, 2),
  (14, -16, -2),
  (34, 72, -6),
  (-2, -72, 6),
  (-2, 72, 6),
  (34, -72, -6),
  (22, 40, -2),
  (22, -40, -2),
  (10, -40, 2),
  (10, 40, 2),
  (22, -8, -2),
  (22, 8, -2),
  (10, 8, 2),
  (10, -8, 2)]

set_option maxRecDepth 100000
set_option maxHeartbeats 0
theorem witness_valid : IsConfiguration 23 4 points lines := by
  norm_num [IsConfiguration, points, lines, Incident, DifferentLines,
    List.pairwise_cons, Prod.mk.injEq]

theorem exists_configuration : ∃ ps ls, IsConfiguration 23 4 ps ls :=
  ⟨points, lines, witness_valid⟩

end Config23
#print axioms Config23.exists_configuration
