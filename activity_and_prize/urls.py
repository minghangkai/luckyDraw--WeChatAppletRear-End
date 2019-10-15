from django.urls import path

from . import views

urlpatterns = [
    path('upload_file_json', views.upload_file_json, name='upload_file_json'),
    path('get_activity_info', views.get_activity_info, name='get_activity_info'),
    path('get_prize_info', views.get_prize_info, name='get_prize_info'),
    path('return_activity_main_info', views.return_activity_main_info, name='return_activity_main_info'),
    path('create_image_url/<path:imagepath>', views.return_image, name='create_image_url'),
    path('return_activity_info', views.return_activity_info, name='return_activity_info'),
]