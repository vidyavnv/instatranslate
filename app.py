import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from azure.storage.file import ContentSettings

from config import block_blob_service, VIDEOS_COLLECTION
from constants import CONTAINER, VIDEO_DIR


UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/resources/videos/uploadedVideos/'
ALLOWED_EXTENSIONS = set(['mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_pyfile('constants.py')
container = app.config['CONTAINER'] # Container name



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    return '''
    <!doctype html>
    <title>Upload Video</title>
    <h1>Upload Video</h1>
    <form method=post enctype=multipart/form-data action=/uploadFile>
      <p><input type=file name=file>
         Name: <input type=text name=name>
         Description: <input type=text name=desc>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # generator = file_service.list_directories_and_files(ROOT_DIR)
        # for file_or_dir in generator:
        #     print(file_or_dir.name)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            block_blob_service.create_blob_from_stream(container, filename, file)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            result = VIDEOS_COLLECTION.insert_one({'video_name': filename, 'video_url': filename, 'video_desc': request.form['desc']})
            return redirect(url_for('index'))
    return "Upload Fail"


if __name__ == '__main__':
    app.run(debug=True)