import time
import os
from datetime import datetime
import pytz
from collections import defaultdict
import json
import struct
import re
import sys

from function.detect import HumanDetect, ConfirmDetect
from function.display import OLED
from function.chatbot import ChatBot
from function.record import record
from function.receipt import receiptRun
from speech.chinese_stt import chinese_recognize
from speech.chinese_tts import TTSClient

if __name__ == '__main__':
    # 設定時區
    twZone = pytz.timezone('Asia/Taipei')
    timeHour = datetime.now(twZone).hour
    # 載入全部餐點價格
    with open("./files/menu.json", "r", encoding="utf-8") as f:
        menu = json.load(f)
    # 語言 & 聊天機器人初始化
    ttsClient = TTSClient()
    ttsClient.set_language("chinese", "male")
    chatbot = ChatBot(0.3)
    # 人體偵測 => 開始程式主體
    humanDetect = HumanDetect(26)
    humanDetect.setDetect()
    while not humanDetect.isActive():
        time.sleep(1)
    os.system('aplay ./files/hello.wav')
    time.sleep(1)
    # 根據不一樣的時間輸出對應的問候
    if timeHour < 11:
        os.system('aplay ./files/morning.wav')
    elif timeHour >= 17:
        os.system('aplay ./files/night.wav')
    else:
        os.system('aplay ./files/noon.wav')
    orderList = defaultdict(int)
    # 開始錄音直到 "這樣就好"
    while True:
        record()
        question = chinese_recognize('./files/question.wav')
        result = chatbot.ask(question)
        if result["reply"] is None:
            break
        if result["alter"] == 1:
            if len(result["order"]) == 0:
                result["reply"] = "沒有這份餐點"
            else:
                orderList[result["order"]] += result["number"]
        elif result["alter"] == -1:
            if len(result["order"]) == 0:
                result["reply"] = "沒有這份餐點"
            else:
                orderList[result["order"]] -= result["number"]
        elif result["alter"] == 2:
            if len(result["order"]) == 0:
                result["reply"] = "沒有這份餐點"
            else:
                orderList[result["order"][0]] -= 1
                orderList[result["order"][1]] += 1
        ttsClient.askForService(result["reply"])
        os.system('aplay ./files/reply.wav')

    ttsClient.askForService("請確認餐點是否正確")
    os.system('aplay ./files/reply.wav')
    text = []
    for order, count in orderList.items():
        if count != 0:
            text.append(order + "  " + str(count) + "份")
    confirmDetect = ConfirmDetect(5, 6)
    oled = OLED(10)
    while True:
        dist = confirmDetect.distance()
        oled.display_text(text)
        if dist <= 5:
            break
    total = 0
    for order, count in orderList.items():
        total += (int(menu[order])*count)

    ttsClient.askForService("請確認金額，並投入零錢")
    os.system('aplay ./files/reply.wav')

    oled.setFontSize(15)
    text = ["總金額:  $" + str(total) + "元"]
    while True:
        dist = confirmDetect.distance()
        oled.display_text(text)
        if dist <= 5:
            break

    ttsClient.askForService("祝您用餐愉快")
    os.system('aplay ./files/reply.wav')
    confirmDetect.end()
    oled.clear()
    receiptRun()
