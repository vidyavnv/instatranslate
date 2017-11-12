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
from threading import Thread

from translate import get_transcript, tts, merge 
from utils import upload_to_bucket, email_to_user

from video_insights import get_video_insights

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

            result = VIDEOS_COLLECTION.update({'video_name': request.form['name']+'.mp4', 'video_url': blob_url+request.form['name']+'.mp4', 'video_desc': request.form['desc'], 'video_lang': request.form['lang']},
                {'video_name': request.form['name']+'.mp4', 'video_url': blob_url+request.form['name']+'.mp4', 'video_desc': request.form['desc'], 'video_lang': request.form['lang']}, upsert=True)
            upload_to_indexer(filename)
            return "Sucess"
    return "Upload Fail"


@app.route('/getVideos', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_videos():
    videos_cursor = VIDEOS_COLLECTION.find({})
    videos = [video for video in videos_cursor]
    return json_util.dumps(videos)


def run_translation(video_id, email_id, output_lang):
    video = VIDEOS_COLLECTION.find({"insight_id": video_id}, {"video_lang": 1, "_id": 0})
    input_lang = [v.video_lang for v in video][0]
    get_transcript.download_transcript(video_id, input_lang)
    tts.tts(video_id, input_lang, output_lang)
    output_file = merge.merge(video_id, output_lang)
    link_to_video = upload_to_bucket(output_file, output_lang)
    email_to_user(video_id, email_id, output_lang, link_to_video)



@app.route('/gettranslationreq', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_translation_req():
    if request.method == 'POST':
        video_id = request.form['video_id']
        email_id = request.form['email']
        lang = request.form['lang']
        is_success = False
        Thread(target = run_translation(video_id, email_id, lang)).start()
        # check_query = REQUEST_COLLECTION.find_one(
        #     {'video_id': video_id, 'email_id': email_id, 'language': lang})
        # if not check_query:
        #     REQUEST_COLLECTION.insert_one(
        #         {'video_id': video_id, 'email_id': email_id, 'language': lang, 'is_success': is_success}, 
        #     )


        return 'SUCCESS'


@app.route('/addVideoDetailsToDB', methods=['POST'])
def add_details():
    print(request)

    video_id_insight = request.args.get("id")

    insight_data = get_video_insights(video_id_insight)
    insight_data = json.loads(insight_data.decode('utf-8'))
    summary = insight_data["summarizedInsights"]
    # print(insight_data["breakdowns"][0])
    # print(summary)
    # print("here")
    result = VIDEOS_COLLECTION.update({'video_name': insight_data["breakdowns"][0]["externalId"]},
            { "$set":
                {
                    "faces": summary["faces"]
                    }
                })
    # print("here2")
    result = VIDEOS_COLLECTION.update({'video_name': insight_data["breakdowns"][0]["externalId"]},
            { "$set":
                {
                    "insight_id": video_id_insight,
                    "events": summary["annotations"]
                    }
                })
    # print("here3")

    result = VIDEOS_COLLECTION.update({'video_name': insight_data["breakdowns"][0]["externalId"]},
            { "$set":
                {
                    "topics": summary["topics"]
                    }
                })

    # print("here4")


    return "success"

if __name__ == '__main__':
    app.run(debug=True)
