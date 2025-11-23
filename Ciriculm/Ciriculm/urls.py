from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forms.urls', namespace='forms')),
    path('subscription/', include('subscription.urls', namespace='subscription')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
]



