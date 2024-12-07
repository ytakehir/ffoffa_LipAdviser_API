from flask import Blueprint, jsonify
from flask_pydantic import validate
from flask import current_app
from flask_cors import cross_origin
from DB.dataBase import Dao
from Utils import responseBean
from Utils import settings as set

app = Blueprint('tag', __name__)

class TagSearch:
  @app.route("/tags",  methods=["GET"])
  @cross_origin(supports_credentials=True)
  @validate()
  def tags():
    """タグ一覧取得API

    タグを重複なしで取得する

    Returns:
      json: 取得結果
    """

    try:
      tagList = []

      dao = Dao()
      result = dao.tagSelect()

      for re in result:
        tagList.append(responseBean.BaseTag(
          tagId = re.get('ID'),
          tagName = re.get('TAG_NAME'),
          tagGenre = re.get('TAG_GENRE'),
        ))

      response = responseBean.TagList(
        tagList = tagList
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["タグ一覧取得API"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200

