from django.urls import path

from . import views

urlpatterns = [
    path('upload_file', views.upload_file, name='upload_file'),
    path('get_activity_info', views.get_activity_info, name='get_activity_info'),
    path('create_image_url/<path:imagepath>', views.return_image, name='create_image_url'),
]