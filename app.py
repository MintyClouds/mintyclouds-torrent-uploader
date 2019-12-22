import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from settings_local import UPLOAD_PATH
from templates.upload import upload_template

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'torrent'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['GET', 'POST'])
def upload_torrent():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_torrent',
                                    filename=filename))
    return upload_template


if __name__ == '__main__':
    app.run()
