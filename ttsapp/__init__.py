from datetime import datetime, timezone
from os import path, getcwd
from time import mktime
from threading import Lock
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit


from speechapi import *

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret!"
app.config["DOWNLOAD_FOLDER"] = path.join(getcwd(), "instance/data")
socketio = SocketIO(app)

thread = None
thread_lock = Lock()

filedb = {}


def heartbeat_thread():
    count = 0
    while True:
        count += 1
        utc_datetime = datetime.now(timezone.utc)
        utc_datetime_for_js = int(mktime(utc_datetime.timetuple())) * 1000
        socketio.emit(
            "heartbeat",
            {"datetime": utc_datetime_for_js, "count": count},
            namespace="/global",
        )
        socketio.sleep(5)


def start_heartbeat_thread():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=heartbeat_thread)


@socketio.on("connect", namespace="/global")
def test_connect():
    print("Client connected")
    start_heartbeat_thread()
    emit("server_heartbeat", {"data": "Connected", "count": 0})


@socketio.on("disconnect", namespace="/global")
def test_disconnect():
    print("Client disconnected")


@socketio.on("update", namespace="/global")
def update(payload):
    print(payload)
    uuid = payload["uuid"]
    filename = payload["filename"]
    text = payload["text"]
    datetime = payload["datetime"]
    ssml = payload["ssml"]
    result = get_tts(filename="%s.wav" % uuid, text=text, ssml=ssml)
    status = result["status"]
    error = result ["error"]
    # path = result["path"]
    url = "/download/%s" % uuid
    # construct and store in memory
    data = {
        "filename": filename,
        "text": text,
        "datetime": datetime,
        "status": status,
        "url": url,
        "error": error
    }
    filedb[uuid] = data
    data["uuid"] = uuid

    emit("update", data)


@app.route("/")
def index():
    return render_template("index.j2")


@app.route("/download/<uuid>")
def download(uuid):
    filename = "%s.wav" % uuid
    attachment_filename = filedb[uuid]["filename"]
    print(uuid)
    print(app.config["DOWNLOAD_FOLDER"])
    print(filename)
    return send_from_directory(
        app.config["DOWNLOAD_FOLDER"],
        filename,
        as_attachment=True,
        attachment_filename=attachment_filename,
    )
