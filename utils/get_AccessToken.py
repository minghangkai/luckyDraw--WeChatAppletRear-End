import requests

from utils.util import APPID, APP_SECRET


def get_access_token():
    appid = APPID
    app_secret = APP_SECRET
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + app_secret
    r = requests.get(url)
    access_token = r.json()['access_token']
    print('access_token')
    print(access_token)
    return access_token
