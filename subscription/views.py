from django.shortcuts import render
from .models import CVPackage

def packages_view(request):
    """Display all CV subscription packages"""
    packages = CVPackage.objects.all()
    return render(request, "subscription/packages.html", {"packages": packages})


