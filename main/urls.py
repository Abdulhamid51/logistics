from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-driver/', views.add_driver, name='add_driver'),
    path('update-driver/<int:pk>/', views.update_driver, name='update_driver'),
    path('delete-driver/<int:pk>/', views.delete_driver, name='delete_driver'),
    path('add-cargo/<int:driver_id>/', views.add_cargo, name='add_cargo'),
    path('delete-cargo/<int:pk>/', views.delete_cargo, name='delete_cargo'),
    path('driver-history/<int:pk>/', views.driver_history, name='driver_history'),
    path('driver/<str:token>/', views.driver_page, name='driver_page'),
]
