from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import sys
sys.path.append('/home/c8473744/program/lipAdviser/')
from API import colorCodeSearchApp, tagSearchApp, imageSearchApp, rankingApp, testApp, webhookApp
from API.authApp import Auth
from Utils import settings as set
from Utils import inputBean

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app, origins=["http://localhost:3000/", "https://ffoffa.com/"], supports_credentials=True)
logging.basicConfig(level=logging.ERROR)

CORS(testApp.app, supports_credentials=True)
CORS(colorCodeSearchApp.app, supports_credentials=True)
CORS(tagSearchApp.app, supports_credentials=True)
CORS(imageSearchApp.app, supports_credentials=True)
CORS(rankingApp.app, supports_credentials=True)
CORS(webhookApp.app, supports_credentials=True)

app.register_blueprint(testApp.app)
app.register_blueprint(colorCodeSearchApp.app)
app.register_blueprint(tagSearchApp.app)
app.register_blueprint(imageSearchApp.app)
app.register_blueprint(rankingApp.app)
app.register_blueprint(webhookApp.app)

def build_cors_preflight_response():
    response = jsonify({"status": "CORS Preflight OK"})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, accessId, accessKey")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response

@app.before_request
def handle_options_request():
  if request.method == "OPTIONS":
    return build_cors_preflight_response()

  # /webhookへのアクセスはスルーする
  if request.method == "OPTIONS" and request.path == '/webhook':
    return None

  if not (request.headers.get('accessId') and request.headers.get('accessKey')):
    return jsonify({"errorId": set.MESID_AUTH_ERROR, "errorMessage":["API認証"]}), 403

  auth = inputBean.AuthInput(
    accessId=request.headers.get('accessId'),
    accessKey=request.headers.get('accessKey')
  )
  if not Auth.authLogin(auth):
    return jsonify({"errorId": set.MESID_AUTH_ERROR, "errorMessage":["API認証"]}), 403

if __name__ == '__main__':
  app.run(debug=True)
