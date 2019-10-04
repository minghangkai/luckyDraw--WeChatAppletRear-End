from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from luckyDraw_1.models import User,Activity,Certification,Prize
import jwt
import datetime


# Create your views here.


def index(request):
    appid = 'wxd5230cfaaa6e5d93'
    app_secret = '8601382f45e82ca2188d50afabd69771'
    js_code = request.GET.get('code')
    print('code: '+js_code)
    url = 'https://api.weixin.qq.com/sns/jscode2session' + '?appid=' + appid + '&secret=' + app_secret + '&js_code=' + js_code + '&grant_type=authorization_code'
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
        pass
    else:
        # 注册新用户
        user = User(openid=openid)
        user.save()
    secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'
    dic = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=3),  # 过期时间
        'iat': datetime.datetime.now(),  # 开始时间
        'iss': 'cyb',  # 签名
        'data': {  # 内容，一般存放该用户id和开始时间
            'openid': openid,
            'session_key': session_key,
        },
    }

    s = jwt.encode(dic, secret, algorithm='HS256')  # 加密生成字符串
    print(s)
    s = jwt.decode(s, secret, issuer='cyb', algorithms=['HS256'])  # 解密，校验签名
    print(s)
    print(type(s))

    return HttpResponse("hello!")


def getUserInfo(request):
    nickName = request.GET.get('nickName')
    avatarUrl = request.GET.get('avatarUrl')
    city = request.GET.get('city')
    country = request.GET.get('country')
    gender = request.GET.get('gender')
    language = request.GET.get('language')
    province = request.GET.get('province')
    user = User.objects.filter(openid="oV_xW49aNIjYqwuO9wPahL_FUfr8")
    user.username = nickName
    user.avatarUrl = avatarUrl
    user.city = city
    user.country = country
    user.gender = gender
    user.language = language
    user.province = province
    user.update(username=nickName, avatarUrl=avatarUrl, city=city, country=country, gender=gender, language=language,
                province=province,)
    print(nickName + " " + avatarUrl + " " + city + " " + country + " " + gender + " " + language + " " + province)
    return HttpResponse("hello!")


"""def upload_file(request):
    # 请求方法为POST时，进行处理
    if request.method == "POST":
        # 获取上传的文件，如果没有文件，则默认为None
        File = request.FILES.get("myfile", None)
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
