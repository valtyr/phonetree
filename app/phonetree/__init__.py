from flask import Flask, request, send_from_directory, redirect
from flask_sqlalchemy import SQLAlchemy

from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///calls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


from phonetree.models import Recording
from sqlalchemy.sql.expression import func


def path_for_recording(rec):
    root = request.host_url
    return '{}recordings/{}.wav'.format(root, rec)


@app.route('/', methods=['GET', 'POST'])
def intro():
    resp = VoiceResponse()
    with resp.gather(num_digits=1, action="/handle-key", method="POST") as g:
        g.play(path_for_recording('greeting'))
    return str(resp)


@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
    """Handle key press from a user."""

    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "1":
        print('{}, record'.format(request.values.get("From", None)))
        resp = VoiceResponse()
        resp.play(path_for_recording('leave_message'))
        resp.record(timeout=5, trim='trim-silence', action="/handle-recording")

        return str(resp)

    elif digit_pressed == "2":
        print('{}, listen'.format(request.values.get("From", None)))
        resp = VoiceResponse()
        resp.play(path_for_recording('listen'))

        rand_message = Recording.query.order_by(func.random()).first()
        resp.play(rand_message.url)

        resp.play(path_for_recording('bye'))
        return str(resp)

    else:
        return redirect("/")


@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    recording = Recording()
    recording.url = request.values.get("RecordingUrl", None)
    recording.caller = request.values.get("From", None)
    db.session.add(recording)
    db.session.commit()

    resp = VoiceResponse()
    resp.play(path_for_recording('bye'))
    return str(resp)


@app.route('/recordings/<path:path>')
def send_js(path):
    return send_from_directory('recordings', path)
