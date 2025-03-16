from django.urls import path
from .views import *

urlpatterns = [
    path('add_money/', add_money_view, name='add_money'),
    path('tracker/', tracker_view, name='tracker')
]
