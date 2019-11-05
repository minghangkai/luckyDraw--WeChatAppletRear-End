from django.contrib import admin
from .models import Certification

class CertificationInfo(admin.ModelAdmin):
    #list_display 表示汇总界面显示哪些列
    list_display = ('SponsorRealName', 'CertificateWay', 'IdPhotoPositive_data', 'IdPhotoNegative_data', 'check_color', 'pass_check_color')
    search_fields = ['SponsorRealName', 'CertificateWay', 'check', 'pass_check'] #表示汇总界面可以搜索哪些列
    fieldsets = [
        ('认证方式及证件类型', {'fields': ['CertificateWay', 'IdType', 'sign1', 'sign2']}),
        ('证件照片与证件号码', {'fields': ['OrganizationName', 'UnifiedSocialCreditCode', 'LegalRepresentativeName', 'OrganizationIdPhoto_data',
                                         'SponsorRealName', 'IdNumber', 'IdPhotoPositive_data', 'IdPhotoNegative_data',
                                         'PhoneNumber', 'check', 'pass_check']}),
        ('修改图片', {'fields': ['OrganizationIdPhoto', 'IdPhotoPositive', 'IdPhotoNegative']})
    ]  #  详情页分板块来显示
    readonly_fields = ('IdPhotoPositive_data', 'IdPhotoNegative_data', 'OrganizationIdPhoto_data')  #  没有这一行详情页的图片就无法显示

admin.site.register(Certification, CertificationInfo)