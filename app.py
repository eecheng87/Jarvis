import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message


# from dotenv import load_dotenv
load_dotenv()


machine = TocMachine(
    states=["idle", "active", "ptt","baseball","bchoose","weather","degree","train",
            "train_result","beauty","popular","next","np","show_fsm"],
    transitions=[
        {"trigger": "advance","source": "idle","dest": "active","conditions": "is_going_to_active"},
        {"trigger": "advance","source": "active","dest": "ptt","conditions": "is_going_to_ptt"},
        {"trigger": "advance","source": "ptt","dest": "baseball","conditions": "is_going_to_baseball"},
        {"trigger": "advance","source": "baseball","dest":"bchoose","conditions":"is_going_to_bchoose"},
        {"trigger": "advance","source": "active","dest": "weather","conditions": "is_going_to_weather"},
        {"trigger": "advance","source": "weather","dest": "degree","conditions": "is_going_to_degree"},
        {"trigger": "advance","source": "active","dest": "train","conditions": "is_going_to_train"},
        {"trigger": "advance","source": "train","dest": "train_result","conditions": "is_going_to_train_result"},
        {"trigger": "advance","source": "ptt","dest": "beauty","conditions": "is_going_to_beauty"},
        {"trigger": "advance","source": "beauty","dest": "popular","conditions": "is_going_to_popular"},
        {"trigger": "advance","source": "popular","dest": "next","conditions": "is_going_to_next"},
        {"trigger": "advance","source": "next","dest": "popular","conditions": "is_going_to_popular"},
        {"trigger": "advance","source": "popular","dest": "np","conditions": "is_going_to_np"},
        {"trigger": "advance","source": "np","dest": "popular","conditions": "is_going_to_popular"},
        {"trigger": "advance","source": "idle","dest": "show_fsm","conditions": "is_going_to_show_fsm"},
        {"trigger": "prev","source": "ptt","dest": "active"},
        {"trigger": "prev","source": "baseball","dest": "ptt"},
       # {"trigger": "prev","source": "bchoose","dest": "active"},
        {"trigger": "prev","source": "weather","dest": "active"},
        #{"trigger": "prev","source": "degree","dest": "weather"},
        #{"trigger": "prev","source": "train_result","dest": "train"},
        #{"trigger": "prev","source": "bchoose","dest": "baseball"},
        #{"trigger": "prev","source": "popular","dest": "beauty"},
        {"trigger": "prev","source": "beauty","dest": "ptt"},
        {"trigger": "prev","source": "train","dest": "active"},
        {"trigger": "go_back","source": ["train_result","degree","bchoose","show_fsm"],"dest":"idle"},
        {"trigger": "sleep", "source": ["active", "ptt","baseball","weather","train",
            "beauty","popular","next","np"], "dest": "idle"},
    ],
    initial="idle",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
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

        #line_bot_api.reply_message(
        #    event.reply_token, TextSendMessage(text=event.message.text)
        #)
        #rec_url = get_recommend_link(2)
        #line_bot_api.reply_message(
        #    event.reply_token, TextSendMessage(text=rec_url)
        #)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )


    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    #line_bot_api.reply_message(reply_token, 'hello!!')
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

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
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        if event.message.text.lower() == "prev":
            machine.prev(event)
            response = True
        elif event.message.text.lower() == "sleep":
            machine.sleep(event)
            response = True
        else:
            response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, "Not Entering any State")
    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    #show_fsm()
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)