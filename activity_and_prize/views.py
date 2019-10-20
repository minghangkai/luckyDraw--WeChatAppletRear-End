from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from utils.util import get_user, create_dir_according_time
from activity_and_prize.models import Activity, Prize
from user.models import User
import datetime, os, time
from django.core import serializers

host = 'http://127.0.0.1:8000/'
# host = 'https://www.luckydraw.net.cn/'
# Create your views here.


def upload_file_json(request):
    myFile = request.FILES.get("fileName", None)
    myFile.name = 'richtext_' + '_' + myFile.name
    localtime = time.strftime('/%Y/%m/%d/', time.localtime(time.time()))
    filePath = os.getcwd() + '/media/uploadfile' + localtime + 'richtext_' + myFile.name  # 需要等待自动任务函数才真正能用
    with open(filePath, 'wb+') as f:
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
    url = host + 'activity_and_prize/create_image_url/' + filePath
    return HttpResponse(url)


def get_activity_info(request):
    obj = json.loads(request.body)
    """print("obj的类型为：")
    print(type(obj))"""
    # print(obj)
    user = get_user(obj)
    if not user:
        return HttpResponse('false')  # token过期
    else:
        sponsorWay = obj['newBy']  # 活动类型：快速、高级……
        sponsorPhoneNumber = obj['phoneNum']
        activityName = obj['activityName']
        conditionObject = obj['conditionObject']
        kindOfAcitivity = int(obj['kindOfPrize'])  # 奖品种类
        endTime = None
        conditionInfo = None
        if int(conditionObject['id']) == 0:
            print('0')
            endTime = datetime.datetime.strptime(conditionObject['info'], "%Y-%m-%d %H:%M:%S")
            conditionInfo = None
        elif int(conditionObject['id']) == 1:
            print('1')
            endTime = None
            conditionInfo = conditionObject['info']
        elif int(conditionObject['id']) == 2:
            print('2')
            endTime = None
            conditionInfo = None
        activity = Activity(sponsor=user, certificate=user.certificate, SponsorWay=sponsorWay,
                            SponsorPhoneNumber=sponsorPhoneNumber, ActivityName=activityName,
                            EndTime=endTime, ConditionType=int(conditionObject['id']), ConditionInfo=conditionInfo,
                            KindOfAcitivity=kindOfAcitivity)
        # activity.save()
        if sponsorWay == 1:
            activityDetails = json.dumps(obj['infoOfActivity'])
            # print(type(activity.ActivityDetails))
            # print(activity.ActivityDetails)
            activity.ParticipantAttention = obj['participantAttention']
            activity.InviateFriends = obj['inviateFriends']
            activity.ActivityDetails = activityDetails
            activity.save()
        elif sponsorWay == 2:
            activity.ActivityDetails = obj['infoOfActivity']
            # print(type(activity.ActivityDetails))
            # print(activity.ActivityDetails)
            activity.SponsorNickName = obj['initiatorName']
            activity.ParticipantAttention = obj['participantAttention']
            activity.ShareJurisdiction = obj['shareJurisdiction']
            activity.AllowQuitOrNot = obj['allowQuitOrNot']
            activity.InviateFriends = obj['inviateFriends']
            activity.InputCommandOrNot = obj['inputCommandOrNot']
            activity.save()
        elif sponsorWay == 3:
            activity.ActivityDetails = obj['infoOfActivity']
            # print(type(activity.ActivityDetails))
            # print(activity.ActivityDetails)
            activity.OfficialAccountsName = obj['officialAccountsName']
            activity.SponsorWechatNumber = obj['initiatorWxNumber']
            activity.ParticipateWay = obj['participateWay']
            activity.AllowQuitOrNot = obj['allowQuitOrNot']
            activity.save()
        elif sponsorWay == 4:
            activity.ActivityDetails = obj['infoOfActivity']
            # print(type(activity.ActivityDetails))
            # print(activity.ActivityDetails)
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
                prize = Prize(PrizeName=ImageArray[index]['nameOfPrize'],
                              PrizeNumber=ImageArray[index]['numberOfPrize'],
                              WinningProbability=ImageArray[index]['probity'],
                              activity=activity)
            else:
                prize = Prize(PrizeName=ImageArray[index]['nameOfPrize'],
                              PrizeNumber=ImageArray[index]['numberOfPrize'],
                              activity=activity)
            prize.save()
            primary_key_of_prize.append(prize.id)
        data = {'prizeLen': len(ImageArray),
                'activityId': primary_key_of_activity,
                'prizeId': primary_key_of_prize,}
        # print('primary_key_of_activity' + str(primary_key_of_activity))
        user.CreateActivityNum = user.CreateActivityNum + 1
        user.save()
        return JsonResponse(data)


