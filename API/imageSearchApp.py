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

app = Blueprint('image', __name__)

class TagSearch:
    @app.route("/search/logoImage",  methods=["GET"])
    @cross_origin(supports_credentials=True)
    @validate()
    def getBrandLogoImage():
        """ロゴ画像一覧取得API

        ロゴ画像を重複なしで取得する

        Returns:
            json: 取得結果
        """

        try:
            imageInfo = []

            dao = Dao()
            result = dao.logoImageSelect()
            current_app.logger.error(result)

            for re in result:
                imageInfo.append(responseBean.BaseImageInfo(
                                path = f"{set.IMAGE_PATH}{re.get('BRAND_NAME')}/logo/{re.get('PATH')}"
                            ))

            response = responseBean.ImageInfoList(
                imageList = imageInfo
            ).model_dump_json()

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ErrorInfo(
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["ロゴ画像一覧取得API"]
            )

        return response

    @app.route("/search/productImage",  methods=["POST"])
    @cross_origin(supports_credentials=True)
    @validate()
    def getProductImage(body: inputBean.ImageSearchInput):
        """商品画像取得API

        商品画像を取得する

        Returns:
            json: 取得結果
        """

        try:
            imageInfo = []

            dao = Dao()
            result = dao.productImageSelect(body.lipId)
            current_app.logger.error(result)

            for re in result:
                imageInfo.append(responseBean.BaseImageInfo(
                                path = f"{set.IMAGE_PATH}{re.get('BRAND_NAME')}/product/{re.get('PATH')}"
                            ))

            response = responseBean.ImageInfoList(
                imageList = imageInfo
            ).model_dump_json()

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ErrorInfo(
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["商品画像取得API"]
            )

        return response
