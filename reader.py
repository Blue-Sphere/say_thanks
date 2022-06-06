import json

def get_key_LineBotApi():
    with open("files/security.json","r",encoding="utf-8") as file:
        return json.load(file)["line_bot_api"]

def get_key_handler():
    with open("files/security.json","r",encoding="utf-8") as file:
        return json.load(file)["handler"]

def get_key_Deta_key():
    with open("files/security.json","r",encoding="utf-8") as file:
        return json.load(file)["Deta_key"]