def get_prize_info(request):
    newBy = int(request.POST.get('newBy'))
    activityId = request.POST.get('activityId')
    prizeId = request.POST.get('prizeId')
    myFile = request.FILES.get("fileName", None)
    myFile.name = activityId + '_' + prizeId + '_' + myFile.name
    prizeId = int(prizeId)
    activityId = int(activityId)
    if newBy == 1:
        activity = Activity.objects.get(id=activityId)
        activity.activityPhoto = ''
        activity.save()
        # Prize.objects.filter(id=prizeId).update(PrizePhoto=myFile, activity=activity)
        # prize(prizePhoto=myFile)
        prize = Prize.objects.get(activity=activity)
        prize.prizePhoto = myFile
        prize.activity = activity
        prize.save()
        return HttpResponse('存储奖品图成功')
    else:
        activity = Activity.objects.get(id=activityId)
        if prizeId == 0:
            # Activity.objects.get(id=activityId).update(ActivityPhoto=myFile)
            activity.ActivityPhoto = myFile
            activity.save()
            print('存储活动头图成功')
            return HttpResponse('存储活动头图成功')
        else:
            prize = Prize.objects.get(id=prizeId) #.update(PrizePhoto=myFile, activity=activity)
            prize.PrizePhoto = myFile
            prize.activity = activity
            prize.save()
            print('存储奖品图成功')
            return HttpResponse('存储奖品图成功')

    #         var filesrc = util.fileUpload('luckyDraw_1/upload_file', res.tempFilePaths[0], 'fileName') 前端请求


def return_image(request, imagepath):
    # print("imagepath=" + str(imagepath))
    image_data = open(imagepath, "rb").read()
    return HttpResponse(image_data, content_type="image/png")


def return_index_activity_main_info(request):
    activity_num = Activity.objects.filter(ActivityEnd=False).count()
    activity_array = []  # 'activity_photo': , 'activity_sponsor':, 'certificate':, 'activity_end_time':, 'prize_of_acitivity_array':,
    prize_of_an_acitivity_array = []  # 'prize_name': , 'prize_num':
    activities = Activity.objects.filter(ActivityEnd=False, ConditionType=0) # 0为按时间开奖
    for e in activities:
        prizes = e.prize_set.all()
        # print('prizes:')
        # print(prizes)
        # print(type(prizes))
        prize_array = []
        for f in prizes:
            dict_prize = {'prize_name': f.PrizeName, 'prize_num': f.PrizeNumber}
            prize_array.append(dict_prize)
        if e.ActivityPhoto == '':
            activity_photo = str(e.ActivityPhoto)
        else:
            activity_photo = str(e.prize_set.all()[0].PrizePhoto)
        dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo, 'activity_sponsor': e.SponsorNickName,
                         'certificate': e.certificate, 'activity_end_time': str(e.EndTime)[:-3],
                         'prize_of_activity_array': prize_array}  # str(e.EndTime)[:-3]:将datetime类型转为字符串
        activity_array.append(dict_activity)
        # print('activity_array:')
        # print(type(activity_array))
    # data = serializers.serialize("json", activity_array)
    print(str(activity_array))
    return JsonResponse(activity_array, safe=False)


