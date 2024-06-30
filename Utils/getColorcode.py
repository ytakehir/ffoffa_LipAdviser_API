from PIL import Image
import numpy as np

# 画像を読み込む
image_path = '../スクリーンショット 2024-06-07 001841.png'
image = Image.open(image_path)

# 画像の幅と高さを取得
width, height = image.size

# 各行の中央のピクセルの色を取得
color_list_in_order = [image.getpixel((width // 2, y)) for y in range(height)]

# これらの色を16進数のカラーコードに変換
color_hex_codes_in_order = [f'#{r:02x}{g:02x}{b:02x}' for r, g, b, a in color_list_in_order]

# 重複するカラーコードを除去し、順序を維持するために辞書を使用
color_hex_codes_in_order = list(dict.fromkeys(color_hex_codes_in_order))

# 配列の要素数を取得
number_of_colors = len(color_hex_codes_in_order)

print(color_hex_codes_in_order)
print(f"Number of unique colors: {number_of_colors}")