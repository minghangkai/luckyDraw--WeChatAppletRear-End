from django.db import models
from django_mysql.models import JSONField
from user.models import User
# Create your models here.
class Activity(models.Model):
    sponsor               = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='sponsor') #连接用户表
    certificate	  = models.BooleanField(default=False, null=True)   # 活动创建人是否认证
    SponsorWay	          = models.SmallIntegerField(default=1, null=True)  # 活动创建方式：快速、高级、公众号、转盘
    ActivityName	      = models.CharField(max_length=60, null=True)  # 活动名称
    ActivityPhoto	      = models.FileField(max_length=255, null=True) # 活动头图
    ActivityDetails	      = JSONField(null=True)    # 活动介绍
    StartTime             = models.DateTimeField(auto_now=True, null=True)  # 活动开始时间
    EndTime               = models.DateTimeField(null=True) # 活动结束时间
    ConditionType         = models.PositiveSmallIntegerField(default=1, null=True)  # 开奖条件
    ConditionInfo	      = models.PositiveIntegerField(default=1, null=True) # 存总人数
    ConditionNum          = models.PositiveIntegerField(default=0, null=True) # 存现有人数
    SponsorPhoneNumber	  = models.CharField(max_length=20, null=True)  # 活动创建人电话号码
    SponsorNickName	      = models.CharField(max_length=40, null=True)  # 活动创建人名称
    SponsorWechatNumber	  = models.CharField(max_length=255, null=True)  # 活动创建人微信号
    ParticipantAttention  = models.BooleanField(default=False, null=True)  # 活动参与者关注（快速）
    ShareJurisdiction	  = models.BooleanField(default=False, null=True)  # 活动能否分享（快速、高级）
    AllowQuitOrNot	      = models.BooleanField(default=False, null=True)   # 是否能退出活动（高级、公众号）
    InviateFriends	      = models.BooleanField(default=False, null=True)   # 是否能邀请好友（快速、高级）
    InputCommandOrNot	  = models.BooleanField(default=False, null=True)   # 是否输入指令才能参加活动（高级）
    ParticipateWay	      = models.BooleanField(default=False, null=True)   # 活动参与途径（公众号）
    WinnerList            = models.BooleanField(default=False, null=True)   # 显示中奖者名单（转盘）
    ParticipantDrawNumber = models.PositiveSmallIntegerField(default=1, null=True)  # 参与者的抽奖次数（转盘）
    participate = models.ManyToManyField('user.User', related_name='participate')   # 活动参与者，连接用户表
    OfficialAccountsName = models.CharField(max_length=40, null=True)   # 需要关注的公众号名称（公众号，但新版本已经取消）
    KindOfAcitivity = models.SmallIntegerField(default=0, null=True)  # 活动奖品种类
    ActivityEnd = models.BooleanField(default=False, null=True)  # 活动是否结束

    def __str__(self):
        return self.ActivityName


class Prize(models.Model):
    PrizePhoto         = models.URLField(max_length=255, null=True)
    PrizeName          = models.CharField(max_length=60, null=True)
    PrizeNumber	       = models.PositiveSmallIntegerField(default=1, null=True)
    WinningProbability = models.DecimalField(max_digits=6,decimal_places=3, null=True)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, default=1, null=True)  # 连接奖品表

    def __str__(self):
        return self.PrizeName