import requests
from django.http import HttpResponse, JsonResponse
import json

from utils.get_AccessToken import get_access_token
from utils.util import get_user
from activity_and_prize.models import Activity, Prize, InviteArray, PrizeWinner
import traceback
import datetime
import random
import os
import time
from django.core import serializers

def timed_draw():
    activities = Activity.objects.filter(ConditionType=0, ActivityEnd=False).order_by('EndTime')
    print(str(activities))
    for e in activities:
        if (e.EndTime - datetime.datetime.now()).seconds <= 60 and (e.EndTime - datetime.datetime.now()).seconds > 0:
            participations = e.participate.all()
            participations_num = participations.__len__()
            if participations_num == 0:  # 判断是否存在参与者
                print('活动没有参与者')  # 接入微信通知接口
            else:
                prizes = e.prize_set.all()  # print(random.randint(0,9))  # 获取当前活动的所有奖品
                for p in prizes:
                    prize_number = p.PrizeNumber  # 取得每个奖品的数量
                    i = 0
                    while i < prize_number:  # 循环内为一份奖品分配中奖者
                        prize_winner = PrizeWinner(winner=participations[random.randint(0, participations_num)],
                                                   prize=p)
                        prize_winner.save()
                print('开奖')  # 接入微信通知接口
                access_token = get_access_token()

            e.ActivityEnd = True
            e.save()
        else:
            break


