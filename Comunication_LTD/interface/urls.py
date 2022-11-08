from django.urls import path

from . import views
app_name = 'interface'

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('forGotPassword', views.forGotPassword, name='forGotPassword'),
    path('register', views.register, name='register'),

]