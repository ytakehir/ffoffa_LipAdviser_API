from flask import current_app
import hashlib
import sys
sys.path.append('/home/c8473744/program/lipAdviser/')
from DB.dataBase import Dao
from Utils import inputBean, responseBean
from Utils import settings as set

class Auth:
    def authLogin(body: inputBean.AuthInput):
        """API認証

        認証確認

        Returns:
            json: 認証可否
        """

        try:
            dao = Dao()
            result = dao.authKeySelect(body.accessId, body.accessKey)
            current_app.logger.error(result)

            response = result == hashlib.sha512(body.accessId + body.accessKey)

        except Exception as e:
            current_app.logger.error(F'エラー詳細：{e}')
            result = responseBean.ErrorInfo(
                errorId = set.MESID_SYSTEM_ERROR,
                errorMessage = ["API認証"]
            )

        return response

