# encoding: utf-8
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('avIDjwy7hrp4tlLjEbnOTTT2XF5jhApx96zUN2sRDtLl5w5u1PZ+iJ5FXCDX53Mu9vEpg7Eq0eV3Pl8m4v5MnD8P4TKjjlOClf/VVShXzEqtJsspCDpOMNehiOyJePPRXlhpyEibfoX/b5zu8a3k8gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9f530fcd5e1273891a2541d873387272')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text #message from user

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)) #reply the same message from user
    

import os
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)