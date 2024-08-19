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

app = Blueprint('tag', __name__)

class TagSearch:
    @app.route("/search/tags",  methods=["GET"])
    @cross_origin(supports_credentials=True)
    @validate()
    def getBrandName():
        """タグ一覧取得API

        タグを重複なしで取得する

        Returns:
            json: 取得結果
        """

        try:
            tagInfo = []

            dao = Dao()
            result = dao.tagSelect()

            for re in result:
                tagInfo.append(responseBean.BaseTagInfo(
                                tagId = re.get('ID'),
                                tagName = re.get('TAG_NAME'),
                                tagGenre = re.get('TAG_GENRE'),
                            ))

            response = responseBean.TagInfoList(
                tagList = tagInfo
            ).model_dump_json()

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ErrorInfo(
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["タグ一覧取得API"]
            )

        return response
