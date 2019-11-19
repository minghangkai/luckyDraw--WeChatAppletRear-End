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

#七牛云key
AccessKey = '3QeKd51jEBv62Wvxn8QPSkRBdVCm1nT1XdwAF4Zi'
SecretKey = '115kaklqgLgmISwzrHHgOIBDYb_fYH2Kp1Ff7JFN'
policy = {  # 七牛云上传策略——https://developer.qiniu.com/kodo/manual/1206/put-policy
    'callbackUrl': 'get_qiniu_info',  # 回调URL 上传成功后，七牛云向业务服务器发送 POST 请求的 URL。
    'callbackHost': 'www.luckydraw.net.cn',  # 回调URL指定的Host 上传成功后，七牛云向业务服务器发送回调通知时的 Host 值。与 callbackUrl 配合使用，仅当设置了 callbackUrl 时才有效。
    'callbackBodyType': 'application/json',  # 回调Body的Content-Type 上传成功后，七牛云向业务服务器发送回调通知 callbackBody 的 Content-Type。默认为 application/x-www-form-urlencoded，也可设置为 application/json。
    "mimeLimit": 'image/*',  # 只允许上传图片类型
    }

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