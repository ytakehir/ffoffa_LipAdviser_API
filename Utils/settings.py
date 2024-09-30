# 許可するオリジンのリスト
ALLOWED_ORIGINS = ["http://localhost:3000/", "https://ffoffa.com/"]

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

# ffoffaAPI接続情報
FFOFFA_URL = "https://ffoffa.com/"
FFOFFA_LIP_ADVISER_URL = "https://ffoffa.com/python/lipAdviser/"
API_ACCESS_ID = "ffoffa"
API_ACCESS_KEY = "Ff0ffa_API"

# InstagramAPIパス
INSTAGRAM_API_PATH = 'https://graph.facebook.com/v20.0/'

# デフォルト画像パス
IMAGE_PATH = 'https://ffoffa.com/image/'

# colorService設定値
SEARCH_RANGE_VALUE = 3
JUDGE_RANGE_VALUE = 9.0
MAX_SIMILAR_POINT = 10.0

# サクセスフラグ
SUCCESS = "1"
NOT_SUCCESS = "0"

WEBHOOK_VERIFY_TOKEN = "cd53420c44ef033dca5267f8680e27914bd17772c0536544eb61bde33d7e4e95b98668ecc26a88bd87eac317a14a6ea26be828f2ab456d93063a8beeafdc9635"
WEBHOOK_ACCESS_TOKEN = "EAAMDui2blx4BO3mfD6K0WiiVtHZANPjS87KhLxnHygyb3zsUkVzrj6AR8H0228BsCuR1ZB2UyQZB9QU2Ld8kGqf1btzuFITlbxKtqxizuRquSsJ0e4cH3janhlMFoCC3SGCdCFH4gHQqNuVPtCrhYjYvfgstvJrD1EV6c9L3sQPYifZAESdqGqmi4OFDia5WeN6XAy9o"
WEBHOOK_PAGE_ID = "460508600469897"


# エラーID 一覧
MESID_SYSTEM_ERROR = { 'SYSE001': 'システムエラー' }
MESID_INPUT_ERROR = { 'SYSE002': '入力値エラー' }
MESID_MAINTENANCE_ERROR = { 'SYSE003': 'メンテナンスエラー'}
MESID_AUTH_ERROR = { 'SYSE004': '認証エラー' }
MESID_INVALID_REQ_ERROR = { 'SYSE005': '入力値不正エラー：{0}：{1} 「{2}」' }
MESID_DB_ACCESS_ERROR = { 'SYSE006': 'DB接続エラー' }
MESID_SSL_ERROR = { 'SYSE007': '非SSL接続エラー' }
MESID_PROCESSING_ERROR = { 'SYSE008': F'{0}に処理中エラー' }