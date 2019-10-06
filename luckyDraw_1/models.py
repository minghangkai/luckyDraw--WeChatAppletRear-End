from django.db import models
from django_mysql.models import JSONField
# Create your models here.
class User(models.Model):
    openid      = models.CharField(db_index=True, max_length=100, default='0', null=True)
    username    = models.CharField(max_length=40, null=True)
    avatarUrl   = models.URLField(max_length=255, null=True)
    gender      = models.PositiveSmallIntegerField(default=0, null=True)
    country     = models.CharField(max_length=40, null=True)
    province    = models.CharField(max_length=40, null=True)
    city        = models.CharField(max_length=40, null=True)
    language    = models.CharField(max_length=40, null=True)
    contactName = models.CharField(max_length=60, null=True)
    phoneNumber = models.CharField(max_length=20, null=True)
    address     = models.CharField(max_length=255, null=True)
    certificate = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.username


class Activity(models.Model):
    sponsor               = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sponsor') #连接用户表
    certificateOrNot	  = models.BooleanField(default=False, null=True)
    sponsorWay	          = models.SmallIntegerField(default=1, null=True)
    activityName	      = models.CharField(max_length=60, null=True)
    activityPhoto	      = models.FileField(max_length=255, null=True)
    activityDetails	      = JSONField(null=True)
    startTime             = models.DateTimeField(auto_now=True, null=True)
    endTime               = models.DateTimeField(null=True)
    conditionType         = models.SmallIntegerField(default=1, null=True)
    conditionInfo	      = models.SmallIntegerField(default=1, null=True)
    sponsorPhoneNumber	  = models.CharField(max_length=20, null=True)
    sponsorNickName	      = models.CharField(max_length=40, null=True)
    sponsorWechatNumber	  = models.CharField(max_length=255, null=True)
    participantAttention  = models.BooleanField(default=False, null=True)
    shareJurisdiction	  = models.BooleanField(default=False, null=True)
    allowQuitOrNot	      = models.BooleanField(default=False, null=True)
    inviateFriends	      = models.BooleanField(default=False, null=True)
    inputCommandOrNot	  = models.BooleanField(default=False, null=True)
    participateWay	      = models.BooleanField(default=False, null=True)
    winnerList            = models.BooleanField(default=False, null=True)
    participantDrawNumber = models.PositiveSmallIntegerField(default=1, null=True)
    participate = models.ManyToManyField('User', related_name='participate')
    phoneNumber = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.activityName

class Prize(models.Model):
    prizePhoto         = models.URLField(max_length=255, null=True)
    prizeName          = models.CharField(max_length=60, null=True)
    prizeNumber	       = models.PositiveSmallIntegerField(default=1, null=True)
    winningProbability = models.DecimalField(max_digits=6,decimal_places=3, null=True)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, default=1, null=True)  # 连接奖品表

    def __str__(self):
        return self.prizeName


class Certification(models.Model):
    certificateWay	        = models.SmallIntegerField(default=1, null=True)
    unifiedSocialCreditCode	= models.CharField(max_length=18, null=True)
    legalRepresentativeName	= models.CharField(max_length=100, null=True)
    OrganizationIdPhoto	    = models.URLField(max_length=255, null=True)
    sponsorRealName	        = models.CharField(max_length=20, null=True)
    idType	                = models.PositiveSmallIntegerField(default=1, null=True)
    idNumber	            = models.CharField(max_length=18, null=True)
    phoneNumber	            = models.CharField(max_length=20, null=True)
    idPhotoPositive	        = models.URLField(max_length=255, null=True)
    idPhotoNegative         = models.URLField(max_length=255, null=True)

    def __str__(self):
        return self.sponsorRealName
