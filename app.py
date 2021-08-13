import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'torrent'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/data'
app.secret_key = os.getenv('SECRET_KEY')    # for session


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_torrent():
    upload_template = 'index.html'
    error = None

    if request.method == 'POST':
        files = request.files.getlist('file')

        if 'clear' in request.form:
            return render_template(upload_template)

        if len(files) > 0:
            for file in files:
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                elif file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    flash(str('Uploaded file: {fn}'.format(fn=filename)))
                else:
                    flash('Unsupported file extension in file: {fn}'.format(fn=file.filename))
            return redirect(url_for('upload_torrent'))
        else:
            flash('No files selected')
            return redirect(request.url)

    return render_template(upload_template, error=error)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
