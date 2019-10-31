# Generated by Django 2.2.6 on 2019-10-21 20:29

from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate', models.BooleanField(blank=True, default=False, null=True, verbose_name='活动创建人是否认证')),
                ('SponsorWay', models.SmallIntegerField(blank=True, default=1, null=True, verbose_name='活动创建方式')),
                ('ActivityName', models.CharField(blank=True, max_length=60, null=True, verbose_name='活动名称')),
                ('ActivityPhoto', models.ImageField(blank=True, max_length=255, null=True, upload_to='uploadfile/%Y/%m/%d/', verbose_name='活动头图')),
                ('ActivityDetails', django_mysql.models.JSONField(blank=True, default=dict, null=True, verbose_name='活动介绍')),
                ('StartTime', models.DateTimeField(auto_now=True, null=True, verbose_name='活动开始时间')),
                ('EndTime', models.DateTimeField(blank=True, null=True, verbose_name='活动结束时间')),
                ('ConditionType', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='开奖条件')),
                ('ConditionInfo', models.PositiveIntegerField(blank=True, default=1, null=True, verbose_name='存总人数')),
                ('ConditionNum', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='存现有人数')),
                ('SponsorPhoneNumber', models.CharField(blank=True, max_length=20, null=True, verbose_name='活动创建人电话号码')),
                ('SponsorNickName', models.CharField(blank=True, max_length=40, null=True, verbose_name='活动创建人名称')),
                ('SponsorWechatNumber', models.CharField(blank=True, max_length=255, null=True, verbose_name='活动创建人微信号')),
                ('ParticipantAttention', models.BooleanField(blank=True, default=False, null=True, verbose_name='活动参与者关注（快速）')),
                ('ShareJurisdiction', models.BooleanField(blank=True, default=False, null=True, verbose_name='活动能否分享（快速、高级）')),
                ('AllowQuitOrNot', models.BooleanField(blank=True, default=False, null=True, verbose_name='是否能退出活动（高级、公众号）')),
                ('InviateFriends', models.BooleanField(blank=True, default=False, null=True, verbose_name='是否能邀请好友（快速、高级）')),
                ('InputCommandOrNot', models.BooleanField(blank=True, default=False, null=True, verbose_name='是否输入指令才能参加活动（高级）')),
                ('ParticipateWay', models.BooleanField(blank=True, default=False, null=True, verbose_name='活动参与途径（公众号）')),
                ('WinnerList', models.BooleanField(blank=True, default=False, null=True, verbose_name='显示中奖者名单（转盘）')),
                ('ParticipantDrawNumber', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='参与者的抽奖次数（转盘）')),
                ('OfficialAccountsName', models.CharField(blank=True, max_length=40, null=True, verbose_name='需要关注的公众号名称')),
                ('KindOfAcitivity', models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='活动奖品种类')),
                ('ActivityEnd', models.BooleanField(blank=True, default=False, null=True, verbose_name='活动是否结束')),
            ],
        ),
        migrations.CreateModel(
            name='Prize',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PrizePhoto', models.ImageField(max_length=255, null=True, upload_to='uploadfile/%Y/%m/%d/', verbose_name='奖品图片')),
                ('PrizeName', models.CharField(max_length=60, null=True, verbose_name='奖品名称')),
                ('PrizeNumber', models.PositiveSmallIntegerField(default=1, null=True, verbose_name='奖品数量')),
                ('WinningProbability', models.DecimalField(decimal_places=3, max_digits=6, null=True, verbose_name='中奖概率')),
                ('activity', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='activity_and_prize.Activity')),
            ],
        ),
        migrations.CreateModel(
            name='InviteArray',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='activity', to='activity_and_prize.Activity', verbose_name='活动ID')),
                ('invite_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invite_1', to='user.User', verbose_name='被邀请人1')),
                ('invite_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invite_2', to='user.User', verbose_name='被邀请人2')),
                ('invite_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invite_3', to='user.User', verbose_name='被邀请人3')),
                ('invite_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invite_4', to='user.User', verbose_name='被邀请人4')),
                ('invite_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invite_5', to='user.User', verbose_name='被邀请人5')),
                ('participant', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='participant', to='user.User', verbose_name='参与者')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='participate',
            field=models.ManyToManyField(blank=True, related_name='participate', through='activity_and_prize.InviteArray', to='user.User'),
        ),
        migrations.AddField(
            model_name='activity',
            name='sponsor',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sponsor', to='user.User', verbose_name='创建者'),
        ),
        migrations.AddField(
            model_name='activity',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner', to='user.User', verbose_name='中奖者'),
        ),
    ]
