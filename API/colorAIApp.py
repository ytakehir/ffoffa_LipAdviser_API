from flask import Blueprint, jsonify
from flask import current_app
from flask_cors import cross_origin
from flask_pydantic import validate
import cv2
import numpy as np
import mediapipe as mp
import base64
import requests
from io import BytesIO
import sys
from Utils import colorUtil, responseBean, inputBean
from Utils import settings as set

app = Blueprint('colorAI', __name__)

class ColorAI:
  @app.route('/getColor', methods=['POST'])
  @cross_origin(supports_credentials=True)
  @validate()
  def getColor(body: inputBean.Base64Input):
    try:
      # MediaPipeのセットアップ
      mpFaceMesh = mp.solutions.face_mesh
      lips = [73, 72, 11, 302, 303, 404, 315, 16, 85, 180]
      fullLips = [61, 185, 40, 39, 37, 0, 269, 270, 409, 291, 375, 321, 405, 314, 17, 84, 181, 91, 146,
                  76, 184, 74, 73, 72, 11, 302, 303, 304, 408, 306, 307, 320, 404, 315, 16, 85, 180, 90, 77,
                  62, 183, 42, 41, 38, 12, 268, 271, 272, 407, 292, 325, 319, 403, 316, 15, 86, 179, 89, 96,
                  78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308, 324, 318, 402, 317, 14, 87, 178, 88, 95,]
      drawing = mp.solutions.drawing_utils
      drawing_spec = drawing.DrawingSpec(thickness=1, color=(70, 70, 70))

      if not body.base64:
        response = responseBean.Error(
          errorId = set.MESID_SYSTEM_ERROR,
          errorMessage = ["画像データが含まれていません。"]
        ).model_dump_json()
        return jsonify(response), 400

      # Base64デコードして画像を復元
      try:
        imageDate = base64.b64decode(body.base64.split(",")[-1])
        image = cv2.imdecode(np.frombuffer(imageDate, np.uint8), cv2.IMREAD_COLOR)
      except Exception as e:
        current_app.logger.error(f'Base64デコードエラー: {e}')
        response = responseBean.Error(
          errorId = set.MESID_SYSTEM_ERROR,
          errorMessage = ["画像データのデコードに失敗しました。"]
        ).model_dump_json()
        return jsonify(response), 400

      if image is None:
        response = responseBean.Error(
          errorId = set.MESID_SYSTEM_ERROR,
          errorMessage = ["画像の読み込みに失敗しました。"]
        ).model_dump_json()
        return jsonify(response), 400

      imageRgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      # 明るさとコントラストの調整
      image = cv2.convertScaleAbs(image, alpha=1.05, beta=11)

      # Face Meshのモデルを使用
      with mpFaceMesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True) as faceMesh:
        results = faceMesh.process(imageRgb)

      if results.multi_face_landmarks:
        emptyLip = []
        lipColors = []
        points = []
        for faceLandmarks in results.multi_face_landmarks:
          for i in lips:
            pt1 = faceLandmarks.landmark[i]
            h, w, _ = image.shape
            x = int(pt1.x * w)
            y = int(pt1.y * h)
            emptyLip.append((x, y))
            lipColors.append(image[y, x])

          # 平均色を計算
          avgColor = np.mean(lipColors, axis=0).astype(int)

          # BGR->RGB->HEXに変換
          cc = colorUtil.ConvertColor()
          avgColorHEX = cc.rgbToHex(avgColor[[2, 1, 0]])

          # 緑色で唇のランドマークを描画
          for i in fullLips:
            pt = faceLandmarks.landmark[i]
            h, w, _ = image.shape
            x = int(pt.x * w)
            y = int(pt.y * h)
            points.append((x, y))
            cv2.circle(image, (x, y), 2, (0, 255, 0), -1)  # 緑色の点


          for _ in results.multi_face_landmarks:
            drawing.draw_landmarks(
                image=image,
                landmark_list=None,
                connections=mpFaceMesh.FACEMESH_LIPS,  # fullLipsのランドマークを接続
                connection_drawing_spec=drawing_spec # デフォルトの接続スタイル
            )

      # 画像をBase64に変換
      _, buffer = cv2.imencode('.jpg', image)
      imageBase64 = base64.b64encode(buffer).decode('utf-8')

    except Exception as e:
      current_app.logger.error(f'エラー詳細：{e}')
      response = responseBean.Error(
        errorId = set.MESID_SYSTEM_ERROR,
        errorMessage = ["画像解析色取得API"]
      ).model_dump_json()
      return jsonify(response), 400

    response = responseBean.colorAI(
      colorCode = avgColorHEX,
      base64 = 'data:image/jpeg;base64,' + imageBase64
    ).model_dump_json()
    return jsonify(response), 200
