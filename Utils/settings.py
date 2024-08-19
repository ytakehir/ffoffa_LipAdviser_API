# SSH接続情報
SSH_HOST = 'www86.conoha.ne.jp'
SSH_PORT = 8022,
SSH_USER = 'c1343520',
SSH_KEY_PATH = 'C:\\Users\\takeg\\work\\key\\key-tiltok-trend.pem',
SSH_PASS = 'Take_5030'

# LipAdviser DB接続情報
LIP_ADVISER_DB_NAME = 'cikpt_twu7j5yk'
LIP_ADVISER_DB_HOST = 'mysql16.conoha.ne.jp'
LIP_ADVISER_DB_PORT = 3306,
LIP_ADVISER_DB_USER = 'cikpt_admin'
LIP_ADVISER_DB_PASS = 'Ff0ffa_admin'
LIP_ADVISER_DB_CHARSET = "utf8"

# デフォルト画像パス
IMAGE_PATH = 'https://ffoffa.com/image/'

# colorService設定値
SEARCH_RANGE_VALUE = 3
JUDGE_RANGE_VALUE = 9.0
MAX_SIMILAR_POINT = 10.0

# @cosme URL
COSME_URL_BASE = 'https://www.cosme.net/variations/{COSME_URL}/'

# エラーID 一覧
MESID_SYSTEM_ERROR = { 'SYSE001': 'システムエラー' }
MESID_INPUT_ERROR = { 'SYSE002': '入力値エラー' }
MESID_MAINTENANCE_ERROR = { 'SYSE003': 'メンテナンスエラー'}
MESID_AUTH_ERROR = { 'SYSE004': '認証エラー' }
MESID_INVALID_REQ_ERROR = { 'SYSE005': '入力値不正エラー：{0}：{1} 「{2}」' }
MESID_DB_ACCESS_ERROR = { 'SYSE006': 'DB接続エラー' }
MESID_SSL_ERROR = { 'SYSE007': '非SSL接続エラー' }
MESID_PROCESSING_ERROR = { 'SYSE008': F'{0}に処理中エラー' }