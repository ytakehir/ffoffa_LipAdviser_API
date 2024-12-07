import requests
import json

class ApiRequest:
  def post(self, url, headers, body):
    response = requests.post(url, headers=headers, json=body)

    # ステータスコードを確認
    if response.status_code == 200:
      strData = response.json()
      data = json.loads(strData)
    else:
      return None

    return data
