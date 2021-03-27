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

line_bot_api = LineBotApi('PCHw0UUEjHa52OD68zeyvgRu40P09cdk3hnVM/C+hZhBfJ5ePleFn6mzd235F4Lc1eYw9RC0D7Mytcr9GuK+kENvSILqNs5+BTw44HltSRShX1NO4KhNoZuQ7Gelm2wJxUG1q2bY0pfKJq5omVl6aAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ec9e6c143178072751ebc6f44922f4a4')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()