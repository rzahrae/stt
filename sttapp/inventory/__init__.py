from pathlib import Path
from .. import db

def run_inventory(basepath):
	print("Inventorying base path: " + basepath)
	for path in Path(basepath).rglob('*.wav'):
	    path = path.relative_to(basepath)
	    db.Call(path=path).save()