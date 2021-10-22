import os
from flask import Flask, abort, render_template, request, send_file

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret!"
app.config["DOWNLOAD_FOLDER"] = os.path.join(os.getcwd(), "instance/data")

@app.route('/', defaults={'req_path': ''})
@app.route("/<path:req_path>")
def index(req_path):
    BASE_DIR = app.config["DOWNLOAD_FOLDER"]

    print(request.path)
    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

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
    else:
        leaf = False
    print(len(files))
    print(abs_path)
    print(os.path.isfile(abs_path))
    print(os.path.isfile(files[0]))
    print(leaf)

    return render_template('index.j2', files=files, leaf=leaf)



