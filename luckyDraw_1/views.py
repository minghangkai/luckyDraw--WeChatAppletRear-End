from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import requests
from jwt import ExpiredSignatureError
from luckyDraw_1.models import User,Activity,Certification,Prize
import jwt
import datetime,time
import os
import time

# Create your views here.
host = 'http://127.0.0.1:8000/'
# host = 'https://www.luckydraw.net.cn/'

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
        #print(user)
        return user
    except ExpiredSignatureError:
        return False

def create_dir_according_time():
    localtime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print('localtime='+localtime)
    # 系统当前时间年份
    year=time.strftime('%Y',time.localtime(time.time()))
    # 月份
    month=time.strftime('%m',time.localtime(time.time()))
    # 日期
    # day=time.strftime('%d',time.localtime(time.time()))
    #具体时间 小时分钟毫秒
    mdhms = time.strftime('%m%d%H%M%S',time.localtime(time.time()))
    print(os.getcwd())
    fileYear = os.getcwd()+'/luckyDraw_1/static/luckyDraw_1/uploadfile'+'/'+year
    print('fileyear'+fileYear)
    fileMonth = fileYear+'/'+month
    print('filemonth'+fileMonth)
    # fileDay=fileMonth+'/'+day
    if not os.path.exists(fileYear):
      print('1')
      os.mkdir(fileYear)
      os.mkdir(fileMonth)

      # os.mkdir(fileDay)
    else:
      if not os.path.exists(fileMonth):
        print('2')
        os.mkdir(fileMonth)

    return fileMonth


def create_image_url(request, imagepath):
    print("imagepath=" + str(imagepath))
    image_data = open(imagepath, "rb").read()
    return HttpResponse(image_data, content_type="image/png")




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
        return HttpResponse('true')

def get_activity_info(request):
    obj = json.loads(request.body)
    print("obj的类型为：")
    print(type(obj))
    # print(obj)
    user = get_user(obj)
    if not user:
        return HttpResponse('false')  # token过期
    else:
        newBy = obj['newBy']
        phoneNum = obj['phoneNum']
        activityName = obj['activityName']
        conditionObject = obj['conditionObject']
        kindOfAcitivity = int(obj['kindOfPrize'])
        primary_key_of_activity = 0
        if conditionObject['id'] == 0:
            endTime = datetime.datetime.strptime(conditionObject['info'], "%Y-%m-%d %H:%M:%S")
            conditionInfo = None
        elif conditionObject['id'] == 1:
            endTime = None
            conditionInfo = conditionObject['info']
        elif conditionObject['id'] == 2:
            endTime = None
            conditionInfo = None
        activity = Activity(sponsor=user, certificateOrNot=user.certificate, sponsorWay=newBy, phoneNumber=phoneNum, activityName=activityName,
                            endTime=endTime, conditionType=conditionObject['id'], conditionInfo=conditionInfo,
                            kindOfAcitivity=kindOfAcitivity)
        # activity.save()
        if newBy == 1:
            activityDetails = json.dumps(obj['infoOfActivity'])
            activity.participantAttention = obj['participantAttention']
            activity.inviateFriends = obj['inviateFriends']
            activity.activityDetails = activityDetails
            activity.save()
        elif newBy == 2:
            activity.activityDetails = obj['infoOfActivity']
            activity.sponsorNickName = obj['initiatorName']
            activity.participantAttention = obj['participantAttention']
            activity.shareJurisdiction = obj['shareJurisdiction']
            activity.allowQuitOrNot = obj['allowQuitOrNot']
            activity.inviateFriends = obj['inviateFriends']
            activity.inputCommandOrNot = obj['inputCommandOrNot']
            activity.save()
        elif newBy == 3:
            activity.officialAccountsName = obj['officialAccountsName']
            activity.sponsorWechatNumber = obj['initiatorWxNumber']
            activity.participateWay = obj['participateWay']
            activity.allowQuitOrNot = obj['allowQuitOrNot']
            activity.save()
        elif newBy == 4:
            activity.sponsorNickName = obj['initiatorName']
            activity.sponsorWechatNumber = obj['initiatorWxNumber']
            activity.participantDrawNumber = obj['participantDrawNumber']
            activity.shareJurisdiction = obj['shareJurisdiction']
            activity.winnerList = obj['winnerList']
            activity.save()
        primary_key_of_activity = activity.id
        imageArray = obj['imageArray']
        primary_key_of_prize = []
        for index in range(len(imageArray)):
            if newBy == 4:
                prize = Prize(prizeName=imageArray[index]['nameOfPrize'],
                              prizeNumber=imageArray[index]['numberOfPrize'],
                              winningProbability=imageArray[index]['probity'],
                              activity=activity)
            else:
                prize = Prize(prizeName=imageArray[index]['nameOfPrize'],
                              prizeNumber=imageArray[index]['numberOfPrize'],
                              activity=activity)
            prize.save()
            primary_key_of_prize.append(prize.id)
        activity_url = create_dir_according_time()
        data = {'prizeLen': len(imageArray),
                'activityId': primary_key_of_activity,
                'prizeId': primary_key_of_prize,}
        data1 = data
        print(type(data))
        print(type(json.dumps(data1)))
        print("111111111")
        print('primary_key_of_activity'+ str(primary_key_of_activity))
        return JsonResponse(data)

def upload_file(request):
    newBy = int(request.POST.get('newBy'))
    activityId = request.POST.get('activityId')
    prizeId = request.POST.get('prizeId')
    myFile = request.FILES.get("fileName", None)  # 获取上传的文件，如果没有文件，则默认为None
    # 打开特定的文件进行二进制的写操作
    # print(os.path.exists('/temp_file/'))
    myFile.name = activityId + '_' + prizeId + myFile.name
    filePath = create_dir_according_time() + '/' + myFile.name
    with open(filePath, 'wb+') as f:
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
    url = host+'luckyDraw_1/create_image_url/'+filePath
    if newBy == 0:
        print(str( HttpResponse(url)))
        return HttpResponse(url)
    # http://127.0.0.1:8000/luckyDraw_1/create_image_url//Users/apple/PycharmProjects/luckyDraw--WeChatAppletRear-End/
    # luckyDraw_1/static/luckyDraw_1/uploadfile/2019/10/0_0wxd5230cfaaa6e5d93.o6zAJs-4EoVuB_dbionVOX2wp3x8.WOqs3IyIrEau2457b75be1163444072681dd518a1d83.png
    elif newBy == 1:
        activity = Activity.objects.get(id=activityId)
        activity.activityPhoto = ''
        activity.save()
        prize = Prize.objects.get(id=prizeId)
        prize.prizePhoto = filePath
        prize.activity = activity
        prize.save()
        return HttpResponse('存储奖品图成功' + filePath)
    else:
        activity = Activity.objects.get(id=activityId)
        if prizeId == 0:
            activity.activityPhoto = filePath
            activity.save()
            return HttpResponse('存储活动头图成功'+filePath)
        else:
            prize = Prize.objects.get(id=prizeId)
            prize.prizePhoto = filePath
            prize.activity = activity
            prize.save()
            return HttpResponse('存储奖品图成功'+filePath)

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