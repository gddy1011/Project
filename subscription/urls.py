from django.urls import path
from . import views

app_name = 'subscription'

urlpatterns = [
    path("packages/", views.packages_view, name="cv-packages"),
]

