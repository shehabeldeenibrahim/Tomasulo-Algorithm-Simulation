from flask import Flask, request, redirect, url_for, flash,render_template, send_from_directory
from json import dump
import numpy
import os
import sys
import io
import json_tricks
import requests
from werkzeug.utils import secure_filename
from main import *


UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/index",methods=['GET','POST'])
def upload_file():
   
    if request.method == 'POST':
        #return "posted"

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files["file"]
        starting_point = request.form['text']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save("test.txt") 
            result = main_fun(starting_point)
            return result
    else:
        return "nothing"
if __name__ == '__main__':
    app.run(debug=True)