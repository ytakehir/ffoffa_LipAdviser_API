from flask import jsonify
import pymysql.cursors
from flask import current_app
import sys
sys.path.append('C:\\Users\\takeg\\work\\ffoffa_LipAdviser_API\\')
# sys.path.append('/home/c1343520/program/lipAdviser/')
from Utils import sql, responseBean
from Utils import settings as set

class DBAccess:
    def dbAccess():
        """DBの接続
        Returns:
            Obj: DB接続情報
        """
        conn = pymysql.connect(
            host = set.LIP_ADVISER_DB_HOST,
            db = set.LIP_ADVISER_DB_NAME,
            user = set.LIP_ADVISER_DB_USER,
            password = set.LIP_ADVISER_DB_PASS,
            cursorclass = pymysql.cursors.DictCursor
        )

        return conn


class Dao:
    def brandNameSelect(self):
        """SELECT
        Returns:
            Obj: DB接続情報
        """

        try:
            conn = DBAccess.dbAccess()
            cur = conn.cursor()

            # 結果を取得
            cur.execute(sql.SELECT_DISTINCT_BRAND_NAME)
            result = cur.fetchall()
        except Exception as e:
            # 結果を取得
            result = {"Error": e}
        finally:
            cur.close()
            conn.close()

        return result

    def lipIdSelect(self, lipId):
        """SELECT
        Returns:
            Obj: DB接続情報
        """

        try:
            conn = DBAccess.dbAccess()
            cur = conn.cursor()

            # 結果を取得
            cur.execute(sql.SELECT_WHERE_LIP_ID, {"lipId": lipId})
            result = cur.fetchall()
        except Exception as e:
            # 結果を取得
            result = {"Error": e}
        finally:
            cur.close()
            conn.close()

        return result

    def brandsLipSelect(self, brandName):
        """SELECT
        Returns:
            Obj: DB接続情報
        """

        try:
            conn = DBAccess.dbAccess()
            cur = conn.cursor()

            # 結果を取得
            cur.execute(sql.SELECT_WHERE_BRAND_NAME, {"brandName": brandName})
            result = cur.fetchall()
        except Exception as e:
            # 結果を取得
            result = {"Error": e}
        finally:
            cur.close()
            conn.close()

        return result

    def similarSelect(self, similarValue, similarSaturation, lipId):
        """SELECT
        Returns:
            Obj: DB接続情報
        """

        try:
            conn = DBAccess.dbAccess()
            cur = conn.cursor()

            # 結果を取得
            cur.execute(sql.SELECT_WHERE_SIMILAR_COLORCODE, {"downVCode": similarValue[0], "upVCode": similarValue[1], "downSCode": similarSaturation[0], "upSCode": similarSaturation[1], "lipId" : lipId})
            result = cur.fetchall()
        except Exception as e:
            # 結果を取得
            result = {"Error": e}
        finally:
            cur.close()
            conn.close()

        return result