
from flask import Flask

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import os

gmail_user = "architechsdoom@gmail.com"
gmail_pwd = raw_input('pwd > ')


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return 'hello world!'

@app.route('/send/<string:to>')
def send(to):
	mail(to,
	   "Welcome to the team!",
"""
You have successfully joined the sailing team.

Your membership code is attached.
Save it to your device, and show it at events.
""",
	   "./code.png")

	return "Sent."

def mail(to, subject, text, attach):
   msg = MIMEMultipart()

   msg['From'] = gmail_user
   msg['To'] = to
   msg['Subject'] = subject

   msg.attach(MIMEText(text))

   part = MIMEBase('application', 'octet-stream')
   part.set_payload(open(attach, 'rb').read())
   encoders.encode_base64(part)
   part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attach))
   msg.attach(part)

   mailServer = smtplib.SMTP("smtp.gmail.com", 587)
   mailServer.ehlo()
   mailServer.starttls()
   mailServer.ehlo()
   mailServer.login(gmail_user, gmail_pwd)
   mailServer.sendmail(gmail_user, to, msg.as_string())
   # Should be mailServer.quit(), but that crashes...
   mailServer.close()


if __name__ == '__main__':
	app.run()