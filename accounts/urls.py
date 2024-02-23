from django.urls import path
from . import views
from .views import admin_home
from .views import admin_login_view, admin_dashboard_view
from .views import registered_users_view
from .views import admin_logout_view

urlpatterns = [
    path('register/',views.register,name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('',views.dashboard,name='dashboard'),
    path('admin_home/', admin_home, name='admin_home'),
    path('admin_login/', admin_login_view, name='admin_login'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('registered-users/', registered_users_view, name='registered_users'),
    path('admin/logout/', admin_logout_view, name='admin_logout'),


    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('forgotPassword/',views.forgotPassword,name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetPassword/',views.resetPassword,name='resetPassword'),
   
]