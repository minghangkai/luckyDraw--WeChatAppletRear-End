import jwt
import requests
from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from utils.util import get_user, create_dir_according_time, APPID, MCHID, KEY, NOTIFY_URL
from certification.models import Certification
import hashlib
import xmltodict
import time
import random
import string
from user.models import User
import datetime
from django.core import serializers

# Create your views here.

#host = 'http://127.0.0.1:8000/'
host = 'https://www.luckydraw.net.cn/'

def get_orginization_certificate_info(request):
    certificationKind = request.POST.get('certificationKind')
    print(type(certificationKind))
    print('certificationKind: ')
    print(certificationKind)
    orginizationName = request.POST.get('orginizationName')
    myFile = request.FILES.get("fileName", None)  # 获取上传的文件，如果没有文件，则默认为None
    myFile.name = '组织认证_' + orginizationName + '_' + myFile.name
    """filePath = create_dir_according_time() + '/certification/' + myFile.name
    with open(filePath, 'wb+') as f:
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
    filePath = host + 'activity_and_prize/create_image_url/' + filePath"""
    if certificationKind != 2:
        unifiedSocialCred = request.POST.get('unifiedSocialCred')
        principalName = request.POST.get('principalName')
        certification = Certification(CertificateWay=certificationKind, UnifiedSocialCreditCode=unifiedSocialCred,
                                      LegalRepresentativeName=principalName, OrganizationName=orginizationName,
                                      OrganizationIdPhoto=myFile)
        certification.save()
    else:
        unifiedSocialCred = request.POST.get('unifiedSocialCred')
        principalName = request.POST.get('principalName')
        certification = Certification(CertificateWay=certificationKind, UnifiedSocialCreditCode=unifiedSocialCred,
                                      LegalRepresentativeName=principalName, OrganizationName=orginizationName,
                                      OrganizationIdPhoto=myFile)
        certification.save()
    return HttpResponse('上传认证图片成功')
    # http://127.0.0.1:8000/activity_and_prize/create_image_url//Users/apple/PycharmProjects/luckyDraw--WeChatAppletRear-End/
    # uploadfile/2019/10/0_0wxd5230cfaaa6e5d93.o6zAJs-4EoVuB_dbionVOX2wp3x8.WOqs3IyIrEau2457b75be1163444072681dd518a1d83.png


def get_personal_certificate_info_positive(request):
    certificationKind = request.POST.get('certificationKind')
    IdType = request.POST.get('kindForCredentials')
    IdNumber = request.POST.get('credentialsNumber')
    PhoneNumber = request.POST.get('phoneNum')
    SponsorRealName = request.POST.get('realName')
    token = request.POST.get('token')
    secret = b'\x7d\xef\x87\xd5\xf8\xbb\xff\xfc\x80\x91\x06\x91\xfd\xfc\xed\x69'
    EncryptedString = token
    print(type(EncryptedString))
    EncryptedString = jwt.decode(token, secret, issuer='cyb', algorithms=['HS256'])  # 解密，校验签名
    primary_key = (EncryptedString['data'])['id']
    user = User.objects.get(id=primary_key)
    myFile = request.FILES.get("fileName", None)
    myFile.name = '认证人正面_' + SponsorRealName + '_' + myFile.name
    """filePath = create_dir_according_time() + '/certification/' + myFile.name
    with open(filePath, 'wb+') as f:
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
    #filePath = host + 'activity_and_prize/create_image_url/' + filePath
    print('filePath')
    print(filePath)
    print(type(filePath))"""
    certification = Certification(CertificateWay=certificationKind, IdType=IdType,
                                  IdNumber=IdNumber, PhoneNumber=PhoneNumber, SponsorRealName=SponsorRealName,
                                  IdPhotoPositive=myFile, user=user)
    certification.save()
    certification_id = certification.id
    print('插入正面的图片id：')
    print(certification_id)
    return HttpResponse(certification_id)

def get_personal_certificate_info_negative(request):
    SponsorRealName = request.POST.get('realName')
    print('sponsorName:')
    print(SponsorRealName)
    print(type(SponsorRealName))
    certification_id = request.POST.get('certification_id')
    print('certification_id:')
    print(certification_id)
    print(type(certification_id))
    certification_id = int(certification_id)
    print('certification_id:')
    print(certification_id)
    print(type(certification_id))
    certification = Certification.objects.get(id=certification_id)
    myFile = request.FILES.get("fileName", None)
    myFile.name = '认证人反面_' + SponsorRealName + '_' + myFile.name
    """filePath = create_dir_according_time() + '/certification/' + myFile.name
    with open(filePath, 'wb+') as f:
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
    #filePath = host + 'activity_and_prize/create_image_url/' + filePath
    IdPhotoNegative = filePath"""
    certification.IdPhotoNegative = myFile  # IdPhotoNegative
    certification.save()
    print('插入反面的图片id：')
    print(certification.id)
    return HttpResponse('成功上传个人证件背面')

