from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from utils.util import get_user, create_dir_according_time
import requests
from jwt import ExpiredSignatureError
from activity_and_prize.models import Activity, Prize
import jwt
import datetime,time
import os
import time

host = 'http://127.0.0.1:8000/'
# host = 'https://www.luckydraw.net.cn/'
# Create your views here.
def get_activity_info(request):
    obj = json.loads(request.body)
    print("obj的类型为：")
    print(type(obj))
    # print(obj)
    user = get_user(obj)
    if not user:
        return HttpResponse('false')  # token过期
    else:
        sponsorWay = obj['newBy']
        sponsorPhoneNumber = obj['phoneNum']
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
        activity = Activity(sponsor=user, certificate=user.certificate, SponsorWay=sponsorWay,
                            SponsorPhoneNumber=sponsorPhoneNumber, ActivityName=activityName,
                            EndTime=endTime, ConditionType=conditionObject['id'], ConditionInfo=conditionInfo,
                            KindOfAcitivity=kindOfAcitivity)
        # activity.save()
        if sponsorWay == 1:
            activityDetails = json.dumps(obj['infoOfActivity'])
            print(type(activity.ActivityDetails))
            print(activity.ActivityDetails)
            activity.ParticipantAttention = obj['participantAttention']
            activity.InviateFriends = obj['inviateFriends']
            activity.ActivityDetails = activityDetails
            activity.save()
        elif sponsorWay == 2:
            activity.ActivityDetails = obj['infoOfActivity']
            print(type(activity.ActivityDetails))
            print(activity.ActivityDetails)
            activity.SponsorNickName = obj['initiatorName']
            activity.ParticipantAttention = obj['participantAttention']
            activity.ShareJurisdiction = obj['shareJurisdiction']
            activity.AllowQuitOrNot = obj['allowQuitOrNot']
            activity.InviateFriends = obj['inviateFriends']
            activity.InputCommandOrNot = obj['inputCommandOrNot']
            activity.save()
        elif sponsorWay == 3:
            activity.ActivityDetails = obj['infoOfActivity']
            print(type(activity.ActivityDetails))
            print(activity.ActivityDetails)
            activity.OfficialAccountsName = obj['officialAccountsName']
            activity.SponsorWechatNumber = obj['initiatorWxNumber']
            activity.ParticipateWay = obj['participateWay']
            activity.AllowQuitOrNot = obj['allowQuitOrNot']
            activity.save()
        elif sponsorWay == 4:
            activity.ActivityDetails = obj['infoOfActivity']
            print(type(activity.ActivityDetails))
            print(activity.ActivityDetails)
            activity.SponsorNickName = obj['initiatorName']
            activity.SponsorWechatNumber = obj['initiatorWxNumber']
            activity.ParticipantDrawNumber = obj['participantDrawNumber']
            activity.ShareJurisdiction = obj['shareJurisdiction']
            activity.WinnerList = obj['winnerList']
            activity.save()
        primary_key_of_activity = activity.id
        ImageArray = obj['imageArray']
        primary_key_of_prize = []
        for index in range(len(ImageArray)):
            if sponsorWay == 4:
                prize = Prize(prizeName=ImageArray[index]['nameOfPrize'],
                              prizeNumber=ImageArray[index]['numberOfPrize'],
                              winningProbability=ImageArray[index]['probity'],
                              activity=activity)
            else:
                prize = Prize(prizeName=ImageArray[index]['nameOfPrize'],
                              prizeNumber=ImageArray[index]['numberOfPrize'],
                              activity=activity)
            prize.save()
            primary_key_of_prize.append(prize.id)
        activity_url = create_dir_according_time()
        data = {'prizeLen': len(ImageArray),
                'activityId': primary_key_of_activity,
                'prizeId': primary_key_of_prize,}
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
    url = host+'activity_and_prize/create_image_url/'+filePath
    if newBy == 0:
        print(str( HttpResponse(url)))
        return HttpResponse(url)
    # http://127.0.0.1:8000/activity_and_prize/create_image_url//Users/apple/PycharmProjects/luckyDraw--WeChatAppletRear-End/
    # uploadfile/2019/10/0_0wxd5230cfaaa6e5d93.o6zAJs-4EoVuB_dbionVOX2wp3x8.WOqs3IyIrEau2457b75be1163444072681dd518a1d83.png
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

def return_image(request, imagepath):
    print("imagepath=" + str(imagepath))
    image_data = open(imagepath, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def return_activity_main_info(request):
    activity_num = Activity.objects.filter(activityEnd=False).count()
    activity_array = Activity.objects.get(activityEnd=False)
    print('activity_array:')
    print(activity_array)