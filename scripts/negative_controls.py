"""Run sequentially in a disposable checkout after verify-comparator.sh.

Temporarily mutates Solution.lean, restores its exact bytes in finally, and
rebuilds the original. Never run concurrently with a build or another editor.
"""
from pathlib import Path
import hashlib, json, os, subprocess, time

root=Path(__file__).resolve().parent.parent
source=root/'Solution.lean'
original=source.read_bytes()
text=original.decode('utf-8')
cache=Path(os.environ.get('PALOMAR_COMPARATOR_CACHE',str(root/'.cache/palomar-comparator')))
env=os.environ.copy()
env.update(PALOMAR_LANDRUN_BIN=str(cache/'bin/landrun'),
 COMPARATOR_LEAN4EXPORT=str(cache/'lean4export/.lake/build/bin/lean4export'),
 COMPARATOR_NANODA=str(cache/'nanoda/target/release/nanoda_bin'),
 COMPARATOR_LANDRUN=str(root/'scripts/landrun-wrapper.sh'))
comparator=['lake','env',str(cache/'comparator/.lake/build/bin/comparator'),'comparator.json']
needle='theorem exists_configuration : ∃ ps ls, IsConfiguration 23 4 ps ls :=\n  ⟨points, lines, witness_valid⟩'
assert needle in text
variants=[
 ('moved_point',text.replace('((1 / 3), 0)','((2 / 3), 0)',1),['lake','env','lean','Solution.lean']),
 ('weakened_theorem',text.replace(needle,'theorem exists_configuration : True := True.intro'),comparator),
 ('unproved_solution',text.replace(needle,'theorem exists_configuration : ∃ ps ls, IsConfiguration 23 4 ps ls := by sorry'),comparator)]
results=[]
try:
 for label,content,command in variants:
  source.write_text(content,encoding='utf-8',newline='\n')
  start=time.monotonic()
  r=subprocess.run(command,cwd=root,env=env,capture_output=True,text=True,timeout=600)
  assert r.returncode!=0,(label,r.stdout,r.stderr)
  output=r.stdout+r.stderr
  assert 'Your solution is okay!' not in output
  if label=='moved_point': assert 'unsolved goals' in output,output
  elif label=='weakened_theorem': assert 'statement do not match' in output,output
  else: assert 'sorryAx' in output,output
  results.append(dict(control=label,exit_code=r.returncode,seconds=round(time.monotonic()-start,3),output=output))
  print(label, 'rejected',flush=True)
finally:
 source.write_bytes(original)
assert hashlib.sha256(source.read_bytes()).digest()==hashlib.sha256(original).digest()
subprocess.run(['lake','build','Solution'],cwd=root,env=env,check=True)
(root/'verification').mkdir(exist_ok=True)
(root/'verification/negative-controls.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8',newline='\n')