def pay(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    open_id = user.OpenId
    certification_id = obj['certification_id']
    certification_id = int(certification_id)
    certification = Certification.objects.get(id=certification_id)
    data = generate_bill(open_id, certification)
    print('pay_data：')
    print(data)
    return JsonResponse(data, safe=False)

# 生成nonce_str
def generate_randomStr():
    return ''.join(random.sample(string.ascii_letters + string.digits, 32))

# 生成签名
def generate_sign(param):
    stringA = ''

    ks = sorted(param.keys())
    # 参数排序
    for k in ks:
        stringA += k + "=" + str(param[k]) + "&"
    #拼接商户KEY
    stringSignTemp = stringA + "key=" + KEY

    # md5加密
    hash_md5 = hashlib.md5(stringSignTemp.encode('utf8'))
    sign = hash_md5.hexdigest().upper()

    return sign


def trans_dict_to_xml(data):
    """
    将 dict 对象转换成微信支付交互所需的 XML 格式数据

    :param data: dict 对象
    :return: xml 格式数据
    """
    xml = []
    for k in sorted(data.keys()):
        v = data.get(k)
        if k == 'detail' and not v.startswith('<![CDATA['):
            v = '<![CDATA[{}]]>'.format(v)
        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(xml))


# 发送xml请求
def send_xml_request(url, param):
    # dict 2 xml

    xml = trans_dict_to_xml(param)

    response = requests.post(url, data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'})
    # xml 2 dict
    msg = response.text
    xmlmsg = xmltodict.parse(msg)

    return xmlmsg


def get_wx_pay_order_id():
    return str(int(time.time()))

# 统一下单
def generate_bill(openid, certification):
    #url = "https://api.mch.weixin.qq.com/sandboxnew/pay/micropay"
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    nonce_str = generate_randomStr()  # 订单中加nonce_str字段记录（回调判断使用）
    payment_order_number = get_wx_pay_order_id()  # 支付单号，只能使用一次，不可重复支付

    '''
    order.out_trade_no = out_trade_no
    order.nonce_str = nonce_str
    order.save()
    '''

    # 1. 参数
    param = {
        "appid": APPID,
        "mch_id": MCHID,  # 商户号
        "nonce_str": nonce_str,  # 随机字符串
        "body": 'TEST_pay',  # 支付说明
        "out_trade_no": payment_order_number,  # 自己生成的订单号
        "total_fee": 99,
        "spbill_create_ip": '127.0.0.1',  # 发起统一下单的ip
        "notify_url": NOTIFY_URL,
        "trade_type": 'JSAPI',  # 小程序写JSAPI
        "openid": openid,
    }
    # 2. 统一下单签名
    sign = generate_sign(param)
    certification.sign1 = sign
    certification.save()
    param["sign"] = sign  # 加入签名
    # 3. 调用接口
    xmlmsg = send_xml_request(url, param)
    # xmlmsg['xml']['return_msg']
    if xmlmsg['xml']['return_code'] == 'SUCCESS':
        if xmlmsg['xml']['result_code'] == 'SUCCESS':
            prepay_id = xmlmsg['xml']['prepay_id']     # 4. 获取prepay_id
            # 时间戳
            timeStamp = str(int(time.time()))
            # 5. 根据文档，六个参数，否则app提示签名验证失败，https://pay.weixin.qq.com/wiki/doc/api/app/app.php?chapter=9_12
            data = {
                "appId": APPID,
                # "partnerid": MCHID,
                "signType": 'MD5',
                "package": "prepay_id=" + prepay_id,
                "nonceStr": nonce_str,
                "timeStamp": timeStamp,
            }  # 6. paySign签名
            paySign = generate_sign(data)
            certification.sign2 = paySign
            certification.save()
            data["paySign"] = paySign  # 加入签名
            # 7. 传给前端的签名后的参数
            return data


#支付回调，用于接受官方返回的支付数据
def get_pay_info(request):
    msg = request.body.decode('utf-8')
    xmlmsg = xmltodict.parse(msg)

    return_code = xmlmsg['xml']['return_code']

    if return_code == 'FAIL':
        # 官方发出错误
        return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
                                <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""",
                            content_type='text/xml', status=200)

    elif return_code == 'SUCCESS':
        # 拿到这次支付的订单号
        out_trade_no = xmlmsg['xml']['out_trade_no']
        certification = Certification.objects.get(payment_order_number=out_trade_no)
        print("xmlmsg['xml']['sign']:")
        print(xmlmsg['xml']['sign'])
        if xmlmsg['xml']['sign'] != certification.sign2:
            # 随机字符串不一致
            return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>
                                            <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""",
                                content_type='text/xml', status=200)

        # 根据需要处理业务逻辑
        else:
            user = certification.user
            user.certificate = True
            user.save()
            certification.pass_check = True
            certification.save()
            return HttpResponse("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                                            <return_msg><![CDATA[OK]]></return_msg></xml>""",
                                content_type='text/xml', status=200)