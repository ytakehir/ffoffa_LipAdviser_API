from flask import Blueprint, jsonify
from pydantic import ValidationError
from flask_pydantic import validate
from flask import current_app
import requests
import sys
sys.path.append('C:/Users/takeg/work/ffoffa_LipAdviser_API/')
# sys.path.append('/home/c1343520/program/lipAdviser/')
from DB.dataBase import Dao
from Utils import colorUtil, inputBean, responseBean
from Utils import settings as set

app = Blueprint('lipAdviser', __name__)

class LipSearch:
    @app.route("/search/brand",  methods=["POST"])
    @validate()
    def searchBrand(body: inputBean.BrandNameSearchInput):
        """同ブランドリップ一覧検索API

        ブランド名から同じブランドのリップを検索する

        Args:
            brandName (str): ブランド名

        Returns:
            json: 取得結果
        """

        try:
            lipColorInfo = []

            url = 'https://spot-search.tokyo/python/lipAdviser/dbLocalAccess'

            data = {
                "sqlIndex": "1",
                "sqlParam1": body.brandName,
                "sqlParam2": "",
                "sqlParam3": "",
                "sqlParam4": "",
                "sqlParam5": "",
                "sqlParam6": ""
            }

            result = requests.post(url, json = data).json()

            for re in result:
                lipColorInfo.append(responseBean.LipColorInfo(
                                ripId = re.get('RIP_ID'),
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
    @validate()
    def searchLipId(body: inputBean.RipIdSearchInput):
        """リップIDリップ検索API

        リップIDからリップを検索する

        Args:
            lipId (int): リップID

        Returns:
            json: 取得結果
        """

        try:
            url = 'https://spot-search.tokyo/python/lipAdviser/dbLocalAccess'

            data = {
                "sqlIndex": "2",
                "sqlParam1": body.ripId,
                "sqlParam2": "",
                "sqlParam3": "",
                "sqlParam4": "",
                "sqlParam5": "",
                "sqlParam6": ""
            }

            result = requests.post(url, json = data).json()

            response = responseBean.BaseLipInfo(
                                ripId = result.get('RIP_ID'),
                                brandName = result.get('BRAND_NAME'),
                                productName = result.get('PRODUCT_NAME'),
                                colorNumber = result.get('COLOR_NUMBER'),
                                colorName = result.get('COLOR_NAME'),
                                colorCode = result.get('COLORCODE'),
                                amount = result.get('AMOUNT'),
                                limitedProductFlag = result.get('LIMITED_PRODUCT_FLAG'),
                                salesStopFlag = result.get('SALES_STOP_FLAG'),
                                cosmeURL = set.COSME_URL_BASE.format(COSME_URL = result.get('COSME_URL'))
                            ).model_dump_json()

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            response = responseBean.ErrorInfo(
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["リップIDリップ検索API"]
            )

        return response

    @app.route("/search/similarColor",  methods=["POST"])
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
            result = dao.similarSelect(similarValue, similarSaturation)

            checkColorList = [re.get('COLORCODE') for re in result]
            similarDict = cs.checkDistanceLab(body.colorCode, checkColorList)
            current_app.logger.debug(similarDict)

            for re in result:
                if re.get('COLORCODE') in similarDict:
                    lipInfo.append(responseBean.SimilarLipInfo(
                                    similarPoint = similarDict[re.get('COLORCODE')],
                                    lipInfo = responseBean.BaseLipInfo(
                                        ripId = re.get('RIP_ID'),
                                        brandName = re.get('BRAND_NAME'),
                                        productName = re.get('PRODUCT_NAME'),
                                        colorNumber = re.get('COLOR_NUMBER'),
                                        colorName = re.get('COLOR_NAME'),
                                        colorCode = re.get('COLORCODE'),
                                        amount = re.get('AMOUNT'),
                                        limitedProductFlag = re.get('LIMITED_PRODUCT_FLAG'),
                                        salesStopFlag = re.get('SALES_STOP_FLAG'),
                                        cosmeURL = set.COSME_URL_BASE.format(COSME_URL = re.get('COSME_URL'))
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