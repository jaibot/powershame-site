from flask import render_template
from app import app
import requests
from werkzeug.datastructures import MultiDict


@app.route('/send_message.html')
def mail_test():
   a = requests.post(
        "https://api.mailgun.net/v2/powershame.mailgun.org/messages",
        auth=("api", 'key-231mtboe2i9bwkxgw5pses5u-rw6u-j4' ),
        data={"from": 'jai@powershame.mailgun.org',
              "to": 'jai@jaibot.com',
              "subject": "Powershame ON THE INTERNET",
              "text": "hey you" }
   )
   return str(a)
