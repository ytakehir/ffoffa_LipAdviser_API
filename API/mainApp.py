from flask import Flask
import sys
sys.path.append('C:/Users/takeg/work/ffoffa_LipAdviser_API/')
# sys.path.append('/home/c1343520/program/lipAdviser/')
from API import colorCodeSearchApp, testApp, dbLocalAccess

# APIを読み込み
app = Flask(__name__)
app.register_blueprint(testApp.app)
app.register_blueprint(colorCodeSearchApp.app)
app.register_blueprint(dbLocalAccess.app)

if __name__ == '__main__':
    app.run(debug=True)