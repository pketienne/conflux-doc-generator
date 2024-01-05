import json, sys
from pathlib import Path


current_module = module = sys.modules[__name__]
p = Path('json')

def read_json(file):
	with open(f"json/{file}") as f:
		return json.loads(f.read(), strict=False)

for p in list(p.glob('**/*.json')):
	setattr(current_module, p.stem, read_json(p.name))
