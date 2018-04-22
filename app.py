from __future__ import unicode_literals

import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

xline_bot_api = LineBotApi('avIDjwy7hrp4tlLjEbnOTTT2XF5jhApx96zUN2sRDtLl5w5u1PZ+iJ5FXCDX53Mu9vEpg7Eq0eV3Pl8m4v5MnD8P4TKjjlOClf/VVShXzEqtJsspCDpOMNehiOyJePPRXlhpyEibfoX/b5zu8a3k8gdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('9f530fcd5e1273891a2541d873387272')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )

    return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=5000, help='port')
    arg_parser.add_argument('-d', '--debug', default=True, help='debug')
    options = arg_parser.parse_args()

app.run(
    host="0.0.0.0",
    port=os.environ.get('PORT')
)