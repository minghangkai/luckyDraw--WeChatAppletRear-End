from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path, re_path
from django.views.static import serve

urlpatterns = [
    path('get_orginization_certificate_info', views.get_orginization_certificate_info, name='get_orginization_certificate_info'),
    path('get_personal_certificate_info_positive', views.get_personal_certificate_info_positive, name='get_personal_certificate_info_positive'),
    path('get_personal_certificate_info_negative', views.get_personal_certificate_info_negative, name='get_personal_certificate_info_negative'),
]