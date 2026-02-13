from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('driver/<str:token>/', views.driver_page, name='driver_page'),
]
