from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
sys.path.append('/home/c8473744/program/lipAdviser/')
from API import colorCodeSearchApp, tagSearchApp, imageSearchApp, rankingApp, testApp, dbLocalAccess
from API.authApp import Auth
from Utils import settings as set
from Utils import inputBean, responseBean

# APIを読み込み
app = Flask(__name__)
CORS(app, supports_credentials=True)  # CORS設定

app.register_blueprint(testApp.app)
app.register_blueprint(colorCodeSearchApp.app)
app.register_blueprint(tagSearchApp.app)
app.register_blueprint(imageSearchApp.app)
app.register_blueprint(rankingApp.app)
app.register_blueprint(dbLocalAccess.app)

@app.before_request
def check_authentication():
    if not (request.headers.get('accessId') and request.headers.get('accessKey')):
        return jsonify({"errorId": set.MESID_AUTH_ERROR, "errorMessage":["API認証"]}), 403

    auth = inputBean.AuthInput(
        accessId=request.headers.get('accessId'),
        accessKey=request.headers.get('accessKey')
    )
    if not Auth.authLogin(auth):
        return jsonify({"errorId": set.MESID_AUTH_ERROR, "errorMessage":["API認証"]}), 403

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin in set.ALLOWED_ORIGINS:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,accessId,accessKey')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True)
