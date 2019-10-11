from django.db import models

# Create your models here.
class User(models.Model):
    OpenId      = models.CharField(db_index=True, max_length=100, default='0', null=True)   # 唯一表示微信用户的id
    UserName    = models.CharField(max_length=40, null=True)    # 用户微信名
    AvatarUrl   = models.URLField(max_length=255, null=True)    # 用户头像
    gender      = models.PositiveSmallIntegerField(default=0, null=True)    # 用户性别
    country     = models.CharField(max_length=40, null=True)  # 用户国家
    province    = models.CharField(max_length=40, null=True)  # 用户省份
    city        = models.CharField(max_length=40, null=True)  # 用户城市
    language    = models.CharField(max_length=40, null=True)  # 用户语言
    ContactName = models.CharField(max_length=60, null=True)  # 用户收货联系名称
    PhoneNumber = models.CharField(max_length=20, null=True)  # 用户收货电话号码
    address     = models.CharField(max_length=255, null=True)  # 用户收货地址
    certificate = models.BooleanField(default=False, null=True)  # 用户是否认证
    CreateActivityNum = models.PositiveSmallIntegerField(default=0, null=True)  # 用户创建的活动数
    ParticipateActivityNum = models.PositiveSmallIntegerField(default=0, null=True)  # 用户参与的活动数
    WinNum = models.PositiveSmallIntegerField(default=0, null=True)  # 用户的中奖数

    def __str__(self):
        return self.UserName