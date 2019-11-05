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
    print('stringSignTemp')
    print(stringSignTemp)
    # md5加密
    hash_md5 = hashlib.md5(stringSignTemp.encode('utf-8'))
    sign = hash_md5.hexdigest().upper()
    return sign

"""
appId=wx6ac3ca8cc6189b5b&nonceStr=rLKuQS7bldznYtymhBDq9Msv2WVoHZc1&
package=prepay_id=wx05233803277806f816af52181819100500&
signType=MD5&timeStamp=1572968283&key=WUCHUANTONGCHENGWANGsR10280923sR


appId=wx6ac3ca8cc6189b5b&nonceStr=rLKuQS7bldznYtymhBDq9Msv2WVoHZc1&
package=prepay_id=wx05233803277806f816af52181819100500&sign=1F7741E91A4D7CDEAAB42574897A2119&
signType=MD5&timeStamp=1572968283

"""



param={
    'appId': 'wx6ac3ca8cc6189b5b',
    'timeStamp': "1572968283",
    'nonceStr': "rLKuQS7bldznYtymhBDq9Msv2WVoHZc1",
    'package': 'prepay_id=wx05233803277806f816af52181819100500',
    'signType': "MD5",
}

sign = generate_sign(param)
print(sign)
param['sign'] = sign
param_xml = trans_dict_to_xml(param)
print(param_xml)