import os
from flask import Flask, abort, render_template, redirect, request, send_file, url_for
from peewee import *
from . import speech_api
from . import inventory
from . import db

db.database.create_tables([db.Call])

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret!"
app.config["DOWNLOAD_FOLDER"] = os.path.join(os.getcwd(), "instance/data")

@app.before_request
def before_request():
    db.database.connect()

@app.after_request
def after_request(response):
    db.database.close()
    return response

@app.route('/', defaults={'req_path': ''})
@app.route("/<path:req_path>")
def explore(req_path):
    # Joining the base and the requested path
    abs_path = os.path.join(app.config["DOWNLOAD_FOLDER"], req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = os.listdir(abs_path)

    # Determine if we are on a directory leaf
    if len(files) > 0 and os.path.isfile(os.path.join(abs_path, files[0])):
        leaf = True
        speech_api.get_stt(os.path.join(abs_path, files[0]))

    else:
        leaf = False

    return render_template('index.j2', files=files, leaf=leaf)

@app.route("/inventory")
def run_inventory():
    print(inventory.run_inventory(app.config["DOWNLOAD_FOLDER"]))
    return redirect(url_for("explore"))



