from pathlib import Path

def run_inventory(basepath):
	paths = []
	print("inventorying base path:" + basepath)
	for path in Path(basepath).rglob('*.wav'):
	    path = path.relative_to(basepath)
	    paths.append(path)
	return paths