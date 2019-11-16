from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
import requests
from jwt import ExpiredSignatureError
from user.models import User
import jwt
import os
import time

APPID = 'wx6ac3ca8cc6189b5b'
APP_SECRET = 'bde0c35566a000030b78d99dbf08bbbe'
MCHID = '1491830732'
KEY = 'WUCHUANTONGCHENGWANGsR10280923sR'
NOTIFY_URL = 'http://www.luckydraw.net.cn/certification/get_pay_info'

#消息推送中的变量设置
url = 'https://www.luckydraw.net.cn/user/customerService'
token = 'gDcIOy2NHXrqTRY6C93Lhm7lWMEGoJiQ'
EncodingAESKey = '3E16LhGIlRbrjVx3qBikgljG15IKBxXbOomlwIXWiAV'




def get_user(obj):
    # print(obj)
    # print(type(obj))
    token = obj['token']
    secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'
    EncryptedString = token
    print(type(EncryptedString))
    print("EncryptedString:")
    print(EncryptedString)
    try:
        EncryptedString = jwt.decode(token, secret, issuer='cyb', algorithms=['HS256'])  # 解密，校验签名
        # print(type(EncryptedString))
        # print(EncryptedString)
        primary_key = (EncryptedString['data'])['id']
        print('primary_key')
        print(primary_key)
        # print(type(primary_key))
        # print(primary_key)
        user = User.objects.get(id=primary_key) # 通过openid获取user
        # print(type(user))
        #print(user)
        return user
    except ExpiredSignatureError:
        return False