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
import os
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)

line_bot_api = LineBotApi('avIDjwy7hrp4tlLjEbnOTTT2XF5jhApx96zUN2sRDtLl5w5u1PZ+iJ5FXCDX53Mu9vEpg7Eq0eV3Pl8m4v5MnD8P4TKjjlOClf/VVShXzEqtJsspCDpOMNehiOyJePPRXlhpyEibfoX/b5zu8a3k8gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9f530fcd5e1273891a2541d873387272')
url = 'http://cdcb.judicial.gov.tw/abbs/wkw/WHD9A02.jsp'

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
def handle_message(event):
    id = event.message.text

    res = requests.post(url,headers={'Content-Type':'application/x-www-form-urlencoded'},data='idno='+id)
    res.encoding = 'big5' #轉換enconding, 預設為utf8
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.findAll('table')[1].findAll('td', {'class':'trB'})
    if len(data) > 2 :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='Has data'))
    else :
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='No data'))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )