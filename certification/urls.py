from django.urls import path

from . import views

urlpatterns = [
    path('get_orginization_certificate_info_positive', views.get_orginization_certificate_info_positive, name='get_orginization_certificate_info_positive'),
    path('get_orginization_certificate_info_negative', views.get_orginization_certificate_info_negative, name='get_orginization_certificate_info_negative')
]