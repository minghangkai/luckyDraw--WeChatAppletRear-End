import base64

import requests
from utils.util import APPID, MCHID, KEY, NOTIFY_URL
import hashlib
import xmltodict
import random
import string
import time
from Crypto.Cipher import AES



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
def send_xml_request1(url, param):
    # dict 2 xml

    xml = trans_dict_to_xml(param)

    response = requests.post(url, data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'})
    # xml 2 dict
    msg = response.text
    xmlmsg = xmltodict.parse(msg)

    return xmlmsg


def send_xml_request2(url, param):
    # dict 2 xml

    xml = trans_dict_to_xml(param)

    response = requests.post(url, data=xml.encode('utf-8'), headers={'Content-Type': 'text/xml'},
                             cert=('/home/luckyDraw/certificate_of_wctcw/apiclient_cert.pem',
                                   '/home/luckyDraw/certificate_of_wctcw/apiclient_key.pem'))
    # xml 2 dict
    msg = response.content.decode('utf-8')
    print(msg)
    xmlmsg = xmltodict.parse(msg)

    return xmlmsg

def get_wx_pay_order_id():
    return str(int(time.time()))


def refund(payment_order_number):
    url = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
    nonce_str = generate_randomStr()
    out_refund_no = get_wx_pay_order_id()
    param = {
        "appid": APPID,
        "mch_id": MCHID,
        # "sub_mch_id": MCHID,
        "nonce_str": nonce_str,
        "out_trade_no": payment_order_number,
        "out_refund_no": out_refund_no,
        "total_fee": 1,  # 9900
        "refund_fee": 1,  # 9900
        "notify_url": 'http://www.luckydraw.net.cn/certification/get_refund_info'
    }
    sign = generate_sign(param)
    param["sign"] = sign  # 加入签名
    # 3. 调用接口
    xmlmsg = send_xml_request2(url, param)
    if xmlmsg['xml']['return_code'] == 'SUCCESS':
        if xmlmsg['xml']['result_code'] == 'SUCCESS':
            print('调用退款API成功')
        else:
            print("xmlmsg['xml']['err_code']:")
            print(xmlmsg['xml']['err_code'])
    else:
        print("xmlmsg['xml']:")
        print(xmlmsg['xml'])
        print("xmlmsg['xml']['return_msg']:")
        print(type(xmlmsg['xml']['return_msg']))
        print(xmlmsg['xml']['return_msg'])
    return out_refund_no


class AESCipher():
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        key_temp = hashlib.md5(key.encode('utf8')).hexdigest()
        self.key = key_temp.encode('utf-8')
        # Padding for the input string --not
        # related to encryption itself.
        self.BLOCK_SIZE = 32  # Bytes
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    # 加密
    def encrypt(self, raw):
        raw = self.pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw))

    # 解密，针对微信用此方法即可
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        a = self.unpad(cipher.decrypt(enc))
        print("a:")
        print(type(a))
        print(a)
        print('a.decode("utf-8"):')
        print(type(a.decode('utf8')))
        print(a.decode('utf8'))
        return self.unpad(cipher.decrypt(enc)).decode('utf8')