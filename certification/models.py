from django.db import models
from django.utils.html import format_html

# Create your models here.
class Certification(models.Model):
    CertificateWay	        = models.SmallIntegerField('认证方式', default=1, null=True, blank=True)  # 认证方式（组织、企业、公众号、个人）
    UnifiedSocialCreditCode	= models.CharField('统一社会信用代码', max_length=18, null=True, blank=True)  # 统一社会信用代码
    LegalRepresentativeName	= models.CharField('法定代表人姓名', max_length=100, null=True, blank=True)   # 法定代表人姓名
    OrganizationIdPhoto	    = models.ImageField('组织证件照', default='defaultId.png', upload_to='uploadfile/%Y/%m/%d/', max_length=400, null=True)    # 营业执照、单位登记证书、法人证
    SponsorRealName	        = models.CharField('个人认证者名字', max_length=20, null=True, blank=True)    # 个人认证者名字
    IdType	                = models.PositiveSmallIntegerField('个人证件类型', default=1, null=True, blank=True)    # 个人证件类型
    IdNumber	            = models.CharField('个人证件号码', max_length=18, null=True, blank=True)    # 个人证件号码
    PhoneNumber	            = models.CharField('个人手机号码', max_length=20, null=True, blank=True)    # 个人手机号码
    IdPhotoPositive	        = models.ImageField('个人证件正面', upload_to='uploadfile/%Y/%m/%d/', max_length=400, null=True, blank=True)    # 个人证件正面
    IdPhotoNegative         = models.ImageField('个人证件反面', upload_to='uploadfile/%Y/%m/%d/', max_length=400, null=True, blank=True)    # 个人证件反面
    OrganizationName            = models.CharField('组织名称', max_length=200, null=True, blank=True)   # 组织名称
    check = models.BooleanField('是否已经检查', default=False)  # 是否经过后台检查
    pass_check = models.BooleanField('是否认证成功', default=False) # 是否认证成功
    def OrganizationIdPhoto_data(self):
        return format_html(
            '<img src="{}" width="400px"/>',
            self.OrganizationIdPhoto.url,
        )

    def IdPhotoPositive_data(self):
        return format_html(
            '<img src="{}" width="400px"/>',
            self.IdPhotoPositive.url,
        )

    def IdPhotoNegative_data(self):
        return format_html(
            '<img src="{}" width="400px"/>',
            self.IdPhotoNegative.url,
        )

    def check_color(self):
        if self.check == False:
            color_code = 'red'
        else:
            color_code = 'green'
        return format_html(
            '<span style="color:{};">{}</span>',
            color_code,
            self.check,
        )

    def pass_check_color(self):
        if self.pass_check == False:
            color_code = 'red'
        else:
            color_code = 'green'
        return format_html(
            '<span style="color:{};">{}</span>',
            color_code,
            self.pass_check,
        )

    IdPhotoPositive_data.short_description = u'个人正面证件照显示'
    IdPhotoNegative_data.short_description = u'个人反面证件照显示'
    OrganizationIdPhoto_data.short_description = u'组织证件照显示'
    check_color.short_description = u'是否人工检查'
    pass_check_color.short_description = u'是否通过人工认证'

    def __str__(self):
        return self.SponsorRealName