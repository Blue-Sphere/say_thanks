from deta import Deta
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone, timedelta

#--

import reader

#--

DETA_KEY = reader.get_key_Deta_key()

#--

#score_1~5 -> 珍惜當下, 知足惜福, 逆境感恩, 感謝他人, 感謝恩典
class User_info(BaseModel):
    name: str
    score_1: int
    score_2: int
    score_3: int
    score_4: int
    score_5: int

def user_already_exist(user_id: str):
    deta = Deta(DETA_KEY)
    db = deta.Base("say_thanks")
    return db.fetch({"key":user_id}).count > 0

def register(user_id: str, username: str):
    try:
        deta = Deta(DETA_KEY)
        db = deta.Base("say_thanks")
        db.put({"name":username,"珍惜當下":0,"知足惜福":0,"逆境感恩":0,"感謝他人":0,"感謝恩典":0,"allow_to_get_point_status":False,"temp":None},user_id)
        return f"{username} 註冊成功！"
    except:
        return "註冊失敗"

def change_get_point_status(user_id: str, open: bool):
    deta = Deta(DETA_KEY)
    db = deta.Base("say_thanks")
    db.update({"allow_to_get_point_status":open}, user_id)

def check_allow_to_get_point_status(user_id: str):
    deta = Deta(DETA_KEY)
    db = deta.Base("say_thanks")
    return db.get(user_id)["allow_to_get_point_status"]

def get_point(user_id: str, aim: int):
    get_point_string = ("珍惜當下", "知足惜福", "逆境感恩", "感謝他人", "感謝恩典")
    deta = Deta(DETA_KEY)
    db = deta.Base("say_thanks")
    db.update({get_point_string[aim]: db.util.increment()}, user_id)

def write_message_in_temp(user_id: str, message: str):
    deta = Deta(DETA_KEY)
    db = deta.Base("say_thanks")
    db.update({"temp":message}, user_id)

def load_message_temp(user_id: str):
    deta = Deta(DETA_KEY)
    db = deta.Base("say_thanks")
    return db.get(user_id)["temp"]

def get_point_message_detail(user_id: str, aim: int):
    get_point_string = ("珍惜當下", "知足惜福", "逆境感恩", "感謝他人", "感謝恩典")
    message_from_temp = load_message_temp(user_id)
    dt1 = datetime.utcnow().replace(tzinfo=timezone.utc)
    dt2 = dt1.astimezone(timezone(timedelta(hours=8)))
    time_formated = dt2.strftime("%Y-%m-%d %H:%M:%S")
    return f"{time_formated}\n內容：{message_from_temp}\n「{get_point_string[aim]}」分數+1"

def get_user_info(user_id):
    deta = Deta(DETA_KEY)
    db = deta.Base("say_thanks")
    result = db.get(user_id)
    user_info = User_info(
        name= result["name"],
        score_1= result["珍惜當下"],
        score_2= result["知足惜福"],
        score_3= result["逆境感恩"],
        score_4= result["感謝他人"],
        score_5= result["感謝恩典"]
    )
    return user_info

def rename(user_id, new_name):
    deta = Deta(DETA_KEY)
    db = deta.Base("say_thanks")
    db.update({"name":new_name}, user_id)