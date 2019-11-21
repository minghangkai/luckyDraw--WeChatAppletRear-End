import qiniu
import requests
from django.http import HttpResponse, JsonResponse
import json
from user.models import User
from utils.get_AccessToken import get_access_token
from utils.notification import postToUrlOfAllParticipate
from utils.util import get_user, AccessKey, SecretKey
from activity_and_prize.models import Activity, Prize, InviteArray
import datetime
from django.core import serializers

#host = 'http://127.0.0.1:8000/'
host = 'https://www.luckydraw.net.cn/'
# Create your views here.



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
            activity.ActivityPhoto = obj['srcOfHeadImage']
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
            activity.ActivityPhoto = obj['srcOfHeadImage']
            activity.ActivityDetails = obj['infoOfActivity']
            # print(type(activity.ActivityDetails))
            # print(activity.ActivityDetails)
            activity.OfficialAccountsName = obj['officialAccountsName']
            activity.SponsorWechatNumber = obj['initiatorWxNumber']
            activity.ParticipateWay = obj['participateWay']
            activity.AllowQuitOrNot = obj['allowQuitOrNot']
            activity.save()
        elif sponsorWay == 4:
            activity.ActivityPhoto = obj['srcOfHeadImage']
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
        prizeImageArray = obj['imageArray']
        prizeImageArrayLen = len(prizeImageArray)
        primary_key_of_prize = []
        for index in range(prizeImageArrayLen):
            if sponsorWay == 4:
                prize = Prize(PrizeName=prizeImageArray[index]['nameOfPrize'],
                              PrizeNumber=prizeImageArray[index]['numberOfPrize'],
                              PrizePhoto=prizeImageArray[index]['imageSrc'],
                              WinningProbability=prizeImageArray[index]['probity'],
                              activity=activity)
            else:
                prize = Prize(PrizeName=prizeImageArray[index]['nameOfPrize'],
                              PrizeNumber=prizeImageArray[index]['numberOfPrize'],
                              PrizePhoto=prizeImageArray[index]['imageSrc'],
                              activity=activity)
            prize.save()
        user.CreateActivityNum = user.CreateActivityNum + 1
        user.save()
        return HttpResponse('上传活动信息成功')


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
    activity_id = request.GET.get('activity_id') #['activity_id']
    activity = Activity.objects.get(id=activity_id)
    user_id = request.GET.get('user_id')
    haveParticipate = False
    try:
        participant = activity.participate.get(id=user_id)
    except Exception as e:
        participant = None
    if participant:
        haveParticipate = True
        print('该用户已经参加该活动\n')
    else:
        print('该用户没有参加该活动\n')
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
                        'have_participate': haveParticipate,
                        'participate_avatar_array': participate_avatar_array, 'activity_end': activity.ActivityEnd}
    """print('dict_of_activity:')
    print(type(dict_of_activity))
    dict_of_activity_json = json.dumps(dict_of_activity)"""
    # dict_of_activity_json = serializers.serialize("json", dict_of_activity)
    return JsonResponse(dict_of_activity, safe=False)
    #return  JsonResponse(dict_of_activity)


def participate_activity(request):
    obj = json.loads(request.body)
    print('participate_activity_obj:')
    print(str(obj))
    user = get_user(obj)
    activity = Activity.objects.get(id=int(obj['activity_id']))
    invite_array = InviteArray(activity=activity, participant=user)
    invite_array.save()
    user.ParticipateActivityNum = user.ParticipateActivityNum + 1
    user.save()
    return HttpResponse('用户参与活动成功')


def participate_activity_by_share(request):
    obj = json.loads(request.body)
    user = get_user(obj)
    shareUser = User.objects.get(id=int(obj['shareUserId']))
    activity = Activity.objects.get(id=int(obj['activity_id']))
    invite_array = InviteArray(activity=activity, participant=user)
    invite_array_share = InviteArray.objects.get(activity=activity, participant=shareUser)
    invite_num = invite_array_share.invite_num
    if invite_num <= 5:
        print('invite_num<=5')
        print(invite_num)
        if invite_num == 0:
            print('invite_num=0')
            invite_array_share.invite_1 = shareUser
        elif invite_num == 1:
            print('invite_num=1')
            invite_array_share.invite_2 = shareUser
        elif invite_num == 2:
            print('invite_num=2')
            invite_array_share.invite_3 = shareUser
        elif invite_num == 3:
            print('invite_num=3')
            invite_array_share.invite_4 = shareUser
        elif invite_num == 4:
            print('invite_num=4')
            invite_array_share.invite_5 = shareUser
        print('已经将用户赋予invite_n')
        invite_array_share.invite_num = invite_num + 1
        invite_array_share.save()
    invite_array.save()
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


def test_message(request):
    print('test_message函数执行')
    obj = json.loads(request.body)
    user = get_user(obj)
    print('user.id:')
    print(user.OpenId)
    activity = Activity.objects.get(id=int(obj['activity_id']))
    access_token = get_access_token()
    postToUrlOfAllParticipate(activity, user, access_token)
    return HttpResponse('finish')


def return_qiniu_upload_token(request):
    bucket = "miniprogram-luckydraw"  # 上传的空间名
    key = ""  # 上传的文件名，默认为空
    auth = qiniu.Auth(AccessKey, SecretKey)
    policy = {
        "mimeLimit": "image/*"
    }
    upToken = auth.upload_token(bucket, policy=policy)  # 生成上传凭证
    #upToken = auth.upload_token(bucket)  # 生成上传凭证
    print('upToken:')
    print(upToken)
    data = {"uptoken": upToken}
    return JsonResponse(data, safe=False)

def get_qiniu_info(request):
    print('执行get_qiniu_info函数')
    info = request.body
    print('info:')
    print(info)
    return HttpResponse('success')


def return_miniprogram_wxacode(request):
    obj = json.loads(request.body)
    activityId = str(obj['activityId'])
    shareUserId = str(obj['shareUserId'])  # 创建该活动分享的用户在数据库的主键id
    accessToken = get_access_token()
    url = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=' + accessToken
    params = {
        'scene': 'activityId:' + activityId + ',shareUserId:' + shareUserId,   # 'activityId=1&shareUserId=2',
        #'page': "pages/activityInfo/activityInfo",  # 'pages/activityInfo/activityInfo',
        'width': 100,
        'is_hyaline': True
    }
    paramsJson = json.dumps(params)
    wxacode = requests.post(url=url, data=paramsJson)  # 获得二维码图片的二进制数据
    print('type(wxacode.text)')
    print(type(wxacode.content))
    bucket = "miniprogram-luckydraw"  # 上传的空间名
    key = activityId + '_' + shareUserId + "_wxacode"  # 上传的文件名，默认为空
    auth = qiniu.Auth(AccessKey, SecretKey)
    policy = {
        "mimeLimit": "image/*"
    }
    upToken = auth.upload_token(bucket, policy=policy)  # 生成上传凭证
    ret, info = qiniu.put_data(upToken, key, wxacode.content)
    print(info)

    # assert ret['key'] == key
    # assert ret['hash'] == qiniu.etag(wxacode)
    wxacodeUrl = "https://images.luckydraw.net.cn/" + key

    return HttpResponse(wxacodeUrl)