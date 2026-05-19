from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/scan-rfid/', views.scan_rfid, name='scan_rfid'),
    path('api/start-sesi/', views.start_sesi, name='start_sesi'),
    path('api/scan-tong/', views.scan_tong, name='scan_tong'),
    path('api/submit-sesi/', views.submit_sesi, name='submit_sesi'),
]