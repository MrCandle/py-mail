from flask import Flask, request
from flask_cors import cross_origin
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import configparser

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('./config.ini')

@app.route("/", methods=['POST'])
@cross_origin()
def sendEmail():

    # We read smtp config from config.ini
    smtp_host = config['smtp']['smtp_host']
    smtp_port = config['smtp']['smtp_port']
    smtp_username = config['smtp']['smtp_username']
    smtp_password = config['smtp']['smtp_password']
    smtp_from = config['smtp']['smtp_from']
    smtp_to = config['smtp']['smtp_to']

    # request will contain some form
    form = request.get_json()
    
    body = 'Hello World!'

    msg = MIMEMultipart()
    msg['From'] = smtp_from
    msg['To'] = smtp_to
    msg['Subject'] = 'Test email'

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(smtp_host, smtp_port)
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.login(smtp_username, smtp_password)

    server.sendmail(smtp_from, smtp_to, msg.as_string())
    server.quit()
    return 'Hello, World! from POST'


if __name__ == "__main__":
    app.run()
