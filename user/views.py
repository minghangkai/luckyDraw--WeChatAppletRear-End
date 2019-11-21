import hashlib

import xmltodict
from django.http import HttpResponse, JsonResponse
import json
import requests
from jwt import ExpiredSignatureError
from user.models import User
import jwt
import datetime
import time
from utils.util import get_user, APPID, APP_SECRET
from utils.get_phone_number import WXBizDataCrypt



def get_openid_session_key(request): # 获取openid和session_key，创建用户数据，并返回加密token给前端
    appid = APPID
    app_secret = APP_SECRET
    primary_key_id = 0  # 记录用户主键
    js_code = json.loads(request.body) # js_code为dict = {'code': '……'}
    """print(request.POST)
    print(type(request.POST))
    js_code = str(request.body)[2:-1] # request.body为b'code'，类型为bytes，故将其转为string且用字符串方法去掉b''"""
    #js_code = request.GET.get('code')  # get方法
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + app_secret + '&js_code=' + \
          js_code['code'] + '&grant_type=authorization_code'
    r = requests.get(url)
    print(r.json())
    OpenId = r.json()['openid']
    session_key = r.json()['session_key']
    print("OpenId: " + OpenId)
    print("session_key: " + session_key)
    print(len(session_key))
    try:
        user = User.objects.get(OpenId=OpenId)
    except Exception as e:
        user = None
    if user:
        primary_key_id = user.id
        print('数据库中有该用户\n')
    else:
        print('注册新用户\n')
        user = User(OpenId=OpenId)
        user.save()
        primary_key_id = user.id  # 主键
    secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'
    print('primary_key_id')
    print(primary_key_id)
    dic = {
        'exp': datetime.datetime.now() + datetime.timedelta(hours=3),  # 过期时间
        'iat': datetime.datetime.now(),  # 开始时间
        'iss': 'cyb',  # 签名
        'data': {  # 内容，一般存放该用户id和开始时间
            'id': primary_key_id,
            'OpenId': OpenId,
        },
    } # 由此生成的token将由用户保存，不存入数据库。用户传回服务端后，解析出整数型主键id（用以检索，速度比检索openid快）

    encrypted_string = jwt.encode(dic, secret, algorithm='HS256')
    print('encrypted_string:')
    print(type(encrypted_string))
    print(encrypted_string)
    # jwt.encode为加密生成字节流,为b'code'，类型为bytes，故将其转为string且用字符串方法去掉b'
    print('get_openid_session_key运行结束\n')
    dicIncludeTokenAndUserid = {
        'token': str(encrypted_string, encoding='utf8'),  # encrypted_string为bytes类型，需转为字符串才能通过jsonResponse传输
        'user_id': primary_key_id,                        # 若直接把字节型的encrypted_string通过HttpResponse传给前端，前端会自动转为字符串
    }
    print('返回dicIncludeTokenAndUserid')
    return JsonResponse(dicIncludeTokenAndUserid, safe=False)
    #return HttpResponse(encrypted_string)


def check_token(request):
    secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'
    encrypted_string = json.loads(request.body)
    print('encrypted_string of check_token:')
    print(encrypted_string)
    print(type(encrypted_string))
    print('check_token开始运行\n')
    try:
        decrypt_string = jwt.decode(encrypted_string['token'], secret, issuer='cyb', algorithms=['HS256'])  # 解密，校验签名
        #print(type(decrypt_string))
        #print(decrypt_string)
        print('check_token运行结束，返回true\n')
        return HttpResponse('true')  # 没过期
    except ExpiredSignatureError:
        print('check_token运行结束，返回false\n')
        return HttpResponse('false')  # 过期，令前端重新调用函数get_openid_session_key
    except jwt.exceptions.DecodeError:
        print('check_token运行结束，返回false\n')
        return HttpResponse('false')  # 过期，令前端重新调用函数get_openid_session_key
    """endTime = time.localtime(decrypt_string['exp'])
    now = time.localtime(datetime.datetime.now())"""



def get_user_info(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    if not user:
        return HttpResponse('false')  # token过期
    else:
        user.UserName = obj['nickName']
        user.AvatarUrl = obj['avatarUrl']
        user.city = obj['city']
        user.country = obj['country']
        user.gender = obj['gender']
        user.language = obj['language']
        user.province = obj['province']
        user.save()
        return HttpResponse('true')

def storage_address(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    if not user:
        return HttpResponse('false')  # token过期
    else:
        user.ContactName = obj['participantName']
        user.PhoneNumber = obj['participantPhoneNumber']
        user.address = obj['participantAddress']
        user.save()
        return HttpResponse('true')

def return_user_luckyDraw_info(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    data = {'CreateActivityNum': user.CreateActivityNum,
            'ParticipateActivityNum': user.ParticipateActivityNum,
            'WinNum': user.WinNum}

    return JsonResponse(data)


def get_user_phone_number(request):
    obj = json.loads(request.body)
    encryptedData = obj['encryptedData']
    iv = obj['iv']
    appid = APPID
    app_secret = APP_SECRET
    js_code = json.loads(request.body)  # js_code为dict = {'code': '……'}
    """print(request.POST)
    print(type(request.POST))
    js_code = str(request.body)[2:-1] # request.body为b'code'，类型为bytes，故将其转为string且用字符串方法去掉b''"""
    # js_code = request.GET.get('code')  # get方法
    print('code: ' + js_code['code'])
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + app_secret + '&js_code=' + \
          js_code['code'] + '&grant_type=authorization_code'
    r = requests.get(url)
    print(r.json())
    OpenId = r.json()['openid']
    session_key = r.json()['session_key']
    pc = WXBizDataCrypt(appid, session_key)#wx_jm(appid, session_key)
    res = pc.decrypt(encryptedData, iv)
    return JsonResponse(res)


def customerService(request):
    signature = request.GET["signature"]
    print('signature:')
    print(signature)
    timestamp = request.GET["timestamp"]
    print('timestamp')
    print(timestamp)
    nonce = request.GET["nonce"]
    print('nonce')
    print(nonce)
    echostr = request.GET['echostr']
    print('echostr')
    print(echostr)
    token = 'gDcIOy2NHXrqTRY6C93Lhm7lWMEGoJiQ'
    param = {
        'token': token,
        'timestamp': timestamp,
        'nonce': nonce,
    }
    ks = sorted(param.keys())
    stringA = ''
    for k in ks:
        stringA += str(param[k])
    print('stringA')
    print(stringA)
    tmp_signature = hashlib.sha1(stringA.encode('utf-8')).hexdigest()
    print('tmp_signature')
    print(tmp_signature)
    if tmp_signature == signature:
        print('tmp_signature == signature')
        return HttpResponse(echostr)
        #return JsonResponse(data, safe=False)
    else:
        print('tmp_signature != signature')
        return HttpResponse(echostr)
        #return JsonResponse(data,safe=False)
