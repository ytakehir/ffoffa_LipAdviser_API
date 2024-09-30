from flask import Blueprint, jsonify
from flask_pydantic import validate
from flask import current_app
from flask_cors import cross_origin
import sys
sys.path.append('/home/c8473744/program/lipAdviser/')
from DB.dataBase import Dao
from Utils import apiUtil, colorUtil, inputBean, responseBean
from Utils import settings as set

app = Blueprint('lipAdviser', __name__)

class LipSearch:
  @app.route("/brandName",  methods=["GET"])
  @cross_origin(supports_credentials=True)
  @validate()
  def brandName():
    """ブランド名一覧取得API

    ブランド名を重複なしで取得する

    Args:
        brandName (str): ブランド名

    Returns:
        json: 取得結果
    """

    try:
      brandNameList= []

      dao = Dao()
      result = dao.brandNameSelect()

      for re in result:
        brandNameList.append(responseBean.BrandName(
          brandName = re.get('BRAND_NAME'),
        ))

      response = responseBean.BrandNameList(
        brandNameList = brandNameList
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["ブランド名一覧取得API"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200

  @app.route("/brandsLip",  methods=["POST"])
  @cross_origin(supports_credentials=True)
  @validate()
  def brandsLip(body: inputBean.BrandNameInput):
    """同ブランドリップ一覧検索API

    ブランド名から同じブランドのリップを検索する

    Args:
        brandName (str): ブランド名

    Returns:
        json: 取得結果
    """

    try:
      lipColorList = []

      dao = Dao()
      result = dao.brandsLipSelect(body.brandName)

      for re in result:
        lipColorList.append(responseBean.LipColor(
            lipId = re.get('LIP_ID'),
            productId = re.get('PRODUCT_ID'),
            colorCode = re.get('COLORCODE'),
            brandName = re.get('BRAND_NAME'),
            productName = re.get('PRODUCT_NAME'),
            colorNumber = re.get('COLOR_NUMBER'),
            colorName = re.get('COLOR_NAME')
        ))

      response = responseBean.LipColorList(
        lipColorList = lipColorList
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["同ブランドリップ一覧検索API"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200

  @app.route("/similarColor",  methods=["POST"])
  @cross_origin(supports_credentials=True)
  @validate()
  def similarColor(body: inputBean.ColorCodeInput):
    """類似色リップ検索API

    カラーコードから同じブランドの似た色のリップを検索する

    Args:
        colorCode (str(16進数)): カラーコード

    Returns:
        json: 取得結果
    """

    try:
      lipList = []
      cs = colorUtil.ColorService()
      similarValue = cs.searchSimilarValue(body.colorCode)
      similarSaturation = cs.searchSimilarSaturation(body.colorCode)

      dao = Dao()
      result = dao.similarSelect(similarValue, similarSaturation)

      checkColorList = [re.get('COLORCODE') for re in result]
      similarDict = cs.checkDistanceLab(body.colorCode, checkColorList)

      for re in result:
        if re.get('COLORCODE') in similarDict:
          lipList.append(responseBean.SimilarLip(
            similarPoint = similarDict[re.get('COLORCODE')],
            lipId = re.get('LIP_ID'),
            productId = re.get('PRODUCT_ID'),
            brandName = re.get('BRAND_NAME'),
            productName = re.get('PRODUCT_NAME'),
            colorNumber = re.get('COLOR_NUMBER'),
            colorName = re.get('COLOR_NAME'),
            colorCode = re.get('COLORCODE'),
            amount = re.get('AMOUNT'),
            limitedProductFlag = re.get('LIMITED_PRODUCT_FLAG'),
            salesStopFlag = re.get('SALES_STOP_FLAG'),
            prFlag = re.get('PR_FLAG'),
            officialURL = re.get('OFFICIAL_URL'),
            amazonURL = re.get('AMAZON_URL'),
            qooTenURL = re.get('QOO_TEN_URL')
          ))

      response = responseBean.SimilarLipList(
        lipList = lipList
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["類似色リップ検索API"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200

  @app.route("/similarLip",  methods=["POST"])
  @cross_origin(supports_credentials=True)
  @validate()
  def similarLip(body: inputBean.ColorCodeInput):
    """類似色リップ検索API（タグ付き）

    カラーコードから同じブランドの似た色のリップを検索する

    Args:
        colorCode (str(16進数)): カラーコード

    Returns:
        json: 取得結果
    """

    try:
      productList = []
      cs = colorUtil.ColorService()
      similarValue = cs.searchSimilarValue(body.colorCode)
      similarSaturation = cs.searchSimilarSaturation(body.colorCode)

      dao = Dao()
      result = dao.similarSelect(similarValue, similarSaturation)

      checkColorList = [re.get('COLORCODE') for re in result]
      similarDict = cs.checkDistanceLab(body.colorCode, checkColorList)

      for re in result:
        if re.get('COLORCODE') in similarDict:
          lip = responseBean.SimilarLip(
            similarPoint = similarDict[re.get('COLORCODE')],
            lipId = re.get('LIP_ID'),
            productId = re.get('PRODUCT_ID'),
            brandName = re.get('BRAND_NAME'),
            productName = re.get('PRODUCT_NAME'),
            colorNumber = re.get('COLOR_NUMBER'),
            colorName = re.get('COLOR_NAME'),
            colorCode = re.get('COLORCODE'),
            amount = re.get('AMOUNT'),
            limitedProductFlag = re.get('LIMITED_PRODUCT_FLAG'),
            salesStopFlag = re.get('SALES_STOP_FLAG'),
            prFlag = re.get('PR_FLAG'),
            officialURL = re.get('OFFICIAL_URL'),
            amazonURL = re.get('AMAZON_URL'),
            qooTenURL = re.get('QOO_TEN_URL')
          )

          aus = apiUtil.ApiService()
          tagResult = dao.lipTagSelect(re.get('LIP_ID'))
          tagList = aus.createTag(tagResult)

          imageResult = dao.productImageSelect(re.get('LIP_ID'))
          imageList = aus.createImage(re, imageResult)

          productList.append(responseBean.Product(
            imageList = imageList,
            lip = lip,
            tagList = tagList
          ))

      response = responseBean.ProductList(
        productList = productList
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["類似色リップ検索API（タグ付き）"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200

  @app.route("/sameLip",  methods=["POST"])
  @cross_origin(supports_credentials=True)
  @validate()
  def sameLip(body: inputBean.ProductIdInput):
    """同一商品検索API（タグ付き）

    リップのカラーバリエーションなどを検索する

    Args:
        productId (int): リップID

    Returns:
        json: 取得結果
    """

    try:
      productList = []
      dao = Dao()
      result = dao.productIdSelect(body.productId)

      for re in result:
        lip = responseBean.BaseLip(
          lipId = re.get('LIP_ID'),
          productId = re.get('PRODUCT_ID'),
          brandName = re.get('BRAND_NAME'),
          productName = re.get('PRODUCT_NAME'),
          colorNumber = re.get('COLOR_NUMBER'),
          colorName = re.get('COLOR_NAME'),
          colorCode = re.get('COLORCODE'),
          amount = re.get('AMOUNT'),
          limitedProductFlag = re.get('LIMITED_PRODUCT_FLAG'),
          salesStopFlag = re.get('SALES_STOP_FLAG'),
          prFlag = re.get('PR_FLAG'),
          officialURL = re.get('OFFICIAL_URL'),
          amazonURL = re.get('AMAZON_URL'),
          qooTenURL = re.get('QOO_TEN_URL')
        )

        aus = apiUtil.ApiService()
        tagResult = dao.lipTagSelect(re.get('LIP_ID'))
        tagList = aus.createTag(tagResult)

        imageResult = dao.productImageSelect(re.get('LIP_ID'))
        imageList = aus.createImage(re, imageResult)

        productList.append(responseBean.Product(
          imageList = imageList,
          lip = lip,
          tagList = tagList
        ))

      response = responseBean.ProductList(
        productList = productList
      ).model_dump_json()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["同一商品検索API（タグ付き）"]
      ).model_dump_json()
      return jsonify(response), 400

    return jsonify(response), 200
