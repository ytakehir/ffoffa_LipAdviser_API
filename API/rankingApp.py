from flask import Blueprint, jsonify
from pydantic import ValidationError
from flask_pydantic import validate
from flask import current_app
from flask_cors import cross_origin
import sys
sys.path.append('/home/c8473744/program/lipAdviser/')
from DB.dataBase import Dao
from Utils import inputBean, responseBean
from Utils import settings as set

app = Blueprint('ranking', __name__)

class Ranking:
    @app.route("/post/lipHistory",  methods=["POST"])
    @cross_origin(supports_credentials=True)
    @validate()
    def getBrandLogoImage(body: inputBean.LipHistoryInput):
        """LIP検索履歴登録API

        検索回数と履歴を登録する

        Returns:
            json: 実行可否
        """

        try:
            dao = Dao()
            result = dao.LipHistoryInsert(body.lipId)
            response = responseBean.ExecResultInfo(
                successFlag = result,
                errorId = None,
                errorMessage = None
            )

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ExecResultInfo(
                successFlag = result,
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["LIP検索履歴登録API"]
            )

        return response

    @app.route("/post/colorCodeHistory",  methods=["POST"])
    @cross_origin(supports_credentials=True)
    @validate()
    def getProductImage(body: inputBean.ColorCodeHistoryInput):
        """カラーコード検索履歴登録API

        検索回数と履歴を登録する

        Returns:
            json: 実行可否
        """

        try:
            dao = Dao()
            result = dao.ColorCodeHistoryInsert(body.colorCode)
            current_app.logger.error(result)
            response = responseBean.ExecResultInfo(
                successFlag = result,
                errorId = None,
                errorMessage = None
            )

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ExecResultInfo(
                successFlag = result,
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["カラーコード検索履歴登録API"]
            )

        return response