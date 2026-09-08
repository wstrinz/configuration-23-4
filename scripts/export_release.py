"""Produce a deterministic, self-contained source archive, or verify its manifest."""
from pathlib import Path
import argparse, hashlib, json, os, zipfile

root=Path(__file__).resolve().parent.parent
ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
directories={'.github','scripts','schema','third_party','standalone','verification','assets','evidence','docs'}
files=[]
paths=[]
for parent, dirs, names in os.walk(root, followlinks=False):
 dirs[:]=[d for d in dirs if d not in {'.git','.lake','.cache','__pycache__'} and not d.startswith('negative-') and (Path(parent)!=root or d in directories)]
 for d in dirs: assert not (Path(parent)/d).is_symlink(),d
 paths.extend(Path(parent)/n for n in names)
for p in sorted(paths):
 rel=p.relative_to(root)
 if p.is_dir(): continue
 if len(rel.parts)>1 and rel.parts[0] not in directories: continue
 if p.name in {'manifest.json','release.zip'}: continue
 if len(rel.parts)==1 and p.suffix not in {'.lean','.md','.json','.yaml','.toml','.txt','.svg','.cff'} and p.name not in {'LICENSE','lean-toolchain','.gitignore','.gitattributes'}: continue
 assert not p.is_symlink(),str(rel)
 assert p.stat().st_size < 5*1024*1024,str(rel)
 assert p.suffix not in {'.olean','.ilean','.o','.so','.exe'},str(rel)
 files.append(p)
manifest={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
target=root/'manifest.json'
if a.check:
 assert json.loads(target.read_text())==manifest,'Release file list or hashes changed'
 print('Release manifest: PASS')
else:
 target.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8',newline='\n')
 with zipfile.ZipFile(root/'release.zip','w',zipfile.ZIP_DEFLATED) as z:
  for p in files+[target]:
   info=zipfile.ZipInfo(p.relative_to(root).as_posix(),(2026,9,8,0,0,0))
   info.create_system=3
   info.external_attr=(0o100755 if p.suffix=='.sh' else 0o100644)<<16
   info.compress_type=zipfile.ZIP_DEFLATED
   z.writestr(info,p.read_bytes())
 print('Packaged',len(files)+1,'files;', (root/'release.zip').stat().st_size,'bytes')
