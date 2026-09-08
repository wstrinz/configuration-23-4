import json, os, sys, time
HERE=os.path.dirname(os.path.abspath(__file__)); ART=os.path.dirname(HERE)
sys.path.insert(0,HERE)
import replay_census as rc
vc = rc.load_sidecar('vc_abs')
rows=[]
for cell in [(0,1,0,1),(0,1,1,2)]:
    for mode in ('fence','abstract'):
        ps,slots,meta = vc.cell23(*cell, mode=mode)
        se = vc.Search(ps, slots, mode, time.monotonic()+1500.0)
        res = se.run('n23-%s-b%d%d-bs%d%d'%((mode,)+cell), meta)
        fv = sum(1 for r in res.values() if r['fence_valid'])
        rows.append({'cell':'b%d%d-bs%d%d'%cell,'mode':mode,'types':len(res),
                     'fence_valid_types':fv,'labelled':se.placed_final,
                     'status':'TRUNCATED' if se.truncated else 'COMPLETE',
                     'digests':sorted(res)})
        print(json.dumps({k:v for k,v in rows[-1].items() if k!='digests'}),flush=True)
out={}
for i in (0,2):
    f,a = rows[i],rows[i+1]
    out[f['cell']]={'fence_types':f['types'],'abstract_types':a['types'],
        'abstract_fence_valid_subset':a['fence_valid_types'],
        'abstract_status':a['status'],'fence_status':f['status'],
        'fence_digests_subset_of_abstract': set(f['digests'])<=set(a['digests']),
        'abstract_fence_valid_equals_fence_set':
            {d for d in a['digests']}>=set(f['digests']),
        'abstract_adds_types_beyond_fence': len(set(a['digests'])-set(f['digests']))}
with open(os.path.join(ART,'output','item2_abstract_vs_fence_n23.json'),'w') as fh:
    json.dump(out,fh,indent=1,default=str)
print(json.dumps(out,indent=1,default=str))
