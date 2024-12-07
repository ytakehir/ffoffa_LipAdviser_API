from flask import current_app
import hashlib
from ..DB.dataBase import Dao
from ..Utils import inputBean

class Auth:
  def authLogin(auth: inputBean.AuthInput):
    """API認証

    認証確認

    Returns:
      json: 認証可否
    """

    try:
      dao = Dao()
      result = dao.authKeySelect(auth.accessId, auth.accessKey)
      response = result.get('HASH_KEY') == hashlib.sha512(auth.accessId.encode('utf-8') + auth.accessKey.encode('utf-8')).hexdigest()

    except Exception as e:
      current_app.logger.error(F'エラー詳細：{e}')
      response = False

    return response

