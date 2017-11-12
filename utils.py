import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import block_blob_service
from constants import CONVERTED_VIDEOS_COLLECTION, CONTAINER

def upload_to_bucket(output_file, output_lang):
	file = open(filename, 'r')
	block_blob_service.create_blob_from_stream(CONTAINER, output_file, file)
	blob_url = 'https://instatranslatefile.blob.core.windows.net/resources/'
    result = CONVERTED_VIDEOS_COLLECTION.insert({'video_name': output_file, 'video_url': blob_url+output_file, 'video_lang': output_lang})
	return blob_url+output_file


def email_to_user(video_id, email_id, output_lang, url):
	sender = "vidya.vnv@gmail.com"
	recipient = email_id

	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Link To Video"
	msg['From'] = sender
	msg['To'] = recipient

	# Create the body of the message (a plain-text and an HTML version).
	text = "Hi!\nHow are you?\nHere is the link you wanted:\n {} in {} language".format(url, output_lang)
	html = """\
	<html>
	  <head></head>
	  <body>
	    <p>Hi!<br>
	       How are you?<br>
	       Here is the <a href={}>link</a> you wanted.
	    </p>
	  </body>
	</html>
	"""
	html = html.format(url)

	# Record the MIME types of both parts - text/plain and text/html.
	part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')

	# Attach parts into message container.
	# According to RFC 2046, the last part of a multipart message, in this case
	# the HTML message, is best and preferred.
	msg.attach(part1)
	msg.attach(part2)

	# Send the message via local SMTP server.
	s = smtplib.SMTP('localhost')
	# sendmail function takes 3 arguments: sender's address, recipient's address
	# and message to send - here it is sent as one string.
	s.sendmail(sender, recipient, msg.as_string())
	s.quit()