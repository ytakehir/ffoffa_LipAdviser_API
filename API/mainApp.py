from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import logging
import sys
sys.path.append('/home/c8473744/program/lipAdviser/')
from API import colorCodeSearchApp, tagSearchApp, imageSearchApp, rankingApp, testApp, webhookApp, dbLocalAccess
from API.authApp import Auth
from Utils import settings as set
from Utils import inputBean

app = Flask(__name__)
app.json.ensure_ascii = False
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:3000", "https://ffoffa.com"]}})
logging.basicConfig(level=logging.ERROR)

app.register_blueprint(testApp.app)
app.register_blueprint(colorCodeSearchApp.app)
app.register_blueprint(tagSearchApp.app)
app.register_blueprint(imageSearchApp.app)
app.register_blueprint(rankingApp.app)
app.register_blueprint(webhookApp.app)
app.register_blueprint(dbLocalAccess.app)

@app.before_request
def check_authentication():
  # /webhookへのアクセスはスルーする
  if request.path == '/webhook':
    return None

  if not (request.headers.get('accessId') and request.headers.get('accessKey')):
    return jsonify({"errorId": set.MESID_AUTH_ERROR, "errorMessage":["API認証"]}), 403

  auth = inputBean.AuthInput(
    accessId=request.headers.get('accessId'),
    accessKey=request.headers.get('accessKey')
  )
  if not Auth.authLogin(auth):
    return jsonify({"errorId": set.MESID_AUTH_ERROR, "errorMessage":["API認証"]}), 403

@app.route('/<path:path>', methods=['OPTIONS'])
def handle_options(path):
  origin = request.headers.get('Origin')
  if origin in ['http://localhost:3000/', 'http://localhost:4173/', 'https://ffoffa.com/']:
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, accessId, accessKey')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response, 200
  return jsonify({"error": "Origin not allowed"}), 403

@app.after_request
def after_request(response):
  origin = request.headers.get('Origin')
  if origin in ['http://localhost:3000/', 'http://localhost:4173/', 'https://ffoffa.com/']:
    response.headers.add('Access-Control-Allow-Origin', origin)
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, accessId, accessKey')
  response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
  return response

if __name__ == '__main__':
  app.run(debug=True)
