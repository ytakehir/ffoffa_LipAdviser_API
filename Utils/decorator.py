from flask import current_app
from DB import dataBase
from Utils import responseBean
from Utils import settings as set

def a(func):
    def wrapper(*args, **kwargs):
        try:
            func()
        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            result = responseBean.ErrorInfo(
                errorId = set.MESID_DB_ACCSESS_ERROR,
                errorMessage = ["DB接続"]
            )
        finally:
            dataBase.dao.dbClose()