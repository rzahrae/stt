from pathlib import Path
from datetime import datetime
import re
import librosa
from .. import db
from .. import speech_api


def run_inventory(basepath):
    print("Inventorying base path: " + basepath)
    for abs_path in Path(basepath).rglob("*.wav"):
        rel_path = abs_path.relative_to(basepath)
        # Check if our path has already been inventoried
        print("checking " + str(rel_path))

        query = db.Call.select().where(db.Call.path == str(rel_path))

        if not query.exists():
            filename = rel_path.name

            if re.search("^external.*$", filename):
                incoming = True
            else:
                incoming = False

            str_date = re.search("^.*-([0-9].*)-(.*)-.*([0-9]{8})-([0-9]{6})-.*$", filename)

            date_time = datetime.strptime(str_date.group(3) + str_date.group(4), '%Y%m%d%H%M%S')

            receiving = str_date.group(1)

            initiating = str_date.group(2)

            # Path has not been inventoried, call API
            text = speech_api.get_stt(str(abs_path))
            duration = librosa.get_duration(filename=abs_path)
            db.Call(path=rel_path, text=text, duration=duration, date_time=date_time, number1=recieving, number2=initiating, incoming=incoming ).save()

