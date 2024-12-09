from flask import jsonify, current_app
import pymysql.cursors
from Utils import config
from Utils import sql
from Utils import settings as set

class DBAccess:
  def dbAccess():
    """DBの接続
    Returns:
      Obj: DB接続情報
    """

    pymysql.install_as_MySQLdb()
    pymysql.DEBUG = True

    try:
      conn = pymysql.connect(
        host = config.LIP_ADVISER_DB_HOST,
        db = config.LIP_ADVISER_DB_NAME,
        user = config.LIP_ADVISER_DB_USER,
        password = config.LIP_ADVISER_DB_PASS,
        cursorclass = pymysql.cursors.DictCursor
      )
    except Exception as e:
      # 結果を取得
      current_app.logger.error(repr(e))

      return {"Error": repr(e)}

    return conn

class Dao:
  def authKeySelect(self, accessId, accessKey):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # 結果を取得
      cur.execute(sql.SELECT_AUTH, {"accessId": accessId, "accessKey": accessKey})
      result = cur.fetchone()
    except Exception as e:
      # 結果を取得
      result = {"Error": e}
    finally:
      cur.close()
      conn.close()

    return result

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
      result = cur.fetchone()
    except Exception as e:
      # 結果を取得
      result = {"Error": e}
    finally:
      cur.close()
      conn.close()

    return result

  def productIdSelect(self, productId):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # 結果を取得
      cur.execute(sql.SELECT_WHERE_PRODUCT_ID, {"productId": productId})
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

  def similarSelect(self, similarValue, similarSaturation):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # 結果を取得
      cur.execute(sql.SELECT_WHERE_SIMILAR_COLORCODE, {"downVCode": similarValue[0], "upVCode": similarValue[1], "downSCode": similarSaturation[0], "upSCode": similarSaturation[1]})
      result = cur.fetchall()
    except Exception as e:
      # 結果を取得
      result = {"Error": e}
    finally:
      cur.close()
      conn.close()

    return result

  def lipTagSelect(self, lipId):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # 結果を取得
      cur.execute(sql.SELECT_WHERE_LIP_TAG, {"lipId": lipId})
      result = cur.fetchall()
    except Exception as e:
      # 結果を取得
      result = {"Error": e}
    finally:
      cur.close()
      conn.close()

    return result

  def tagSelect(self):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # 結果を取得
      cur.execute(sql.SELECT_DISTINCT_TAG_NAME)
      result = cur.fetchall()
    except Exception as e:
      # 結果を取得
      result = {"Error": e}
    finally:
      cur.close()
      conn.close()

    return result

  def logoImageSelect(self):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # 結果を取得
      cur.execute(sql.SELECT_DISTINCT_LOGO_IMAGE)
      result = cur.fetchall()
    except Exception as e:
      # 結果を取得
      result = {"Error": e}
    finally:
      cur.close()
      conn.close()

    return result

  def productImageSelect(self, lipId):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # 結果を取得
      cur.execute(sql.SELECT_WHERE_LIP_IMAGE, {"lipId": lipId})
      result = cur.fetchall()
    except Exception as e:
      # 結果を取得
      result = {"Error": e}
    finally:
      cur.close()
      conn.close()

    return result

  def lipHistoryInsert(self, lipId):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # データを登録
      cur.execute(sql.INSERT_UPDATE_LIP_COUNT, {"lipId": lipId})
      cur.execute(sql.INSERT_LIP_SEARCH_HISTORY, {"lipId": lipId})
      conn.commit()
      result = set.SUCCESS
    except Exception as e:
      result = set.NOT_SUCCESS
    finally:
      cur.close()
      conn.close()

    return result

  def colorCodeHistoryInsert(self, colorCode):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # データを登録
      cur.execute(sql.INSERT_UPDATE_COLORCODE_COUNT, {"colorCode": colorCode})
      cur.execute(sql.INSERT_COLORCODE_SEARCH_HISTORY, {"colorCode": colorCode})
      conn.commit()
      result = set.SUCCESS
    except Exception as e:
      result = set.NOT_SUCCESS
    finally:
      cur.close()
      conn.close()

    return result

  def productSelect(self):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # 結果を取得
      cur.execute(sql.SELECT_DISTINCT_PRODUCT_ID)
      result = cur.fetchall()
    except Exception as e:
      # 結果を取得
      result = {"Error": e}
    finally:
      cur.close()
      conn.close()

    return result

  def lipRankingSelect(self, interval):
    """SELECT
    Returns:
      Obj: DB接続情報
    """

    try:
      conn = DBAccess.dbAccess()
      cur = conn.cursor()

      # 結果を取得
      cur.execute(sql.SELECT_RANKING_LIP, {"interval": interval})
      result = cur.fetchall()
    except Exception as e:
      # 結果を取得
      result = {"Error": e}
    finally:
      cur.close()
      conn.close()

    return result