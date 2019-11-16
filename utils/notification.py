#消息模板ID
import requests
from activity_and_prize.models import Activity, Prize, InviteArray
lotteryResltNotification = '3HNEeIjVsSDRLXjIkMAmECv7RvBijDLkkyhx3l6zjdA'  # 抽奖结果通知：发送给所有的参与抽奖用户
certificationSuccessNotification = 'BwXvzccbNEaWK98Vdl6CIwW7lSeaWTHGbY-JQ40Cyjc'  # 认证成功通知
authenticationFailureNotification = 'NoQSZKY3ccapaK2G0IlQQv3Ti3hBkkvRdk4zLSLWGl8'  # 认证失败通知



def postToUrlOfAllParticipate(activity, participations, access_token):
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + access_token
    prizes = Prize.objects.filter(activity=activity)
    prizeName = ''
    for prize in prizes:
        prizeName = prize.PrizeName + ' ' + prizeName
    for participate in participations:
        openid = participate.OpenId

        paramsOfParticpate = {
            "touser": openid,
            "weapp_template_msg": {
                "template_id": lotteryResltNotification,
                "page": "pages/activityInfo/activityInfo/?activity_id=" + str(activity.id),
                "form_id": "",
                "data": {
                    "keyword1": {
                        "DATA": "中奖名单已公布"
                    },
                    "keyword2": {
                        "DATA": prizeName[:16] + '...'
                    },
                    "keyword3": {
                        "DATA": "点击查看中奖名单"
                    },
                },
                "emphasis_keyword": "keyword1.DATA"
            },
        }
        messageSendToParticpate = requests.post(url=url, data=paramsOfParticpate)
        print('messageSendToParticpate:')
        print(messageSendToParticpate)

def postToUrlOfAllParticipate1(activity, participate, access_token):
    url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/uniform_send?access_token=' + access_token
    prizes = Prize.objects.filter(activity=activity)
    prizeName = ''
    for prize in prizes:
        prizeName = prize.PrizeName + ' ' + prizeName
    openid = participate.OpenId
    print('openid')
    print(openid)
    paramsOfParticpate = {
        "touser": openid,
        "weapp_template_msg": {
            "template_id": lotteryResltNotification,
            "page": "pages/activityInfo/activityInfo/?activity_id=" + str(activity.id),
            "form_id": "",
            "data": {
                "keyword1": {
                    "DATA": "中奖名单已公布"
                },
                "keyword2": {
                    "DATA": prizeName[:16] + '...'
                },
                "keyword3": {
                    "DATA": "点击查看中奖名单"
                },
            },
            "emphasis_keyword": "keyword1.DATA"
        },
    }
    messageSendToParticpate = requests.post(url=url, data=paramsOfParticpate)
    print(messageSendToParticpate.text)

























