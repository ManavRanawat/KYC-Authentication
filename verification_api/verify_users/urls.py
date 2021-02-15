from django.urls import path

from .views import *

urlpatterns = [
    path('passport/', PassportList.as_view()), 
    path('passport/<int:pk>/', PassportDetail.as_view()),
    path('driving_license/',Driving_LicenseList.as_view()),
    path('pancard/',PanCardList.as_view())
    
]