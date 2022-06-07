from fastapi import FastAPI, Request, Header, HTTPException

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage, emojis, flex_message, Emojis
)
#--

import sql_function

import flex_message_function

import reader

#--

LINE_BOT_API = reader.get_key_LineBotApi()
HANDLER = reader.get_key_handler()

#--

line_bot_api = LineBotApi(LINE_BOT_API)
handler = WebhookHandler(HANDLER)

app = FastAPI()

@app.post("/line")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    try:
        handler.handle(body.decode("utf-8"), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="handle body error.")
    return 'OK'

@handler.add(MessageEvent ,message=TextMessage)
def message_text(event):
    user_id = event.source.user_id
    reply_token = event.reply_token
    message = event.message.text
    get_point_string = ("+珍惜當下", "+知足惜福", "+逆境感恩", "+感謝他人", "+感謝恩典")
    try:
        if sql_function.user_already_exist(user_id) == True:
            if message not in get_point_string:
                if message == "/info":
                    user_info = sql_function.get_user_info(user_id)
                    line_bot_api.reply_message(reply_token,TextSendMessage(f"嗨 {user_info.name} ！\n以下是你各感恩類型的分數\n————\n珍惜當下：{user_info.score_1}\n知足惜福：{user_info.score_2}\n逆境感恩：{user_info.score_3}\n感謝他人：{user_info.score_4}\n感謝恩典：{user_info.score_5}"))
                elif message == "/introduce":
                    flex_message = flex_message_function.thanks_type_template_flexMessage()
                    replay_array = []
                    replay_array.append(TextSendMessage("嗨您好！我是此LineBot的開發人員！\n以下為此LineBot的開源程式碼。\n————\n除了某些安全問題的密鑰，其餘都以上傳至GitHub：https://github.com/Blue-Sphere/say_thanks"))
                    replay_array.append(TextSendMessage("這個聊天室主要是透過輸入相對訊息而執行後端的程式，其目的是為讓使用者更好的紀錄每日所感恩的事情，只要直接在訊息中輸入今天所感謝的事情後再選擇其中相對應的五大感恩類型，系統就可以為您紀錄專屬您的各項感恩類型總分，以下為方式與成效。"))
                    replay_array.append(TextSendMessage("方式：每天紀錄三件感恩的事\n成效：持續2週可以提升感恩、幸福感、樂觀"))
                    replay_array.append(TextSendMessage("以下為五大感恩類型的簡介，輸入感恩的內容後請記得選取相對應的感恩類型，系統才會為您加分喔！"))
                    replay_array.append(FlexSendMessage(alt_text="五大感恩類型介紹", contents=flex_message))
                    line_bot_api.reply_message(reply_token, replay_array)
                elif message == "/?":
                    replay_array = []
                    replay_array.append(TextSendMessage("嗨您好！我是此LineBot的開發人員！"))
                    replay_array.append(TextSendMessage("直接輸入感謝的文字內容就可以觸發「五大類型的選擇版」，選擇後即可為對應的項目加分！"))
                    replay_array.append(TextSendMessage("以下為各種指令之用途，可以透過輸入或點擊面板來觸發"))
                    replay_array.append(TextSendMessage("/info\n透過這個指令來查看自己各感恩類型的得分，可以透過輸入與點擊面板中的「個人資訊」觸發！\n\n/introduce\n透過這個指令來查看此LineBot的簡單介紹與如何實施感恩細數，可以透過輸入與點擊面板中的「簡單介紹」觸發！\n\n/?\n透過這個指令來查看各種指令的運用與詳細的資訊，可以透過輸入與點擊面板中的「如何使用」觸發！\n\n/rename [新姓名]\n透過這個指令來改變系統對您的稱謂，只能透過輸入觸發！"))
                    replay_array.append(TextSendMessage("以上！感謝您的查詢，若傳輸的訊息並非以上的指令或加分用的系統保留字時，將一律視為使用者輸入的「感恩內容」，若輸入錯內容再重新輸入即可！"))
                    line_bot_api.reply_message(reply_token, replay_array)
                elif message.startswith("/rename "):
                    new_name = message.replace("/rename ","")
                    sql_function.rename(user_id, new_name)
                    line_bot_api.reply_message(reply_token,TextSendMessage(f"已成功改名為「{new_name}」！"))
                else:
                    sql_function.change_get_point_status(user_id, True)
                    sql_function.write_message_in_temp(user_id, message)
                    flex_message = flex_message_function.get_point_template_flexMassage()
                    replay_array = []
                    replay_array.append(FlexSendMessage(alt_text="加分選擇版", contents=flex_message))
                    replay_array.append(TextSendMessage(f"請為您所輸入的「{message}」感恩內容，選擇屬於此內容的感謝類型"))
                    line_bot_api.reply_message(reply_token, replay_array)
            else:
                if sql_function.check_allow_to_get_point_status(user_id) == True:
                    aim = get_point_string.index(message)
                    sql_function.get_point(user_id, aim)
                    access_message = sql_function.get_point_message_detail(user_id, aim)
                    sql_function.change_get_point_status(user_id, False)
                    line_bot_api.reply_message(reply_token,TextSendMessage(access_message))
                line_bot_api.reply_message(reply_token,TextSendMessage("請先輸入感恩的內容才能選擇喔！"))
        else:
            if message.startswith("/register "):
                username = message.replace("/register ","")
                return_message = sql_function.register(user_id, username)
                line_bot_api.reply_message(reply_token, TextSendMessage(return_message))
            else:
                line_bot_api.reply_message(reply_token, TextSendMessage("尚未有您的帳號資料，請透過輸入指令「/register [姓名/別名]」來註冊，如/register Sphere"))
    except:
        line_bot_api.reply_message(reply_token, TextSendMessage("目前系統出現問題，請稍後再嘗試！"))
