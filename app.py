import os
import json

from flask import Flask, request, redirect, url_for, render_template
from flask.ext.cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from azure.storage.file import ContentSettings
from bson import json_util

from config import block_blob_service, VIDEOS_COLLECTION
from constants import CONTAINER, VIDEO_DIR

from upload import upload_to_indexer

UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + '/resources/videos/uploadedVideos/'
ALLOWED_EXTENSIONS = set(['mp4'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#cors = CORS(app, resources={r"/uploadFile": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


app.config.from_pyfile('constants.py')
container = app.config['CONTAINER'] # Container name



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/uploadFile', methods=['POST','OPTIONS'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)

        # generator = file_service.list_directories_and_files(ROOT_DIR)
        # for file_or_dir in generator:
        #     print(file_or_dir.name)
        print(file.filename)
        if file and allowed_file(file.filename):
            print("Inside IF")
            filename = secure_filename(file.filename)
            block_blob_service.create_blob_from_stream(container, filename, file)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            blob_url = 'https://instatranslatefile.blob.core.windows.net/resources/'
            result = VIDEOS_COLLECTION.update({'video_name': file.filename, 'video_url': blob_url+file.filename, 'video_desc': "Test Video", 'video_lang': "English"},
                {'video_name': file.filename, 'video_url': file.filename, 'video_desc': "Test Video", 'video_lang': "English"}, upsert=True)
            upload_to_indexer(filename)
            return "Sucess"
    return "Upload Fail"


@app.route('/getVideos', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_videos():
    videos_cursor = VIDEOS_COLLECTION.find({})
    videos = [video for video in videos_cursor]
    return json_util.dumps(videos)



@app.route('/gettranslationreq', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_translation_req():
    generator = block_blob_service.list_blobs(CONTAINER)
    result = [blob.name for blob in generator]
    return result


if __name__ == '__main__':
    app.run(debug=True)
