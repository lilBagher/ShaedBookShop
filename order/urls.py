# order/urls.py
from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
	path('', views.order_list, name="order_list"),
	path('<int:id>', views.order_details, name="order_details"),
	path('shipping/', views.order_create, name="order_create"),
	path('pdf/<int:id>',views.pdf.as_view(), name="pdf"),
	path('payment/', views.fake_payment_page, name='fake_payment_page'),
	path('payment/success/', views.payment_success, name='payment_success'),
	path('payment/fail/', views.payment_fail, name='payment_fail'),
]