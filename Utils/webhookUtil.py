import requests
from flask import current_app
from ..Utils import apiRequest
from ..Utils import settings as set

class WebhookService:
  def replyMessage(self, senderId, messaging):
    sm = SendMessage()
    if 'message' in messaging:
      if 'text' in messaging['message']:
          messageText = messaging['message']['text']
          reply = sm.sendAutoReplyText(senderId, messageText)
      elif 'attachments' in messaging['message']:
          attachments = messaging['message']['attachments']
          for attachment in attachments:
              if attachment['type'] == 'image' or attachment['type'] == 'share':
                  colorCode = self.getColorCode()
                  reply = sm.sendAutoReplyProductTemplate(senderId, colorCode)
              else:
                  messageText = '現在は画像のみ受け付けています。'
                  reply = reply = sm.sendAutoReplyText(senderId, messageText)
    else:
      return None
    return reply

  def judgeText(self, messageText):
    if 'hello' in messageText:
        replyText = "Hello! How can I assist you today?"
    elif 'help' in messageText:
        replyText = "Sure, I can help! What do you need assistance with?"
    elif 'info' in messageText:
        replyText = "Here is some information about our services."
    else:
        replyText = messageText

    return replyText

  def getColorCode(self):
    return 'cb4a54'

  def createTemplate(self, senderId, colorCode, productList):
    productList = productList['productList']
    sortedProducts = sorted(productList, key=lambda product: product['lip']['similarPoint'], reverse=True)[:3]

    elementList = []
    for product in sortedProducts:
      element = {
        "title": f"{product['lip']['brandName']} {product['lip']['productName']}",
        "subtitle": f"{product['lip']['colorNumber']} {product['lip']['colorName']}\n{product['lip']['amount']}",
        "image_url": product['imageList'][0]['path'],
        "buttons": [
            {
                "type": "web_url",
                "url": product['lip']['officialURL'],
                "title": "OFFICIAL"
            },
            {
                "type": "web_url",
                "url": product['lip']['amazonURL'],
                "title": "Amazon"
            },
            {
                "type": "web_url",
                "url": product['lip']['qooTenURL'],
                "title": "Qoo10"
            }
        ]
      }
      elementList.append(element)

    showMore = {
      "title": f"似ているリップをもっと見る",
      "default_action": {
          "type": "web_url",
          "url": f'{set.FFOFFA_URL}result/{colorCode}',
      },
      "buttons": [
        {
            "type": "web_url",
            "url": f'{set.FFOFFA_URL}result/{colorCode}',
            "title": "もっと見る"
        }
      ]
    }
    elementList.append(showMore)

    # 送信するメッセージのデータ
    data = {
      "recipient": {
        "id": senderId,
      },
      "message": {
        "attachment": {
          "type": "template",
          "payload": {
            "template_type": "generic",
            "elements": elementList
          }
        }
      }
    }

    return data

class SendMessage:
  def sendAutoReplyText(self, senderId, message):
    ws = WebhookService()
    reply = ws.judgeText(message)
    data = {
        "recipient": {"id": senderId},
        "message": {"text": reply}
    }

    return data

  def sendAutoReplyProductTemplate(self, senderId, colorCode):
    ar = apiRequest.ApiRequest()
    headers = {
      "Content-Type": "application/json; charset=UTF-8",
      "accessId": set.API_ACCESS_ID,
      "accessKey": set.API_ACCESS_KEY
    }

    body = {
      "colorCode": colorCode
    }

    response = ar.post(f'{set.FFOFFA_LIP_ADVISER_URL}similarLip', headers, body)
    ar.post(f'{set.FFOFFA_LIP_ADVISER_URL}colorCodeHistory', headers, body)

    if response != None:
      ws = WebhookService()
      data = ws.createTemplate(senderId, colorCode, response)

    else:
      current_app.logger.error(f"Failed to send reply: {response.status_code}, {response.text}")

    return data

  def sendAutoReply(self, senderId, message):
    ws = WebhookService()
    data = ws.replyMessage(senderId, message)

    # POSTリクエストでメッセージを送信
    url = f"{set.INSTAGRAM_API_PATH}me/messages?access_token={set.WEBHOOK_ACCESS_TOKEN}"
    response = requests.post(url, json=data)

    if response.status_code == 200:
        current_app.logger.error(f"Auto-reply sent to {senderId}")
    else:
        current_app.logger.error(f"Failed to send reply: {response.status_code}, {response.text}")

