from django.urls import path
from  sui_api.views import *

urlpatterns = [
    path('getOrderByDate/',GetOrderdateView.as_view(), name='GetOrderdateView'),
    path('<path:invalid_path>', Custom404View.as_view(), name='invalid_path'),
]
