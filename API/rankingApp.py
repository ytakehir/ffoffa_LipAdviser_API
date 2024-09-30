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
  @app.route("/lipHistory",  methods=["POST"])
  @cross_origin(supports_credentials=True)
  @validate()
  def lipHistory(body: inputBean.LipIdInput):
    """LIP検索履歴登録API

    検索回数と履歴を登録する

    Returns:
        json: 実行可否
    """

    try:
      dao = Dao()
      result = dao.lipHistoryInsert(body.lipId)
      response = responseBean.ExecResult(
        successFlag = result,
        errorId = None,
        errorMessage = None
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.ExecResult(
        successFlag = result,
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["LIP検索履歴登録API"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200


  @app.route("/colorCodeHistory",  methods=["POST"])
  @cross_origin(supports_credentials=True)
  @validate()
  def colorCodeHistory(body: inputBean.ColorCodeInput):
    """カラーコード検索履歴登録API

    検索回数と履歴を登録する

    Returns:
        json: 実行可否
    """

    try:
      dao = Dao()
      result = dao.colorCodeHistoryInsert(body.colorCode)
      current_app.logger.error(result)
      response = responseBean.ExecResult(
        successFlag = result,
        errorId = None,
        errorMessage = None
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.ExecResult(
        successFlag = result,
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["カラーコード検索履歴登録API"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200
