from flask import Blueprint, jsonify
from pydantic import BaseModel, ValidationError
from flask_pydantic import validate
from typing import Optional
import sys
sys.path.append('C:\\Users\\takeg\\work\\ffoffa_LipAdviser_API\\')
# sys.path.append('/home/c1343520/program/lipAdviser/')
from DB import dataBase
from Utils import sql

# バリデーション
class DBLocalAccessInput(BaseModel):
    sqlIndex : str
    sqlParam1 : Optional[str]
    sqlParam2 : Optional[str]
    sqlParam3 : Optional[str]
    sqlParam4 : Optional[str]
    sqlParam5 : Optional[str]
    sqlParam6 : Optional[str]

app = Blueprint('db', __name__)

class DBLocalAccess:
    @app.route("/dbLocalAccess",  methods=["POST"])
    @validate()
    def colorCodeSearch(body: DBLocalAccessInput):
        """DBアクセスAPI

        ブランド名とカラーコードから同じブランドの似た色のリップを検索する

        Args:
            sqlStr (str): sql文

        Returns:
            json: 取得結果

        Raises:
            例外の名前: 例外の説明

        Yields:
            戻り値の型: 戻り値についての説明

        """

        try:
            conn = dataBase.DBAccess.dbAccess()
            cur = conn.cursor()

            # 結果を取得
            if body.sqlIndex == "1":
                cur.execute(sql.SELECT_WHERE_BRAND_COLORCODE, {"brandName": body.sqlParam1, "colorCode": body.sqlParam2})

            if body.sqlIndex == "2":
                cur.execute(sql.SELECT_WHERE_COLORCODE, {"colorCode": body.sqlParam1})

            if body.sqlIndex == "3":
                cur.execute(sql.SELECT_WHERE_SIMILAR_COLORCODE, {"downVCode": body.sqlParam1, "upVCode": body.sqlParam2, "downSCode": body.sqlParam3, "upSCode": body.sqlParam4})

            result = cur.fetchall()
        except Exception as e:
            # 結果を取得
            result = {"Error": e}
        finally:
            cur.close()
            conn.close()

        return jsonify(result)