import Mathlib.Data.Real.Basic
import Mathlib.Data.List.Pairwise

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

/-- There exists a geometric (23_4) configuration with finite real coordinates. -/
theorem exists_configuration : ∃ ps ls, IsConfiguration 23 4 ps ls := by
  sorry

end Config23
