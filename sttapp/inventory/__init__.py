from pathlib import Path
from .. import db
from .. import speech_api


def run_inventory(basepath):
    print("Inventorying base path: " + basepath)
    for abs_path in Path(basepath).rglob("*.wav"):
        rel_path = abs_path.relative_to(basepath)
        # Check if our path has already been inventoried
        query = db.Call.select().where(db.Call.path == rel_path)
        if not query.exists():
            # Path has not been inventoried, call API
            result = speech_api.get_stt(str(abs_path))
            print(result)
            db.Call(path=rel_path, text=text).save()
            pass
