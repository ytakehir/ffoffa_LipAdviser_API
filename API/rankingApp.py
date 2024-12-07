from flask import Blueprint, jsonify
from flask_pydantic import validate
from flask import current_app
from flask_cors import cross_origin
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

    Args:
      lipId (int): リップID

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

  @app.route("/lipRanking",  methods=["POST"])
  @cross_origin(supports_credentials=True)
  @validate()
  def lipRanking(body: inputBean.IntervalInput):
    """LIP検索ランキング取得API

    検索回数の上位10個取得する

    Args:
      interval (int): 検索期間

    Returns:
      json: 実行可否
    """

    try:
      rank = []
      dao = Dao()
      result = dao.lipRankingSelect(body.interval)

      for re in result:
        rank.append(responseBean.LipRanking(
          lipId = re.get('LIP_ID'),
          count = re.get('COUNT'),
        ))

      response = responseBean.LipRankingList(
        lipRankingList = rank
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["LIP検索ランキング取得API"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200


  @app.route("/colorCodeHistory",  methods=["POST"])
  @cross_origin(supports_credentials=True)
  @validate()
  def colorCodeHistory(body: inputBean.ColorCodeInput):
    """カラーコード検索履歴登録API

    検索回数と履歴を登録する

    Args:
      colorCode (str(16進数)): カラーコード

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
