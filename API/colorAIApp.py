# from flask import Blueprint, jsonify
# from flask import current_app
# from flask_cors import cross_origin
# from flask_pydantic import validate
# import cv2
# import numpy as np
# import mediapipe as mp
# import requests
# from io import BytesIO
# import sys
# # sys.path.append('/home/c8473744/program/lipAdviser/')
# sys.path.append('C:/Users/takeg/work/ffoffa_LipAdviser_API/')
# from Utils import colorUtil, responseBean, inputBean
# from Utils import settings as set

# # app = Blueprint('colorAI', __name__)

# # class ColorAI:
# #     @app.route('/getColor', methods=['POST'])
# #     @cross_origin(supports_credentials=True)
# #     @validate()
# def getColor():
#   try:
#     # MediaPipeのセットアップ
#     mpFaceMesh = mp.solutions.face_mesh
#     lips = [73, 72, 11, 302, 303, 404, 315, 16, 85, 180]

#     # 画像をURLから取得
#     response = requests.get("https://scontent-nrt1-2.cdninstagram.com/v/t51.29350-15/459961347_823500002958139_2851689646455737883_n.jpg?stp=dst-jpg_e35&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xNDQweDE3OTkuc2RyLmYyOTM1MC5kZWZhdWx0X2ltYWdlIn0&_nc_ht=scontent-nrt1-2.cdninstagram.com&_nc_cat=1&_nc_ohc=4Ayk8BYc2zkQ7kNvgHQhTPO&edm=AOmX9WgBAAAA&ccb=7-5&ig_cache_key=MzQ1NzczNzk3NjI0MTQzNjUyNg%3D%3D.3-ccb7-5&oh=00_AYDGIJF5Vq6ZlVXKcoTEJCztSg2120y21sHSEnORyD1dtQ&oe=66F6EFBB&_nc_sid=bfaa47")
#     if response.status_code != 200:
#       return jsonify(responseBean.ErrorInfo(
#         errorId=set.MESID_SYSTEM_ERROR,
#         errorMessage=["画像の取得に失敗しました。"]
#       )), 400

#     # 画像をメモリにロード
#     image = cv2.imdecode(np.asarray(bytearray(response.content), dtype=np.uint8), cv2.IMREAD_COLOR)
#     imageRgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # 明るさとコントラストの調整
#     image = cv2.convertScaleAbs(image, alpha=1.05, beta=11)

#     # Face Meshのモデルを使用
#     with mpFaceMesh.FaceMesh(static_image_mode=True) as faceMesh:
#       results = faceMesh.process(imageRgb)

#     if results.multi_face_landmarks:
#       emptyLip = []
#       lipColors = []
#       for faceLandmarks in results.multi_face_landmarks:
#         for i in lips:
#           pt1 = faceLandmarks.landmark[i]
#           h, w, _ = image.shape
#           x = int(pt1.x * w)
#           y = int(pt1.y * h)
#           emptyLip.append((x, y))
#           lipColors.append(image[y, x])

#         # 平均色を計算
#         avgColor = np.mean(lipColors, axis=0).astype(int)

#         # BGR->RGB->HEXに変換
#         cc = colorUtil.ConvertColor()
#         avgColorHEX = cc.rgbToHex(avgColor[[2, 1, 0]])

#         # 緑色で唇のランドマークを描画
#         for (x, y) in emptyLip:
#             cv2.circle(image, (x, y), 2, (0, 255, 0), -1)  # 緑色の点

#     # 結果を表示
#     cv2.imshow("Lip Detection", image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#   except Exception as e:
#     current_app.logger.error(f'エラー詳細：{e}')
#     return jsonify(responseBean.ErrorInfo(
#       errorId=set.MESID_SYSTEM_ERROR,
#       errorMessage=["画像解析色取得API"]
#     )), 400

#   print(avgColorHEX)
#   return jsonify(responseBean.ColorCodeInfo(
#       colorCode=avgColorHEX
#   )), 200

# getColor()
