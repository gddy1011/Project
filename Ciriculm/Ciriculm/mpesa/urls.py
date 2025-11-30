from django.urls import path
from .views import mpesa_pay, mpesa_callback, mpesa_status

urlpatterns = [
    path('pay/', mpesa_pay, name='mpesa_pay'),
    path('callback/', mpesa_callback, name='mpesa_callback'),
    path('status/<str:checkout_request_id>/', mpesa_status, name='mpesa_status'),
]
