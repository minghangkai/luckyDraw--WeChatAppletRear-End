from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
import requests
from jwt import ExpiredSignatureError
from luckyDraw_1.models import User,Activity,Certification,Prize
import jwt
import datetime,time


# Create your views here.

def get_user(obj):
    print(obj)
    print(type(obj))
    token = obj['token']
    secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'
    encryptedString = token
    print(type(encryptedString))
    print("encryptedString:")
    print(encryptedString)
    try:
        decryptString = jwt.decode(token, secret, issuer='cyb', algorithms=['HS256'])  # 解密，校验签名
        print(type(decryptString))
        print(decryptString)
        primary_key = (decryptString['data'])['id']
        print(type(primary_key))
        print(primary_key)
        user = User.objects.get(id=primary_key) # 通过openid获取user
        print(type(user))
        print(user)
        return user
    except ExpiredSignatureError:
        return False


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
    openid = r.json()['openid']
    session_key = r.json()['session_key']
    print("openid: " + openid)
    print("session_key: " + session_key)
    try:
        user = User.objects.get(openid=openid)
    except Exception as e:
        user = None
    if user:
        primary_key_id = user.id
    else:
        # 注册新用户
        user = User(openid=openid)
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
            'openid': openid,
            #'session_key': session_key,
        },
    } # 由此生成的token将由用户保存，不存入数据库。用户传回服务端后，解析出整数型主键id（用以检索，速度比检索openid快）

    encryptedString = jwt.encode(dic, secret, algorithm='HS256')
    # jwt.encode为加密生成字节流,为b'code'，类型为bytes，故将其转为string且用字符串方法去掉b'
    """#s = jwt.decode(s, secret, issuer='cyb', algorithms=['HS256'])  # 解密，校验签名
    #print(s)"""
    print(encryptedString)
    return HttpResponse(encryptedString)


def check_token(request):
    secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'
    encryptedString = json.loads(request.body)
    print(type(encryptedString))
    print("encryptedString:")
    print(encryptedString)
    try:
        decryptString = jwt.decode(encryptedString['token'], secret, issuer='cyb', algorithms=['HS256'])  # 解密，校验签名
        print(type(decryptString))
        print(decryptString)
        return HttpResponse('true')  # 没过期
    except ExpiredSignatureError:
        return HttpResponse('false')  # 过期，令前端重新调用函数get_openid_session_key
    """endTime = time.localtime(decryptString['exp'])
    now = time.localtime(datetime.datetime.now())"""



def get_user_info(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    if not user:
        return HttpResponse('false')  # token过期
    else:
        user.username = obj['nickName']
        user.avatarUrl = obj['avatarUrl']
        user.city = obj['city']
        user.country = obj['country']
        user.gender = obj['gender']
        user.language = obj['language']
        user.province = obj['province']
        user.save()
        return HttpResponse('true')

def storage_address(request):
    obj = json.loads(request.body)
    print(type(obj))
    print(obj)
    user = get_user(obj)
    if not user:
        return HttpResponse('false')  # token过期
    else:
        user.contactName = obj['participantName']
        user.phoneNumber = obj['participantPhoneNumber']
        user.address = obj['participantAddress']
        user.save()
        return HttpResponse('hello')

def get_activity_info(request):
    obj = json.loads(request.body)
    print(type(obj))
    print(obj)
    user = get_user(obj)
    if not user:
        return HttpResponse('false')  # token过期
    else:
        newBy = obj['newBy']
        phoneNum = obj['phoneNum']
        activityName = obj['activityName']
        activityDetails = json.dumps(obj['infoOfActivity'])
        conditionObject = obj['conditionObject']
        if conditionObject[id] == 0:
            endTime = datetime.datetime.strptime(conditionObject['info'], "%Y-%m-%d %H:%M:%S")
            conditionInfo = None
        elif conditionObject[id] == 1:
            endTime = None
            conditionInfo = conditionObject['info']
        elif conditionObject[id] == 2:
            endTime = None
            conditionInfo = None
        activity = Activity(sponsor=user, certificateOrNot=user.certificate, sponsorWay=newBy, phoneNum=phoneNum, activityName=activityName,
                            endTime=endTime, activityDetails=activityDetails, conditionType=conditionObject[id], conditionInfo=conditionInfo)
        # activity.save()
        if newBy == 1:
            activity.participantAttention = obj['participantAttention']
            activity.inviateFriends = obj['inviateFriends']
            activity.save()
        elif newBy == 2:
            activity. = obj['']
            activity. = obj['']
            activity. = obj['']
            activity. = obj['']
            activity. = obj['']
            activity. = obj['']
        elif newBy == 3:
            activity. = obj['']
            activity. = obj['']
            activity. = obj['']
            activity. = obj['']
            activity. = obj['']
            activity. = obj['']
            activity. = obj['']
        elif newBy == 4:



        return HttpResponse({'activityUrl': activity_url,
                             })

def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("fileName", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        else:
            # 打开特定的文件进行二进制的写操作
            # print(os.path.exists('/temp_file/'))
            with open("./luckyDraw_1/static/luckyDraw_1/static/%s" % myFile.name, 'wb+') as f:
                # 分块写入文件
                for chunk in myFile.chunks():
                    f.write(chunk)
            return HttpResponse("UPload over!")
    else:
        return HttpResponse("没有监听到POST请求")
#         var filesrc = util.fileUpload('luckyDraw_1/upload_file', res.tempFilePaths[0], 'fileName') 前端请求

"""def upload_file(request):
    # 请求方法为POST时，进行处理
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，则默认为None

        if File is None:
            return HttpResponse("没有需要上传的文件")
        else:
            #打开特定的文件进行二进制的写操作
            #print(os.path.exists('/temp_file/'))
            with open("./luckyDraw_1/static/luckyDraw_1/static/%s" % File.name, 'wb+') as f:
                #分块写入文件
                for chunk in  File.chunks():
                    f.write(chunk)
            return HttpResponse("UPload over!")
    else:
        return HttpResponse("没有监听到POST请求")"""

"""def upload_file(request):
    if request.method == 'POST':
        form = Activity(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponseRedirect('/success/url/')
    else:
        form = ModelFormWithFileField()
    return HttpResponse("UPload over!")"""