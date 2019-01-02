# -*- coding: UTF-8 -*-
import hashlib
import json
import time
from urllib.parse import urlencode

import requests

URL = "http://ltpapi.xfyun.cn/v1/"


def getHeader(appid, apikey):
    curTime = str(int(time.time()))
    paramBase64 = 'ew0KICAgICJ0eXBlIjogImRlcGVuZGVudCINCn0='
    m2 = hashlib.md5()
    m2.update((apikey + curTime + paramBase64).encode(encoding='UTF-8'))
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': appid,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def get_header(app_id, api_key):
    curTime = str(int(time.time()))
    paramBase64 = 'ew0KICAgICJ0eXBlIjogImRlcGVuZGVudCINCn0='
    m2 = hashlib.md5()
    m2.update((api_key + curTime + paramBase64).encode(encoding='UTF-8'))
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': app_id,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


# 讯飞自然语言处理接口 调用
def xunfei_api(text, type, appid, apikey):
    '''
    APPID = "5c1234b7"
    中文分词(cws)
    词性标注(pos)
    命名实体识别(ner)
    依存句法分析(dp)
    语义角色标注(srl)
    语义依存 (依存树) 分析(sdp)
    语义依存 (依存图) 分析(sdgp)
    :param text:  需要调用接口处理的文本
    :param type:  处理的类型  cws,pos,ner,dp,srl,sdp,sdgp
    :return: 讯飞接口调用返回的结果，已经转为 json 对象
    '''
    body = urlencode({'text': text})
    r = requests.post(URL + type, headers=getHeader(appid, apikey), data=body)
    result = json.loads(r.content)
    return result
