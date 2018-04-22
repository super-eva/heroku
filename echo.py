from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('avIDjwy7hrp4tlLjEbnOTTT2XF5jhApx96zUN2sRDtLl5w5u1PZ+iJ5FXCDX53Mu9vEpg7Eq0eV3Pl8m4v5MnD8P4TKjjlOClf/VVShXzEqtJsspCDpOMNehiOyJePPRXlhpyEibfoX/b5zu8a3k8gdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('9f530fcd5e1273891a2541d873387272')

@app.route("/callback")
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()