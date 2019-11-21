#消息模板ID
import requests
import json
from activity_and_prize.models import Activity, Prize, InviteArray
lotteryResltNotification = '3HNEeIjVsSDRLXjIkMAmEJmyLc9SOq8aalnB9hkZT9s'  # 抽奖结果通知：发送给所有的参与抽奖用户
certificationSuccessNotification = 'BwXvzccbNEaWK98Vdl6CIwW7lSeaWTHGbY-JQ40Cyjc'  # 认证成功通知
authenticationFailureNotification = 'NoQSZKY3ccapaK2G0IlQQv3Ti3hBkkvRdk4zLSLWGl8'  # 认证失败通知


def postToUrlOfAllParticipate(activity, participate, access_token):
    url = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + access_token
    prizes = Prize.objects.filter(activity=activity)
    prizeName = ''
    for prize in prizes:
        prizeName = prize.PrizeName + ' ' + prizeName
    openid = participate.OpenId
    print('openid')
    print(openid)
    paramsOfParticpate = {
      "touser": openid,
      "template_id": lotteryResltNotification,
      "page": "pages/activityInfo/activityInfo/?activity_id=" + str(activity.id),
      "data": {
          "thing8": {
              "value": "您参与的抽奖已经开奖，点击查看中奖名单"
          },
          "thing10": {
              "value": prizeName[:20]
          }
      }
    }
    paramsJson = json.dumps(paramsOfParticpate)
    messageSendToParticpate = requests.post(url=url, data=paramsJson)
    #messageSendToParticpate = requests.post(url=url, data=paramsOfParticpate, headers={'Content-Type': 'application/json'})
    print("messageSendToParticpate回调：")
    print(messageSendToParticpate.text)

"""{
    "data":[
        {
            "priTmplId": "NoQSZKY3ccapaK2G0IlQQv3Ti3hBkkvRdk4zLSLWGl8",
            "title":"审核结果通知",
            "content":"审核结果:{{phrase1 5个以内汉字.DATA}}\n审核内容:{{thing2.DATA}}\n拒绝理由:{{thing5.DATA}}\n",
            "example":"审核结果:不通过\n审核内容:北区6楼23寸屏幕投放申请\n拒绝理由:不符合当地法律法规\n","type":2},
        {
            "priTmplId":"BwXvzccbNEaWK98Vdl6CIwW7lSeaWTHGbY-JQ40Cyjc",
            "title":"审核通过通知",
            "content":"审核结果:{{phrase1.DATA}}\n审核内容:{{thing2.DATA}}\n",
            "example":"审核结果:通过/成功\n审核内容:北区6楼24寸屏幕投影请求\n","type":2},
        {
            "priTmplId":"3HNEeIjVsSDRLXjIkMAmECv7RvBijDLkkyhx3l6zjdA",
            "title":"开奖结果通知",
            "content":"开奖结果:{{character_string7.DATA}}\n奖品名称:{{thing10.DATA}}\n特别提醒:{{thing8.DATA}}\n",
            "example":"开奖结果:01 08 09 13 16 33+01\n奖品名称:电动牙刷\n特别提醒:最终开奖结果请已彩票官网为准\n","type":2}],
    "errmsg":"ok","errcode":0
}"""

























