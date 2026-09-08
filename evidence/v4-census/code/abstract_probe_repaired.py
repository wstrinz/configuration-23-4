"""Re-run the abstract-vs-fence control with defect D1 repaired, so that
the "abstract mode finds no extra fence-valid type" conclusion does not
depend on the defective stab-1 coset generator."""
import json, os, sys, time
HERE=os.path.dirname(os.path.abspath(__file__)); ART=os.path.dirname(HERE)
sys.path.insert(0,HERE)
import adversaries as adv
m = adv._load_sidecar('vc_abs_rep', 'repair_i1')
out={}
for cell in [(0,1,0,1),(0,1,1,2)]:
    row={}
    for mode in ('fence','abstract'):
        ps,slots,meta = m.cell23(*cell, mode=mode)
        se = m.Search(ps, slots, mode, time.monotonic()+2400.0)
        res = se.run('n23-%s'%mode, meta)
        row[mode]={'types':len(res),
                   'fence_valid':sum(1 for r in res.values() if r['fence_valid']),
                   'fence_valid_digests':sorted(d for d,r in res.items() if r['fence_valid']),
                   'status':'TRUNCATED' if se.truncated else 'COMPLETE'}
        print(json.dumps({'cell':'b%d%d-bs%d%d'%cell,'mode':mode,
                          'types':row[mode]['types'],
                          'fence_valid':row[mode]['fence_valid'],
                          'status':row[mode]['status']}),flush=True)
    out['b%d%d-bs%d%d'%cell]={
        'repaired_fence_types':row['fence']['types'],
        'repaired_abstract_types':row['abstract']['types'],
        'repaired_abstract_fence_valid':row['abstract']['fence_valid'],
        'fence_valid_sets_equal':
            set(row['abstract']['fence_valid_digests'])==set(row['fence']['fence_valid_digests']),
        'status':(row['fence']['status'],row['abstract']['status'])}
with open(os.path.join(ART,'output','item2_abstract_vs_fence_repaired.json'),'w') as fh:
    json.dump(out,fh,indent=1,default=str)
print(json.dumps(out,indent=1,default=str))
