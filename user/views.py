from django.http import HttpResponse, JsonResponse
import json
import requests
from jwt import ExpiredSignatureError
from user.models import User
import jwt
import datetime,time
from utils.util import get_user



def get_openid_session_key(request): # 获取openid和session_key，创建用户数据，并返回加密token给前端
    appid = 'wxd5230cfaaa6e5d93'
    app_secret = '8601382f45e82ca2188d50afabd69771'
    primary_key_id = 0 # 记录用户主键
    js_code = json.loads(request.body) # js_code为dict = {'code': '……'}
    """print(request.POST)
    print(type(request.POST))
    js_code = str(request.body)[2:-1] # request.body为b'code'，类型为bytes，故将其转为string且用字符串方法去掉b''"""
    #js_code = request.GET.get('code')  # get方法
    print('code: ' + js_code['code'])
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + app_secret + '&js_code=' + js_code['code'] + '&grant_type=authorization_code'
    r = requests.get(url)
    print(r.json())
    OpenId = r.json()['openid']
    session_key = r.json()['session_key']
    print("OpenId: " + OpenId)
    print("session_key: " + session_key)
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
            #'session_key': session_key,
        },
    } # 由此生成的token将由用户保存，不存入数据库。用户传回服务端后，解析出整数型主键id（用以检索，速度比检索openid快）

    encrypted_string = jwt.encode(dic, secret, algorithm='HS256')
    # jwt.encode为加密生成字节流,为b'code'，类型为bytes，故将其转为string且用字符串方法去掉b'
    """#s = jwt.decode(s, secret, issuer='cyb', algorithms=['HS256'])  # 解密，校验签名
    #print(s)"""
    print(encrypted_string)
    print('get_openid_session_key运行结束\n')
    return HttpResponse(encrypted_string)


def check_token(request):
    secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'
    encrypted_string = json.loads(request.body)
    print('check_token开始运行\n')
    print(type(encrypted_string))
    print("encrypted_string:")
    print(encrypted_string)
    try:
        decrypt_string = jwt.decode(encrypted_string['token'], secret, issuer='cyb', algorithms=['HS256'])  # 解密，校验签名
        print(type(decrypt_string))
        print(decrypt_string)
        print('check_token运行结束，返回true\n')
        return HttpResponse('true')  # 没过期
    except ExpiredSignatureError:
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