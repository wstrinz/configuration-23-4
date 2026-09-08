import Std
set_option maxRecDepth 100000
set_option maxHeartbeats 0
abbrev V := Int × Int × Int
def dot (p l : V) : Int := p.1*l.1 + p.2.1*l.2.1 + p.2.2*l.2.2
def cross (p q : V) : V :=
  (p.2.1*q.2.2-p.2.2*q.2.1, p.2.2*q.1-p.1*q.2.2, p.1*q.2.1-p.2.1*q.1)
def points : List V := [
  (1,0,0),
  (0,1,1),
  (0,1,-1),
  (0,2,3),
  (0,2,-3),
  (1,0,1),
  (1,0,-1),
  (3,-2,-2),
  (3,2,2),
  (3,-2,2),
  (3,2,-2),
  (2,2,3),
  (2,-2,-3),
  (2,2,-3),
  (2,-2,3),
  (6,2,5),
  (6,-2,-5),
  (6,2,-5),
  (6,-2,5),
  (6,2,-1),
  (6,-2,1),
  (6,2,1),
  (6,-2,-1)]
def lines : List V := [
  (1,0,0),
  (0,1,-1),
  (0,1,1),
  (0,3,-2),
  (0,3,2),
  (1,-3,0),
  (1,3,0),
  (1,2,-2),
  (1,-2,2),
  (1,2,2),
  (1,-2,-2),
  (2,9,-6),
  (2,-9,6),
  (2,9,6),
  (2,-9,-6),
  (2,5,-2),
  (2,-5,-2),
  (2,-5,2),
  (2,5,2),
  (2,-1,-2),
  (2,1,-2),
  (2,1,2),
  (2,-1,2)]
def valid (ps ls : List V) : Prop :=
  ps.length = 23 ∧ ls.length = 23 ∧
  (∀ p ∈ ps, p ≠ (0,0,0)) ∧ (∀ l ∈ ls, l ≠ (0,0,0)) ∧
  ps.Pairwise (fun p q => cross p q ≠ (0,0,0)) ∧
  ls.Pairwise (fun p q => cross p q ≠ (0,0,0)) ∧
  (∀ p ∈ ps, (ls.filter (fun l => dot p l == 0)).length = 4) ∧
  (∀ l ∈ ls, (ps.filter (fun p => dot p l == 0)).length = 4) ∧
  (∀ p ∈ ps, 3*p.1+8*p.2.2 ≠ 0)
theorem witness_valid : valid points lines := by
  unfold valid
  decide
theorem integer_certificate_exists : ∃ ps ls : List V, valid ps ls :=
  ⟨points, lines, witness_valid⟩
#print axioms witness_valid
#print axioms integer_certificate_exists
