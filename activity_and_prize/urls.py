from django.urls import path

from . import views

urlpatterns = [
    path('get_activity_info', views.get_activity_info, name='get_activity_info'),
    path('return_index_activity_main_info', views.return_index_activity_main_info, name='return_index_activity_main_info'),
    path('return_selfhelp_activity_main_info', views.return_selfhelp_activity_main_info, name='return_selfhelp_activity_main_info'),
    path('create_image_url/<path:imagepath>', views.return_image, name='create_image_url'),
    path('return_activity_info', views.return_activity_info, name='return_activity_info'),
    path('participate_activity', views.participate_activity, name='participate_activity'),
    path('participate_activity_by_share', views.participate_activity_by_share, name='participate_activity_by_share'),
    path('return_personal_paticipate_info', views.return_personal_paticipate_info ,name='return_personal_paticipate_info'),
    path('return_personal_create_info', views.return_personal_create_info ,name='return_personal_create_info'),
    path('return_personal_win_info', views.return_personal_win_info, name='return_personal_win_info'),
    path('test_message', views.test_message, name='test_message'),
    path('return_qiniu_upload_token', views.return_qiniu_upload_token, name='return_qiniu_upload_token'),
    path('get_qiniu_info', views.get_qiniu_info, name='get_qiniu_info'),
    #path('', views., name=''),
]

#http://127.0.0.1:8000/activity_and_prize/create_image_url//Users/apple/PycharmProjects/luckyDraw--WeChatAppletRear-End/media/uploadfile/2019/10/31/richtext_richtext__wx6ac3ca8cc6189b5b.o6zAJs-4EoVuB_dbionVOX2wp3x8.n5taKJeFOKJP2457b75be1163444072681dd518a1d83.png
#https://www.luckydraw.net.cn/activity_and_prize/create_image_url//home/luckyDraw/media/uploadfile/2019/10/31/richtext_richtext__wx6ac3ca8cc6189b5b.o6zAJs-4EoVuB_dbionVOX2wp3x8.WOKdbwH6NBaz2457b75be1163444072681dd518a1d83.png