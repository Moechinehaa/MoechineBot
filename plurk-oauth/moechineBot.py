#!/usr/bin/python
# -*- coding:utf-8 -*-
 
import re
import json
import urllib.request as urllib2
import random
 
from plurk_oauth import PlurkAPI

random_list = ["掰噗[emo1]",
                "花生厚片 熱狗 中涼奶",
                "早安早安!祝大家有美好的一天~(heart)",
                "有人知道美人魚為什麼這麼專情嗎B-)",
                "為什麼沒聽過中涼奶阿(annoyed)",
                "感謝我媽媽把我生得這麼帥:-))",
                "其實我是土星周子翔:-p",
                "你也氣噗噗嗎...",
                "我只能虛心接受了",
                "我才不是寶寶(angey)",
                "巴拉巴拉巴拉噗噗噗噗嚕嚕噗嚕噗噗噗(ooxx)",
                "粉絲福利就是 請你們快點睡覺"]

def plurkResponse(pid,content):
    plurk.callAPI('/APP/Responses/responseAdd',
                              {'plurk_id': pid,
                               'content': content,
                               'qualifier': ':' })

def dealContent(pid,content):
    if content.find("李老闆") != -1:
        plurkResponse(pid,'傻:)')
    elif content.find("周小葵") != -1:
        plurkResponse(pid,'你在叫我嗎~(flower)')
    elif content.find("老婆") != -1:
        plurkResponse(pid,"我也喜歡你鴨(heart)")
    elif content.find("喜歡") != -1:
        plurkResponse(pid,"我不要(p-blush)")
    else:
        con = random.choice(random_list)
        plurkResponse(pid, con)
 
plurk = PlurkAPI('', '')
plurk.authorize('', '')
 
comet = plurk.callAPI('/APP/Realtime/getUserChannel')
comet_channel = comet.get('comet_server') + "&new_offset=%d"
jsonp_re = re.compile('CometChannel.scriptCallback\((.+)\);\s*');
new_offset = -1
while True:
    plurk.callAPI('/APP/Alerts/addAllAsFriends') #Accept all friendship requests as friends.
    req = urllib2.urlopen(comet_channel % new_offset, timeout=80)
    rawdata = req.read().decode('utf-8')
    match = jsonp_re.match(rawdata)
    if match:
        rawdata = match.group(1)
    data = json.loads(rawdata)
    new_offset = data.get('new_offset', -1)
    msgs = data.get('data')
    #dealMentioned()

    if not msgs:
        continue
    for msg in msgs:
        if msg.get('type') == 'new_plurk':
            #print(msg)
            pid = msg.get('plurk_id')
            content = msg.get('content_raw')
            if content.find("慎入") != -1:
                print("qq")
            else:
                dealContent(pid,content)