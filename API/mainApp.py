from flask import Flask
from flask_cors import CORS
import sys
sys.path.append('C:/Users/takeg/work/ffoffa_LipAdviser_API/')
# sys.path.append('/home/c1343520/program/lipAdviser/')
from API import colorCodeSearchApp, testApp, dbLocalAccess

# APIを読み込み
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(testApp.app)
app.register_blueprint(colorCodeSearchApp.app)
app.register_blueprint(dbLocalAccess.app)

@app.after_request
def after_request(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True)