# views.py

import os
from flask import render_template
from flask import send_from_directory

from labeling_app.app import app
from labeling_app import config

@app.route('/')
def index():
    print("app.root_path", app.root_path)
    file_path = "live_user_liliasplays-0x7201507137414.jpg"
    # print(file_path)
    # file_path = os.path.join(config.MEDIA_FOLDER, "live_user_liliasplays-0x7201507137414.jpg")
    # print(file_path + " bla\n")
    return render_template("index.html", file_path=file_path)

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/upload/<filename>')
def send_unlabeled_image(filename):
    print(config.UNLABELED_IMAGES_FOLDER, filename, "?????")
    return send_from_directory(config.UNLABELED_IMAGES_FOLDER, filename)
