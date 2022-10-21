from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name="signup"),
    path('userhome',views.userhome,name='userhome'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('superadmin',views.super_admin,name='super_admin'),
    path('registration',views.registration,name='registration'),
    path('login',views.login_page,name='login_page'),
    path('logout',views.user_logout,name='user_logout'),
    path('vehicle',views.add_vehicle,name='add_vehicle'),
    path('update_vehicle/<int:pk>',views.update_vehicle,name='update_vehicle'),
    path('delete/<int:pk>',views.delete_vehicle,name='delete_vehicle'),
    path('update_vehicle_admin/<int:pk>',views.update_vehicle_admin,name='update_vehicle_admin'),
]
