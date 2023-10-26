# middleman for miles-lite-client::aws-server

from flask import (
  Flask, 
  request, 
  jsonify, 
  render_template
)

from flask_cors import CORS
from waitress import serve
import requests
import json

# Flask app
app = Flask(__name__)
CORS(app)

# Address of your main server
address = "http://localhost:1234"

# get reply from aws-server
def get_reply(data):
  url = address + "/get_reply"
  headers = {"Content-Type": "application/json"}
  response = requests.post(url, headers=headers, data=json.dumps(data))
  result = response.json()
  return result['reply']

# refresh app
def refresh(data):
  url = address + "/refresh"
  headers = {"Content-Type": "application/json"}
  response = requests.post(url, headers=headers, data=json.dumps(data))
  result = response.json()
  return result

# index
@app.route('/')
def index():
  return jsonify({'status': 'online'}), 200

# generate reply
@app.route('/get_reply', methods=['POST'])
def receive_message():
  try:
    data = request.get_json()
    print('[+] tagged')
    reply = get_reply(data)
    print('[=] reply_len:', len(reply))
    return jsonify({'reply': reply}), 200
  except:
    return jsonify({'reply': "[SERVER SIDE ERROR] Sorry for the inconvenience"})

# collect user's data
@app.route('/refresh', methods=['POST'])
def refresh_data():
  data = request.get_json()
  status = refresh(data)
  return jsonify(status), 200

# for keeping the server alive
@app.route('/keep_alive')
def alive():
  print("[ ] pinged by uptime-robot")
  return jsonify({'status': 'online'}), 200

# start server
if __name__ == '__main__':
  print("[server going online]")
  serve(
    app=app, 
    host="0.0.0.0", 
    port=80
  )
