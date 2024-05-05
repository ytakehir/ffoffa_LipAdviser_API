from flask import Blueprint, jsonify
from pydantic import BaseModel, Field, ValidationError
from flask_pydantic import validate
import sys
sys.path.append('/home/c1343520/program/lipAdviser/')
from Utils import colorUtil, sql
from DB import db

# バリデーション
class colorCodeSerachInput(BaseModel):
    brandName: str
    colorCode: str = Field(min_length = 3, max_length = 6, pattern = r"[A-Fa-f0-9]")

app = Blueprint('lipAdviser', __name__)


@app.route("/sameColorCodeSerach",  methods=["POST"])
@validate()
def sameColorCodeSerach(body: colorCodeSerachInput):
    """同ブランド同色リップ検索API

    ブランド名とカラーコードから同じブランドの似た色のリップを検索する

    Args:
        brandName (str): ブランド名
        colorCode (str(16進数)): カラーコード

    Returns:
        json: 取得結果

    Raises:
        例外の名前: 例外の説明

    Yields:
        戻り値の型: 戻り値についての説明

    """

    try:
        conn = db.dbAccess()
        cur = conn.cursor()

        # データ取得
        cur.execute(sql.SELECT_WHERE_BRAND_COLORCODE, {"brandName": body.brandName, "colorCode": body.colorCode})

        # 結果を取得
        result = cur.fetchall()
    except ValidationError as e:
        # 結果を取得
        result = {"Error": e}
    finally:
        cur.close()
        conn.close()

    return jsonify(result)


@app.route("/similarColorCodeSearch",  methods=["POST"])
@validate()
def similarColorCodeSearch(body: colorCodeSerachInput):
    """同ブランド類似色リップ検索API

    ブランド名とカラーコードから同じブランドの似た色のリップを検索する

    Args:
        brandName (str): ブランド名
        colorCode (str(16進数)): カラーコード

    Returns:
        json: 取得結果

    Raises:
        例外の名前: 例外の説明

    Yields:
        戻り値の型: 戻り値についての説明

    """

    try:
        conn = db.dbAccess()
        cur = conn.cursor()

        similarValue = colorUtil.searchSimilarValue(body.colorCode)
        similarSaturation = colorUtil.searchSimilarSaturation(body.colorCode)
        
        print(similarValue[0], similarValue[1], similarSaturation[0], similarSaturation[1])

        # データ取得
        cur.execute(sql.SELECT_WHERE_SIMILAR_COLORCODE, {"downVCode": similarValue[0], "upVCode": similarValue[1], "downSCode": similarSaturation[0], "upSCode": similarSaturation[1]})

        # 結果を取得
        result = cur.fetchall()
    except ValidationError as e:
        # 結果を取得
        result = {"Error": e}
    finally:
        cur.close()
        conn.close()

    return jsonify({"result": similarValue[0]})