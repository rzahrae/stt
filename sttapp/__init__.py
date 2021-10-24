import os
from pathlib import Path
import datetime
from flask import Flask, abort, render_template, redirect, request, send_file, url_for
from peewee import *
from . import speech_api
from . import inventory
from . import db

db.database.create_tables([db.Call])

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret!"
app.config["DOWNLOAD_FOLDER"] = os.path.join(os.getcwd(), "instance/data")

@app.template_filter('parent')
def parent(path):
    path = Path(path)
    return path.parent

@app.template_filter('time_fmt')
def time_fmt(seconds):
    return str(datetime.timedelta(seconds = int(seconds)))

@app.before_request
def before_request():
    db.database.connect()


@app.after_request
def after_request(response):
    db.database.close()
    return response


@app.route("/", defaults={"req_path": ""})
@app.route("/<path:req_path>")
def explore(req_path):
    # Joining the base and the requested path
    abs_path = Path(app.config["DOWNLOAD_FOLDER"]).joinpath(req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if abs_path.is_file():
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)
    metadata = None
    # Determine if we are on a directory leaf
    if len(files) > 0 and abs_path.joinpath(files[0]).is_file():
        leaf = True
        rel_path = abs_path.relative_to(app.config["DOWNLOAD_FOLDER"])
        # Compose a dict where relative path is the key
        metadata = {}
        for file in files:
            path = str(rel_path) + "/" + file
            file_metadata = db.Call.select().where(db.Call.path == path)
            if file_metadata:
                file_metadata = file_metadata.get()
                data = {
                    "incoming": file_metadata.incoming,
                    "receiving": file_metadata.receiving,
                    "initiating": file_metadata.initiating,
                    "text": file_metadata.text,
                    "date_time": file_metadata.date_time,
                    "duration": file_metadata.duration,
                }
                metadata[path] = data
            else:
                metadata[path] = None
    else:
        leaf = False

    return render_template("explore.j2", files=files, metadata=metadata, leaf=leaf)


@app.route("/inventory")
def run_inventory():
    inventory.run_inventory(app.config["DOWNLOAD_FOLDER"])
    return redirect(url_for("explore"))
