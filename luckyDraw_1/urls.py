from django.urls import path

from . import views

urlpatterns = [
    path('get_openid_session_key', views.get_openid_session_key, name='get_openid_session_key'),
    path('check_token', views.check_token, name='check_token'),
    path('getUserInfo',views.get_user_info,name='getUserInfo'), #第一个参数为route，第二个参数为view，第三个为kwargs，第四个为name
    path('storage_address', views.storage_address, name='storage_address'),
    path('upload_file', views.upload_file, name='upload_file'),
    path('get_activity_info', views.get_activity_info, name='get_activity_info'),
    path('create_image_url/<path:imagepath>', views.create_image_url, name='create_image_url'),
]