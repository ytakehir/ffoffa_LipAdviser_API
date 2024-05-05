import pymysql.cursors
import sys
sys.path.append('/home/c1343520/program/lipAdviser/')
from Utils import settings as set

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