from flask import Blueprint, request, jsonify
from flask import current_app
import sys
sys.path.append('/home/c8473744/program/lipAdviser/')
from Utils import webhookUtil as wh
from Utils import settings as set

app = Blueprint('webhook', __name__)

class Webhook:
  @app.route('/webhook', methods=['GET'])
  def verify():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode and token:
      if mode == 'subscribe' and token == set.WEBHOOK_VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge, 200
      else:
        return "Forbidden", 403

  @app.route('/webhook', methods=['POST'])
  def handleWebhook():
    data = request.get_json()
    current_app.logger.error(data)

    if data and 'entry' in data:
      entry = data['entry'][0]

      if 'messaging' in entry:
        messaging = entry['messaging'][0]

        senderId = messaging['sender']['id']

        sm = wh.SendMessage()
        reply = sm.sendAutoReply(senderId, messaging)
        if reply == None:
          current_app.logger.error('no reply date')
          return jsonify({'status': 'no data'}), 400

      return jsonify({'status': 'success'}), 200
    else:
      return jsonify({'status': 'no data'}), 400
