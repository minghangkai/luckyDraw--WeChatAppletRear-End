from django.db import models
from django_mysql.models import JSONField
# Create your models here.
class User(models.Model):
    openid      = models.CharField(db_index=True, max_length=100, default='0')
    token       = models.CharField(max_length=255,default='0')
    username    = models.CharField(max_length=40)
    avatarUrl   = models.URLField(max_length=255)
    gender      = models.PositiveSmallIntegerField(default=0)
    country     = models.CharField(max_length=40)
    province    = models.CharField(max_length=40)
    city        = models.CharField(max_length=40)
    language    = models.CharField(max_length=40)
    contactName = models.CharField(max_length=60)
    phoneNumber = models.CharField(max_length=20)
    address     = models.URLField(max_length=255)

    def __str__(self):
        return self.username

class Activity(models.Model):
    sponsor               = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sponsor') #连接用户表
    certificateOrNot	  = models.BooleanField(default=False)
    sponsorWay	          = models.SmallIntegerField(default=0)
    activityName	      = models.CharField(max_length=60)
    activityPhoto	      = models.URLField(max_length=255)
    prizeInfo             = models.ForeignKey('Prize', on_delete=models.CASCADE) #连接奖品表
    activityDetails	      = JSONField()
    startTime             = models.DateField(null=True)
    endTime               = models.DateField(null=True)
    conditionType         = models.SmallIntegerField(default=0, null=True)
    conditionInfo	      = models.SmallIntegerField(default=0)
    sponsorPhoneNumber	  = models.CharField(max_length=20)
    sponsorNickName	      = models.CharField(max_length=40)
    sponsorWechatNumber	  = models.CharField(max_length=255)
    participantAttention  = models.BooleanField(default=False)
    shareJurisdiction	  = models.BooleanField(default=False)
    allowQuitOrNot	      = models.BooleanField(default=False)
    inviateFriends	      = models.BooleanField(default=False)
    inputCommandOrNot	  = models.BooleanField(default=False)
    participateWay	      = models.BooleanField(default=False)
    winnerList            = models.BooleanField(default=False)
    participantDrawNumber = models.PositiveSmallIntegerField(default=1)
    participate = models.ManyToManyField('User', related_name='participate')

    def __str__(self):
        return self.activityName

class Prize(models.Model):
    prizePhoto         = models.URLField(max_length=255, null=True)
    prizeName          = models.CharField(max_length=60)
    prizeNumber	       = models.PositiveSmallIntegerField(default=0)
    winningProbability = models.DecimalField(max_digits=6,decimal_places=3)

    def __str__(self):
        return self.prizeName


class Certification(models.Model):
    certificateWay	        = models.SmallIntegerField(default=0)
    unifiedSocialCreditCode	= models.CharField(max_length=18)
    legalRepresentativeName	= models.CharField(max_length=100)
    OrganizationIdPhoto	    = models.URLField(max_length=255)
    user_id                 = models.ForeignKey('User', on_delete=models.CASCADE) #连接用户表
    sponsorRealName	        = models.CharField(max_length=20)
    idType	                = models.PositiveSmallIntegerField(default=0)
    idNumber	            = models.CharField(max_length=18)
    phoneNumber	            = models.CharField(max_length=20)
    idPhotoPositive	        = models.URLField(max_length=255)
    idPhotoNegative         = models.URLField(max_length=255)

    def __str__(self):
        return self.sponsorRealName
