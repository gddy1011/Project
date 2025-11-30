# forms/urls.py

from django.urls import path
from . import views

app_name = 'forms'

urlpatterns = [
    # Homepage (e.g., accessed via http://127.0.0.1:8000/)
    path('', views.home, name='home'),             
    # API endpoints
    path('api/submit/cv/', views.submit_cv, name='submit_cv_api'),
    path('api/extract/cv/', views.extract_cv, name='extract_cv_api'),
]
