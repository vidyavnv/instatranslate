from config import block_blob_service
from constants import CONVERTED_VIDEOS_COLLECTION

def upload_to_bucket(output_file):
	block_blob_service.create_blob_from_stream(container, filename, file)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    blob_url = 'https://instatranslatefile.blob.core.windows.net/resources/'
    result = CONVERTED_VIDEOS_COLLECTION.update({'video_name': request.form['name']+'.mp4', 'video_url': blob_url+request.form['name']+'.mp4', 'video_desc': request.form['desc'], 'video_lang': request.form['lang']},
        {'video_name': request.form['name']+'.mp4', 'video_url': request.form['name']+'.mp4', 'video_desc': request.form['desc'], 'video_lang': request.form['lang']}, upsert=True)
	return link


def email_to_user(video_id, email_id, output_lang, url):
	pass