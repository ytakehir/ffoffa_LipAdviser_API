from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import logging
from . import colorCodeSearchApp, tagSearchApp, imageSearchApp, rankingApp, testApp, webhookApp
from .authApp import Auth
from Utils import settings as set
from Utils import inputBean

app = Flask(__name__)
CORS(app, origins=[set.ALLOWED_ORIGINS], methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type", "Authorization", "accessId", "accessKey"], supports_credentials=True)
app.json.ensure_ascii = False
logging.basicConfig(level=logging.DEBUG)

app.register_blueprint(testApp.app)
app.register_blueprint(colorCodeSearchApp.app)
app.register_blueprint(tagSearchApp.app)
app.register_blueprint(imageSearchApp.app)
app.register_blueprint(rankingApp.app)
app.register_blueprint(webhookApp.app)

@app.before_request
def handle_options_request():
  # /webhookへのアクセスはスルーする
  if request.method == "OPTIONS" or request.path == '/webhook' or request.path == '/test':
    return None

  if not (request.headers.get('accessId') and request.headers.get('accessKey')):
    return jsonify({"errorId": set.MESID_AUTH_ERROR, "errorMessage":["API認証1"]}), 403

  auth = inputBean.AuthInput(
    accessId=request.headers.get('accessId'),
    accessKey=request.headers.get('accessKey')
  )

  if not Auth.authLogin(auth):
    return jsonify({"errorId": set.MESID_AUTH_ERROR, "errorMessage":["API認証2"]}), 403

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
