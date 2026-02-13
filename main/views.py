from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Driver, Cargo
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
import json

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main:admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main:login')

@login_required(login_url='main:login')
def admin_dashboard(request):
    drivers = Driver.objects.filter(owner=request.user).prefetch_related('cargos')
    return render(request, 'main/admin_dashboard.html', {'drivers': drivers})

@login_required(login_url='main:login')
@csrf_exempt
def add_driver(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        driver = Driver.objects.create(name=data.get('name'), owner=request.user)
        return JsonResponse({
            'status': 'success',
            'id': driver.id,
            'name': driver.name,
            'token': driver.token,
            'url': request.build_absolute_uri(f'/driver/{driver.token}/')
        })

@login_required(login_url='main:login')
@csrf_exempt
def update_driver(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        driver = get_object_or_404(Driver, pk=pk, owner=request.user)
        driver.name = data.get('name', driver.name)
        driver.status = data.get('status', driver.status)
        driver.save()
        return JsonResponse({'status': 'success'})

@login_required(login_url='main:login')
@csrf_exempt
def delete_driver(request, pk):
    if request.method == 'POST':
        driver = get_object_or_404(Driver, pk=pk, owner=request.user)
        driver.delete()
        return JsonResponse({'status': 'success'})

@login_required(login_url='main:login')
@csrf_exempt
def add_cargo(request, driver_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        driver = get_object_or_404(Driver, pk=driver_id, owner=request.user)
        cargo = Cargo.objects.create(name=data.get('name'), driver=driver)
        return JsonResponse({'status': 'success', 'id': cargo.id, 'name': cargo.name})

@login_required(login_url='main:login')
@csrf_exempt
def delete_cargo(request, pk):
    if request.method == 'POST':
        cargo = get_object_or_404(Cargo, pk=pk, driver__owner=request.user)
        cargo.delete()
        return JsonResponse({'status': 'success'})

def driver_page(request, token):
    driver = get_object_or_404(Driver, token=token)
    return render(request, 'main/driver_page.html', {'driver': driver})
