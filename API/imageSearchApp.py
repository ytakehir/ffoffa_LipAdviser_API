from flask import Blueprint, jsonify
from flask_pydantic import validate
from flask import current_app
from flask_cors import cross_origin
from DB.dataBase import Dao
from Utils import inputBean, responseBean
from Utils import settings as set

app = Blueprint('image', __name__)

class TagSearch:
  @app.route("/logoImage",  methods=["GET"])
  @cross_origin(supports_credentials=True)
  @validate()
  def brandLogoImage():
    """ロゴ画像一覧取得API

    ロゴ画像を重複なしで取得する

    Returns:
      json: 取得結果
    """

    try:
      imageList = []

      dao = Dao()
      result = dao.logoImageSelect()

      for re in result:
        imageList.append(responseBean.BaseImage(
          alt = re.get('BRAND_NAME'),
          path = f"{set.IMAGE_PATH}{re.get('BRAND_NAME')}/logo/{re.get('PATH')}"
        ))

      response = responseBean.ImageList(
        imageList = imageList
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["ロゴ画像一覧取得API"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200

  @app.route("/productImage",  methods=["POST"])
  @cross_origin(supports_credentials=True)
  @validate()
  def productImage(body: inputBean.LipIdInput):
    """商品画像取得API

    商品画像を取得する

    Returns:
      json: 取得結果
    """

    try:
      imageList = []

      dao = Dao()
      result = dao.productImageSelect(body.lipId)

      for re in result:
        imageList.append(responseBean.BaseImage(
          alt = re.get('BRAND_NAME'),
          path = f"{set.IMAGE_PATH}{re.get('BRAND_NAME')}/product/{re.get('PATH')}"
        ))

      response = responseBean.ImageList(
        imageList = imageList
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["商品画像取得API"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200