def return_activity_info(request):
    obj = json.loads(request.body)
    activity = Activity.objects.get(id=obj['activity_id'])
    prizes = serializers.serialize("json", activity.prize_set.all())
    if activity.ActivityPhoto == '':
        activity_photo = str(activity.ActivityPhoto)
    else:
        activity_photo = str(activity.prize_set.all()[0].PrizePhoto)
    participate_avatar_array = []
    participates = activity.participate.all()
    for e in participates:
        participate_avatar = e.AvatarUrl
        participate_avatar_array.append(participate_avatar)
    dict_of_activity = {'activity_photo': str(activity_photo), 'activity_certificate': activity.certificate,
                        'activity_details': activity.ActivityDetails, 'activity_end_time': str(activity.EndTime)[:-3], # str(e.EndTime)[:-3]
                        'activity_prizes': prizes, 'sponsor_nickname': activity.SponsorNickName,
                        'activity_end': activity.ActivityEnd, 'share_jurisdiction': activity.ShareJurisdiction,
                        'participate_avatar_array': participate_avatar_array, 'activity_end': activity.ActivityEnd}
    """print('dict_of_activity:')
    print(type(dict_of_activity))
    dict_of_activity_json = json.dumps(dict_of_activity)"""
    # dict_of_activity_json = serializers.serialize("json", dict_of_activity)
    return JsonResponse(dict_of_activity, safe=False)
    #return  JsonResponse(dict_of_activity)


def participate_activity(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    print('user')
    print(user)
    activity = Activity.objects.get(id=int(obj['activity_id']))
    activity.participate.add(user)
    activity.save()
    user.ParticipateActivityNum = user.ParticipateActivityNum + 1
    user.save()
    return HttpResponse('用户参与活动成功')

def return_selfhelp_activity_main_info(request):
    activity_num = Activity.objects.filter(ActivityEnd=False).count()
    activity_array = []  # 'activity_photo': , 'activity_sponsor':, 'certificate':, 'activity_end_time':, 'prize_of_acitivity_array':,
    prize_of_an_acitivity_array = []  # 'prize_name': , 'prize_num':
    activities = Activity.objects.filter(ActivityEnd=False, ConditionType=1) # 1为按人数开奖
    for e in activities:
        prizes = e.prize_set.all()
        # print('prizes:')
        # print(prizes)
        # print(type(prizes))
        prize_array = []
        for f in prizes:
            dict_prize = {'prize_name': f.PrizeName, 'prize_num': f.PrizeNumber}
            prize_array.append(dict_prize)
        if e.ActivityPhoto == '':
            activity_photo = str(e.ActivityPhoto)
        else:
            activity_photo = str(e.prize_set.all()[0].PrizePhoto)
        print('endTime')
        print(e.EndTime)
        dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo, 'activity_sponsor': e.SponsorNickName,
                         'certificate': e.certificate, 'participate_number': e.ConditionInfo,
                         'prize_of_activity_array': prize_array}  # str(e.EndTime)[:-3]:将datetime类型转为字符串
        activity_array.append(dict_activity)
        # print('activity_array:')
        # print(type(activity_array))
    # data = serializers.serialize("json", activity_array)
    print(str(activity_array))
    return JsonResponse(activity_array, safe=False)


def return_personal_paticipate_info(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    # activities = Activity.objects.filter(participate=user)
    activities = user.participate.all()
    activity_array = []
    end_string = ''
    for e in activities:
        prizes = e.prize_set.all()
        prize_array = []

        for f in prizes:
            dict_prize = {'prize_name': f.PrizeName, 'prize_num': f.PrizeNumber}
            prize_array.append(dict_prize)
        if e.ActivityPhoto == '':
            activity_photo = str(e.ActivityPhoto)
        else:
            activity_photo = str(e.prize_set.all()[0].PrizePhoto)
        if e.ActivityEnd == False:
            end_string = '[进行中]'
            color_string = '#64DD17'
        else:
            end_string = '[已结束]'
            color_string = '#E57373'
        if e.ConditionType == 0:
            dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo,
                             'activity_sponsor': e.SponsorNickName, 'condition_type': '按时间开奖',
                             'info': str(e.EndTime)[:-3], 'end': end_string, 'color': color_string,
                             'prize_of_activity_array': prize_array, 'now_participate_number': e.ConditionNum}  # str(e.EndTime)[:-3]:将datetime类型转为字符串
        elif e.ConditionType == 1:
            dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo,
                             'activity_sponsor': e.SponsorNickName, 'condition_type': '按人数开奖',
                             'info': '满'+str(e.ConditionInfo)+'人开奖', 'end': end_string, 'color': color_string,
                             'prize_of_activity_array': prize_array, 'now_participate_number': e.ConditionNum}
        elif e.ConditionType ==2:
            dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo,
                             'activity_sponsor': e.SponsorNickName, 'condition_type': '发起人手动开奖',
                             'info': '', 'end': end_string, 'color': color_string,
                             'prize_of_activity_array': prize_array,'now_participate_number': e.ConditionNum}
        activity_array.append(dict_activity)
    return JsonResponse(activity_array, safe=False)

