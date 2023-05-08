from flask import render_template, request, redirect, url_for
from . import app
import pathlib
from src.repository import detection


@app.route('/healthcheck', strict_slashes=False)
def healthcheck():
    return 'I am working'


@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        img_file = request.files['image']
        file_path = pathlib.Path(app.config['UPLOAD_FOLDER']) / img_file.filename
        if not detection.allowed_file(img_file.filename):
            return redirect(request.url)
        img_file.save(file_path)
        img_class = detection.predict_image(file_path)
        print(file_path)
        file_path = 'uploads/' + img_file.filename
        print(file_path)

        return render_template('index.html', img_class=img_class,
                               image_url=url_for('static', filename='uploads/' + img_file.filename, _external=True,
                                                 url_prefix=''))
    return render_template('index.html')
