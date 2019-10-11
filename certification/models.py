from django.db import models

# Create your models here.
class Certification(models.Model):
    CertificateWay	        = models.SmallIntegerField(default=1, null=True)  # 认证方式（组织、企业、公众号、个人）
    UnifiedSocialCreditCode	= models.CharField(max_length=18, null=True)  # 统一社会信用代码
    LegalRepresentativeName	= models.CharField(max_length=100, null=True)   # 法定代表人姓名
    OrganizationIdPhoto	    = models.URLField(max_length=255, null=True)    # 营业执照、单位登记证书、法人证
    SponsorRealName	        = models.CharField(max_length=20, null=True)    # 个人认证者名字
    IdType	                = models.PositiveSmallIntegerField(default=1, null=True)    # 个人证件类型
    IdNumber	            = models.CharField(max_length=18, null=True)    # 个人证件号码
    PhoneNumber	            = models.CharField(max_length=20, null=True)    # 个人手机号码
    IdPhotoPositive	        = models.URLField(max_length=255, null=True)    # 个人证件正面
    IdPhotoNegative         = models.URLField(max_length=255, null=True)    # 个人证件反面
    OrganizationName            = models.CharField(max_length=200, null=True)   # 组织名称

    def __str__(self):
        return self.SponsorRealName