# 標準ライブラリ
import json
import os
import logging

# 外部ライブラリ
import feedparser
import requests
from dotenv import load_dotenv


load_dotenv()
ANIPLEX_RDF = os.environ["ANIPLEX_RDF"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]


logger = logging.getLogger(__name__)


def __is_bocchi_the_radio(target: str):
    return "ぼっち・ざ・らじお！" in target


def __send_slack_webhook(message: str):
    payload = dict(
        text=message,
        link_names=1,
    )
    res = requests.post(
        url=SLACK_WEBHOOK_URL,
        data=json.dumps(payload),
        timeout=3.5,
    )
    res.raise_for_status()


def handler(event, context):
    try:
        logger.info("処理: 開始")
        # RSSでデータ取得
        parser_dict = feedparser.parse(ANIPLEX_RDF)
        for entry in parser_dict.entries:
            title = entry.title

            # タイトルが違う場合、早期continue
            if not __is_bocchi_the_radio(target=title):
                return

            link = entry.link
            logger.info(f"title: {title}, link: {link}")

            slack_message = f"ぼっちざラジオの日だぞ！\n{link}"
            __send_slack_webhook(message=slack_message)
            break

        return dict(
            status=200,
            error_message=None,
        )

    except Exception as e:
        logger.error(e, exc_info=True)
        return dict(
            status=200,
            error_message=str(e),
        )
    finally:
        logger.info("処理: 終了")


if __name__ == "__main__":
    handler("", "")
    pass
