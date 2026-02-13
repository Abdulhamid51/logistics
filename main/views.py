from django.shortcuts import render, get_object_or_404
from .models import Driver

def admin_dashboard(request):
    drivers = Driver.objects.all()
    return render(request, 'main/admin_dashboard.html', {'drivers': drivers})

def driver_page(request, token):
    driver = get_object_or_404(Driver, token=token)
    return render(request, 'main/driver_page.html', {'driver': driver})
