from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('getUserInfo',views.getUserInfo,name='getUserInfo'), #第一个参数为route，第二个参数为view，第三个为kwargs，第四个为name
]