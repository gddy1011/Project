from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('submit_cv/', views.submit_cv, name='submit_cv'),
    path('extract_cv/', views.extract_cv, name='extract_cv'),
]
