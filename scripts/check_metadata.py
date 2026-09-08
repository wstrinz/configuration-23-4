"""Validate the pinned v0.4 schema and this release's editorial/mechanical metadata."""
from pathlib import Path
import hashlib, json, re
import yaml
from jsonschema import Draft7Validator

root=Path(__file__).resolve().parent.parent
data=yaml.safe_load((root/'formalization.yaml').read_text(encoding='utf-8'))
schema=json.loads((root/'schema/v0.4.schema.json').read_text())
Draft7Validator(schema).validate(data)
assert data['version']=='v0.4'
assert data['project']['license']=='MIT'
assert data['project']['authors']==['Will Strinz']
assert data['project']['responsible_maintainers']==['Will Strinz']
license_text=(root/'LICENSE').read_text()
assert hashlib.sha256(license_text.encode()).hexdigest()=='dbd82e1cbdaea50b491764f30161abf4eea4a9eb4333216ce73344ed7d7308b0'
assert 'MIT License' in license_text and 'Copyright (c) 2026 Will Strinz' in license_text
assert 'Permission is hereby granted, free of charge' in license_text
assert 'THE SOFTWARE IS PROVIDED "AS IS"' in license_text
assert 'TEMPLATE' not in (root/'formalization.yaml').read_text()
assert data['status']['sorry_count']==0 and data['status']['sorry_in_definitions']==0
assert data['repository']['role']=='substantive-development'
sources=data['sources']
assert sum(s.get('type')=='original-proof' for s in sources)==1
assert all(s['relationship'] in ('background','other') for s in sources)
cfg=json.loads((root/'comparator.json').read_text())
assert cfg['theorem_names']==['Config23.exists_configuration']
assert set(cfg['permitted_axioms'])=={'propext','Quot.sound','Classical.choice'}
solution=(root/'Solution.lean').read_text(encoding='utf-8')
assert not re.search(r'\b(sorry|axiom|native_decide|sorryAx)\b',solution)
challenge=(root/'Challenge.lean').read_text(encoding='utf-8')
assert len(challenge.splitlines()) <= 300 and len(challenge.encode()) <= 32768
for pkg in json.loads((root/'lake-manifest.json').read_text())['packages']:
 assert pkg['type']=='git' and re.fullmatch('[0-9a-f]{40}',pkg['rev'])
 assert re.fullmatch(r'https://github.com/[\w.-]+/[\w.-]+(?:\.git)?',pkg['url'])
for lean in root.glob('*.lean'):
 for imp in re.findall(r'^import (.+)$',lean.read_text(encoding='utf-8'),re.M):
  assert imp.startswith('Mathlib.'),imp
print('Metadata schema, license declaration, proof surface and dependency pins: PASS')

# Cross-check the two citation formats: Zenodo gives its JSON file precedence.
citation=yaml.safe_load((root/'CITATION.cff').read_text(encoding='utf-8'))
zenodo=json.loads((root/'.zenodo.json').read_text(encoding='utf-8'))
assert citation['cff-version']=='1.2.0'
assert citation['type']==zenodo['upload_type']=='software'
assert citation['title']==zenodo['title']=='A real affine (23_4) configuration'
assert citation['license']==zenodo['license']=='MIT'
assert citation['authors']==[{'family-names':'Strinz','given-names':'Will'}]
assert zenodo['creators']==[{'name':'Strinz, Will'}]
assert citation['keywords']==zenodo['keywords']
assert citation.get('version')==zenodo.get('version')
assert citation.get('date-released')==zenodo.get('publication_date')
assert 'doi' not in zenodo, 'Let the integration allocate each release DOI'
assert zenodo['access_right']=='open'
print('Citation and Zenodo metadata consistency: PASS (not a live deposit validation)')
