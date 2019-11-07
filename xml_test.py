import random
import string
import hashlib

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


def generate_sign(param):
    stringA = ''
    ks = sorted(param.keys())
    # 参数排序
    for k in ks:
        stringA += k + "=" + str(param[k]) + "&"
    #拼接商户KEY
    stringSignTemp = stringA + "key=WUCHUANTONGCHENGWANGsR10280923sR"
    print(stringSignTemp)
    # md5加密
    hash_md5 = hashlib.md5(stringSignTemp.encode('utf-8'))
    sign = hash_md5.hexdigest().upper()
    return sign






param = {
        "appid": 'wx6ac3ca8cc6189b5b',
        "mch_id": '1491830732',  # 商户号
        "nonce_str": ''.join(random.sample(string.ascii_letters + string.digits, 32)),  # 随机字符串
        "body": 'TEST_pay',  # 支付说明
        "out_trade_no": 'payment_order_number',  # 自己生成的订单号
        "total_fee": 99,
        "spbill_create_ip": '127.0.0.1',  # 发起统一下单的ip
        "notify_url": 'http://www.luckydraw.net.cn/',
        "trade_type": 'JSAPI',  # 小程序写JSAPI
        "openid": 'okSsB5Zh1hJ0b4QJt7zHK1UmdfpU',
    }
sign = generate_sign(param)
print(sign)
param['sign'] = sign
param_xml = trans_dict_to_xml(param)
print(param_xml)