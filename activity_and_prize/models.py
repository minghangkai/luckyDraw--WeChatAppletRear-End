from django.db import models
from django_mysql.models import JSONField
from user.models import User
from django.utils.html import format_html
# Create your models here.
class Activity(models.Model):
    sponsor               = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='sponsor', blank=True) #连接用户表
    certificate	  = models.BooleanField('活动创建人是否认证', default=False, null=True, blank=True)   # 活动创建人是否认证
    SponsorWay	          = models.SmallIntegerField('活动创建方式', default=1, null=True, blank=True)  # 活动创建方式：快速、高级、公众号、转盘
    ActivityName	      = models.CharField('活动名称', max_length=60, null=True, blank=True)  # 活动名称
    ActivityPhoto	      = models.ImageField('活动头图', upload_to='uploadfile/%Y/%m/%d/', max_length=255, null=True, blank=True) # 活动头图
    ActivityDetails	      = JSONField('活动介绍', null=True, blank=True)    # 活动介绍
    StartTime             = models.DateTimeField('活动开始时间', auto_now=True, null=True, blank=True)  # 活动开始时间
    EndTime               = models.DateTimeField('活动结束时间', null=True, blank=True) # 活动结束时间
    ConditionType         = models.PositiveSmallIntegerField('开奖条件', default=1, null=True, blank=True)  # 开奖条件
    ConditionInfo	      = models.PositiveIntegerField('存总人数', default=1, null=True, blank=True) # 存总人数
    ConditionNum          = models.PositiveIntegerField('存现有人数', default=0, null=True, blank=True) # 存现有人数
    SponsorPhoneNumber	  = models.CharField('活动创建人电话号码', max_length=20, null=True, blank=True)  # 活动创建人电话号码
    SponsorNickName	      = models.CharField('活动创建人名称', max_length=40, null=True, blank=True)  # 活动创建人名称
    SponsorWechatNumber	  = models.CharField('活动创建人微信号', max_length=255, null=True, blank=True)  # 活动创建人微信号
    ParticipantAttention  = models.BooleanField('活动参与者关注（快速）', default=False, null=True, blank=True)  # 活动参与者关注（快速）
    ShareJurisdiction	  = models.BooleanField('活动能否分享（快速、高级）', default=False, null=True, blank=True)  # 活动能否分享（快速、高级）
    AllowQuitOrNot	      = models.BooleanField('是否能退出活动（高级、公众号）', default=False, null=True, blank=True)   # 是否能退出活动（高级、公众号）
    InviateFriends	      = models.BooleanField('是否能邀请好友（快速、高级）', default=False, null=True, blank=True)   # 是否能邀请好友（快速、高级）
    InputCommandOrNot	  = models.BooleanField('是否输入指令才能参加活动（高级）', default=False, null=True, blank=True)   # 是否输入指令才能参加活动（高级）
    ParticipateWay	      = models.BooleanField('活动参与途径（公众号）', default=False, null=True, blank=True)   # 活动参与途径（公众号）
    WinnerList            = models.BooleanField('显示中奖者名单（转盘）', default=False, null=True, blank=True)   # 显示中奖者名单（转盘）
    ParticipantDrawNumber = models.PositiveSmallIntegerField('参与者的抽奖次数（转盘）', default=1, null=True, blank=True)  # 参与者的抽奖次数（转盘）
    participate = models.ManyToManyField('user.User', related_name='participate', blank=True)   # 活动参与者，连接用户表
    OfficialAccountsName = models.CharField('需要关注的公众号名称', max_length=40, null=True, blank=True)   # 需要关注的公众号名称（公众号，但新版本已经取消）
    KindOfAcitivity = models.SmallIntegerField('活动奖品种类', default=0, null=True, blank=True)  # 活动奖品种类
    ActivityEnd = models.BooleanField('活动是否结束', default=False, null=True, blank=True)  # 活动是否结束

    def __str__(self):
        return self.ActivityName


class Prize(models.Model):
    PrizePhoto         = models.ImageField('奖品图片', upload_to='uploadfile/%Y/%m/%d/', max_length=255, null=True)
    PrizeName          = models.CharField('奖品名称', max_length=60, null=True)
    PrizeNumber	       = models.PositiveSmallIntegerField('奖品数量', default=1, null=True)
    WinningProbability = models.DecimalField('中奖概率', max_digits=6,decimal_places=3, null=True)
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, default=1, null=True)  # 连接奖品表

    def __str__(self):
        return self.PrizeName