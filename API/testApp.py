from flask import Blueprint, jsonify

app = Blueprint('func', __name__)

class test:
  @app.route("/test")
  def test():
    """接続確認用API
    Returns:
      json: 接続できた場合"Hello World"が返却される
    """
    return jsonify({'message': 'Hello world'}), 200