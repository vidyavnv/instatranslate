import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import json

from config import block_blob_service, CONVERTED_VIDEOS_COLLECTION, CONTAINER


def upload_to_bucket(output_file, output_lang):
	file = open(output_file, 'rb')
	block_blob_service.create_blob_from_stream(CONTAINER, output_file, file)
	blob_url = 'https://instatranslatefile.blob.core.windows.net/resources/'
	result = CONVERTED_VIDEOS_COLLECTION.insert({'video_name': output_file, 'video_url': blob_url+output_file, 'video_lang': output_lang})
	return blob_url+output_file


def email_to_user(video_id, email_id, output_lang, url):
	import http.client
	conn = http.client.HTTPSConnection("api.sendgrid.com")
	text = "<html><p>{}</p></html>".format(url)
	payload = {"personalizations":[{"to":[{"email":email_id,"name":"John Doe"}],"subject":"Your video is ready!"}],"from":{"email":"anuraag.advani@gmail.com","name":"Sam Smith"},"reply_to":{"email":"anuraag.advani@gmail.com","name":"Sam Smith"},"subject":"Your Video is ready!","content":[{"type":"text/html","value":text}]}
	payload = json.dumps(payload)
	print(payload)
	headers = {
	 'authorization': "Bearer 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",
	 'content-type': "application/json"
	 }
	conn.request("POST", "/v3/mail/send", payload, headers)
	res = conn.getresponse()
	data = res.read()
	print(data.decode("utf-8"))
