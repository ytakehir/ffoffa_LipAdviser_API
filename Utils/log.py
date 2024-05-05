import logging.handlers
import time

def main():
    # ロギングの基本設定
    formatter = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level = logging.INFO, format = formatter, encoding = "utf_8")

    # ロガーの作成
    logger = logging.getLogger(__name__)
    # ログレベルをDEBUGへ変更
    logger.setLevel(logging.DEBUG)

    # ログローテーションのハンドラーを設定
    handler = logging.handlers.TimedRotatingFileHandler(
        'LipAdviser.log', when = 'MIDNIGHT', backupCount = 31
    )

    # フォーマットを設定
    handler.setFormatter(logging.Formatter(formatter))

    # ロガーにハンドラーを設定
    logger.addHandler(handler)
    for _ in range(1000):
        time.sleep(0.1)
        logger.debug("log rotation test")

if __name__ == "__main__":
    main()