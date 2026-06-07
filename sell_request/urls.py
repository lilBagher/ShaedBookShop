from django.urls import path
from . import views

app_name = 'sell_request'

urlpatterns = [
    path('submit/', views.submit_sell_request, name='submit'),
    path('my-requests/', views.my_sell_requests, name='my_requests'),
    path('my-requests/<int:pk>/', views.sell_request_detail, name='detail'),
    path('my-requests/<int:pk>/delete/', views.delete_sell_request, name='delete'),
]
