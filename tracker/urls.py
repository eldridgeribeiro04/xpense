from django.urls import path
from .views import *

urlpatterns = [
    path('add_money/', add_money_view, name='add_money'),
    path('tracker/', tracker_view, name='tracker'),
    path('delete/<int:pk>/', delete_product, name='delete'),
    path('update/<int:pk>/', update_product, name='update')
]
