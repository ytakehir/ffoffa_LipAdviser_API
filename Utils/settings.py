# 許可するオリジンのリスト
ALLOWED_ORIGINS = ["http://localhost","http://localhost:3000/", "https://ffoffa.com/", "https://ffoffa.net/"]

# InstagramAPIパス
INSTAGRAM_API_PATH = 'https://graph.facebook.com/v20.0/'

# デフォルト画像パス
IMAGE_PATH = 'https://ffoffa.net/image/'

# colorService設定値
SEARCH_RANGE_VALUE = 3
JUDGE_RANGE_VALUE = 9.0
MAX_SIMILAR_POINT = 10.0

# サクセスフラグ
SUCCESS = "1"
NOT_SUCCESS = "0"

# エラーID 一覧
MESID_SYSTEM_ERROR = { 'SYSE001': 'システムエラー' }
MESID_INPUT_ERROR = { 'SYSE002': '入力値エラー' }
MESID_MAINTENANCE_ERROR = { 'SYSE003': 'メンテナンスエラー'}
MESID_AUTH_ERROR = { 'SYSE004': '認証エラー' }
MESID_INVALID_REQ_ERROR = { 'SYSE005': '入力値不正エラー：{0}：{1} 「{2}」' }
MESID_DB_ACCESS_ERROR = { 'SYSE006': 'DB接続エラー' }
MESID_SSL_ERROR = { 'SYSE007': '非SSL接続エラー' }
MESID_PROCESSING_ERROR = { 'SYSE008': F'{0}に処理中エラー' }