from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('<int:package_id>/', views.checkout_view, name='checkout'),
    path('<int:package_id>/success/', views.payment_success, name='success'),
    path('<int:package_id>/failure/', views.payment_failure, name='failure'),
    path('mpesa/status/<str:checkout_request_id>/', views.mpesa_status, name='mpesa_status'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
]