def return_personal_create_info(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    activities = Activity.objects.filter(sponsor=user)
    activity_array = []
    end_string = ''
    for e in activities:
        prizes = e.prize_set.all()
        prize_array = []
        for f in prizes:
            dict_prize = {'prize_name': f.PrizeName, 'prize_num': f.PrizeNumber}
            prize_array.append(dict_prize)
        if e.ActivityPhoto == '':
            activity_photo = str(e.ActivityPhoto)
        else:
            activity_photo = str(e.prize_set.all()[0].PrizePhoto)
        if e.ActivityEnd == False:
            end_string = '[进行中]'
            color_string = '#64DD17'

        else:
            end_string = '[已结束]'
            color_string = '#E57373'
        if e.ConditionType == 0:
            dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo,
                             'activity_sponsor': e.SponsorNickName, 'condition_type': '按时间开奖',
                             'info': str(e.EndTime)[:-3], 'end': end_string, 'color': color_string,
                             'prize_of_activity_array': prize_array,
                             'now_participate_number': e.ConditionNum}  # str(e.EndTime)[:-3]:将datetime类型转为字符串
        elif e.ConditionType == 1:
            dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo,
                             'activity_sponsor': e.SponsorNickName, 'condition_type': '按人数开奖',
                             'info': '满' + str(e.ConditionInfo) + '人开奖', 'end': end_string, 'color': color_string,
                             'prize_of_activity_array': prize_array, 'now_participate_number': e.ConditionNum}
        elif e.ConditionType == 2:
            dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo,
                             'activity_sponsor': e.SponsorNickName, 'condition_type': '发起人手动开奖',
                             'info': '', 'end': end_string, 'color': color_string,
                             'prize_of_activity_array': prize_array, 'now_participate_number': e.ConditionNum}
        activity_array.append(dict_activity)
    return JsonResponse(activity_array, safe=False)

def return_personal_win_info(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    end_string = ''
    activities = Activity.objects.filter(winner=user)
    activity_array = []
    for e in activities:
        prizes = e.prize_set.all()
        prize_array = []
        for f in prizes:
            dict_prize = {'prize_name': f.PrizeName, 'prize_num': f.PrizeNumber}
            prize_array.append(dict_prize)
        if e.ActivityPhoto == '':
            activity_photo = str(e.ActivityPhoto)
        else:
            activity_photo = str(e.prize_set.all()[0].PrizePhoto)
        if e.ActivityEnd == False:
            end_string = '[进行中]'
            color_string = '#64DD17'
        else:
            end_string = '[已结束]'
            color_string = '#E57373'
        if e.ConditionType == 0:
            dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo,
                             'activity_sponsor': e.SponsorNickName, 'condition_type': '按时间开奖',
                             'info': str(e.EndTime)[:-3], 'end': end_string, 'color': color_string,
                             'prize_of_activity_array': prize_array,
                             'now_participate_number': e.ConditionNum}  # str(e.EndTime)[:-3]:将datetime类型转为字符串
        elif e.ConditionType == 1:
            dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo,
                             'activity_sponsor': e.SponsorNickName, 'condition_type': '按人数开奖',
                             'info': '满' + str(e.ConditionInfo) + '人开奖', 'end': end_string, 'color': color_string,
                             'prize_of_activity_array': prize_array, 'now_participate_number': e.ConditionNum}
        elif e.ConditionType == 2:
            dict_activity = {'activity_id': e.id, 'activity_photo': activity_photo,
                             'activity_sponsor': e.SponsorNickName, 'condition_type': '发起人手动开奖',
                             'info': '', 'end': end_string, 'color': color_string,
                             'prize_of_activity_array': prize_array, 'now_participate_number': e.ConditionNum}
        activity_array.append(dict_activity)
    return JsonResponse(activity_array, safe=False)
