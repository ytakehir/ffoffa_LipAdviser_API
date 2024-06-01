from flask import Blueprint, jsonify
from pydantic import ValidationError
from flask_pydantic import validate
from flask import current_app
from flask_cors import cross_origin
import requests
import sys
sys.path.append('C:/Users/takeg/work/ffoffa_LipAdviser_API/')
# sys.path.append('/home/c1343520/program/lipAdviser/')
from DB.dataBase import Dao
from Utils import colorUtil, inputBean, responseBean
from Utils import settings as set

app = Blueprint('lipAdviser', __name__)

class LipSearch:
    @app.route("/search/brandName",  methods=["GET"])
    @cross_origin(supports_credentials=True)
    @validate()
    def searchBrandName():
        """ブランド名一覧取得API

        ブランド名を重複なしで取得する

        Args:
            brandName (str): ブランド名

        Returns:
            json: 取得結果
        """

        try:
            brandNameInfo = []

            dao = Dao()
            result = dao.brandNameSelect()

            for re in result:
                brandNameInfo.append(responseBean.BrandNameInfo(
                                brandName = re.get('BRAND_NAME'),
                            ))

            response = responseBean.BrandNameInfoList(
                brandNameList = brandNameInfo
            ).model_dump_json()

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ErrorInfo(
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["ブランド名一覧取得API"]
            )

        return response

    @app.route("/search/brandsLip",  methods=["POST"])
    @cross_origin(supports_credentials=True)
    @validate()
    def searchBrandsLip(body: inputBean.BrandNameSearchInput):
        """同ブランドリップ一覧検索API

        ブランド名から同じブランドのリップを検索する

        Args:
            brandName (str): ブランド名

        Returns:
            json: 取得結果
        """

        try:
            lipColorInfo = []

            dao = Dao()
            result = dao.brandsLipSelect(body.brandName)

            for re in result:
                lipColorInfo.append(responseBean.LipColorInfo(
                                lipId = re.get('LIP_ID'),
                                colorCode = re.get('COLORCODE'),
                                brandName = re.get('BRAND_NAME'),
                                productName = re.get('PRODUCT_NAME'),
                                colorNumber = re.get('COLOR_NUMBER'),
                                colorName = re.get('COLOR_NAME')
                            ))

            response = responseBean.LipColorInfoList(
                lipColorInfoList = lipColorInfo
            ).model_dump_json()

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ErrorInfo(
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["同ブランドリップ一覧検索API"]
            )

        return response

    @app.route("/search/lipId",  methods=["POST"])
    @cross_origin(supports_credentials=True)
    @validate()
    def searchLipId(body: inputBean.LipIdSearchInput):
        """リップIDリップ検索API

        リップIDからリップを検索する

        Args:
            lipId (int): リップID

        Returns:
            json: 取得結果
        """

        try:
            dao = Dao()
            result = dao.lipIdSelect(body.lipId)

            for re in result:
                    response = responseBean.BaseLipInfo(
                                    lipId = re.get('LIP_ID'),
                                    brandName = re.get('BRAND_NAME'),
                                    productName = re.get('PRODUCT_NAME'),
                                    colorNumber = re.get('COLOR_NUMBER'),
                                    colorName = re.get('COLOR_NAME'),
                                    colorCode = re.get('COLORCODE'),
                                    amount = re.get('AMOUNT'),
                                    limitedProductFlag = re.get('LIMITED_PRODUCT_FLAG'),
                                    salesStopFlag = re.get('SALES_STOP_FLAG'),
                                    officialURL = re.get('OFFICIAL_URL'),
                                    amazonURL = re.get('AMAZON_URL'),
                                    qooTenURL = re.get('QOO_TEN_URL')
                                ).model_dump_json()

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ErrorInfo(
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["リップIDリップ検索API"]
            )

        return response

    @app.route("/search/similarColor",  methods=["POST"])
    @cross_origin(supports_credentials=True)
    @validate()
    def searchSimilarColor(body: inputBean.ColorCodeSearchInput):
        """類似色リップ検索API

        カラーコードから同じブランドの似た色のリップを検索する

        Args:
            colorCode (str(16進数)): カラーコード

        Returns:
            json: 取得結果
        """

        try:
            current_app.logger.debug('Start!!!!!!!')
            lipInfo = []
            cs = colorUtil.ColorService()
            similarValue = cs.searchSimilarValue(body.colorCode)
            similarSaturation = cs.searchSimilarSaturation(body.colorCode)

            dao = Dao()
            result = dao.similarSelect(similarValue, similarSaturation, body.lipId)

            checkColorList = [re.get('COLORCODE') for re in result]
            similarDict = cs.checkDistanceLab(body.colorCode, checkColorList)
            current_app.logger.debug(similarDict)

            for re in result:
                if re.get('COLORCODE') in similarDict:
                    lipInfo.append(responseBean.SimilarLipInfo(
                                    similarPoint = similarDict[re.get('COLORCODE')],
                                    lipInfo = responseBean.BaseLipInfo(
                                        lipId = re.get('LIP_ID'),
                                        brandName = re.get('BRAND_NAME'),
                                        productName = re.get('PRODUCT_NAME'),
                                        colorNumber = re.get('COLOR_NUMBER'),
                                        colorName = re.get('COLOR_NAME'),
                                        colorCode = re.get('COLORCODE'),
                                        amount = re.get('AMOUNT'),
                                        limitedProductFlag = re.get('LIMITED_PRODUCT_FLAG'),
                                        salesStopFlag = re.get('SALES_STOP_FLAG'),
                                        officialURL = re.get('OFFICIAL_URL'),
                                        amazonURL = re.get('AMAZON_URL'),
                                        qooTenURL = re.get('QOO_TEN_URL')
                                    )
                                ))

            response = responseBean.SimilarLipInfoList(
                lipInfoList = lipInfo
            ).model_dump_json()
            current_app.logger.debug(response)

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ErrorInfo(
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["類似色リップ検索API"]
            )

        return response