# 標準ライブラリ
import json
import os
from enum import Enum


# 外部ライブラリ
import feedparser
import requests
from dotenv import load_dotenv


load_dotenv()
ANIPLEX_RDF = os.environ["ANIPLEX_RDF"]
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]


class LogLevelEnum(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


def __log(level: LogLevelEnum, message: str):
    print(f"[{level.value}] {message}")


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


def lambda_handler(event, context):
    try:
        __log(level=LogLevelEnum.INFO, message="処理: 開始")
        # RSSでデータ取得
        parser_dict = feedparser.parse(ANIPLEX_RDF)
        for entry in parser_dict.entries:
            title = entry.title

            # タイトルが違う場合、早期continue
            if not __is_bocchi_the_radio(target=title):
                continue

            link = entry.link
            __log(level=LogLevelEnum.INFO, message=f"title: {title}, link: {link}")

            slack_message = f"ぼっちざラジオの日だぞ！\n{link}"
            __send_slack_webhook(message=slack_message)

            return dict(
                status=200,
                error_message=None,
            )

        __log(level=LogLevelEnum.WARNING, message="bocchi the radio is not found.")
        return dict(
            status=404,
            error_message="bocchi the radio is not found.",
        )

    except Exception as e:
        __log(level=LogLevelEnum.ERROR, message=str(e))
        return dict(
            status=200,
            error_message=str(e),
        )
    finally:
        __log(level=LogLevelEnum.INFO, message="処理: 終了")
