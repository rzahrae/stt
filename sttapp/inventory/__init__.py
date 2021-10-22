from pathlib import Path

def inventory(basepath):
	paths = []
	print("inventorying base path:" + basepath)
	for path in Path(basepath).rglob('*.wav'):
	    print(path)
	    paths.append(path)
	return paths