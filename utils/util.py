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
MCHID = '1491830732'
KEY = ''
NOTIFY_URL = ''

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
        # print(type(primary_key))
        # print(primary_key)
        user = User.objects.get(id=primary_key) # 通过openid获取user
        # print(type(user))
        #print(user)
        return user
    except ExpiredSignatureError:
        return False

def create_dir_according_time():
    localtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    #print('localtime='+localtime)
    # 系统当前时间年份
    year=time.strftime('%Y',time.localtime(time.time()))
    # 月份
    month=time.strftime('%m',time.localtime(time.time()))
    # 日期
    # day=time.strftime('%d',time.localtime(time.time()))
    #具体时间 小时分钟毫秒
    mdhms = time.strftime('%m%d%H%M%S',time.localtime(time.time()))
    #print(os.getcwd())
    fileYear = os.getcwd()+'/uploadfile'+'/'+year
    #print('fileyear'+fileYear)
    fileMonth = fileYear+'/'+month
    #print('filemonth'+fileMonth)
    fileCertification = fileMonth+'/'+'certification'
    # fileDay=fileMonth+'/'+day
    if not os.path.exists(fileYear):
        print('1')
        os.mkdir(fileYear)
        os.mkdir(fileMonth)
        os.mkdir(fileCertification)
        # os.mkdir(fileDay)
    else:
      if not os.path.exists(fileMonth):
        print('2')
        os.mkdir(fileMonth)
        os.mkdir(fileCertification)
    return fileMonth