from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from utils.util import get_user, create_dir_according_time
from certification.models import Certification
import datetime
from django.core import serializers

# Create your views here.

host = 'http://127.0.0.1:8000/'
# host = 'https://www.luckydraw.net.cn/'

def get_orginization_certificate_info(request):
    certificationKind = request.POST.get('certificationKind')
    print(type(certificationKind))
    print('certificationKind: ')
    print(certificationKind)
    orginizationName = request.POST.get('orginizationName')
    myFile = request.FILES.get("fileName", None)  # 获取上传的文件，如果没有文件，则默认为None
    myFile.name = '组织认证_' + orginizationName + '_' + myFile.name
    """filePath = create_dir_according_time() + '/certification/' + myFile.name
    with open(filePath, 'wb+') as f:
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
    filePath = host + 'activity_and_prize/create_image_url/' + filePath"""
    if certificationKind != 2:
        unifiedSocialCred = request.POST.get('unifiedSocialCred')
        principalName = request.POST.get('principalName')
        certification = Certification(CertificateWay=certificationKind, UnifiedSocialCreditCode=unifiedSocialCred,
                                      LegalRepresentativeName=principalName, OrganizationName=orginizationName,
                                      OrganizationIdPhoto=myFile)
        certification.save()
    else:
        unifiedSocialCred = request.POST.get('unifiedSocialCred')
        principalName = request.POST.get('principalName')
        certification = Certification(CertificateWay=certificationKind, UnifiedSocialCreditCode=unifiedSocialCred,
                                      LegalRepresentativeName=principalName, OrganizationName=orginizationName,
                                      OrganizationIdPhoto=filePath)
        certification.save()
    return HttpResponse('上传认证图片成功')
    # http://127.0.0.1:8000/activity_and_prize/create_image_url//Users/apple/PycharmProjects/luckyDraw--WeChatAppletRear-End/
    # uploadfile/2019/10/0_0wxd5230cfaaa6e5d93.o6zAJs-4EoVuB_dbionVOX2wp3x8.WOqs3IyIrEau2457b75be1163444072681dd518a1d83.png


def get_personal_certificate_info_positive(request):
    certificationKind = request.POST.get('certificationKind')
    IdType = request.POST.get('kindForCredentials')
    IdNumber = request.POST.get('credentialsNumber')
    PhoneNumber = request.POST.get('phoneNum')
    SponsorRealName = request.POST.get('realName')
    myFile = request.FILES.get("fileName", None)
    myFile.name = '认证人正面_' + SponsorRealName + '_' + myFile.name
    """filePath = create_dir_according_time() + '/certification/' + myFile.name
    with open(filePath, 'wb+') as f:
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
    #filePath = host + 'activity_and_prize/create_image_url/' + filePath
    print('filePath')
    print(filePath)
    print(type(filePath))"""
    certification = Certification(CertificateWay=certificationKind, IdType=IdType,
                                  IdNumber=IdNumber, PhoneNumber=PhoneNumber, SponsorRealName=SponsorRealName,
                                  IdPhotoPositive=myFile)
    certification.save()
    certification_id = certification.id
    print('插入正面的图片id：')
    print(certification_id)
    return HttpResponse(certification_id)

def get_personal_certificate_info_negative(request):
    SponsorRealName = request.POST.get('realName')
    print('sponsorName:')
    print(SponsorRealName)
    print(type(SponsorRealName))
    certification_id = request.POST.get('certification_id')
    print('certification_id:')
    print(certification_id)
    print(type(certification_id))
    certification_id = int(certification_id)
    print('certification_id:')
    print(certification_id)
    print(type(certification_id))
    certification = Certification.objects.get(id=certification_id)
    myFile = request.FILES.get("fileName", None)
    myFile.name = '认证人反面_' + SponsorRealName + '_' + myFile.name
    """filePath = create_dir_according_time() + '/certification/' + myFile.name
    with open(filePath, 'wb+') as f:
        # 分块写入文件
        for chunk in myFile.chunks():
            f.write(chunk)
    #filePath = host + 'activity_and_prize/create_image_url/' + filePath
    IdPhotoNegative = filePath"""
    certification.IdPhotoNegative = myFile  # IdPhotoNegative
    certification.save()
    print('插入反面的图片id：')
    print(certification.id)
    return  HttpResponse('成功上传个人证件背面')
